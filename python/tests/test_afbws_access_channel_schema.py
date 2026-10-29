"""afbws/auth.v1.json + afbws/access.channel.v1.json (AFB backend<->AFB frontend only;
not part of afb.execution.v1). Freemium access model: tier x capabilities x mode.

Convention (as link/screener): ONE schema id per operation = request = response
(= push for auth); `request_id` required in requests; server-initiated messages are
the push `afbws.auth.v1` (no `request_id`, whole auth response on access change)
and `access.denied` (on the refused request's channel, with its `request_id`)."""
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
    "users.list", "users.set", "users.tier.set", "trial.start", "policy.get", "policy.set", "tiers.get", "tiers.set",
    "groups.get", "groups.set", "stats", "denied", "error",
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
    assert ids == {"afbws.auth.v1", "afbws.auth.error.v1"}
    assert len(doc["oneOf"]) == 2


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
        if "channel" not in props:
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
    out = copy.deepcopy(_example("auth_v1", "response.json")["access"])
    out.update(kw)
    return out


def test_access_block_all_fields_required(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access())
    for key in ("tier", "capabilities", "limits", "mode", "trial", "grace"):
        a = _access()
        del a[key]
        _bad(v, a)
    _ok(v, _access(mode="basic"))
    _bad(v, _access(mode="trial"))


def test_access_block_has_no_reason_until_showcase(registry):
    v = _v(_COMMON_ID, "access", registry)
    _bad(v, _access(reason="subscription"))
    _bad(v, _access(until=None))
    _bad(v, _access(mode="basic", showcase=True))


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


def test_access_block_trial_and_grace(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access(trial=None, grace=None))
    _ok(v, _access(trial={"state": "available", "days": 14}))
    _ok(v, _access(trial={"state": "active", "ends_on": "2026-11-11", "days_left": 5}))
    _ok(v, _access(grace={"ends_on": "2026-11-01", "days_left": 3}))
    _bad(v, _access(trial={"state": "available", "days": 0}))
    _bad(v, _access(trial={"state": "available", "days": 14, "ends_on": "2026-11-11"}))
    _bad(v, _access(trial={"state": "active", "ends_on": "2026-11-11"}))
    _bad(v, _access(trial={"state": "active", "ends_on": "2026-11-11", "days_left": 0}))
    _bad(v, _access(trial={"state": "ended"}))
    _bad(v, _access(grace={"ends_on": "2026-11-01"}))
    _bad(v, _access(grace={"ends_on": "2026-11-01", "days_left": 3, "state": "active"}))


def test_access_block_capabilities_are_open_strings(registry):
    v = _v(_COMMON_ID, "access", registry)
    _ok(v, _access(capabilities=["trade", "local"]))  # local — added by the backend, not assignable
    _bad(v, _access(capabilities=["trade", "trade"]))


def test_auth_examples_cover_trial_and_grace():
    states = set()
    for path in (_ROOT / "examples" / "auth_v1").glob("*.json"):
        msg = json.loads(path.read_text(encoding="utf-8"))
        if "access" in msg:
            a = msg["access"]
            states.add("trial:" + (a["trial"]["state"] if a["trial"] else "null"))
            states.add("grace:" + ("set" if a["grace"] else "null"))
    assert states == {"trial:null", "trial:available", "trial:active", "grace:null", "grace:set"}


# --- auth ---------------------------------------------------------------------

def test_auth_request_shape(registry):
    v = _v(_AUTH_ID, "auth", registry)
    req = _example("auth_v1", "request.json")
    _ok(v, req)
    _ok(v, _example("auth_v1", "request.session_id.json"))
    _bad(v, {**req, "type": "auth"})
    _bad(v, {**req, "demo": False})  # demo removed
    for key in ("support", "version", "request_id"):
        _bad(v, {k: x for k, x in req.items() if k != key})


def test_auth_request_forbids_response_fields(registry):
    v = _v(_AUTH_ID, "auth", registry)
    req = _example("auth_v1", "request.json")
    resp = _example("auth_v1", "response.json")
    for key in ("timezone", "brokers", "access"):
        _bad(v, {**req, key: resp[key]})


