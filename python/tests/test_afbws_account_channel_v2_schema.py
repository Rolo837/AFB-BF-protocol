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
    ops = {"list", "orders", "events", "cash", "set", "ledger", "settings", "error"}
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


_KEY = "MISX:TQOB:SU26238RMFS4"
_BOND_SNAP = {**{k: x for k, x in _SNAP.items() if k != "readonly"}, "owner": {}, "bf_id": "bond", "account_id": "bond:p-1", "cash": [{"currency": "RUB", "value": "100"}],
              "positions": [{"quantity": 10, "average_price": "968", "instrument_key": _KEY, "accrued_int": "12.4"}]}
_OP = {"op_id": "o1", "ts": "2026-11-07T09:30:00+00:00", "kind": "deposit", "reason": "user_cash", "currency": "RUB", "amount": "5"}


def test_account_v2_bond_account_snapshot(registry):
    v = _v("list", registry)
    v.validate(_m("list", request_id="r", bf_id="bond", account_id="bond:p-1"))
    v.validate(_m("list", request_id="r", items=[_BOND_SNAP]))
    v.validate(_m("list", bf_id="bond", default_account_id="bond:p-1", items=[_BOND_SNAP]))
    v.validate(_m("list", request_id="r", items=[{**_BOND_SNAP, "positions": [{"quantity": 1, "average_price": "1", "accrued_int": None}]}]))
    _invalid(v, _m("list", request_id="r", items=[{**_BOND_SNAP, "positions": [{"quantity": 1, "average_price": "1", "accrued_int": 1.5}]}]))


def test_account_v2_snapshot_branches_by_bf_id(registry):
    v = _v("accountSnapshot", registry)
    v.validate(_BOND_SNAP)
    v.validate({**_BOND_SNAP, "owner": {"name": "Иван Петров", "tier": "manager"}})
    v.validate({**_BOND_SNAP, "owner": {"name": None, "tier": None}})
    _invalid(v, {**_BOND_SNAP, "readonly": False})  # bond: owner, not readonly
    _invalid(v, {**_BOND_SNAP, "readonly": True})
    _invalid(v, {k: x for k, x in _BOND_SNAP.items() if k != "owner"})
    _invalid(v, {**_BOND_SNAP, "owner": {"name": "A", "extra": 1}})
    _invalid(v, {**_BOND_SNAP, "owner": {"name": 1}})
    v.validate(_SNAP)  # broker / virtual: readonly
    v.validate({**_SNAP, "bf_id": "finam", "readonly": True})
    _invalid(v, {**_SNAP, "owner": {}})
    _invalid(v, {k: x for k, x in _SNAP.items() if k != "readonly"})
    pub = json.loads((_EXAMPLES / "list.response.bond_public.json").read_text())["items"][0]
    assert pub["owner"] == {"name": "Иван Петров", "tier": "manager"} and "readonly" not in pub
    own = json.loads((_EXAMPLES / "list.response.bond.json").read_text())["items"][0]
    assert own["owner"] == {} and "readonly" not in own


def test_account_v2_cash(registry):
    v = _v("cash", registry)
    req = _m("cash", request_id="r", account_id="bond:p-1", kind="deposit", currency="RUB", amount="10.5")
    v.validate(req)
    v.validate({**req, "kind": "withdraw"})
    v.validate(_m("cash", request_id="r", item=_BOND_SNAP))
    _invalid(v, {**req, "kind": "open"})
    _invalid(v, {k: x for k, x in req.items() if k != "amount"})
    _invalid(v, {k: x for k, x in req.items() if k != "request_id"})
    _invalid(v, {**req, "item": _BOND_SNAP})  # request fields in a response
    _invalid(v, {**req, "amount": 10})  # money is a string


def test_account_v2_set(registry):
    v = _v("set", registry)
    req = _m("set", request_id="r", account_id="bond:p-1", targets=[{"instrument_key": _KEY, "quantity": 0}])
    v.validate(req)
    v.validate(_m("set", request_id="r", item=_BOND_SNAP, rejected=[]))
    for reason in ("no_last_price", "no_fx", "insufficient_cash", "not_in_set", "not_supported", "forbidden"):
        v.validate(_m("set", request_id="r", item=_BOND_SNAP, rejected=[{"instrument_key": _KEY, "reason": reason}]))
    _invalid(v, _m("set", request_id="r", item=_BOND_SNAP, rejected=[{"instrument_key": _KEY, "reason": "x"}]))
    _invalid(v, _m("set", request_id="r", item=_BOND_SNAP))  # response needs rejected
    _invalid(v, _m("set", request_id="r", account_id="a", targets=[]))
    _invalid(v, _m("set", request_id="r", account_id="a", targets=[{"instrument_key": _KEY, "quantity": -1}]))
    _invalid(v, _m("set", request_id="r", account_id="a", targets=[{"instrument_key": _KEY, "quantity": 1.5}]))
    _invalid(v, _m("set", request_id="r", account_id="a", targets=[{"instrument_key": _KEY, "quantity": 1}] * 201))
    _invalid(v, _m("set", request_id="r", targets=req["targets"]))


def test_account_v2_ledger(registry):
    v = _v("ledger", registry)
    v.validate(_m("ledger", request_id="r", account_id="a"))
    v.validate(_m("ledger", request_id="r", account_id="a", before="o9", limit=200))
    v.validate(_m("ledger", request_id="r", account_id="a", items=[_OP], next=None))
    v.validate(_m("ledger", request_id="r", account_id="a", items=[_OP, {**_OP, "kind": "future_kind", "reason": "x", "subkind": None}], next="o1"))
    _invalid(v, _m("ledger", request_id="r", account_id="a", limit=201))
    _invalid(v, _m("ledger", request_id="r", account_id="a", limit=0))
    _invalid(v, _m("ledger", request_id="r", account_id="a", items=[_OP]))  # response needs next
    _invalid(v, _m("ledger", request_id="r", account_id="a", items=[_OP], next=None, limit=5))
    _invalid(v, _m("ledger", request_id="r", account_id="a", items=[{k: x for k, x in _OP.items() if k != "reason"}], next=None))
    _invalid(v, _m("ledger", request_id="r", account_id="a", items=[{**_OP, "amount": 5}], next=None))
    _invalid(v, _m("ledger", account_id="a"))


def test_account_v2_settings(registry):
    v = _v("settings", registry)
    v.validate(_m("settings", request_id="r"))
    v.validate(_m("settings", request_id="r", fx_spread_pct="0.5"))
    _invalid(v, _m("settings", request_id="r", fx_spread_pct=0.5))
    _invalid(v, _m("settings", fx_spread_pct="0.5"))
    _invalid(v, _m("settings", request_id="r", account_id="a"))


def test_account_v2_error_codes(registry):
    v = _v("error", registry)
    for code in ("insufficient_cash", "forbidden", "not_supported"):
        v.validate(_m("error", request_id="r", code=code, message="x"))
    _invalid(v, _m("error", request_id="r", code="insufficient", message="x"))


def test_account_v2_root_dispatch_new_ops(registry):
    root = _root(registry)
    root.validate(_m("cash", request_id="r", account_id="a", kind="deposit", currency="RUB", amount="1"))
    root.validate(_m("ledger", request_id="r", account_id="a"))
    root.validate(_m("settings", request_id="r"))
    root.validate(_m("set", request_id="r", item=_BOND_SNAP, rejected=[]))
