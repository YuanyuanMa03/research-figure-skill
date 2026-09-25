"""Behavior checks for cross-discipline figure planning clues."""

import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from profile_data import profile_data, render_report  # noqa: E402


class ProfileDataTest(unittest.TestCase):
    def test_repeated_units_are_not_reported_as_independent_rows(self):
        df = pd.DataFrame({
            "subject": [1, 1, 2, 2, 3, 3, 4, 4],
            "group": ["A"] * 4 + ["B"] * 4,
            "visit": [0, 1] * 4,
            "response": [1.0, 2.0, 1.5, 2.5, 0.5, 1.0, 0.8, 1.2],
        })
        result = profile_data(df, group_cols=["group"],
                              unit_col="subject", time_col="visit")
        design = result["design_summary"]
        self.assertEqual(design["n_units"], 4)
        self.assertEqual(design["n_repeated_units"], 4)
        self.assertEqual(design["n_duplicate_unit_time"], 0)
        self.assertEqual(
            [(x["n_rows"], x["n_units"]) for x in design["per_group_unit_counts"]],
            [(4, 2), (4, 2)],
        )
        self.assertTrue(any("独立样本数" in s for s in result["suggestions"]))
        self.assertNotIn("subject", result["correlation"] or {})

    def test_duplicate_unit_time_and_nonpositive_values_are_visible(self):
        df = pd.DataFrame({
            "subject": ["S1", "S1", "S1", "S2"],
            "visit": [1, 1, 2, 1],
            "response": [0.0, -1.0, 2.0, 3.0],
        })
        result = profile_data(df, unit_col="subject", time_col="visit")
        self.assertEqual(result["design_summary"]["n_duplicate_unit_time"], 1)
        self.assertEqual(result["columns"]["response"]["n_zero"], 1)
        self.assertEqual(result["columns"]["response"]["n_negative"], 1)
        self.assertIn("普通对数轴不适用", " ".join(result["warnings"]))
        self.assertIn("Duplicate unit-time rows: 1", render_report(result))

    def test_no_role_columns_preserves_basic_profile(self):
        df = pd.DataFrame({"group": ["A", "A", "B", "B"],
                           "value": [1.0, 2.0, 3.0, 4.0]})
        result = profile_data(df, group_cols=["group"])
        self.assertIsNone(result["design_summary"])
        self.assertEqual(result["group_summary"]["n_groups"], 2)
        self.assertIn("Chart suggestions", render_report(result))

    def test_integer_measurement_can_be_declared_as_value(self):
        df = pd.DataFrame({"group": ["A", "A", "B", "B"],
                           "score": [0, 1, 2, 3]})
        guessed = profile_data(df, group_cols=["group"])
        declared = profile_data(df, group_cols=["group"], value_cols=["score"])
        self.assertEqual(guessed["columns"]["score"]["type"], "ordinal")
        self.assertEqual(declared["columns"]["score"]["type"], "continuous")
        self.assertTrue(any("原始点" in s for s in declared["suggestions"]))

    def test_same_unit_and_time_in_different_groups_is_not_duplicate(self):
        df = pd.DataFrame({"subject": ["S1", "S1"],
                           "group": ["A", "B"],
                           "visit": [1, 1],
                           "response": [1.0, 2.0]})
        result = profile_data(df, group_cols=["group"], unit_col="subject",
                              time_col="visit", value_cols=["response"])
        self.assertEqual(result["design_summary"]["n_duplicate_unit_time"], 0)


if __name__ == "__main__":
    unittest.main()