def test_auth_response_and_push(registry):
    v = _v(_AUTH_ID, "auth", registry)
    resp = _example("auth_v1", "response.json")
    push = _example("auth_v1", "push.guest_basic.json")
    _ok(v, resp)
    _ok(v, push)
    assert "request_id" in resp and "request_id" not in push
    for key in ("timezone", "brokers", "support", "access"):
        _bad(v, {k: x for k, x in resp.items() if k != key})
        _bad(v, {k: x for k, x in push.items() if k != key})
    _bad(v, {k: x for k, x in resp.items() if k != "user_id"})  # read as a request: response fields forbidden
    for key, val in (("version", "3.4.1"), ("session_id", "s")):
        _bad(v, {**resp, key: val})  # request-only field in a response
    _bad(v, {**resp, "tier": "user"})  # legacy flat fields are not part of the typed form


def test_auth_error_closed_codes(registry):
    v = _v(_AUTH_ID, "error", registry)
    _ok(v, {"channel": "auth", "schema": "afbws.auth.error.v1", "code": "session_invalid", "message": "x"})
    _ok(v, _example("auth_v1", "error.json"))
    _bad(v, {"channel": "auth", "schema": "afbws.auth.error.v1", "code": "forbidden", "message": "x"})


# --- access channel: tiers / policy / groups --------------------------------

def test_roles_operations_removed():
    doc = json.loads((_SCHEMAS / "access.channel.v1.json").read_text())
    assert not {"rolesGet", "rolesSet", "userRole", "userSet", "userTierSet", "groupRole"} & set(doc["$defs"])
    assert "roles.get" not in doc["description"]
    assert "user.set" not in doc["description"]


def test_access_description_names_admin_only_and_staff_operations():
    desc = json.loads((_SCHEMAS / "access.channel.v1.json").read_text())["description"]
    assert "admin-only" in desc and "staff" in desc and "forbidden" in desc and "trial.start" in desc


def test_capability_enum_has_no_local(registry):
    v = _v(_ACCESS_ID, "capability", registry)
    for c in ("trade", "virtual", "screener"):
        _ok(v, c)
    _bad(v, "local")
    _bad(v, "Trade")


def test_tiers_get_request_vs_response(registry):
    v = _v(_ACCESS_ID, "tiersGet", registry)
    req = _example("access_channel_v1", "tiers.get.request.json")
    resp = _example("access_channel_v1", "tiers.get.response.json")
    _ok(v, req)
    _ok(v, resp)
    _bad(v, {**req, "group_roles": []})


def test_tiers_set_request_vs_response(registry):
    v = _v(_ACCESS_ID, "tiersSet", registry)
    req = _example("access_channel_v1", "tiers.set.request.json")
    _ok(v, req)
    _ok(v, _example("access_channel_v1", "tiers.set.response.json"))
    _bad(v, {k: x for k, x in req.items() if k != "tiers"})
    _bad(v, {**req, "tiers": []})
    _bad(v, {**req, "tiers": req["tiers"] + req["tiers"][:1]})  # identical duplicate rows
    _bad(v, {**req, "user_roles": []})
    row = req["tiers"][-1]
    _bad(v, {**req, "tiers": [{**row, "policy": None}]})  # no policy in tiers.*


def test_tier_row_shape(registry):
    v = _v(_ACCESS_ID, "tierRow", registry)
    rows = _example("access_channel_v1", "tiers.get.response.json")["tiers"]
    assert {r["tier"] for r in rows} >= {"admin", "manager"}
    for row in rows:
        _ok(v, row)
    row = rows[0]
    for key in ("tier", "title", "rank", "subscription", "capabilities", "limits"):
        _bad(v, {k: x for k, x in row.items() if k != key})
    _ok(v, {**row, "capabilities": []})
    _bad(v, {**row, "capabilities": ["local"]})
    _bad(v, {**row, "capabilities": ["trade", "trade"]})
    _bad(v, {**row, "subscription": 1})
    _bad(v, {**row, "paid": False})
    _bad(v, {**row, "policy": None})
    _bad(v, {**row, "tier": "Manager"})


