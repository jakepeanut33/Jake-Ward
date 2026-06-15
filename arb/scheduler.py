"""Simple interval scheduler.

Re-polls every source on a configurable interval. No external dependency -- a
plain loop with graceful shutdown keeps it easy to run solo. A failure in one
cycle is logged and the loop continues to the next interval.
"""
from __future__ import annotations

import signal
import threading

from .config import Config
from .db import Database
from .logging_setup import get_logger
from .pipeline import Pipeline

log = get_logger("scheduler")


class Scheduler:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._stop = threading.Event()

    def _handle_signal(self, signum, frame):  # noqa: ARG002
        log.info("received signal %s, shutting down after current cycle", signum)
        self._stop.set()

    def run(self) -> None:
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        db = Database(self.cfg.db_path)
        pipeline = Pipeline(self.cfg, db)
        interval = self.cfg.poll_interval_seconds
        log.info("scheduler started; polling every %ds", interval)

        try:
            while not self._stop.is_set():
                try:
                    pipeline.run_once()
                except Exception as exc:  # noqa: BLE001 - never let one cycle kill the loop
                    log.exception("poll cycle failed: %s", exc)
                # wait the interval, but wake immediately on shutdown
                self._stop.wait(interval)
        finally:
            db.close()
            log.info("scheduler stopped")
