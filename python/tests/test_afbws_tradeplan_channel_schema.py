"""afbws/tradeplan.channel.v1.json — schema-first tradeplan channel (AFB
backend<->AFB frontend only). Negotiated via auth.support/auth_ok.support; not
part of the afb.execution.v1 AFB<->BF wire. `entity` covers both afb.tradeplan.v1
(schema made mandatory here, unlike its own canon file) and afb.tradeplan.v2
(already mandatory there)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

TRADEPLAN_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/tradeplan.channel.v1.json"

_V1_ITEM = {
    "schema": "afb.tradeplan.v1",
    "id": "tp1",
    "ticker": "SBER",
    "entry_condition": {"condition_type": "price", "price_value": 100},
}
_V2_ITEM = {
    "schema": "afb.tradeplan.v2",
    "id": "tp2",
    "ticker": "SBER",
    "direction": "long",
    "entries": [{"condition": {"left": {"source": "price"}, "op": "touch", "right": {"const": "100"}}}],
    "sizing": {"mode": "lots", "value": "1"},
}


def _validator(def_name: str, registry):
    """See test_afbws_alarm_channel_schema.py::_validator — full-URI $ref so
    internal cross-refs (entity -> entityV1/tradeplan.v2, amend_results ->
    amendResultItem) resolve against the whole document."""
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{TRADEPLAN_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- entity (schema-required wrapping of v1) --------------------------------

def test_entity_accepts_v1_with_explicit_schema(registry):
    _validator("entity", registry).validate(_V1_ITEM)  # does not raise


def test_entity_accepts_v2(registry):
    _validator("entity", registry).validate(_V2_ITEM)  # does not raise


def test_entity_rejects_v1_without_schema(registry):
    """Unlike the plain tradeplan.v1.json canon (schema optional for legacy
    back-compat), the new channel always requires an explicit schema."""
    from jsonschema import ValidationError

    bad = {k: v for k, v in _V1_ITEM.items() if k != "schema"}
    with pytest.raises(ValidationError):
        _validator("entity", registry).validate(bad)


# --- get ---------------------------------------------------------------

def test_get_request_valid(registry):
    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.get.request.v1",
        "request_id": "req-1",
        "id": "tp1",
    }
    _validator("getRequest", registry).validate(msg)  # does not raise


def test_get_response_valid_v1_and_v2(registry):
    for item in (_V1_ITEM, _V2_ITEM):
        msg = {
            "channel": "tradeplan",
            "schema": "afbws.tradeplan.get.response.v1",
            "request_id": "req-1",
            "item": item,
        }
        _validator("getResponse", registry).validate(msg)  # does not raise


def test_get_request_wrong_channel_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "alarm",
        "schema": "afbws.tradeplan.get.request.v1",
        "request_id": "req-1",
        "id": "tp1",
    }
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_extra_field_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.get.request.v1",
        "request_id": "req-1",
        "id": "tp1",
        "unexpected": "nope",
    }
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


# --- list ----------------------------------------------------------------

def test_list_request_ticker_optional(registry):
    msg = {"channel": "tradeplan", "schema": "afbws.tradeplan.list.request.v1", "request_id": "req-1"}
    _validator("listRequest", registry).validate(msg)  # does not raise


def test_list_response_mixed_v1_v2_valid(registry):
    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.list.response.v1",
        "request_id": "req-1",
        "items": [_V1_ITEM, _V2_ITEM],
    }
    _validator("listResponse", registry).validate(msg)  # does not raise


def test_list_response_item_without_schema_rejected(registry):
    from jsonschema import ValidationError

    bad_item = {k: v for k, v in _V1_ITEM.items() if k != "schema"}
    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.list.response.v1",
        "request_id": "req-1",
        "items": [bad_item],
    }
    with pytest.raises(ValidationError):
        _validator("listResponse", registry).validate(msg)


# --- set / delete ----------------------------------------------------------

def test_set_request_and_response_valid(registry):
    req = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.set.request.v1",
        "request_id": "req-1",
        "item": _V2_ITEM,
    }
    _validator("setRequest", registry).validate(req)  # does not raise
    resp = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.set.response.v1",
        "request_id": "req-1",
        "item": _V2_ITEM,
        "amend_results": [
            {"schema": "afbws.tradeplan.amend_result.v1", "deal_id": "deal-1", "accepted": True, "revision": 3}
        ],
    }
    _validator("setResponse", registry).validate(resp)  # does not raise


def test_set_response_amend_result_without_schema_rejected(registry):
    from jsonschema import ValidationError

    resp = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.set.response.v1",
        "request_id": "req-1",
        "item": _V2_ITEM,
        "amend_results": [{"deal_id": "deal-1", "accepted": True}],
    }
    with pytest.raises(ValidationError):
        _validator("setResponse", registry).validate(resp)


def test_set_response_requires_amend_results_key(registry):
    from jsonschema import ValidationError

    resp = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.set.response.v1",
        "request_id": "req-1",
        "item": _V2_ITEM,
    }
    with pytest.raises(ValidationError):
        _validator("setResponse", registry).validate(resp)


def test_delete_request_valid(registry):
    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.delete.request.v1",
        "request_id": "req-1",
        "id": "tp1",
    }
    _validator("deleteRequest", registry).validate(msg)  # does not raise


# --- error (with optional conflict item) ------------------------------------

def test_error_response_valid_without_item(registry):
    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.error.response.v1",
        "request_id": "req-1",
        "code": "not_found",
        "message": "Plan not found",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_conflict_carries_current_item(registry):
    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.error.response.v1",
        "request_id": "req-1",
        "code": "conflict",
        "message": "Deal already entered position",
        "item": _V2_ITEM,
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_unknown_code_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.error.response.v1",
        "request_id": "req-1",
        "code": "totally_unknown",
        "message": "x",
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


# --- sync push ---------------------------------------------------------------

def test_sync_push_valid(registry):
    msg = {
        "channel": "tradeplan",
        "schema": "afbws.tradeplan.sync.push.v1",
        "items": [_V1_ITEM, _V2_ITEM],
    }
    _validator("syncPush", registry).validate(msg)  # does not raise


def test_sync_push_has_no_request_id_property(registry):
    """Server-initiated push, not correlated to a request."""
    resolved = registry[TRADEPLAN_CHANNEL_ID]
    assert "request_id" not in resolved.contents["$defs"]["syncPush"]["properties"]


def test_no_message_def_declares_a_type_property():
    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "tradeplan.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"