def test_policy_get_request_vs_response(registry):
    v = _v(_ACCESS_ID, "policyGet", registry)
    req = _example("access_channel_v1", "policy.get.request.json")
    resp = _example("access_channel_v1", "policy.get.response.json")
    _ok(v, req)
    _ok(v, resp)
    assert not {r["tier"] for r in resp["tiers"]} & {"admin", "manager"}
    _bad(v, {**req, "tier": "guest"})


def test_policy_set_request_vs_response(registry):
    v = _v(_ACCESS_ID, "policySet", registry)
    req = _example("access_channel_v1", "policy.set.request.json")
    resp = _example("access_channel_v1", "policy.set.response.json")
    _ok(v, req)
    _ok(v, {**req, "policy": None})
    _ok(v, resp)
    _bad(v, {k: x for k, x in req.items() if k != "policy"})
    _bad(v, {k: x for k, x in req.items() if k != "tier"})
    _bad(v, {**req, "tiers": resp["tiers"]})  # response field in a request
    _bad(v, {**req, "policy": {"trial_days": 3}})
    _bad(v, {**req, "policy": {"as_tier": "user", "grace_days": -1}})


def test_policy_row_shape(registry):
    v = _v(_ACCESS_ID, "policyRow", registry)
    for row in _example("access_channel_v1", "policy.get.response.json")["tiers"]:
        _ok(v, row)
    row = {"tier": "guest", "title": "Гость", "rank": 10, "policy": None}
    for key in row:
        _bad(v, {k: x for k, x in row.items() if k != key})
    _bad(v, {**row, "limits": {}})
    _bad(v, {**row, "subscription": False})


def test_groups_get_request_vs_response(registry):
    v = _v(_ACCESS_ID, "groupsGet", registry)
    req = _example("access_channel_v1", "groups.get.request.json")
    resp = _example("access_channel_v1", "groups.get.response.json")
    _ok(v, req)
    _ok(v, resp)
    for key in ("groups", "provider_groups", "provider_groups_error"):
        _bad(v, {**req, key: resp[key]})  # response field in a request
        _bad(v, {k: x for k, x in resp.items() if k != key})  # incomplete response
    _bad(v, {**req, "group_roles": []})


def test_groups_set_request_vs_response(registry):
    v = _v(_ACCESS_ID, "groupsSet", registry)
    req = _example("access_channel_v1", "groups.set.request.json")
    resp = _example("access_channel_v1", "groups.set.response.json")
    _ok(v, req)
    _ok(v, {**req, "groups": []})
    _ok(v, resp)
    _bad(v, {k: x for k, x in req.items() if k != "groups"})
    _bad(v, {**req, "group_roles": []})
    _bad(v, {**req, "user_roles": []})
    _bad(v, {**req, "tiers": []})
    for key in ("provider_groups", "provider_groups_error"):
        _bad(v, {**req, key: resp[key]})
        _bad(v, {k: x for k, x in resp.items() if k != key})


def test_policy_requires_as_tier_and_closed(registry):
    v = _v(_ACCESS_ID, "policy", registry)
    _ok(v, {"as_tier": "user"})
    _ok(v, {"as_tier": "user", "trial_days": 0, "workday": None, "weekend": None})
    _ok(v, {"as_tier": "user", "trial_days": 14, "grace_days": 3})
    _ok(v, {"as_tier": "user", "grace_days": 0})
    _bad(v, {"as_tier": "user", "grace_days": -1})
    _bad(v, {"as_tier": "user", "grace_days": 1.5})
    _ok(v, {"as_tier": "user", "workday": {"from": "22:00", "to": "02:00"}})  # across midnight
    _ok(v, {"as_tier": "user", "showcase": {"enabled": True, "collection": "c-1"}})
    _bad(v, {"trial_days": 14})  # no as_tier
    _bad(v, {"as_tier": "user", "trial_days": -1})
    _bad(v, {"as_tier": "user", "workday": {"from": "24:00", "to": "02:00"}})
    _bad(v, {"as_tier": "user", "workday": {"from": "19:00"}})
    _bad(v, {"as_tier": "user", "showcase": {"enabled": True}})
    _bad(v, {"as_tier": "user", "revision": 1})


