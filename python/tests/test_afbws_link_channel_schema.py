"""afbws/link.channel.v2.json — schema-first `link` channel v2 (AFB backend<->AFB
frontend only): one schema id per operation = request = response = push."""
from __future__ import annotations

import json

import pytest

LINK_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/link.channel.v2.json"
LINK_USER_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/link.user.v1.json"
LINK_ADMIN_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/link.admin.v1.json"

_EXECUTION_POLICY = {"max_spread_steps": 5, "execution_mode": "client"}

_USER_ITEM = {
    "schema": "afbws.link.user.v1",
    "bf_id": "bf-1",
    "name": "MyBF",
    "enabled": True,
    "broker": "finam-arena",
    "protocol": "afb.execution.v1",
    "description": "Demo connector",
    "dry_run": True,
    "margin_trading": None,
    "execution_policy": _EXECUTION_POLICY,
    "paired": True,
    "pairing_pending": False,
    "pairing_expires_at": None,
    "kind": "connector",
    "editable": True,
}

_ADMIN_ITEM = {
    **{k: v for k, v in _USER_ITEM.items() if k != "schema"},
    "schema": "afbws.link.admin.v1",
    "allowed_users": ["id_abc123"],
    "public_key_id": None,
    "public_key_file": None,
}

_VIRTUAL_ITEM = {
    **_USER_ITEM,
    "bf_id": "virtual",
    "kind": "virtual",
    "editable": False,
}

_STATUS_ITEM = {
    "schema": "afbws.link.state.v2",
    "bf_id": "bf-1",
    "connected": True,
    "heartbeat_stale": False,
    "updated_at": "2026-07-20T10:00:00Z",
    "daemon": None,
    "session": None,
}


def _validator(schema_id: str, def_name: str, registry):
    """Full-URI $ref so internal cross-refs resolve against the whole
    document — see test_afbws_alarm_channel_schema.py::_validator."""
    from jsonschema import Draft202012Validator

    ref = f"{schema_id}#/$defs/{def_name}" if def_name else schema_id
    return Draft202012Validator({"$ref": ref}, registry=registry)


