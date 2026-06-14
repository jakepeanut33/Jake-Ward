#!/usr/bin/env python3
"""
Send personalized SMS to business owners with their preview website link.
"""

import os

from twilio.rest import Client

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def send_outreach(business: dict, preview_url: str, dry_run: bool = True) -> bool:
    name = business["name"]
    phone = business["phone"]

    # Clean phone to E.164 format for Twilio
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        digits = "1" + digits
    to_number = f"+{digits}"

    message = (
        f"Hey! I noticed {name} doesn't have a website yet. "
        f"I went ahead and built you a free one so you can see what it could look like:\n\n"
        f"{preview_url}\n\n"
        f"No strings attached — just reply if you want to keep it or make any changes. 🙌"
    )

    if dry_run:
        print(f"[DRY RUN] Would text {phone} ({to_number}):")
        print(f"  {message}\n")
        return True

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=to_number,
        )
        print(f"  Sent to {phone} — SID: {msg.sid}")
        return True
    except Exception as e:
        print(f"  [error] Failed to text {phone}: {e}")
        return False