def test_tier_group_shape(registry):
    v = _v(_ACCESS_ID, "tierGroup", registry)
    _ok(v, {"tier": "user", "provider": "getcourse", "group_id": "3125478"})
    _bad(v, {"tier": "user", "group_id": "3125478"})
    _bad(v, {"tier": "user", "provider": "getcourse"})
    _bad(v, {"provider": "getcourse", "group_id": "3125478"})
    _bad(v, {"tier": "user", "provider": "getcourse", "group_id": ""})
    _bad(v, {"tier": "user", "provider": "GetCourse", "group_id": "1"})
    _bad(v, {"tier": "user", "provider": "getcourse", "group_id": 3125478})
    _bad(v, {"tier": "User", "provider": "getcourse", "group_id": "1"})
    _bad(v, {"role": "user", "provider": "getcourse", "group_id": "1"})


def test_provider_group_shape(registry):
    v = _v(_ACCESS_ID, "providerGroup", registry)
    for g in _example("access_channel_v1", "groups.get.response.json")["provider_groups"]:
        _ok(v, g)
    _bad(v, {"provider": "getcourse", "group_id": "1"})
    _bad(v, {"id": "1", "title": "x"})


# --- access channel: users ----------------------------------------------------

def test_users_list_request_vs_response(registry):
    v = _v(_ACCESS_ID, "usersList", registry)
    req = _example("access_channel_v1", "users.list.request.json")
    resp = _example("access_channel_v1", "users.list.response.json")
    _ok(v, req)
    _ok(v, resp)
    _bad(v, {k: x for k, x in resp.items() if k != "request_id"})
    for key in ("items", "tiers", "capabilities"):
        _bad(v, {k: x for k, x in resp.items() if k != key})  # incomplete response
    for key in ("tiers", "capabilities"):
        _bad(v, {**req, key: resp[key]})  # response field in a request
    _bad(v, {**resp, "tier": "guest"})  # no filters
    _bad(v, {**resp, "total": 2})  # no paging


def test_users_list_labels_shape(registry):
    tl = _v(_ACCESS_ID, "tierLabel", registry)
    cl = _v(_ACCESS_ID, "capabilityLabel", registry)
    resp = _example("access_channel_v1", "users.list.response.json")
    for row in resp["tiers"]:
        _ok(tl, row)
    for row in resp["capabilities"]:
        _ok(cl, row)
    _bad(tl, {"tier": "user"})
    _bad(tl, {"tier": "user", "title": "x", "rank": 20})
    _bad(cl, {"capability": "", "title": "x"})
    _bad(cl, {"capability": "trade"})


def test_user_row_shape(registry):
    v = _v(_ACCESS_ID, "userRow", registry)
    rows = _example("access_channel_v1", "users.list.response.json")["items"]
    assert {r["tier_source"] for r in rows} == {"personal", "group", "default"}
    for r in rows:
        _ok(v, r)
    row = rows[0]
    _ok(v, {**row, "subscription": None})
    for key in ("provider", "tier_source", "personal_capabilities", "trial_started_on", "trial_ends_on",
                "grace_until", "late_days"):
        _bad(v, {k: x for k, x in row.items() if k != key})
    for removed in ("personal_tier", "trial_started_at", "trial_ends_at", "grant_until"):
        _bad(v, {**row, removed: None})
    _bad(v, {**row, "tier_source": "manual"})
    _bad(v, {**row, "late_days": -1})
    _bad(v, {**row, "grace_until": "2026-11-15T21:00:00Z"})  # a date, not a moment
    _bad(v, {**row, "personal_capabilities": ["trade", "trade"]})
    _bad(v, {**row, "personal_capabilities": ["local"]})
    _bad(v, {**row, "subscription": {"tier": "user", "started_at": "2026-09-01T08:00:00Z"}})
    _bad(v, {**row, "mode": "full"})


