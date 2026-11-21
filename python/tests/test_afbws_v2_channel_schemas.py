"""afbws/alarm.channel.v2.json and afbws/gp.channel.v2.json (AFB backend<->AFB
frontend only).

Convention (as afbws.market): ONE schema id per message, the same schema is
the request, its response and (where documented) a server push; a message
without `request_id` is a push.
"""
from __future__ import annotations

import json

import pytest

from conftest import EXAMPLES

_BASE = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/"
_ALARM = _BASE + "alarm.channel.v2.json"
_GP = _BASE + "gp.channel.v2.json"
_ALARM_ITEM = json.loads((EXAMPLES / "alarms_v2" / "alarm.touch.json").read_text())
_GP_ITEM = {
    "schema": "afb.gp.v2", "id": "gp-1", "instrument_key": "MISX:TQBR:SBER", "kind": "trendline",
    "settings": {"start": {"time": 1721000000, "price": 1.0}, "stop": {"time": 1721000600, "price": 2.0}},
}
_IND = {
    "id": "ind-1", "type": "kama", "scope": "shared",
    "settings": {"erPeriod": 10, "fastPeriod": 2, "slowPeriod": 30},
    "style": {"seriesType": "Line", "color": "#ffffffff", "lineWidth": 2, "lineStyle": 1},
}
_KEY = "MISX:TQBR:SBER"


