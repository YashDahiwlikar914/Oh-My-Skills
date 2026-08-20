#!/usr/bin/env python3
"""Fetch one public URL and extract its main content, search the web,
list a page's links, or crawl a site section.

Fetch cascade order: trafilatura, requests + BeautifulSoup, Playwright.
Playwright renders JavaScript pages and runs first when --render is set.
Search uses the Bing HTML endpoint with a DuckDuckGo fallback, no API key.
Crawling is bounded, same-origin by default, and honors robots.txt.
Stop on access denial. Never escalate past a paywall or anti-bot block.
"""

from __future__ import annotations

import argparse
import base64
import ipaddress
import re
import socket
import sys
import time
import urllib.robotparser
from collections import deque
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

STOP_STATUS_CODES = {401, 403, 429}
MAX_REDIRECTS = 5
USER_AGENT = "ResearchScraper/1.0 (+https://example.org/contact)"
MIN_CONTENT = 100

POISON_PATTERNS = [
    ("paywall", r"subscribe to continue|subscription required|become a member|sign up to read|article limit reached"),
    ("captcha", r"verify you are human|captcha|robot verification|prove you're not a robot"),
    ("rate_limit", r"too many requests|rate limit exceeded|slow down"),
    ("cloudflare", r"checking your browser before accessing|cloudflare ray id|performance & security by cloudflare"),
    ("login", r"sign in to continue|log in required|create an account"),
]


class AccessDeniedError(RuntimeError):
    """The origin denied automated access. Do not try another scraper."""


class PoisonPillError(RuntimeError):
    """The response looks like a paywall, CAPTCHA, or anti-bot page."""


@dataclass
class Result:
    content: str
    title: str
    method: str


def validate_public_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP(S) URLs are allowed")
    if parsed.username or parsed.password or not parsed.hostname:
        raise ValueError("Credentials and missing hosts are not allowed")

    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        addresses = {result[4][0] for result in socket.getaddrinfo(parsed.hostname, port)}
    except OSError as exc:
        raise ValueError(f"Host lookup failed: {exc}") from exc
    if not addresses or any(not ipaddress.ip_address(a).is_global for a in addresses):
        raise ValueError("Local and private-network destinations are blocked")
    return url


def fetch_public_response(url: str, timeout: int) -> requests.Response:
    current = url
    for _ in range(MAX_REDIRECTS + 1):
        current = validate_public_url(current)
        response = requests.get(
            current,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
            allow_redirects=False,
        )
        if response.status_code in STOP_STATUS_CODES:
            response.close()
            raise AccessDeniedError(f"Origin denied automated access (HTTP {response.status_code})")
        if response.is_redirect:
            location = response.headers.get("Location")
            response.close()
            if not location:
                raise ValueError("Redirect response has no Location header")
            current = urljoin(current, location)
            continue
        response.raise_for_status()
        return response
    raise ValueError("Redirect limit exceeded")


def check_poison_pill(url: str, content: str) -> None:
    lowered = content.lower()
    for kind, pattern in POISON_PATTERNS:
        if re.search(pattern, lowered):
            raise PoisonPillError(f"Response looks like a {kind} page from {urlparse(url).netloc}")


def try_trafilatura(url: str, timeout: int) -> Result | None:
    try:
        response = fetch_public_response(url, timeout)
        text = response.text
        import trafilatura

        content = trafilatura.extract(
            text, include_comments=False, include_tables=True, favor_recall=True
        )
        if not content or len(content) < MIN_CONTENT:
            return None
        soup = BeautifulSoup(text, "html.parser")
        title_el = soup.find("title")
        title = title_el.get_text() if title_el else url
        check_poison_pill(url, content)
        return Result(content, title, "trafilatura")
    except AccessDeniedError:
        raise
    except PoisonPillError:
        raise
    except Exception:
        return None


def try_requests(url: str, timeout: int) -> Result | None:
    try:
        response = fetch_public_response(url, timeout)
        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "nav", "footer", "aside"]):
            element.decompose()
        main = soup.find("main") or soup.find("article") or soup.find("body")
        content = main.get_text(separator="\n", strip=True) if main else ""
        if len(content) < MIN_CONTENT:
            return None
        check_poison_pill(url, content)
        title_el = soup.find("title")
        title = title_el.get_text() if title_el else url
        return Result(content, title, "requests")
    except AccessDeniedError:
        raise
    except PoisonPillError:
        raise
    except Exception:
        return None


