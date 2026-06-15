"""Pluggable interface for sold-comp providers.

The MVP ships a CSV-backed provider (no ToS risk, fully testable). Swap in
eBay's Marketplace Insights API or another sold-data provider later by
implementing this interface and registering it -- no core logic changes.
"""
from __future__ import annotations

import abc
from typing import List

from ..models import Comp


class CompSource(abc.ABC):
    @abc.abstractmethod
    def get_sold_comps(self, identity_key: str, grade: str) -> List[Comp]:
        """Return sold comps for an item identity + grade, newest first."""
        raise NotImplementedError
