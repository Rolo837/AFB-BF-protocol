"""afbws/auth.v1.json + afbws/access.channel.v1.json (AFB backend<->AFB frontend only;
not part of afb.execution.v1). Freemium access model: tier x capabilities x mode.

Convention (as link/screener): ONE schema id per operation = request = response;
`request_id` required in requests; server-initiated messages are the push
`access.state` (no `request_id`) and `access.denied` (on the refused request's
channel, with its `request_id`)."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCHEMAS = _ROOT / "spec" / "schemas" / "afbws"
_ACCESS_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/access.channel.v1.json"
_AUTH_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/auth.v1.json"
_COMMON_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/common.v1.json"

_ACCESS_OPS = {
    "roles.get", "roles.set", "settings.get", "settings.set", "users.list", "user.get", "trial.set",
    "grant.set", "grant.revoke", "stats", "state", "denied", "error",
}


def _v(schema_id, def_name, registry):
    from jsonschema import Draft202012Validator

    ref = f"{schema_id}#/$defs/{def_name}" if def_name else schema_id
    return Draft202012Validator({"$ref": ref}, registry=registry)


def _ok(validator, message):
    validator.validate(message)


def _bad(validator, message):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        validator.validate(message)


def _example(dirname, name):
    return json.loads((_ROOT / "examples" / dirname / name).read_text(encoding="utf-8"))


# --- declarations -----------------------------------------------------------

def test_support_ids():
    assert json.loads((_SCHEMAS / "auth.v1.json").read_text())["x-afbws-support-id"] == "afbws.auth.v1"
    assert json.loads((_SCHEMAS / "access.channel.v1.json").read_text())["x-afbws-support-id"] == "afbws.access.channel.v1"


def test_access_one_id_per_operation():
    doc = json.loads((_SCHEMAS / "access.channel.v1.json").read_text())
    ids = {d["properties"]["schema"]["const"] for d in doc["$defs"].values()
           if "schema" in d.get("properties", {}) and "channel" in d["properties"]}
    assert ids == {f"afbws.access.{op}.v1" for op in _ACCESS_OPS}
    assert len(doc["oneOf"]) == len(_ACCESS_OPS)


def test_auth_ids():
    doc = json.loads((_SCHEMAS / "auth.v1.json").read_text())
    ids = {d["properties"]["schema"]["const"] for d in doc["$defs"].values()}
    assert ids == {"afbws.auth.request.v1", "afbws.auth.ok.v1", "afbws.auth.error.v1"}


def test_no_message_def_declares_a_type_property():
    for name in ("auth.v1.json", "access.channel.v1.json"):
        doc = json.loads((_SCHEMAS / name).read_text())
        for def_name, def_schema in doc["$defs"].items():
            assert "type" not in def_schema.get("properties", {}), (name, def_name)


def test_access_error_codes_are_subset_of_common():
    access = json.loads((_SCHEMAS / "access.channel.v1.json").read_text())
    common = json.loads((_SCHEMAS / "common.v1.json").read_text())
    codes = set(access["$defs"]["error"]["properties"]["code"]["enum"])
    assert codes <= set(common["$defs"]["errorCode"]["enum"])
    assert {"forbidden", "validation_error", "not_found", "conflict", "invalid_schema", "internal_error"} == codes


def test_requests_require_request_id():
    doc = json.loads((_SCHEMAS / "access.channel.v1.json").read_text())
    for def_name, d in doc["$defs"].items():
        props = d.get("properties", {})
        if "channel" not in props or def_name == "state":
            continue
        assert "request_id" in d["required"], def_name


# --- examples ---------------------------------------------------------------

def test_auth_examples_validate(registry):
    root = _v(_AUTH_ID, None, registry)
    files = sorted((_ROOT / "examples" / "auth_v1").glob("*.json"))
    assert len(files) >= 5
    for path in files:
        root.validate(json.loads(path.read_text(encoding="utf-8")))


def test_access_examples_validate_and_cover_every_operation(registry):
    root = _v(_ACCESS_ID, None, registry)
    files = sorted((_ROOT / "examples" / "access_channel_v1").glob("*.json"))
    seen = set()
    for path in files:
        msg = json.loads(path.read_text(encoding="utf-8"))
        root.validate(msg)
        seen.add(msg["schema"])
    assert seen == {f"afbws.access.{op}.v1" for op in _ACCESS_OPS}


# --- access block (common) --------------------------------------------------

def _access(**kw):
    out = copy.deepcopy(_example("auth_v1", "ok.json")["access"])
    out.update(kw)
    return out


def test_access_block_mode_required(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access())
    a = _access()
    del a["mode"]
    _bad(v, a)


def test_access_block_basic_implies_reason_none(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access(mode="basic", reason="none"))
    _bad(v, _access(mode="basic", reason="window"))
    _ok(v, _access(mode="full", reason="none"))  # stage 1: guests are full without a reason


def test_access_block_showcase_only_in_basic(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access(mode="basic", reason="none", showcase=True))
    _bad(v, _access(showcase=True))


def test_access_block_limits_closed_and_non_negative(registry):
    v = _v(_COMMON_ID, "access", registry)
    lim = dict(_access()["limits"])
    _bad(v, _access(limits={**lim, "max_alarms": 3}))
    _bad(v, _access(limits={**lim, "max_sets": -1}))
    _bad(v, _access(tier="admin"))


# --- auth ---------------------------------------------------------------------

def test_auth_request_shape(registry):
    v = _v(_AUTH_ID, "request", registry)
    req = _example("auth_v1", "request.json")
    _bad(v, {**req, "type": "auth"})
    _bad(v, {k: x for k, x in req.items() if k != "support"})
    _bad(v, {**req, "request_id": "x"})


def test_auth_ok_requires_access(registry):
    v = _v(_AUTH_ID, "ok", registry)
    ok = _example("auth_v1", "ok.json")
    _bad(v, {k: x for k, x in ok.items() if k != "access"})
    _bad(v, {**ok, "tier": "user"})  # legacy flat fields are not part of the typed form


def test_auth_error_closed_codes(registry):
    v = _v(_AUTH_ID, "error", registry)
    _ok(v, {"channel": "auth", "schema": "afbws.auth.error.v1", "code": "session_invalid", "message": "x"})
    _bad(v, {"channel": "auth", "schema": "afbws.auth.error.v1", "code": "forbidden", "message": "x"})


# --- access channel: request/response shapes --------------------------------

def test_roles_get_request_carries_no_snapshot(registry):
    v = _v(_ACCESS_ID, "rolesGet", registry)
    _bad(v, {**_example("access_channel_v1", "roles.get.request.json"), "tiers": {}})
    resp = _example("access_channel_v1", "roles.get.response.json")
    _bad(v, {k: x for k, x in resp.items() if k != "local_groups"})


def test_roles_set_request_requires_tiers_and_capabilities(registry):
    v = _v(_ACCESS_ID, "rolesSet", registry)
    req = _example("access_channel_v1", "roles.set.request.json")
    _bad(v, {k: x for k, x in req.items() if k != "capabilities"})
    _bad(v, {**req, "default_tier": "user"})
    _ok(v, {k: x for k, x in req.items() if k != "local_groups"})
    tiers = {k: x for k, x in req["tiers"].items() if k != "guest"}
    _bad(v, {**req, "tiers": tiers})
    bad_member = copy.deepcopy(req)
    bad_member["tiers"]["user"]["members"].append("bogus")
    _bad(v, bad_member)


def test_settings_windows_and_revision(registry):
    v = _v(_ACCESS_ID, "settingsSet", registry)
    req = _example("access_channel_v1", "settings.set.request.json")
    _ok(v, {**req, "settings": {"revision": 1, "window_workday": {"from": "22:00", "to": "02:00"}}})
    _bad(v, {**req, "settings": {"revision": 1, "window_workday": {"from": "24:00", "to": "02:00"}}})
    _bad(v, {**req, "settings": {"trial_days": 3}})  # no revision
    _bad(v, {**req, "settings": {"revision": 1}})  # nothing to change
    _bad(v, {**req, "settings": {"revision": 1, "default_tier": "manager"}})


def test_users_list_request_vs_response(registry):
    v = _v(_ACCESS_ID, "usersList", registry)
    resp = _example("access_channel_v1", "users.list.response.json")
    _bad(v, {k: x for k, x in resp.items() if k != "total"})
    _bad(v, {**resp, "tier": "guest"})
    _bad(v, {k: x for k, x in resp.items() if k != "request_id"})


def test_trial_set_ends_at_rules(registry):
    v = _v(_ACCESS_ID, "trialSet", registry)
    req = _example("access_channel_v1", "trial.set.request.json")
    _bad(v, {k: x for k, x in req.items() if k != "ends_at"})
    _bad(v, {**req, "action": "reset"})  # reset carries no ends_at
    _ok(v, {**req, "action": "extend"})
    _bad(v, {**req, "action": "cancel"})


def test_grant_set_only_user_tier(registry):
    v = _v(_ACCESS_ID, "grantSet", registry)
    req = _example("access_channel_v1", "grant.set.request.json")
    _bad(v, {**req, "tier": "manager"})
    _bad(v, {k: x for k, x in req.items() if k != "ends_at"})


def test_state_is_push_only(registry):
    v = _v(_ACCESS_ID, "state", registry)
    _bad(v, {**_example("access_channel_v1", "state.push.json"), "request_id": "r"})


def test_denied_uses_refused_request_channel(registry):
    v = _v(_ACCESS_ID, "denied", registry)
    msg = _example("access_channel_v1", "denied.json")
    assert msg["channel"] != "access"
    _bad(v, {k: x for k, x in msg.items() if k != "request_id"})
    _bad(v, {**msg, "reason": "window"})
    _bad(v, {**msg, "refs": ["MISX:TQBR:SBER", "MISX:TQBR:SBER"]})


def test_error_item_only_with_conflict(registry):
    v = _v(_ACCESS_ID, "error", registry)
    conflict = _example("access_channel_v1", "error.conflict.json")
    _bad(v, {**conflict, "code": "forbidden"})
    _bad(v, {**conflict, "code": "bf_offline"})
