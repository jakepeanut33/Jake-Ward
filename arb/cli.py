"""Command-line entrypoint.

    python -m arb.cli run-once       # one poll cycle
    python -m arb.cli run            # scheduled polling on the configured interval
    python -m arb.cli serve          # launch the dashboard
    python -m arb.cli test-alert     # send a sample email alert
    python -m arb.cli init-db        # create the SQLite schema
"""
from __future__ import annotations

import argparse
import sys

from .config import load_config
from .db import Database
from .logging_setup import get_logger, setup_logging

log = get_logger("cli")


def _load(args):
    cfg = load_config(args.config)
    setup_logging(cfg.log_level)
    return cfg


def cmd_run_once(args):
    cfg = _load(args)
    from .pipeline import Pipeline

    db = Database(cfg.db_path)
    try:
        opps = Pipeline(cfg, db).run_once()
    finally:
        db.close()
    print(f"\nFound {len(opps)} opportunities (margin >= {cfg.margin_threshold_pct}%):\n")
    from .alerts.base import format_digest_text

    if opps:
        print(format_digest_text(opps[: max(cfg.email.top_n, 10)]))
    else:
        print("(none cleared the threshold this cycle)")


def cmd_run(args):
    cfg = _load(args)
    from .scheduler import Scheduler

    Scheduler(cfg).run()


def cmd_serve(args):
    cfg = _load(args)
    from .dashboard.app import create_app

    app = create_app(cfg)
    log.info("dashboard at http://%s:%d", cfg.dashboard.host, cfg.dashboard.port)
    app.run(host=cfg.dashboard.host, port=cfg.dashboard.port)


def cmd_test_alert(args):
    cfg = _load(args)
    from .pipeline import Pipeline

    db = Database(cfg.db_path)
    try:
        opps = Pipeline(cfg, db).run_once()
    finally:
        db.close()
    from .alerts.email_alert import EmailAlerter

    sent = EmailAlerter(cfg.email).send(opps)
    print("email sent" if sent else "email NOT sent (check alerts.email config / enabled flag)")


def cmd_init_db(args):
    cfg = _load(args)
    Database(cfg.db_path).close()
    print(f"initialized database at {cfg.db_path}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="arb", description="Auction arbitrage MVP")
    p.add_argument("-c", "--config", default="config.yaml", help="path to config YAML")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("run-once", help="run a single poll cycle").set_defaults(func=cmd_run_once)
    sub.add_parser("run", help="run scheduled polling").set_defaults(func=cmd_run)
    sub.add_parser("serve", help="launch the dashboard").set_defaults(func=cmd_serve)
    sub.add_parser("test-alert", help="run once and send an email alert").set_defaults(func=cmd_test_alert)
    sub.add_parser("init-db", help="create the SQLite schema").set_defaults(func=cmd_init_db)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
