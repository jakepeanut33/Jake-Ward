import os
import tempfile
import unittest

from arb.config import CategoryConfig
from arb.models import Listing
from arb.valuation.csv_comps import CsvCompSource
from arb.valuation.engine import ValuationEngine

CSV = """identity_key,grade,sold_price,sold_date
k,10,100.00,2026-06-10
k,10,120.00,2026-06-08
k,10,110.00,2026-06-05
thin,10,50.00,2026-06-01
"""


class TestValuation(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w") as fh:
            fh.write(CSV)
        self.engine = ValuationEngine(CsvCompSource(self.path))

    def tearDown(self):
        os.unlink(self.path)

    def _listing(self, key, grade="10"):
        return Listing(source="t", source_id="1", url="", title="x", current_bid=1.0,
                       identity_key=key, grade=grade)

    def test_median_of_comps(self):
        cat = CategoryConfig(key="c", sold_comp_window=10, min_comps=5)
        v = self.engine.value(self._listing("k"), cat)
        self.assertEqual(v.estimated_value, 110.0)
        self.assertEqual(v.sample_size, 3)

    def test_low_confidence_when_below_min_comps(self):
        cat = CategoryConfig(key="c", sold_comp_window=10, min_comps=5)
        v = self.engine.value(self._listing("k"), cat)
        self.assertTrue(v.low_confidence)  # only 3 comps < 5

    def test_full_confidence_when_enough_comps(self):
        cat = CategoryConfig(key="c", sold_comp_window=10, min_comps=3)
        v = self.engine.value(self._listing("k"), cat)
        self.assertFalse(v.low_confidence)
        self.assertEqual(v.confidence, 1.0)

    def test_no_comps_returns_none(self):
        cat = CategoryConfig(key="c", sold_comp_window=10, min_comps=5)
        self.assertIsNone(self.engine.value(self._listing("missing"), cat))

    def test_window_limits_sample(self):
        cat = CategoryConfig(key="c", sold_comp_window=2, min_comps=1)
        v = self.engine.value(self._listing("k"), cat)
        self.assertEqual(v.sample_size, 2)  # newest 2 only


if __name__ == "__main__":
    unittest.main()
