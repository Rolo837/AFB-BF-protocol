"""afbws/account.channel.v1.json — schema-first account channel (AFB backend
<->AFB frontend only). Negotiated via auth.support/auth_ok.support; not part
of the afb.execution.v1 AFB<->BF wire. `account` means a broker account (one
bf_id/connector may have more than one — see broker.get_accounts/
broker.accounts on the AFB<->BF wire), not the connector itself."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ACCOUNT_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/account.channel.v1.json"

_SNAPSHOT = {
    "bf_id": "bf-main",
    "account_id": "1899011",
    "tradable": True,
    "readonly": False,
    "status": "ok",
    "equity": "152340.11",
    "cash": [{"currency": "RUB", "value": "12000"}],
    "positions": [
        {"quantity": 10, "average_price": "280.5", "current_price": "281.0", "unrealized_pnl": "5.0"}
    ],
}
_ORDER = {
    "order_id": "ord-1",
    "deal_id": "deal-1",
    "symbol": "SBER@MISX",
    "side": "buy",
    "role": "entry",
    "status": "filled",
    "quantity": 10,
    "filled_quantity": 10,
    "limit_price": "280.5",
    "average_price": "280.5",
    "updated_at": "2026-01-01T00:00:00Z",
}
_EVENT_RECORD = {
    "logged_at": "2026-01-01T00:00:00Z",
    "bf_id": "bf-main",
    "deal_id": "deal-1",
    "category": "order",
    "event": "filled",
    "data": {"order_id": "ord-1"},
}


def _validator(def_name: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{ACCOUNT_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- list ------------------------------------------------------------------

def test_list_request_valid_with_and_without_bf_id(registry):
    _validator("listRequest", registry).validate(
        {"channel": "account", "schema": "afbws.account.list.request.v1", "request_id": "req-1"}
    )
    _validator("listRequest", registry).validate(
        {"channel": "account", "schema": "afbws.account.list.request.v1", "request_id": "req-1", "bf_id": "bf-main", "force": True}
    )


def test_list_response_valid(registry):
    msg = {"channel": "account", "schema": "afbws.account.list.response.v1", "request_id": "req-1", "items": [_SNAPSHOT]}
    _validator("listResponse", registry).validate(msg)  # does not raise


# --- get ---------------------------------------------------------------

def test_get_request_valid_with_and_without_account_id(registry):
    _validator("getRequest", registry).validate(
        {"channel": "account", "schema": "afbws.account.get.request.v1", "request_id": "req-1", "bf_id": "bf-main"}
    )
    _validator("getRequest", registry).validate(
        {"channel": "account", "schema": "afbws.account.get.request.v1", "request_id": "req-1", "bf_id": "bf-main", "account_id": "1899012"}
    )


def test_get_request_requires_bf_id(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(
            {"channel": "account", "schema": "afbws.account.get.request.v1", "request_id": "req-1"}
        )


def test_get_response_valid(registry):
    msg = {"channel": "account", "schema": "afbws.account.get.response.v1", "request_id": "req-1", "item": _SNAPSHOT}
    _validator("getResponse", registry).validate(msg)  # does not raise


def test_account_snapshot_rejects_broker_account_id(registry):
    """The account_id/broker_account_id duplication in the deprecated
    broker.account is deliberately not carried into this projection."""
    from jsonschema import ValidationError

    bad = {**_SNAPSHOT, "broker_account_id": "1899011"}
    with pytest.raises(ValidationError):
        _validator("accountSnapshot", registry).validate(bad)


# --- orders ------------------------------------------------------------

def test_orders_request_response_valid(registry):
    req = {"channel": "account", "schema": "afbws.account.orders.request.v1", "request_id": "req-1", "bf_id": "bf-main"}
    _validator("ordersRequest", registry).validate(req)  # does not raise

    resp = {
        "channel": "account",
        "schema": "afbws.account.orders.response.v1",
        "request_id": "req-1",
        "bf_id": "bf-main",
        "account_id": "1899011",
        "items": [_ORDER],
    }
    _validator("ordersResponse", registry).validate(resp)  # does not raise


def test_order_only_requires_order_id(registry):
    """symbol/client_order_id/cancel_source are AFB/frontend-synthesized or
    simply absent from BF's wire shape — see payloads/broker.orders.json."""
    _validator("order", registry).validate({"order_id": "ord-1"})  # does not raise


def test_order_rejects_unknown_field(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("order", registry).validate({"order_id": "ord-1", "not_a_real_field": 1})


# --- events (unchanged from legacy account/get_events) ------------------

def test_events_request_response_valid(registry):
    req = {"channel": "account", "schema": "afbws.account.events.request.v1", "request_id": "req-1", "bf_id": "bf-main", "date": "2026-01-01"}
    _validator("eventsRequest", registry).validate(req)  # does not raise

    resp = {
        "channel": "account",
        "schema": "afbws.account.events.response.v1",
        "request_id": "req-1",
        "bf_id": "bf-main",
        "date": "2026-01-01",
        "items": [_EVENT_RECORD],
    }
    _validator("eventsResponse", registry).validate(resp)  # does not raise


def test_event_record_category_enum(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("eventRecord", registry).validate({**_EVENT_RECORD, "category": "not_a_real_category"})


# --- error ---------------------------------------------------------------

@pytest.mark.parametrize(
    "code",
    ["not_found", "invalid_schema", "validation_error", "forbidden", "conflict", "bf_offline", "unsupported_action", "internal_error"],
)
def test_error_response_known_codes(registry, code):
    msg = {"channel": "account", "schema": "afbws.account.error.response.v1", "request_id": "req-1", "code": code, "message": "x"}
    _validator("errorResponse", registry).validate(msg)  # does not raise


# --- pushes ----------------------------------------------------------------

def test_snapshot_push_valid_and_has_no_request_id(registry):
    msg = {
        "channel": "account",
        "schema": "afbws.account.snapshot.push.v1",
        "bf_id": "bf-main",
        "default_account_id": "1899011",
        "items": [_SNAPSHOT],
    }
    _validator("snapshotPush", registry).validate(msg)  # does not raise

    schema_path = Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "account.channel.v1.json"
    doc = json.loads(schema_path.read_text())
    assert "request_id" not in doc["$defs"]["snapshotPush"]["properties"]


def test_orders_push_valid_and_has_no_request_id(registry):
    msg = {
        "channel": "account",
        "schema": "afbws.account.orders.push.v1",
        "bf_id": "bf-main",
        "account_id": "1899011",
        "items": [_ORDER],
    }
    _validator("ordersPush", registry).validate(msg)  # does not raise

    schema_path = Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "account.channel.v1.json"
    doc = json.loads(schema_path.read_text())
    assert "request_id" not in doc["$defs"]["ordersPush"]["properties"]


# --- no `type` field anywhere ------------------------------------------

def test_no_message_def_declares_a_type_property():
    schema_path = Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "account.channel.v1.json"
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"


def test_wrong_channel_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "deal", "schema": "afbws.account.list.request.v1", "request_id": "req-1"}
    with pytest.raises(ValidationError):
        _validator("listRequest", registry).validate(msg)
