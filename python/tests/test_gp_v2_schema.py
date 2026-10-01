"""afb.gp.v2 — instrument_key instead of ticker, kinds trendline/fibonacci,
primitive parameters in the strictly kind-typed `settings` dictionary,
and the chart-indicator $defs."""
from __future__ import annotations

import pytest

GP_V2_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/gp.v2.json"
_POINT = {"time": 1721000000, "price": 123.45}
_KEY = "MISX:TQBR:SBER"


def _item(kind="line", **settings):
    """Valid item for `kind`; `settings` overrides the default settings dict."""
    default = {"start": dict(_POINT)}
    if kind in ("zone", "ruler", "trendline", "fibonacci"):
        default["stop"] = dict(_POINT)
    return {
        "schema": "afb.gp.v2", "id": "gp-1", "instrument_key": _KEY, "kind": kind,
        "settings": settings or default,
    }


def _validator(registry, fragment=""):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": GP_V2_ID + fragment}, registry=registry)


@pytest.mark.parametrize("kind", ["line", "line_enter", "line_sl", "line_tp", "note"])
def test_single_anchor_kinds_valid(kind, registry):
    _validator(registry).validate(_item(kind))


@pytest.mark.parametrize("kind", ["zone", "ruler", "trendline", "fibonacci"])
def test_two_anchor_kinds_require_stop(kind, registry):
    from jsonschema import ValidationError

    _validator(registry).validate(_item(kind))
    with pytest.raises(ValidationError):
        _validator(registry).validate(_item(kind, start=dict(_POINT)))


@pytest.mark.parametrize("kind", ["trendline", "fibonacci", "zone", "ruler", "line", "line_sl"])
def test_only_note_accepts_text(kind, registry):
    from jsonschema import ValidationError

    settings = {"start": dict(_POINT), "text": "x"}
    if kind in ("zone", "ruler", "trendline", "fibonacci"):
        settings["stop"] = dict(_POINT)
    with pytest.raises(ValidationError):
        _validator(registry).validate(_item(kind, **settings))


def test_note_text_optional_and_bounded(registry):
    from jsonschema import ValidationError

    _validator(registry).validate(_item("note", start=dict(_POINT), text="hello"))
    with pytest.raises(ValidationError):
        _validator(registry).validate(_item("note", start=dict(_POINT), text="x" * 161))


def test_single_anchor_rejects_stop(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_item("line", start=dict(_POINT), stop=dict(_POINT)))


def test_settings_required_and_root_params_rejected(registry):
    from jsonschema import ValidationError

    no_settings = _item()
    del no_settings["settings"]
    flat = _item()
    del flat["settings"]
    flat["start"] = dict(_POINT)  # v1-style flat parameters are not valid in v2
    leaked = _item()
    leaked["stop"] = dict(_POINT)  # root-level parameter next to settings
    for bad in (no_settings, flat, leaked):
        with pytest.raises(ValidationError):
            _validator(registry).validate(bad)


def test_settings_rejects_unknown_keys(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_item("line", start=dict(_POINT), color="#fff"))


def test_tradeplan_id_stays_on_root(registry):
    item = _item("line_sl")
    item["tradeplan_id"] = "tp-1"
    _validator(registry).validate(item)


def test_ticker_rejected_and_instrument_key_required(registry):
    from jsonschema import ValidationError

    bad = _item()
    del bad["instrument_key"]
    bad["ticker"] = "SBER"
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_v1_schema_const_rejected(registry):
    from jsonschema import ValidationError

    bad = _item()
    bad["schema"] = "afb.gp.v1"
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def _indicator(**overrides):
    ind = {
        "id": "ind-1", "type": "wma", "scope": "personal",
        "settings": {"color": "#2962FF", "lineWidth": 2, "lineStyle": "Solid", "period": 5},
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


def test_indicator_rejects_enabled_flag(registry):
    """`enabled` is a per-device view setting (localStorage), not protocol."""
    import pytest
    from jsonschema import ValidationError

    bad_outer = dict(_indicator(), enabled=True)
    bad_inner = _indicator()
    bad_inner["settings"] = dict(bad_inner["settings"], enabled=True)
    for bad in (bad_outer, bad_inner):
        with pytest.raises(ValidationError):
            _validator(registry, "#/$defs/indicator").validate(bad)


def test_primitive_styles_valid_and_strict(registry):
    import pytest
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/primitiveStyles")
    v.validate({"line": {"color": "#112233", "lineWidth": 3, "lineStyle": 0}, "note": {"color": "#AABBCC", "lineWidth": 2, "lineStyle": 2}})
    v.validate({})
    for bad in (
        {"rsi": {"color": "#112233", "lineWidth": 3, "lineStyle": 0}},
        {"line": {"color": "red", "lineWidth": 3, "lineStyle": 0}},
        {"line": {"color": "#112233", "lineWidth": 7, "lineStyle": 0}},
        {"line": {"color": "#112233", "lineWidth": 3, "lineStyle": 9}},
        {"line": {"color": "#112233", "lineWidth": 3}},
    ):
        with pytest.raises(ValidationError):
            v.validate(bad)
