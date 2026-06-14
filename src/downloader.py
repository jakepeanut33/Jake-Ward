"""Download source footage with yt-dlp.

We download only the segment we need (when start/end are given) using yt-dlp's
download-sections support, which avoids pulling whole long videos.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def _hhmmss_to_seconds(value: str) -> float:
    parts = [float(p) for p in str(value).split(":")]
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + part
    return seconds


def download_segment(
    url: str,
    out_path: Path,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> Path:
    """Download (a section of) a video to out_path as mp4.

    Returns the path to the downloaded file. Requires yt-dlp and ffmpeg on PATH.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--force-overwrites",
        # Prefer an mp4/h264 stream so ffmpeg work later is cheap and compatible.
        "-f",
        "bestvideo[ext=mp4][height<=1920]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format",
        "mp4",
        "-o",
        str(out_path),
    ]

    if start is not None and end is not None:
        start_s = _hhmmss_to_seconds(start)
        end_s = _hhmmss_to_seconds(end)
        # Re-encode the keyframe-cut so the section is frame-accurate.
        cmd += [
            "--download-sections",
            f"*{start_s}-{end_s}",
            "--force-keyframes-at-cuts",
        ]

    cmd.append(url)

    subprocess.run(cmd, check=True)
    if not out_path.exists():
        raise FileNotFoundError(f"yt-dlp did not produce {out_path}")
    return out_path


def list_recent_uploads(channel_url: str, limit: int) -> list[dict]:
    """Return metadata for the most recent uploads of a channel.

    Uses yt-dlp in flat-playlist mode (fast, no media download).
    """
    import json

    # Normalise an @handle / channel URL to its uploads playlist.
    target = channel_url.rstrip("/")
    if not target.endswith("/videos"):
        target = target + "/videos"

    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--playlist-end",
        str(limit),
        "--dump-single-json",
        target,
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(proc.stdout)
    entries = data.get("entries", []) or []
    results = []
    for entry in entries[:limit]:
        vid = entry.get("id")
        if not vid:
            continue
        results.append(
            {
                "id": vid,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "title": entry.get("title") or "",
            }
        )
    return results
