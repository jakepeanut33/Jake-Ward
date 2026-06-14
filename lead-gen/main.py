#!/usr/bin/env python3
"""
Full pipeline: scrape leads → build websites → send outreach texts.

Usage:
  python main.py --type barbershop          # scrape + build + text (dry run)
  python main.py --type barbershop --send   # actually send texts
  python main.py --from-file leads.json     # skip scraping, use existing leads
"""

import argparse
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from scraper import find_leads
from website_builder import build_and_deploy
from outreach import send_outreach

RESULTS_FILE = Path("results.json")


def run_pipeline(leads: list[dict], send: bool = False, limit: int = 5):
    results = []

    for i, biz in enumerate(leads[:limit], 1):
        print(f"\n[{i}/{min(len(leads), limit)}] {biz['name']} — {biz['phone']}")

        try:
            url = build_and_deploy(biz)
            biz["preview_url"] = url

            sent = send_outreach(biz, url, dry_run=not send)
            biz["contacted"] = sent

            results.append(biz)
            time.sleep(1)
        except Exception as e:
            print(f"  [error] Skipping {biz['name']}: {e}")

    RESULTS_FILE.write_text(json.dumps(results, indent=2))
    print(f"\nDone. {len(results)} businesses processed → {RESULTS_FILE}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", default="barbershop", help="Business type to search")
    parser.add_argument("--from-file", help="Load leads from existing JSON file")
    parser.add_argument("--limit", type=int, default=5, help="Max businesses to process")
    parser.add_argument("--send", action="store_true", help="Actually send texts (default: dry run)")
    args = parser.parse_args()

    if args.from_file:
        leads = json.loads(Path(args.from_file).read_text())
        print(f"Loaded {len(leads)} leads from {args.from_file}")
    else:
        print(f"Searching for {args.type} businesses in Kansas City with no website...")
        leads = find_leads(args.type, max_results=args.limit * 3)
        print(f"Found {len(leads)} leads")

        if not leads:
            print("No leads found. Try a different business type.")
            return

    if not args.send:
        print("\n[DRY RUN MODE] No texts will actually be sent. Use --send to go live.\n")

    run_pipeline(leads, send=args.send, limit=args.limit)


if __name__ == "__main__":
    main()
