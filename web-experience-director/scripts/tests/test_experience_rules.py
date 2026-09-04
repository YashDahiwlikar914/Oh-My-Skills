#!/usr/bin/env python3
"""Behavior contracts for verified ingredients and generated combinations."""

import sys
import unittest
import json
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from experience_rules import compose_experience  # noqa: E402
from design_system import DesignSystemGenerator, format_markdown  # noqa: E402


class ExperienceRulesTest(unittest.TestCase):
    def test_routine_dashboard_does_not_escalate_to_three_d(self):
        result = compose_experience(
            "personal finance dashboard with balances and monthly charts"
        )
        self.assertEqual("routine-ui", result["experience_level"])
        self.assertEqual("generated", result["status"])
        self.assertTrue(result["source_ingredients"])

    def test_spatial_product_need_selects_interactive_three_d(self):
        result = compose_experience(
            "luxury mechanical watch product viewer rotate inspect materials",
            website_type="E-commerce",
            design_language="Minimalism",
            layout_structure="Split Screen",
        )
        self.assertEqual("interactive-3d", result["experience_level"])
        self.assertIn("spatial-inspection", result["activated_rules"])
        self.assertEqual("verified", result["ingredients"]["website_type"]["status"])

    def test_unknown_combination_is_generated_without_fake_citation(self):
        result = compose_experience(
            "multilingual interstellar archive bazaar",
            website_type="Marketplace",
            design_language="Frutiger Aero",
            layout_structure="Faceted Discovery",
        )
        self.assertEqual("generated", result["status"])
        self.assertIn("Frutiger Aero", result["generated_inputs"])
        self.assertNotIn("citation", result["generated_plan"])
        self.assertTrue(result["source_ingredients"])
        self.assertEqual("faceted-discovery", result["ingredients"]["layout_structure"]["id"])

    def test_generated_plan_contains_fallback_and_accessibility_constraints(self):
        result = compose_experience("interactive 3d product viewer")
        plan = result["generated_plan"]
        self.assertTrue(plan["fallback"])
        self.assertIn("keyboard", " ".join(plan["constraints"]).casefold())
        self.assertIn("reduced motion", " ".join(plan["constraints"]).casefold())

    def test_design_system_includes_experience_and_taxonomy_sources(self):
        result = DesignSystemGenerator().generate(
            "luxury mechanical watch product viewer rotate materials"
        )
        self.assertEqual("interactive-3d", result["experience"]["experience_level"])
        self.assertTrue(result["source_identities"]["website_type"])
        self.assertTrue(result["source_identities"]["layout_structure"])

    def test_design_system_text_exposes_taxonomy_ingredients(self):
        result = DesignSystemGenerator().generate("editorial fashion portfolio")
        text = format_markdown(result)
        self.assertIn("Website Type", text)
        self.assertIn("Design Language", text)
        self.assertIn("Layout Structure", text)

    def test_cli_experience_mode_returns_json(self):
        script = SCRIPTS_DIR / "search.py"
        completed = subprocess.run(
            [sys.executable, str(script), "watch product viewer", "--experience", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("generated", json.loads(completed.stdout)["status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
