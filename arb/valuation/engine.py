"""Estimate fair resale value as the median of the last N sold comps.

Sample size drives a confidence score; low-comp items are flagged
low-confidence (and penalized later in scoring) rather than hidden.
"""
from __future__ import annotations

from statistics import median
from typing import Optional

from ..config import CategoryConfig, Config, CompsConfig
from ..models import Listing, Valuation
from .base import CompSource
from .csv_comps import CsvCompSource


def build_comp_source(comps_cfg: CompsConfig) -> CompSource:
    if comps_cfg.type == "csv":
        path = comps_cfg.options.get("path")
        if not path:
            raise ValueError("csv comps require a 'path'")
        return CsvCompSource(path)
    raise ValueError(f"unknown comps source type: {comps_cfg.type!r}")


class ValuationEngine:
    def __init__(self, comp_source: CompSource):
        self.comp_source = comp_source

    def value(self, listing: Listing, category: CategoryConfig) -> Optional[Valuation]:
        """Return a Valuation, or None if there are zero comps to value against."""
        comps = self.comp_source.get_sold_comps(listing.identity_key, listing.grade)
        comps = comps[: category.sold_comp_window]
        n = len(comps)
        if n == 0:
            return None
        est = float(median(c.sold_price for c in comps))
        confidence = min(1.0, n / max(1, category.min_comps))
        return Valuation(
            identity_key=listing.identity_key,
            grade=listing.grade,
            estimated_value=est,
            sample_size=n,
            confidence=confidence,
            low_confidence=n < category.min_comps,
            comps=comps,
        )
