"""afbws/alarm.channel.v1.json — schema-first alarm channel (AFB backend<->AFB
frontend only). Negotiated via auth.support/auth_ok.support; not part of the
afb.execution.v1 AFB<->BF wire. Validated as dict literals directly against the
channel schema's $defs (no fixture files — see test_alarm_schema.py for the
plain afb.alarm.v1 domain-schema examples reused here as `item`)."""
from __future__ import annotations

import json

import pytest

from conftest import EXAMPLES

ALARM_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/alarm.channel.v1.json"

_ALARM_ITEM = json.loads((EXAMPLES / "alarms" / "alarm.touch.json").read_text())


def _validator(def_name: str, registry):
    """Validate against a named $def of the channel file via a full-URI $ref,
    so its own internal `#/$defs/...` cross-refs (e.g. errorResponse's shared
    errorCode, triggeredPush's events->triggerEvent) resolve against the whole
    document rather than the extracted fragment alone."""
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{ALARM_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- get ---------------------------------------------------------------

def test_get_request_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.get.request.v1",
        "request_id": "req-1",
        "id": "alarm-1",
    }
    _validator("getRequest", registry).validate(msg)  # does not raise


def test_get_response_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.get.response.v1",
        "request_id": "req-1",
        "item": _ALARM_ITEM,
    }
    _validator("getResponse", registry).validate(msg)  # does not raise


def test_get_request_missing_schema_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "alarm", "request_id": "req-1", "id": "alarm-1"}
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_wrong_channel_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "tradeplan",
        "schema": "afbws.alarm.get.request.v1",
        "request_id": "req-1",
        "id": "alarm-1",
    }
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_extra_field_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.get.request.v1",
        "request_id": "req-1",
        "id": "alarm-1",
        "unexpected": "nope",
    }
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_missing_request_id_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "alarm", "schema": "afbws.alarm.get.request.v1", "id": "alarm-1"}
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


# --- list ----------------------------------------------------------------

def test_list_request_ticker_optional(registry):
    msg = {"channel": "alarm", "schema": "afbws.alarm.list.request.v1", "request_id": "req-1"}
    _validator("listRequest", registry).validate(msg)  # does not raise


def test_list_response_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.list.response.v1",
        "request_id": "req-1",
        "items": [_ALARM_ITEM],
    }
    _validator("listResponse", registry).validate(msg)  # does not raise


def test_list_response_item_without_schema_rejected(registry):
    from jsonschema import ValidationError

    bad_item = {k: v for k, v in _ALARM_ITEM.items() if k != "schema"}
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.list.response.v1",
        "request_id": "req-1",
        "items": [bad_item],
    }
    with pytest.raises(ValidationError):
        _validator("listResponse", registry).validate(msg)


# --- set / delete ----------------------------------------------------------

def test_set_request_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.set.request.v1",
        "request_id": "req-1",
        "item": _ALARM_ITEM,
    }
    _validator("setRequest", registry).validate(msg)  # does not raise


def test_set_request_item_missing_schema_rejected(registry):
    from jsonschema import ValidationError

    bad_item = {k: v for k, v in _ALARM_ITEM.items() if k != "schema"}
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.set.request.v1",
        "request_id": "req-1",
        "item": bad_item,
    }
    with pytest.raises(ValidationError):
        _validator("setRequest", registry).validate(msg)


def test_delete_request_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.delete.request.v1",
        "request_id": "req-1",
        "id": "alarm-1",
    }
    _validator("deleteRequest", registry).validate(msg)  # does not raise


# --- error -----------------------------------------------------------------

def test_error_response_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.error.response.v1",
        "request_id": "req-1",
        "code": "not_found",
        "message": "Alarm not found",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_unknown_code_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.error.response.v1",
        "request_id": "req-1",
        "code": "totally_unknown",
        "message": "x",
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


# --- triggered push / ack ----------------------------------------------------

def test_triggered_push_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.triggered.push.v1",
        "events": [
            {
                "schema": "afb.alarm.trigger.v1",
                "alarm_id": "alarm-1",
                "triggered_at": "2026-07-20T10:00:00Z",
                "alarm": _ALARM_ITEM,
                "current_price": 123.45,
            }
        ],
    }
    _validator("triggeredPush", registry).validate(msg)  # does not raise


def test_triggered_push_event_without_schema_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.triggered.push.v1",
        "events": [
            {
                "alarm_id": "alarm-1",
                "triggered_at": "2026-07-20T10:00:00Z",
                "alarm": _ALARM_ITEM,
            }
        ],
    }
    with pytest.raises(ValidationError):
        _validator("triggeredPush", registry).validate(msg)


def test_ack_request_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.ack.request.v1",
        "request_id": "req-1",
        "events": [
            {"schema": "afb.alarm.trigger_ack.v1", "alarm_id": "alarm-1", "triggered_at": "2026-07-20T10:00:00Z"}
        ],
    }
    _validator("ackRequest", registry).validate(msg)  # does not raise


def test_ack_response_valid(registry):
    msg = {
        "channel": "alarm",
        "schema": "afbws.alarm.ack.response.v1",
        "request_id": "req-1",
        "results": [
            {
                "schema": "afbws.alarm.ack_result.v1",
                "alarm_id": "alarm-1",
                "triggered_at": "2026-07-20T10:00:00Z",
                "status": "ok",
            }
        ],
    }
    _validator("ackResponse", registry).validate(msg)  # does not raise


def test_no_message_def_declares_a_type_property():
    """New channels forbid `type`: routing is channel+schema only. Enforced
    structurally by additionalProperties:false + the declared properties list
    on every message $def, checked here so a future edit can't reintroduce it."""
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "alarm.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"
