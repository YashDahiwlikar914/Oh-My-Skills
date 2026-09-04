#!/usr/bin/env python3

import argparse
import csv
import json
import os
import re
import sys
import tempfile
from pathlib import Path


WEIGHTS = ["thin", "light", "regular", "bold", "fill", "duotone"]


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(2)


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {path}: {error}")


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


def validate_source(icons, expected):
    if not isinstance(icons, list) or len(icons) != expected:
        fail(f"expected {expected} icons")
    names = set()
    components = set()
    for icon in icons:
        if not isinstance(icon, dict) or not icon.get("name") or not icon.get("pascal_name"):
            fail("invalid official IconEntry schema")
        name, component = icon["name"], icon["pascal_name"]
        if name in names or component in components:
            fail("duplicate official icon identity")
        names.add(name)
        components.add(component)
        alias = icon.get("alias") or {}
        if alias.get("name") in names or alias.get("pascal_name") in components:
            fail(f"alias collides with canonical icon: {alias.get('name')}")
    return icons


def validate_packages(package, react_package):
    if (package.get("name"), package.get("version")) != ("@phosphor-icons/core", "2.1.1"):
        fail("core package version must be 2.1.1")
    if (react_package.get("name"), react_package.get("version")) != ("@phosphor-icons/react", "2.1.10"):
        fail("React package version must be 2.1.10")


def validate_exports(exports, components):
    required = set(components)
    if not isinstance(exports, dict) or not required <= set(exports.get("client", [])) or not required <= set(exports.get("ssr", [])):
        fail("React exports missing canonical icon components")


def validate_curated(path, icons):
    source_components = {icon["name"]: icon["pascal_name"] for icon in icons}
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    validated = 0
    for row in rows:
        if row.get("Library") != "Phosphor":
            continue
        name = row.get("Icon Name", "")
        match = re.search(r"import\s*\{\s*([A-Za-z0-9]+)", row.get("Import Code", ""))
        if source_components.get(name) != (match.group(1) if match else ""):
            fail(f"curated icon import component does not match: {name}")
        validated += 1
    return validated


def build(args):
    icons = validate_source(read_json(args.input), args.expected_count)
    package = read_json(args.package_json)
    react_package = read_json(args.react_package_json)
    validate_packages(package, react_package)
    components = [icon["pascal_name"] for icon in icons]
    validate_exports(read_json(args.react_exports_input), components)
    curated_count = validate_curated(args.curated_csv, icons)
    manifest_icons = []
    for icon in sorted(icons, key=lambda value: value["name"]):
        categories = list(dict.fromkeys(icon.get("categories", [])))
        manifest_icons.append({
            "name": icon["name"],
            "component": icon["pascal_name"],
            "codepoint": icon.get("codepoint"),
            "categories": categories,
            "tags": icon.get("tags", []),
            "clientImport": f'import {{ {icon["pascal_name"]} }} from "@phosphor-icons/react"',
            "ssrImport": f'import {{ {icon["pascal_name"]} }} from "@phosphor-icons/react/ssr"',
        })
    manifest = {
        "schemaVersion": 1,
        "source": {
            "package": package["name"],
            "version": package["version"],
            "reactPackage": react_package["name"],
            "reactVersion": react_package["version"],
        },
        "status": "active",
        "verifiedAt": args.verified_at,
        "weights": WEIGHTS,
        "reactImports": {
            "clientModule": "@phosphor-icons/react",
            "ssrModule": "@phosphor-icons/react/ssr",
        },
        "iconCount": len(manifest_icons),
        "curatedValidatedCount": curated_count,
        "icons": manifest_icons,
    }
    atomic_write(args.output, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Refresh the pinned Phosphor icon manifest")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--package-json", type=Path, required=True)
    parser.add_argument("--react-package-json", type=Path, required=True)
    parser.add_argument("--react-exports-input", type=Path, required=True)
    parser.add_argument("--curated-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verified-at", required=True)
    parser.add_argument("--expected-count", type=int, required=True)
    args = parser.parse_args()
    build(args)


if __name__ == "__main__":
    main()
