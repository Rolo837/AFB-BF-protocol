"""afbws/deal.channel.v2.json (AFB backend<->AFB frontend only).

Convention (as afbws.alarm/account/tradeplan v2): ONE schema id per message,
the same schema is the request, its response and (record/outcome/event/pnl/
triggered) a server push; a message without `request_id` is a push. The
`event` message is typed per (category, event): every event has exactly one
branch with its own `data` shape.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SPEC = _ROOT / "spec" / "schemas"
_EXAMPLES = _ROOT / "examples" / "deal_channel_v2"
_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/deal.channel.v2.json"
_OPS = {"get", "list", "publish", "rebind", "operation", "amend", "ack", "error",
        "record", "outcome", "event", "pnl", "triggered"}
_PUSHES = {"record", "outcome", "event", "pnl", "triggered"}
_EVENTS = {
    ("deal", "created"), ("deal", "amended"), ("deal", "accepted"), ("deal", "rejected"),
    ("deal", "status_changed"), ("deal", "deleted"), ("deal", "report"), ("deal", "orders_synced"),
    ("deal", "positions_synced"), ("order", "created"), ("order", "filled"), ("order", "partially_filled"),
    ("order", "cancelled"), ("order", "rejected"), ("position", "opened"), ("position", "changed"),
    ("position", "closed"), ("condition", "triggered"),
}

_COND = {"node_type": "event", "op": "above", "left": {"source": "price", "field": "last"},
         "right": {"const": "100"}}
_DETAIL = {
    "deal_id": "d1", "revision": 2, "status": "active", "execution_phase": "holding", "bf_id": "bf1",
    "tradeplan_id": "tp1", "ticker": "SBER", "direction": "long",
    "created_at": "2026-10-21T10:00:00+03:00", "updated_at": "2026-10-21T10:00:00+03:00",
    "deal": {
        "schema": "afb.deal.v2", "deal_id": "d1", "revision": 2,
        "target": {"bf_id": "bf1", "broker": "finam",
                   "instrument": {"exchange": "MOEX", "board": "TQBR", "ticker": "SBER"}},
        "direction": "long", "entry": [{"condition": _COND}], "sizing": {"mode": "lots", "value": "1"},
        "source": {"tradeplan_id": "tp1"},
    },
    "editable_fields": ["stop_loss"],
}
_SUMMARY = {k: v for k, v in _DETAIL.items() if k not in ("deal", "editable_fields")}


def _m(op, **kw):
    return {"channel": "deal", "schema": f"afbws.deal.{op}.v2", **kw}


def _event(category, event, data, **kw):
    return _m("event", deal_id="d1", bf_id="bf1", category=category, event=event,
              logged_at="2026-10-21T10:00:00+03:00", data=data, **kw)


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


def _schema():
    return json.loads((_SPEC / "afbws" / "deal.channel.v2.json").read_text())


def test_deal_v2_one_id_per_message():
    schema = _schema()
    assert schema["x-afbws-support-id"] == "afbws.deal.channel.v2"
    assert _OPS <= set(schema["$defs"])
    stale = {"getRequest", "getResponse", "listRequest", "listResponse", "publishRequest", "publishResponse",
             "rebindRequest", "rebindResponse", "operationRequest", "operationResponse", "amendRequest",
             "amendResponse", "ackRequest", "ackResponse", "errorResponse", "triggeredPush"}
    assert not stale & set(schema["$defs"])
    # message ids: each message def (except the typed unions) carries exactly one schema const
    ids = set()
    for name, d in schema["$defs"].items():
        props = d.get("properties", {})
        if props.get("channel") == {"const": "deal"} and name in _OPS:
            ids.add(props["schema"]["const"])
    assert ids == {f"afbws.deal.{op}.v2" for op in _OPS - {"event"}}
    event_ids = {schema["$defs"][b["$ref"].split("/")[-1]]["properties"]["schema"]["const"]
                 for b in schema["$defs"]["event"]["oneOf"]}
    assert event_ids == {"afbws.deal.event.v2"}
    root = [b["$ref"].split("/")[-1] for b in schema["oneOf"]]
    assert set(root) == _OPS and len(root) == len(_OPS)
    text = json.dumps(schema)
    assert "deal.channel.v1" not in text and "deal.record.v1" not in text
    assert "deal.event.v1" not in text and "deal.pnl.v1" not in text
    assert "details" not in schema["$defs"]["error"]["properties"]
    # one convention for $ref: afbws-local files without `../`, spec/schemas files with it
    for ref in _collect_refs(schema):
        file_part = ref.split("#")[0]
        if file_part in ("common.v1.json", "deal.public.v1.json", ""):
            continue
        assert file_part.startswith("../"), ref


def _collect_refs(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref":
                yield v
            else:
                yield from _collect_refs(v)
    elif isinstance(node, list):
        for item in node:
            yield from _collect_refs(item)


def test_deal_v2_closed_objects():
    schema = _schema()
    for name, d in schema["$defs"].items():
        if d.get("type") == "object" and "properties" in d:
            assert d.get("additionalProperties") is False, name


def test_deal_v2_shared_enums_match_deal_state():
    deal_state = json.loads((_SPEC / "deal_state.v2.json").read_text())
    common = json.loads((_SPEC / "common.v1.json").read_text())
    schema = _schema()
    assert common["$defs"]["dealStatus"]["enum"] == deal_state["properties"]["status"]["enum"]
    assert common["$defs"]["executionPhase"]["enum"] == deal_state["properties"]["execution_phase"]["enum"]
    d = schema["$defs"]
    assert d["dealSummary"]["properties"]["status"] == {"$ref": "../common.v1.json#/$defs/dealStatus"}
    assert d["dealDetail"]["properties"]["execution_phase"] == {"$ref": "../common.v1.json#/$defs/executionPhase"}
    assert d["statusChangedData"]["properties"]["status"] == {"$ref": "../common.v1.json#/$defs/dealStatus"}
    assert d["amend"]["properties"]["status"] == {"$ref": "../common.v1.json#/$defs/dealStatus"}
    order = deal_state["$defs"]["order"]["properties"]
    assert set(order["role"]["enum"]) <= set(d["orderRole"]["enum"])
    assert set(d["orderRole"]["enum"]) - set(order["role"]["enum"]) == {"external_close"}
    assert set(order["status"]["enum"]) <= set(d["orderEventStatus"]["enum"])
    assert set(d["orderEventStatus"]["enum"]) - set(order["status"]["enum"]) == {"unknown"}
    assert d["orderSide"]["enum"] == order["side"]["enum"]
    tradeplan = json.loads((_SPEC / "afbws" / "tradeplan.channel.v2.json").read_text())
    assert "dealStatus" not in tradeplan["$defs"]


def test_deal_v2_summary_and_detail(registry):
    v = _v("dealSummary", registry)
    v.validate(_SUMMARY)
    v.validate(_with(_SUMMARY, instrument_key="MISX:TQBR:SBER", market="stock",
                     broker_sizing={"lots": 1, "required_cash": "100", "resolved_lots": 1},
                     position={"qty": 1, "avg_price": "1", "as_of": "t"},
                     realized_pnl={"value": None, "degraded": "missing_price"}))
    for status in ("draft", "publishing", "published", "active", "paused", "closed", "cancelled", "orphaned"):
        v.validate(_with(_SUMMARY, status=status))
    for status in ("deleted", "new", "weird", ""):
        _invalid(v, _with(_SUMMARY, status=status))
    for phase in ("idle", "awaiting_entry", "entry_working", "holding", "exit_working"):
        v.validate(_with(_SUMMARY, execution_phase=phase))
    _invalid(v, _with(_SUMMARY, execution_phase="running"))
    for field in ("source_refs", "status_history", "event_journal", "orders", "owner_user_id",
                  "broker_instrument", "observed", "deal"):
        _invalid(v, _with(_SUMMARY, **{field: {}}))
    for field in ("deal_id", "revision", "status", "execution_phase", "bf_id", "tradeplan_id", "ticker",
                  "direction", "created_at", "updated_at"):
        _invalid(v, _with(_SUMMARY, **{field: None}))
    _invalid(v, _with(_SUMMARY, realized_pnl={"value": "1", "degraded": "missing_price"}))
    d = _v("dealDetail", registry)
    d.validate(_DETAIL)
    _invalid(d, _with(_DETAIL, deal=None))
    _invalid(d, _with(_DETAIL, editable_fields=None))
    _invalid(d, _with(_DETAIL, editable_fields=["instrument"]))
    _invalid(d, _with(_DETAIL, source_refs={}))


def test_deal_v2_get_list(registry):
    v = _v("get", registry)
    v.validate(_m("get", request_id="r", deal_id="d1"))
    v.validate(_m("get", request_id="r", item=_DETAIL))
    _invalid(v, _m("get", deal_id="d1"))
    _invalid(v, _m("get", request_id="r"))
    _invalid(v, _m("get", request_id="r", deal_id="d1", item=_DETAIL))
    _invalid(v, _m("get", request_id="r", item=_SUMMARY))
    v = _v("list", registry)
    v.validate(_m("list", request_id="r"))
    v.validate(_m("list", request_id="r", items=[_SUMMARY]))
    v.validate(_m("list", request_id="r", items=[]))
    _invalid(v, _m("list"))
    _invalid(v, _m("list", request_id="r", tradeplan_id="tp1"))
    _invalid(v, _m("list", request_id="r", items=[_DETAIL]))


def test_deal_v2_result(registry):
    v = _v("dealResult", registry)
    v.validate({"deal_id": "d1", "bf_id": "bf1", "status": "published", "accepted": True})
    v.validate({"deal_id": "d1", "bf_id": "bf1", "status": "deleted", "accepted": True})
    v.validate({"deal_id": "d1", "bf_id": "bf1", "status": "active", "accepted": True, "revision": 2,
                "item": _DETAIL})
    v.validate({"deal_id": "d1", "accepted": False, "message": "no"})
    _invalid(v, {"deal_id": "d1", "bf_id": "bf1", "status": "weird", "accepted": True})
    _invalid(v, {"deal_id": "d1", "accepted": True})
    _invalid(v, {"deal_id": "d1", "bf_id": "bf1", "status": "active", "accepted": True, "message": "x"})
    _invalid(v, {"deal_id": "d1", "accepted": False})
    _invalid(v, {"deal_id": "d1", "bf_id": "bf1", "status": "active", "accepted": False, "message": "x"})
    _invalid(v, {"deal_id": "d1", "bf_id": "bf1", "status": "active", "accepted": True, "code": "x"})
    _invalid(v, {"deal_id": "d1", "bf_id": "bf1", "status": "active", "accepted": True, "item": _SUMMARY})


def test_deal_v2_publish_rebind(registry):
    row = {"deal_id": "d1", "bf_id": "bf1", "status": "published", "accepted": True}
    v = _v("publish", registry)
    v.validate(_m("publish", request_id="r", tradeplan_id="tp1", bf_id="bf1"))
    v.validate(_m("publish", request_id="r", results=[row], accepted=True))
    _invalid(v, _m("publish", tradeplan_id="tp1", bf_id="bf1"))
    _invalid(v, _m("publish", request_id="r", tradeplan_id="tp1"))
    _invalid(v, _m("publish", request_id="r", results=[row]))
    _invalid(v, _m("publish", request_id="r", tradeplan_id="tp1", bf_id="bf1", results=[row], accepted=True))
    _invalid(v, _m("publish", request_id="r", tradeplan_id="tp1", bf_id="bf1", accepted=True))
    _invalid(v, _m("publish", request_id="r", tradeplan_id="", bf_id="bf1"))
    v = _v("rebind", registry)
    v.validate(_m("rebind", request_id="r", deal_id="d1", bf_id="bf1"))
    v.validate(_m("rebind", request_id="r", results=[row], accepted=True))
    _invalid(v, _m("rebind", request_id="r", deal_id="d1"))
    _invalid(v, _m("rebind", request_id="r", results=[row]))
    _invalid(v, _m("rebind", request_id="r", deal_id="d1", bf_id="bf1", results=[row], accepted=True))


def test_deal_v2_operation(registry):
    row = {"deal_id": "d1", "bf_id": "bf1", "status": "paused", "accepted": True}
    v = _v("operation", registry)
    v.validate(_m("operation", request_id="r", items=[{"deal_id": "d1", "action": "pause"}]))
    v.validate(_m("operation", request_id="r", items=[{"deal_id": "d1", "action": "cancel",
                                                       "cancel_open_orders": False}]))
    v.validate(_m("operation", request_id="r", results=[row, {"deal_id": "d2", "accepted": False, "message": "x"}],
                  accepted=True))
    for action in ("activate", "pause", "resume", "cancel", "reconcile", "delete"):
        v.validate(_m("operation", request_id="r", items=[{"deal_id": "d1", "action": action}]))
    _invalid(v, _m("operation", request_id="r", items=[]))
    _invalid(v, _m("operation", request_id="r", items=[{"deal_id": "d1", "action": "archive"}]))
    _invalid(v, _m("operation", request_id="r", items=[{"deal_id": "d1", "action": "pause",
                                                        "cancel_open_orders": True}]))
    _invalid(v, _m("operation", request_id="r", items=[{"deal_id": "d1", "action": "pause", "revision": 1}]))
    _invalid(v, _m("operation", request_id="r"))
    _invalid(v, _m("operation", request_id="r", results=[row]))
    _invalid(v, _m("operation", request_id="r", items=[{"deal_id": "d1", "action": "pause"}], results=[row],
                   accepted=True))


def test_deal_v2_amend(registry):
    edit = {
        "entry": {"edited": [{"index": 0, "condition": _COND, "percent": "50", "logic": "and"}],
                  "removed_indices": [1], "reset_indices": [2], "new_legs": [{"condition": _COND}]},
        "stop_loss": {}, "sizing": {"mode": "lots", "value": "2"}, "execution_policy": {"margin_trading": True},
    }
    v = _v("amend", registry)
    v.validate(_m("amend", request_id="r", deal_id="d1"))
    v.validate(_m("amend", request_id="r", deal_id="d1", base_revision=2, deal_edit=edit))
    v.validate(_m("amend", request_id="r", item=_DETAIL, revision=3, status="active", accepted=True))
    _invalid(v, _m("amend", deal_id="d1"))
    _invalid(v, _m("amend", request_id="r"))
    _invalid(v, _m("amend", request_id="r", item=_DETAIL, revision=3, status="active"))
    _invalid(v, _m("amend", request_id="r", item=_DETAIL, revision=3, status="deleted", accepted=True))
    _invalid(v, _m("amend", request_id="r", item=_DETAIL, revision=3, status="active", accepted=True,
                   base_revision=2))
    _invalid(v, _m("amend", request_id="r", deal_id="d1", accepted=True))
    _invalid(v, _m("amend", request_id="r", deal_id="d1", base_revision=0))
    _invalid(v, _m("amend", request_id="r", deal_id="d1", deal_edit={"instrument": {}}))
    _invalid(v, _m("amend", request_id="r", deal_id="d1", deal_edit={"entry": {"edited": [{"condition": _COND}]}}))
    _invalid(v, _m("amend", request_id="r", deal_id="d1", deal_edit={"entry": {"new_legs": [{"percent": "1"}]}}))


def test_deal_v2_ack(registry):
    ev = {"schema": "afb.deal.trigger_ack.v2", "notification_id": "n1"}
    res = {"schema": "afbws.deal.ack_result.v2", "notification_id": "n1", "status": "ok"}
    v = _v("ack", registry)
    v.validate(_m("ack", request_id="r", events=[ev]))
    v.validate(_m("ack", request_id="r", results=[res]))
    v.validate(_m("ack", request_id="r", results=[{**res, "status": "not_found"}]))
    _invalid(v, _m("ack", request_id="r"))
    _invalid(v, _m("ack", request_id="r", events=[]))
    _invalid(v, _m("ack", request_id="r", events=[ev], results=[res]))
    _invalid(v, _m("ack", request_id="r", events=[{**ev, "schema": "afb.deal.trigger_ack.v1"}]))
    _invalid(v, _m("ack", request_id="r", results=[{**res, "status": "late"}]))
    _invalid(v, _m("ack", events=[ev]))


def test_deal_v2_error(registry):
    v = _v("error", registry)
    v.validate(_m("error", request_id="r", code="not_found", message="x"))
    v.validate(_m("error", request_id="r", code="conflict", message="x"))
    v.validate(_m("error", request_id="r", code="conflict", message="x", item=_DETAIL))
    for code in ("invalid_schema", "invalid_channel", "validation_error", "internal_error", "forbidden",
                 "bf_offline"):
        v.validate(_m("error", request_id="r", code=code, message="x"))
    _invalid(v, _m("error", code="not_found", message="x"))
    _invalid(v, _m("error", request_id="r", code="nope", message="x"))
    _invalid(v, _m("error", request_id="r", code="not_found", message=""))
    # the authoritative record only comes with `conflict`; no code carries `details`
    _invalid(v, _m("error", request_id="r", code="not_found", message="x", item=_DETAIL))
    _invalid(v, _m("error", request_id="r", code="conflict", message="x", item=_SUMMARY))
    _invalid(v, _m("error", request_id="r", code="conflict", message="x", details={}))
    _invalid(v, _m("error", request_id="r", code="not_found", message="x", details={"deal_ids": ["d1"]}))


def test_deal_v2_record(registry):
    v = _v("record", registry)
    v.validate(_m("record", deal_id="d1", bf_id="bf1", item=_DETAIL))
    _invalid(v, _m("record", request_id="r", deal_id="d1", bf_id="bf1", item=_DETAIL))  # push only
    _invalid(v, _m("record", deal_id="d1", bf_id="bf1", item=_SUMMARY))
    _invalid(v, _m("record", deal_id="d1", bf_id="bf1"))
    # the outcome is a separate push
    _invalid(v, _m("record", deal_id="d1", bf_id="bf1", item=_DETAIL,
                   outcome={"command": "deal.amend", "result": "accepted"}))


def test_deal_v2_outcome(registry):
    base = {"deal_id": "d1", "bf_id": "bf1"}
    v = _v("outcome", registry)
    v.validate(_m("outcome", **base, command="deal.amend", result="accepted"))
    v.validate(_m("outcome", **base, command="deal.amend", result="rejected", code="x", message="m"))
    v.validate(_m("outcome", **base, command=None, result="rejected", code="x", message=None))
    v.validate(_m("outcome", **base, command=None, result="rejected", code="x",
                  broker_error={"kind": "insufficient_funds", "native_code": "145", "native_message": "m"}))
    _invalid(v, _m("outcome", request_id="r", **base, command="deal.amend", result="accepted"))
    _invalid(v, _m("outcome", **base, result="accepted"))  # command is mandatory (nullable)
    _invalid(v, _m("outcome", **base, command="deal.operation", result="accepted"))
    _invalid(v, _m("outcome", **base, command=None, result="accepted"))
    _invalid(v, _m("outcome", **base, command="deal.amend", result="accepted", code="x"))
    _invalid(v, _m("outcome", **base, command="deal.amend", result="accepted", message=None))
    _invalid(v, _m("outcome", **base, command="deal.amend", result="rejected"))  # code required
    _invalid(v, _m("outcome", **base, command="deal.amend", result="rejected", code=""))
    _invalid(v, _m("outcome", **base, command="deal.amend", result="pending"))
    _invalid(v, _m("outcome", **base, command="deal.amend", result="rejected", code="x", broker_error={}))


def test_deal_v2_pnl(registry):
    data = {"unrealized": "1.5", "currency": "RUB", "qty": 2, "avg_price": "10", "last_price": "11",
            "as_of": "t"}
    v = _v("pnl", registry)
    v.validate(_m("pnl", deal_id="d1", bf_id="bf1", data=data))
    _invalid(v, _m("pnl", request_id="r", deal_id="d1", bf_id="bf1", data=data))
    _invalid(v, _m("pnl", deal_id="d1", bf_id="bf1", data={**data, "trend": "up"}))
    _invalid(v, _m("pnl", deal_id="d1", bf_id="bf1", data={k: x for k, x in data.items() if k != "qty"}))


def test_deal_v2_triggered(registry):
    base = {"schema": "afb.deal.trigger.v2", "notification_id": "n1", "deal_id": "d1", "bf_id": "bf1",
            "created_at": "t"}
    ok = [
        {**base, "event": "status_changed", "data": {"status": "closed", "last_price": "1"}},
        {**base, "event": "rejected", "data": {"code": "x", "broker_error": {"kind": "rejected"}}},
        {**base, "event": "report", "data": {"status": "closed", "close_reason": "take_profit"}},
    ]
    v = _v("triggered", registry)
    v.validate(_m("triggered", events=ok))
    _invalid(v, _m("triggered", events=[]))
    _invalid(v, _m("triggered", request_id="r", events=ok))
    # only MAIL_DEAL_EVENTS, each with its own data shape
    _invalid(v, _m("triggered", events=[{**base, "event": "created", "data": {"revision": 1}}]))
    _invalid(v, _m("triggered", events=[{**base, "event": "status_changed", "data": {"status": "deleted"}}]))
    _invalid(v, _m("triggered", events=[{**base, "event": "status_changed", "data": {"code": "x"}}]))
    _invalid(v, _m("triggered", events=[{**base, "event": "report", "data": {"status": "closed", "fills": []}}]))
    _invalid(v, _m("triggered", events=[{**base, "event": "rejected", "data": {}}]))
    _invalid(v, _m("triggered", events=[{**base, "event": "report", "data": {"status": "closed"}, "extra": 1}]))
    _invalid(v, _m("triggered", events=[{**base, "schema": "afb.deal.trigger.v1", "event": "report",
                                         "data": {"status": "closed"}}]))


def test_deal_v2_event_branches_cover_each_event_once():
    schema = _schema()
    seen = []
    for branch in schema["$defs"]["event"]["oneOf"]:
        d = schema["$defs"][branch["$ref"].split("/")[-1]]
        props = d["properties"]
        assert props["schema"] == {"const": "afbws.deal.event.v2"}
        assert set(d["required"]) == {"channel", "schema", "deal_id", "bf_id", "category", "event", "logged_at",
                                      "data"}
        assert "$ref" in props["data"]
        seen.append((props["category"]["const"], props["event"]["const"]))
    assert len(seen) == len(set(seen))
    assert set(seen) == _EVENTS


def test_deal_v2_event_data(registry):
    root = _root(registry)
    at = "2026-10-21T10:00:00+03:00"
    order = {"order_id": "o1", "side": "buy", "role": "entry", "quantity": 1, "price": "10", "status": "filled",
             "filled_quantity": 1, "at": at}
    valid = [
        ("deal", "created", {"revision": 1}),
        ("deal", "amended", {"revision": 2}),
        ("deal", "accepted", {"command_type": "deal.amend"}),
        ("deal", "accepted", {"command_type": "deal.publish", "revision": 1, "at": at}),
        ("deal", "rejected", {"code": "x"}),
        ("deal", "rejected", {"code": "x", "message": "m", "command_type": "deal.amend",
                              "broker_error": {"kind": "invalid_order"}, "at": at}),
        ("deal", "status_changed", {"status": "active"}),
        ("deal", "status_changed", {"status": "paused", "execution_phase": "holding", "last_price": "1",
                                    "cancel_reason": "x", "quantity": 3, "at": at}),
        ("deal", "deleted", {}),
        ("deal", "deleted", {"reason": "user_delete", "archived_at": at, "revision": 2}),
        ("deal", "report", {"status": "closed"}),
        ("deal", "report", {"status": "closed", "close_reason": "stop_loss", "fills": [
            {"trade_id": "t", "order_id": "o1", "role": "entry", "side": "buy", "price": None, "quantity": 1,
             "timestamp": None}]}),
        ("deal", "orders_synced", {}),
        ("deal", "positions_synced", {"at": at}),
        ("order", "created", {"order_id": "o1", "broker_order_id": "b1", "side": "buy", "role": "backstop",
                              "quantity": 1, "price": None, "status": "new"}),
        ("order", "filled", order),
        ("order", "partially_filled", {**order, "status": "partially_filled", "leg_index": 0}),
        ("order", "cancelled", {**order, "status": "expired", "role": "external_close"}),
        ("order", "rejected", {"order_id": "o1", "side": "sell", "role": "stop_loss", "status": "rejected"}),
        ("position", "opened", {"symbol": "SBER@MISX", "quantity": 1, "average_price": "10"}),
        ("position", "changed", {"symbol": "SBER", "quantity": -2, "average_price": None, "at": at}),
        ("position", "closed", {"symbol": "SBER", "quantity": 0}),
        ("condition", "triggered", {"condition_id": "c1", "phase": "entry"}),
        ("condition", "triggered", {"condition_id": "c1", "price": "10", "phase": "take_profit", "at": at}),
    ]
    for category, event, data in valid:
        root.validate(_event(category, event, data))
    seen = {(c, e) for c, e, _ in valid}
    assert seen == _EVENTS
    invalid = [
        ("deal", "created", {}),
        ("deal", "created", {"revision": 1, "at": at}),  # produced by AFB, no BF time
        ("deal", "created", {"revision": 0}),
        ("deal", "created", {"revision": 1, "status": "draft", "deal_id": "d1"}),  # no snapshot
        ("deal", "amended", {"revision": 2, "deal": {}}),
        ("deal", "accepted", {"revision": 1}),
        ("deal", "accepted", {"command_type": "deal.amend", "broker_instrument": {}}),
        ("deal", "accepted", {"command_type": "deal.amend", "validation": {}}),
        ("deal", "accepted", {"command_type": "deal.amend", "binding": {}}),
        ("deal", "accepted", {"command_type": "deal.amend", "target_instrument_patch": {}}),
        ("deal", "rejected", {"message": "m"}),
        ("deal", "rejected", {"code": "x", "reason": "r"}),
        ("deal", "rejected", {"code": "x", "broker_error": {}}),
        ("deal", "status_changed", {}),
        ("deal", "status_changed", {"status": "deleted"}),  # deleted is its own event
        ("deal", "status_changed", {"status": "waiting"}),
        ("deal", "status_changed", {"status": "active", "execution_phase": "x"}),
        ("deal", "status_changed", {"status": "active", "revision": 1}),
        ("deal", "deleted", {"status": "deleted"}),
        ("deal", "report", {}),
        ("deal", "report", {"status": "closed", "summary": {"realized_pnl": "1"}}),
        ("deal", "report", {"status": "closed", "fills": [{"order_id": "o1", "role": "entry"}]}),
        ("deal", "report", {"status": "closed", "fills": [{"order_id": "o1", "role": "x", "side": "buy"}]}),
        ("deal", "orders_synced", {"changed": []}),
        ("deal", "snapshot", {}),
        ("deal", "archived", {"reason": "user_delete"}),
        ("order", "created", {"order_id": "o1", "side": "buy", "role": "entry"}),
        ("order", "created", {"order_id": "o1", "side": "short", "role": "entry", "status": "new"}),
        ("order", "created", {"order_id": "o1", "side": "buy", "role": "exit", "status": "new"}),
        ("order", "created", {"order_id": "o1", "side": "buy", "role": "entry", "status": "pending"}),
        ("order", "created", {"order_id": "o1", "side": "buy", "role": "entry", "status": "new",
                              "client_order_id": "o1"}),
        ("order", "filled", {**order, "price": 10}),
        ("order", "filled", {k: x for k, x in order.items() if k != "order_id"}),
        ("order", "unknown", order),
        ("position", "opened", {"quantity": 1}),
        ("position", "opened", {"symbol": "S", "quantity": 1, "instrument": {"ticker": "S"}}),
        ("position", "closed", {"symbol": "S", "quantity": 0, "broker_ref": {"symbol": "S"}}),
        ("position", "changed", {"symbol": "S", "quantity": "1"}),
        ("condition", "triggered", {"condition_id": "c1"}),
        ("condition", "triggered", {"condition_id": "c1", "phase": "exit"}),
        ("condition", "triggered", {"phase": "entry"}),
        ("condition", "triggered", {"condition_id": "c1", "phase": "entry", "eval": {}}),
        ("condition", "created", {"revision": 1}),
    ]
    for category, event, data in invalid:
        _invalid(root, _event(category, event, data))
    # category is bound to the event; no push may carry request_id
    _invalid(root, _event("order", "created", {"revision": 1}))
    _invalid(root, _event("deal", "filled", order))
    _invalid(root, _event("order", "report", {"status": "closed"}))
    _invalid(root, _event("deal", "created", {"revision": 1}, request_id="r"))
    _invalid(root, _event("trade", "created", {"revision": 1}))
    _invalid(root, _with(_event("deal", "created", {"revision": 1}), data=None))
    _invalid(root, _with(_event("deal", "created", {"revision": 1}), logged_at=None))


def test_deal_v2_root_dispatch(registry):
    root = _root(registry)
    root.validate(_m("get", request_id="r", deal_id="d1"))
    root.validate(_m("record", deal_id="d1", bf_id="bf1", item=_DETAIL))
    root.validate(_m("operation", request_id="r", items=[{"deal_id": "d1", "action": "pause"}]))
    # v1 ids and suffixed ids are rejected
    for schema in ("afbws.deal.get.request.v1", "afbws.deal.get.response.v1", "afbws.deal.record.push.v1",
                   "afbws.deal.event.push.v1", "afbws.deal.pnl.push.v1", "afbws.deal.triggered.push.v1",
                   "afbws.deal.error.response.v1", "afbws.deal.get.request.v2", "afbws.deal.record.push.v2",
                   "afbws.deal.archive.v2"):
        _invalid(root, {"channel": "deal", "schema": schema, "request_id": "r", "deal_id": "d1"})
    _invalid(root, _m("get", request_id="r", deal_id="d1", unexpected=1))
    _invalid(root, {**_m("get", request_id="r", deal_id="d1"), "channel": "alarm"})


def test_deal_v2_examples_validate(registry):
    root = _root(registry)
    files = sorted(_EXAMPLES.glob("*.json"))
    assert len(files) >= 40
    seen = set()
    events = set()
    for path in files:
        message = json.loads(path.read_text(encoding="utf-8"))
        root.validate(message)
        seen.add(message["schema"])
        if message["schema"] == "afbws.deal.event.v2":
            events.add((message["category"], message["event"]))
            assert path.name == f"event.{message['category']}.{message['event']}.push.json"
        # pushes carry no request_id
        if message["schema"].split(".")[2] in _PUSHES:
            assert "request_id" not in message, path.name
    assert seen == {f"afbws.deal.{op}.v2" for op in _OPS}
    assert events == _EVENTS
    # every example item is a valid deal.public projection (checked through dealDetail's $ref)
    for name in ("get.response", "record.push", "error.conflict"):
        message = json.loads((_EXAMPLES / f"{name}.json").read_text())
        assert "source_refs" not in json.dumps(message)
