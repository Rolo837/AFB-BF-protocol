"""afbws/instrument.channel.v1.json — schema-first `instrument` channel
(AFB backend<->AFB frontend only). Negotiated via auth.support/auth_ok.support;
not part of the afb.execution.v1 AFB<->BF wire. Replaces legacy
`securities/list`, `setup/markets`+`get_assign`+`set_assign`, and
`account/get_catalog`+`get_instrument`+`resolve_instrument`."""
from __future__ import annotations

import json

import pytest

CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/instrument.channel.v1.json"

_ITEM = {
    "schema": "afb.instrument.v1",
    "ticker": "SBER",
    "exchange": "MOEX",
    "board": "TQBR",
    "market": "stock",
    "group": "Stocks",
    "source": "moex",
}

_POOL_ITEM = {**_ITEM, "group": None, "source": "arena"}


def _validator(def_name: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- list ------------------------------------------------------------------

def test_list_request_no_filters(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.list.request.v1", "request_id": "r1"}
    _validator("listRequest", registry).validate(msg)  # does not raise


def test_list_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.list.response.v1", "request_id": "r1",
        "items": [_ITEM],
        "groups": [{"key": "Stocks", "name": "Акции", "order": 3}],
        "assets": {"SBER": {"name": "Сбербанк"}},
    }
    _validator("listResponse", registry).validate(msg)  # does not raise


def test_list_response_missing_groups_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.list.response.v1", "request_id": "r1",
        "items": [_ITEM], "assets": {},
    }
    with pytest.raises(ValidationError):
        _validator("listResponse", registry).validate(msg)


# --- get ---------------------------------------------------------------

def test_get_request_and_response_valid(registry):
    req = {"channel": "instrument", "schema": "afbws.instrument.get.request.v1", "request_id": "r1", "ticker": "SBER"}
    _validator("getRequest", registry).validate(req)  # does not raise
    resp = {"channel": "instrument", "schema": "afbws.instrument.get.response.v1", "request_id": "r1", "item": _ITEM}
    _validator("getResponse", registry).validate(resp)  # does not raise


# --- pool (manager only, meta vs slice) -------------------------------------

def test_pool_request_source_required(registry):
    from jsonschema import ValidationError

    msg = {"channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1"}
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


def test_pool_request_moex_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1", "source": "moex"}
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_request_bf_id_with_exchange_market(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "source": "arena", "exchange": "MOEX", "market": "stock", "query": "sber",
    }
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_response_meta_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "exchanges": ["MOEX"], "markets": [{"exchange": "MOEX", "market": "stock"}],
    }
    _validator("poolResponse", registry).validate(msg)  # does not raise


def test_pool_response_slice_valid_with_null_group(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "arena", "exchange": "MOEX", "market": "stock", "items": [_POOL_ITEM],
    }
    _validator("poolResponse", registry).validate(msg)  # does not raise


