#!/usr/bin/env python3

import argparse
import csv
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus, urlsplit
from urllib.request import Request, urlopen


LICENSES = {"OFL", "APACHE2", "UFL"}
CSV_FIELDS = [
    "Family", "Category", "Stroke", "Classifications", "Keywords", "Styles",
    "Variable Axes", "Subsets", "Designers", "Popularity Rank", "Trending Rank",
    "Is Noto", "Date Added", "Last Modified", "Google Fonts URL",
]


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(2)


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {path}: {error}")


def valid_date(value):
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError):
        return False
    return date(1970, 1, 1) < parsed <= date.today()


def normalize_category(value):
    return {"sans-serif": "Sans Serif", "serif": "Serif", "monospace": "Monospace", "display": "Display", "handwriting": "Handwriting"}.get(value, str(value or "").title())


def style_sort_key(value):
    match = re.fullmatch(r"(\d+)(i)?", value)
    return (int(match.group(1)), bool(match.group(2))) if match else (9999, value)


def normalize_styles(variants):
    normalized = []
    for variant in variants:
        if variant == "regular":
            value = "400"
        elif variant == "italic":
            value = "400i"
        else:
            value = variant
        if value not in normalized:
            normalized.append(value)
    return " | ".join(sorted(normalized, key=style_sort_key))


def normalize_axes(axes):
    result = []
    seen = set()
    for axis in axes or []:
        tag = axis.get("tag")
        if tag in seen:
            fail(f"duplicate axis tags: {tag}")
        seen.add(tag)
        start = axis.get("start", axis.get("min"))
        end = axis.get("end", axis.get("max"))
        if not isinstance(tag, str) or start is None or end is None:
            fail("invalid axis definition")
        result.append(f"{tag}: {_number(start)}..{_number(end)}")
    return " | ".join(result)


def _number(value):
    return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)


def metadata_from_root(root, expected):
    found = {}
    for path in Path(root).rglob("METADATA.pb"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r'^name:\s*"([^"]+)"', text, re.MULTILINE)
        license_match = re.search(r'^license:\s*"([^"]+)"', text, re.MULTILINE)
        date_match = re.search(r'^date_added:\s*"([^"]+)"', text, re.MULTILINE)
        if match:
            found[match.group(1)] = {
                "name": match.group(1),
                "designer": re.findall(r'^designer:\s*"([^"]+)"', text, re.MULTILINE),
                "license": license_match.group(1) if license_match else "",
                "date_added": date_match.group(1) if date_match else "",
            }
    if len(found) < expected * 0.9:
        fail(f"official metadata covers fewer than 90% of families: {len(found)}/{expected}")
    return found


def validate_exclusion_source(source):
    try:
        parsed = urlsplit(source)
        has_private = bool(parsed.username or parsed.password or parsed.port)
    except ValueError:
        return False
    if parsed.scheme != "https" or has_private:
        return False
    if parsed.hostname == "fonts.google.com":
        return bool(parsed.path)
    return parsed.hostname == "github.com" and (
        parsed.path == "/google/fonts" or parsed.path.startswith("/google/fonts/")
    )


def load_family_metadata(args, count):
    if args.metadata_root:
        return metadata_from_root(args.metadata_root, count), []
    payload = read_json(args.metadata_input)
    families = payload.get("families")
    if not isinstance(families, list):
        fail("metadata families must be an array")
    excluded = payload.get("excludedFamilies", [])
    if not isinstance(excluded, list):
        fail("excludedFamilies must be an array")
    for entry in excluded:
        if not isinstance(entry, dict) or not entry.get("name") or not entry.get("reason") or not validate_exclusion_source(entry.get("source", "")):
            fail("invalid excluded family source or reason")
    return {entry.get("name"): entry for entry in families if isinstance(entry, dict)}, excluded


