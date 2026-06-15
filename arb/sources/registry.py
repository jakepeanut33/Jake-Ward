"""Builds source instances from config. Add new source types here."""
from __future__ import annotations

from typing import Dict, List, Type

from ..config import Config, SourceConfig
from ..logging_setup import get_logger
from .base import AuctionSource
from .ebay import EbayBrowseSource
from .sample import SampleSource

log = get_logger("source.registry")

#: Map a config `type` to its implementation. Register new sources here.
SOURCE_TYPES: Dict[str, Type[AuctionSource]] = {
    "ebay": EbayBrowseSource,
    "sample": SampleSource,
}


def build_sources(cfg: Config) -> List[AuctionSource]:
    sources: List[AuctionSource] = []
    for sc in cfg.sources:
        if not sc.enabled:
            log.info("source %s disabled, skipping", sc.name)
            continue
        cls = SOURCE_TYPES.get(sc.type)
        if cls is None:
            log.warning("unknown source type %r for %s, skipping", sc.type, sc.name)
            continue
        instance = cls(sc)
        if not instance.tos_allows_access:
            log.warning(
                "source %s skipped: ToS prohibits automated access (%s)",
                sc.name, instance.skip_reason or "no reason given",
            )
            continue
        sources.append(instance)
    return sources
