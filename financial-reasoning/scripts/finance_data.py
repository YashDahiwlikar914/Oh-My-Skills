#!/usr/bin/env python3
"""Read-only adapters for approved public finance data sources."""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


AMFI_URL = "https://www.amfiindia.com/spages/NAVAll.txt"
MFAPI_URL = "https://api.mfapi.in/mf"
RBI_DBIE_URL = "https://data.rbi.org.in/DBIE/"
WORLD_BANK_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
SCRAPE_SCRIPT = Path(__file__).resolve().parents[2] / "web-scraping" / "scrape.py"
ALLOWED_HOSTS = {
    "api.mfapi.in",
    "api.worldbank.org",
    "data.rbi.org.in",
    "portal.amfiindia.com",
    "www.amfiindia.com",
}
MAX_RESPONSE_BYTES = 10_000_000
MAX_REDIRECTS = 5


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, newurl):
        return None


OPENER = build_opener(NoRedirect)


class SourceError(RuntimeError):
    """A source was unavailable or returned invalid data."""


def retrieved_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise SourceError("Only credential-free HTTPS URLs are allowed")
    if parsed.hostname.lower() not in ALLOWED_HOSTS:
        raise SourceError(f"Source host is not allowlisted: {parsed.hostname}")
    return url


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    current = validate_url(url)
    for _ in range(MAX_REDIRECTS + 1):
        request = Request(current, headers={"User-Agent": "financial-reasoning/1.0"})
        try:
            with OPENER.open(request, timeout=timeout) as response:
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > MAX_RESPONSE_BYTES:
                    raise SourceError("Source response exceeds the size limit")
                body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    raise SourceError("Source response exceeds the size limit")
                return body
        except HTTPError as exc:
            if 300 <= exc.code < 400:
                location = exc.headers.get("Location")
                if not location:
                    raise SourceError("Source redirect has no location") from exc
                current = validate_url(urljoin(current, location))
                continue
            if exc.code in {401, 403, 429}:
                raise SourceError(f"Source denied automated access with HTTP {exc.code}") from exc
            raise SourceError(f"Source returned HTTP {exc.code}") from exc
        except URLError as exc:
            raise SourceError(f"Source request failed: {exc.reason}") from exc
    raise SourceError("Source redirect limit exceeded")


def fetch_text(url: str, timeout: int = 30) -> str:
    return fetch_bytes(url, timeout).decode("utf-8-sig", errors="replace")


def fetch_json(url: str, timeout: int = 30):
    try:
        return json.loads(fetch_text(url, timeout))
    except json.JSONDecodeError as exc:
        raise SourceError(f"Source returned invalid JSON: {url}") from exc


def number(value, field: str) -> int | float:
    if isinstance(value, bool):
        raise SourceError(f"{field} must be numeric")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise SourceError(f"{field} must be numeric") from exc
    if not math.isfinite(parsed):
        raise SourceError(f"{field} must be finite")
    if parsed.is_integer() and isinstance(value, int):
        return int(parsed)
    return parsed


def parse_date(value: str, format_string: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"invalid date {value!r}")
    try:
        return datetime.strptime(value.strip(), format_string).date().isoformat()
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid date {value!r}") from exc


def as_iso_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError) as exc:
        raise SourceError(f"invalid ISO date {value!r}") from exc


def business_days_behind(observed_date: str, reference_date: str, holidays: set[str] | None = None) -> int:
    observed = as_iso_date(observed_date)
    reference = as_iso_date(reference_date)
    holiday_dates = {as_iso_date(value) for value in (holidays or set())}
    if observed >= reference:
        return 0
    elapsed = 0
    current = observed + timedelta(days=1)
    while current <= reference:
        if current.weekday() < 5 and current not in holiday_dates:
            elapsed += 1
        current += timedelta(days=1)
    return elapsed


