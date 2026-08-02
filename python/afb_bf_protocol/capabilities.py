"""Capability IDs for schema-first afbws channels (x-afbws-support-id).

DO NOT EDIT BY HAND — regenerated from spec/schemas/afbws/*.json by
``tools/generate.py`` (scans each schema's top-level "x-afbws-support-id").
Edit the schema's x-afbws-support-id, then run ``afb-bf-protocol-generate``.

These ids are negotiated in the AFB WS handshake (auth.support /
auth_ok.support) between AFB backend and AFB frontend — they are NOT part
of the afb.execution.v1 AFB<->BF taxonomy (see taxonomy.py).
"""
from __future__ import annotations

__all__ = [
    "ACCOUNT_CHANNEL_V1",
    "ALARM_CHANNEL_V1",
    "DEAL_CHANNEL_V1",
    "GP_CHANNEL_V1",
    "INSTRUMENT_CHANNEL_V1",
    "LINK_CHANNEL_V1",
    "TRADEPLAN_CHANNEL_V1",
    "ALL_CAPABILITY_IDS",
]

ACCOUNT_CHANNEL_V1 = "afbws.account.channel.v1"
ALARM_CHANNEL_V1 = "afbws.alarm.channel.v1"
DEAL_CHANNEL_V1 = "afbws.deal.channel.v1"
GP_CHANNEL_V1 = "afbws.gp.channel.v1"
INSTRUMENT_CHANNEL_V1 = "afbws.instrument.channel.v1"
LINK_CHANNEL_V1 = "afbws.link.channel.v1"
TRADEPLAN_CHANNEL_V1 = "afbws.tradeplan.channel.v1"

ALL_CAPABILITY_IDS: frozenset[str] = frozenset({
    ACCOUNT_CHANNEL_V1,
    ALARM_CHANNEL_V1,
    DEAL_CHANNEL_V1,
    GP_CHANNEL_V1,
    INSTRUMENT_CHANNEL_V1,
    LINK_CHANNEL_V1,
    TRADEPLAN_CHANNEL_V1,
})
