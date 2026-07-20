"""afbws/gp.channel.v1.json — schema-first `gp` (graphic primitive) channel
(AFB backend<->AFB frontend only). Negotiated via auth.support/auth_ok.support;
not part of the afb.execution.v1 AFB<->BF wire."""
from __future__ import annotations

import json

import pytest

GP_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/gp.channel.v1.json"

_GP_ITEM = {
    "schema": "afb.gp.v1",
    "id": "gp-1",
    "ticker": "SBER",
    "kind": "line",
    "start": {"time": 1721000000, "price": 123.45},
}


def _validator(def_name: str, registry):
    """Full-URI $ref so internal cross-refs resolve against the whole
    document — see test_afbws_alarm_channel_schema.py::_validator."""
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{GP_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- get ---------------------------------------------------------------

def test_get_request_valid(registry):
    msg = {"channel": "gp", "schema": "afbws.gp.get.request.v1", "request_id": "req-1", "id": "gp-1"}
    _validator("getRequest", registry).validate(msg)  # does not raise


def test_get_response_valid(registry):
    msg = {
        "channel": "gp", "schema": "afbws.gp.get.response.v1", "request_id": "req-1",
        "item": _GP_ITEM,
    }
    _validator("getResponse", registry).validate(msg)  # does not raise


def test_get_request_missing_schema_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "gp", "request_id": "req-1", "id": "gp-1"}
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_wrong_channel_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "alarm", "schema": "afbws.gp.get.request.v1", "request_id": "req-1", "id": "gp-1"}
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_extra_field_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "gp", "schema": "afbws.gp.get.request.v1", "request_id": "req-1",
        "id": "gp-1", "unexpected": "nope",
    }
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


# --- list ----------------------------------------------------------------

def test_list_request_ticker_optional(registry):
    msg = {"channel": "gp", "schema": "afbws.gp.list.request.v1", "request_id": "req-1"}
    _validator("listRequest", registry).validate(msg)  # does not raise


def test_list_request_with_ticker_valid(registry):
    msg = {"channel": "gp", "schema": "afbws.gp.list.request.v1", "request_id": "req-1", "ticker": "SBER"}
    _validator("listRequest", registry).validate(msg)  # does not raise


def test_list_response_valid(registry):
    msg = {
        "channel": "gp", "schema": "afbws.gp.list.response.v1", "request_id": "req-1",
        "items": [_GP_ITEM],
    }
    _validator("listResponse", registry).validate(msg)  # does not raise


def test_list_response_item_without_schema_rejected(registry):
    from jsonschema import ValidationError

    bad_item = {k: v for k, v in _GP_ITEM.items() if k != "schema"}
    msg = {
        "channel": "gp", "schema": "afbws.gp.list.response.v1", "request_id": "req-1",
        "items": [bad_item],
    }
    with pytest.raises(ValidationError):
        _validator("listResponse", registry).validate(msg)


def test_list_response_item_with_used_in_tradeplans_rejected(registry):
    from jsonschema import ValidationError

    bad_item = {**_GP_ITEM, "used_in_tradeplans": True}
    msg = {
        "channel": "gp", "schema": "afbws.gp.list.response.v1", "request_id": "req-1",
        "items": [bad_item],
    }
    with pytest.raises(ValidationError):
        _validator("listResponse", registry).validate(msg)


# --- set / delete ----------------------------------------------------------

def test_set_request_valid(registry):
    msg = {
        "channel": "gp", "schema": "afbws.gp.set.request.v1", "request_id": "req-1",
        "item": _GP_ITEM,
    }
    _validator("setRequest", registry).validate(msg)  # does not raise


def test_set_request_move_is_a_plain_set(registry):
    """Moving a primitive (new start) is the exact same request shape as
    creating/editing one — no separate `move` command exists."""
    moved = {**_GP_ITEM, "start": {"time": 1721003600, "price": 130.0}}
    msg = {
        "channel": "gp", "schema": "afbws.gp.set.request.v1", "request_id": "req-1",
        "item": moved,
    }
    _validator("setRequest", registry).validate(msg)  # does not raise


def test_set_request_item_missing_schema_rejected(registry):
    from jsonschema import ValidationError

    bad_item = {k: v for k, v in _GP_ITEM.items() if k != "schema"}
    msg = {
        "channel": "gp", "schema": "afbws.gp.set.request.v1", "request_id": "req-1",
        "item": bad_item,
    }
    with pytest.raises(ValidationError):
        _validator("setRequest", registry).validate(msg)


def test_delete_request_and_response_valid(registry):
    req = {"channel": "gp", "schema": "afbws.gp.delete.request.v1", "request_id": "req-1", "id": "gp-1"}
    _validator("deleteRequest", registry).validate(req)  # does not raise
    resp = {"channel": "gp", "schema": "afbws.gp.delete.response.v1", "request_id": "req-1", "id": "gp-1"}
    _validator("deleteResponse", registry).validate(resp)  # does not raise


# --- error, including details ------------------------------------------------

def test_error_response_minimal_valid(registry):
    msg = {
        "channel": "gp", "schema": "afbws.gp.error.response.v1", "request_id": "req-1",
        "code": "not_found", "message": "Primitive not found",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_unknown_code_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "gp", "schema": "afbws.gp.error.response.v1", "request_id": "req-1",
        "code": "totally_unknown", "message": "x",
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


def test_error_response_conflict_carries_item_and_details(registry):
    msg = {
        "channel": "gp", "schema": "afbws.gp.error.response.v1", "request_id": "req-1",
        "code": "conflict", "message": "Referenced by an active plan",
        "item": _GP_ITEM,
        "details": {
            "tradeplan_ids": ["tp-1"],
            "deal_ids": ["deal-1:bf-1"],
            "locked_scopes": ["entry", "stop_loss"],
        },
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_details_rejects_unknown_scope(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "gp", "schema": "afbws.gp.error.response.v1", "request_id": "req-1",
        "code": "conflict", "message": "x",
        "details": {"locked_scopes": ["not_a_real_scope"]},
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


def test_error_response_details_rejects_extra_field(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "gp", "schema": "afbws.gp.error.response.v1", "request_id": "req-1",
        "code": "conflict", "message": "x",
        "details": {"unexpected": True},
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


# --- no move/usage/bulk-set/confirm commands --------------------------------

def test_no_move_usage_confirm_or_bulk_defs():
    """The plan explicitly rejects separate move/usage/bulk-set/confirmation
    commands — moving is a plain set(), usage is backend-computed, never
    wire concepts."""
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "gp.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    forbidden_substrings = ("move", "usage", "bulk", "confirm")
    for def_name in doc["$defs"]:
        lowered = def_name.lower()
        assert not any(s in lowered for s in forbidden_substrings), f"unexpected $def: {def_name}"


def test_no_message_def_declares_a_type_property():
    """New channels forbid `type`: routing is channel+schema only."""
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "gp.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"
