import unittest
from datetime import datetime, timedelta, timezone

from arb.config import ScoringConfig
from arb.models import CostBreakdown, Listing, ProceedsBreakdown, Valuation
from arb.score import build_opportunity, clears_threshold, rank

SCORING = ScoringConfig(profit_weight=1.0, margin_weight=100.0,
                        low_confidence_penalty=0.5, ending_soon_minutes=30,
                        ending_soon_penalty=0.5)


def _listing(end_minutes=600):
    return Listing(source="t", source_id="1", url="", title="x", current_bid=100.0,
                   end_time=datetime.now(timezone.utc) + timedelta(minutes=end_minutes))


def _val(n=10, low=False):
    return Valuation(identity_key="k", grade="10", estimated_value=200.0,
                     sample_size=n, confidence=1.0 if not low else 0.4, low_confidence=low)


def _opp(end_minutes=600, low=False, all_in=100.0, net=150.0):
    cost = CostBreakdown(100, 0, 0, 0, all_in)
    proceeds = ProceedsBreakdown(200, 0, 0, 0, net)
    return build_opportunity(_listing(end_minutes), _val(low=low), cost, proceeds, SCORING)


class TestScore(unittest.TestCase):
    def test_profit_and_margin(self):
        opp = _opp(all_in=100.0, net=150.0)
        self.assertEqual(opp.profit, 50.0)
        self.assertEqual(opp.margin_pct, 50.0)

    def test_low_confidence_penalizes_and_flags(self):
        good = _opp(low=False)
        bad = _opp(low=True)
        self.assertLess(bad.score, good.score)
        self.assertTrue(any("low confidence" in r for r in bad.reasons))

    def test_ending_soon_penalizes_and_flags(self):
        soon = _opp(end_minutes=10)
        later = _opp(end_minutes=600)
        self.assertLess(soon.score, later.score)
        self.assertTrue(any("ending soon" in r for r in soon.reasons))

    def test_threshold_filtering(self):
        opp = _opp(all_in=100.0, net=150.0)  # 50% margin, $50 profit
        self.assertTrue(clears_threshold(opp, margin_threshold_pct=25.0, min_profit=20.0))
        self.assertFalse(clears_threshold(opp, margin_threshold_pct=60.0, min_profit=20.0))
        self.assertFalse(clears_threshold(opp, margin_threshold_pct=25.0, min_profit=100.0))

    def test_rank_orders_by_score_desc(self):
        a = _opp(net=120.0)   # smaller profit
        b = _opp(net=180.0)   # bigger profit
        ranked = rank([a, b])
        self.assertEqual(ranked[0], b)


if __name__ == "__main__":
    unittest.main()
