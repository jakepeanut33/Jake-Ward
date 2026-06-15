import unittest

from arb.config import BidProjectionConfig, FeesConfig
from arb.margin import compute_cost, compute_proceeds, project_winning_bid
from arb.models import Listing


def _listing(**kw):
    base = dict(source="t", source_id="1", url="", title="x", current_bid=100.0)
    base.update(kw)
    return Listing(**base)


class TestMargin(unittest.TestCase):
    def test_project_bid_uses_min_increment(self):
        bp = BidProjectionConfig(multiplier=1.0, min_increment=5.0)
        self.assertEqual(project_winning_bid(100.0, bp), 105.0)

    def test_project_bid_uses_multiplier_when_larger(self):
        bp = BidProjectionConfig(multiplier=1.10, min_increment=1.0)
        self.assertAlmostEqual(project_winning_bid(100.0, bp), 110.0, places=6)

    def test_all_in_cost_includes_every_component(self):
        fees = FeesConfig(buyer_premium_pct=10.0, sales_tax_pct=8.0,
                          default_inbound_shipping=5.0)
        bp = BidProjectionConfig(multiplier=1.0, min_increment=0.0)
        cost = compute_cost(_listing(current_bid=100.0, shipping_cost=None), fees, bp)
        # bid 100, premium 10, tax on 110 = 8.80, inbound default 5 => 123.80
        self.assertEqual(cost.projected_bid, 100.0)
        self.assertEqual(cost.buyer_premium, 10.0)
        self.assertEqual(cost.sales_tax, 8.80)
        self.assertEqual(cost.inbound_shipping, 5.0)
        self.assertEqual(cost.all_in_cost, 123.80)

    def test_listing_shipping_overrides_default(self):
        fees = FeesConfig(default_inbound_shipping=5.0)
        bp = BidProjectionConfig(multiplier=1.0, min_increment=0.0)
        cost = compute_cost(_listing(shipping_cost=0.0), fees, bp)
        self.assertEqual(cost.inbound_shipping, 0.0)  # free shipping respected

    def test_net_proceeds_subtract_all_fees(self):
        fees = FeesConfig(marketplace_fee_pct=13.0, payment_fee_pct=3.0,
                          payment_fee_fixed=0.30, outbound_shipping=5.0)
        proceeds = compute_proceeds(100.0, fees)
        # 100 - 13 - (3 + 0.30) - 5 = 78.70
        self.assertEqual(proceeds.marketplace_fee, 13.0)
        self.assertEqual(proceeds.payment_fee, 3.30)
        self.assertEqual(proceeds.net_proceeds, 78.70)


if __name__ == "__main__":
    unittest.main()
