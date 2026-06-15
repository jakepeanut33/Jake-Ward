"""Config loading and validation.

A single YAML file drives the whole tool: sources, categories, fee assumptions,
margin threshold, poll interval, and alert targets. Secrets may be supplied via
environment variables so they need not live in the file.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

import yaml


@dataclass
class CategoryConfig:
    key: str
    label: str = ""
    sold_comp_window: int = 10
    min_comps: int = 5


@dataclass
class SourceConfig:
    name: str
    type: str
    enabled: bool = True
    category: str = ""
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompsConfig:
    type: str = "csv"
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FeesConfig:
    buyer_premium_pct: float = 0.0
    sales_tax_pct: float = 0.0
    default_inbound_shipping: float = 0.0
    marketplace_fee_pct: float = 13.25
    payment_fee_pct: float = 2.9
    payment_fee_fixed: float = 0.30
    outbound_shipping: float = 0.0


@dataclass
class BidProjectionConfig:
    multiplier: float = 1.0
    min_increment: float = 1.0


@dataclass
class ScoringConfig:
    profit_weight: float = 1.0
    margin_weight: float = 100.0
    low_confidence_penalty: float = 0.5
    ending_soon_minutes: float = 30.0
    ending_soon_penalty: float = 0.5


@dataclass
class EmailConfig:
    enabled: bool = False
    top_n: int = 5
    smtp_host: str = ""
    smtp_port: int = 587
    use_tls: bool = True
    username: str = ""
    password: str = ""
    from_addr: str = ""
    to_addrs: List[str] = field(default_factory=list)


@dataclass
class DashboardConfig:
    host: str = "127.0.0.1"
    port: int = 8000


@dataclass
class Config:
    db_path: str = "auction_arb.db"
    poll_interval_seconds: int = 600
    margin_threshold_pct: float = 25.0
    min_profit: float = 0.0
    log_level: str = "INFO"
    categories: Dict[str, CategoryConfig] = field(default_factory=dict)
    sources: List[SourceConfig] = field(default_factory=list)
    comps: CompsConfig = field(default_factory=CompsConfig)
    fees: FeesConfig = field(default_factory=FeesConfig)
    bid_projection: BidProjectionConfig = field(default_factory=BidProjectionConfig)
    scoring: ScoringConfig = field(default_factory=ScoringConfig)
    email: EmailConfig = field(default_factory=EmailConfig)
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)


def _only(d: Dict[str, Any], keys) -> Dict[str, Any]:
    """Return the subset of d whose keys are in `keys` (ignore unknown keys)."""
    return {k: v for k, v in d.items() if k in keys}


def load_config(path: str) -> Config:
    """Load and validate config from a YAML file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    cfg = Config()
    cfg.db_path = data.get("db_path", cfg.db_path)
    cfg.poll_interval_seconds = int(data.get("poll_interval_seconds", cfg.poll_interval_seconds))
    cfg.margin_threshold_pct = float(data.get("margin_threshold_pct", cfg.margin_threshold_pct))
    cfg.min_profit = float(data.get("min_profit", cfg.min_profit))
    cfg.log_level = data.get("log_level", cfg.log_level)

    # categories
    for key, c in (data.get("categories") or {}).items():
        c = c or {}
        cfg.categories[key] = CategoryConfig(
            key=key,
            label=c.get("label", key),
            sold_comp_window=int(c.get("sold_comp_window", 10)),
            min_comps=int(c.get("min_comps", 5)),
        )

    # sources -- everything that isn't a known field is kept under `options`
    known_src = {"name", "type", "enabled", "category"}
    for s in (data.get("sources") or []):
        if not s.get("name") or not s.get("type"):
            raise ValueError(f"source entry missing name/type: {s!r}")
        cfg.sources.append(
            SourceConfig(
                name=s["name"],
                type=s["type"],
                enabled=bool(s.get("enabled", True)),
                category=s.get("category", ""),
                options={k: v for k, v in s.items() if k not in known_src},
            )
        )

    # comps
    comps = data.get("comps") or {}
    cfg.comps = CompsConfig(
        type=comps.get("type", "csv"),
        options={k: v for k, v in comps.items() if k != "type"},
    )

    # fees / bid projection / scoring / dashboard
    fees = data.get("fees") or {}
    cfg.fees = FeesConfig(**_only(fees, FeesConfig.__dataclass_fields__))

    bp = data.get("bid_projection") or {}
    cfg.bid_projection = BidProjectionConfig(**_only(bp, BidProjectionConfig.__dataclass_fields__))

    sc = data.get("scoring") or {}
    cfg.scoring = ScoringConfig(**_only(sc, ScoringConfig.__dataclass_fields__))

    dash = data.get("dashboard") or {}
    cfg.dashboard = DashboardConfig(**_only(dash, DashboardConfig.__dataclass_fields__))

    # alerts.email (with env fallback for the password)
    email = ((data.get("alerts") or {}).get("email")) or {}
    cfg.email = EmailConfig(**_only(email, EmailConfig.__dataclass_fields__))
    cfg.email.password = cfg.email.password or os.environ.get("EMAIL_PASSWORD", "")

    _validate(cfg)
    return cfg


def _validate(cfg: Config) -> None:
    if cfg.poll_interval_seconds <= 0:
        raise ValueError("poll_interval_seconds must be > 0")
    if not cfg.sources:
        raise ValueError("no sources configured")
    for s in cfg.sources:
        if s.category and s.category not in cfg.categories:
            raise ValueError(
                f"source {s.name!r} references unknown category {s.category!r}"
            )
