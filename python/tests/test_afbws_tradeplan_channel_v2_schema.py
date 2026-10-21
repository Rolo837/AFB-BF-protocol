"""afbws/tradeplan.channel.v2.json (AFB backend<->AFB frontend only).

Convention (as afbws.alarm/account v2): ONE schema id per message, the same
schema is the request, its response and (sync) a server push; a message
without `request_id` is a push. `planInput` (what `set` accepts) and
`planItem` (what the server returns) are strict projections of the storage
schema tradeplan.v2.json.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_EXAMPLES = _ROOT / "examples" / "tradeplan_channel_v2"
_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/tradeplan.channel.v2.json"
_OPS = {"get", "list", "set", "delete", "archive", "sync", "error"}

_LEG = {"condition": {"op": "touch", "left": {"source": "price"}, "right": {"const": "100"}}}
_INPUT = {
    "schema": "afb.tradeplan.v2",
    "id": "tp1",
    "instrument_key": "MISX:TQBR:SBER",
    "direction": "long",
    "entries": [_LEG],
    "stop_loss": [],
    "take_profit": [],
    "sizing": {"mode": "lots", "value": "1"},
}
_ITEM = {
    "schema": "afb.tradeplan.v2",
    "id": "tp1",
    "ticker": "SBER",
    "instrument_key": "MISX:TQBR:SBER",
    "direction": "long",
    "status": "draft",
    "entries": [{"leg_id": "leg-1", **_LEG}],
    "stop_loss": [],
    "take_profit": [],
    "sizing": {"mode": "lots", "value": "1"},
    "activated_at": "",
    "closed_at": "",
    "created_at": "2026-10-21T10:00:00+03:00",
    "updated_at": "2026-10-21T10:00:00+03:00",
}


def _m(op, **kw):
    return {"channel": "tradeplan", "schema": f"afbws.tradeplan.{op}.v2", **kw}


def _v(def_name, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{_ID}#/$defs/{def_name}"}, registry=registry)


def _root(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": _ID}, registry=registry)


def _invalid(validator, message):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        validator.validate(message)


def _with(base, **over):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if v is None:
            out.pop(k, None)
        else:
            out[k] = v
    return out


def test_tradeplan_v2_one_id_per_message():
    schema = json.loads((_ROOT / "spec" / "schemas" / "afbws" / "tradeplan.channel.v2.json").read_text())
    assert schema["x-afbws-support-id"] == "afbws.tradeplan.channel.v2"
    assert _OPS <= set(schema["$defs"])
    stale = {"getRequest", "getResponse", "listRequest", "listResponse", "setRequest", "setResponse",
             "deleteRequest", "deleteResponse", "archiveRequest", "archiveResponse", "errorResponse",
             "syncPush", "entity"}
    assert not stale & set(schema["$defs"])
    ids = {d["properties"]["schema"]["const"] for d in schema["$defs"].values()
           if "schema" in d.get("properties", {}) and "channel" in d["properties"]}
    assert ids == {f"afbws.tradeplan.{op}.v2" for op in _OPS}
    assert "tradeplan.channel.v1" not in json.dumps(schema)
    assert "legacy:" not in json.dumps(schema["$defs"]["legInput"]) + json.dumps(schema["$defs"]["planInput"])


def test_tradeplan_v2_deal_status_matches_deal_state():
    spec = _ROOT / "spec" / "schemas"
    channel = json.loads((spec / "afbws" / "tradeplan.channel.v2.json").read_text())
    common = json.loads((spec / "common.v1.json").read_text())
    deal_state = json.loads((spec / "deal_state.v2.json").read_text())
    assert "dealStatus" not in channel["$defs"]  # shared def, not a local copy
    assert channel["$defs"]["amendResultItem"]["properties"]["status"] == {
        "$ref": "../common.v1.json#/$defs/dealStatus"
    }
    assert common["$defs"]["dealStatus"]["enum"] == deal_state["properties"]["status"]["enum"]


def test_tradeplan_v2_plan_input(registry):
    v = _v("planInput", registry)
    v.validate(_INPUT)
    v.validate(_with(_INPUT, publish={"bf_id": "virtual", "account_id": "a"}))
    v.validate(_with(_INPUT, entries=[{"leg_id": "leg-1", "percent": "100", "logic": "split", **_LEG}]))
    # mandatory fields
    for field in ("schema", "id", "instrument_key", "direction", "entries", "stop_loss", "take_profit", "sizing"):
        _invalid(v, _with(_INPUT, **{field: None}))
    _invalid(v, _with(_INPUT, entries=[]))
    _invalid(v, _with(_INPUT, schema="afb.tradeplan.v1"))
    # server-owned and legacy fields are not accepted on input
    for field, value in (("status", "draft"), ("activated_at", ""), ("closed_at", ""), ("archived_at", "t"),
                         ("created_at", "t"), ("updated_at", "t"), ("delivery_at", "t"),
                         ("instrument_missing", True), ("ticker", "SBER"), ("editor", "simple"),
                         ("archived_components", {"primitives": [], "indicators": []}),
                         ("connector", "bf"), ("account_id", "a"), ("deal_id", "")):
        _invalid(v, _with(_INPUT, **{field: value}))
    # legs: `op` mandatory, no synthetic legacy leg ids, closed
    no_op = {"condition": {"left": {"source": "price"}, "right": {"const": "100"}}}
    _invalid(v, _with(_INPUT, entries=[no_op]))
    _invalid(v, _with(_INPUT, entries=[{"leg_id": "", **_LEG}]))
    _invalid(v, _with(_INPUT, entries=[{**_LEG, "extra": 1}]))
    _invalid(v, _with(_INPUT, entries=[{"condition": {**_LEG["condition"], "extra": 1}}]))
    _invalid(v, _with(_INPUT, publish={"bf_id": "x", "extra": 1}))


def test_tradeplan_v2_condition_vocabulary(registry):
    v = _v("planInput", registry)
    imm = {"condition": {"op": "above", "left": {"source": "immediate"}, "right": {"const": "0"}}}
    v.validate(_with(_INPUT, entries=[imm]))
    ref = {"condition": {"op": "touch", "left": {"source": "price"}, "right": {"primitive_id": "p-1"}}}
    v.validate(_with(_INPUT, entries=[ref]))
    ds = {"condition": {"op": "above", "left": {"source": "dataset", "field": "position.size"},
                        "right": {"const": "1"}}}
    v.validate(_with(_INPUT, stop_loss=[ds]))
    dur = {"condition": {"op": "above", "left": {"source": "price"}, "right": {"const": "1"}, "duration": 5}}
    v.validate(_with(_INPUT, entries=[dur]))
    _invalid(v, _with(_INPUT, entries=[{"condition": {**dur["condition"], "duration": 0}}]))
    _invalid(v, _with(_INPUT, entries=[{"condition": {**dur["condition"], "op": "sideways"}}]))


def test_tradeplan_v2_plan_item(registry):
    v = _v("planItem", registry)
    v.validate(_ITEM)
    v.validate(_with(_ITEM, publish={"bf_id": "virtual"}))
    # instrument: key, or instrument_missing (possibly without ticker)
    missing = _with(_ITEM, instrument_key=None, ticker=None, instrument_missing=True)
    v.validate(missing)
    v.validate(_with(_ITEM, instrument_missing=True))
    v.validate(_with(_ITEM, instrument_key=None, instrument_missing=True))
    _invalid(v, _with(_ITEM, instrument_key=None))
    _invalid(v, _with(_ITEM, instrument_missing=False))
    for field in ("schema", "id", "direction", "status", "entries", "stop_loss", "take_profit", "sizing",
                  "activated_at", "closed_at", "created_at", "updated_at"):
        _invalid(v, _with(_ITEM, **{field: None}))
    for status in ("draft", "published", "completed", "archived"):
        v.validate(_with(_ITEM, status=status))
    for status in ("new", "active", "closed", "expired"):
        _invalid(v, _with(_ITEM, status=status))
    # never returned
    for field, value in (("delivery_at", "t"), ("archived_at", "t"), ("editor", "simple"),
                         ("archived_components", {"primitives": [], "indicators": []})):
        _invalid(v, _with(_ITEM, **{field: value}))
    # leg_id is mandatory on output
    _invalid(v, _with(_ITEM, entries=[_LEG]))
    _invalid(v, _with(_ITEM, entries=[{"leg_id": "leg-1", "condition": {"left": {"source": "price"},
                                                                       "right": {"const": "1"}}}]))


def test_tradeplan_v2_get(registry):
    v = _v("get", registry)
    v.validate(_m("get", request_id="r", id="tp1"))
    v.validate(_m("get", request_id="r", item=_ITEM))
    _invalid(v, _m("get", id="tp1"))  # no push
    _invalid(v, _m("get", request_id="r"))
    _invalid(v, _m("get", request_id="r", id="tp1", item=_ITEM))
    _invalid(v, _m("get", request_id="r", item=_INPUT))
    _invalid(v, _m("get", request_id="r", id=""))


def test_tradeplan_v2_list(registry):
    v = _v("list", registry)
    v.validate(_m("list", request_id="r"))
    v.validate(_m("list", request_id="r", instrument_keys=["MISX:TQBR:SBER"]))
    v.validate(_m("list", request_id="r", items=[_ITEM]))
    v.validate(_m("list", request_id="r", items=[]))
    _invalid(v, _m("list"))
    _invalid(v, _m("list", request_id="r", ticker="SBER"))  # the filter is by instrument_key only
    _invalid(v, _m("list", request_id="r", instrument_keys=[]))
    _invalid(v, _m("list", request_id="r", instrument_keys=["a", "a"]))
    _invalid(v, _m("list", request_id="r", instrument_keys=["MISX:TQBR:SBER"], items=[_ITEM]))
    _invalid(v, _m("list", request_id="r", items=[_INPUT]))


def test_tradeplan_v2_set(registry):
    v = _v("set", registry)
    v.validate(_m("set", request_id="r", item=_INPUT))  # request
    v.validate(_m("set", request_id="r", item=_ITEM, amend_results=[]))  # response, create
    ok = {"schema": "afbws.tradeplan.amend_result.v2", "deal_id": "d1", "accepted": True,
          "revision": 3, "status": "active"}
    no = {"schema": "afbws.tradeplan.amend_result.v2", "deal_id": "d2", "accepted": False, "message": "x"}
    v.validate(_m("set", request_id="r", item=_ITEM, amend_results=[ok, no]))
    # no push on set
    _invalid(v, _m("set", item=_ITEM, amend_results=[]))
    _invalid(v, _m("set", item=_INPUT))
    # request carries a planInput, response a planItem
    _invalid(v, _m("set", request_id="r", item=_ITEM))
    _invalid(v, _m("set", request_id="r", item=_INPUT, amend_results=[]))
    _invalid(v, _m("set", request_id="r", item=_with(_INPUT, status="draft")))
    _invalid(v, _m("set", request_id="r"))


def test_tradeplan_v2_amend_result(registry):
    v = _v("amendResultItem", registry)
    base = {"schema": "afbws.tradeplan.amend_result.v2", "deal_id": "d1"}
    v.validate({**base, "accepted": True, "revision": 2, "status": "published"})
    v.validate({**base, "accepted": True, "revision": None, "status": "paused"})
    v.validate({**base, "accepted": False, "message": "gate"})
    v.validate({**base, "accepted": False, "message": "plan is gone", "code": "tradeplan_missing"})
    for status in ("draft", "publishing", "published", "active", "paused", "closed", "cancelled", "orphaned"):
        v.validate({**base, "accepted": True, "revision": 1, "status": status})
    _invalid(v, {**base, "accepted": True, "revision": 1, "status": "weird"})
    _invalid(v, {**base, "accepted": True, "revision": "3", "status": "active"})  # integer|null only
    _invalid(v, {**base, "accepted": True, "status": "active"})
    _invalid(v, {**base, "accepted": True, "revision": 1})
    _invalid(v, {**base, "accepted": True, "revision": 1, "status": "active", "message": "x"})
    _invalid(v, {**base, "accepted": False})
    _invalid(v, {**base, "accepted": False, "message": "x", "revision": 1})
    _invalid(v, {**base, "accepted": False, "message": "x", "code": "weird"})
    _invalid(v, {**base, "accepted": False, "message": ""})
    _invalid(v, {k: x for k, x in {**base, "accepted": False, "message": "x"}.items() if k != "schema"})
    _invalid(v, {**base, "accepted": False, "message": "x", "extra": 1})


def test_tradeplan_v2_delete_and_archive(registry):
    v = _v("delete", registry)
    v.validate(_m("delete", request_id="r", id="tp1"))
    _invalid(v, _m("delete", id="tp1"))
    _invalid(v, _m("delete", request_id="r"))
    _invalid(v, _m("delete", request_id="r", id="tp1", item=_ITEM))
    v = _v("archive", registry)
    v.validate(_m("archive", request_id="r", id="tp1"))
    v.validate(_m("archive", request_id="r", item=_with(_ITEM, status="archived")))
    _invalid(v, _m("archive", id="tp1"))
    _invalid(v, _m("archive", request_id="r"))
    _invalid(v, _m("archive", request_id="r", id="tp1", item=_ITEM))


def test_tradeplan_v2_sync(registry):
    v = _v("sync", registry)
    v.validate(_m("sync", items=[_ITEM]))
    _invalid(v, _m("sync", items=[]))
    _invalid(v, _m("sync"))
    _invalid(v, _m("sync", request_id="r", items=[_ITEM]))  # push only
    _invalid(v, _m("sync", items=[_INPUT]))


def test_tradeplan_v2_error(registry):
    v = _v("error", registry)
    v.validate(_m("error", request_id="r", code="not_found", message="x"))
    v.validate(_m("error", request_id="r", code="conflict", message="x", details={"current_item": _ITEM}))
    for code in ("invalid_schema", "invalid_channel", "validation_error", "internal_error"):
        v.validate(_m("error", request_id="r", code=code, message="x"))
    _invalid(v, _m("error", code="not_found", message="x"))
    _invalid(v, _m("error", request_id="r", code="nope", message="x"))
    _invalid(v, _m("error", request_id="r", code="not_found", message="x", extra=1))
    # conflict carries the current plan, other codes carry no details
    _invalid(v, _m("error", request_id="r", code="conflict", message="x"))
    _invalid(v, _m("error", request_id="r", code="conflict", message="x", details={}))
    _invalid(v, _m("error", request_id="r", code="conflict", message="x", details={"current_item": _INPUT}))
    _invalid(v, _m("error", request_id="r", code="conflict", message="x",
                   details={"current_item": _ITEM, "extra": 1}))
    _invalid(v, _m("error", request_id="r", code="not_found", message="x", details={"current_item": _ITEM}))
    _invalid(v, _m("error", request_id="r", code="not_found", message="x", item=_ITEM))  # v1 form


def test_tradeplan_v2_root_dispatch(registry):
    root = _root(registry)
    root.validate(_m("get", request_id="r", id="tp1"))
    root.validate(_m("set", request_id="r", item=_INPUT))
    root.validate(_m("sync", items=[_ITEM]))
    # v1 ids and the old suffixed ids are rejected
    for schema in ("afbws.tradeplan.get.request.v1", "afbws.tradeplan.get.response.v1",
                   "afbws.tradeplan.set.request.v1", "afbws.tradeplan.sync.push.v1",
                   "afbws.tradeplan.error.response.v1", "afbws.tradeplan.get.request.v2",
                   "afbws.tradeplan.sync.push.v2"):
        _invalid(root, {"channel": "tradeplan", "schema": schema, "request_id": "r", "id": "tp1"})
    _invalid(root, _m("get", request_id="r", id="tp1", unexpected=1))
    _invalid(root, {**_m("get", request_id="r", id="tp1"), "channel": "alarm"})


def test_tradeplan_v2_examples_validate(registry):
    root = _root(registry)
    files = sorted(_EXAMPLES.glob("*.json"))
    assert len(files) >= 14
    seen = set()
    for path in files:
        message = json.loads(path.read_text(encoding="utf-8"))
        root.validate(message)
        seen.add(message["schema"])
    assert seen == {f"afbws.tradeplan.{op}.v2" for op in _OPS}
    # every example plan is also a valid storage-schema plan once server-only fields are added back
    from jsonschema import Draft202012Validator

    storage = Draft202012Validator(
        {"$ref": "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/tradeplan.v2.json"}, registry=registry
    )
    for name in ("set.request", "get.response"):
        message = json.loads((_EXAMPLES / f"{name}.json").read_text())
        plan = {**message["item"], "status": "draft", "delivery_at": ""}
        storage.validate(plan)
