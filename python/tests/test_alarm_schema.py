"""afb.alarm.v1 — AFB-side alarm schema. Like trade-plan templates, alarms
never cross the AFB<->BF wire, so examples/alarms/*.json are plain JSON, not
signed envelopes (see test_tradeplan_schema.py for the same pattern)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES

ALARM_EXAMPLES = sorted((EXAMPLES / "alarms").glob("*.json"))
assert ALARM_EXAMPLES, "no alarm examples found"

ALARM_V1_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/alarm.v1.json"


def _validator(registry):
    from jsonschema import Draft202012Validator

    resolved = registry[ALARM_V1_ID]
    return Draft202012Validator(resolved.contents, registry=registry)


@pytest.mark.parametrize("path", ALARM_EXAMPLES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    data = json.loads(path.read_text())
    _validator(registry).validate(data)


def test_rejects_missing_required_fields(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate({"schema": "afb.alarm.v1"})


def test_rejects_unknown_schema(registry):
    from jsonschema import ValidationError

    plan = json.loads((EXAMPLES / "alarms" / "alarm.touch.json").read_text())
    plan["schema"] = "afb.alarm.v2"
    with pytest.raises(ValidationError):
        _validator(registry).validate(plan)


def test_rejects_legacy_break_up_operator(registry):
    """break_up/break_down are the legacy alarm operator names (see the
    condition_type/trigger_type mapping table in docs/PROTOCOL.md); the wire
    vocabulary is breakout/breakdown."""
    from jsonschema import ValidationError

    plan = json.loads((EXAMPLES / "alarms" / "alarm.breakout.json").read_text())
    plan["condition"]["op"] = "break_up"
    with pytest.raises(ValidationError):
        _validator(registry).validate(plan)


def test_candle_op_without_timeframe_is_rejected(registry):
    from jsonschema import ValidationError

    plan = json.loads((EXAMPLES / "alarms" / "alarm.breakout.json").read_text())
    del plan["condition"]["timeframe"]
    with pytest.raises(ValidationError):
        _validator(registry).validate(plan)


def test_indicator_condition_does_not_require_type_or_params(registry):
    """Unlike deal.v2/tradeplan.v2's indicatorExpr, an alarm's indicator leg
    only needs source+id — AFB resolves type/params from user settings."""
    plan = json.loads((EXAMPLES / "alarms" / "alarm.indicator_crossing.json").read_text())
    assert "type" not in plan["condition"]["left"]
    _validator(registry).validate(plan)  # does not raise
