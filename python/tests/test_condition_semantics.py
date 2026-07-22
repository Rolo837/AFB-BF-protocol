"""afb_bf_protocol.condition_semantics — the reference evaluator for
condition.v1.json. BF and AFB each have their own regression suites that
exercise this through their real data plumbing; this suite only pins the pure
math."""
from __future__ import annotations

import pytest

from afb_bf_protocol.condition_semantics import (
    IMMEDIATE_OPS,
    OPS_BY_SOURCE,
    PRICE_CANDLE_OPS,
    PRICE_LEVEL_OPS,
    PRICE_TOUCH_OPS,
    SCALAR_OPS,
    evaluate_candle_op,
    evaluate_immediate,
    evaluate_price_level_op,
    evaluate_scalar_op,
    evaluate_touch,
)


def test_ops_by_source_matches_schema_vocabulary():
    assert OPS_BY_SOURCE["price"] == PRICE_TOUCH_OPS | PRICE_CANDLE_OPS | PRICE_LEVEL_OPS
    assert OPS_BY_SOURCE["indicator"] == SCALAR_OPS
    assert OPS_BY_SOURCE["dataset"] == SCALAR_OPS
    assert OPS_BY_SOURCE["immediate"] == IMMEDIATE_OPS
    assert "quote" not in OPS_BY_SOURCE
    assert PRICE_TOUCH_OPS == {"touch"}
    assert IMMEDIATE_OPS == {"above"}


# --- evaluate_immediate ------------------------------------------------------


def test_evaluate_immediate_true_for_positive_price():
    assert evaluate_immediate("2.918") is True
    assert evaluate_immediate(0.01) is True


def test_evaluate_immediate_false_for_missing_or_nonpositive():
    assert evaluate_immediate(None) is False
    assert evaluate_immediate("0") is False
    assert evaluate_immediate("-1") is False


# --- evaluate_touch --------------------------------------------------------


@pytest.mark.parametrize(
    "cur, prev, level, expected",
    [
        ("101", "99", "100", True),  # level strictly between prev/cur
        ("99", "101", "100", True),  # direction doesn't matter
        ("100", "99", "100", True),  # cur == level
        ("101", "100", "100", True),  # prev == level
        ("102", "101", "100", False),  # level outside the [prev, cur] band
        ("101", "102", "100", False),
    ],
)
def test_evaluate_touch(cur, prev, level, expected):
    assert evaluate_touch(cur, prev, level) is expected


def test_evaluate_touch_missing_data_is_false():
    assert evaluate_touch(None, "99", "100") is False
    assert evaluate_touch("101", None, "100") is False
    assert evaluate_touch("101", "99", None) is False


# --- evaluate_price_level_op: inclusive above/below ------------------------


def test_price_level_above_below_inclusive():
    assert evaluate_price_level_op("above", "101", "100") is True
    assert evaluate_price_level_op("above", "100", "100") is True
    assert evaluate_price_level_op("above", "99", "100") is False
    assert evaluate_price_level_op("below", "99", "100") is True
    assert evaluate_price_level_op("below", "100", "100") is True
    assert evaluate_price_level_op("below", "101", "100") is False


def test_price_level_op_missing_data_is_false():
    assert evaluate_price_level_op("above", None, "100") is False
    assert evaluate_price_level_op("above", "101", None) is False


def test_price_level_op_unknown_raises():
    with pytest.raises(ValueError):
        evaluate_price_level_op("crossing", "101", "100")


# --- evaluate_scalar_op: above/below ----------------------------------------


def test_scalar_above_below():
    assert evaluate_scalar_op("above", "101", "99", "100") is True
    assert evaluate_scalar_op("above", "100", "99", "100") is False
    assert evaluate_scalar_op("below", "99", "101", "100") is True
    assert evaluate_scalar_op("below", "100", "101", "100") is False


