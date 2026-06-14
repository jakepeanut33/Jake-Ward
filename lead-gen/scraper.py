#!/usr/bin/env python3
"""
Find local businesses in Kansas City with no website using Google Places API.
"""

import json
import os
import time
from pathlib import Path

import requests

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
PLACES_URL = "https://maps.googleapis.com/maps/api/place"

BUSINESS_TYPES = [
    "barbershop",
    "hair_salon",
    "nail_salon",
    "restaurant",
    "auto_repair",
    "plumber",
    "electrician",
    "cleaning_service",
    "landscaper",
    "painter",
]

KC_LOCATION = "39.0997,-94.5786"  # Kansas City lat/lng
SEARCH_RADIUS = 20000  # 20km


def search_businesses(query: str, page_token: str = None) -> dict:
    params = {
        "key": API_KEY,
        "location": KC_LOCATION,
        "radius": SEARCH_RADIUS,
        "keyword": query,
        "type": "establishment",
    }
    if page_token:
        params = {"key": API_KEY, "pagetoken": page_token}
        time.sleep(2)  # Google requires a short delay before using page tokens

    resp = requests.get(f"{PLACES_URL}/nearbysearch/json", params=params)
    resp.raise_for_status()
    return resp.json()


def get_place_details(place_id: str) -> dict:
    resp = requests.get(f"{PLACES_URL}/details/json", params={
        "key": API_KEY,
        "place_id": place_id,
        "fields": "name,formatted_phone_number,website,formatted_address,types,rating,user_ratings_total",
    })
    resp.raise_for_status()
    return resp.json().get("result", {})


def find_leads(business_type: str, max_results: int = 20) -> list[dict]:
    leads = []
    page_token = None

    while len(leads) < max_results:
        data = search_businesses(business_type, page_token)
        results = data.get("results", [])

        for place in results:
            if len(leads) >= max_results:
                break

            details = get_place_details(place["place_id"])

            # Skip if they already have a website
            if details.get("website"):
                continue

            phone = details.get("formatted_phone_number")
            if not phone:
                continue

            leads.append({
                "name": details.get("name", place.get("name")),
                "phone": phone,
                "address": details.get("formatted_address", ""),
                "type": business_type,
                "rating": details.get("rating"),
                "place_id": place["place_id"],
                "website": None,
            })
            print(f"  Found: {details.get('name')} — {phone}")

        page_token = data.get("next_page_token")
        if not page_token:
            break

    return leads


def main():
    all_leads = []
    output = Path("leads.json")

    for btype in BUSINESS_TYPES:
        print(f"\nSearching: {btype}...")
        leads = find_leads(btype, max_results=10)
        all_leads.extend(leads)
        print(f"  {len(leads)} leads found without a website")

    # Deduplicate by place_id
    seen = set()
    unique = []
    for lead in all_leads:
        if lead["place_id"] not in seen:
            seen.add(lead["place_id"])
            unique.append(lead)

    output.write_text(json.dumps(unique, indent=2))
    print(f"\nTotal unique leads: {len(unique)} → saved to {output}")


if __name__ == "__main__":
    main()
