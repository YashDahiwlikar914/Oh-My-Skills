#!/usr/bin/env python3

import csv
import json
import re
from pathlib import Path

from core import DATA_DIR, search


RULES_FILE = DATA_DIR / "experience-rules.json"
TAXONOMY_FILES = {
    "website_type": "website-types.csv",
    "design_language": "design-languages.csv",
    "layout_structure": "layout-structures.csv",
}
TAXONOMY_DOMAINS = {
    "website_type": "website-types",
    "design_language": "design-languages",
    "layout_structure": "layout-structures",
}


def _load_rules():
    with RULES_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def _tokens(value):
    return set(re.findall(r"[a-z0-9]+", str(value or "").casefold()))


def _read_rows(filename):
    with (DATA_DIR / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _find_requested(domain, requested, query):
    rows = _read_rows(TAXONOMY_FILES[domain])
    requested_tokens = _tokens(requested)
    if requested_tokens:
        for row in rows:
            identities = _tokens(row.get("ID")) | _tokens(row.get("Name")) | _tokens(row.get("Family"))
            if requested_tokens <= identities and row.get("Status") == "active":
                return row
        return {}
    result = search(query, domain=TAXONOMY_DOMAINS[domain], max_results=1)
    return result.get("results", [{}])[0] if result.get("results") else {}


def _verified_ingredient(domain, requested, query):
    row = _find_requested(domain, requested, query)
    if not row or row.get("Status") != "active":
        return {"status": "unmatched", "requested": requested or "", "row": {}}
    return {
        "status": "verified",
        "id": row.get("ID", ""),
        "name": row.get("Name", ""),
        "sources": row.get("Sources", ""),
        "row": row,
    }


def _select_rule(query):
    lowered = str(query or "").casefold()
    rules = _load_rules().get("rules", [])
    matches = []
    for rule in rules:
        matched_signals = [signal for signal in rule["signals"] if signal in lowered]
        if matched_signals:
            matches.append((len(matched_signals), rule, matched_signals))
    if not matches:
        default = _load_rules()["default"]
        return default, [], []
    _, rule, signals = max(matches, key=lambda value: value[0])
    return rule, [rule["id"]], signals


def compose_experience(query, website_type=None, design_language=None, layout_structure=None):
    rule, activated_rules, matched_signals = _select_rule(query)
    requested = {
        "website_type": website_type,
        "design_language": design_language,
        "layout_structure": layout_structure,
    }
    ingredients = {
        domain: _verified_ingredient(domain, value, query)
        for domain, value in requested.items()
    }
    source_ingredients = [
        {
            "kind": domain.replace("_", "-"),
            "id": ingredient.get("id", ""),
            "name": ingredient.get("name", ""),
            "sources": ingredient.get("sources", ""),
            "status": ingredient["status"],
        }
        for domain, ingredient in ingredients.items()
        if ingredient["status"] == "verified"
    ]
    generated_inputs = [value for value in requested.values() if value]
    generated_plan = {
        "experience_level": rule["experienceLevel"],
        "reason": rule["reason"],
        "constraints": list(rule["constraints"]),
        "fallback": rule["fallback"],
        "matched_signals": matched_signals,
    }
    return {
        "status": "generated",
        "experience_level": rule["experienceLevel"],
        "activated_rules": activated_rules,
        "ingredients": ingredients,
        "source_ingredients": source_ingredients,
        "generated_inputs": generated_inputs,
        "generated_plan": generated_plan,
    }


def format_experience(result):
    lines = ["## Experience Recommendation", "", f"- Level: {result['experience_level']}"]
    if result["activated_rules"]:
        lines.append(f"- Rules: {', '.join(result['activated_rules'])}")
    lines.append(f"- Status: {result['status']}")
    lines.append(f"- Reason: {result['generated_plan']['reason']}")
    lines.append("- Constraints:")
    lines.extend(f"  - {constraint}" for constraint in result["generated_plan"]["constraints"])
    lines.append(f"- Fallback: {result['generated_plan']['fallback']}")
    lines.append("- Verified ingredients:")
    for ingredient in result["source_ingredients"]:
        lines.append(f"  - {ingredient['kind']}: {ingredient['name']} [{ingredient['status']}]")
    return "\n".join(lines)
