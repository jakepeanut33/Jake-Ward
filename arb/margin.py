"""Margin calculator -- the heart of the tool.

All-in cost includes: projected winning bid, buyer's premium, sales tax, and
inbound shipping. Net resale proceeds subtract: marketplace fee, payment fee,
and outbound shipping. Every fee is a config value.
"""
from __future__ import annotations

from .config import BidProjectionConfig, FeesConfig
from .models import CostBreakdown, Listing, ProceedsBreakdown


def project_winning_bid(current_bid: float, bp: BidProjectionConfig) -> float:
    """Estimate what it will actually take to win the auction."""
    return max(current_bid * bp.multiplier, current_bid + bp.min_increment)


def compute_cost(listing: Listing, fees: FeesConfig, bp: BidProjectionConfig) -> CostBreakdown:
    projected_bid = project_winning_bid(listing.current_bid, bp)
    buyer_premium = projected_bid * fees.buyer_premium_pct / 100.0
    taxable = projected_bid + buyer_premium
    sales_tax = taxable * fees.sales_tax_pct / 100.0
    inbound = listing.shipping_cost if listing.shipping_cost is not None else fees.default_inbound_shipping
    all_in = projected_bid + buyer_premium + sales_tax + inbound
    return CostBreakdown(
        projected_bid=round(projected_bid, 2),
        buyer_premium=round(buyer_premium, 2),
        sales_tax=round(sales_tax, 2),
        inbound_shipping=round(inbound, 2),
        all_in_cost=round(all_in, 2),
    )


def compute_proceeds(resale_value: float, fees: FeesConfig) -> ProceedsBreakdown:
    marketplace_fee = resale_value * fees.marketplace_fee_pct / 100.0
    payment_fee = resale_value * fees.payment_fee_pct / 100.0 + fees.payment_fee_fixed
    outbound = fees.outbound_shipping
    net = resale_value - marketplace_fee - payment_fee - outbound
    return ProceedsBreakdown(
        resale_value=round(resale_value, 2),
        marketplace_fee=round(marketplace_fee, 2),
        payment_fee=round(payment_fee, 2),
        outbound_shipping=round(outbound, 2),
        net_proceeds=round(net, 2),
    )
