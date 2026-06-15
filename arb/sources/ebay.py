"""eBay Browse API source (official API).

Uses the OAuth2 client-credentials flow + the Browse `item_summary/search`
endpoint, filtered to auctions. Credentials come from config or the
EBAY_APP_ID / EBAY_CERT_ID environment variables.

NOTE ON COMPS: the Browse API returns *active* listings only. Sold/completed
prices are not available here -- they live in the access-gated Marketplace
Insights API. Valuation therefore uses a separate, pluggable CompSource
(see arb/valuation/). This source is only an ingestor of live auctions.
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from typing import List, Optional

import requests

from ..logging_setup import get_logger
from ..models import Listing
from .base import AuctionSource

log = get_logger("source.ebay")

PROD = {
    "oauth": "https://api.ebay.com/identity/v1/oauth2/token",
    "browse": "https://api.ebay.com/buy/browse/v1/item_summary/search",
}
SANDBOX = {
    "oauth": "https://api.sandbox.ebay.com/identity/v1/oauth2/token",
    "browse": "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search",
}
SCOPE = "https://api.ebay.com/oauth/api_scope"


class EbayBrowseSource(AuctionSource):
    def __init__(self, cfg):
        super().__init__(cfg)
        o = cfg.options
        self.app_id = o.get("app_id") or os.environ.get("EBAY_APP_ID", "")
        self.cert_id = o.get("cert_id") or os.environ.get("EBAY_CERT_ID", "")
        self.marketplace_id = o.get("marketplace_id", "EBAY_US")
        self.query = o.get("query", "")
        self.category_ids = str(o.get("ebay_category_ids", "")) if o.get("ebay_category_ids") else ""
        self.limit = int(o.get("limit", 50))
        self.timeout = float(o.get("timeout_seconds", 20))
        self.endpoints = SANDBOX if o.get("sandbox") else PROD
        self._token: Optional[str] = None
        self._token_expiry: float = 0.0

    # --- auth ---
    def _get_token(self) -> str:
        if self._token and time.time() < self._token_expiry - 60:
            return self._token
        if not self.app_id or not self.cert_id:
            raise RuntimeError(
                "missing eBay credentials (set app_id/cert_id in config or "
                "EBAY_APP_ID/EBAY_CERT_ID env vars)"
            )
        resp = requests.post(
            self.endpoints["oauth"],
            auth=(self.app_id, self.cert_id),
            data={"grant_type": "client_credentials", "scope": SCOPE},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        payload = resp.json()
        self._token = payload["access_token"]
        self._token_expiry = time.time() + float(payload.get("expires_in", 7200))
        return self._token

    # --- fetch ---
    def fetch_listings(self) -> List[Listing]:
        token = self._get_token()
        params = {
            "q": self.query,
            "limit": self.limit,
            "filter": "buyingOptions:{AUCTION}",
        }
        if self.category_ids:
            params["category_ids"] = self.category_ids
        resp = requests.get(
            self.endpoints["browse"],
            headers={
                "Authorization": f"Bearer {token}",
                "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
            },
            params=params,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        items = resp.json().get("itemSummaries", []) or []
        log.info("ebay source %s returned %d items", self.name, len(items))
        return [self._to_listing(it) for it in items]

    def _to_listing(self, it: dict) -> Listing:
        bid = it.get("currentBidPrice") or it.get("price") or {}
        bid_value = float(bid.get("value", 0.0)) if isinstance(bid, dict) else 0.0
        currency = bid.get("value") and bid.get("currency") or "USD"

        shipping_cost = None
        for opt in it.get("shippingOptions", []) or []:
            cost = opt.get("shippingCost") or {}
            if "value" in cost:
                shipping_cost = float(cost["value"])
                break

        end_time = None
        if it.get("itemEndDate"):
            end_time = datetime.fromisoformat(it["itemEndDate"].replace("Z", "+00:00"))
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)

        loc = it.get("itemLocation") or {}
        location = ", ".join(p for p in [loc.get("city"), loc.get("stateOrProvince"), loc.get("country")] if p)

        return Listing(
            source=self.name,
            source_id=str(it.get("itemId", "")),
            url=it.get("itemWebUrl", ""),
            title=it.get("title", ""),
            current_bid=bid_value,
            currency=currency,
            bid_count=int(it.get("bidCount", 0) or 0),
            shipping_cost=shipping_cost,
            location=location,
            end_time=end_time,
            raw=it,
        )