def _v(channel_id, def_name, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{channel_id}#/$defs/{def_name}"}, registry=registry)


def _root(channel_id, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": channel_id}, registry=registry)


def _invalid(validator, message):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        validator.validate(message)


# --------------------------------------------------------------------- alarm
def test_alarm_v2_no_request_response_pairs(registry):
    """No duplicated .request/.response/.push ids and no `get` left."""
    schema = json.loads((EXAMPLES.parent / "spec" / "schemas" / "afbws" / "alarm.channel.v2.json").read_text())
    assert set(schema["$defs"]) >= {"list", "set", "delete", "ack", "triggered", "error"}
    assert not {"getRequest", "getResponse", "setRequest", "setResponse", "listRequest", "listResponse"} & set(schema["$defs"])
    ids = {d["properties"]["schema"]["const"] for d in schema["$defs"].values() if "schema" in d.get("properties", {}) and "channel" in d["properties"]}
    assert ids == {f"afbws.alarm.{op}.v2" for op in ("list", "set", "delete", "ack", "triggered", "error")}


def test_alarm_v2_list_set_delete(registry):
    msg = lambda schema, **kw: {"channel": "alarm", "schema": f"afbws.alarm.{schema}.v2", "request_id": "r", **kw}
    # list: request filters / response items share one schema
    _v(_ALARM, "list", registry).validate(msg("list"))
    _v(_ALARM, "list", registry).validate(msg("list", ids=["a"], instrument_keys=[_KEY]))
    _v(_ALARM, "list", registry).validate(msg("list", items=[_ALARM_ITEM]))
    _invalid(_v(_ALARM, "list", registry), msg("list", ids=["a"], items=[_ALARM_ITEM]))
    # set: batched items, partial failure in rejected[]
    _v(_ALARM, "set", registry).validate(msg("set", items=[_ALARM_ITEM]))
    _v(_ALARM, "set", registry).validate(msg("set", items=[], rejected=[{"id": "a", "code": "validation_error", "message": "x"}]))
    # delete: by ids and/or instrument_keys (all alarms of an instrument)
    _v(_ALARM, "delete", registry).validate(msg("delete", ids=["a", "b"]))
    _v(_ALARM, "delete", registry).validate(msg("delete", instrument_keys=[_KEY]))
    _v(_ALARM, "delete", registry).validate(msg("delete", ids=[], rejected=[{"id": "a", "code": "not_found"}]))
    _invalid(_v(_ALARM, "delete", registry), msg("delete"))


def test_alarm_v2_single_item_is_gone(registry):
    msg = {"channel": "alarm", "schema": "afbws.alarm.set.v2", "request_id": "r"}
    _invalid(_v(_ALARM, "set", registry), {**msg, "item": _ALARM_ITEM})
    _invalid(_v(_ALARM, "delete", registry), {**msg, "schema": "afbws.alarm.delete.v2", "id": "a"})
    # v1 items and a ticker filter are rejected
    v1_item = json.loads((EXAMPLES / "alarms_v2" / "alarm.touch.json").read_text())
    v1_item = {**v1_item, "schema": "afb.alarm.v1", "ticker": "SBER"}
    del v1_item["instrument_key"]
    _invalid(_v(_ALARM, "set", registry), {**msg, "items": [v1_item]})
    _invalid(_v(_ALARM, "list", registry), {**msg, "schema": "afbws.alarm.list.v2", "ticker": "SBER"})


def test_alarm_v2_triggered_push_and_ack(registry):
    _v(_ALARM, "triggered", registry).validate({
        "channel": "alarm", "schema": "afbws.alarm.triggered.v2",
        "events": [{"schema": "afb.alarm.trigger.v2", "alarm_id": "a", "triggered_at": "t", "alarm": _ALARM_ITEM}]})
    ack = {"channel": "alarm", "schema": "afbws.alarm.ack.v2", "request_id": "r"}
    ev = {"schema": "afb.alarm.trigger_ack.v2", "alarm_id": "a", "triggered_at": "t"}
    res = {"schema": "afbws.alarm.ack_result.v2", "alarm_id": "a", "triggered_at": "t", "status": "ok"}
    _v(_ALARM, "ack", registry).validate({**ack, "events": [ev]})
    _v(_ALARM, "ack", registry).validate({**ack, "results": [res]})
    _invalid(_v(_ALARM, "ack", registry), {**ack, "events": [ev], "results": [res]})
    _invalid(_v(_ALARM, "ack", registry), ack)


def test_alarm_v2_error(registry):
    _v(_ALARM, "error", registry).validate(
        {"channel": "alarm", "schema": "afbws.alarm.error.v2", "request_id": "r", "code": "validation_error", "message": "bad"})


def test_alarm_v2_root_dispatch(registry):
    root = _root(_ALARM, registry)
    root.validate({"channel": "alarm", "schema": "afbws.alarm.list.v2", "request_id": "r"})
    _invalid(root, {"channel": "alarm", "schema": "afbws.alarm.list.request.v2", "request_id": "r"})


# ------------------------------------------------------------------------ gp
def test_gp_v2_no_request_response_pairs(registry):
    schema = json.loads((EXAMPLES.parent / "spec" / "schemas" / "afbws" / "gp.channel.v2.json").read_text())
    expected = {"list", "set", "delete", "indicatorList", "indicatorSet", "indicatorDelete",
                "datasetList", "datasetSet", "datasetDelete", "presetList", "presetSet", "presetDelete", "presetRejection", "style", "error"}
    assert expected <= set(schema["$defs"])
    stale = {"getRequest", "getResponse", "setRequest", "setResponse", "deleteRequest", "deleteResponse", "syncPush",
             "indicatorSyncPush", "indicatorSetRequest", "indicatorSetResponse", "errorResponse"}
    assert not stale & set(schema["$defs"])
    ids = {d["properties"]["schema"]["const"] for d in schema["$defs"].values() if "schema" in d.get("properties", {}) and "channel" in d["properties"]}
    assert ids == {
        "afbws.gp.list.v2", "afbws.gp.set.v2", "afbws.gp.delete.v2", "afbws.gp.indicator.list.v2",
        "afbws.gp.indicator.set.v2", "afbws.gp.indicator.delete.v2", "afbws.gp.dataset.list.v2",
        "afbws.gp.dataset.set.v2", "afbws.gp.dataset.delete.v2", "afbws.gp.preset.list.v2",
        "afbws.gp.preset.set.v2", "afbws.gp.preset.delete.v2", "afbws.gp.style.v2", "afbws.gp.error.v2",
    }


def test_gp_v2_list(registry):
    m = {"channel": "gp", "schema": "afbws.gp.list.v2", "request_id": "r"}
    v = _v(_GP, "list", registry)
    v.validate(m)
    v.validate({**m, "ids": ["gp-1"]})
    v.validate({**m, "instrument_keys": [_KEY]})
    v.validate({**m, "items": [_GP_ITEM]})
    _invalid(v, {**m, "instrument_keys": [_KEY], "items": [_GP_ITEM]})
    _invalid(v, {**m, "instrument_key": _KEY})


def test_gp_v2_set_request_response_push(registry):
    v = _v(_GP, "set", registry)
    base = {"channel": "gp", "schema": "afbws.gp.set.v2"}
    # request: batched upsert
    v.validate({**base, "request_id": "r", "items": [_GP_ITEM, dict(_GP_ITEM, id="gp-2")]})
    # response: partial failure — applied items + rejected with authoritative item/details
    v.validate({**base, "request_id": "r", "items": [], "rejected": [{
        "id": "gp-1", "code": "conflict", "message": "locked", "item": _GP_ITEM,
        "details": {"tradeplan_ids": ["tp"], "deal_ids": ["d"], "locked_scopes": ["entry"]}}]})
    # push: no request_id, non-empty items, no rejected
    v.validate({**base, "items": [_GP_ITEM]})
    _invalid(v, {**base, "items": []})
    _invalid(v, {**base, "items": [_GP_ITEM], "rejected": [{"id": "gp-1", "code": "conflict"}]})
    # the single `item` form is gone
    _invalid(v, {**base, "request_id": "r", "item": _GP_ITEM})
    # v1 item
    _invalid(v, {**base, "request_id": "r", "items": [dict(_GP_ITEM, schema="afb.gp.v1")]})


def test_gp_v2_delete_by_ids_and_by_instrument(registry):
    v = _v(_GP, "delete", registry)
    base = {"channel": "gp", "schema": "afbws.gp.delete.v2"}
    v.validate({**base, "request_id": "r", "ids": ["a", "b"]})
    v.validate({**base, "request_id": "r", "instrument_keys": [_KEY]})  # "clear all of an instrument" in one message
    v.validate({**base, "request_id": "r", "ids": ["a"], "rejected": [{"id": "b", "code": "conflict", "details": {"tradeplan_ids": ["tp"]}}]})
    v.validate({**base, "request_id": "r", "ids": []})  # nothing removed
    _invalid(v, {**base, "request_id": "r"})
    # push (no request_id): ids only
    v.validate({**base, "ids": ["a"]})
    _invalid(v, {**base, "instrument_keys": [_KEY]})
    _invalid(v, {**base, "ids": []})
    _invalid(v, {**base, "request_id": "r", "id": "a"})


def test_gp_v2_indicator_commands(registry):
    base = {"channel": "gp", "request_id": "r"}
    lst = _v(_GP, "indicatorList", registry)
    lst.validate({**base, "schema": "afbws.gp.indicator.list.v2"})
    lst.validate({**base, "schema": "afbws.gp.indicator.list.v2", "items": [_IND]})
    st = _v(_GP, "indicatorSet", registry)
    st.validate({**base, "schema": "afbws.gp.indicator.set.v2", "items": [_IND]})
    st.validate({**base, "schema": "afbws.gp.indicator.set.v2", "items": [], "rejected": [{"id": "ind-1", "code": "forbidden", "message": "manager only"}]})
    _invalid(st, {**base, "schema": "afbws.gp.indicator.set.v2", "item": _IND})
    # `enabled` is not protocol any more
    _invalid(st, {**base, "schema": "afbws.gp.indicator.set.v2", "items": [dict(_IND, enabled=True)]})
    dl = _v(_GP, "indicatorDelete", registry)
    dl.validate({**base, "schema": "afbws.gp.indicator.delete.v2", "ids": ["ind-1"]})
    dl.validate({**base, "schema": "afbws.gp.indicator.delete.v2", "ids": [], "rejected": [{"id": "x", "code": "not_found"}]})
    _invalid(dl, {**base, "schema": "afbws.gp.indicator.delete.v2", "id": "ind-1"})


def test_gp_v2_indicator_shared_push(registry):
    """Shared-indicator deltas reuse indicator.set / indicator.delete without request_id."""
    st = _v(_GP, "indicatorSet", registry)
    st.validate({"channel": "gp", "schema": "afbws.gp.indicator.set.v2", "items": [_IND]})
    _invalid(st, {"channel": "gp", "schema": "afbws.gp.indicator.set.v2", "items": []})
    dl = _v(_GP, "indicatorDelete", registry)
    dl.validate({"channel": "gp", "schema": "afbws.gp.indicator.delete.v2", "ids": ["ind-1"]})
    _invalid(dl, {"channel": "gp", "schema": "afbws.gp.indicator.delete.v2", "ids": ["ind-1"], "rejected": [{"id": "x", "code": "not_found"}]})


def test_gp_v2_style(registry):
    v = _v(_GP, "style", registry)
    base = {"channel": "gp", "schema": "afbws.gp.style.v2"}
    styles = {"line": {"color": "#112233ff", "lineWidth": 3, "lineStyle": 0}, "zone": {"color": "#445566ff", "lineWidth": 1, "lineStyle": 2}}
    v.validate({**base, "request_id": "r"})                        # read
    v.validate({**base, "request_id": "r", "styles": styles})      # write / response
    v.validate({**base, "styles": styles})                         # push to other connections
    _invalid(v, base)                                               # push without styles
    _invalid(v, {**base, "request_id": "r", "styles": {"line": {"color": "red", "lineWidth": 3, "lineStyle": 0}}})
    _invalid(v, {**base, "request_id": "r", "styles": {"circle": styles["line"]}})


def test_gp_v2_error(registry):
    _v(_GP, "error", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.error.v2", "request_id": "r",
         "code": "forbidden", "message": "shared indicators are manager-only"})
    _invalid(_v(_GP, "error", registry), {"channel": "gp", "schema": "afbws.gp.error.v2", "request_id": "r", "code": "conflict", "message": "x", "item": _GP_ITEM})


def test_gp_v2_root_dispatch(registry):
    root = _root(_GP, registry)
    root.validate({"channel": "gp", "schema": "afbws.gp.delete.v2", "request_id": "r", "instrument_keys": [_KEY]})
    for old in ("afbws.gp.set.request.v2", "afbws.gp.sync.push.v2", "afbws.gp.indicator.sync.push.v2", "afbws.gp.get.request.v2"):
        _invalid(root, {"channel": "gp", "schema": old, "request_id": "r"})


def _alarm_def(registry, name):
    from jsonschema import Draft202012Validator

    schema_id = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/alarm.channel.v2.json"
    return Draft202012Validator({"$ref": f"{schema_id}#/$defs/{name}"}, registry=registry)


def test_alarm_delete_push_without_request_id(registry):
    from jsonschema import ValidationError
    import pytest

    v = _alarm_def(registry, "delete")
    v.validate({"channel": "alarm", "schema": "afbws.alarm.delete.v2", "ids": ["a1"]})  # push
    v.validate({"channel": "alarm", "schema": "afbws.alarm.delete.v2", "request_id": "r1", "instrument_keys": ["MISX:RFUD:SRU6"]})
    for bad in (
        {"channel": "alarm", "schema": "afbws.alarm.delete.v2"},                                   # пустой push
        {"channel": "alarm", "schema": "afbws.alarm.delete.v2", "ids": []},                        # пустой ids в push
        {"channel": "alarm", "schema": "afbws.alarm.delete.v2", "instrument_keys": ["MISX:RFUD:SRU6"]},  # ключи — только в запросе
        {"channel": "alarm", "schema": "afbws.alarm.delete.v2", "ids": ["a1"], "rejected": []},    # rejected — только в ответе
        {"channel": "alarm", "schema": "afbws.alarm.delete.v2", "request_id": "r1"},               # запрос без ids/ключей
    ):
        with pytest.raises(ValidationError):
            v.validate(bad)


def test_alarm_set_push_without_request_id(registry):
    from jsonschema import ValidationError
    import pytest

    v = _alarm_def(registry, "set")
    from conftest import EXAMPLES
    import json as _json

    example = sorted((EXAMPLES / "alarms_v2").glob("*.json"))[0]
    alarm = _json.loads(example.read_text())
    v.validate({"channel": "alarm", "schema": "afbws.alarm.set.v2", "items": [alarm]})  # push
    for bad in (
        {"channel": "alarm", "schema": "afbws.alarm.set.v2", "items": []},                          # пустой push
        {"channel": "alarm", "schema": "afbws.alarm.set.v2", "items": [alarm], "rejected": []},    # rejected без request_id
    ):
        with pytest.raises(ValidationError):
            v.validate(bad)


# ----------------------------------------------------------------- gp presets
_PRESET = {"id": "preset-1", "scope": "personal", "name": "Мой",
           "panes": {"price": [{"dataset": "dataset-0a1b-2c3d-4e5f", "style": {"upColor": "#00c853ff"}}],
                     "upper": [], "lower": []}}
_DATASET = {"id": "dataset-1111-2222-3333", "scope": "shared", "name": "WillCo", "field": "positions.willco@window(180)",
            "unit": "percent", "style": {"seriesType": "Line", "color": "#ab47bcff", "lineWidth": 2, "lineStyle": 0}}


def test_gp_v2_dataset_commands(registry):
    base = {"channel": "gp", "request_id": "r"}
    lst = _v(_GP, "datasetList", registry)
    lst.validate({**base, "schema": "afbws.gp.dataset.list.v2"})
    lst.validate({**base, "schema": "afbws.gp.dataset.list.v2", "items": [_DATASET]})
    _invalid(lst, {**base, "schema": "afbws.gp.dataset.list.v2", "items": [dict(_DATASET, id="ds-1")]})
    st = _v(_GP, "datasetSet", registry)
    st.validate({**base, "schema": "afbws.gp.dataset.set.v2", "items": [_DATASET]})
    st.validate({**base, "schema": "afbws.gp.dataset.set.v2", "items": [],
                 "rejected": [{"id": _DATASET["id"], "code": "forbidden", "message": "staff only"}]})
    _invalid(st, {**base, "schema": "afbws.gp.dataset.set.v2", "item": _DATASET})
    _invalid(st, {**base, "schema": "afbws.gp.dataset.set.v2", "items": [dict(_DATASET, name="")]})
    dl = _v(_GP, "datasetDelete", registry)
    dl.validate({**base, "schema": "afbws.gp.dataset.delete.v2", "ids": [_DATASET["id"]]})
    dl.validate({**base, "schema": "afbws.gp.dataset.delete.v2", "ids": [], "rejected": [{"id": "x", "code": "not_found"}]})
    _invalid(dl, {**base, "schema": "afbws.gp.dataset.delete.v2", "id": _DATASET["id"]})


def test_gp_v2_dataset_shared_push(registry):
    """Shared-dataset deltas reuse dataset.set / dataset.delete without request_id; drafts are never pushed."""
    st = _v(_GP, "datasetSet", registry)
    st.validate({"channel": "gp", "schema": "afbws.gp.dataset.set.v2", "items": [_DATASET]})
    _invalid(st, {"channel": "gp", "schema": "afbws.gp.dataset.set.v2", "items": []})
    _invalid(st, {"channel": "gp", "schema": "afbws.gp.dataset.set.v2", "items": [_DATASET],
                  "rejected": [{"id": "x", "code": "forbidden"}]})
    dl = _v(_GP, "datasetDelete", registry)
    dl.validate({"channel": "gp", "schema": "afbws.gp.dataset.delete.v2", "ids": [_DATASET["id"]]})
    _invalid(dl, {"channel": "gp", "schema": "afbws.gp.dataset.delete.v2", "ids": []})


def test_gp_v2_preset_commands(registry):
    base = {"channel": "gp", "request_id": "r"}
    lst = _v(_GP, "presetList", registry)
    lst.validate({**base, "schema": "afbws.gp.preset.list.v2"})
    lst.validate({**base, "schema": "afbws.gp.preset.list.v2", "items": [_PRESET]})
    _invalid(lst, {**base, "schema": "afbws.gp.preset.list.v2", "items": [dict(_PRESET, name="")]})
    st = _v(_GP, "presetSet", registry)
    st.validate({**base, "schema": "afbws.gp.preset.set.v2", "items": [_PRESET]})
    st.validate({**base, "schema": "afbws.gp.preset.set.v2", "items": [],
                 "rejected": [{"id": "preset-1", "code": "validation_error", "message": "unit"}]})
    _invalid(st, {**base, "schema": "afbws.gp.preset.set.v2", "item": _PRESET})
    _invalid(st, {**base, "schema": "afbws.gp.preset.set.v2", "items": [dict(_PRESET, panes={"price": []})]})
    # old shape (plain indicator ids) is gone
    _invalid(st, {**base, "schema": "afbws.gp.preset.set.v2",
                  "items": [dict(_PRESET, panes={"price": ["ind-1"], "upper": [], "lower": []})]})
    dl = _v(_GP, "presetDelete", registry)
    dl.validate({**base, "schema": "afbws.gp.preset.delete.v2", "ids": ["preset-1"]})
    dl.validate({**base, "schema": "afbws.gp.preset.delete.v2", "ids": [], "rejected": [{"id": "x", "code": "forbidden"}]})
    _invalid(dl, {**base, "schema": "afbws.gp.preset.delete.v2", "id": "preset-1"})


def test_gp_v2_preset_shared_push(registry):
    st = _v(_GP, "presetSet", registry)
    st.validate({"channel": "gp", "schema": "afbws.gp.preset.set.v2", "items": [dict(_PRESET, scope="shared")]})
    _invalid(st, {"channel": "gp", "schema": "afbws.gp.preset.set.v2", "items": []})
    _invalid(st, {"channel": "gp", "schema": "afbws.gp.preset.set.v2", "items": [_PRESET],
                  "rejected": [{"id": "p", "code": "forbidden"}]})  # rejected needs request_id
    dl = _v(_GP, "presetDelete", registry)
    dl.validate({"channel": "gp", "schema": "afbws.gp.preset.delete.v2", "ids": ["preset-1"]})
    _invalid(dl, {"channel": "gp", "schema": "afbws.gp.preset.delete.v2", "ids": []})


def test_gp_v2_root_dispatch_presets(registry):
    root = _root(_GP, registry)
    root.validate({"channel": "gp", "schema": "afbws.gp.preset.list.v2", "request_id": "r"})
    root.validate({"channel": "gp", "schema": "afbws.gp.preset.delete.v2", "ids": ["p"]})


def test_gp_v2_examples_validate(registry):
    import json as _json

    from conftest import EXAMPLES as _EX

    root = _root(_GP, registry)
    from jsonschema import Draft202012Validator

    ind = Draft202012Validator({"$ref": "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/gp.v2.json#/$defs/indicator"},
                               registry=registry)
    files = sorted((_EX / "gp_v2").glob("*.json"))
    assert len(files) >= 10
    for path in files:
        doc = _json.loads(path.read_text(encoding="utf-8"))
        (root if "schema" in doc and doc.get("channel") == "gp" else ind).validate(doc)
