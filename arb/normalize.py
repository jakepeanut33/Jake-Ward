"""Map raw listings onto the common identity schema.

For graded sports cards we extract grade company + grade, year, and card number
from structured fields when present, otherwise from the title via heuristics. A
canonical ``identity_key`` is built so listings can be matched to sold comps.
"""
from __future__ import annotations

import re

from .config import CategoryConfig
from .models import Listing

GRADE_RE = re.compile(r"\b(PSA|BGS|BVG|SGC)\s*\.?\s*(10|9\.5|9|8\.5|8|7|6|5|4|3|2|1)\b", re.I)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
CARDNO_RE = re.compile(r"#\s*([A-Za-z]?\d+[A-Za-z]?)")


def _field_slug(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", "_", value).strip("_")


def build_identity_key(listing: Listing) -> str:
    """Canonical key for comp matching (grade is matched separately)."""
    parts = [listing.year, listing.set_name, listing.player, listing.card_number]
    parts = [_field_slug(p) for p in parts if p]
    if parts:
        return "|".join(parts)
    # Fallback: slug of the title with the grade token removed.
    cleaned = GRADE_RE.sub("", listing.title)
    return _field_slug(cleaned)


def normalize(listing: Listing, category: CategoryConfig) -> Listing:
    listing.category = category.key

    if not listing.grade or not listing.grade_company:
        m = GRADE_RE.search(listing.title)
        if m:
            listing.grade_company = listing.grade_company or m.group(1).upper()
            listing.grade = listing.grade or m.group(2)

    if not listing.year:
        ym = YEAR_RE.search(listing.title)
        if ym:
            listing.year = ym.group(0)

    if not listing.card_number:
        cm = CARDNO_RE.search(listing.title)
        if cm:
            listing.card_number = cm.group(1)

    if not listing.identity_key:
        listing.identity_key = build_identity_key(listing)

    return listing