def test_users_set_request_vs_response(registry):
    v = _v(_ACCESS_ID, "usersSet", registry)
    req = _example("access_channel_v1", "users.set.request.json")
    resp = _example("access_channel_v1", "users.set.response.json")
    _ok(v, req)
    _ok(v, _example("access_channel_v1", "users.set.request.capabilities.json"))
    _ok(v, resp)
    item = {"user_id": "gc_1", "grace_until": "2026-11-15"}
    _ok(v, {**req, "items": [{**item, "capabilities": ["virtual"]}]})
    _ok(v, {**req, "items": [{"user_id": "gc_1", "capabilities": []}]})
    _bad(v, {**req, "items": []})
    _bad(v, {k: x for k, x in req.items() if k != "items"})
    _bad(v, {**req, "items": [{"user_id": "gc_1"}]})  # nothing to set
    _bad(v, {**req, "items": [{"grace_until": None}]})
    _bad(v, {**req, "items": [{**item, "grace_until": "2026-11-15T21:00:00Z"}]})
    _bad(v, {**req, "items": [{**item, "capabilities": ["local"]}]})
    _bad(v, {**req, "items": [{**item, "capabilities": ["trade", "trade"]}]})
    _bad(v, {**req, "items": [{**item, "tier": "user"}]})  # tier — only users.tier.set
    _bad(v, {**req, "items": [{**item, "trial_ends_on": "2026-11-15"}]})  # trial is not managed by staff
    _bad(v, {**req, "items": [item, resp["items"][0]]})  # request and response rows are not mixed
    _bad(v, {**req, "user_id": "gc_1"})


def test_users_tier_set_request_vs_response(registry):
    v = _v(_ACCESS_ID, "usersTierSet", registry)
    req = _example("access_channel_v1", "users.tier.set.request.json")
    resp = _example("access_channel_v1", "users.tier.set.response.json")
    _ok(v, req)
    _ok(v, resp)
    assert any(i["tier"] is None for i in req["items"])
    _bad(v, {**req, "items": []})
    _bad(v, {**req, "items": [{"user_id": "gc_1"}]})  # tier (or null) required
    _bad(v, {**req, "items": [{"tier": "user"}]})
    _bad(v, {**req, "items": [{"user_id": "gc_1", "tier": "Admin"}]})
    _bad(v, {**req, "items": [{"user_id": "gc_1", "tier": "user", "capabilities": []}]})
    _bad(v, {**req, "item": resp["items"][0]})


def test_trial_start_request_vs_response(registry):
    v = _v(_ACCESS_ID, "trialStart", registry)
    req = _example("access_channel_v1", "trial.start.request.json")
    resp = _example("access_channel_v1", "trial.start.response.json")
    _ok(v, req)
    _ok(v, resp)
    assert set(req) == {"channel", "schema", "request_id"}
    _bad(v, {k: x for k, x in req.items() if k != "request_id"})
    _bad(v, {**req, "days": 14})
    _bad(v, {**resp, "trial": {"state": "active", "ends_on": "2026-11-11"}})


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


def test_denied_uses_refused_request_channel(registry):
    v = _v(_ACCESS_ID, "denied", registry)
    msg = _example("access_channel_v1", "denied.json")
    assert msg["channel"] != "access"
    _ok(v, msg)
    _ok(v, {**msg, "channel": "access", "reason": "held"})
    _bad(v, {k: x for k, x in msg.items() if k != "request_id"})
    _bad(v, {**msg, "until": None})
    _bad(v, {**msg, "reason": "window"})
    _bad(v, {**msg, "refs": ["MISX:TQBR:SBER"]})


def test_error_codes(registry):
    v = _v(_ACCESS_ID, "error", registry)
    msg = _example("access_channel_v1", "error.json")
    _ok(v, {**msg, "code": "invalid_channel"})
    _bad(v, {**msg, "code": "conflict"})
    _bad(v, {**msg, "code": "bf_offline"})
    _bad(v, {**msg, "item": {}})
