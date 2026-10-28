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

_ACCESS_OPS = {"roles.get", "roles.set", "users.list", "user.set", "stats", "state", "denied", "error"}


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
    assert {"forbidden", "validation_error", "not_found", "invalid_channel", "invalid_schema", "internal_error"} == codes


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


def test_access_block_all_fields_required(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access())
    for key in ("tier", "capabilities", "limits", "mode", "reason", "until"):
        a = _access()
        del a[key]
        _bad(v, a)


def test_access_block_basic_implies_reason_none(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access(mode="basic", reason="none"))
    _bad(v, _access(mode="basic", reason="window"))
    _ok(v, _access(mode="full", reason="none"))


def test_access_block_has_no_showcase(registry):
    v = _v(_COMMON_ID, "access", registry)
    _bad(v, _access(mode="basic", reason="none", showcase=True))


def test_access_block_tier_is_open_string(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access(tier="lite"))
    _ok(v, _access(tier="premium_2"))
    _bad(v, _access(tier="Lite"))
    _bad(v, _access(tier="2x"))
    _bad(v, _access(tier=""))


def test_access_block_limits_closed_and_non_negative(registry):
    v = _v(_COMMON_ID, "access", registry)
    lim = dict(_access()["limits"])
    _bad(v, _access(limits={**lim, "max_alarms": 3}))
    _bad(v, _access(limits={**lim, "max_sets": -1}))
    _bad(v, _access(limits={k: x for k, x in lim.items() if k != "max_sets"}))


# --- auth ---------------------------------------------------------------------

def test_auth_request_shape(registry):
    v = _v(_AUTH_ID, "request", registry)
    req = _example("auth_v1", "request.json")
    _bad(v, {**req, "type": "auth"})
    _bad(v, {k: x for k, x in req.items() if k != "support"})
    _bad(v, {k: x for k, x in req.items() if k != "version"})
    _bad(v, {**req, "request_id": "x"})
    _ok(v, _example("auth_v1", "request.session_id.json"))


def test_auth_ok_requires_access(registry):
    v = _v(_AUTH_ID, "ok", registry)
    ok = _example("auth_v1", "ok.json")
    _bad(v, {k: x for k, x in ok.items() if k != "access"})
    _bad(v, {**ok, "tier": "user"})  # legacy flat fields are not part of the typed form


def test_auth_error_closed_codes(registry):
    v = _v(_AUTH_ID, "error", registry)
    _ok(v, {"channel": "auth", "schema": "afbws.auth.error.v1", "code": "session_invalid", "message": "x"})
    _bad(v, {"channel": "auth", "schema": "afbws.auth.error.v1", "code": "forbidden", "message": "x"})


# --- access channel: roles ----------------------------------------------------

def test_roles_get_request_vs_response(registry):
    v = _v(_ACCESS_ID, "rolesGet", registry)
    req = _example("access_channel_v1", "roles.get.request.json")
    resp = _example("access_channel_v1", "roles.get.response.json")
    _ok(v, req)
    _ok(v, resp)
    for key in ("tiers", "members", "capabilities", "getcourse_groups", "getcourse_groups_error"):
        _bad(v, {**req, key: resp[key]})  # response field in a request
        _bad(v, {k: x for k, x in resp.items() if k != key})  # incomplete response


def test_roles_set_request_vs_response(registry):
    v = _v(_ACCESS_ID, "rolesSet", registry)
    req = _example("access_channel_v1", "roles.set.request.json")
    resp = _example("access_channel_v1", "roles.set.response.json")
    _ok(v, req)
    _ok(v, resp)
    _bad(v, {k: x for k, x in req.items() if k != "members"})
    _bad(v, {**req, "tiers": []})
    for key in ("capabilities", "getcourse_groups", "getcourse_groups_error"):
        _bad(v, {**req, key: resp[key]})
        _bad(v, {k: x for k, x in resp.items() if k != key})


def test_roles_set_duplicate_identical_tier_rows_rejected(registry):
    v = _v(_ACCESS_ID, "rolesSet", registry)
    req = _example("access_channel_v1", "roles.set.request.json")
    _bad(v, {**req, "tiers": req["tiers"] + req["tiers"][:1]})


def test_tier_row_shape(registry):
    v = _v(_ACCESS_ID, "tierRow", registry)
    rows = _example("access_channel_v1", "roles.get.response.json")["tiers"]
    for row in rows:
        _ok(v, row)
    row = rows[0]
    for key in ("tier", "title", "rank", "paid", "limits", "policy"):
        _bad(v, {k: x for k, x in row.items() if k != key})
    _bad(v, {**row, "paid": 1})
    _bad(v, {**row, "tier": "Manager"})


