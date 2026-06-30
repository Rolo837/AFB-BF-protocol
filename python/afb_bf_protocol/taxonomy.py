"""Message taxonomy for afb.execution.v1.

DO NOT EDIT BY HAND — regenerated from ``spec/asyncapi.yaml`` by
``tools/generate.py`` (the message tags ``class:*`` / ``dir:*`` / ``persisted``).
Edit the spec, then run ``afb-bf-protocol-generate``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

__all__ = [
    "SupportedMarket",
    "SUPPORTED_MARKETS",
    "MessageClass",
    "MessageDirection",
    "MessageMeta",
    "MESSAGE_REGISTRY",
    "ALL_MESSAGE_TYPES",
    "COMMAND_TYPES",
    "BF_EVENT_TYPES",
    "PERSISTED_BF_EVENT_TYPES",
    "split_category_type",
]

SupportedMarket = Literal["stock", "futures", "currency"]
SUPPORTED_MARKETS: frozenset[str] = frozenset({"stock", "futures", "currency"})

MessageClass = Literal["system", "user", "trading"]
MessageDirection = Literal["afb2bf", "bf2afb"]


@dataclass(frozen=True, slots=True)
class MessageMeta:
    message_class: MessageClass
    direction: MessageDirection
    category: str
    event: str
    persists_on_bf: bool = False


def split_category_type(message_type: str) -> tuple[str, str]:
    category, dot, event = str(message_type).partition(".")
    if not dot or not category or not event:
        raise ValueError(f"Invalid message type {message_type!r}, expected 'category.type'")
    return category, event


MESSAGE_REGISTRY: dict[str, MessageMeta] = {
    "session.hello": MessageMeta("system", "bf2afb", "session", "hello"),
    "session.heartbeat": MessageMeta("system", "bf2afb", "session", "heartbeat"),
    "session.resync_request": MessageMeta("system", "bf2afb", "session", "resync_request"),
    "session.hello_ack": MessageMeta("system", "afb2bf", "session", "hello_ack"),
    "session.resync_response": MessageMeta("system", "afb2bf", "session", "resync_response"),
    "daemon.status": MessageMeta("system", "bf2afb", "daemon", "status"),
    "daemon.capabilities": MessageMeta("system", "bf2afb", "daemon", "capabilities"),
    "daemon.error": MessageMeta("system", "bf2afb", "daemon", "error", persists_on_bf=True),
    "daemon.capabilities_query": MessageMeta("system", "afb2bf", "daemon", "capabilities_query"),
    "daemon.restart": MessageMeta("system", "afb2bf", "daemon", "restart"),
    "broker.get_account": MessageMeta("user", "afb2bf", "broker", "get_account"),
    "broker.get_orders": MessageMeta("user", "afb2bf", "broker", "get_orders"),
    "broker.get_catalog": MessageMeta("user", "afb2bf", "broker", "get_catalog"),
    "broker.get_instrument": MessageMeta("user", "afb2bf", "broker", "get_instrument"),
    "broker.resolve_instrument": MessageMeta("user", "afb2bf", "broker", "resolve_instrument"),
    "broker.account": MessageMeta("user", "bf2afb", "broker", "account"),
    "broker.orders": MessageMeta("user", "bf2afb", "broker", "orders"),
    "broker.catalog": MessageMeta("user", "bf2afb", "broker", "catalog"),
    "broker.instrument": MessageMeta("user", "bf2afb", "broker", "instrument"),
    "broker.instrument_resolved": MessageMeta("user", "bf2afb", "broker", "instrument_resolved"),
    "deal.publish": MessageMeta("user", "afb2bf", "deal", "publish"),
    "deal.operation": MessageMeta("user", "afb2bf", "deal", "operation"),
    "deal.amend": MessageMeta("user", "afb2bf", "deal", "amend"),
    "deal.resync": MessageMeta("system", "afb2bf", "deal", "resync"),
    "deal.signal": MessageMeta("system", "afb2bf", "deal", "signal"),
    "deal.accepted": MessageMeta("trading", "bf2afb", "deal", "accepted", persists_on_bf=True),
    "deal.rejected": MessageMeta("trading", "bf2afb", "deal", "rejected", persists_on_bf=True),
    "deal.status_changed": MessageMeta("trading", "bf2afb", "deal", "status_changed", persists_on_bf=True),
    "deal.archived": MessageMeta("trading", "bf2afb", "deal", "archived", persists_on_bf=True),
    "deal.orders_synced": MessageMeta("trading", "bf2afb", "deal", "orders_synced", persists_on_bf=True),
    "deal.positions_synced": MessageMeta("trading", "bf2afb", "deal", "positions_synced", persists_on_bf=True),
    "deal.report": MessageMeta("trading", "bf2afb", "deal", "report", persists_on_bf=True),
    "deal.snapshot": MessageMeta("trading", "bf2afb", "deal", "snapshot"),
    "condition.triggered": MessageMeta("trading", "bf2afb", "condition", "triggered", persists_on_bf=True),
    "order.created": MessageMeta("trading", "bf2afb", "order", "created", persists_on_bf=True),
    "order.partially_filled": MessageMeta("trading", "bf2afb", "order", "partially_filled", persists_on_bf=True),
    "order.filled": MessageMeta("trading", "bf2afb", "order", "filled", persists_on_bf=True),
    "order.cancelled": MessageMeta("trading", "bf2afb", "order", "cancelled", persists_on_bf=True),
    "order.rejected": MessageMeta("trading", "bf2afb", "order", "rejected", persists_on_bf=True),
    "position.opened": MessageMeta("trading", "bf2afb", "position", "opened", persists_on_bf=True),
    "position.changed": MessageMeta("trading", "bf2afb", "position", "changed", persists_on_bf=True),
    "position.closed": MessageMeta("trading", "bf2afb", "position", "closed", persists_on_bf=True),
}

ALL_MESSAGE_TYPES: frozenset[str] = frozenset(MESSAGE_REGISTRY.keys())
COMMAND_TYPES: frozenset[str] = frozenset(
    t for t, m in MESSAGE_REGISTRY.items() if m.direction == "afb2bf"
)
BF_EVENT_TYPES: frozenset[str] = frozenset(
    t for t, m in MESSAGE_REGISTRY.items() if m.direction == "bf2afb"
)
PERSISTED_BF_EVENT_TYPES: frozenset[str] = frozenset(
    t for t, m in MESSAGE_REGISTRY.items() if m.persists_on_bf
)
