"""afb.gp.v1 — AFB-side graphic (chart) primitive schema. Promotes the parked
settings.primitives[secid][] draft into a strict canonical entity: no
examples/gp/*.json fixtures — inline dicts cover the kind/point matrix, same
style as test_afbws_alarm_channel_schema.py's inline `_ALARM_ITEM`."""
from __future__ import annotations

import pytest

GP_V1_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/gp.v1.json"

_POINT = {"time": 1721000000, "price": 123.45}


def _line(**overrides):
    item = {
        "schema": "afb.gp.v1",
        "id": "gp-1",
        "ticker": "SBER",
        "kind": "line",
        "start": dict(_POINT),
    }
    item.update(overrides)
    return item


def _zone(**overrides):
    item = _line(kind="zone", stop=dict(_POINT))
    item.update(overrides)
    return item


def _note(**overrides):
    item = _line(kind="note")
    item.update(overrides)
    return item


def _validator(registry):
    from jsonschema import Draft202012Validator

    resolved = registry[GP_V1_ID]
    return Draft202012Validator(resolved.contents, registry=registry)


# --- required fields / basic shape ------------------------------------------

@pytest.mark.parametrize("kind", ["line", "line_enter", "line_sl", "line_tp"])
def test_single_anchor_kinds_valid(kind, registry):
    _validator(registry).validate(_line(kind=kind))  # does not raise


@pytest.mark.parametrize("kind", ["zone", "ruler"])
def test_two_anchor_kinds_require_stop(kind, registry):
    _validator(registry).validate(_zone(kind=kind))  # does not raise


def test_note_valid_with_and_without_text(registry):
    _validator(registry).validate(_note())  # does not raise
    _validator(registry).validate(_note(text="entry idea"))  # does not raise


def test_rejects_missing_required_fields(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate({"schema": "afb.gp.v1"})


def test_rejects_unknown_schema(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(schema="afb.gp.v2"))


def test_rejects_extra_top_level_field(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(unexpected=1))


def test_rejects_used_in_tradeplans(registry):
    """The whole point of the migration: this derived flag is never part of
    the wire entity — additionalProperties: false rejects it outright."""
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(used_in_tradeplans=True))


# --- conditional stop (zone/ruler only) --------------------------------------

@pytest.mark.parametrize("kind", ["zone", "ruler"])
def test_zone_ruler_require_stop(kind, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(kind=kind))  # no stop


@pytest.mark.parametrize("kind", ["line", "line_enter", "line_sl", "line_tp", "note"])
def test_non_zone_ruler_kinds_reject_stop(kind, registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(kind=kind, stop=dict(_POINT)))


# --- conditional text (note only) --------------------------------------------

@pytest.mark.parametrize("kind", ["line", "line_enter", "line_sl", "line_tp", "zone", "ruler"])
def test_non_note_kinds_reject_text(kind, registry):
    from jsonschema import ValidationError

    base = _zone(kind=kind) if kind in ("zone", "ruler") else _line(kind=kind)
    base["text"] = "should not be allowed here"
    with pytest.raises(ValidationError):
        _validator(registry).validate(base)


def test_text_over_max_length_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_note(text="x" * 161))


# --- point strictness ---------------------------------------------------------

def test_point_rejects_non_integer_time(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(start={"time": 1721000000.5, "price": 1.0}))


def test_point_rejects_extra_field(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(start={"time": 1721000000, "price": 1.0, "extra": True}))


def test_point_requires_both_fields(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_line(start={"time": 1721000000}))
