"""Read/write the clip queue (data/queue.json).

The queue is the source of truth for what to post next. Each pipeline run pops
the first un-posted clip, processes it, and marks it posted. GitHub Actions
commits the updated queue back to the repo so state persists between runs.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .config import QUEUE_PATH


def load_queue(path: Path = QUEUE_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_queue(data: dict[str, Any], path: Path = QUEUE_PATH) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def next_clip(data: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Return the first clip that hasn't been posted yet, or None."""
    for clip in data.get("clips", []):
        if not clip.get("posted"):
            return clip
    return None


def pending_count(data: dict[str, Any]) -> int:
    return sum(1 for c in data.get("clips", []) if not c.get("posted"))


def mark_posted(data: dict[str, Any], clip_id: str, video_id: str) -> None:
    for clip in data.get("clips", []):
        if clip.get("id") == clip_id:
            clip["posted"] = True
            clip["posted_at"] = datetime.now(timezone.utc).isoformat()
            clip["video_id"] = video_id
            return
    raise KeyError(f"clip id {clip_id!r} not found in queue")


def add_clip(data: dict[str, Any], clip: dict[str, Any]) -> bool:
    """Add a clip if its id isn't already present. Returns True if added."""
    existing = {c.get("id") for c in data.get("clips", [])}
    if clip["id"] in existing:
        return False
    data.setdefault("clips", []).append(clip)
    return True
