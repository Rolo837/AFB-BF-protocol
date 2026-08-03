"""session.hello / session.hello_ack accept the v1.10.0 margin_trading fields."""
from __future__ import annotations

import json

import pytest
from jsonschema import Draft202012Validator

from conftest import SPEC_SCHEMAS


def _payload_schema(msg_type: str) -> dict:
    return json.loads((SPEC_SCHEMAS / "payloads" / f"{msg_type}.json").read_text())


def test_hello_accepts_margin_trading(registry):
    schema = _payload_schema("session.hello")
    payload = {
        "bf_id": "bf-1",
        "nonce": "n1",
        "protocol": "afb.execution.v1",
        "dry_run": True,
        "margin_trading": False,
    }
    Draft202012Validator(schema, registry=registry).validate(payload)


def test_hello_accepts_heartbeat_interval_sec(registry):
    schema = _payload_schema("session.hello")
    payload = {
        "bf_id": "bf-1",
        "nonce": "n1",
        "protocol": "afb.execution.v1",
        "heartbeat_interval_sec": 120,
    }
    Draft202012Validator(schema, registry=registry).validate(payload)


def test_hello_rejects_non_positive_heartbeat_interval(registry):
    schema = _payload_schema("session.hello")
    payload = {
        "bf_id": "bf-1",
        "nonce": "n1",
        "protocol": "afb.execution.v1",
        "heartbeat_interval_sec": 0,
    }
    with pytest.raises(Exception):
        Draft202012Validator(schema, registry=registry).validate(payload)


def test_hello_ack_split_fields_still_valid_but_deprecated(registry):
    """deprecated fields remain schema-valid for wire compatibility."""
    schema = _payload_schema("session.hello_ack")
    for field in ("dry_run_afb", "dry_run_bf", "margin_trading_afb", "margin_trading_bf"):
        assert schema["properties"][field].get("deprecated") is True
    payload = {
        "protocol": "afb.execution.v1",
        "dry_run": True,
        "dry_run_afb": True,
        "dry_run_bf": False,
        "margin_trading": False,
        "margin_trading_afb": False,
        "margin_trading_bf": True,
        "heartbeat_interval_sec": 60,
    }
    Draft202012Validator(schema, registry=registry).validate(payload)


def test_hello_ack_accepts_margin_trading_trio(registry):
    schema = _payload_schema("session.hello_ack")
    payload = {
        "protocol": "afb.execution.v1",
        "accepted_protocol": "afb.execution.v1",
        "dry_run": True,
        "dry_run_afb": True,
        "dry_run_bf": False,
        "margin_trading": False,
        "margin_trading_afb": False,
        "margin_trading_bf": True,
    }
    Draft202012Validator(schema, registry=registry).validate(payload)


def test_hello_ack_rejects_non_boolean_margin_trading(registry):
    schema = _payload_schema("session.hello_ack")
    payload = {"protocol": "afb.execution.v1", "margin_trading": "yes"}
    with pytest.raises(Exception):
        Draft202012Validator(schema, registry=registry).validate(payload)