def test_policy_requires_as_tier_and_closed(registry):
    v = _v(_ACCESS_ID, "policy", registry)
    _ok(v, {"as_tier": "user"})
    _ok(v, {"as_tier": "user", "trial_days": 0, "workday": None, "weekend": None})
    _ok(v, {"as_tier": "user", "workday": {"from": "22:00", "to": "02:00"}})  # across midnight
    _ok(v, {"as_tier": "user", "showcase": {"enabled": True, "collection": "c-1"}})
    _bad(v, {"trial_days": 14})  # no as_tier
    _bad(v, {"as_tier": "user", "trial_days": -1})
    _bad(v, {"as_tier": "user", "workday": {"from": "24:00", "to": "02:00"}})
    _bad(v, {"as_tier": "user", "workday": {"from": "19:00"}})
    _bad(v, {"as_tier": "user", "showcase": {"enabled": True}})
    _bad(v, {"as_tier": "user", "revision": 1})


def test_member_tokens(registry):
    v = _v(_ACCESS_ID, "member", registry)
    for token in ("id_9910336377", "gc_282811500", "gc:3125478", "gc_AbC"):
        _ok(v, {"role": "user", "token": token})
    for token in ("bogus", "id:grp", "id_", "gc_12345678901", "gc:", "gc_1-2"):
        _bad(v, {"role": "user", "token": token})
    _bad(v, {"role": "User", "token": "gc_1"})
    _bad(v, {"role": "user"})


# --- access channel: users ----------------------------------------------------

def test_users_list_request_vs_response(registry):
    v = _v(_ACCESS_ID, "usersList", registry)
    _ok(v, _example("access_channel_v1", "users.list.request.json"))
    resp = _example("access_channel_v1", "users.list.response.json")
    _ok(v, resp)
    _bad(v, {k: x for k, x in resp.items() if k != "request_id"})
    _bad(v, {**resp, "tier": "guest"})  # no filters
    _bad(v, {**resp, "total": 2})  # no paging


def test_user_row_shape(registry):
    v = _v(_ACCESS_ID, "userRow", registry)
    row = _example("access_channel_v1", "users.list.response.json")["items"][0]
    _ok(v, row)
    _ok(v, {**row, "subscription": None})
    _bad(v, {k: x for k, x in row.items() if k != "grant_until"})
    _bad(v, {**row, "subscription": {"tier": "user", "started_at": "2026-09-01T08:00:00Z"}})
    _bad(v, {**row, "mode": "full"})


def test_user_set_request_vs_response(registry):
    v = _v(_ACCESS_ID, "userSet", registry)
    req = _example("access_channel_v1", "user.set.request.json")
    resp = _example("access_channel_v1", "user.set.response.json")
    _ok(v, req)
    _ok(v, _example("access_channel_v1", "user.set.request.trial.json"))
    _ok(v, {**req, "trial_ends_at": "2026-11-01T00:00:00Z"})
    _ok(v, resp)
    _bad(v, {k: x for k, x in req.items() if k != "grant_until"})  # no fields to set
    _bad(v, {k: x for k, x in req.items() if k != "user_id"})
    _bad(v, {**req, "item": resp["item"]})  # response field in a request
    _bad(v, {**req, "grant_until": 5})


# --- access channel: stats / server messages --------------------------------

def test_stats_request_vs_response(registry):
    v = _v(_ACCESS_ID, "stats", registry)
    req = _example("access_channel_v1", "stats.request.json")
    resp = _example("access_channel_v1", "stats.response.json")
    _ok(v, req)
    _ok(v, resp)
    _bad(v, {k: x for k, x in req.items() if k != "to"})
    week = resp["weeks"][0]
    _bad(v, {**resp, "weeks": [{**week, "converted": -1}]})
    _bad(v, {**resp, "weeks": [{k: x for k, x in week.items() if k != "active"}]})
    _bad(v, {**req, "group_by": "week"})


def test_state_is_push_only(registry):
    v = _v(_ACCESS_ID, "state", registry)
    msg = _example("access_channel_v1", "state.push.json")
    _ok(v, msg)
    _bad(v, {**msg, "request_id": "r"})


def test_denied_uses_refused_request_channel(registry):
    v = _v(_ACCESS_ID, "denied", registry)
    msg = _example("access_channel_v1", "denied.json")
    assert msg["channel"] != "access"
    _ok(v, msg)
    _ok(v, {**msg, "channel": "access", "reason": "held", "until": None})
    _bad(v, {k: x for k, x in msg.items() if k != "request_id"})
    _bad(v, {k: x for k, x in msg.items() if k != "until"})
    _bad(v, {**msg, "reason": "window"})
    _bad(v, {**msg, "refs": ["MISX:TQBR:SBER"]})


def test_error_codes(registry):
    v = _v(_ACCESS_ID, "error", registry)
    msg = _example("access_channel_v1", "error.json")
    _ok(v, {**msg, "code": "invalid_channel"})
    _bad(v, {**msg, "code": "conflict"})
    _bad(v, {**msg, "code": "bf_offline"})
    _bad(v, {**msg, "item": {}})