def test_scalar_above_below_do_not_need_prev():
    assert evaluate_scalar_op("above", "101", None, "100") is True
    assert evaluate_scalar_op("below", "99", None, "100") is True


# --- evaluate_scalar_op: crossing family + the prev==ref regression --------


def test_crosses_above_prev_equal_ref_fires():
    """Regression 3.248 (alarm alarm-5a01-4480-ba65): prev == ref used to be
    treated as 'not yet crossed' (strict prev < ref), silently missing the
    cross. Non-strict prev <= ref_prev must fire here."""
    assert evaluate_scalar_op("crosses_above", cur="101", prev="100", ref_cur="100", ref_prev="100") is True


def test_crosses_below_prev_equal_ref_fires():
    assert evaluate_scalar_op("crosses_below", cur="99", prev="100", ref_cur="100", ref_prev="100") is True


def test_crossing_prev_equal_ref_fires_either_direction():
    assert evaluate_scalar_op("crossing", cur="101", prev="100", ref_cur="100", ref_prev="100") is True
    assert evaluate_scalar_op("crossing", cur="99", prev="100", ref_cur="100", ref_prev="100") is True


def test_touch_without_departure_is_not_a_cross():
    # cur == ref exactly: no departure past the level -> never a cross.
    assert evaluate_scalar_op("crosses_above", cur="100", prev="99", ref_cur="100") is False
    assert evaluate_scalar_op("crosses_below", cur="100", prev="101", ref_cur="100") is False


def test_crosses_above_requires_actually_ending_above():
    assert evaluate_scalar_op("crosses_above", cur="99", prev="98", ref_cur="100") is False


def test_crossing_constant_right_defaults_ref_prev_to_ref_cur():
    # ref_prev omitted -> defaults to ref_cur, i.e. a constant threshold.
    assert evaluate_scalar_op("crosses_above", cur="101", prev="99", ref_cur="100") is True
    assert evaluate_scalar_op("crosses_above", cur="101", prev="99", ref_cur="100", ref_prev=None) is True


def test_crossing_family_missing_prev_is_false():
    assert evaluate_scalar_op("crosses_above", cur="101", prev=None, ref_cur="100") is False
    assert evaluate_scalar_op("crosses_below", cur="99", prev=None, ref_cur="100") is False
    assert evaluate_scalar_op("crossing", cur="101", prev=None, ref_cur="100") is False


def test_scalar_op_missing_cur_or_ref_is_false():
    assert evaluate_scalar_op("above", None, "99", "100") is False
    assert evaluate_scalar_op("above", "101", "99", None) is False


def test_scalar_op_unknown_raises():
    with pytest.raises(ValueError):
        evaluate_scalar_op("sideways", "101", "99", "100")


# --- evaluate_candle_op ------------------------------------------------------


def test_breakout_open_below_close_above():
    assert evaluate_candle_op("breakout", open_="99", close="101", level="100") is True


def test_breakout_rejects_open_above_level():
    assert evaluate_candle_op("breakout", open_="101", close="102", level="100") is False


def test_breakdown_open_above_close_below():
    assert evaluate_candle_op("breakdown", open_="101", close="99", level="100") is True


def test_crossing_candle_is_breakout_or_breakdown():
    assert evaluate_candle_op("crossing", open_="99", close="101", level="100") is True
    assert evaluate_candle_op("crossing", open_="101", close="99", level="100") is True
    assert evaluate_candle_op("crossing", open_="99", close="99.5", level="100") is False


def test_candle_op_missing_data_is_false():
    assert evaluate_candle_op("breakout", open_=None, close="101", level="100") is False
    assert evaluate_candle_op("breakout", open_="99", close=None, level="100") is False
    assert evaluate_candle_op("breakout", open_="99", close="101", level=None) is False


def test_candle_op_unknown_raises():
    with pytest.raises(ValueError):
        evaluate_candle_op("sideways", open_="99", close="101", level="100")
