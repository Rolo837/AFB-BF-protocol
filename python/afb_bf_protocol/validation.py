"""Envelope-level (transport) validation and replay protection.

Scope is the wire envelope only: protocol version, expiry, recipient,
``payload_hash`` integrity, and idempotency/replay tracking. Deep deal-payload
business rules (condition trees, sizing modes, v2 percent allocation) remain in
BF — they are not duplicated across projects and depend on BF domain modules.
Structural payload validation is handled declaratively by the AsyncAPI/JSON
Schemas in ``spec/``.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

from .envelope import parse_iso_datetime, payload_hash
from .version import PROTOCOL_VERSION

__all__ = [
    "ProtocolValidationError",
    "validate_envelope_fields",
    "validate_envelope_shape",
    "ReplayCache",
]


class ProtocolValidationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def validate_envelope_fields(
    data: dict[str, Any], *, expected_recipient: str | None = None
) -> None:
    """Validate a raw envelope dict (protocol / expiry / recipient)."""
    if data.get("protocol") != PROTOCOL_VERSION:
        raise ProtocolValidationError("invalid_protocol", "Unsupported protocol version")
    expires_at = parse_iso_datetime(str(data.get("expires_at") or ""))
    if datetime.now(timezone.utc) > expires_at.astimezone(timezone.utc):
        raise ProtocolValidationError("expired", "Message expired")
    if expected_recipient and data.get("recipient") != expected_recipient:
        raise ProtocolValidationError("wrong_recipient", "Envelope recipient mismatch")


def validate_envelope_shape(data: dict[str, Any], *, recipient: str) -> None:
    """Stricter check including ``payload_hash`` integrity (AFB inbound path)."""
    validate_envelope_fields(data, expected_recipient=recipient)
    payload = data.get("payload") or {}
    if payload_hash(payload) != data.get("payload_hash"):
        raise ProtocolValidationError("payload_hash_mismatch", "payload_hash mismatch")


class ReplayCache:
    """In-memory dedup of seen keys (message_id / idempotency_key) with a TTL."""

    def __init__(self, ttl_sec: int = 600) -> None:
        self.ttl_sec = max(1, int(ttl_sec))
        self._seen: dict[str, float] = {}

    def remember(self, key: str) -> bool:
        """Return True if ``key`` is new; False if seen within the TTL window."""
        now = time.time()
        cutoff = now - self.ttl_sec
        for k, ts in list(self._seen.items()):
            if ts < cutoff:
                self._seen.pop(k, None)
        if key in self._seen:
            return False
        self._seen[key] = now
        return True
