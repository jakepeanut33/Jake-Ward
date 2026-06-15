# Auction Arbitrage (MVP)

Monitors auction listings for underpriced **graded sports cards (PSA/BGS)** and
flags likely flips: listings where **estimated resale value − all-in cost**
clears a target profit margin. Results are ranked, alerted via email, and shown
on a lightweight local dashboard.

It is built **config-driven and source-pluggable** so you can add categories and
auction sources later without touching the core logic.

## Why graded cards first
Clean comps and standardized identifiers (player / year / set / card # / grade)
make the valuation and matching tractable. The architecture is generic — adding
a category is a config change plus, optionally, a new source/comp adapter.

## Pipeline
```
ingest → normalize → value (sold comps) → margin → score → filter → persist → alert
                                                                        ↘ dashboard
```

| Stage | Module | Notes |
|------|--------|-------|
| Ingestor | `arb/sources/` | Each source behind `AuctionSource`. eBay uses the **official Browse API**. A source that fails is logged and skipped — the run continues. A source whose ToS forbids access sets `tos_allows_access = False` and is refused by the registry. |
| Normalizer | `arb/normalize.py` | Maps every listing to a common schema + canonical `identity_key`. |
| Valuation | `arb/valuation/` | Median of last *N* **sold** comps via a pluggable `CompSource` (CSV in the MVP). Sample size → confidence; thin comps are **flagged low-confidence, not hidden**. |
| Margin | `arb/margin.py` | All-in cost = projected bid + buyer's premium + sales tax + inbound shipping. Net resale = value − marketplace fee − payment fee − outbound shipping. **Every fee is a config value.** |
| Scorer | `arb/score.py` | Blends profit ($) and margin (%); penalizes low confidence and auctions ending too soon. |
| Alerts | `arb/alerts/` | Email digest of the top *N*. |
| Dashboard | `arb/dashboard/` | Flask; sortable/filterable table of the latest poll. |
| Scheduler | `arb/scheduler.py` | Re-polls on `poll_interval_seconds`; a bad cycle never kills the loop. |
| Storage | `arb/db.py` | SQLite. Every poll is a `run`; listings + opportunities are stored as historical snapshots so you can later measure how often flagged flips actually hit. |

## A note on sold comps (important)
eBay's free **Browse API returns only *active* listings** — not sold prices.
Sold data lives in the access-gated **Marketplace Insights API**. So valuation
uses a **separate, pluggable `CompSource`**. The MVP ships a CSV-backed provider
(`fixtures/sample_comps.csv`) you control — no ToS risk, fully testable — and you
can drop in a live sold-data provider later by implementing `CompSource`.

## Quick start
```bash
pip install -r requirements.txt
cp config.example.yaml config.yaml

# Runs entirely offline using the bundled sample source + sample comps:
python -m arb.cli run-once          # one poll cycle, prints ranked opportunities
python -m arb.cli serve             # dashboard at http://127.0.0.1:8000
python -m arb.cli run               # scheduled polling on the configured interval

python -m unittest discover -s tests
```

## Enabling eBay (official API)
1. Create an eBay developer app → get an **App ID (Client ID)** and **Cert ID (Client Secret)**.
2. Set them via env vars or in `config.yaml`:
   ```bash
   export EBAY_APP_ID=...   EBAY_CERT_ID=...
   ```
3. In `config.yaml`, set the `ebay_us` source `enabled: true`.

## Enabling email alerts
Fill in `alerts.email` in `config.yaml` (set `enabled: true`, SMTP host/port,
`from_addr`, `to_addrs`). Provide the password via `EMAIL_PASSWORD` env var or
the config. Test with:
```bash
python -m arb.cli test-alert
```

## Configuration
Everything lives in `config.yaml` (see `config.example.yaml` for the annotated
template): sources, categories, fee assumptions, `margin_threshold_pct`,
`min_profit`, `poll_interval_seconds`, scoring weights/penalties, alert targets,
and the dashboard host/port.

## Extending
- **New auction source:** subclass `AuctionSource`, register it in
  `arb/sources/registry.py`, add a config entry. **Respect robots.txt, rate
  limits, and ToS** — set `tos_allows_access = False` to opt a source out.
- **New comp/sold-data provider:** implement `CompSource`, wire it into
  `arb/valuation/engine.build_comp_source`.
- **New category:** add a `categories` entry and point a source at it.

> ⚠️ Use official APIs and respect each site's Terms of Service and robots.txt.
> This tool deliberately skips sources that prohibit automated access.
