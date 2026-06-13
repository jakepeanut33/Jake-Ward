#!/usr/bin/env python3
"""
Fetch recent VODs and chat logs for CORE House streamers.
Usage: python fetch_vods.py --client-id YOUR_ID --client-secret YOUR_SECRET
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

CORE_STREAMERS = [
    "adapt",
    "silky",
    "jasontheween",
    "lacy",
    "marlon",
    "stableronaldo",
]

TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_API_URL = "https://api.twitch.tv/helix"


def get_token(client_id: str, client_secret: str) -> str:
    resp = requests.post(TWITCH_AUTH_URL, params={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_user_ids(usernames: list[str], headers: dict) -> dict[str, str]:
    params = [("login", u) for u in usernames]
    resp = requests.get(f"{TWITCH_API_URL}/users", params=params, headers=headers)
    resp.raise_for_status()
    return {u["login"]: u["id"] for u in resp.json()["data"]}


def get_vods(user_id: str, headers: dict, max_vods: int = 5) -> list[dict]:
    resp = requests.get(f"{TWITCH_API_URL}/videos", params={
        "user_id": user_id,
        "type": "archive",
        "first": max_vods,
    }, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]


def download_vod(vod: dict, output_dir: Path) -> Path | None:
    vod_id = vod["id"]
    url = f"https://www.twitch.tv/videos/{vod_id}"
    out_file = output_dir / f"{vod_id}.mp4"

    if out_file.exists():
        print(f"  [skip] VOD {vod_id} already downloaded")
        return out_file

    print(f"  Downloading VOD {vod_id}: {vod['title'][:60]}")
    result = subprocess.run([
        "yt-dlp",
        "-o", str(out_file),
        "--no-part",
        url,
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  [error] yt-dlp failed: {result.stderr[:200]}")
        return None

    return out_file


def download_chat(vod_id: str, output_dir: Path) -> Path | None:
    """Download chat replay using Twitch's GQL API."""
    chat_file = output_dir / f"{vod_id}_chat.json"

    if chat_file.exists():
        print(f"  [skip] Chat for {vod_id} already downloaded")
        return chat_file

    print(f"  Fetching chat for VOD {vod_id}...")
    messages = []
    cursor = None

    while True:
        payload = [{
            "operationName": "VideoCommentsByOffsetOrCursor",
            "variables": {
                "videoID": vod_id,
                **({"cursor": cursor} if cursor else {"contentOffsetSeconds": 0}),
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044aa76adf6a",
                }
            },
        }]

        resp = requests.post(
            "https://gql.twitch.tv/gql",
            json=payload,
            headers={"Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko"},
        )

        if resp.status_code != 200:
            print(f"  [error] Chat fetch failed: {resp.status_code}")
            return None

        data = resp.json()[0].get("data", {})
        video = data.get("video")
        if not video:
            print(f"  [error] No video data returned for {vod_id}")
            return None

        comments = video.get("comments", {})
        edges = comments.get("edges", [])

        for edge in edges:
            node = edge["node"]
            messages.append({
                "offset": node["contentOffsetSeconds"],
                "user": node["commenter"]["displayName"] if node.get("commenter") else "unknown",
                "text": node["message"]["fragments"][0]["text"] if node.get("message") else "",
            })

        page_info = comments.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break

        cursor = edges[-1]["cursor"] if edges else None
        time.sleep(0.3)

    chat_file.write_text(json.dumps(messages, indent=2))
    print(f"  Saved {len(messages)} messages -> {chat_file.name}")
    return chat_file


def main():
    parser = argparse.ArgumentParser(description="Fetch CORE House VODs and chat")
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    parser.add_argument("--streamers", nargs="+", default=CORE_STREAMERS)
    parser.add_argument("--max-vods", type=int, default=3, help="VODs per streamer")
    parser.add_argument("--output", default="vods", help="Output directory")
    parser.add_argument("--chat-only", action="store_true", help="Skip video download")
    args = parser.parse_args()

    token = get_token(args.client_id, args.client_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": args.client_id,
    }

    print(f"Resolving {len(args.streamers)} streamers...")
    user_ids = get_user_ids(args.streamers, headers)

    for username in args.streamers:
        uid = user_ids.get(username)
        if not uid:
            print(f"[warn] Could not find user: {username}")
            continue

        print(f"\n=== {username} (id={uid}) ===")
        vods = get_vods(uid, headers, args.max_vods)

        if not vods:
            print("  No VODs found")
            continue

        out_dir = Path(args.output) / username
        out_dir.mkdir(parents=True, exist_ok=True)

        for vod in vods:
            print(f"\n  VOD: {vod['id']} | {vod['duration']} | {vod['published_at'][:10]}")
            download_chat(vod["id"], out_dir)
            if not args.chat_only:
                download_vod(vod, out_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
