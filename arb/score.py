"""Score and rank opportunities.

Score blends expected profit ($) and margin (%), then penalizes:
  * low comp-confidence (thin sold-comp sample), and
  * auctions ending too soon to realistically act on.
Profit = net resale proceeds - all-in cost.
"""
from __future__ import annotations

from typing import List, Optional

from .config import ScoringConfig
from .models import (
    CostBreakdown,
    Listing,
    Opportunity,
    ProceedsBreakdown,
    Valuation,
)


def build_opportunity(
    listing: Listing,
    valuation: Valuation,
    cost: CostBreakdown,
    proceeds: ProceedsBreakdown,
    scoring: ScoringConfig,
) -> Opportunity:
    profit = round(proceeds.net_proceeds - cost.all_in_cost, 2)
    margin_pct = round((profit / cost.all_in_cost * 100.0), 2) if cost.all_in_cost > 0 else 0.0

    reasons: List[str] = []

    # base score in roughly "dollar" units: profit plus a margin bonus
    base = profit * scoring.profit_weight + (margin_pct / 100.0) * scoring.margin_weight

    # confidence penalty
    conf_factor = 1.0
    if valuation.low_confidence:
        conf_factor = scoring.low_confidence_penalty
        reasons.append(f"low confidence ({valuation.sample_size} comps)")

    # ending-soon penalty
    time_factor = 1.0
    secs = listing.seconds_left()
    if secs is not None and secs <= scoring.ending_soon_minutes * 60:
        time_factor = scoring.ending_soon_penalty
        mins = max(0, int(secs // 60))
        reasons.append(f"ending soon ({mins}m left)")

    score = round(base * conf_factor * time_factor, 2)

    return Opportunity(
        listing=listing,
        valuation=valuation,
        cost=cost,
        proceeds=proceeds,
        profit=profit,
        margin_pct=margin_pct,
        score=score,
        confidence=round(valuation.confidence, 3),
        reasons=reasons,
    )


def clears_threshold(opp: Opportunity, margin_threshold_pct: float, min_profit: float) -> bool:
    return opp.margin_pct >= margin_threshold_pct and opp.profit >= min_profit


def rank(opps: List[Opportunity]) -> List[Opportunity]:
    return sorted(opps, key=lambda o: o.score, reverse=True)
