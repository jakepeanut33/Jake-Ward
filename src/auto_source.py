"""Optionally populate the queue from recent uploads of source channels.

This is a convenience for keeping the queue topped up. It does NOT try to be
clever about finding the "funniest" moment — it grabs a fixed window from each
recent upload. Curate timestamps by hand in data/queue.json for best results.
"""
from __future__ import annotations

from typing import Any

from .downloader import list_recent_uploads


def _seconds_to_hhmmss(seconds: int) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def build_candidates(auto_cfg: dict[str, Any], channel: dict[str, Any]) -> list[dict]:
    """Return queue-clip dicts for recent uploads of the configured channels."""
    if not auto_cfg.get("enabled"):
        return []

    limit = int(auto_cfg.get("videos_per_channel", 5))
    offset = int(auto_cfg.get("clip_offset_seconds", 0))
    length = int(auto_cfg.get("clip_length_seconds", 50))

    candidates: list[dict] = []
    for channel_url in auto_cfg.get("channels", []) or []:
        try:
            uploads = list_recent_uploads(channel_url, limit)
        except Exception as exc:  # noqa: BLE001 - one bad channel shouldn't abort all
            print(f"[auto_source] failed to list {channel_url}: {exc}")
            continue

        for up in uploads:
            candidates.append(
                {
                    "id": f"auto-{up['id']}",
                    "source_url": up["url"],
                    "start": _seconds_to_hhmmss(offset),
                    "end": _seconds_to_hhmmss(offset + length),
                    "title": (up["title"] or channel.get("name", "Funny Short"))[:100],
                    "caption": up["title"][:80] if up.get("title") else "",
                    "posted": False,
                    "posted_at": None,
                    "video_id": None,
                }
            )
    return candidates
