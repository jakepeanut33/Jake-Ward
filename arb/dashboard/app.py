"""Flask dashboard: a sortable/filterable table of the latest opportunities."""
from __future__ import annotations

import json
from typing import List

from flask import Flask, jsonify, render_template

from ..config import Config
from ..db import Database


def _rows_for_latest(db: Database) -> List[dict]:
    run_id = db.latest_run_id()
    if run_id is None:
        return []
    rows = db.opportunities_for_run(run_id)
    for r in rows:
        try:
            r["reasons"] = json.loads(r.get("reasons") or "[]")
        except (TypeError, ValueError):
            r["reasons"] = []
    return rows


def create_app(cfg: Config) -> Flask:
    app = Flask(__name__)

    def _db() -> Database:
        # one short-lived connection per request keeps SQLite happy across threads
        return Database(cfg.db_path)

    @app.route("/")
    def index():
        db = _db()
        try:
            rows = _rows_for_latest(db)
        finally:
            db.close()
        return render_template("index.html", rows=rows, threshold=cfg.margin_threshold_pct)

    @app.route("/api/opportunities")
    def api_opportunities():
        db = _db()
        try:
            rows = _rows_for_latest(db)
        finally:
            db.close()
        return jsonify(rows)

    return app
