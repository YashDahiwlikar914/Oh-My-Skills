"""Reference implementation of the scraping cascade for custom code.

The bundled scrape.py CLI covers most single-page jobs. Read this file when
the task needs the cascade embedded in a larger program, a Jupyter notebook
variant, poison-pill classification with confidence scores, or per-domain
politeness logic.

Contents:
    1. validate_public_url      SSRF guard, run before every fetch and redirect
    2. ScrapingCascade          trafilatura -> requests -> Playwright, sync
    3. PlaywrightScraperAsync   notebook-safe variant for .ipynb cells
    4. PoisonPillDetector       paywall, CAPTCHA, rate-limit, and block classification
    5. RequestManager           retries with exponential backoff
    6. PoliteRequester          per-domain randomized delays

The stop rule matters more than the code. HTTP 401, 403, or 429 means the
origin denied automated access. AccessDeniedError propagates and the cascade
stops. Never escalate to another scraper or an evasion technique past a denial.
"""

from abc import ABC, abstractmethod
from typing import Optional

import ipaddress
import random
import re
import socket
import time
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import trafilatura

#for .py files
from playwright.sync_api import sync_playwright

#for .ipynb files
import asyncio
from playwright.async_api import async_playwright

STOP_STATUS_CODES = {401, 403, 429}
MAX_REDIRECTS = 5


# 1. SSRF guard

def validate_public_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'}:
        raise ValueError('Only HTTP(S) URLs are allowed')
    if parsed.username or parsed.password or not parsed.hostname:
        raise ValueError('Credentials and missing hosts are not allowed')

    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    addresses = {
        result[4][0]
        for result in socket.getaddrinfo(parsed.hostname, port)
    }
    if not addresses or any(
        not ipaddress.ip_address(address).is_global for address in addresses
    ):
        raise ValueError('Local and private-network destinations are blocked')
    return url


def fetch_public_response(url: str, *, headers: dict,
                          timeout: int = 30) -> requests.Response:
    """Follow a small redirect chain, validating every hop before fetching."""
    current_url = url
    for _ in range(MAX_REDIRECTS + 1):
        current_url = validate_public_url(current_url)
        response = requests.get(
            current_url,
            headers=headers,
            timeout=timeout,
            allow_redirects=False,
        )
        if response.status_code in STOP_STATUS_CODES:
            response.close()
            raise AccessDeniedError('The origin denied automated access')
        if response.is_redirect:
            location = response.headers.get('Location')
            response.close()
            if not location:
                raise ValueError('Redirect response has no Location header')
            current_url = urljoin(current_url, location)
            continue
        response.raise_for_status()
        return response
    raise ValueError('Redirect limit exceeded')


class AccessDeniedError(RuntimeError):
    """The origin denied access; do not escalate to another scraper."""


# 2. Sync cascade

class ScrapingResult:
    def __init__(self, content: str, title: str, method: str):
        self.content = content
        self.title = title
        self.method = method  # Track which method succeeded


class Scraper(ABC):
    @abstractmethod
    def fetch(self, url: str) -> Optional[ScrapingResult]: ...


class TrafilaturaScraper(Scraper):
    """Fast, lightweight extraction for standard articles."""

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            response = fetch_public_response(
                url,
                headers={'User-Agent': 'ResearchScraper/1.0 (+https://example.org/contact)'},
                timeout=30,
            )
            downloaded = response.text

            content = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=True,
                favor_recall=True
            )

            if not content or len(content) < 100:
                return None

            # Extract title separately
            soup = BeautifulSoup(downloaded, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text() if title else ''

            return ScrapingResult(content, title_text, 'trafilatura')
        except AccessDeniedError:
            raise
        except Exception:
            return None


class RequestsScraper(Scraper):
    """HTTP extraction with a descriptive, stable user agent."""

    USER_AGENT = 'ResearchScraper/1.0 (+https://example.org/contact)'

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        headers = {
            'User-Agent': self.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        try:
            response = fetch_public_response(url, headers=headers, timeout=30)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script/style elements
            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()

            # Find main content
            main = soup.find('main') or soup.find('article') or soup.find('body')
            content = main.get_text(separator='\n', strip=True) if main else ''

            title = soup.find('title')
            title_text = title.get_text() if title else ''

            if len(content) < 100:
                return None

            return ScrapingResult(content, title_text, 'requests')
        except AccessDeniedError:
            raise
        except Exception:
            return None


class PlaywrightScraper(Scraper):
    """JavaScript rendering for an authorized public page."""

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            url = validate_public_url(url)
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='ResearchScraper/1.0 (+https://example.org/contact)'
                )
                page = context.new_page()

                def allow_public_route(route):
                    try:
                        validate_public_url(route.request.url)
                    except (OSError, ValueError):
                        route.abort('blockedbyclient')
                        return
                    route.continue_()

                page.route('**/*', allow_public_route)
                response = page.goto(url, wait_until='networkidle', timeout=60000)
                if response and response.status in STOP_STATUS_CODES:
                    raise AccessDeniedError('The origin denied automated access')
                validate_public_url(page.url)

                # Wait for content to load
                page.wait_for_timeout(2000)

                # Extract content
                content = page.evaluate('''() => {
                    const article = document.querySelector('article, main, .content, #content');
                    return article ? article.innerText : document.body.innerText;
                }''')

                title = page.title()

                browser.close()

                if len(content) < 100:
                    return None

                return ScrapingResult(content, title, 'playwright')
        except AccessDeniedError:
            raise
        except Exception:
            return None


class ScrapingCascade:
    """Try multiple scrapers in order until one succeeds."""

    def __init__(self):
        self.scrapers = [
            TrafilaturaScraper(),
            RequestsScraper(),
            PlaywrightScraper(),
        ]

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        for scraper in self.scrapers:
            result = scraper.fetch(url)
            if result:
                return result
        return None


# 3. Notebook variant

class PlaywrightScraperAsync:
    """Async Playwright scraper for Jupyter notebooks (.ipynb files).

    Jupyter notebooks run their own event loop, so sync Playwright won't work.
    Use this async version with `await` in notebook cells.
    """

    async def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            url = validate_public_url(url)
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='ResearchScraper/1.0 (+https://example.org/contact)'
                )
                page = await context.new_page()

                async def allow_public_route(route):
                    try:
                        validate_public_url(route.request.url)
                    except (OSError, ValueError):
                        await route.abort('blockedbyclient')
                        return
                    await route.continue_()

                await page.route('**/*', allow_public_route)
                response = await page.goto(url, wait_until='networkidle', timeout=60000)
                if response and response.status in STOP_STATUS_CODES:
                    raise AccessDeniedError('The origin denied automated access')
                validate_public_url(page.url)

                # Wait for content to load
                await page.wait_for_timeout(2000)

                # Extract content
                content = await page.evaluate('''() => {
                    const article = document.querySelector('article, main, .content, #content');
                    return article ? article.innerText : document.body.innerText;
                }''')

                title = await page.title()

                await browser.close()

                if len(content) < 100:
                    return None

                return ScrapingResult(content, title, 'playwright_async')
        except AccessDeniedError:
            raise
        except Exception:
            return None

