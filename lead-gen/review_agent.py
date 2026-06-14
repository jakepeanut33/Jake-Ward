#!/usr/bin/env python3
"""
Google Review Collection Agent
Texts customers a direct link to leave a Google review after their visit.

Usage:
  python review_agent.py --place-id YOUR_GOOGLE_PLACE_ID --phone "816-555-0123" --name "John"
  python review_agent.py --place-id YOUR_GOOGLE_PLACE_ID --batch customers.csv
"""

import argparse
import csv
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "us")


def review_link(place_id: str) -> str:
    return f"https://search.google.com/local/writereview?placeid={place_id}"


def send_review_request(phone: str, name: str, place_id: str, dry_run: bool = True) -> bool:
    link = review_link(place_id)
    first_name = name.split()[0]

    message = (
        f"Hey {first_name}! Thanks for visiting {BUSINESS_NAME} 🙏 "
        f"If you have 30 seconds, we'd love a Google review — it helps us out a ton:\n\n"
        f"{link}\n\n"
        f"Reply STOP to opt out."
    )

    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        digits = "1" + digits
    to_number = f"+{digits}"

    if dry_run:
        print(f"[DRY RUN] → {phone}")
        print(f"  {message}\n")
        return True

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(body=message, from_=FROM_NUMBER, to=to_number)
        print(f"  Sent to {first_name} ({phone}) — SID: {msg.sid}")
        return True
    except Exception as e:
        print(f"  [error] {phone}: {e}")
        return False


def run_batch(csv_file: str, place_id: str, dry_run: bool = True):
    """
    CSV format: name,phone
    Example:
      John Smith,8165550123
      Maria Garcia,9135550456
    """
    path = Path(csv_file)
    if not path.exists():
        print(f"File not found: {csv_file}")
        return

    rows = list(csv.DictReader(path.open()))
    print(f"Loaded {len(rows)} customers from {csv_file}\n")

    sent = 0
    for row in rows:
        name = row.get("name", "").strip()
        phone = row.get("phone", "").strip()
        if not name or not phone:
            continue
        ok = send_review_request(phone, name, place_id, dry_run=dry_run)
        if ok:
            sent += 1
        time.sleep(0.5)

    print(f"\nDone. {sent}/{len(rows)} messages {'queued (dry run)' if dry_run else 'sent'}.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--place-id", required=True, help="Google Place ID for your business")
    parser.add_argument("--phone", help="Single customer phone number")
    parser.add_argument("--name", help="Single customer name")
    parser.add_argument("--batch", help="CSV file with columns: name,phone")
    parser.add_argument("--send", action="store_true", help="Actually send (default: dry run)")
    args = parser.parse_args()

    if args.batch:
        run_batch(args.batch, args.place_id, dry_run=not args.send)
    elif args.phone and args.name:
        send_review_request(args.phone, args.name, args.place_id, dry_run=not args.send)
    else:
        parser.error("Provide either --batch <file.csv> or both --phone and --name")


if __name__ == "__main__":
    main()
