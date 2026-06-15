"""SQLite persistence: historical snapshots of listings and scored opportunities.

Every poll is recorded as a `run`. We store both the raw normalized listings and
the scored opportunities so you can later analyze how often flagged flips
actually hit.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from .models import Opportunity

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at    TEXT NOT NULL,
    finished_at   TEXT,
    source_count  INTEGER DEFAULT 0,
    listing_count INTEGER DEFAULT 0,
    opp_count     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS listings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES runs(id),
    source        TEXT,
    source_id     TEXT,
    url           TEXT,
    title         TEXT,
    category      TEXT,
    identity_key  TEXT,
    grade_company TEXT,
    grade         TEXT,
    current_bid   REAL,
    shipping_cost REAL,
    end_time      TEXT,
    fetched_at    TEXT
);

CREATE TABLE IF NOT EXISTS opportunities (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL REFERENCES runs(id),
    source          TEXT,
    source_id       TEXT,
    url             TEXT,
    title           TEXT,
    category        TEXT,
    identity_key    TEXT,
    grade           TEXT,
    est_value       REAL,
    sample_size     INTEGER,
    confidence      REAL,
    low_confidence  INTEGER,
    all_in_cost     REAL,
    net_proceeds    REAL,
    profit          REAL,
    margin_pct      REAL,
    score           REAL,
    seconds_left    REAL,
    reasons         TEXT,
    created_at      TEXT
);

CREATE INDEX IF NOT EXISTS idx_opps_run ON opportunities(run_id);
CREATE INDEX IF NOT EXISTS idx_opps_identity ON opportunities(identity_key);
"""


def _iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


class Database:
    def __init__(self, path: str):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # --- run lifecycle ---
    def start_run(self) -> int:
        cur = self.conn.execute(
            "INSERT INTO runs (started_at) VALUES (?)",
            (_iso(datetime.now(timezone.utc)),),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def finish_run(self, run_id: int, source_count: int, listing_count: int, opp_count: int) -> None:
        self.conn.execute(
            "UPDATE runs SET finished_at=?, source_count=?, listing_count=?, opp_count=? WHERE id=?",
            (_iso(datetime.now(timezone.utc)), source_count, listing_count, opp_count, run_id),
        )
        self.conn.commit()

    # --- writes ---
    def save_listings(self, run_id: int, listings) -> None:
        rows = [
            (
                run_id, l.source, l.source_id, l.url, l.title, l.category,
                l.identity_key, l.grade_company, l.grade, l.current_bid,
                l.shipping_cost, _iso(l.end_time), _iso(l.fetched_at),
            )
            for l in listings
        ]
        self.conn.executemany(
            """INSERT INTO listings
               (run_id, source, source_id, url, title, category, identity_key,
                grade_company, grade, current_bid, shipping_cost, end_time, fetched_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            rows,
        )
        self.conn.commit()

    def save_opportunities(self, run_id: int, opps: List[Opportunity]) -> None:
        now = _iso(datetime.now(timezone.utc))
        rows = []
        for o in opps:
            rows.append(
                (
                    run_id, o.listing.source, o.listing.source_id, o.listing.url,
                    o.listing.title, o.listing.category, o.listing.identity_key,
                    o.listing.grade, o.valuation.estimated_value, o.valuation.sample_size,
                    o.confidence, int(o.valuation.low_confidence), o.cost.all_in_cost,
                    o.proceeds.net_proceeds, o.profit, o.margin_pct, o.score,
                    o.listing.seconds_left(), json.dumps(o.reasons), now,
                )
            )
        self.conn.executemany(
            """INSERT INTO opportunities
               (run_id, source, source_id, url, title, category, identity_key, grade,
                est_value, sample_size, confidence, low_confidence, all_in_cost,
                net_proceeds, profit, margin_pct, score, seconds_left, reasons, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            rows,
        )
        self.conn.commit()

    # --- reads (dashboard) ---
    def latest_run_id(self) -> Optional[int]:
        row = self.conn.execute(
            "SELECT id FROM runs WHERE finished_at IS NOT NULL ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return int(row["id"]) if row else None

    def opportunities_for_run(self, run_id: int) -> List[dict]:
        rows = self.conn.execute(
            "SELECT * FROM opportunities WHERE run_id=? ORDER BY score DESC",
            (run_id,),
        ).fetchall()
        return [dict(r) for r in rows]
