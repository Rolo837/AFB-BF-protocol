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

    for bad in (_indicator(scope="global"), _indicator(type="RSI"), _indicator(type="1x"), _indicator(type="")):
        with pytest.raises(ValidationError):
            _validator(registry, "#/$defs/indicator").validate(bad)


def test_indicator_open_type_and_extra_settings(registry):
    """type is an open string; settings take extra number/string/boolean keys."""
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/indicator")
    ind = _indicator(type="rsi_smooth")
    ind["settings"] = dict(ind["settings"], smoothing="ema", upperLevel=70, showFill=True)
    v.validate(ind)
    bad = _indicator()
    bad["settings"] = dict(bad["settings"], levels=[30, 70])  # non-scalar extra value
    with pytest.raises(ValidationError):
        v.validate(bad)
    bad = _indicator()
    del bad["settings"]["color"]  # required keys stay required
    with pytest.raises(ValidationError):
        v.validate(bad)


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


# ----------------------------------------------------- indicator inputs / preset
_IND_SETTINGS = {"color": "#2962FF", "lineWidth": 2, "lineStyle": "Solid"}


@pytest.mark.parametrize("ref", [
    "candles.close", "candles.open", "candles.high", "candles.low", "candles.volume",
    "positions.yur_net", "trades.val_b@median(30)", "obstats.vol_b@median(1)", "hhi.volume",
])
def test_indicator_inputs_valid(ref, registry):
    v = _validator(registry, "#/$defs/indicator")
    v.validate(_indicator(type="sma", inputs={"value": ref}))
    v.validate(_indicator(type="cot", inputs={"net": "positions.yur_net", "oi": "positions.openinterest"}))


@pytest.mark.parametrize("ref", [
    "candles.", "Candles.close", "close", "positions.yur_net@median(0)",
    "positions.yur_net@median(1000)", "positions.yur_net@mean(3)", "trades.val_b@median(3)@median(3)",
    "positions.", ".yur_net", "", 5,
])
def test_indicator_inputs_bad_ref(ref, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry, "#/$defs/indicator").validate(_indicator(type="sma", inputs={"value": ref}))


def test_indicator_inputs_bad_slot_name_and_shape(registry):
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/indicator")
    for bad in ({"Value": "candles.close"}, {"1v": "candles.close"}, {"": "candles.close"}):
        with pytest.raises(ValidationError):
            v.validate(_indicator(inputs=bad))
    with pytest.raises(ValidationError):
        v.validate(_indicator(inputs=["candles.close"]))


def test_indicator_without_inputs_still_valid(registry):
    v = _validator(registry, "#/$defs/indicator")
    ind = _indicator()
    assert "inputs" not in ind
    v.validate(ind)
    v.validate(_indicator(inputs={}))
    # type=field schema-wise valid even without inputs.value (server enforces it)
    v.validate(_indicator(type="field", inputs={"value": "positions.yur_long"}))
    v.validate(_indicator(type="field"))


@pytest.mark.parametrize("st", ["Line", "Histogram", "Area", "Baseline"])
def test_indicator_series_type(st, registry):
    v = _validator(registry, "#/$defs/indicator")
    v.validate(_indicator(settings={**_IND_SETTINGS, "seriesType": st}))


def test_indicator_series_type_invalid(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry, "#/$defs/indicator").validate(
            _indicator(settings={**_IND_SETTINGS, "seriesType": "Candles"}))


def _preset(**overrides):
    p = {"id": "preset-1", "scope": "personal", "name": "Мой",
         "panes": {"price": ["a"], "upper": ["b"], "lower": []}}
    p.update(overrides)
    return p


def test_preset_valid(registry):
    v = _validator(registry, "#/$defs/preset")
    v.validate(_preset())
    v.validate(_preset(scope="shared", panes={"price": [], "upper": [], "lower": []}))
    v.validate(_preset(name="x" * 64, panes={"price": [f"i{n}" for n in range(16)], "upper": [], "lower": []}))


@pytest.mark.parametrize("patch", [
    {"panes": {"price": [], "upper": []}},                                  # missing pane
    {"panes": {"price": [], "upper": [], "lower": [], "extra": []}},         # unknown pane
    {"panes": {"price": [f"i{n}" for n in range(17)], "upper": [], "lower": []}},  # > 16
    {"panes": {"price": ["a", "a"], "upper": [], "lower": []}},             # not unique in pane
    {"panes": {"price": [""], "upper": [], "lower": []}},                   # empty id
    {"name": ""},
    {"name": "x" * 65},
    {"scope": "global"},
    {"id": ""},
    {"unknown": 1},
])
def test_preset_invalid(patch, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry, "#/$defs/preset").validate(_preset(**patch))


def test_preset_required_keys(registry):
    from jsonschema import ValidationError

    for key in ("id", "scope", "name", "panes"):
        bad = _preset()
        del bad[key]
        with pytest.raises(ValidationError):
            _validator(registry, "#/$defs/preset").validate(bad)
