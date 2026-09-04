#!/usr/bin/env python3
"""Contracts for the verified website taxonomy datasets."""

import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from core import CSV_CONFIG, search  # noqa: E402
import validate_data  # noqa: E402


class ExtendedTaxonomyTest(unittest.TestCase):
    def test_taxonomy_domains_are_registered_and_searchable(self):
        for domain, query, identity in (
            ("website-types", "government benefits eligibility", "Government"),
            ("design-languages", "Bauhaus Swiss International", "Bauhaus"),
            ("layout-structures", "editorial masonry spread", "Editorial Spread"),
        ):
            with self.subTest(domain=domain):
                self.assertIn(domain, CSV_CONFIG)
                result = search(query, domain=domain, max_results=3)
                self.assertGreater(result["count"], 0)
                text = " ".join(
                    str(value) for row in result["results"] for value in row.values()
                )
                self.assertIn(identity.casefold(), text.casefold())

    def test_unverified_candidates_do_not_appear_in_default_search(self):
        result = search("candidate experimental", domain="design-languages", max_results=20)
        self.assertTrue(all(row.get("Status") == "active" for row in result["results"]))

    def test_taxonomy_rows_have_source_and_delivery_fields(self):
        for domain, query in (
            ("website-types", "website"),
            ("design-languages", "design"),
            ("layout-structures", "layout"),
        ):
            result = search(query, domain=domain, max_results=3)
            for row in result["results"]:
                with self.subTest(domain=domain, identity=row.get("Name")):
                    self.assertEqual("active", row["Status"])
                    self.assertTrue(row["Sources"])
                    responsive_field = "Motion And Depth" if domain == "design-languages" else "Responsive Notes"
                    self.assertTrue(row[responsive_field])
                    self.assertTrue(row["Accessibility Notes"])
                    self.assertTrue(row["Anti-Patterns"])

    def test_full_validator_checks_taxonomy_and_rule_contracts(self):
        problems = validate_data.validate()
        self.assertEqual([], [problem for problem in problems if "taxonomy" in problem.lower()])
        self.assertEqual([], [problem for problem in problems if "experience-rules" in problem.lower()])

    def test_taxonomy_checker_rejects_unknown_status_and_missing_source(self):
        rows = {"website-types": [{"ID": "broken", "Name": "Broken", "Status": "draft", "Sources": ""}]}
        problems = []
        validate_data._check_taxonomy_contract(rows, problems)
        self.assertTrue(any("invalid Status" in problem for problem in problems))
        self.assertTrue(any("Sources" in problem for problem in problems))

    def test_experience_rule_checker_rejects_unknown_level(self):
        problems = []
        validate_data._check_experience_rules_contract(
            {"schemaVersion": 1, "rules": [{"id": "bad", "experienceLevel": "teleport"}]},
            problems,
        )
        self.assertTrue(any("experienceLevel" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main(verbosity=2)
