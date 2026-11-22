"""afb.gp.v2 — instrument_key instead of ticker, kinds trendline/fibonacci,
primitive parameters in the strictly kind-typed `settings` dictionary,
the chart-indicator, dataset and preset $defs."""
from __future__ import annotations

import json
from pathlib import Path

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
        "settings": {"period": 5}, "style": dict(_LINE_STYLE),
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
    del bad["style"]  # style is required
    with pytest.raises(ValidationError):
        v.validate(bad)
    for key, val in (("color", "#112233ff"), ("lineWidth", 2), ("lineStyle", 0)):
        bad = _indicator()
        bad["settings"] = dict(bad["settings"], **{key: val})  # look moved to `style`
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
    v.validate({"line": {"color": "#112233ff", "lineWidth": 3, "lineStyle": 0}, "note": {"color": "#aabbcc80", "lineWidth": 2, "lineStyle": 2}})
    v.validate({})
    for bad in (
        {"rsi": {"color": "#112233ff", "lineWidth": 3, "lineStyle": 0}},
        {"line": {"color": "red", "lineWidth": 3, "lineStyle": 0}},
        {"line": {"color": "#112233", "lineWidth": 3, "lineStyle": 0}},    # no alpha
        {"line": {"color": "#112233FF", "lineWidth": 3, "lineStyle": 0}},  # upper case
        {"line": {"color": "#112233ff", "lineWidth": 7, "lineStyle": 0}},
        {"line": {"color": "#112233ff", "lineWidth": 3, "lineStyle": 9}},
        {"line": {"color": "#112233ff", "lineWidth": 3}},
    ):
        with pytest.raises(ValidationError):
            v.validate(bad)


# ----------------------------------------------------- datasets / presets
_LINE_STYLE = {"seriesType": "Line", "color": "#ab47bcff", "lineWidth": 2, "lineStyle": 0}
_CANDLE_STYLE = {"chartType": "candles", "upColor": "#26a69aff", "downColor": "#ef5350ff",
                 "volumeUpColor": "#26a69a80", "volumeDownColor": "#ef535080"}
_DS_A = "dataset-0a1b-2c3d-4e5f"
_DS_B = "dataset-1111-2222-3333"


def test_indicator_inputs_and_series_type_removed(registry):
    """Stage 8 rolled back `inputs` / `settings.seriesType` of the indicator (datasets replace them)."""
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/indicator")
    v.validate(_indicator())
    with pytest.raises(ValidationError):
        v.validate(_indicator(inputs={"value": "candles.close"}))
    with pytest.raises(ValidationError):
        v.validate(_indicator(type="sma", inputs={}))
    schema = json.loads((Path(__file__).parents[2] / "spec" / "schemas" / "gp.v2.json").read_text(encoding="utf-8"))
    assert "seriesType" not in schema["$defs"]["indicatorSettings"]["properties"]
    assert "fieldRef" not in schema["$defs"]
    assert "inputs" not in schema["$defs"]["indicator"]["properties"]


def _dataset(**overrides):
    d = {"id": _DS_B, "scope": "shared", "name": "WillCo, 180 баров", "field": "positions.willco@window(180)",
         "unit": "percent", "style": dict(_LINE_STYLE)}
    d.update(overrides)
    return d


@pytest.mark.parametrize("ds", [
    {},
    {"scope": "personal"},
    {"unit": None},  # removed below: unit is optional
    {"id": "dataset-0a1b-2c3d-4e5f", "field": "candles", "unit": "price", "style": _CANDLE_STYLE},
    {"field": "trades.val_b", "unit": "rub", "style": {**_LINE_STYLE, "seriesType": "Histogram", "color": "#26a69a99"}},
    {"field": "trades.val_b@median(30)", "style": {**_LINE_STYLE, "color": "#11223380", "lineWidth": 4, "lineStyle": 4}},
    {"name": "x" * 64},
])
def test_dataset_valid(ds, registry):
    d = _dataset(**ds)
    if d.get("unit") is None:
        d.pop("unit", None)
    _validator(registry, "#/$defs/dataset").validate(d)


