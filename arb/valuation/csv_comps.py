"""CSV-backed sold-comp provider.

Expected columns: identity_key, grade, sold_price, sold_date (ISO date).
This is the MVP comp source -- you control the data, there's no ToS risk, and
it's trivially testable. Replace with a live sold-data API later.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from ..logging_setup import get_logger
from ..models import Comp
from .base import CompSource

log = get_logger("valuation.csv")


def _parse_date(value: str):
    value = (value or "").strip()
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


class CsvCompSource(CompSource):
    def __init__(self, path: str):
        self.path = path
        self._index: Dict[Tuple[str, str], List[Comp]] = {}
        self._load()

    def _load(self) -> None:
        with open(self.path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            count = 0
            for row in reader:
                try:
                    comp = Comp(
                        identity_key=row["identity_key"].strip(),
                        grade=str(row["grade"]).strip(),
                        sold_price=float(row["sold_price"]),
                        sold_date=_parse_date(row.get("sold_date", "")),
                        source="csv",
                    )
                except (KeyError, ValueError) as exc:
                    log.warning("skipping malformed comp row %r: %s", row, exc)
                    continue
                self._index.setdefault((comp.identity_key, comp.grade), []).append(comp)
                count += 1
        # newest first within each bucket
        for comps in self._index.values():
            comps.sort(key=lambda c: (c.sold_date or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)
        log.info("loaded %d sold comps across %d identity/grade buckets from %s",
                 count, len(self._index), self.path)

    def get_sold_comps(self, identity_key: str, grade: str) -> List[Comp]:
        return list(self._index.get((identity_key, str(grade).strip()), []))
