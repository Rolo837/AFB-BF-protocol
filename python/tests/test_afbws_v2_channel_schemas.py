"""afbws/alarm.channel.v2.json and afbws/gp.channel.v2.json (AFB backend<->AFB
frontend only)."""
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
    "start": {"time": 1721000000, "price": 1.0}, "stop": {"time": 1721000600, "price": 2.0},
}
_IND = {
    "id": "ind-1", "type": "kama", "enabled": True, "scope": "shared",
    "settings": {"enabled": True, "color": "#fff", "lineWidth": 2, "lineStyle": "Dots",
                 "erPeriod": 10, "fastPeriod": 2, "slowPeriod": 30},
}


def _v(channel_id, def_name, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{channel_id}#/$defs/{def_name}"}, registry=registry)


def test_alarm_v2_set_get_list(registry):
    _v(_ALARM, "setRequest", registry).validate(
        {"channel": "alarm", "schema": "afbws.alarm.set.request.v2", "request_id": "r", "item": _ALARM_ITEM})
    _v(_ALARM, "listRequest", registry).validate(
        {"channel": "alarm", "schema": "afbws.alarm.list.request.v2", "request_id": "r", "instrument_key": "MISX:TQBR:SBER"})
    _v(_ALARM, "listResponse", registry).validate(
        {"channel": "alarm", "schema": "afbws.alarm.list.response.v2", "request_id": "r", "items": [_ALARM_ITEM]})


def test_alarm_v2_rejects_v1_item_and_ticker_filter(registry):
    from jsonschema import ValidationError

    v1_item = json.loads((EXAMPLES / "alarms" / "alarm.touch.json").read_text())
    with pytest.raises(ValidationError):
        _v(_ALARM, "setRequest", registry).validate(
            {"channel": "alarm", "schema": "afbws.alarm.set.request.v2", "request_id": "r", "item": v1_item})
    with pytest.raises(ValidationError):
        _v(_ALARM, "listRequest", registry).validate(
            {"channel": "alarm", "schema": "afbws.alarm.list.request.v2", "request_id": "r", "ticker": "SBER"})


def test_alarm_v2_triggered_push_and_ack(registry):
    _v(_ALARM, "triggeredPush", registry).validate({
        "channel": "alarm", "schema": "afbws.alarm.triggered.push.v2",
        "events": [{"schema": "afb.alarm.trigger.v2", "alarm_id": "a", "triggered_at": "t", "alarm": _ALARM_ITEM}]})
    _v(_ALARM, "ackRequest", registry).validate({
        "channel": "alarm", "schema": "afbws.alarm.ack.request.v2", "request_id": "r",
        "events": [{"schema": "afb.alarm.trigger_ack.v2", "alarm_id": "a", "triggered_at": "t"}]})


def test_gp_v2_primitive_commands(registry):
    _v(_GP, "setRequest", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.set.request.v2", "request_id": "r", "item": _GP_ITEM})
    _v(_GP, "listRequest", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.list.request.v2", "request_id": "r"})
    _v(_GP, "syncPush", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.sync.push.v2", "items": [_GP_ITEM]})


def test_gp_v2_indicator_commands(registry):
    _v(_GP, "indicatorListRequest", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.indicator.list.request.v2", "request_id": "r"})
    _v(_GP, "indicatorListResponse", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.indicator.list.response.v2", "request_id": "r", "items": [_IND]})
    _v(_GP, "indicatorSetRequest", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.indicator.set.request.v2", "request_id": "r", "item": _IND})
    _v(_GP, "indicatorSetResponse", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.indicator.set.response.v2", "request_id": "r", "item": _IND})
    _v(_GP, "indicatorDeleteRequest", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.indicator.delete.request.v2", "request_id": "r", "id": "ind-1"})
    _v(_GP, "indicatorDeleteResponse", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.indicator.delete.response.v2", "request_id": "r", "id": "ind-1"})


def test_gp_v2_indicator_sync_push(registry):
    from jsonschema import ValidationError

    v = _v(_GP, "indicatorSyncPush", registry)
    v.validate({"channel": "gp", "schema": "afbws.gp.indicator.sync.push.v2", "items": [_IND]})
    v.validate({"channel": "gp", "schema": "afbws.gp.indicator.sync.push.v2", "removed_ids": ["x"]})
    with pytest.raises(ValidationError):
        v.validate({"channel": "gp", "schema": "afbws.gp.indicator.sync.push.v2"})


def test_gp_v2_error_response_forbidden(registry):
    _v(_GP, "errorResponse", registry).validate(
        {"channel": "gp", "schema": "afbws.gp.error.response.v2", "request_id": "r",
         "code": "forbidden", "message": "shared indicators are manager-only"})


def test_gp_v2_rejects_v1_item(registry):
    from jsonschema import ValidationError

    v1 = dict(_GP_ITEM, schema="afb.gp.v1")
    with pytest.raises(ValidationError):
        _v(_GP, "setRequest", registry).validate(
            {"channel": "gp", "schema": "afbws.gp.set.request.v2", "request_id": "r", "item": v1})