@pytest.mark.parametrize("patch", [
    {"id": "dataset-1"},
    {"id": "dataset-0A1B-2c3d-4e5f"},          # upper-case hex
    {"id": "preset-0a1b-2c3d-4e5f"},
    {"id": ""},
    {"name": ""},
    {"name": "x" * 65},
    {"scope": "global"},
    {"unit": "kg"},
    {"field": "positions.willco@window(0)"},
    {"field": "positions.willco@window(1000)"},
    {"field": "positions.willco@window()"},
    {"field": "positions.willco@mean(3)"},
    {"field": "Positions.willco"},
    {"field": "willco"},
    {"style": {}},                                        # style must be complete
    {"style": {**_LINE_STYLE, "seriesType": "Candles"}},
    {"style": {**_LINE_STYLE, "lineWidth": 5}},
    {"style": {**_LINE_STYLE, "lineStyle": 5}},
    {"style": {**_LINE_STYLE, "color": "red"}},
    {"style": {**_LINE_STYLE, "color": "#112233"}},       # alpha is mandatory
    {"style": {**_LINE_STYLE, "unknown": 1}},
    {"style": {**_LINE_STYLE, "upColor": "#26a69aff"}},   # mixed candle + series keys
    {"style": {k: v for k, v in _CANDLE_STYLE.items() if k != "volumeUpColor"}},
    {"style": {**_CANDLE_STYLE, "wickUpColor": "#26a69aff"}},
    {"style": {**_CANDLE_STYLE, "chartType": "line"}},
    {"unknown": 1},
])
def test_dataset_invalid(patch, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry, "#/$defs/dataset").validate(_dataset(**patch))


@pytest.mark.parametrize("key", ["id", "scope", "name", "field", "style"])
def test_dataset_required_keys(key, registry):
    from jsonschema import ValidationError

    bad = _dataset()
    del bad[key]
    with pytest.raises(ValidationError):
        _validator(registry, "#/$defs/dataset").validate(bad)


@pytest.mark.parametrize("ref", [
    "candles", "positions.yur_net", "trades.val_b@median(30)", "obstats.vol_b@median(1)", "hhi.volume",
    "positions.willco@window(180)", "positions.willco@window(2)", "positions.willco@window(500)",
])
def test_dataset_ref_valid(ref, registry):
    _validator(registry, "#/$defs/datasetRef").validate(ref)


@pytest.mark.parametrize("ref", [
    "candles.", "Candles", "close", "positions.yur_net@median(0)", "positions.yur_net@median(1000)",
    "positions.willco@window(0)", "positions.willco@window(05)", "positions.willco@window(x)",
    "trades.val_b@median(3)@median(3)", "trades.val_b@median(3)@window(3)", "positions.", ".yur_net", "", 5,
])
def test_dataset_ref_invalid(ref, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry, "#/$defs/datasetRef").validate(ref)


def test_dataset_style_candles_and_overrides(registry):
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/datasetStyle")
    v.validate(_CANDLE_STYLE)
    v.validate({**_CANDLE_STYLE, "chartType": "bars"})
    v.validate(_LINE_STYLE)
    for bad in ({}, {"color": "#112233ff"}):
        with pytest.raises(ValidationError):
            v.validate(bad)


def test_series_style_bottom_color(registry):
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/seriesStyle")
    v.validate({**_LINE_STYLE, "seriesType": "Baseline", "bottomColor": "#ff9800ff"})
    v.validate(_LINE_STYLE)  # bottomColor is optional
    for bad in ("#ff9800", "red", "#FF9800FF", 5):
        with pytest.raises(ValidationError):
            v.validate({**_LINE_STYLE, "seriesType": "Baseline", "bottomColor": bad})


def test_dataset_shadow_valid(registry):
    """A personal row with the id of a shared dataset is the caller's personal style (shadow)."""
    _validator(registry, "#/$defs/dataset").validate(
        _dataset(scope="personal", style={**_LINE_STYLE, "seriesType": "Baseline", "bottomColor": "#ff9800ff"}))


