#!/usr/bin/env python3

import argparse
import hashlib
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIR = ROOT / "scripts"
DATA_DIR = ROOT / "data"
FIXTURE_DIR = RUNTIME_DIR / "tests" / "fixtures"
REQUIRED_METRICS = (
    "routingAccuracy", "precisionAt1", "precisionAt3", "mrrAt3",
    "ndcgAt3", "negativeAbstention", "typoRecoveryAt3",
    "designSystemCoherence",
)


def precision_at_k(grades, k):
    if k <= 0:
        return 0.0
    return sum(grade > 0 for grade in grades[:k]) / k


def reciprocal_rank(grades, k=3):
    for index, grade in enumerate(grades[:k], 1):
        if grade > 0:
            return 1 / index
    return 0.0


def ndcg_at_k(grades, ideal_grades, k=3):
    def dcg(values):
        return sum((2 ** value - 1) / math.log2(index + 2)
                   for index, value in enumerate(values[:k]))

    ideal = dcg(sorted(ideal_grades, reverse=True))
    return dcg(grades) / ideal if ideal else 0.0


def _matches_identity(result, identity):
    return all(result.get(key) == value for key, value in identity.items())


def grades_for_results(results, judgments):
    grades = []
    for result in results:
        matched = [judgment.get("grade", 0) for judgment in judgments
                   if _matches_identity(result, judgment.get("identity", {}))]
        grades.append(max(matched, default=0))
    return grades


def validate_fixture(fixture, domains, stacks):
    errors = []
    if not isinstance(fixture, dict):
        return ["fixture must be an object"]
    cases = fixture.get("cases")
    if not isinstance(cases, list) or not 60 <= len(cases) <= 100:
        errors.append("cases must contain 60-100 entries")
        cases = cases if isinstance(cases, list) else []
    ids = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case must be an object")
            continue
        case_id = case.get("id")
        if case_id in ids:
            errors.append(f"duplicate case id: {case_id}")
        ids.add(case_id)
        for judgment in case.get("judgments", []):
            if judgment.get("grade") not in {1, 2}:
                errors.append(f"grade 1 or 2 required in case {case_id}")
        mode = case.get("mode")
        if mode == "domain" and case.get("domain") not in domains:
            errors.append(f"unknown domain in case {case_id}")
        if mode == "stack" and case.get("stack") not in stacks:
            errors.append(f"unknown stack in case {case_id}")
    return errors


def runtime_fingerprint():
    digest = hashlib.sha256()
    for name in ("core.py", "design_system.py", "reasoning_contract.py"):
        path = RUNTIME_DIR / name
        digest.update(name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def oracle_fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_thresholds(report, manifest):
    failures = []
    for metric, requirement in manifest.get("metrics", {}).items():
        value = report.get("metrics", {}).get(metric)
        floor = requirement.get("floor")
        if value is None or value + requirement.get("tolerance", 0) < floor:
            failures.append(f"{metric} below floor {floor}")
    for sample, minimum in manifest.get("sampleMinimums", {}).items():
        actual = report.get("samples", {}).get(sample, 0)
        if actual < minimum:
            failures.append(f"{sample} sample count {actual} below minimum {minimum}")
    report_cases = {case.get("id"): case for case in report.get("cases", [])}
    for case_id, requirement in manifest.get("lockedCases", {}).items():
        case = report_cases.get(case_id)
        if not case:
            failures.append(f"locked case missing: {case_id}")
            continue
        grades = case.get("grades", [])
        within_top = requirement.get("withinTop", 0)
        minimum = requirement.get("minimumGrade", 0)
        if not any(grade >= minimum for grade in grades[:within_top]):
            actual = case.get("actual", [])
            failures.append(f"locked case {case_id} below grade {minimum}: {actual}")
    return failures


def validate_manifest(manifest, expected_runtime=None, expected_oracle=None):
    errors = []
    required = {
        "schemaVersion", "status", "approvingMaintainer", "units",
        "splitPolicy", "runtimeFingerprint", "oracleFingerprint",
        "baselineRevision", "metrics", "sampleMinimums", "lockedCases",
        "splits",
    }
    missing = sorted(required - set(manifest)) if isinstance(manifest, dict) else sorted(required)
    if missing:
        errors.append("missing sections: " + ", ".join(missing))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("metrics"), dict):
        errors.append("missing metrics")
        return errors
    for name in REQUIRED_METRICS:
        metric = manifest["metrics"].get(name)
        if not isinstance(metric, dict) or not isinstance(metric.get("floor"), (int, float)):
            errors.append(f"missing metrics entry: {name}")
        elif not math.isfinite(metric["floor"]):
            errors.append(f"metric {name} floor must be finite")
    for name, value in manifest.get("sampleMinimums", {}).items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append(f"sample minimum {name} must be a non-negative integer")
    if expected_runtime and manifest.get("runtimeFingerprint") != expected_runtime:
        errors.append("runtimeFingerprint does not match the selected runtime")
    if expected_oracle and manifest.get("oracleFingerprint") != expected_oracle:
        errors.append("oracleFingerprint does not match the selected oracle")
    if not re.fullmatch(r"[0-9a-f]{7,40}", str(manifest.get("baselineRevision", ""))):
        errors.append("baselineRevision must be a git revision")
    return errors


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Evaluate catalog relevance fixtures")
    parser.add_argument("--fixture", default=FIXTURE_DIR / "relevance-cases.json")
    parser.add_argument("--baseline", default=FIXTURE_DIR / "relevance-baseline.json")
    parser.add_argument("--manifest", default=FIXTURE_DIR / "relevance-thresholds.json")
    args = parser.parse_args()
    fixture = _load(args.fixture)
    baseline = _load(args.baseline)
    manifest = _load(args.manifest)
    domains = fixture.get("globalNegativeApplicability", {}).get("domains", [])
    stacks = fixture.get("globalNegativeApplicability", {}).get("stacks", [])
    errors = validate_fixture(fixture, set(domains), set(stacks))
    errors.extend(validate_manifest(manifest, runtime_fingerprint(), oracle_fingerprint(args.baseline)))
    errors.extend(check_thresholds(baseline, manifest))
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("relevance contract passed")


if __name__ == "__main__":
    main()
