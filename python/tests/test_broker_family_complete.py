"""Closes out the broker.* message family (see the account-channel migration
plan, P0.6): every broker.* type must have a payload schema, and the pairs
superseded by broker.get_accounts/broker.accounts and
broker.resolve_instrument/broker.instrument_resolved stay in the taxonomy as
`deprecated`, not removed (removal is a MAJOR, forbidden by default)."""
from __future__ import annotations

import json

from afb_bf_protocol import BF_EVENT_TYPES, COMMAND_TYPES, MESSAGE_REGISTRY
from conftest import REPO_ROOT

_DEPRECATED_TYPES = {
    "broker.get_account",
    "broker.account",
    "broker.get_instrument",
    "broker.instrument",
}


def test_every_broker_message_has_a_payload_schema():
    """Guard against a future broker.* type shipping without a schema — the
    whole point of this migration was to close that gap."""
    payloads_dir = REPO_ROOT / "spec" / "schemas" / "payloads"
    missing = [
        t for t, m in MESSAGE_REGISTRY.items()
        if m.category == "broker" and not (payloads_dir / f"{t}.json").exists()
    ]
    assert missing == [], f"broker.* types without a payload schema: {missing}"


def test_deprecated_broker_pairs_are_tagged_in_spec():
    spec = json.loads(_yaml_to_json())
    messages = spec["components"]["messages"]
    for key, msg in messages.items():
        msg_type = msg["name"]
        if msg_type not in _DEPRECATED_TYPES:
            continue
        tags = {t["name"] for t in msg.get("tags", [])}
        assert "deprecated" in tags, f"{msg_type} must carry the 'deprecated' tag"


def test_deprecated_broker_types_remain_in_taxonomy():
    """Depreciation != removal — see VERSIONING.md §4."""
    for msg_type in _DEPRECATED_TYPES:
        assert msg_type in MESSAGE_REGISTRY
        assert msg_type in COMMAND_TYPES or msg_type in BF_EVENT_TYPES


def test_replacement_pairs_are_not_deprecated():
    for msg_type in (
        "broker.get_accounts", "broker.accounts",
        "broker.resolve_instrument", "broker.instrument_resolved",
        "broker.get_orders", "broker.orders",
        "broker.get_catalog", "broker.catalog",
    ):
        assert msg_type in MESSAGE_REGISTRY, msg_type


def _yaml_to_json() -> str:
    import yaml

    spec = yaml.safe_load((REPO_ROOT / "spec" / "asyncapi.yaml").read_text())
    return json.dumps(spec)