def assess_freshness(
    reference_date: str | None,
    observed_date: str | None,
    holidays: set[str] | None = None,
    calendar_source: str = "weekends-only",
) -> dict:
    result = {
        "reference_date": reference_date,
        "observed_date": observed_date,
        "business_days_behind": None,
        "freshness_status": "unverified",
        "calendar_source": calendar_source if holidays is not None else "weekends-only",
        "calendar_confidence": "medium" if holidays is not None else "low",
        "warnings": [],
    }
    if not reference_date or not observed_date:
        result["warnings"].append("Freshness cannot be verified without both source dates")
        return result
    result["business_days_behind"] = business_days_behind(observed_date, reference_date, holidays)
    if result["business_days_behind"] == 0:
        result["freshness_status"] = "current"
    elif result["business_days_behind"] == 1:
        result["freshness_status"] = "delayed"
    else:
        result["freshness_status"] = "stale"
    if holidays is None:
        result["warnings"].append("No official holiday calendar was supplied; weekends-only calculation used")
    return result


def parse_world_bank(payload: list) -> list[dict]:
    if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[0], dict):
        raise SourceError("World Bank response has an unexpected shape")
    metadata, rows = payload
    if not isinstance(rows, list):
        raise SourceError("World Bank response has no data rows")
    records = []
    for row in rows:
        if not isinstance(row, dict) or row.get("value") is None:
            continue
        indicator = row.get("indicator") or {}
        country = row.get("country") or {}
        warnings = []
        if row.get("obs_status"):
            warnings.append(f"Observation status {row['obs_status']}")
        records.append({
            "source": "world-bank",
            "publisher": "World Bank",
            "dataset": indicator.get("id"),
            "series": indicator.get("value"),
            "jurisdiction": country.get("value"),
            "country_code": row.get("countryiso3code"),
            "period": row.get("date"),
            "observed_at": retrieved_at(),
            "published_at": metadata.get("lastupdated"),
            "value": number(row["value"], "value"),
            "unit": row.get("unit") or None,
            "currency": None,
            "source_reference": "api.worldbank.org",
            "source_tier": "primary",
            "confidence": "high",
            "warnings": warnings,
        })
    return records


def world_bank(country: str, indicator: str, start: str | None = None, end: str | None = None) -> list[dict]:
    if not country.isalpha() or not 2 <= len(country) <= 3:
        raise SourceError("country must be a two or three letter code")
    if not indicator.replace(".", "").replace("_", "").isalnum():
        raise SourceError("indicator contains unsupported characters")
    params = {"format": "json", "per_page": "1000"}
    if start or end:
        params["date"] = f"{start or ''}:{end or ''}"
    url = WORLD_BANK_URL.format(country=country.upper(), indicator=indicator)
    return parse_world_bank(fetch_json(f"{url}?{urlencode(params)}"))


def parse_mfapi(payload: dict, scheme_code: str) -> list[dict]:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise SourceError("MFAPI response has an unexpected shape")
    rows = payload["data"]
    meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
    invalid = 0
    records = []
    for row in rows:
        if not isinstance(row, dict):
            invalid += 1
            continue
        try:
            nav_date = parse_date(row["date"], "%d-%m-%Y")
            nav = number(row["nav"], "nav")
        except (KeyError, SourceError, ValueError):
            invalid += 1
            continue
        records.append({
            "source": "mfapi",
            "publisher": "MFAPI",
            "dataset": "Mutual Fund NAV",
            "series": meta.get("scheme_name"),
            "jurisdiction": "India",
            "scheme_code": str(scheme_code),
            "nav_date": nav_date,
            "observed_at": retrieved_at(),
            "published_at": None,
            "nav": nav,
            "value": nav,
            "unit": "INR per unit",
            "currency": "INR",
            "source_reference": f"api.mfapi.in/mf/{scheme_code}",
            "source_tier": "secondary",
            "confidence": "medium",
            "warnings": [],
        })
    if invalid:
        warning = f"{invalid} invalid MFAPI record(s) skipped"
        for record in records:
            record["warnings"].append(warning)
    return records


