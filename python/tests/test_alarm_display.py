"""Tests for afb_bf_protocol.alarm_display — mirrors frontend alarm cards."""
from __future__ import annotations

from afb_bf_protocol.alarm_display import (
    build_display,
    chart_indicator_display_label,
    condition_description,
    condition_op_label,
    condition_text,
    instrument_label,
)

INDICATORS = [
    {"id": "wma20", "type": "wma", "settings": {"period": 20}},
    {"id": "kama10", "type": "kama", "settings": {"erPeriod": 10}},
]


def test_condition_op_label_touch():
    assert condition_op_label(None) == "Касание"
    assert condition_op_label("breakout") == "Пробой вверх"


def test_condition_description_price():
    cond = {"left": {"source": "price"}, "right": {"const": "250.5"}}
    assert condition_description(cond) == "Цена 250.5"


def test_condition_description_indicator_crossing():
    cond = {
        "op": "crosses_above",
        "left": {"source": "indicator", "id": "wma20"},
        "right": {"source": "indicator", "id": "kama10"},
    }
    assert condition_description(cond, INDICATORS) == "WMA (20) / KAMA (10)"


def test_condition_description_indicator_vs_const():
    cond = {
        "op": "above",
        "left": {"source": "indicator", "id": "wma20"},
        "right": {"const": "100"},
    }
    assert condition_description(cond, INDICATORS) == "WMA (20) 100"


def test_condition_description_dataset():
    cond = {
        "op": "above",
        "left": {"source": "dataset", "dataset_id": "positions", "field": "long"},
        "right": {"const": "1000"},
    }
    assert condition_description(cond) == "Позиции/long 1000"


def test_condition_text_price_touch():
    cond = {"left": {"source": "price"}, "right": {"const": "250.5"}}
    assert condition_text(cond) == "Цена касание 250.5"


def test_condition_text_dataset():
    cond = {
        "op": "above",
        "left": {"source": "dataset", "dataset_id": "orders", "field": "delta"},
        "right": {"const": "10000"},
    }
    assert condition_text(cond) == "Ордера/delta выше 10000"


def test_condition_text_indicator_crossing():
    cond = {
        "op": "crosses_above",
        "left": {"source": "indicator", "id": "wma20"},
        "right": {"source": "indicator", "id": "kama10"},
    }
    assert condition_text(cond, INDICATORS) == "WMA (20) пересечение вверх KAMA (10)"


def test_instrument_label_with_shortname():
    assert instrument_label("Сбербанк", "SBER") == "Сбербанк (SBER)"


def test_instrument_label_without_shortname():
    assert instrument_label(None, "SBER") == "SBER"


def test_chart_indicator_display_label():
    assert chart_indicator_display_label({"type": "wma", "settings": {"period": 5}}) == "WMA (5)"


def test_build_display():
    cond = {"left": {"source": "price"}, "right": {"const": "250.5"}}
    display = build_display(condition=cond, ticker="SBER", shortname="Сбербанк")
    assert display["instrument_label"] == "Сбербанк (SBER)"
    assert display["condition_text"] == "Цена касание 250.5"
