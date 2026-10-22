"""afbws/screener.channel.v1.json — schema-first screener channel (AFB backend<->AFB
frontend only; not part of afb.execution.v1). Read-only access to the screener's
published JSON exports: `list` and `get` (+ typed `error`). Validated as dict
literals against the channel schema's $defs (no fixture files)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

SCREENER_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/screener.channel.v1.json"
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "screener.channel.v1.json"


def _validator(def_name: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{SCREENER_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


def _root_validator(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": SCREENER_CHANNEL_ID}, registry=registry)


def _list_response(**overrides):
    msg = {
        "channel": "screener",
        "schema": "afbws.screener.list.v1",
        "request_id": "req-1",
        "items": [
            {
                "id": "intraday:2026-10-21T1130",
                "kind": "intraday",
                "trading_day": "2026-10-21",
                "asof": "2026-10-21T11:30:00",
                "generated_at": "2026-10-21T11:31:02+03:00",
                "size": 201345,
            },
            {
                "id": "night:2026-10-20",
                "kind": "night",
                "trading_day": "2026-10-20",
                "asof": "2026-10-20T19:00:00",
                "generated_at": "2026-10-20T23:10:00+03:00",
                "size": 198000,
            },
        ],
        "latest": "night:2026-10-20",
        "intraday_latest": "intraday:2026-10-21T1130",
    }
    msg.update(overrides)
    return msg


def _get_response(**overrides):
    msg = {
        "channel": "screener",
        "schema": "afbws.screener.get.v1",
        "request_id": "req-2",
        "id": "night:2026-10-20",
        "kind": "night",
        "document": {"contract_version": 1, "kind": "night", "models": [], "anything": {"goes": [1, 2]}},
    }
    msg.update(overrides)
    return msg


def test_x_afbws_support_id():
    doc = json.loads(SCHEMA_PATH.read_text())
    assert doc["x-afbws-support-id"] == "afbws.screener.channel.v1"


def test_no_message_def_declares_a_type_property():
    doc = json.loads(SCHEMA_PATH.read_text())
    for def_name, def_schema in doc["$defs"].items():
        assert "type" not in def_schema.get("properties", {}), def_name


# --- list -------------------------------------------------------------------

def test_list_request_empty_and_filtered(registry):
    v = _validator("list", registry)
    v.validate({"channel": "screener", "schema": "afbws.screener.list.v1", "request_id": "r"})
    v.validate({"channel": "screener", "schema": "afbws.screener.list.v1", "request_id": "r", "kind": "night", "limit": 10})


def test_list_response_valid(registry):
    _validator("list", registry).validate(_list_response())
    _validator("list", registry).validate(_list_response(items=[], latest=None, intraday_latest=None))


def test_list_response_requires_latest_fields(registry):
    from jsonschema import ValidationError

    msg = _list_response()
    del msg["latest"]
    with pytest.raises(ValidationError):
        _validator("list", registry).validate(msg)


def test_list_request_id_required(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("list", registry).validate({"channel": "screener", "schema": "afbws.screener.list.v1"})


def test_list_bad_kind_and_limit_rejected(registry):
    from jsonschema import ValidationError

    base = {"channel": "screener", "schema": "afbws.screener.list.v1", "request_id": "r"}
    for extra in ({"kind": "weekly"}, {"limit": 0}):
        with pytest.raises(ValidationError):
            _validator("list", registry).validate({**base, **extra})


def test_list_item_bad_id_rejected(registry):
    from jsonschema import ValidationError

    msg = _list_response()
    msg["items"][0]["id"] = "latest"
    with pytest.raises(ValidationError):
        _validator("list", registry).validate(msg)


# --- get --------------------------------------------------------------------

@pytest.mark.parametrize(
    "ref",
    ["latest", "intraday_latest", "night:2026-10-20", "intraday:2026-10-21T1130"],
)
def test_get_request_accepts_ids_and_aliases(registry, ref):
    _validator("get", registry).validate(
        {"channel": "screener", "schema": "afbws.screener.get.v1", "request_id": "r", "id": ref}
    )


@pytest.mark.parametrize(
    "ref",
    ["../etc/passwd", "night:../x", "night:2026-10-20/../x", "intraday:2026-10-21T11:30", "", "LATEST"],
)
def test_get_request_rejects_bad_ids(registry, ref):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("get", registry).validate(
            {"channel": "screener", "schema": "afbws.screener.get.v1", "request_id": "r", "id": ref}
        )


def test_get_response_document_is_open_object(registry):
    _validator("get", registry).validate(_get_response())


def test_get_response_document_must_be_object(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("get", registry).validate(_get_response(document=[1]))


def test_get_response_document_requires_kind(registry):
    from jsonschema import ValidationError

    msg = _get_response()
    del msg["kind"]
    with pytest.raises(ValidationError):
        _validator("get", registry).validate(msg)


# --- error ------------------------------------------------------------------

@pytest.mark.parametrize("code", ["forbidden", "not_found", "invalid_schema", "internal_error", "unsupported_action"])
def test_error_valid(registry, code):
    _validator("error", registry).validate(
        {"channel": "screener", "schema": "afbws.screener.error.v1", "request_id": "r", "code": code, "message": "x"}
    )


def test_error_unknown_code_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("error", registry).validate(
            {"channel": "screener", "schema": "afbws.screener.error.v1", "code": "boom", "message": "x"}
        )


# --- root oneOf -------------------------------------------------------------

def test_root_dispatches_each_schema(registry):
    v = _root_validator(registry)
    v.validate(_list_response())
    v.validate(_get_response())
    v.validate({"channel": "screener", "schema": "afbws.screener.error.v1", "code": "forbidden", "message": "x"})


def test_root_rejects_foreign_channel(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _root_validator(registry).validate(_list_response(channel="market"))


# --- participants -----------------------------------------------------------

_NUM_FIELDS = [
    "fiz_long", "fiz_short", "fiz_net", "fiz_persons_long", "fiz_persons_short",
    "yur_long", "yur_short", "yur_net", "yur_persons_long", "yur_persons_short",
    "openinterest", "volume",
]


def _participants_item(**overrides):
    item = {
        "derivative": "MISX:Si",
        "name": "Si",
        "active_instrument_key": "MISX:SiZ6",
        "collection_id": "currencies",
        "collection_name": "Валюты",
        "collection_color": "blue",
    }
    item.update({k: 1.5 for k in _NUM_FIELDS})
    item.update(overrides)
    return item


def _participants_response(**overrides):
    lists = [
        {
            "key": key,
            "trading_day": "2026-10-22",
            "asof": "2026-10-22T11:30:00",
            "source": "intraday" if key == "now" else "daily",
            "items": [_participants_item()],
        }
        for key in ("now", "d1", "d2", "w1")
    ]
    msg = {
        "channel": "screener",
        "schema": "afbws.screener.participants.v1",
        "request_id": "req-3",
        "received_at": "2026-10-22T11:31:02+03:00",
        "tz": "Europe/Moscow",
        "lists": lists,
    }
    msg.update(overrides)
    return msg


def test_participants_request_valid(registry):
    _validator("participants", registry).validate(
        {"channel": "screener", "schema": "afbws.screener.participants.v1", "request_id": "r"}
    )


def test_participants_request_id_required(registry):
    from jsonschema import ValidationError

    push = _participants_response()
    del push["request_id"]
    for msg in ({"channel": "screener", "schema": "afbws.screener.participants.v1"}, push):
        with pytest.raises(ValidationError):
            _validator("participants", registry).validate(msg)


def test_participants_request_rejects_extra_params(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("participants", registry).validate(
            {"channel": "screener", "schema": "afbws.screener.participants.v1", "request_id": "r", "day": "x"}
        )


def test_participants_response_valid(registry):
    _validator("participants", registry).validate(_participants_response())
    _validator("participants", registry).validate(_participants_response(lists=[]))


def test_participants_item_nulls_extra_fields_and_colorless(registry):
    msg = _participants_response()
    msg["lists"][0]["items"] = [
        _participants_item(
            collection_id=None, collection_name=None, collection_color=None,
            name=None, active_instrument_key=None, extra_field={"a": 1},
            **{k: None for k in _NUM_FIELDS},
        )
    ]
    _validator("participants", registry).validate(msg)


def test_participants_item_bad_color_and_number_rejected(registry):
    from jsonschema import ValidationError

    for bad in ({"collection_color": "magenta"}, {"fiz_net": "12"}, {"volume": True}):
        msg = _participants_response()
        msg["lists"][0]["items"] = [_participants_item(**bad)]
        with pytest.raises(ValidationError):
            _validator("participants", registry).validate(msg)


def test_participants_list_key_and_source_enums(registry):
    from jsonschema import ValidationError

    for field, value in (("key", "m1"), ("source", "live")):
        msg = _participants_response()
        msg["lists"][0][field] = value
        with pytest.raises(ValidationError):
            _validator("participants", registry).validate(msg)


def test_participants_partial_response_rejected(registry):
    from jsonschema import ValidationError

    msg = _participants_response()
    del msg["tz"]
    with pytest.raises(ValidationError):
        _validator("participants", registry).validate(msg)


def test_root_dispatches_participants(registry):
    _root_validator(registry).validate(_participants_response())
