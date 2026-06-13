#!/usr/bin/env python3
"""
Analyze chat logs to find hype moments and cut highlight clips.
Usage: python find_highlights.py vods/adapt/123456_chat.json vods/adapt/123456.mp4
"""

import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path


def find_spikes(messages: list[dict], window: int = 10, top_n: int = 10) -> list[dict]:
    """Find timestamps with the highest chat activity (messages per window seconds)."""
    counts: dict[int, int] = defaultdict(int)
    for msg in messages:
        bucket = int(msg["offset"]) // window
        counts[bucket] += 1

    sorted_buckets = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    seen = set()
    spikes = []

    for bucket, count in sorted_buckets:
        timestamp = bucket * window
        # deduplicate spikes within 60s of each other
        if any(abs(timestamp - s) < 60 for s in seen):
            continue
        seen.add(timestamp)
        spikes.append({"timestamp": timestamp, "message_count": count})
        if len(spikes) >= top_n:
            break

    return sorted(spikes, key=lambda x: x["timestamp"])


def cut_clip(video: Path, start: int, duration: int, output: Path):
    pad = 15  # seconds before the spike
    clip_start = max(0, start - pad)
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(clip_start),
        "-i", str(video),
        "-t", str(duration),
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac",
        str(output),
    ], capture_output=True)
    print(f"  Saved: {output.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_file", help="Path to _chat.json file")
    parser.add_argument("video_file", nargs="?", help="Path to .mp4 (optional, skips cutting if omitted)")
    parser.add_argument("--window", type=int, default=10, help="Seconds per analysis bucket")
    parser.add_argument("--clips", type=int, default=5, help="Number of clips to cut")
    parser.add_argument("--clip-length", type=int, default=45, help="Clip duration in seconds")
    args = parser.parse_args()

    chat_path = Path(args.chat_file)
    messages = json.loads(chat_path.read_text())
    print(f"Loaded {len(messages)} chat messages from {chat_path.name}")

    spikes = find_spikes(messages, window=args.window, top_n=args.clips)

    print(f"\nTop {len(spikes)} hype moments:")
    for i, spike in enumerate(spikes, 1):
        t = spike["timestamp"]
        mins, secs = divmod(t, 60)
        print(f"  #{i}  {mins:02d}:{secs:02d}  ({spike['message_count']} msgs/{args.window}s)")

    if not args.video_file:
        print("\n(No video file provided — skipping clip cutting)")
        return

    video_path = Path(args.video_file)
    clips_dir = video_path.parent / "clips"
    clips_dir.mkdir(exist_ok=True)

    print(f"\nCutting {len(spikes)} clips...")
    for i, spike in enumerate(spikes, 1):
        out = clips_dir / f"clip_{i:02d}_{spike['timestamp']}s.mp4"
        cut_clip(video_path, spike["timestamp"], args.clip_length, out)

    print(f"\nAll clips saved to {clips_dir}/")


if __name__ == "__main__":
    main()