def test_preset_item_scale_visible(registry):
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/presetItem")
    v.validate({"dataset": _DS_A})
    for scale in ("right", "left", "own"):
        v.validate({"dataset": _DS_A, "visible": False, "scale": scale})
    v.validate({"dataset": _DS_A, "visible": True})
    for bad in ({"dataset": _DS_A, "style": {"color": "#112233ff"}}, {"dataset": _DS_A, "scale": "top"},
                {"dataset": _DS_A, "visible": "yes"}, {"dataset": _DS_A, "extra": 1}, {"visible": True}):
        with pytest.raises(ValidationError):
            v.validate(bad)


def test_style_defs_shape(registry):
    """The style atoms and the three object styles are complete and closed."""
    schema = json.loads((Path(__file__).parents[2] / "spec" / "schemas" / "gp.v2.json").read_text(encoding="utf-8"))
    defs = schema["$defs"]
    assert "primitiveKindStyle" not in defs
    for name, keys in (("lineObjectStyle", {"color", "lineWidth", "lineStyle"}),
                       ("seriesStyle", {"seriesType", "color", "lineWidth", "lineStyle"}),
                       ("candleStyle", {"chartType", "upColor", "downColor", "volumeUpColor", "volumeDownColor"})):
        assert set(defs[name]["required"]) == keys == set(defs[name]["properties"]) - ({"bottomColor"} if name == "seriesStyle" else set())
        assert defs[name]["additionalProperties"] is False
    assert "datasetStyleOverride" not in defs
    assert "required" not in defs["indicatorSettings"]
    assert "style" in defs["indicator"]["required"]


def test_dataset_rejection(registry):
    from jsonschema import ValidationError

    v = _validator(registry, "#/$defs/datasetRejection")
    v.validate({"id": _DS_A, "code": "forbidden"})
    v.validate({"id": _DS_A, "code": "validation_error", "message": "x"})
    for bad in ({"id": _DS_A}, {"code": "forbidden"}, {"id": "", "code": "forbidden"},
                {"id": _DS_A, "code": "nope"}, {"id": _DS_A, "code": "forbidden", "extra": 1}):
        with pytest.raises(ValidationError):
            v.validate(bad)


def _preset(**overrides):
    p = {"id": "preset-1", "scope": "personal", "name": "Мой",
         "panes": {"price": [{"dataset": _DS_A}], "upper": [{"dataset": _DS_B, "visible": False, "scale": "left"}], "lower": []}}
    p.update(overrides)
    return p


def _items(n):
    return [{"dataset": f"dataset-0000-0000-{n_:04x}"} for n_ in range(n)]


def test_preset_valid(registry):
    v = _validator(registry, "#/$defs/preset")
    v.validate(_preset())
    v.validate(_preset(scope="shared", panes={"price": [], "upper": [], "lower": []}))
    v.validate(_preset(name="x" * 64, panes={"price": _items(16), "upper": [], "lower": []}))
    v.validate(_preset(panes={"price": [{"dataset": _DS_A, "scale": "own"}], "upper": [], "lower": []}))


@pytest.mark.parametrize("patch", [
    {"panes": {"price": [], "upper": []}},                                          # missing pane
    {"panes": {"price": [], "upper": [], "lower": [], "extra": []}},                 # unknown pane
    {"panes": {"price": _items(17), "upper": [], "lower": []}},                      # > 16
    {"panes": {"price": [], "upper": _items(17), "lower": []}},
    {"panes": {"price": [], "upper": [], "lower": _items(17)}},
    {"panes": {"price": ["a"], "upper": [], "lower": []}},                           # old string ids
    {"panes": {"price": [{"dataset": ""}], "upper": [], "lower": []}},               # empty id
    {"panes": {"price": [{}], "upper": [], "lower": []}},                            # no dataset
    {"panes": {"price": [{"dataset": "a", "extra": 1}], "upper": [], "lower": []}},  # unknown item key
    {"panes": {"price": [{"dataset": "a", "style": {"color": "#112233ff"}}], "upper": [], "lower": []}},  # style is gone
    {"panes": {"price": [{"dataset": "a", "scale": "top"}], "upper": [], "lower": []}},
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
