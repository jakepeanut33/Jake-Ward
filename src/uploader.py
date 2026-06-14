"""Upload a finished Short to YouTube via the Data API v3 (resumable upload)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from .config import OAuthSecrets

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_URI = "https://oauth2.googleapis.com/token"


def _credentials(secrets: OAuthSecrets) -> Credentials:
    creds = Credentials(
        token=None,
        refresh_token=secrets.refresh_token,
        token_uri=TOKEN_URI,
        client_id=secrets.client_id,
        client_secret=secrets.client_secret,
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return creds


def build_description(channel: dict[str, Any], clip: dict[str, Any]) -> str:
    parts = []
    if clip.get("description"):
        parts.append(clip["description"].strip())
    tags = channel.get("hashtags", [])
    if tags:
        parts.append(" ".join(tags))
    return "\n\n".join(parts).strip()


def upload_short(
    video_path: Path,
    clip: dict[str, Any],
    channel: dict[str, Any],
    secrets: OAuthSecrets,
) -> str:
    """Upload the video and return the new YouTube video id."""
    creds = _credentials(secrets)
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)

    title = clip.get("title") or channel.get("name", "Funny Short")
    # YouTube hard-limits titles to 100 characters.
    title = title[:100]

    body = {
        "snippet": {
            "title": title,
            "description": build_description(channel, clip),
            "tags": [t.lstrip("#") for t in channel.get("hashtags", [])],
            "categoryId": str(channel.get("category_id", "23")),
        },
        "status": {
            "privacyStatus": channel.get("privacy_status", "public"),
            "selfDeclaredMadeForKids": bool(channel.get("made_for_kids", False)),
        },
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )

    response = None
    while response is None:
        _, response = request.next_chunk()
    return response["id"]
