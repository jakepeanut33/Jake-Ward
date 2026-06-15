"""Common data schemas shared across the pipeline.

Everything the ingestor produces is mapped onto :class:`Listing`. Downstream
stages attach a :class:`Valuation`, :class:`CostBreakdown`,
:class:`ProceedsBreakdown`, and finally bundle everything into an
:class:`Opportunity`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Listing:
    """A normalized auction listing (the common schema for every source)."""

    source: str
    source_id: str
    url: str
    title: str
    current_bid: float
    currency: str = "USD"
    bid_count: int = 0
    shipping_cost: Optional[float] = None  # None => unknown, fall back to config default
    location: str = ""
    end_time: Optional[datetime] = None
    fetched_at: datetime = field(default_factory=_utcnow)

    # --- item identity (populated by the normalizer) ---
    category: str = ""
    player: str = ""
    year: str = ""
    set_name: str = ""
    card_number: str = ""
    grade_company: str = ""
    grade: str = ""
    identity_key: str = ""

    raw: Dict[str, Any] = field(default_factory=dict)

    def seconds_left(self, now: Optional[datetime] = None) -> Optional[float]:
        if self.end_time is None:
            return None
        now = now or _utcnow()
        end = self.end_time
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        return (end - now).total_seconds()


@dataclass
class Comp:
    """A single recent SOLD comparable."""

    identity_key: str
    grade: str
    sold_price: float
    sold_date: Optional[datetime] = None
    source: str = ""


@dataclass
class Valuation:
    """Estimated fair resale value derived from sold comps."""

    identity_key: str
    grade: str
    estimated_value: float
    sample_size: int
    confidence: float  # 0.0 .. 1.0
    low_confidence: bool
    comps: List[Comp] = field(default_factory=list)


@dataclass
class CostBreakdown:
    """All-in acquisition cost."""

    projected_bid: float
    buyer_premium: float
    sales_tax: float
    inbound_shipping: float
    all_in_cost: float


@dataclass
class ProceedsBreakdown:
    """Net proceeds after selling fees."""

    resale_value: float
    marketplace_fee: float
    payment_fee: float
    outbound_shipping: float
    net_proceeds: float


@dataclass
class Opportunity:
    """A scored flip candidate ready for ranking, storage, and alerts."""

    listing: Listing
    valuation: Valuation
    cost: CostBreakdown
    proceeds: ProceedsBreakdown
    profit: float
    margin_pct: float
    score: float
    confidence: float
    reasons: List[str] = field(default_factory=list)
