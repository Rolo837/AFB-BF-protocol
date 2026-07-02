"""afb.tradeplan.v1 / afb.tradeplan.v2 template schemas.

Trade-plan templates are AFB-side only — they never cross the AFB<->BF wire —
so unlike deal/envelope fixtures they are not signed envelopes; they live under
``examples/tradeplans/`` and are validated directly against the schema files.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES

TRADEPLAN_EXAMPLES = sorted((EXAMPLES / "tradeplans").glob("*.json"))
assert TRADEPLAN_EXAMPLES, "no tradeplan examples found"

TRADEPLAN_V1_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/tradeplan.v1.json"
TRADEPLAN_V2_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/tradeplan.v2.json"
_SCHEMA_ID_BY_NAME = {"afb.tradeplan.v1": TRADEPLAN_V1_ID, "afb.tradeplan.v2": TRADEPLAN_V2_ID}


def _validator(schema_url: str, registry):
    from jsonschema import Draft202012Validator

    resolved = registry[schema_url]
    return Draft202012Validator(resolved.contents, registry=registry)


@pytest.mark.parametrize("path", TRADEPLAN_EXAMPLES, ids=lambda p: p.stem)
def test_example_validates_against_declared_or_default_schema(path: Path, registry):
    data = json.loads(path.read_text())
    schema_name = data.get("schema") or "afb.tradeplan.v1"
    _validator(_SCHEMA_ID_BY_NAME[schema_name], registry).validate(data)


def test_no_schema_field_means_v1():
    path = EXAMPLES / "tradeplans" / "tradeplan.v1.no-schema-field.json"
    data = json.loads(path.read_text())
    assert "schema" not in data


def test_v1_rejects_missing_required_fields(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(TRADEPLAN_V1_ID, registry).validate({"id": "x"})  # no ticker/entry_condition


@pytest.mark.parametrize("value", ["buy", "sell", "long", "short"])
def test_v1_direction_accepts_legacy_and_target_vocabulary(value, registry):
    """Transitional: afb.tradeplan.v1.direction accepts both buy/sell (legacy)
    and long/short (target) while the frontend migrates."""
    plan = {
        "id": "tp1",
        "ticker": "SBER",
        "direction": value,
        "entry_condition": {"condition_type": "price", "price_value": 100},
    }
    _validator(TRADEPLAN_V1_ID, registry).validate(plan)  # does not raise


def test_v1_direction_rejects_unknown_value(registry):
    from jsonschema import ValidationError

    plan = {
        "id": "tp1",
        "ticker": "SBER",
        "direction": "up",
        "entry_condition": {"condition_type": "price", "price_value": 100},
    }
    with pytest.raises(ValidationError):
        _validator(TRADEPLAN_V1_ID, registry).validate(plan)


def test_v2_requires_non_empty_entries(registry):
    from jsonschema import ValidationError

    plan = {
        "schema": "afb.tradeplan.v2",
        "id": "tp1",
        "ticker": "SBER",
        "direction": "long",
        "entries": [],
        "sizing": {"mode": "lots", "value": "1"},
    }
    with pytest.raises(ValidationError):
        _validator(TRADEPLAN_V2_ID, registry).validate(plan)


def test_v2_requires_direction(registry):
    from jsonschema import ValidationError

    plan = {
        "schema": "afb.tradeplan.v2",
        "id": "tp1",
        "ticker": "SBER",
        "entries": [
            {"condition": {"left": {"source": "price", "field": "last"}, "right": {"const": "100"}}}
        ],
        "sizing": {"mode": "lots", "value": "1"},
    }
    with pytest.raises(ValidationError):
        _validator(TRADEPLAN_V2_ID, registry).validate(plan)


def test_v2_condition_left_right_pairing_is_not_enforced_here(registry):
    """tradeplan.v2 deliberately does NOT enforce the left/right pairing matrix
    (price/quote const-only, indicator/dataset const-or-same-kind) — that would
    combinatorially explode once primitiveRef is allowed on either side. The
    matrix is enforced after compilation, by deal.v2.json and by BF."""
    plan = {
        "schema": "afb.tradeplan.v2",
        "id": "tp1",
        "ticker": "SBER",
        "direction": "long",
        "entries": [
            {
                "condition": {
                    "left": {"source": "price", "field": "last"},
                    "right": {"source": "indicator", "type": "wma"},
                },
            }
        ],
        "sizing": {"mode": "lots", "value": "1"},
    }
    _validator(TRADEPLAN_V2_ID, registry).validate(plan)  # does not raise


def test_v2_primitive_ref_rejects_extra_keys(registry):
    from jsonschema import ValidationError

    plan = {
        "schema": "afb.tradeplan.v2",
        "id": "tp1",
        "ticker": "SBER",
        "direction": "long",
        "entries": [
            {
                "condition": {
                    "left": {"source": "price", "field": "last"},
                    "right": {"primitive_id": "line-1", "extra": "nope"},
                },
            }
        ],
        "sizing": {"mode": "lots", "value": "1"},
    }
    with pytest.raises(ValidationError):
        _validator(TRADEPLAN_V2_ID, registry).validate(plan)
