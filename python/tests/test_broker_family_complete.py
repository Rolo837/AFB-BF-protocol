"""Closes out the broker.* message family: every broker.* type must have a
payload schema, and the legacy commands removed with BF's own catalog
(broker.get_catalog/catalog, get_instrument/instrument, get_account/account)
must be gone from the taxonomy, the spec and the schemas."""
from __future__ import annotations

import json

from afb_bf_protocol import MESSAGE_REGISTRY
from conftest import REPO_ROOT

_REMOVED_TYPES = {
    "broker.get_catalog",
    "broker.catalog",
    "broker.get_instrument",
    "broker.instrument",
    "broker.get_account",
    "broker.account",
}

_KEPT_TYPES = {
    "broker.get_accounts", "broker.accounts",
    "broker.get_orders", "broker.orders",
    "broker.resolve_instrument", "broker.instrument_resolved",
    "broker.position_ledger", "broker.error",
}


def test_every_broker_message_has_a_payload_schema():
    """Guard against a future broker.* type shipping without a schema."""
    payloads_dir = REPO_ROOT / "spec" / "schemas" / "payloads"
    missing = [
        t for t, m in MESSAGE_REGISTRY.items()
        if m.category == "broker" and not (payloads_dir / f"{t}.json").exists()
    ]
    assert missing == [], f"broker.* types without a payload schema: {missing}"


def test_broker_family_is_exactly_the_kept_set():
    assert {t for t in MESSAGE_REGISTRY if t.startswith("broker.")} == _KEPT_TYPES


def test_removed_broker_types_are_gone_everywhere():
    for msg_type in _REMOVED_TYPES:
        assert msg_type not in MESSAGE_REGISTRY, msg_type
        assert not (REPO_ROOT / "spec" / "schemas" / "payloads" / f"{msg_type}.json").exists(), msg_type
        assert not (
            REPO_ROOT / "python" / "afb_bf_protocol" / "schemas" / "payloads" / f"{msg_type}.json"
        ).exists(), msg_type
    spec = json.loads(_yaml_to_json())
    names = {m["name"] for m in spec["components"]["messages"].values()}
    assert not (names & _REMOVED_TYPES)


def test_no_deprecated_broker_messages_remain():
    spec = json.loads(_yaml_to_json())
    for msg in spec["components"]["messages"].values():
        if msg["name"].startswith("broker."):
            tags = {t["name"] for t in msg.get("tags", [])}
            assert "deprecated" not in tags, msg["name"]


def _yaml_to_json() -> str:
    import yaml

    spec = yaml.safe_load((REPO_ROOT / "spec" / "asyncapi.yaml").read_text())
    return json.dumps(spec)


def test_multi_account_and_catalog_feature_flags_removed():
    """multi_account is a constant now (always supported); features.catalog is gone."""
    caps = json.loads((REPO_ROOT / "spec" / "schemas" / "payloads" / "daemon.capabilities.json").read_text())
    assert "multi_account" not in caps["properties"]["features"]["properties"]
    assert "catalog" not in caps["properties"]["features"]["properties"]
    ack = json.loads((REPO_ROOT / "spec" / "schemas" / "payloads" / "session.hello_ack.json").read_text())
    assert "multi_account" not in ack["properties"]["features"].get("properties", {})
