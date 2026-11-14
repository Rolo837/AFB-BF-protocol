"""afb.alarm.v2 — AFB-side alarm schema (the only alarm entity; afb.alarm.v1
was removed). Like trade-plan templates, alarms never cross the AFB<->BF wire,
so examples/alarms_v2/*.json are plain JSON, not signed envelopes."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from conftest import EXAMPLES

ALARM_EXAMPLES = sorted((EXAMPLES / "alarms_v2").glob("*.json"))
assert ALARM_EXAMPLES, "no alarm examples found"

ALARM_V2_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/alarm.v2.json"


def _validator(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": ALARM_V2_ID}, registry=registry)


def _load(name):
    return json.loads((EXAMPLES / "alarms_v2" / name).read_text())


@pytest.mark.parametrize("path", ALARM_EXAMPLES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    _validator(registry).validate(json.loads(path.read_text()))


def test_rejects_missing_required_fields(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate({"schema": "afb.alarm.v2"})


def test_requires_instrument_key(registry):
    from jsonschema import ValidationError

    data = _load("alarm.touch.json")
    bad = copy.deepcopy(data)
    del bad["instrument_key"]
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_rejects_unknown_schema(registry):
    from jsonschema import ValidationError

    for schema in ("afb.alarm.v1", "afb.alarm.v3"):
        plan = _load("alarm.touch.json")
        plan["schema"] = schema
        with pytest.raises(ValidationError):
            _validator(registry).validate(plan)


def test_rejects_legacy_break_up_operator(registry):
    """break_up/break_down are the legacy alarm operator names (see the
    condition_type/trigger_type mapping table in docs/PROTOCOL.md); the wire
    vocabulary is breakout/breakdown."""
    from jsonschema import ValidationError

    plan = _load("alarm.breakout.json")
    plan["condition"]["op"] = "break_up"
    with pytest.raises(ValidationError):
        _validator(registry).validate(plan)


def test_candle_op_without_timeframe_is_rejected(registry):
    from jsonschema import ValidationError

    plan = _load("alarm.breakout.json")
    del plan["condition"]["timeframe"]
    with pytest.raises(ValidationError):
        _validator(registry).validate(plan)


def test_indicator_condition_does_not_require_type_or_params(registry):
    """Unlike deal.v2/tradeplan.v2's indicatorExpr, an alarm's indicator leg
    only needs source+id — AFB resolves type/params from user settings."""
    plan = _load("alarm.indicator_crossing.json")
    assert "type" not in plan["condition"]["left"]
    _validator(registry).validate(plan)  # does not raise
