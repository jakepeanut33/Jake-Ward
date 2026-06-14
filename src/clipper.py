"""Turn a source clip into a vertical 9:16 Short with ffmpeg.

Handles three background styles (blur / crop / pad), enforces the max length,
and optionally burns a caption across the top.
"""
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Any


def _escape_drawtext(text: str) -> str:
    # ffmpeg drawtext needs colons, quotes and backslashes escaped.
    text = text.replace("\\", "\\\\")
    text = text.replace(":", "\\:")
    text = text.replace("'", "’")  # swap apostrophe for a typographic one
    return text


def build_filter(formatting: dict[str, Any], caption: str | None) -> str:
    w = int(formatting.get("width", 1080))
    h = int(formatting.get("height", 1920))
    style = formatting.get("background", "blur")

    if style == "crop":
        base = (
            f"scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}"
        )
    elif style == "pad":
        base = (
            f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black"
        )
    else:  # blur (default)
        base = (
            f"split=2[bg][fg];"
            f"[bg]scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h},boxblur=24:2[bgb];"
            f"[fg]scale={w}:{h}:force_original_aspect_ratio=decrease[fgs];"
            f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2"
        )

    if formatting.get("burn_caption") and caption:
        text = _escape_drawtext(caption)
        draw = (
            f",drawtext=text='{text}':fontcolor=white:fontsize=54:"
            f"box=1:boxcolor=black@0.5:boxborderw=18:"
            f"x=(w-text_w)/2:y=120"
        )
        base = base + draw

    return base


def make_short(
    src: Path,
    dst: Path,
    formatting: dict[str, Any],
    caption: str | None = None,
    max_seconds: int | None = None,
) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    max_seconds = max_seconds or int(formatting.get("max_seconds", 58))
    vf = build_filter(formatting, caption)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-t",
        str(max_seconds),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-r",
        "30",
        "-movflags",
        "+faststart",
        str(dst),
    ]
    subprocess.run(cmd, check=True)
    if not dst.exists():
        raise FileNotFoundError(f"ffmpeg did not produce {dst}")
    return dst


def ffmpeg_available() -> bool:
    try:
        subprocess.run(
            shlex.split("ffmpeg -version"),
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