def try_playwright(url: str, timeout_ms: int, screenshot: str | None = None) -> Result | None:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}, user_agent=USER_AGENT
            )
            page = context.new_page()

            def allow_public_route(route):
                try:
                    validate_public_url(route.request.url)
                except (OSError, ValueError):
                    route.abort("blockedbyclient")
                    return
                route.continue_()

            page.route("**/*", allow_public_route)
            response = page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            if response and response.status in STOP_STATUS_CODES:
                raise AccessDeniedError(f"Origin denied automated access (HTTP {response.status})")
            validate_public_url(page.url)
            page.wait_for_timeout(2000)
            if screenshot:
                page.screenshot(path=screenshot, full_page=True)

            content = page.evaluate(
                """() => {
                    const article = document.querySelector('article, main, .content, #content');
                    return article ? article.innerText : document.body.innerText;
                }"""
            )
            title = page.title()
            browser.close()

            if len(content) < MIN_CONTENT:
                return None
            check_poison_pill(url, content)
            return Result(content, title or url, "playwright")
    except AccessDeniedError:
        raise
    except PoisonPillError:
        raise
    except Exception:
        return None


BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)


def bing_search(query: str, timeout: int) -> list[tuple[str, str, str]]:
    """Search Bing HTML endpoint without an API key. Returns title, url, snippet."""
    response = requests.get(
        "https://www.bing.com/search",
        params={"q": query, "count": 20, "mkt": "en-US", "setlang": "en", "cc": "US"},
        headers={"User-Agent": BROWSER_UA},
        timeout=timeout,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select("li.b_algo"):
        anchor = item.select_one("h2 a")
        if not anchor:
            continue
        title = anchor.get_text(strip=True)
        href = anchor.get("href") or ""
        match = re.search(r"[?&]u=([^&]+)", href)
        if match:
            raw = match.group(1)
            if raw.startswith("a1"):
                raw = raw[2:]
            try:
                url = base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)).decode("utf-8", "ignore")
            except Exception:
                url = href
        else:
            url = href
        try:
            url = validate_public_url(url)
        except ValueError:
            continue
        snippet_el = item.select_one("p")
        snippet = snippet_el.get_text(strip=True)[:300] if snippet_el else ""
        results.append((title, url, snippet))
    return results


def ddg_search(query: str, timeout: int) -> list[tuple[str, str, str]]:
    """Search the DuckDuckGo HTML endpoint without an API key. Returns title, url, snippet."""
    response = requests.post(
        "https://html.duckduckgo.com/html/",
        data={"q": query, "kl": "us-en"},
        headers={"User-Agent": BROWSER_UA},
        timeout=timeout,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select("div.result, div.web-result"):
        anchor = item.select_one("a.result__a")
        if not anchor:
            continue
        title = anchor.get_text(strip=True)
        href = anchor.get("href") or ""
        # DuckDuckGo wraps targets in /l/?uddg=<urlencoded>; recover the real URL
        match = re.search(r"[?&]uddg=([^&]+)", href)
        url = match.group(1) if match else href
        try:
            url = validate_public_url(url)
        except ValueError:
            continue
        snippet_el = item.select_one(".result__snippet")
        snippet = snippet_el.get_text(strip=True)[:300] if snippet_el else ""
        results.append((title, url, snippet))
    return results


def normalize_url(url: str) -> str:
    """Canonical form for dedup: lowercase scheme and host, no fragment, no empty query."""
    parsed = urlparse(url)
    path = parsed.path or "/"
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))


def origin_of(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}"


def extract_page_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    seen = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = urljoin(base_url, href)
        if urlparse(absolute).scheme not in ("http", "https"):
            continue
        normalized = normalize_url(absolute)
        if normalized not in seen:
            seen.add(normalized)
            links.append(normalized)
    return links


def load_robots(origin: str, timeout: int) -> urllib.robotparser.RobotFileParser | None:
    """Load robots.txt for an origin. None means the rules could not be read; allow."""
    rp = urllib.robotparser.RobotFileParser()
    try:
        response = fetch_public_response(f"{origin}/robots.txt", timeout)
        rp.parse(response.text.splitlines())
        return rp
    except AccessDeniedError:
        # The origin refuses to serve robots.txt over automated access.
        # Mirror robotparser semantics for HTTP 401/403: treat everything as disallowed.
        disallow_all = urllib.robotparser.RobotFileParser()
        disallow_all.parse(["User-agent: *", "Disallow: /"])
        return disallow_all
    except Exception:
        return None


def robots_allows(rp: urllib.robotparser.RobotFileParser | None, url: str) -> bool:
    if rp is None:
        return True
    return rp.can_fetch("*", url) and rp.can_fetch("ResearchScraper", url)


