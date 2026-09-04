import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import finance_data


class FinanceDataTests(unittest.TestCase):
    def test_world_bank_response_preserves_metadata_and_values(self):
        payload = [
            {"page": 1, "pages": 1, "per_page": 50, "total": 1, "sourceid": "2", "lastupdated": "2026-07-13"},
            [{
                "indicator": {"id": "FP.CPI.TOTL", "value": "Consumer price index"},
                "country": {"id": "IN", "value": "India"},
                "countryiso3code": "IND",
                "date": "2025",
                "value": 233.063,
                "unit": "",
                "obs_status": "",
                "decimal": 1,
            }],
        ]

        records = finance_data.parse_world_bank(payload)

        self.assertEqual(records[0]["source"], "world-bank")
        self.assertEqual(records[0]["publisher"], "World Bank")
        self.assertEqual(records[0]["period"], "2025")
        self.assertEqual(records[0]["value"], 233.063)
        self.assertEqual(records[0]["published_at"], "2026-07-13")

    def test_mfapi_history_normalizes_valid_records_and_rejects_invalid_rows(self):
        payload = {
            "meta": {"fund_house": "Example Fund"},
            "data": [
                {"date": "20-08-2026", "nav": "123.4567"},
                {"date": "not-a-date", "nav": "12"},
                {"date": "19-08-2026", "nav": "bad"},
            ],
        }

        records = finance_data.parse_mfapi(payload, "12345")

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["source"], "mfapi")
        self.assertEqual(records[0]["scheme_code"], "12345")
        self.assertEqual(records[0]["nav"], 123.4567)
        self.assertEqual(records[0]["nav_date"], "2026-08-20")
        self.assertTrue(records[0]["warnings"])

    def test_amfi_feed_parses_nav_and_skips_headers(self):
        feed = "\n".join([
            "Scheme Code;ISIN Div Payout/ ISIN Growth;ISIN Div Reinvestment;Scheme Name;Plan;Option;Net Asset Value;Date",
            "12345;INF000000001;-;Example Equity Fund;Direct Plan;GROWTH;123.4567;20-Aug-2026",
            "12346;INF000000002;-;Example Equity Fund;Regular Plan;Growth;120.4567;20-Aug-2026",
            "malformed;row",
        ])

        records = finance_data.parse_amfi(feed)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["source"], "amfi")
        self.assertEqual(records[0]["scheme_code"], "12345")
        self.assertEqual(records[0]["plan"], "Direct Plan")
        self.assertEqual(records[0]["nav"], 123.4567)
        self.assertEqual(records[0]["nav_date"], "2026-08-20")

    def test_rbi_dbie_payload_preserves_series_metadata(self):
        payload = {
            "dataset": "Policy Repo Rate",
            "series": "Policy Repo Rate",
            "period": "2026-08-20",
            "value": "5.25",
            "unit": "percent",
            "frequency": "daily",
            "published_at": "2026-08-20",
        }

        record = finance_data.parse_rbi_dbie(payload)

        self.assertEqual(record["source"], "rbi-dbie")
        self.assertEqual(record["publisher"], "Reserve Bank of India")
        self.assertEqual(record["value"], 5.25)
        self.assertEqual(record["unit"], "percent")
        self.assertEqual(record["frequency"], "daily")

    def test_reconcile_mf_reports_disagreement(self):
        amfi = {"scheme_code": "12345", "nav_date": "2026-08-20", "nav": 100.0}
        mfapi = {"scheme_code": "12345", "nav_date": "2026-08-20", "nav": 101.0}

        result = finance_data.reconcile_mf(amfi, mfapi)

        self.assertFalse(result["match"])
        self.assertEqual(result["difference"], 1.0)
        self.assertIn("discrepancy", result["warnings"][0].lower())

    def test_records_have_serializable_provenance(self):
        payload = [
            {"page": 1, "pages": 1, "per_page": 50, "total": 0, "sourceid": "2", "lastupdated": "2026-07-13"},
            [],
        ]

        records = finance_data.parse_world_bank(payload)

        self.assertEqual(records, [])
        json.dumps(records)

    def test_url_validation_rejects_unapproved_hosts(self):
        with self.assertRaises(finance_data.SourceError):
            finance_data.validate_url("https://example.com/data")

    def test_number_rejects_nonfinite_values(self):
        with self.assertRaises(finance_data.SourceError):
            finance_data.number("nan", "value")

    def test_business_days_behind_ignores_weekends(self):
        self.assertEqual(
            finance_data.business_days_behind("2026-08-14", "2026-08-17"),
            1,
        )

    def test_business_days_behind_uses_holidays(self):
        self.assertEqual(
            finance_data.business_days_behind(
                "2026-08-17",
                "2026-08-20",
                {"2026-08-18"},
            ),
            2,
        )

    def test_assess_freshness_returns_expected_statuses(self):
        self.assertEqual(
            finance_data.assess_freshness("2026-08-20", "2026-08-20")["freshness_status"],
            "current",
        )
        self.assertEqual(
            finance_data.assess_freshness("2026-08-20", "2026-08-19")["freshness_status"],
            "delayed",
        )
        self.assertEqual(
            finance_data.assess_freshness("2026-08-20", "2026-08-17")["freshness_status"],
            "stale",
        )

    def test_assess_freshness_marks_missing_dates_unverified(self):
        result = finance_data.assess_freshness("2026-08-20", None)

        self.assertEqual(result["freshness_status"], "unverified")
        self.assertIsNone(result["business_days_behind"])

    @patch("finance_data.mfapi_history")
    @patch("finance_data.amfi_nav")
    def test_mf_freshness_marks_secondary_source_stale(self, amfi_nav, mfapi_history):
        amfi_nav.return_value = [{"scheme_code": "12345", "nav_date": "2026-08-20", "nav": 100.0}]
        mfapi_history.return_value = [{"scheme_code": "12345", "nav_date": "2026-08-17", "nav": 99.0}]

        result = finance_data.mf_freshness("12345")

        self.assertEqual(result["freshness_status"], "stale")
        self.assertEqual(result["business_days_behind"], 3)
        self.assertIsNone(result["comparison"])


if __name__ == "__main__":
    unittest.main()
