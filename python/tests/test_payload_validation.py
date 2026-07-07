"""afb_bf_protocol.payload_validation — the packaged-schema validators AFB uses
at runtime for deals and trade-plan templates."""
from __future__ import annotations

import copy
import json

import pytest

from afb_bf_protocol.payload_validation import (
    PayloadValidationError,
    resolve_tradeplan_schema,
    validate_alarm,
    validate_deal,
    validate_notification,
    validate_tradeplan,
)
from conftest import EXAMPLES


def _fixture_deal(stem: str) -> dict:
    env = json.loads((EXAMPLES / f"{stem}.json").read_text())
    return env["payload"]["deal"]


def test_validate_deal_accepts_v1_fixture():
    assert validate_deal(_fixture_deal("deal.publish")) == "afb.deal.v1"


def test_validate_deal_accepts_v2_fixture():
    assert validate_deal(_fixture_deal("deal.publish__v2")) == "afb.deal.v2"


def test_validate_deal_rejects_v1_with_quote_left():
    deal = copy.deepcopy(_fixture_deal("deal.publish"))
    deal["entry"]["condition"]["left"] = {"source": "quote", "field": "bid"}
    with pytest.raises(PayloadValidationError):
        validate_deal(deal)


def test_validate_deal_rejects_v2_price_left_with_indicator_right():
    deal = copy.deepcopy(_fixture_deal("deal.publish__v2"))
    deal["entry"][0]["condition"]["right"] = {"source": "indicator", "type": "wma"}
    with pytest.raises(PayloadValidationError):
        validate_deal(deal)


def test_validate_deal_rejects_unknown_schema():
    with pytest.raises(PayloadValidationError):
        validate_deal({"schema": "afb.deal.v3"})


def test_validate_deal_v1_accepts_direction_only_no_entry_side():
    """Transitional: afb.deal.v1 accepts a deal-level `direction` (long/short)
    in place of the legacy `entry.side` (buy/sell)."""
    deal = copy.deepcopy(_fixture_deal("deal.publish"))
    del deal["entry"]["side"]
    deal["direction"] = "long"
    assert validate_deal(deal) == "afb.deal.v1"


def test_validate_deal_v1_rejects_neither_side_nor_direction():
    deal = copy.deepcopy(_fixture_deal("deal.publish"))
    del deal["entry"]["side"]
    with pytest.raises(PayloadValidationError):
        validate_deal(deal)


def test_resolve_tradeplan_schema_defaults_to_v1_without_schema_field():
    assert resolve_tradeplan_schema({"id": "x"}) == "afb.tradeplan.v1"


def test_resolve_tradeplan_schema_rejects_unknown():
    with pytest.raises(PayloadValidationError):
        resolve_tradeplan_schema({"schema": "afb.tradeplan.v3"})


def test_validate_tradeplan_v1_example():
    data = json.loads((EXAMPLES / "tradeplans" / "tradeplan.v1.json").read_text())
    assert validate_tradeplan(data) == "afb.tradeplan.v1"


def test_validate_tradeplan_legacy_no_schema_field():
    data = json.loads((EXAMPLES / "tradeplans" / "tradeplan.v1.no-schema-field.json").read_text())
    assert "schema" not in data
    assert validate_tradeplan(data) == "afb.tradeplan.v1"


def test_validate_tradeplan_v2_example():
    data = json.loads((EXAMPLES / "tradeplans" / "tradeplan.v2.json").read_text())
    assert validate_tradeplan(data) == "afb.tradeplan.v2"


def test_validate_tradeplan_v2_rejects_empty_entries():
    plan = json.loads((EXAMPLES / "tradeplans" / "tradeplan.v2.json").read_text())
    plan["entries"] = []
    with pytest.raises(PayloadValidationError):
        validate_tradeplan(plan)


def test_validate_alarm_accepts_touch_example():
    data = json.loads((EXAMPLES / "alarms" / "alarm.touch.json").read_text())
    assert validate_alarm(data) == "afb.alarm.v1"


def test_validate_alarm_accepts_breakout_example():
    data = json.loads((EXAMPLES / "alarms" / "alarm.breakout.json").read_text())
    assert validate_alarm(data) == "afb.alarm.v1"


def test_validate_alarm_rejects_unknown_schema():
    with pytest.raises(PayloadValidationError):
        validate_alarm({"schema": "afb.alarm.v2"})


def test_validate_alarm_rejects_candle_op_without_timeframe():
    data = json.loads((EXAMPLES / "alarms" / "alarm.breakout.json").read_text())
    del data["condition"]["timeframe"]
    with pytest.raises(PayloadValidationError):
        validate_alarm(data)


def test_validate_notification_accepts_touch_example():
    data = json.loads((EXAMPLES / "notifications" / "alarm_triggered.touch.json").read_text())
    assert validate_notification(data) == "afb.notification.alarm_triggered.v1"


def test_validate_notification_rejects_missing_display():
    data = json.loads((EXAMPLES / "notifications" / "alarm_triggered.touch.json").read_text())
    del data["display"]
    with pytest.raises(PayloadValidationError):
        validate_notification(data)