def test_pool_response_cannot_mix_meta_and_slice_shapes(registry):
    """oneOf(meta, slice) — a message can't satisfy both at once."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "exchanges": ["MOEX"], "markets": [],
        "exchange": "MOEX", "market": "stock", "items": [],
    }
    with pytest.raises(ValidationError):
        _validator("poolResponse", registry).validate(msg)


# --- apply (manager only, bulk-replace) -------------------------------------

def test_apply_request_and_response_valid(registry):
    payload = {
        "items": [_ITEM],
        "groups": [{"key": "Stocks", "name": "Акции"}],
        "assets": {"SBER": {"name": "Сбербанк"}},
    }
    req = {
        "channel": "instrument", "schema": "afbws.instrument.apply.request.v1", "request_id": "r1",
        **payload,
    }
    _validator("applyRequest", registry).validate(req)  # does not raise
    resp = {
        "channel": "instrument", "schema": "afbws.instrument.apply.response.v1", "request_id": "r1",
        **payload,
    }
    _validator("applyResponse", registry).validate(resp)  # does not raise


def test_apply_request_unassigned_item_null_group(registry):
    payload = {
        "items": [{**_ITEM, "group": None}],
        "groups": [{"key": "Stocks", "name": "Акции"}],
        "assets": {},
    }
    req = {"channel": "instrument", "schema": "afbws.instrument.apply.request.v1", "request_id": "r1", **payload}
    _validator("applyRequest", registry).validate(req)  # does not raise


# --- resolve -----------------------------------------------------------

def test_resolve_request_draft_or_tradeplan_id(registry):
    by_draft = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.request.v1", "request_id": "r1",
        "bf_id": "arena", "draft": {"ticker": "SBER"},
    }
    _validator("resolveRequest", registry).validate(by_draft)  # does not raise
    by_id = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.request.v1", "request_id": "r1",
        "bf_id": "arena", "tradeplan_id": "tp-1",
    }
    _validator("resolveRequest", registry).validate(by_id)  # does not raise


def test_resolve_request_bf_id_required(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.request.v1", "request_id": "r1",
        "tradeplan_id": "tp-1",
    }
    with pytest.raises(ValidationError):
        _validator("resolveRequest", registry).validate(msg)


def test_resolve_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.response.v1", "request_id": "r1",
        "item": _ITEM,
        "binding": {"account_id": "1000316", "symbol": "SBER@MISX"},
        "broker_instrument": {"lot_size": 10, "tradable": True},
    }
    _validator("resolveResponse", registry).validate(msg)  # does not raise


# --- detail (lightweight live broker lookup, no draft/plan) ----------------

def test_detail_request_requires_bf_id_and_ticker(registry):
    from jsonschema import ValidationError

    msg = {"channel": "instrument", "schema": "afbws.instrument.detail.request.v1", "request_id": "r1", "bf_id": "arena"}
    with pytest.raises(ValidationError):
        _validator("detailRequest", registry).validate(msg)


def test_detail_request_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.detail.request.v1", "request_id": "r1",
        "bf_id": "arena", "ticker": "SBER",
    }
    _validator("detailRequest", registry).validate(msg)  # does not raise


def test_detail_response_valid(registry):
    """Same shape as resolveResponse, incl. a `broker_instrument` without a
    `symbol` key — to_broker_instrument_dict() strips it (lives in binding)."""
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.detail.response.v1", "request_id": "r1",
        "item": _ITEM,
        "binding": {"account_id": "1000316", "symbol": "SBER@MISX"},
        "broker_instrument": {"lot_size": 10, "tradable": True, "long_initial_margin": "3574.4"},
    }
    _validator("detailResponse", registry).validate(msg)  # does not raise


def test_detail_response_missing_broker_instrument_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.detail.response.v1", "request_id": "r1",
        "item": _ITEM, "binding": {},
    }
    with pytest.raises(ValidationError):
        _validator("detailResponse", registry).validate(msg)


# --- error ---------------------------------------------------------------

def test_error_response_minimal_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "not_found", "message": "Instrument not found",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_manager_only_uses_forbidden_code(registry):
    """pool/apply reject non-managers with the shared `forbidden` code —
    exercised at the handler level, just checking the vocabulary here."""
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "forbidden", "message": "manager only",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_bf_offline_code(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "bf_offline", "message": "BF arena is not connected",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_unknown_code_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "totally_unknown", "message": "x",
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


# --- structural sanity ------------------------------------------------------

def test_no_message_def_declares_a_type_property():
    """New channels forbid `type`: routing is channel+schema only."""
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "instrument.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"


def test_no_binding_field_on_the_curated_entity():
    """The plan explicitly forbids broker bindings inside the catalog entity
    itself — binding only ever appears in resolve's response."""
    from pathlib import Path

    schema_path = Path(__file__).resolve().parents[2] / "spec" / "schemas" / "instrument.v1.json"
    doc = json.loads(schema_path.read_text())
    props = set(doc.get("properties", {}))
    assert not (props & {"bindings", "venues", "bf_id", "broker_symbol", "binding"})
