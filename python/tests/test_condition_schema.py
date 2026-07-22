"""spec/schemas/condition.v1.json — the shared conditionNode vocabulary used by
deal.v2, tradeplan.v2 and alarm.v1. Validates the source x op matrix directly
against the schema (independent of condition_semantics.py's runtime math)."""
from __future__ import annotations

import pytest

CONDITION_V1_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/condition.v1.json"


def _validator(registry):
    from jsonschema import Draft202012Validator

    resolved = registry[CONDITION_V1_ID]
    return Draft202012Validator(resolved.contents, registry=registry)


def _validates(registry, node) -> bool:
    from jsonschema import ValidationError

    try:
        _validator(registry).validate(node)
        return True
    except ValidationError:
        return False


PRICE = {"source": "price"}
QUOTE_BID = {"source": "quote", "field": "bid"}
INDICATOR_WMA = {"source": "indicator", "type": "wma", "id": "ind1"}
DATASET_POS = {"source": "dataset", "dataset_id": "positions.long", "field": "long"}
IMMEDIATE = {"source": "immediate"}
CONST_100 = {"const": "100"}
CONST_0 = {"const": "0"}


@pytest.mark.parametrize(
    "node",
    [
        {"left": PRICE, "right": CONST_100},  # touch, no op (wire back-compat)
        {"left": PRICE, "right": CONST_100, "op": "touch"},  # touch, explicit op
        {"left": PRICE, "right": CONST_100, "op": "breakout", "timeframe": "5min"},
        {"left": PRICE, "right": CONST_100, "op": "breakdown", "timeframe": "1d"},
        {"left": PRICE, "right": CONST_100, "op": "crossing", "timeframe": "1h"},
        {"left": PRICE, "right": CONST_100, "op": "above"},  # price level op
        {"left": PRICE, "right": CONST_100, "op": "above", "duration": 3},
        {"left": PRICE, "right": CONST_100, "op": "below", "duration": 1},
        {"left": INDICATOR_WMA, "right": CONST_100, "op": "above"},
        {"left": INDICATOR_WMA, "right": INDICATOR_WMA, "op": "crosses_above"},
        {"left": INDICATOR_WMA, "right": CONST_100, "op": "above", "timeframe": "30min"},
        {"left": INDICATOR_WMA, "right": INDICATOR_WMA, "op": "crosses_above", "timeframe": "1h"},
        {"left": DATASET_POS, "right": CONST_100, "op": "crossing"},
        {"left": DATASET_POS, "right": DATASET_POS, "op": "below"},
        {"left": IMMEDIATE, "right": CONST_0, "op": "above"},
    ],
    ids=[
        "price-touch-no-op",
        "price-touch-explicit-op",
        "price-breakout-with-timeframe",
        "price-breakdown-with-timeframe",
        "price-crossing-candle-with-timeframe",
        "price-level-above",
        "price-level-above-with-duration",
        "price-level-below-with-duration",
        "indicator-vs-const",
        "indicator-vs-indicator",
        "indicator-vs-const-with-timeframe",
        "indicator-vs-indicator-with-timeframe",
        "dataset-vs-const",
        "dataset-vs-dataset",
        "immediate-entry",
    ],
)
def test_valid_condition_nodes(node, registry):
    assert _validates(registry, node)


@pytest.mark.parametrize(
    "node",
    [
        {"left": PRICE, "right": CONST_100, "op": "touch", "timeframe": "5min"},  # touch + timeframe rejected
        {"left": PRICE, "right": CONST_100, "op": "above", "timeframe": "5min"},  # level op + timeframe rejected
        {"left": PRICE, "right": CONST_100, "op": "above", "duration": 0},  # duration minimum 1
        {"left": PRICE, "right": CONST_100, "op": "breakout"},  # candle op without required timeframe
        {"left": INDICATOR_WMA, "right": CONST_100, "op": "breakout"},  # candle op not valid for indicator
        {"left": DATASET_POS, "right": CONST_100, "op": "sideways"},  # unknown op
        {"left": PRICE, "right": CONST_100, "op": "crosses_above", "timeframe": "5min"},  # op not in the candle enum
        {"left": PRICE, "right": CONST_100, "op": "crossing"},  # candle crossing without required timeframe (removed v2.0.0: deprecated tick path)
        {"left": INDICATOR_WMA, "right": DATASET_POS, "op": "above"},  # cross-kind right not allowed
        {"left": {"source": "dataset", "dataset_id": "positions.long"}, "right": CONST_100, "op": "above"},  # missing field
        {"left": QUOTE_BID, "right": CONST_100},  # quote source no longer accepted (removed v2.0.0)
        {"left": QUOTE_BID, "right": CONST_100, "op": "above"},  # quote source no longer accepted (removed v2.0.0)
        {"right": CONST_100},  # missing left
        {"left": PRICE},  # missing right
        {"left": INDICATOR_WMA, "right": CONST_100, "op": "above", "timeframe": "1min"},  # not in enum
        {"left": IMMEDIATE, "right": CONST_0, "op": "below"},  # op fixed to "above" only
        {"left": IMMEDIATE, "right": CONST_0},  # op required even though its value is a placeholder
        {"left": IMMEDIATE, "right": CONST_0, "op": "above", "timeframe": "5min"},  # no timeframe concept
        {"left": IMMEDIATE, "op": "above"},  # right required even though its value is a placeholder
    ],
    ids=[
        "price-touch-with-timeframe-rejected",
        "price-level-op-with-timeframe-rejected",
        "price-duration-below-minimum-rejected",
        "price-breakout-without-timeframe-rejected",
        "indicator-with-candle-op-rejected",
        "dataset-unknown-op-rejected",
        "price-crosses-above-not-a-candle-op-rejected",
        "price-crossing-without-timeframe-rejected",
        "indicator-vs-dataset-cross-kind-rejected",
        "dataset-missing-field-rejected",
        "quote-source-rejected-no-op",
        "quote-source-rejected-with-op",
        "missing-left-rejected",
        "missing-right-rejected",
        "indicator-timeframe-not-in-enum-rejected",
        "immediate-op-must-be-above-rejected",
        "immediate-missing-op-rejected",
        "immediate-timeframe-rejected",
        "immediate-missing-right-rejected",
    ],
)
def test_invalid_condition_nodes(node, registry):
    assert not _validates(registry, node)
