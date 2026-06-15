"""Common interface every auction source implements."""
from __future__ import annotations

import abc
from typing import List

from ..config import SourceConfig
from ..models import Listing


class AuctionSource(abc.ABC):
    """Pulls live auction listings from one source.

    Implementations must:
      * respect the source's ToS, robots.txt, and rate limits;
      * raise on hard failures (the pipeline isolates and logs them);
      * return listings already populated with source/id/url/title/bid/end_time.
        Item identity is filled in later by the normalizer.
    """

    #: Set to False (and explain in `skip_reason`) if the source's ToS prohibits
    #: automated access. The registry will refuse to build it.
    tos_allows_access: bool = True
    skip_reason: str = ""

    def __init__(self, cfg: SourceConfig):
        self.cfg = cfg
        self.name = cfg.name
        self.category = cfg.category

    @abc.abstractmethod
    def fetch_listings(self) -> List[Listing]:
        """Return the current set of live auction listings for this source."""
        raise NotImplementedError
