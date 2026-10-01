"""afb.gp.v2 — instrument_key instead of ticker, kinds trendline/fibonacci,
and the chart-indicator $defs."""
from __future__ import annotations

import pytest

GP_V2_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/gp.v2.json"
_POINT = {"time": 1721000000, "price": 123.45}
_KEY = "MISX:TQBR:SBER"


def _item(**overrides):
    item = {"schema": "afb.gp.v2", "id": "gp-1", "instrument_key": _KEY, "kind": "line", "start": dict(_POINT)}
    item.update(overrides)
    return item


def _validator(registry, fragment=""):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": GP_V2_ID + fragment}, registry=registry)


@pytest.mark.parametrize("kind", ["line", "line_enter", "line_sl", "line_tp", "note"])
def test_single_anchor_kinds_valid(kind, registry):
    _validator(registry).validate(_item(kind=kind))


@pytest.mark.parametrize("kind", ["zone", "ruler", "trendline", "fibonacci"])
def test_two_anchor_kinds_require_stop(kind, registry):
    from jsonschema import ValidationError

    _validator(registry).validate(_item(kind=kind, stop=dict(_POINT)))
    with pytest.raises(ValidationError):
        _validator(registry).validate(_item(kind=kind))


@pytest.mark.parametrize("kind", ["trendline", "fibonacci"])
def test_new_kinds_reject_text(kind, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_item(kind=kind, stop=dict(_POINT), text="x"))


def test_single_anchor_rejects_stop(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_item(stop=dict(_POINT)))


def test_ticker_rejected_and_instrument_key_required(registry):
    from jsonschema import ValidationError

    bad = _item()
    del bad["instrument_key"]
    bad["ticker"] = "SBER"
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_v1_schema_const_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_item(schema="afb.gp.v1"))


def _indicator(**overrides):
    ind = {
        "id": "ind-1", "type": "wma", "enabled": True, "scope": "personal",
        "settings": {"enabled": False, "color": "#2962FF", "lineWidth": 2, "lineStyle": "Solid", "period": 5},
    }
    ind.update(overrides)
    return ind


@pytest.mark.parametrize("type_", ["wma", "kama", "psar", "cot"])
def test_indicator_types_valid(type_, registry):
    _validator(registry, "#/$defs/indicator").validate(_indicator(type=type_))


def test_indicator_rejects_bad_scope_and_type(registry):
    from jsonschema import ValidationError

    for bad in (_indicator(scope="global"), _indicator(type="rsi")):
        with pytest.raises(ValidationError):
            _validator(registry, "#/$defs/indicator").validate(bad)