def extract_crawl_content(html: str) -> tuple[str, str]:
    """Return (content, method) using trafilatura, falling back to BeautifulSoup."""
    try:
        import trafilatura

        content = trafilatura.extract(
            html, include_comments=False, include_tables=True, favor_recall=True
        )
        if content and len(content) >= MIN_CONTENT:
            return content, "trafilatura"
    except Exception:
        pass
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "aside"]):
        element.decompose()
    main = soup.find("main") or soup.find("article") or soup.find("body")
    content = main.get_text(separator="\n", strip=True) if main else ""
    if len(content) >= MIN_CONTENT:
        return content, "requests"
    return "", "none"


def run_cascade(url: str, args: argparse.Namespace) -> int:
    timeout_ms = max(args.timeout, 30) * 1000

    screenshot = getattr(args, "screenshot", None)
    if screenshot:
        result = try_playwright(url, max(args.timeout, 60) * 1000, screenshot=screenshot)
        if result:
            content = result.content[: args.max_chars]
            print(f"# {result.title}")
            print(f"<!-- method: {result.method} source: {url} -->")
            print(content)
            print(f"<!-- screenshot: {screenshot} -->", file=sys.stderr)
            return 0
        print(f"error: screenshot failed for {url}, Playwright did not load the page", file=sys.stderr)
        return 1

    if args.method == "trafilatura":
        scrapers = [try_trafilatura]
    elif args.method == "requests":
        scrapers = [try_requests]
    elif args.method == "playwright":
        scrapers = [try_playwright]
    elif args.render_only:
        scrapers = [try_playwright]
        args.timeout = max(args.timeout, 60)
    elif args.render:
        scrapers = [try_playwright, try_trafilatura, try_requests]
    else:
        scrapers = [try_trafilatura, try_requests, try_playwright]

    for scraper in scrapers:
        if scraper is try_playwright:
            result = try_playwright(url, timeout_ms)
        else:
            result = scraper(url, args.timeout)
        if result:
            content = result.content[: args.max_chars]
            print(f"# {result.title}")
            print(f"<!-- method: {result.method} source: {url} -->")
            print(content)
            return 0

    print(f"error: all scrapers failed for {url}", file=sys.stderr)
    return 1


def search_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="scrape.py search",
        description="Search the web (Bing, with DuckDuckGo fallback) and list results",
    )
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("--max-results", type=int, default=5, help="How many results to list")
    parser.add_argument(
        "--fetch",
        type=int,
        metavar="N",
        help="After listing, fetch result N through the cascade",
    )
    parser.add_argument(
        "--engine",
        choices=["auto", "bing", "ddg"],
        default="auto",
        help="Search engine: auto tries Bing then DuckDuckGo (default: auto)",
    )
    parser.add_argument("--timeout", type=int, default=15, help="Search timeout in seconds")
    args = parser.parse_args(argv)

    query = " ".join(args.query)
    results: list[tuple[str, str, str]] = []
    errors: list[str] = []
    engine_used = None

    if args.engine in ("auto", "bing"):
        try:
            results = bing_search(query, args.timeout)
            engine_used = "bing"
        except Exception as exc:
            errors.append(f"bing: {exc}")
        if not results:
            errors.append("bing: no results")

    if (args.engine == "auto" and not results) or args.engine == "ddg":
        try:
            results = ddg_search(query, args.timeout)
            engine_used = "ddg"
        except Exception as exc:
            errors.append(f"ddg: {exc}")
        if not results:
            errors.append("ddg: no results")

    if not results:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print("error: search failed on all engines, they may be rate-limited", file=sys.stderr)
        return 1

    print(f"# Search: {query} ({engine_used})")
    for i, (title, url, snippet) in enumerate(results[: args.max_results], 1):
        print(f"{i}. {title}")
        print(f"   {url}")
        if snippet:
            print(f"   {snippet}")
        print()

    if args.fetch:
        index = args.fetch - 1
        if index < 0 or index >= len(results):
            print(f"error: result {args.fetch} does not exist", file=sys.stderr)
            return 1
        title, url, _ = results[index]
        print(f"--- fetching {title} ---")
        fetch_args = argparse.Namespace(
            url=url,
            method="auto",
            render=False,
            render_only=False,
            timeout=30,
            max_chars=200_000,
        )
        return run_cascade(url, fetch_args)
    return 0


