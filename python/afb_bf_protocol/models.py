"""Wire models for the AFB <-> BF execution protocol.

Single canonical envelope shape, unifying the two implementations that had
drifted (BF ``Envelope`` with a nested ``Signature`` and a required
``idempotency_key``; AFB ``ExecutionEnvelope`` with ``signature: dict`` and an
optional key). Here ``idempotency_key`` is a single ``str`` type; ``from_dict``
coerces a missing/``None`` value to ``""`` so parsing stays lenient while the
constructed type is consistent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .version import PROTOCOL_VERSION

__all__ = ["PROTOCOL_VERSION", "Signature", "Envelope", "ExecutionDeal"]


@dataclass
class Signature:
    alg: str
    key_id: str
    value: str

    def to_dict(self) -> dict[str, Any]:
        return {"alg": self.alg, "key_id": self.key_id, "value": self.value}

    @classmethod
    def from_dict(cls, data: Any) -> "Signature":
        if not isinstance(data, dict):
            raise ValueError("signature must be an object")
        return cls(
            alg=str(data.get("alg") or ""),
            key_id=str(data.get("key_id") or ""),
            value=str(data.get("value") or ""),
        )


def _opt_str(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


@dataclass
class Envelope:
    protocol: str
    message_id: str
    sender: str
    recipient: str
    type: str
    created_at: str
    expires_at: str
    idempotency_key: str
    payload_hash: str
    payload: dict[str, Any]
    signature: Signature
    correlation_id: str | None = None
    causation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol": self.protocol,
            "message_id": self.message_id,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "type": self.type,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "idempotency_key": self.idempotency_key,
            "payload_hash": self.payload_hash,
            "payload": self.payload,
            "signature": self.signature.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Any) -> "Envelope":
        if not isinstance(data, dict):
            raise ValueError("envelope must be an object")
        payload = data.get("payload")
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")
        return cls(
            protocol=str(data["protocol"]),
            message_id=str(data["message_id"]),
            correlation_id=_opt_str(data.get("correlation_id")),
            causation_id=_opt_str(data.get("causation_id")),
            sender=str(data["sender"]),
            recipient=str(data["recipient"]),
            type=str(data["type"]),
            created_at=str(data["created_at"]),
            expires_at=str(data["expires_at"]),
            idempotency_key=str(data.get("idempotency_key") or ""),
            payload_hash=str(data["payload_hash"]),
            payload=payload,
            signature=Signature.from_dict(data.get("signature")),
        )


@dataclass
class ExecutionDeal:
    """Thin accessor over a deal payload (``afb.deal.v1`` / ``afb.deal.v2``)."""

    deal_id: str
    revision: int
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, deal: dict[str, Any]) -> "ExecutionDeal":
        return cls(deal_id=deal["deal_id"], revision=int(deal["revision"]), raw=deal)

    @property
    def schema(self) -> str:
        return str(self.raw.get("schema") or "")
