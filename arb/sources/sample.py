"""Offline sample source.

Reads listings from a local JSON fixture so the whole pipeline runs end-to-end
without any external API access. Useful for development, demos, and tests.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import List

from ..models import Listing
from .base import AuctionSource


def _parse_end_time(value) -> datetime:
    """Accept an ISO timestamp or a relative '+<minutes>m' offset from now."""
    if isinstance(value, str) and value.startswith("+") and value.endswith("m"):
        minutes = float(value[1:-1])
        return datetime.now(timezone.utc) + timedelta(minutes=minutes)
    if isinstance(value, str):
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    raise ValueError(f"unrecognized end_time: {value!r}")


class SampleSource(AuctionSource):
    def fetch_listings(self) -> List[Listing]:
        path = self.cfg.options.get("fixture_path")
        if not path:
            raise ValueError(f"sample source {self.name!r} requires 'fixture_path'")
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        listings: List[Listing] = []
        for item in data:
            listings.append(
                Listing(
                    source=self.name,
                    source_id=str(item["source_id"]),
                    url=item.get("url", ""),
                    title=item["title"],
                    current_bid=float(item["current_bid"]),
                    currency=item.get("currency", "USD"),
                    bid_count=int(item.get("bid_count", 0)),
                    shipping_cost=item.get("shipping_cost"),
                    location=item.get("location", ""),
                    end_time=_parse_end_time(item["end_time"]) if item.get("end_time") else None,
                    # identity fields may be supplied directly by the fixture
                    player=item.get("player", ""),
                    year=str(item.get("year", "")),
                    set_name=item.get("set_name", ""),
                    card_number=str(item.get("card_number", "")),
                    grade_company=item.get("grade_company", ""),
                    grade=str(item.get("grade", "")),
                    raw=item,
                )
            )
        return listings