# Usage in Jupyter notebook cells:
# scraper = PlaywrightScraperAsync()
# result = await scraper.fetch('https://example.com')


# 4. Poison pill classification

class PoisonPillType(Enum):
    PAYWALL = 'paywall'
    CAPTCHA = 'captcha'
    RATE_LIMIT = 'rate_limit'
    CLOUDFLARE = 'cloudflare'
    LOGIN_REQUIRED = 'login_required'
    NOT_FOUND = 'not_found'
    NONE = 'none'


@dataclass
class PoisonPillResult:
    detected: bool
    type: PoisonPillType
    confidence: float
    details: str


class PoisonPillDetector:
    PATTERNS = {
        PoisonPillType.PAYWALL: [
            r'subscribe to continue',
            r'subscription required',
            r'become a member',
            r'sign up to read',
            r"you've reached your limit",
            r'article limit reached',
        ],
        PoisonPillType.CAPTCHA: [
            r'verify you are human',
            r'captcha',
            r'robot verification',
            r"prove you're not a robot",
        ],
        PoisonPillType.RATE_LIMIT: [
            r'too many requests',
            r'rate limit exceeded',
            r'slow down',
            r'429',
        ],
        PoisonPillType.CLOUDFLARE: [
            r'checking your browser before accessing',
            r'cloudflare ray id',
            r'performance & security by cloudflare',
        ],
        PoisonPillType.LOGIN_REQUIRED: [
            r'sign in to continue',
            r'log in required',
            r'create an account',
        ],
    }

    PAYWALL_DOMAINS = {
        'nytimes.com': PoisonPillType.PAYWALL,
        'wsj.com': PoisonPillType.PAYWALL,
        'washingtonpost.com': PoisonPillType.PAYWALL,
        'ft.com': PoisonPillType.PAYWALL,
        'bloomberg.com': PoisonPillType.PAYWALL,
    }

    def detect(self, url: str, content: str, status_code: int = 200) -> PoisonPillResult:
        # Check status code
        if status_code == 429:
            return PoisonPillResult(True, PoisonPillType.RATE_LIMIT, 1.0, 'HTTP 429')
        if status_code == 403:
            return PoisonPillResult(True, PoisonPillType.CLOUDFLARE, 0.8, 'HTTP 403')
        if status_code == 404:
            return PoisonPillResult(True, PoisonPillType.NOT_FOUND, 1.0, 'HTTP 404')

        # Check known paywall domains
        domain = urlparse(url).netloc.replace('www.', '')
        for paywall_domain, pill_type in self.PAYWALL_DOMAINS.items():
            if paywall_domain in domain:
                # Check if content is suspiciously short (paywall truncation)
                if len(content) < 500:
                    return PoisonPillResult(True, pill_type, 0.9, f'Short content from {domain}')

        # Pattern matching
        content_lower = content.lower()
        for pill_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    return PoisonPillResult(True, pill_type, 0.7, f'Pattern match: {pattern}')

        return PoisonPillResult(False, PoisonPillType.NONE, 0.0, '')


# 5. Retries with backoff

class RequestManager:
    def __init__(self):
        self.session = requests.Session()

    def get_headers(self) -> dict:
        return {
            'User-Agent': 'ResearchScraper/1.0 (+https://example.org/contact)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
        }

    def fetch(self, url: str, retry_count: int = 3) -> requests.Response:
        url = validate_public_url(url)
        for attempt in range(retry_count):
            try:
                response = self.session.get(
                    url,
                    headers=self.get_headers(),
                    timeout=30,
                    allow_redirects=False
                )
                if response.is_redirect:
                    raise ValueError(
                        'Redirect target must be validated before fetching'
                    )
                response.raise_for_status()
                return response
            except requests.RequestException:
                if attempt == retry_count - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff


# 6. Per-domain politeness

class PoliteRequester:
    def __init__(self, min_delay: float = 1.0, max_delay: float = 3.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_per_domain = {}

    def wait_for_domain(self, url: str):
        domain = urlparse(url).netloc
        last_request = self.last_request_per_domain.get(domain, 0)

        elapsed = time.time() - last_request
        delay = random.uniform(self.min_delay, self.max_delay)

        if elapsed < delay:
            time.sleep(delay - elapsed)

        self.last_request_per_domain[domain] = time.time()
