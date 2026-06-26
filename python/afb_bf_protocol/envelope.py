"""Canonicalisation, hashing and envelope construction.

Canonical JSON and the signing string are the byte-for-byte compatibility
contract with the prior AFB and BF implementations:

* ``canonical_json``  -> ``json.dumps(sort_keys=True, separators=(",", ":"),
  ensure_ascii=False)`` (BF returned ``str``, AFB returned ``bytes`` of the same
  text; unified here on ``str``).
* ``payload_hash``    -> ``sha256(canonical_json(payload).encode("utf-8")).hexdigest()``.
* ``signing_string``  -> ``"{protocol}|{type}|{message_id}|{created_at}|{payload_hash}"``.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from .models import Envelope, Signature
from .version import PROTOCOL_VERSION

__all__ = [
    "canonical_json",
    "payload_hash",
    "signing_string",
    "parse_iso_datetime",
    "make_envelope",
]


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def payload_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def signing_string(envelope: Envelope) -> str:
    return "|".join(
        [
            envelope.protocol,
            envelope.type,
            envelope.message_id,
            envelope.created_at,
            envelope.payload_hash,
        ]
    )


def parse_iso_datetime(value: str) -> datetime:
    s = str(value or "").strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def make_envelope(
    *,
    sender: str,
    recipient: str,
    msg_type: str,
    payload: dict[str, Any],
    key_id: str,
    ttl_sec: int = 300,
    correlation_id: str | None = None,
    causation_id: str | None = None,
    idempotency_key: str = "",
    message_id: str | None = None,
    created_at: str | None = None,
) -> Envelope:
    """Build an unsigned envelope with ``payload_hash`` and ``expires_at`` filled in.

    The ``signature.value`` is empty until ``signing.sign_envelope`` is applied.
    """
    created = created_at or datetime.now(timezone.utc).isoformat()
    expires = (parse_iso_datetime(created) + timedelta(seconds=max(1, int(ttl_sec)))).isoformat()
    return Envelope(
        protocol=PROTOCOL_VERSION,
        message_id=message_id or str(uuid.uuid4()),
        correlation_id=correlation_id,
        causation_id=causation_id,
        sender=sender,
        recipient=recipient,
        type=msg_type,
        created_at=created,
        expires_at=expires,
        idempotency_key=idempotency_key,
        payload_hash=payload_hash(payload),
        payload=payload,
        signature=Signature(alg="Ed25519", key_id=key_id, value=""),
    )
