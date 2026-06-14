#!/usr/bin/env python3
"""
AI Voice Calling Agent
Makes outbound calls to business owners, pitches the website service,
and sends a preview link via SMS if they're interested.

Requirements:
  - Twilio account with Voice enabled
  - A public webhook URL (use ngrok to expose locally)
  - Run the webhook server first: python caller.py --server
  - Then make calls: python caller.py --call --phone "816-555-0123" --name "KC Cuts" --url "https://..."

Usage:
  # Terminal 1 — start the webhook server
  python caller.py --server

  # Terminal 2 — trigger a call
  python caller.py --call --phone "8165550123" --business "KC Fresh Cuts" --url "https://kc-fresh-cuts.vercel.app"
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, Response, request
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse

load_dotenv()

app = Flask(__name__)

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
WEBHOOK_BASE = os.getenv("WEBHOOK_BASE_URL", "http://localhost:5000")  # your ngrok URL

# Store active call context (in production use a DB or Redis)
CALL_CONTEXT: dict[str, dict] = {}


def twiml(response: VoiceResponse) -> Response:
    return Response(str(response), mimetype="text/xml")


@app.route("/voice/intro", methods=["POST"])
def intro():
    call_sid = request.form.get("CallSid")
    ctx = CALL_CONTEXT.get(call_sid, {})
    business = ctx.get("business", "your business")

    response = VoiceResponse()
    gather = Gather(
        input="speech dtmf",
        timeout=5,
        action=f"{WEBHOOK_BASE}/voice/response",
        method="POST",
        speech_timeout="auto",
    )
    gather.say(
        f"Hey, quick question — I noticed {business} doesn't have a website yet. "
        f"I actually built you a free preview so you can see what it'd look like. "
        f"Want me to text you the link right now? "
        f"Say yes or press 1, or say no thanks to skip.",
        voice="Polly.Matthew",
    )
    response.append(gather)

    # If no input
    response.say("No problem at all! Have a great day.", voice="Polly.Matthew")
    return twiml(response)


@app.route("/voice/response", methods=["POST"])
def handle_response():
    call_sid = request.form.get("CallSid")
    speech = (request.form.get("SpeechResult") or "").lower()
    digits = request.form.get("Digits", "")
    ctx = CALL_CONTEXT.get(call_sid, {})

    response = VoiceResponse()
    interested = (
        "yes" in speech or "sure" in speech or "yeah" in speech
        or "send" in speech or "okay" in speech or digits == "1"
    )

    if interested:
        # Send the SMS with their preview URL
        preview_url = ctx.get("preview_url", "")
        phone = ctx.get("phone", "")
        business = ctx.get("business", "your business")

        if phone and preview_url:
            _send_sms(phone, business, preview_url)

        response.say(
            "Perfect! I just texted you the link. Take a look whenever you get a chance "
            "and reply to that text if you want to keep it or make any changes. "
            "Have a great day!",
            voice="Polly.Matthew",
        )
    else:
        response.say(
            "Totally understand, no worries at all. Have a great day!",
            voice="Polly.Matthew",
        )

    response.hangup()
    return twiml(response)


def _send_sms(phone: str, business: str, preview_url: str):
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        digits = "1" + digits

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        body=(
            f"Here's the free website preview I built for {business}:\n\n"
            f"{preview_url}\n\n"
            f"Reply anytime if you want changes or want to keep it 🙌"
        ),
        from_=FROM_NUMBER,
        to=f"+{digits}",
    )
    print(f"  SMS sent to {phone}")


def make_call(phone: str, business: str, preview_url: str):
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        digits = "1" + digits
    to_number = f"+{digits}"

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    call = client.calls.create(
        to=to_number,
        from_=FROM_NUMBER,
        url=f"{WEBHOOK_BASE}/voice/intro",
        method="POST",
    )

    CALL_CONTEXT[call.sid] = {
        "phone": phone,
        "business": business,
        "preview_url": preview_url,
    }

    print(f"Calling {business} at {phone}... SID: {call.sid}")
    return call.sid


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Server mode
    server_parser = subparsers.add_parser("--server", help="Start webhook server")

    # Call mode
    parser.add_argument("--server", action="store_true", help="Start webhook server")
    parser.add_argument("--call", action="store_true", help="Make a call")
    parser.add_argument("--phone", help="Phone number to call")
    parser.add_argument("--business", help="Business name")
    parser.add_argument("--url", help="Preview website URL")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.server:
        print(f"Starting webhook server on port {args.port}...")
        print(f"Make sure WEBHOOK_BASE_URL is set to your public ngrok URL")
        app.run(port=args.port, debug=False)
    elif args.call:
        if not all([args.phone, args.business, args.url]):
            parser.error("--call requires --phone, --business, and --url")
        make_call(args.phone, args.business, args.url)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
