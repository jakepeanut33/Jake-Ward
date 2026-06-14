"""Configuration loading for the Shorts pipeline.

Non-secret settings live in config/settings.yaml. Secrets are read from
environment variables so they can be supplied as GitHub Actions secrets and
never committed to the repo.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = ROOT / "config" / "settings.yaml"
QUEUE_PATH = ROOT / "data" / "queue.json"
WORK_DIR = ROOT / "work"


@dataclass
class OAuthSecrets:
    """OAuth credentials for the YouTube Data API.

    These come from a Google Cloud "OAuth client" plus a refresh token minted
    once by scripts/authorize.py.
    """

    client_id: str
    client_secret: str
    refresh_token: str

    @classmethod
    def from_env(cls) -> "OAuthSecrets":
        missing = [
            name
            for name in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")
            if not os.environ.get(name)
        ]
        if missing:
            raise SystemExit(
                "Missing required environment variables: "
                + ", ".join(missing)
                + ".\nSet them as GitHub Actions secrets (or locally) before running. "
                "Run scripts/authorize.py once to obtain a refresh token."
            )
        return cls(
            client_id=os.environ["YT_CLIENT_ID"],
            client_secret=os.environ["YT_CLIENT_SECRET"],
            refresh_token=os.environ["YT_REFRESH_TOKEN"],
        )


@dataclass
class Settings:
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path = SETTINGS_PATH) -> "Settings":
        with open(path, "r", encoding="utf-8") as fh:
            return cls(raw=yaml.safe_load(fh) or {})

    # Convenience accessors --------------------------------------------------
    @property
    def channel(self) -> dict[str, Any]:
        return self.raw.get("channel", {})

    @property
    def formatting(self) -> dict[str, Any]:
        return self.raw.get("formatting", {})

    @property
    def auto_source(self) -> dict[str, Any]:
        return self.raw.get("auto_source", {})
