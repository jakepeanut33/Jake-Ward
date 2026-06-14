#!/usr/bin/env python3
"""
Build a cold call list of KC businesses likely to need Facebook ads.
Targets businesses that have a phone number but low review counts
(sign they're not marketing well).

Usage:
  python targets.py --type restaurant --limit 30
  python targets.py --all --limit 100
"""

import argparse
import csv
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
PLACES_URL = "https://maps.googleapis.com/maps/api/place"
KC_LOCATION = "39.0997,-94.5786"
SEARCH_RADIUS = 25000

# Best niches for Facebook ads services
NICHES = {
    "restaurant": "restaurant",
    "barbershop": "hair_care",
    "gym": "gym",
    "dentist": "dentist",
    "realtor": "real_estate_agency",
    "auto_repair": "car_repair",
    "cleaning": "cleaning_service",
    "contractor": "general_contractor",
    "spa": "beauty_salon",
    "chiropractor": "physiotherapist",
}


def search(keyword: str, page_token: str = None) -> dict:
    params = {"key": API_KEY, "location": KC_LOCATION, "radius": SEARCH_RADIUS, "keyword": keyword}
    if page_token:
        params = {"key": API_KEY, "pagetoken": page_token}
        time.sleep(2)
    resp = requests.get(f"{PLACES_URL}/nearbysearch/json", params=params)
    resp.raise_for_status()
    return resp.json()


def details(place_id: str) -> dict:
    resp = requests.get(f"{PLACES_URL}/details/json", params={
        "key": API_KEY,
        "place_id": place_id,
        "fields": "name,formatted_phone_number,website,formatted_address,rating,user_ratings_total",
    })
    resp.raise_for_status()
    return resp.json().get("result", {})


def score_lead(d: dict) -> int:
    """Higher score = better prospect for ads."""
    score = 0
    if not d.get("website"):
        score += 30        # No website = definitely needs help
    reviews = d.get("user_ratings_total", 0) or 0
    if reviews < 20:
        score += 30        # Very few reviews = not marketing
    elif reviews < 50:
        score += 15
    rating = d.get("rating", 0) or 0
    if 3.5 <= rating <= 4.5:
        score += 20        # Good enough to advertise, room to grow
    if d.get("formatted_phone_number"):
        score += 20        # Has a phone = reachable
    return score


def find_targets(niche: str, keyword: str, limit: int = 20) -> list[dict]:
    targets = []
    page_token = None

    while len(targets) < limit:
        data = search(keyword, page_token)
        for place in data.get("results", []):
            if len(targets) >= limit:
                break
            d = details(place["place_id"])
            phone = d.get("formatted_phone_number")
            if not phone:
                continue
            score = score_lead(d)
            targets.append({
                "name": d.get("name", place.get("name")),
                "niche": niche,
                "phone": phone,
                "address": d.get("formatted_address", ""),
                "website": d.get("website", "None"),
                "rating": d.get("rating", "N/A"),
                "reviews": d.get("user_ratings_total", 0),
                "score": score,
                "place_id": place["place_id"],
            })

        page_token = data.get("next_page_token")
        if not page_token:
            break

    return targets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=list(NICHES.keys()), help="Single niche to search")
    parser.add_argument("--all", action="store_true", help="Search all niches")
    parser.add_argument("--limit", type=int, default=20, help="Leads per niche")
    parser.add_argument("--output", default="cold_call_list.csv")
    args = parser.parse_args()

    niches_to_run = NICHES if args.all else {args.type: NICHES[args.type]} if args.type else {}
    if not niches_to_run:
        parser.error("Provide --type or --all")

    all_targets = []
    for niche, keyword in niches_to_run.items():
        print(f"\nSearching: {niche}...")
        found = find_targets(niche, keyword, args.limit)
        all_targets.extend(found)
        print(f"  {len(found)} prospects found")

    # Sort best leads first
    all_targets.sort(key=lambda x: x["score"], reverse=True)

    # Save CSV
    out = Path(args.output)
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name","niche","phone","address","website","rating","reviews","score","place_id"])
        writer.writeheader()
        writer.writerows(all_targets)

    print(f"\n✓ {len(all_targets)} total prospects → {out}")
    print(f"Top 5 leads:")
    for t in all_targets[:5]:
        print(f"  {t['name']} ({t['niche']}) — {t['phone']} — score: {t['score']}")


if __name__ == "__main__":
    main()
