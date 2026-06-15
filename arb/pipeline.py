"""Orchestrates one full poll cycle.

ingest -> normalize -> value -> margin -> score -> filter -> persist -> alert

A single source going down logs an error and is skipped; the run continues with
whatever other sources returned.
"""
from __future__ import annotations

from typing import List

from .alerts.email_alert import EmailAlerter
from .config import Config
from .db import Database
from .logging_setup import get_logger
from .margin import compute_cost, compute_proceeds
from .models import Listing, Opportunity
from .normalize import normalize
from .score import build_opportunity, clears_threshold, rank
from .sources.registry import build_sources
from .valuation.engine import ValuationEngine, build_comp_source

log = get_logger("pipeline")


class Pipeline:
    def __init__(self, cfg: Config, db: Database):
        self.cfg = cfg
        self.db = db
        self.sources = build_sources(cfg)
        self.valuation = ValuationEngine(build_comp_source(cfg.comps))
        self.alerter = EmailAlerter(cfg.email)

    def _ingest(self) -> List[Listing]:
        """Fetch from every source, isolating failures."""
        listings: List[Listing] = []
        ok_sources = 0
        for source in self.sources:
            try:
                fetched = source.fetch_listings()
                ok_sources += 1
                # tag each listing with the source's configured category
                for l in fetched:
                    if not l.category:
                        l.category = source.category
                log.info("source %s: %d listings", source.name, len(fetched))
                listings.extend(fetched)
            except Exception as exc:  # noqa: BLE001 - one source must not kill the run
                log.error("source %s failed, skipping: %s", source.name, exc)
        self._ok_sources = ok_sources
        return listings

    def run_once(self) -> List[Opportunity]:
        run_id = self.db.start_run()
        self._ok_sources = 0
        listings = self._ingest()

        opportunities: List[Opportunity] = []
        for listing in listings:
            category = self.cfg.categories.get(listing.category)
            if category is None:
                # default to the source's configured category if listing didn't carry one
                continue
            normalize(listing, category)

            valuation = self.valuation.value(listing, category)
            if valuation is None:
                log.debug("no comps for %s (%s grade %s); skipping",
                          listing.title, listing.identity_key, listing.grade)
                continue

            cost = compute_cost(listing, self.cfg.fees, self.cfg.bid_projection)
            proceeds = compute_proceeds(valuation.estimated_value, self.cfg.fees)
            opp = build_opportunity(listing, valuation, cost, proceeds, self.cfg.scoring)

            if clears_threshold(opp, self.cfg.margin_threshold_pct, self.cfg.min_profit):
                opportunities.append(opp)

        opportunities = rank(opportunities)

        # persist snapshot + scored opportunities
        self.db.save_listings(run_id, listings)
        self.db.save_opportunities(run_id, opportunities)
        self.db.finish_run(run_id, self._ok_sources, len(listings), len(opportunities))

        log.info("run %d complete: %d sources ok, %d listings, %d opportunities",
                 run_id, self._ok_sources, len(listings), len(opportunities))

        # alert on the best
        if opportunities:
            self.alerter.send(opportunities)

        return opportunities