def links_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="scrape.py links",
        description="Fetch one URL and list every link on the page, one absolute URL per line",
    )
    parser.add_argument("url", help="HTTP(S) URL to fetch")
    parser.add_argument(
        "--same-origin",
        action="store_true",
        help="Only list links that stay on the fetched page's origin",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    args = parser.parse_args(argv)

    url = validate_public_url(args.url)
    try:
        response = fetch_public_response(url, args.timeout)
    except AccessDeniedError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    links = extract_page_links(response.text, url)
    if args.same_origin:
        origin = origin_of(url)
        links = [link for link in links if origin_of(link) == origin]

    for link in links:
        print(link)
    print(f"<!-- {len(links)} links from {url} -->", file=sys.stderr)
    return 0


def crawl_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="scrape.py crawl",
        description="Bounded, polite crawl of a site section. Same-origin by default, honors robots.txt",
    )
    parser.add_argument("url", help="Seed HTTP(S) URL")
    parser.add_argument("--max-pages", type=int, default=10, help="Stop after this many fetched pages")
    parser.add_argument(
        "--max-depth", type=int, default=1, help="Link distance from the seed URL to follow"
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        metavar="REGEX",
        help="Only follow URLs matching this regex (repeatable)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="REGEX",
        help="Never follow URLs matching this regex (repeatable)",
    )
    parser.add_argument(
        "--allow-external",
        action="store_true",
        help="Follow links to other origins (off by default)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Minimum seconds between requests (raised if robots.txt demands more)",
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="Render each page with Playwright (slow; needed for JS-only sites)",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument(
        "--max-chars", type=int, default=20_000, help="Truncate each page's content to this many characters"
    )
    args = parser.parse_args(argv)

    seed = normalize_url(validate_public_url(args.url))
    seed_origin = origin_of(seed)
    includes = [re.compile(p) for p in args.include]
    excludes = [re.compile(p) for p in args.exclude]
    robots = load_robots(seed_origin, args.timeout)

    crawl_delay = 0.0
    if robots is not None:
        crawl_delay = robots.crawl_delay("*") or 0.0
    delay = max(args.delay, crawl_delay)
    if crawl_delay:
        print(f"crawl: robots.txt crawl-delay {crawl_delay}s in effect", file=sys.stderr)

    queue: deque[tuple[str, int]] = deque([(seed, 0)])
    queued = {seed}
    visited: set[str] = set()
    fetched = 0

    def url_allowed(candidate: str) -> bool:
        if excludes and any(p.search(candidate) for p in excludes):
            return False
        if includes and not any(p.search(candidate) for p in includes):
            return False
        return True

    while queue and fetched < args.max_pages:
        current, depth = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        if not robots_allows(robots, current):
            print(f"crawl: skipped {current} (disallowed by robots.txt)", file=sys.stderr)
            continue

        if fetched > 0:
            time.sleep(delay)

        try:
            if args.render:
                result = try_playwright(current, max(args.timeout, 60) * 1000)
                if result is None:
                    print(f"crawl: failed to render {current}, skipping", file=sys.stderr)
                    continue
                html = f"<html><body>{result.content}</body></html>"
                content, method = result.content, "playwright"
                links = extract_page_links(html, current)
            else:
                response = fetch_public_response(current, args.timeout)
                html = response.text
                links = extract_page_links(html, current)
                content, method = extract_crawl_content(html)
        except AccessDeniedError as exc:
            print(f"error: crawl aborted, {exc}", file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"crawl: failed to fetch {current} ({exc}), skipping", file=sys.stderr)
            continue

        if content:
            try:
                check_poison_pill(current, content)
            except PoisonPillError as exc:
                print(f"crawl: skipped {current} ({exc})", file=sys.stderr)
                continue

        fetched += 1
        print(f"## {current} (depth {depth}, {method})")
        if content:
            print(content[: args.max_chars])
        else:
            print("(no main content extracted)")
        print()

        if depth >= args.max_depth:
            continue
        for link in links:
            if link in queued or link in visited:
                continue
            if not args.allow_external and origin_of(link) != seed_origin:
                continue
            if not url_allowed(link):
                continue
            queued.add(link)
            queue.append((link, depth + 1))

    print(
        f"crawl: fetched {fetched} page(s), visited {len(visited)}, "
        f"frontier {len(queued)} (limits: max-pages {args.max_pages}, max-depth {args.max_depth})",
        file=sys.stderr,
    )
    return 0 if fetched else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        return search_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == "links":
        return links_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == "crawl":
        return crawl_main(sys.argv[2:])

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="HTTP(S) URL to fetch")
    parser.add_argument(
        "--render",
        action="store_true",
        help="Use Playwright first for JavaScript pages",
    )
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="Use only Playwright, skip the fast scrapers",
    )
    parser.add_argument(
        "--screenshot",
        metavar="PATH",
        help="Save a full-page PNG screenshot with Playwright and print the page text",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument(
        "--method",
        choices=["auto", "trafilatura", "requests", "playwright"],
        default="auto",
        help="Force one scraper instead of the cascade",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=200_000,
        help="Truncate content to this many characters",
    )
    args = parser.parse_args()

    url = validate_public_url(args.url)
    return run_cascade(url, args)


if __name__ == "__main__":
    sys.exit(main())
