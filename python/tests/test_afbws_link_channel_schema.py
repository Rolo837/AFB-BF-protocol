"""afbws/link.channel.v1.json — schema-first `link` channel (AFB backend<->AFB
frontend only). Negotiated via auth.support/auth_ok.support; not part of the
afb.execution.v1 AFB<->BF wire. Covers role views (user/admin/virtual), the
config/status split, and all RPC/push variants."""
from __future__ import annotations

import json

import pytest

LINK_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/link.channel.v1.json"
LINK_USER_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/link.user.v1.json"
LINK_ADMIN_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/link.admin.v1.json"
LINK_STATUS_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/link.status.v1.json"

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
    "allowed_roles": ["trade"],
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
    "schema": "afbws.link.status.v1",
    "bf_id": "bf-1",
    "connected": True,
    "updated_at": "2026-07-20T10:00:00Z",
    "last_heartbeat_at": "2026-07-20T10:00:12Z",
    "heartbeat_interval_sec": 15,
    "heartbeat_stale": False,
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


@pytest.mark.parametrize("forbidden_field", ["allowed_roles", "allowed_users", "public_key_id", "public_key_file"])
def test_user_record_rejects_manager_only_fields(forbidden_field, registry):
    from jsonschema import ValidationError

    bad = {**_USER_ITEM, forbidden_field: ["x"] if "roles" in forbidden_field or "users" in forbidden_field else "x"}
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
    — that's link.status.v1.json's job, delivered on a separate push."""
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
    ("broker", "x"), ("allowed_roles", ["trade"]), ("margin_trading", True), ("display_name", "x"),
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
        "allowed_roles": ["trade"], "allowed_users": ["id_abc123"],
    }
    _validator(LINK_ADMIN_ID, "setInput", registry).validate(full)  # does not raise


def test_admin_set_input_rejects_display_name(registry):
    from jsonschema import ValidationError

    bad = {"name": "x", "broker": "finam-arena", "display_name": "badge"}
    with pytest.raises(ValidationError):
        _validator(LINK_ADMIN_ID, "setInput", registry).validate(bad)


# --- status: config fields forbidden ----------------------------------------

def test_status_record_valid(registry):
    _root_validator(LINK_STATUS_ID, registry).validate(_STATUS_ITEM)  # does not raise


def test_status_record_valid_with_session(registry):
    with_session = {
        **_STATUS_ITEM,
        "session": {"account_id": "acc-1", "dry_run": False, "capabilities": {"margin_trading": True}},
    }
    _root_validator(LINK_STATUS_ID, registry).validate(with_session)  # does not raise


@pytest.mark.parametrize("forbidden_field,value", [
    ("name", "x"), ("broker", "x"), ("description", "x"), ("protocol", "x"),
    ("allowed_roles", ["trade"]), ("allowed_users", ["id_abc123"]),
    ("public_key_id", "x"), ("public_key_file", "x"),
    ("execution_policy", {}), ("paired", True), ("kind", "connector"),
])
def test_status_record_rejects_config_fields(forbidden_field, value, registry):
    from jsonschema import ValidationError

    bad = {**_STATUS_ITEM, forbidden_field: value}
    with pytest.raises(ValidationError):
        _root_validator(LINK_STATUS_ID, registry).validate(bad)


def test_status_session_rejects_margin_fields():
    """Regression: margin_trading[_afb|_bf] were considered and explicitly
    dropped — nothing in the backend serializes them today, no plans to."""
    from jsonschema import Draft202012Validator, ValidationError
    from conftest import _load_registry

    registry = _load_registry()
    session_validator = Draft202012Validator(
        {"$ref": f"{LINK_STATUS_ID}#/$defs/session"}, registry=registry
    )
    bad = {"account_id": "acc-1", "dry_run": False, "capabilities": {}, "margin_trading": True}
    with pytest.raises(ValidationError):
        session_validator.validate(bad)


def test_status_session_rejects_dry_run_afb_bf_split():
    """Regression: dry_run_afb/dry_run_bf exist in the legacy bfs.registry.v1.json
    entry — deliberately not carried over into the new session shape (user
    request: keep only the effective dry_run)."""
    from jsonschema import Draft202012Validator, ValidationError
    from conftest import _load_registry

    registry = _load_registry()
    session_validator = Draft202012Validator(
        {"$ref": f"{LINK_STATUS_ID}#/$defs/session"}, registry=registry
    )
    for field in ("dry_run_afb", "dry_run_bf"):
        bad = {"account_id": "acc-1", "dry_run": False, "capabilities": {}, field: True}
        with pytest.raises(ValidationError):
            session_validator.validate(bad)


def test_status_daemon_null_and_populated(registry):
    populated = {**_STATUS_ITEM, "daemon": {"bf_id": "bf-1", "code": "ok", "reason": "connected"}}
    _root_validator(LINK_STATUS_ID, registry).validate(populated)  # does not raise


def test_status_record_allows_missing_optional_heartbeat_fields(registry):
    legacy = {k: v for k, v in _STATUS_ITEM.items() if k not in {
        "last_heartbeat_at", "heartbeat_interval_sec", "heartbeat_stale"
    }}
    _root_validator(LINK_STATUS_ID, registry).validate(legacy)  # does not raise


def test_status_record_allows_null_last_heartbeat(registry):
    never_seen = {**_STATUS_ITEM, "last_heartbeat_at": None}
    _root_validator(LINK_STATUS_ID, registry).validate(never_seen)  # does not raise


def test_status_record_rejects_non_boolean_heartbeat_stale(registry):
    from jsonschema import ValidationError

    bad = {**_STATUS_ITEM, "heartbeat_stale": "nope"}
    with pytest.raises(ValidationError):
        _root_validator(LINK_STATUS_ID, registry).validate(bad)


# --- RPC operations ------------------------------------------------------

def test_get_request_and_response_valid(registry):
    req = {"channel": "link", "schema": "afbws.link.get.request.v1", "request_id": "r1", "id": "bf-1"}
    _validator(LINK_CHANNEL_ID, "getRequest", registry).validate(req)  # does not raise
    resp = {"channel": "link", "schema": "afbws.link.get.response.v1", "request_id": "r1", "item": _USER_ITEM}
    _validator(LINK_CHANNEL_ID, "getResponse", registry).validate(resp)  # does not raise
    resp_admin = {"channel": "link", "schema": "afbws.link.get.response.v1", "request_id": "r1", "item": _ADMIN_ITEM}
    _validator(LINK_CHANNEL_ID, "getResponse", registry).validate(resp_admin)  # does not raise


def test_list_request_has_no_filters(registry):
    req = {"channel": "link", "schema": "afbws.link.list.request.v1", "request_id": "r1"}
    _validator(LINK_CHANNEL_ID, "listRequest", registry).validate(req)  # does not raise


def test_list_request_rejects_extra_filter_field(registry):
    from jsonschema import ValidationError

    bad = {"channel": "link", "schema": "afbws.link.list.request.v1", "request_id": "r1", "ticker": "SBER"}
    with pytest.raises(ValidationError):
        _validator(LINK_CHANNEL_ID, "listRequest", registry).validate(bad)


def test_list_response_mixed_user_admin_valid(registry):
    resp = {
        "channel": "link", "schema": "afbws.link.list.response.v1", "request_id": "r1",
        "items": [_USER_ITEM, _ADMIN_ITEM, _VIRTUAL_ITEM],
    }
    _validator(LINK_CHANNEL_ID, "listResponse", registry).validate(resp)  # does not raise


def test_set_request_accepts_user_and_admin_set_input(registry):
    user_set = {
        "channel": "link", "schema": "afbws.link.set.request.v1", "request_id": "r1",
        "item": {"bf_id": "bf-1", "dry_run": True},
    }
    _validator(LINK_CHANNEL_ID, "setRequest", registry).validate(user_set)  # does not raise
    admin_set = {
        "channel": "link", "schema": "afbws.link.set.request.v1", "request_id": "r1",
        "item": {"name": "New", "broker": "finam-arena"},
    }
    _validator(LINK_CHANNEL_ID, "setRequest", registry).validate(admin_set)  # does not raise


def test_set_response_valid(registry):
    resp = {"channel": "link", "schema": "afbws.link.set.response.v1", "request_id": "r1", "item": _USER_ITEM}
    _validator(LINK_CHANNEL_ID, "setResponse", registry).validate(resp)  # does not raise


def test_delete_request_and_response_valid(registry):
    req = {"channel": "link", "schema": "afbws.link.delete.request.v1", "request_id": "r1", "id": "bf-1"}
    _validator(LINK_CHANNEL_ID, "deleteRequest", registry).validate(req)  # does not raise
    resp = {"channel": "link", "schema": "afbws.link.delete.response.v1", "request_id": "r1", "id": "bf-1"}
    _validator(LINK_CHANNEL_ID, "deleteResponse", registry).validate(resp)  # does not raise


def test_pair_request_requires_id(registry):
    from jsonschema import ValidationError

    bad = {"channel": "link", "schema": "afbws.link.pair.request.v1", "request_id": "r1"}
    with pytest.raises(ValidationError):
        _validator(LINK_CHANNEL_ID, "pairRequest", registry).validate(bad)


def test_pair_response_valid(registry):
    resp = {
        "channel": "link", "schema": "afbws.link.pair.response.v1", "request_id": "r1",
        "item": _USER_ITEM, "pairing_string": "abc.def", "expires_at": "2026-07-20T10:05:00Z",
    }
    _validator(LINK_CHANNEL_ID, "pairResponse", registry).validate(resp)  # does not raise


def test_restart_request_requires_explicit_id_never_implicit(registry):
    from jsonschema import ValidationError

    bad = {"channel": "link", "schema": "afbws.link.restart.request.v1", "request_id": "r1"}
    with pytest.raises(ValidationError):
        _validator(LINK_CHANNEL_ID, "restartRequest", registry).validate(bad)
    good = {"channel": "link", "schema": "afbws.link.restart.request.v1", "request_id": "r1", "id": "bf-1"}
    _validator(LINK_CHANNEL_ID, "restartRequest", registry).validate(good)  # does not raise


def test_restart_response_valid(registry):
    resp = {"channel": "link", "schema": "afbws.link.restart.response.v1", "request_id": "r1", "id": "bf-1"}
    _validator(LINK_CHANNEL_ID, "restartResponse", registry).validate(resp)  # does not raise


# --- error response, including business codes -------------------------------

@pytest.mark.parametrize("code", [
    "not_found", "forbidden", "validation_error", "conflict", "bf_offline", "not_paired", "unsupported_action",
])
def test_error_response_accepts_all_business_codes(code, registry):
    msg = {
        "channel": "link", "schema": "afbws.link.error.response.v1", "request_id": "r1",
        "code": code, "message": "x",
    }
    _validator(LINK_CHANNEL_ID, "errorResponse", registry).validate(msg)  # does not raise


def test_error_response_code_is_an_open_string(registry):
    """`code` is deliberately not a strict enum — the schema doesn't police
    the vocabulary, the backend does (user decision: no error-code enum)."""
    msg = {
        "channel": "link", "schema": "afbws.link.error.response.v1", "request_id": "r1",
        "code": "totally_unknown", "message": "x",
    }
    _validator(LINK_CHANNEL_ID, "errorResponse", registry).validate(msg)  # does not raise


def test_error_response_rejects_empty_code(registry):
    from jsonschema import ValidationError

    bad = {
        "channel": "link", "schema": "afbws.link.error.response.v1", "request_id": "r1",
        "code": "", "message": "x",
    }
    with pytest.raises(ValidationError):
        _validator(LINK_CHANNEL_ID, "errorResponse", registry).validate(bad)


def test_error_response_conflict_carries_current_item(registry):
    msg = {
        "channel": "link", "schema": "afbws.link.error.response.v1", "request_id": "r1",
        "code": "conflict", "message": "Deal already active", "item": _ADMIN_ITEM,
    }
    _validator(LINK_CHANNEL_ID, "errorResponse", registry).validate(msg)  # does not raise


# --- push: config vs status, never mixed ------------------------------------

def test_sync_push_config_only(registry):
    msg = {"channel": "link", "schema": "afbws.link.sync.push.v1", "items": [_USER_ITEM, _ADMIN_ITEM]}
    _validator(LINK_CHANNEL_ID, "syncPush", registry).validate(msg)  # does not raise


def test_sync_push_has_no_request_id(registry):
    resolved = registry[LINK_CHANNEL_ID]
    assert "request_id" not in resolved.contents["$defs"]["syncPush"]["properties"]


def test_status_sync_push_valid(registry):
    msg = {"channel": "link", "schema": "afbws.link.status.sync.push.v1", "items": [_STATUS_ITEM]}
    _validator(LINK_CHANNEL_ID, "statusSyncPush", registry).validate(msg)  # does not raise


def test_status_push_single_item_not_array(registry):
    msg = {"channel": "link", "schema": "afbws.link.status.push.v1", "item": _STATUS_ITEM}
    _validator(LINK_CHANNEL_ID, "statusPush", registry).validate(msg)  # does not raise


def test_status_push_rejects_config_item(registry):
    """Status pushes must never carry a config record — the whole point of
    splitting config/status into separate wire models."""
    from jsonschema import ValidationError

    bad = {"channel": "link", "schema": "afbws.link.status.push.v1", "item": _USER_ITEM}
    with pytest.raises(ValidationError):
        _validator(LINK_CHANNEL_ID, "statusPush", registry).validate(bad)


def test_sync_push_rejects_status_item(registry):
    from jsonschema import ValidationError

    bad = {"channel": "link", "schema": "afbws.link.sync.push.v1", "items": [_STATUS_ITEM]}
    with pytest.raises(ValidationError):
        _validator(LINK_CHANNEL_ID, "syncPush", registry).validate(bad)


def test_no_message_def_declares_a_type_property():
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "link.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"
