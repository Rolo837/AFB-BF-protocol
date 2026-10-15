"""afbws/account.channel.v2.json (AFB backend<->AFB frontend only).

Convention (as afbws.alarm.v2/market): ONE schema id per message, the same
schema is the request, its response and (list/orders) a server push; a message
without `request_id` is a push. `events` has no push.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_EXAMPLES = _ROOT / "examples" / "account_channel_v2"
_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/account.channel.v2.json"
_SNAP = {
    "bf_id": "virtual", "account_id": "virtual:id_u1", "tradable": True, "readonly": False, "status": "ok",
    "equity": "100", "cash": [{"currency": "RUB", "value": "60"}, {"currency": "USD", "value": "1"}],
    "positions": [], "as_of": "2026-10-15T09:30:00+00:00",
}
_ORDER = {"order_id": "o-1", "status": "filled", "quantity": 1}
_EVENT = {"logged_at": "t", "bf_id": "bf", "category": "order", "event": "order.filled"}


def _m(op, **kw):
    return {"channel": "account", "schema": f"afbws.account.{op}.v2", **kw}


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


def test_account_v2_one_id_per_message():
    schema = json.loads((_ROOT / "spec" / "schemas" / "afbws" / "account.channel.v2.json").read_text())
    ops = {"list", "orders", "events", "error"}
    assert ops <= set(schema["$defs"])
    stale = {"getRequest", "getResponse", "listRequest", "listResponse", "ordersRequest", "ordersResponse",
             "eventsRequest", "eventsResponse", "errorResponse", "snapshotPush", "ordersPush"}
    assert not stale & set(schema["$defs"])
    ids = {d["properties"]["schema"]["const"] for d in schema["$defs"].values()
           if "schema" in d.get("properties", {}) and "channel" in d["properties"]}
    assert ids == {f"afbws.account.{op}.v2" for op in ops}
    assert "account.channel.v1" not in json.dumps(schema["$defs"])
    assert "equity_by_currency" not in json.dumps(schema)


def test_account_v2_list(registry):
    v = _v("list", registry)
    v.validate(_m("list", request_id="r"))
    v.validate(_m("list", request_id="r", bf_id="virtual", account_id="a", force=True))
    v.validate(_m("list", request_id="r", items=[_SNAP]))  # response
    v.validate(_m("list", request_id="r", items=[]))
    v.validate(_m("list", bf_id="virtual", default_account_id="virtual:id_u1", items=[_SNAP]))  # push
    v.validate(_m("list", bf_id="virtual", default_account_id="a", items=[]))
    # request must not carry items-side fields
    _invalid(v, _m("list", request_id="r", default_account_id="a"))
    # push needs bf_id, default_account_id and items
    _invalid(v, _m("list", default_account_id="a", items=[_SNAP]))
    _invalid(v, _m("list", bf_id="virtual", items=[_SNAP]))
    _invalid(v, _m("list", bf_id="virtual", default_account_id="a"))
    _invalid(v, _m("list"))
    # push must not carry request-only fields
    _invalid(v, _m("list", bf_id="b", default_account_id="a", items=[], force=True))
    _invalid(v, _m("list", bf_id="b", default_account_id="a", items=[], account_id="a"))
    # response is only request_id + items
    _invalid(v, _m("list", request_id="r", bf_id="b", items=[_SNAP]))
    _invalid(v, _m("list", request_id="r", force=True, items=[_SNAP]))
    _invalid(v, _m("list", request_id="r", default_account_id="a", items=[_SNAP]))


def test_account_v2_snapshot_strict(registry):
    v = _v("list", registry)
    _invalid(v, _m("list", request_id="r", items=[{**_SNAP, "status": "weird"}]))
    _invalid(v, _m("list", request_id="r", items=[{**_SNAP, "broker_account_id": "1"}]))
    _invalid(v, _m("list", request_id="r", items=[{**_SNAP, "equity_by_currency": {"RUB": "1"}}]))
    bad = dict(_SNAP)
    del bad["cash"]
    _invalid(v, _m("list", request_id="r", items=[bad]))
    no_asof = {k: x for k, x in _SNAP.items() if k != "as_of"}
    v.validate(_m("list", request_id="r", items=[no_asof]))


def test_account_v2_orders(registry):
    v = _v("orders", registry)
    v.validate(_m("orders", request_id="r", bf_id="bf"))
    v.validate(_m("orders", request_id="r", bf_id="bf", account_id="a"))
    v.validate(_m("orders", request_id="r", bf_id="bf", account_id="a", items=[_ORDER]))
    v.validate(_m("orders", bf_id="bf", account_id="a", items=[_ORDER]))  # push
    _invalid(v, _m("orders", request_id="r"))  # no bf_id
    _invalid(v, _m("orders", account_id="a", items=[_ORDER]))  # push without bf_id
    _invalid(v, _m("orders", bf_id="bf", account_id="a"))  # push without items
    _invalid(v, _m("orders", bf_id="bf", items=[_ORDER]))  # push without account_id
    _invalid(v, _m("orders", request_id="r", bf_id="bf", items=[_ORDER]))  # response without account_id
    _invalid(v, _m("orders", request_id="r", bf_id="bf", account_id="a", items=[{**_ORDER, "x": 1}]))


def test_account_v2_events(registry):
    v = _v("events", registry)
    v.validate(_m("events", request_id="r", bf_id="bf"))
    v.validate(_m("events", request_id="r", bf_id="bf", date="2026-10-15"))
    v.validate(_m("events", request_id="r", bf_id="bf", date="2026-10-15", items=[_EVENT]))
    # no push for events: request_id is mandatory
    _invalid(v, _m("events", bf_id="bf", date="2026-10-15", items=[_EVENT]))
    _invalid(v, _m("events", request_id="r"))
    _invalid(v, _m("events", request_id="r", bf_id="bf", items=[_EVENT]))  # response without date
    _invalid(v, _m("events", request_id="r", bf_id="bf", date="d", items=[{**_EVENT, "category": "x"}]))


def test_account_v2_error(registry):
    v = _v("error", registry)
    v.validate(_m("error", request_id="r", code="not_found", message="x"))
    v.validate(_m("error", request_id="r", code="bf_offline", message="x", details={"bf_id": "bf"}))
    _invalid(v, _m("error", code="not_found", message="x"))
    _invalid(v, _m("error", request_id="r", code="nope", message="x"))
    _invalid(v, _m("error", request_id="r", code="not_found", message="x", extra=1))


def test_account_v2_root_dispatch(registry):
    root = _root(registry)
    root.validate(_m("list", request_id="r"))
    root.validate(_m("orders", bf_id="bf", account_id="a", items=[]))
    # v1 ids, the dropped `get` and the old suffixed ids are rejected
    for schema in ("afbws.account.list.request.v1", "afbws.account.list.response.v1", "afbws.account.get.response.v1",
                   "afbws.account.snapshot.push.v1", "afbws.account.orders.push.v1", "afbws.account.error.response.v1",
                   "afbws.account.get.v2", "afbws.account.list.request.v2"):
        _invalid(root, {"channel": "account", "schema": schema, "request_id": "r", "bf_id": "bf"})
    _invalid(root, _m("list", request_id="r", unexpected=1))
    _invalid(root, {**_m("list", request_id="r"), "channel": "alarm"})


def test_account_v2_examples_validate(registry):
    root = _root(registry)
    files = sorted(_EXAMPLES.glob("*.json"))
    assert len(files) >= 10
    for path in files:
        root.validate(json.loads(path.read_text(encoding="utf-8")))
    virtual = json.loads((_EXAMPLES / "list.response.json").read_text())["items"][0]
    assert virtual["bf_id"] == "virtual" and {c["currency"] for c in virtual["cash"]} == {"RUB", "USD"}
    assert virtual["as_of"]
