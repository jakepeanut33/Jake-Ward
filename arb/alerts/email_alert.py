"""Email alerts via SMTP."""
from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import List

from ..config import EmailConfig
from ..logging_setup import get_logger
from ..models import Opportunity
from .base import format_digest_text

log = get_logger("alerts.email")


class EmailAlerter:
    def __init__(self, cfg: EmailConfig):
        self.cfg = cfg

    def _validate(self) -> None:
        missing = [
            k for k in ("smtp_host", "from_addr")
            if not getattr(self.cfg, k)
        ]
        if not self.cfg.to_addrs:
            missing.append("to_addrs")
        if missing:
            raise ValueError(f"email config incomplete: missing {', '.join(missing)}")

    def send(self, opps: List[Opportunity]) -> bool:
        """Send a digest of the given opportunities. Returns True on success."""
        if not self.cfg.enabled:
            log.info("email alerts disabled; skipping")
            return False
        if not opps:
            log.info("no opportunities to alert on")
            return False
        self._validate()

        top = opps[: self.cfg.top_n]
        msg = EmailMessage()
        msg["Subject"] = f"[Auction Arb] {len(top)} flip opportunit{'y' if len(top) == 1 else 'ies'}"
        msg["From"] = self.cfg.from_addr
        msg["To"] = ", ".join(self.cfg.to_addrs)
        msg.set_content(format_digest_text(top))

        try:
            with smtplib.SMTP(self.cfg.smtp_host, self.cfg.smtp_port, timeout=30) as server:
                if self.cfg.use_tls:
                    server.starttls()
                if self.cfg.username:
                    server.login(self.cfg.username, self.cfg.password)
                server.send_message(msg)
            log.info("sent email alert with %d opportunities to %s",
                     len(top), ", ".join(self.cfg.to_addrs))
            return True
        except Exception as exc:  # noqa: BLE001 - alerting must never crash the pipeline
            log.error("failed to send email alert: %s", exc)
            return False