def load_api(args):
    if args.live:
        key = os.environ.get("GOOGLE_FONTS_API_KEY")
        if not key:
            fail("GOOGLE_FONTS_API_KEY is required for --live; use --api-input for offline CI")
        request = Request(
            "https://www.googleapis.com/webfonts/v1/webfonts?sort=popularity&key=" + quote_plus(key),
            headers={"User-Agent": "web-experience-director-font-refresh"},
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except OSError as error:
            fail(f"live Google Fonts request failed: {error}")
    if args.catalog_input:
        return read_json(args.catalog_input)
    if not args.api_input:
        fail("one of --api-input, --catalog-input, or --live is required")
    return read_json(args.api_input)


def validate_api(payload, expected):
    if payload.get("kind") != "webfonts#webfontList":
        fail("invalid API schema, expected webfonts#webfontList")
    items = payload.get("items")
    if not isinstance(items, list) or len(items) != expected:
        fail(f"expected {expected} items")
    for item in items:
        if not isinstance(item, dict) or not item.get("family") or not valid_date(item.get("lastModified")):
            fail(f"invalid or suspicious date for {item.get('family', '')}")
        if any(not isinstance(url, str) or urlsplit(url).hostname != "fonts.gstatic.com" or urlsplit(url).scheme != "https" for url in item.get("files", {}).values()):
            fail("font files must use https://fonts.gstatic.com")
        normalize_axes(item.get("axes"))
    return items


def validate_catalog(payload, expected):
    items = payload.get("familyMetadataList")
    if not isinstance(items, list) or len(items) != expected:
        fail(f"expected {expected} items")
    for item in items:
        popularity = item.get("popularity")
        if not isinstance(popularity, int) or isinstance(popularity, bool):
            fail("invalid popularity")
        normalize_axes(item.get("axes"))
    return items


def read_existing(path):
    if not Path(path).exists():
        return {}, set()
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {row.get("Family"): row for row in rows}, {row.get("Family") for row in rows}


def load_overrides(path):
    payload = read_json(path) if path else {}
    families = payload.get("families", {})
    if not isinstance(families, dict):
        fail("overrides families must be an object")
    return families


def atomic_write(path, content):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def build(args):
    for sentinel, message in (
        (".google-font-refresh.lock", "another refresh is already running"),
        (".google-font-refresh.incomplete.json", "incomplete prior refresh"),
    ):
        if (args.output_csv.parent / sentinel).exists():
            fail(message)
    payload = load_api(args)
    expected = args.expected_count
    if args.catalog_input:
        catalog_items = validate_catalog(payload, expected)
        api_items = None
        catalog = {item["family"]: item for item in catalog_items}
    else:
        api_items = validate_api(payload, expected)
        catalog = {}
    metadata, excluded = load_family_metadata(args, expected)
    existing, existing_names = read_existing(args.existing_csv)
    overrides = load_overrides(args.overrides)
    available_names = {item["family"] for item in (api_items or catalog.values())}
    if set(overrides) - available_names:
        fail("overrides target unknown families: " + ", ".join(sorted(set(overrides) - available_names)))
    excluded_names = {item["name"] for item in excluded}
    names = sorted(available_names - excluded_names)
    if set(names) != existing_names and existing_names and not args.approve_changes:
        changed = sorted(set(names) ^ existing_names)
        print("Family changes require --approve-changes: " + ", ".join(changed))
        fail("family-set changes require --approve-changes")
    rows = []
    licenses = []
    for family in names:
        api = next((item for item in api_items or [] if item["family"] == family), {})
        catalog_item = catalog.get(family, {})
        meta = metadata.get(family, {})
        license_name = meta.get("license", "")
        if license_name not in LICENSES:
            fail(f"invalid or missing official license for {family}")
        designers = meta.get("designer", [])
        if isinstance(designers, str):
            designers = [designers]
        previous = existing.get(family, {})
        row = {
            "Family": family,
            "Category": normalize_category(api.get("category", catalog_item.get("category", previous.get("Category", "")))),
            "Stroke": catalog_item.get("stroke", previous.get("Stroke", "")) or normalize_category(api.get("category", "")),
            "Classifications": " | ".join(catalog_item.get("classifications", [])),
            "Keywords": previous.get("Keywords", ""),
            "Styles": normalize_styles(api.get("variants", [])),
            "Variable Axes": normalize_axes(api.get("axes", catalog_item.get("axes", []))),
            "Subsets": " | ".join(sorted(set(api.get("subsets", catalog_item.get("subsets", []))) - {"menu"})),
            "Designers": " | ".join(designers or catalog_item.get("designers", [])),
            "Popularity Rank": _number(catalog_item.get("popularity", previous.get("Popularity Rank", ""))),
            "Trending Rank": _number(catalog_item.get("trending", previous.get("Trending Rank", ""))),
            "Is Noto": "Yes" if catalog_item.get("isNoto") else previous.get("Is Noto", "No"),
            "Date Added": meta.get("date_added", previous.get("Date Added", "")),
            "Last Modified": api.get("lastModified", previous.get("Last Modified", "")),
            "Google Fonts URL": f"https://fonts.google.com/specimen/{quote_plus(family)}",
        }
        row.update(overrides.get(family, {}))
        rows.append(row)
        licenses.append({
            "name": family,
            "license": license_name,
            "date_added": meta.get("date_added", ""),
            "designer": designers,
            "status": "active",
            "verifiedAt": args.verified_at,
        })
    report_excluded = [dict(item, status="needs-review", verifiedAt=args.verified_at) for item in excluded]
    license_payload = {
        "schemaVersion": 1,
        "source": {"repository": "https://github.com/google/fonts", "metadataFile": "METADATA.pb", "revision": args.metadata_revision},
        "familyCount": len(licenses),
        "families": licenses,
        "excludedFamilies": report_excluded,
    }
    output = []
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", delete=False) as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        handle.flush()
        handle.close()
        output = Path(handle.name).read_text(encoding="utf-8")
        Path(handle.name).unlink()
    atomic_write(args.output_csv, output)
    atomic_write(args.license_output, json.dumps(license_payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"excludedFamilies": report_excluded}, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Refresh the approved Google Fonts catalog")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--api-input", type=Path)
    parser.add_argument("--catalog-input", type=Path)
    parser.add_argument("--metadata-input", type=Path)
    parser.add_argument("--metadata-root", type=Path)
    parser.add_argument("--existing-csv", type=Path, required=True)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--license-output", type=Path, required=True)
    parser.add_argument("--verified-at", required=True)
    parser.add_argument("--metadata-revision", required=True)
    parser.add_argument("--expected-count", type=int, required=True)
    parser.add_argument("--approve-changes", action="store_true")
    args = parser.parse_args()
    build(args)


if __name__ == "__main__":
    main()