def _root_validator(schema_id: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator(registry[schema_id].contents, registry=registry)


# --- role views: user/admin/virtual records ---------------------------------

def test_user_record_valid(registry):
    _root_validator(LINK_USER_ID, registry).validate(_USER_ITEM)  # does not raise


def test_admin_record_valid(registry):
    _root_validator(LINK_ADMIN_ID, registry).validate(_ADMIN_ITEM)  # does not raise


def test_virtual_is_a_valid_user_record(registry):
    _root_validator(LINK_USER_ID, registry).validate(_VIRTUAL_ITEM)  # does not raise


@pytest.mark.parametrize("forbidden_field", ["allowed_users", "public_key_id", "public_key_file"])
def test_user_record_rejects_manager_only_fields(forbidden_field, registry):
    from jsonschema import ValidationError

    bad = {**_USER_ITEM, forbidden_field: ["x"] if "users" in forbidden_field else "x"}
    with pytest.raises(ValidationError):
        _root_validator(LINK_USER_ID, registry).validate(bad)


@pytest.mark.parametrize("forbidden_field,value", [
    ("connected", True),
    ("daemon", None),
    ("session", None),
    ("account_id", "acc-1"),
])
def test_user_record_rejects_runtime_status_fields(forbidden_field, value, registry):
    """user/admin config records never carry connected/daemon/session runtime
    — that is the status record's job."""
    from jsonschema import ValidationError

    bad = {**_USER_ITEM, forbidden_field: value}
    with pytest.raises(ValidationError):
        _root_validator(LINK_USER_ID, registry).validate(bad)


@pytest.mark.parametrize("forbidden_field,value", [
    ("connected", True),
    ("daemon", None),
    ("session", None),
])
def test_admin_record_rejects_runtime_status_fields(forbidden_field, value, registry):
    from jsonschema import ValidationError

    bad = {**_ADMIN_ITEM, forbidden_field: value}
    with pytest.raises(ValidationError):
        _root_validator(LINK_ADMIN_ID, registry).validate(bad)


def test_user_record_rejects_extra_field(registry):
    from jsonschema import ValidationError

    bad = {**_USER_ITEM, "unexpected": 1}
    with pytest.raises(ValidationError):
        _root_validator(LINK_USER_ID, registry).validate(bad)


def test_user_record_rejects_wrong_schema_const(registry):
    from jsonschema import ValidationError

    bad = {**_USER_ITEM, "schema": "afbws.link.admin.v1"}
    with pytest.raises(ValidationError):
        _root_validator(LINK_USER_ID, registry).validate(bad)


def test_user_set_input_accepts_shared_fields(registry):
    valid = {
        "bf_id": "bf-1",
        "name": "MyBF",
        "enabled": True,
        "description": "note",
        "dry_run": False,
        "execution_policy": _EXECUTION_POLICY,
    }
    _validator(LINK_USER_ID, "setInput", registry).validate(valid)  # does not raise


@pytest.mark.parametrize("forbidden_field,value", [
    ("broker", "x"), ("allowed_users", ["trade"]), ("margin_trading", True), ("display_name", "x"), ("allowed_roles", ["trade"]),
])
def test_user_set_input_rejects_manager_only_fields(forbidden_field, value, registry):
    from jsonschema import ValidationError

    bad = {"bf_id": "bf-1", forbidden_field: value}
    with pytest.raises(ValidationError):
        _validator(LINK_USER_ID, "setInput", registry).validate(bad)


def test_admin_set_input_accepts_create_without_bf_id(registry):
    create = {"name": "New BF", "broker": "finam-arena", "protocol": "afb.execution.v1"}
    _validator(LINK_ADMIN_ID, "setInput", registry).validate(create)  # does not raise


def test_admin_set_input_accepts_full_manager_fields(registry):
    full = {
        "bf_id": "bf-1", "name": "x", "enabled": True, "description": "note",
        "broker": "finam-arena", "protocol": "afb.execution.v1",
        "dry_run": True, "margin_trading": None, "execution_policy": _EXECUTION_POLICY,
        "allowed_users": ["id_abc123"],
    }
    _validator(LINK_ADMIN_ID, "setInput", registry).validate(full)  # does not raise


def test_admin_set_input_rejects_allowed_roles(registry):
    from jsonschema import ValidationError

    bad = {"name": "x", "broker": "finam-arena", "allowed_roles": ["trade"]}
    with pytest.raises(ValidationError):
        _validator(LINK_ADMIN_ID, "setInput", registry).validate(bad)


def test_admin_set_input_rejects_display_name(registry):
    from jsonschema import ValidationError

    bad = {"name": "x", "broker": "finam-arena", "display_name": "badge"}
    with pytest.raises(ValidationError):
        _validator(LINK_ADMIN_ID, "setInput", registry).validate(bad)


import json as _json
from pathlib import Path as _Path

_EXAMPLES = _Path(__file__).resolve().parents[2] / "examples" / "link_channel_v2"


def _root(registry):
    return _root_validator(LINK_CHANNEL_ID, registry)


def _m(op, **kw):
    return {"channel": "link", "schema": f"afbws.link.{op}.v2", **kw}


def _ok(registry, msg):
    _root(registry).validate(msg)


def _bad(registry, msg):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _root(registry).validate(msg)


def _status_def(registry, value):
    _validator(LINK_CHANNEL_ID, "statusItem", registry).validate(value)


# --- status record -----------------------------------------------------------

def test_status_record_valid(registry):
    _status_def(registry, _STATUS_ITEM)
    _status_def(registry, {
        **_STATUS_ITEM,
        "daemon": {"bf_id": "bf-1", "code": "ok", "reason": "connected"},
        "session": {"account_id": "acc-1", "dry_run": False, "capabilities": {"margin_trading": True}},
    })


@pytest.mark.parametrize("field,value", [
    ("last_heartbeat_at", "2026-07-20T10:00:12Z"),
    ("heartbeat_interval_sec", 15),
    ("name", "x"), ("broker", "x"), ("allowed_users", ["u"]), ("kind", "connector"), ("paired", True),
])
def test_status_record_rejects_heartbeat_and_config_fields(field, value, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _status_def(registry, {**_STATUS_ITEM, field: value})


@pytest.mark.parametrize("field", ["heartbeat_stale", "updated_at", "connected", "daemon", "session"])
def test_status_record_requires_field(field, registry):
    from jsonschema import ValidationError

    bad = {k: v for k, v in _STATUS_ITEM.items() if k != field}
    with pytest.raises(ValidationError):
        _status_def(registry, bad)


def test_status_record_rejects_non_boolean_stale(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _status_def(registry, {**_STATUS_ITEM, "heartbeat_stale": "nope"})


@pytest.mark.parametrize("extra", [{"margin_trading": True}, {"dry_run_afb": True}, {"dry_run_bf": True}])
def test_status_session_rejects_extra_fields(extra, registry):
    from jsonschema import ValidationError

    bad = {"account_id": "acc-1", "dry_run": False, "capabilities": {}, **extra}
    with pytest.raises(ValidationError):
        _validator(LINK_CHANNEL_ID, "session", registry).validate(bad)


# --- list --------------------------------------------------------------------

def test_list_request_response_push(registry):
    _ok(registry, _m("list", request_id="r1"))
    _ok(registry, _m("list", request_id="r1", scope="admin", ids=["bf-1"]))
    _ok(registry, _m("list", request_id="r1", items=[_USER_ITEM, _ADMIN_ITEM, _VIRTUAL_ITEM]))
    _ok(registry, _m("list", request_id="r1", items=[]))
    _ok(registry, _m("list", items=[_USER_ITEM]))  # push: no request_id


def test_list_invalid(registry):
    _bad(registry, _m("list", request_id="r1", scope="all"))
    _bad(registry, _m("list", request_id="r1", ticker="SBER"))
    _bad(registry, _m("list", request_id="r1", scope="usable", items=[_USER_ITEM]))  # request w/ response shape
    _bad(registry, _m("list"))  # push needs items
    _bad(registry, _m("list", items=[]))  # push minItems 1
    _bad(registry, _m("list", items=[_USER_ITEM], scope="usable"))
    _bad(registry, _m("list", request_id="r1", items=[_STATUS_ITEM]))  # status never in config list


# --- set ---------------------------------------------------------------------

def test_set_request_accepts_user_and_admin_input(registry):
    _ok(registry, _m("set", request_id="r1", items=[{"bf_id": "bf-1", "dry_run": True}]))
    _ok(registry, _m("set", request_id="r1", items=[{"name": "New", "broker": "finam-arena"}, {"bf_id": "bf-2", "enabled": False}]))


def test_set_response_and_push(registry):
    _ok(registry, _m("set", request_id="r1", items=[_USER_ITEM], rejected=[]))
    _ok(registry, _m("set", request_id="r1", items=[], rejected=[{"id": "bf-1", "code": "validation_error", "message": "x"}]))
    _ok(registry, _m("set", items=[_ADMIN_ITEM]))  # push


def test_set_invalid(registry):
    _bad(registry, _m("set", request_id="r1", items=[]))  # request needs >=1
    _bad(registry, _m("set", request_id="r1", item={"bf_id": "bf-1"}))  # v1 singular form
    _bad(registry, _m("set", items=[]))  # push minItems 1
    _bad(registry, _m("set", items=[{"bf_id": "bf-1", "dry_run": True}]))  # push carries records, not inputs
    _bad(registry, _m("set", request_id="r1", items=[_USER_ITEM]))  # record w/o rejected = not a response


def test_rejected_requires_request_id(registry):
    _bad(registry, _m("set", items=[_USER_ITEM], rejected=[]))
    _bad(registry, _m("delete", ids=["bf-1"], rejected=[]))


def test_rejection_item_only_with_conflict(registry):
    ok = {"id": "bf-1", "code": "conflict", "message": "x", "item": _ADMIN_ITEM}
    _ok(registry, _m("set", request_id="r1", items=[], rejected=[ok]))
    _bad(registry, _m("set", request_id="r1", items=[], rejected=[{**ok, "code": "not_found"}]))
    _bad(registry, _m("set", request_id="r1", items=[], rejected=[{"id": "bf-1", "code": "weird"}]))
    _bad(registry, _m("set", request_id="r1", items=[], rejected=[{"id": "bf-1", "code": "not_found", "extra": 1}]))


# --- delete ------------------------------------------------------------------

def test_delete_request_response_push(registry):
    _ok(registry, _m("delete", request_id="r1", ids=["bf-1", "bf-2"]))
    _ok(registry, _m("delete", request_id="r1", ids=[], rejected=[{"id": "bf-1", "code": "conflict", "message": "active deals"}]))
    _ok(registry, _m("delete", ids=["bf-1"]))  # push of removed ids


def test_delete_invalid(registry):
    _bad(registry, _m("delete", request_id="r1", ids=[]))  # request needs >=1
    _bad(registry, _m("delete", request_id="r1", id="bf-1"))
    _bad(registry, _m("delete", ids=[]))  # push minItems 1
    _bad(registry, _m("delete"))


# --- pair / restart ----------------------------------------------------------

def test_pair(registry):
    _ok(registry, _m("pair", request_id="r1", ids=["bf-1"]))
    _ok(registry, _m("pair", request_id="r1", items=[
        {"id": "bf-1", "item": _USER_ITEM, "pairing_string": "abc.def", "expires_at": "2026-07-20T10:05:00Z"}], rejected=[]))
    _bad(registry, _m("pair", request_id="r1"))
    _bad(registry, _m("pair", request_id="r1", ids=[]))
    _bad(registry, _m("pair", ids=["bf-1"]))  # no push
    _bad(registry, _m("pair", request_id="r1", items=[{"id": "bf-1", "item": _USER_ITEM}], rejected=[]))


def test_restart(registry):
    _ok(registry, _m("restart", request_id="r1", ids=["bf-1"]))
    _ok(registry, _m("restart", request_id="r1", ids=["bf-1"], rejected=[
        {"id": "virtual", "code": "unsupported_action", "message": "x"}]))
    _bad(registry, _m("restart", request_id="r1"))  # explicit ids, never implicit
    _bad(registry, _m("restart", request_id="r1", ids=[]))
    _bad(registry, _m("restart", ids=["bf-1"]))


# --- status ------------------------------------------------------------------

def test_status_request_response_push(registry):
    _ok(registry, _m("status", request_id="r1"))
    _ok(registry, _m("status", request_id="r1", ids=["bf-1"]))
    _ok(registry, _m("status", request_id="r1", items=[_STATUS_ITEM]))
    _ok(registry, _m("status", items=[_STATUS_ITEM]))  # push of changed statuses only


def test_status_invalid(registry):
    _bad(registry, _m("status", items=[]))  # push minItems 1
    _bad(registry, _m("status"))
    _bad(registry, _m("status", request_id="r1", ids=["bf-1"], items=[_STATUS_ITEM]))  # request w/ response shape
    _bad(registry, _m("status", items=[_USER_ITEM]))  # config record in status
    _bad(registry, _m("status", items=[{**_STATUS_ITEM, "last_heartbeat_at": None}]))
    _bad(registry, _m("status", item=_STATUS_ITEM))  # v1 singular push
    _bad(registry, _m("status", items=[_STATUS_ITEM], rejected=[]))


# --- error + generic ---------------------------------------------------------

@pytest.mark.parametrize("code", [
    "not_found", "forbidden", "validation_error", "conflict", "bf_offline", "not_paired",
    "unsupported_action", "invalid_schema", "invalid_channel", "internal_error",
])
def test_error_accepts_business_codes(code, registry):
    _ok(registry, _m("error", request_id="r1", code=code, message="x"))


def test_error_invalid(registry):
    _bad(registry, _m("error", request_id="r1", code="totally_unknown", message="x"))  # closed enum
    _bad(registry, _m("error", request_id="r1", code="", message="x"))
    _bad(registry, _m("error", code="forbidden", message="x"))  # request_id required
    _bad(registry, _m("error", request_id="r1", code="conflict", message="x", item=_ADMIN_ITEM))


@pytest.mark.parametrize("schema", [
    "afbws.link.get.request.v1", "afbws.link.list.request.v1", "afbws.link.list.response.v1",
    "afbws.link.sync.push.v1", "afbws.link.status.sync.push.v1", "afbws.link.status.push.v1",
    "afbws.link.error.response.v1", "afbws.link.get.v2",
])
def test_legacy_and_unknown_schema_ids_rejected(schema, registry):
    _bad(registry, {"channel": "link", "schema": schema, "request_id": "r1"})


def test_wrong_channel_rejected(registry):
    _bad(registry, {**_m("list", request_id="r1"), "channel": "alarm"})


def test_examples_validate(registry):
    files = sorted(_EXAMPLES.glob("*.json"))
    assert len(files) >= 15
    for path in files:
        _ok(registry, _json.loads(path.read_text(encoding="utf-8")))


def test_no_message_def_declares_a_type_property():
    doc = json.loads(
        (_Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "link.channel.v2.json").read_text()
    )
    for def_name, def_schema in doc["$defs"].items():
        assert "type" not in def_schema.get("properties", {}), f"{def_name} must not declare a 'type' property"