def mfapi_history(scheme_code: str) -> list[dict]:
    if not scheme_code.isdigit():
        raise SourceError("scheme_code must contain only digits")
    return parse_mfapi(fetch_json(f"{MFAPI_URL}/{scheme_code}"), scheme_code)


def mfapi_list(query: str | None = None) -> list[dict]:
    payload = fetch_json(MFAPI_URL)
    if not isinstance(payload, list):
        raise SourceError("MFAPI scheme list has an unexpected shape")
    lowered = query.lower() if query else None
    records = []
    for row in payload:
        if not isinstance(row, dict):
            continue
        name = str(row.get("schemeName") or row.get("scheme_name") or "")
        if lowered and lowered not in name.lower():
            continue
        records.append({
            "source": "mfapi",
            "publisher": "MFAPI",
            "dataset": "Mutual Fund Scheme List",
            "jurisdiction": "India",
            "scheme_code": str(row.get("schemeCode") or row.get("scheme_code") or ""),
            "series": name,
            "observed_at": retrieved_at(),
            "source_reference": "api.mfapi.in/mf",
            "source_tier": "secondary",
            "confidence": "medium",
            "warnings": ["Verify scheme facts against AMFI and the fund house"],
        })
    return records


def parse_amfi(feed: str) -> list[dict]:
    records = []
    malformed = 0
    for row in csv.reader(feed.splitlines(), delimiter=";"):
        if not row or not row[0].strip().isdigit():
            if row and row[0].strip() and len(row) not in {1, 8}:
                malformed += 1
            continue
        if len(row) != 8:
            malformed += 1
            continue
        try:
            nav = number(row[6], "nav")
            nav_date = parse_date(row[7], "%d-%b-%Y")
        except (SourceError, ValueError):
            malformed += 1
            continue
        records.append({
            "source": "amfi",
            "publisher": "Association of Mutual Funds in India",
            "dataset": "Mutual Fund NAV",
            "series": row[3].strip(),
            "jurisdiction": "India",
            "scheme_code": row[0].strip(),
            "isin_growth_or_payout": row[1].strip() or None,
            "isin_reinvestment": row[2].strip() or None,
            "scheme_name": row[3].strip(),
            "plan": row[4].strip(),
            "option": row[5].strip(),
            "nav_date": nav_date,
            "observed_at": retrieved_at(),
            "published_at": nav_date,
            "nav": nav,
            "value": nav,
            "unit": "INR per unit",
            "currency": "INR",
            "source_reference": AMFI_URL,
            "source_tier": "primary",
            "confidence": "high",
            "warnings": [],
        })
    if not records:
        raise SourceError("AMFI feed contained no valid NAV records")
    if malformed:
        warning = f"{malformed} malformed AMFI row(s) skipped"
        for record in records:
            record["warnings"].append(warning)
    return records


def amfi_nav(scheme_code: str | None = None, nav_date: str | None = None) -> list[dict]:
    records = parse_amfi(fetch_text(AMFI_URL))
    if scheme_code:
        records = [record for record in records if record["scheme_code"] == scheme_code]
    if nav_date:
        try:
            normalized_date = parse_date(nav_date, "%Y-%m-%d")
        except ValueError as exc:
            raise SourceError("date must use YYYY-MM-DD") from exc
        records = [record for record in records if record["nav_date"] == normalized_date]
    return records


def latest_nav_date(records: list[dict]) -> str | None:
    dates = [record.get("nav_date") for record in records if record.get("nav_date")]
    return max(dates) if dates else None


