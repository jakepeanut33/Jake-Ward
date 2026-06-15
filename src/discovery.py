"""Discover top-performing videos via the YouTube Data API and turn them into
candidate clips for the queue.

Two modes:
  * "search"   - search by keywords, ordered by view count (best for a niche)
  * "trending" - the regional "most popular" chart (broad, fast-moving)

Discovery reads public data, so it uses a simple API key (YT_API_KEY) rather
than the upload OAuth token. Get one from the same Google Cloud project:
APIs & Services -> Credentials -> Create credentials -> API key.

NOTE: this finds videos; it cannot tell which 50 seconds are the "funny" part.
It takes a configurable window (skipping the intro by default). Hand-tuned
timestamps still produce better Shorts.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any

from googleapiclient.discovery import build

_DURATION_RE = re.compile(
    r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
)


def _api_key() -> str:
    key = os.environ.get("YT_API_KEY")
    if not key:
        raise SystemExit(
            "Discovery is enabled but YT_API_KEY is not set. Create an API key "
            "in Google Cloud (same project as your OAuth client) and provide it "
            "as the YT_API_KEY environment variable / GitHub secret."
        )
    return key


def _parse_duration(iso: str) -> int:
    """Convert an ISO-8601 duration (e.g. PT1H2M3S) to whole seconds."""
    m = _DURATION_RE.fullmatch(iso or "")
    if not m:
        return 0
    hours, minutes, seconds = (int(x) if x else 0 for x in m.groups())
    return hours * 3600 + minutes * 60 + seconds


def _seconds_to_hhmmss(seconds: int) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _clip_window(duration: int, offset: int, length: int) -> tuple[str, str]:
    """Pick a start/end window that fits inside the source duration."""
    if duration <= 0:
        start = offset
    elif duration <= length:
        start = 0
        length = duration
    else:
        start = min(offset, max(0, duration - length))
    return _seconds_to_hhmmss(start), _seconds_to_hhmmss(start + length)


def _candidate_from_video(video: dict, cfg: dict, channel: dict) -> dict | None:
    vid = video["id"] if isinstance(video["id"], str) else video["id"].get("videoId")
    if not vid:
        return None
    stats = video.get("statistics", {})
    views = int(stats.get("viewCount", 0) or 0)
    if views < int(cfg.get("min_views", 0)):
        return None

    duration = _parse_duration(video.get("contentDetails", {}).get("duration", ""))
    max_dur = int(cfg.get("max_source_duration_seconds", 0) or 0)
    if max_dur and duration > max_dur:
        return None

    snippet = video.get("snippet", {})
    title = (snippet.get("title") or channel.get("name", "Funny Short")).strip()
    start, end = _clip_window(
        duration,
        int(cfg.get("clip_offset_seconds", 30)),
        int(cfg.get("clip_length_seconds", 50)),
    )
    return {
        "id": f"disc-{vid}",
        "source_url": f"https://www.youtube.com/watch?v={vid}",
        "start": start,
        "end": end,
        "title": title[:100],
        "caption": title[:80],
        "source_views": views,
        "posted": False,
        "posted_at": None,
        "video_id": None,
    }


def discover(cfg: dict[str, Any], channel: dict[str, Any]) -> list[dict]:
    """Return candidate clips for the top-performing videos, per config."""
    if not cfg.get("enabled"):
        return []

    youtube = build("youtube", "v3", developerKey=_api_key(), cache_discovery=False)
    mode = cfg.get("mode", "search")
    max_results = min(int(cfg.get("max_results", 10)), 50)
    region = cfg.get("region", "US")

    video_ids: list[str] = []

    if mode == "trending":
        resp = (
            youtube.videos()
            .list(
                part="snippet,statistics,contentDetails",
                chart="mostPopular",
                regionCode=region,
                videoCategoryId=str(cfg.get("category_id", "")) or None,
                maxResults=max_results,
            )
            .execute()
        )
        videos = resp.get("items", [])
    else:  # search mode
        published_after = None
        days = int(cfg.get("published_within_days", 0) or 0)
        if days:
            dt = datetime.now(timezone.utc) - timedelta(days=days)
            published_after = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        for keyword in cfg.get("keywords", []) or []:
            search = (
                youtube.search()
                .list(
                    part="id",
                    q=keyword,
                    type="video",
                    order="viewCount",
                    maxResults=max_results,
                    regionCode=region,
                    publishedAfter=published_after,
                    safeSearch="none",
                )
                .execute()
            )
            for item in search.get("items", []):
                vid = item.get("id", {}).get("videoId")
                if vid and vid not in video_ids:
                    video_ids.append(vid)

        videos = []
        # Fetch stats/duration in batches of 50.
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i : i + 50]
            resp = (
                youtube.videos()
                .list(
                    part="snippet,statistics,contentDetails",
                    id=",".join(batch),
                )
                .execute()
            )
            videos.extend(resp.get("items", []))

    candidates: list[dict] = []
    for video in videos:
        cand = _candidate_from_video(video, cfg, channel)
        if cand:
            candidates.append(cand)

    # Best first.
    candidates.sort(key=lambda c: c.get("source_views", 0), reverse=True)
    return candidates
