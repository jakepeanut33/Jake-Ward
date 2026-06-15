"""Shared formatting for alert channels."""
from __future__ import annotations

from typing import List

from ..models import Opportunity


def _fmt_time_left(opp: Opportunity) -> str:
    secs = opp.listing.seconds_left()
    if secs is None:
        return "unknown"
    if secs < 0:
        return "ended"
    hours = int(secs // 3600)
    mins = int((secs % 3600) // 60)
    return f"{hours}h {mins}m" if hours else f"{mins}m"


def format_opportunity_text(opp: Opportunity, rank: int) -> str:
    l = opp.listing
    conf = "LOW" if opp.valuation.low_confidence else "ok"
    lines = [
        f"#{rank}  {l.title}",
        f"    source:     {l.source}  ->  {l.url}",
        f"    est. value: ${opp.valuation.estimated_value:,.2f}  "
        f"(n={opp.valuation.sample_size}, confidence={conf})",
        f"    all-in:     ${opp.cost.all_in_cost:,.2f}  "
        f"(bid ${opp.cost.projected_bid:,.2f} + premium ${opp.cost.buyer_premium:,.2f} "
        f"+ tax ${opp.cost.sales_tax:,.2f} + ship ${opp.cost.inbound_shipping:,.2f})",
        f"    net resale: ${opp.proceeds.net_proceeds:,.2f}",
        f"    profit:     ${opp.profit:,.2f}   margin: {opp.margin_pct:.1f}%   score: {opp.score:.1f}",
        f"    time left:  {_fmt_time_left(opp)}",
    ]
    if opp.reasons:
        lines.append(f"    flags:      {', '.join(opp.reasons)}")
    return "\n".join(lines)


def format_digest_text(opps: List[Opportunity]) -> str:
    header = f"Auction Arbitrage — {len(opps)} opportunit{'y' if len(opps) == 1 else 'ies'}"
    body = "\n\n".join(format_opportunity_text(o, i + 1) for i, o in enumerate(opps))
    return f"{header}\n{'=' * len(header)}\n\n{body}\n"