def mf_freshness(
    scheme_code: str,
    holidays: set[str] | None = None,
    calendar_source: str = "weekends-only",
) -> dict:
    amfi_records = amfi_nav(scheme_code)
    mfapi_records = mfapi_history(scheme_code)
    reference_date = latest_nav_date(amfi_records)
    observed_date = latest_nav_date(mfapi_records)
    result = assess_freshness(reference_date, observed_date, holidays, calendar_source)
    result.update({
        "scheme_code": scheme_code,
        "reference_source": "amfi",
        "observed_source": "mfapi",
        "checked_at": retrieved_at(),
    })
    if reference_date and observed_date:
        matching_amfi = next((record for record in amfi_records if record["nav_date"] == observed_date), None)
        matching_mfapi = next((record for record in mfapi_records if record["nav_date"] == observed_date), None)
        if matching_amfi and matching_mfapi:
            result["comparison"] = reconcile_mf(matching_amfi, matching_mfapi)
        else:
            result["comparison"] = None
            result["warnings"].append("No same-date AMFI and MFAPI NAV records were available")
    else:
        result["comparison"] = None
    return result


def parse_rbi_dbie(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise SourceError("RBI DBIE payload must be an object")
    required = ("dataset", "series", "period", "value", "unit")
    if any(payload.get(field) is None or payload.get(field) == "" for field in required):
        raise SourceError("RBI DBIE payload is missing required metadata")
    return {
        "source": "rbi-dbie",
        "publisher": "Reserve Bank of India",
        "dataset": payload["dataset"],
        "series": payload["series"],
        "jurisdiction": "India",
        "period": str(payload["period"]),
        "frequency": payload.get("frequency"),
        "observed_at": retrieved_at(),
        "published_at": payload.get("published_at"),
        "value": number(payload["value"], "value"),
        "unit": payload["unit"],
        "currency": payload.get("currency"),
        "source_reference": RBI_DBIE_URL,
        "source_tier": "primary",
        "confidence": "high",
        "warnings": payload.get("warnings") or [],
    }


def rbi_dbie(url: str = RBI_DBIE_URL, render: bool = False, timeout: int = 120) -> dict:
    validate_url(url)
    if not SCRAPE_SCRIPT.exists():
        raise SourceError(f"Web scraping skill not found at {SCRAPE_SCRIPT}")
    command = [sys.executable, str(SCRAPE_SCRIPT)]
    if render:
        command.append("--render")
    command.extend(["--max-chars", "100000", url])
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise SourceError("RBI DBIE scrape timed out") from exc
    if completed.returncode:
        detail = completed.stderr.strip() or "unknown scraping failure"
        raise SourceError(f"RBI DBIE scrape failed: {detail}")
    return {
        "source": "rbi-dbie",
        "publisher": "Reserve Bank of India",
        "dataset": "Database on Indian Economy",
        "series": None,
        "jurisdiction": "India",
        "observed_at": retrieved_at(),
        "published_at": None,
        "content": completed.stdout,
        "unit": None,
        "currency": None,
        "source_reference": url,
        "source_tier": "primary",
        "confidence": "high",
        "warnings": ["Extract series metadata from the returned official page before using values"],
    }


def reconcile_mf(amfi: dict, mfapi: dict, tolerance: float = 0.0001) -> dict:
    if amfi.get("scheme_code") != mfapi.get("scheme_code") or amfi.get("nav_date") != mfapi.get("nav_date"):
        raise SourceError("AMFI and MFAPI records do not identify the same scheme and date")
    difference = abs(float(amfi["nav"]) - float(mfapi["nav"]))
    warnings = []
    if difference > tolerance:
        warnings.append(f"NAV discrepancy of {difference:g} between AMFI and MFAPI")
    return {
        "scheme_code": amfi["scheme_code"],
        "nav_date": amfi["nav_date"],
        "amfi_nav": amfi["nav"],
        "mfapi_nav": mfapi["nav"],
        "difference": difference,
        "match": difference <= tolerance,
        "warnings": warnings,
    }


def output(value) -> None:
    json.dump(value, sys.stdout, ensure_ascii=True, indent=2)
    sys.stdout.write("\n")


def health() -> dict:
    checks = {}
    for name, operation in {
        "world_bank": lambda: world_bank("IND", "FP.CPI.TOTL")[:1],
        "mfapi": lambda: mfapi_history("119551")[:1],
        "amfi": lambda: amfi_nav()[:1],
        "rbi_dbie": lambda: rbi_dbie(),
    }.items():
        try:
            value = operation()
            checks[name] = {"ok": True, "records": len(value) if isinstance(value, list) else 1}
        except SourceError as exc:
            checks[name] = {"ok": False, "error": str(exc)}
    return checks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    world_bank_parser = subparsers.add_parser("world-bank")
    world_bank_parser.add_argument("--country", default="IND")
    world_bank_parser.add_argument("--indicator", required=True)
    world_bank_parser.add_argument("--start")
    world_bank_parser.add_argument("--end")

    mfapi_list_parser = subparsers.add_parser("mfapi-list")
    mfapi_list_parser.add_argument("--query")

    mfapi_parser = subparsers.add_parser("mfapi-history")
    mfapi_parser.add_argument("scheme_code")

    amfi_parser = subparsers.add_parser("amfi-nav")
    amfi_parser.add_argument("--scheme-code")
    amfi_parser.add_argument("--date")

    freshness_parser = subparsers.add_parser("mf-freshness")
    freshness_parser.add_argument("scheme_code")
    freshness_parser.add_argument("--holiday", action="append")
    freshness_parser.add_argument("--calendar-source", default="manual-official-calendar")

    rbi_parser = subparsers.add_parser("rbi-dbie")
    rbi_parser.add_argument("--url", default=RBI_DBIE_URL)
    rbi_parser.add_argument("--render", action="store_true")

    reconcile_parser = subparsers.add_parser("reconcile-mf")
    reconcile_parser.add_argument("scheme_code")
    reconcile_parser.add_argument("--date", required=True)
    reconcile_parser.add_argument("--holiday", action="append")
    reconcile_parser.add_argument("--calendar-source", default="manual-official-calendar")

    subparsers.add_parser("health")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "world-bank":
            result = world_bank(args.country, args.indicator, args.start, args.end)
        elif args.command == "mfapi-list":
            result = mfapi_list(args.query)
        elif args.command == "mfapi-history":
            result = mfapi_history(args.scheme_code)
        elif args.command == "amfi-nav":
            result = amfi_nav(args.scheme_code, args.date)
        elif args.command == "mf-freshness":
            result = mf_freshness(args.scheme_code, set(args.holiday) if args.holiday else None, args.calendar_source)
        elif args.command == "rbi-dbie":
            result = rbi_dbie(args.url, args.render)
        elif args.command == "reconcile-mf":
            amfi_all = amfi_nav(args.scheme_code)
            mfapi_all = mfapi_history(args.scheme_code)
            amfi_records = [record for record in amfi_all if record["nav_date"] == args.date]
            mfapi_records = [record for record in mfapi_all if record["nav_date"] == args.date]
            freshness = assess_freshness(
                latest_nav_date(amfi_all),
                latest_nav_date(mfapi_all),
                set(args.holiday) if args.holiday else None,
                args.calendar_source,
            )
            if not amfi_records or not mfapi_records:
                amfi_dates = sorted({record["nav_date"] for record in amfi_all}, reverse=True)
                mfapi_dates = sorted({record["nav_date"] for record in mfapi_all}, reverse=True)
                result = {
                    "scheme_code": args.scheme_code,
                    "requested_date": args.date,
                    "match": None,
                    "difference": None,
                    "freshness": freshness,
                    "warnings": [
                        "No matching AMFI and MFAPI records were found",
                        f"Latest AMFI date {amfi_dates[0] if amfi_dates else 'unavailable'}",
                        f"Latest MFAPI date {mfapi_dates[0] if mfapi_dates else 'unavailable'}",
                    ],
                }
            else:
                result = reconcile_mf(amfi_records[0], mfapi_records[0])
                result["freshness"] = freshness
        else:
            result = health()
    except SourceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    output(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
