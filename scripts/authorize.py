#!/usr/bin/env python3
"""One-time helper: mint a YouTube refresh token for the automation.

Run this ONCE on your own machine (it opens a browser to log in to the Google
account that owns the YouTube channel). It prints a refresh token that you then
store as the YT_REFRESH_TOKEN secret.

Prerequisites
-------------
1. Create a Google Cloud project and enable "YouTube Data API v3".
2. Configure an OAuth consent screen (External; add yourself as a test user).
3. Create an OAuth client of type "Desktop app" and download the JSON as
   client_secret.json into the repo root (it is git-ignored).

Usage
-----
    pip install -r requirements.txt
    python scripts/authorize.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
ROOT = Path(__file__).resolve().parent.parent
CLIENT_SECRET = ROOT / "client_secret.json"


def main() -> int:
    if not CLIENT_SECRET.exists():
        print(
            f"Could not find {CLIENT_SECRET}.\n"
            "Download your OAuth 'Desktop app' client JSON from Google Cloud "
            "and save it there.",
            file=sys.stderr,
        )
        return 1

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    # Forces a refresh token to be issued.
    creds = flow.run_local_server(
        port=0, access_type="offline", prompt="consent"
    )

    with open(CLIENT_SECRET, "r", encoding="utf-8") as fh:
        client = json.load(fh)
    installed = client.get("installed") or client.get("web") or {}

    print("\n=== Store these as GitHub Actions secrets ===")
    print(f"YT_CLIENT_ID={installed.get('client_id')}")
    print(f"YT_CLIENT_SECRET={installed.get('client_secret')}")
    print(f"YT_REFRESH_TOKEN={creds.refresh_token}")
    print("=============================================")
    print("\nKeep these private. Do not commit them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
