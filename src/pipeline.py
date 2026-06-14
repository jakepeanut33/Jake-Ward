"""Orchestrate a single post: pick a clip, download, format, upload, record."""
from __future__ import annotations

import argparse
import sys

from .auto_source import build_candidates
from .clipper import ffmpeg_available, make_short
from .config import WORK_DIR, OAuthSecrets, Settings
from .downloader import download_segment
from . import queue_manager as qm
from .uploader import upload_short


def refill_queue(settings: Settings, data: dict) -> int:
    """Add auto-sourced candidates to the queue. Returns number added."""
    candidates = build_candidates(settings.auto_source, settings.channel)
    added = 0
    for cand in candidates:
        if qm.add_clip(data, cand):
            added += 1
    if added:
        qm.save_queue(data)
        print(f"[pipeline] added {added} auto-sourced clip(s) to the queue")
    return added


def run_once(dry_run: bool = False) -> int:
    settings = Settings.load()
    data = qm.load_queue()

    # Top up from source channels if enabled and the queue is running low.
    if settings.auto_source.get("enabled") and qm.pending_count(data) == 0:
        refill_queue(settings, data)

    clip = qm.next_clip(data)
    if clip is None:
        print("[pipeline] queue is empty — nothing to post. Add clips to data/queue.json.")
        return 0  # not an error: just nothing to do

    print(f"[pipeline] selected clip: {clip['id']} -> {clip.get('title')!r}")

    if not ffmpeg_available():
        print("[pipeline] ERROR: ffmpeg not found on PATH.", file=sys.stderr)
        return 2

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = WORK_DIR / f"{clip['id']}-raw.mp4"
    short_path = WORK_DIR / f"{clip['id']}-short.mp4"

    print("[pipeline] downloading source segment...")
    download_segment(
        clip["source_url"], raw_path, clip.get("start"), clip.get("end")
    )

    print("[pipeline] formatting vertical Short...")
    make_short(
        raw_path,
        short_path,
        settings.formatting,
        caption=clip.get("caption"),
    )

    if dry_run:
        print(f"[pipeline] DRY RUN — built {short_path}, skipping upload.")
        return 0

    print("[pipeline] uploading to YouTube...")
    secrets = OAuthSecrets.from_env()
    video_id = upload_short(short_path, clip, settings.channel, secrets)
    url = f"https://youtube.com/shorts/{video_id}"
    print(f"[pipeline] uploaded: {url}")

    qm.mark_posted(data, clip["id"], video_id)
    qm.save_queue(data)
    print("[pipeline] queue updated.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Post one Core Boys Short.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build the Short but do not upload (no credentials needed).",
    )
    args = parser.parse_args(argv)
    return run_once(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
