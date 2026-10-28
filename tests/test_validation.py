"""The model reproduces the notes' figures, and every mismatch is explained (plan §1.3)."""

import json
import unittest
from contextlib import redirect_stdout
from io import StringIO

from habitat_model import load, params
from habitat_model import validation
from habitat_model.__main__ import main
from habitat_model.assumptions import STATUSES


class TestValidation(unittest.TestCase):
    def test_every_mismatch_is_explained(self):
        outcomes = validation.run(params(load()))
        self.assertGreater(len(outcomes), 150)
        unexplained = [f"{o.check.section} {o.check.label}: model {o.model:.4g}, notes {o.check.reference:.4g} ({o.diff:+.1%})"
                       for o in outcomes if not o.ok and not o.check.known]
        self.assertEqual(unexplained, [])

    def test_known_mismatches_stay_small(self):
        # A known mismatch is rounding or a missing breakdown, not a different model.
        for o in validation.run(params(load())):
            if o.check.known:
                self.assertLess(abs(o.diff), 0.2, o.check.label)


class TestAssumptions(unittest.TestCase):
    def test_file(self):
        assumptions = load()
        for a in assumptions.values():
            self.assertIn(a.status, STATUSES)
            self.assertTrue(a.source, a.name)
            self.assertTrue(a.unit, a.name)
            if a.status == "design":
                self.assertFalse(a.varies, f"{a.name}: design choices aren't swept")

    def test_overrides(self):
        p = params(load(), shield_areal_t_m2=13)
        self.assertEqual(p.shield_areal_t_m2, 13)
        with self.assertRaises(KeyError):
            params(load(), no_such_input=1)


class TestCommandLine(unittest.TestCase):
    def run_cli(self, *args):
        out = StringIO()
        with redirect_stdout(out):
            self.assertEqual(main(list(args)), 0)
        return out.getvalue()

    def test_summary(self):
        text = self.run_cli("--size", "900", "--stack", "six", "--tiers", "2", "--host", "L", "--site", "Eros")
        self.assertIn("6 × 900 m tori", text)
        self.assertIn("People fed", text)

    def test_period_and_overrides(self):
        text = self.run_cli("--period", "80", "--set", "shield_areal_t_m2=12", "--json", "-")
        stats = json.loads(text)
        self.assertAlmostEqual(stats["design"]["radius_m"], 1600)
        self.assertGreater(stats["per_torus"]["mass_per_floor_t_m2"], 40)

    def test_reports(self):
        for flag in ("--key-tables", "--validate", "--sensitivity", "--assumptions-table"):
            self.assertTrue(self.run_cli(flag).startswith("#"), flag)
        self.assertIn("Median", self.run_cli("--monte-carlo", "20"))


if __name__ == "__main__":
    unittest.main()
