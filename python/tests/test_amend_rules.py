"""amend_rules: the allowed-edit matrix (phase × field) for live deals."""
from __future__ import annotations

import copy

import pytest

from afb_bf_protocol import AmendContext, evaluate_amend, is_amend_allowed


def _deal_v1(**over):
    d = {
        "schema": "afb.deal.v1",
        "deal_id": "deal-x:bf1",
        "revision": 1,
        "owner": {"user_id": "u"},
        "target": {
            "bf_id": "bf1",
            "broker": "finam-arena",
            "instrument": {
                "exchange": "MOEX", "board": "TQBR", "ticker": "SBER",
                "market": "stock", "price_step": "0.01",
            },
        },
        "entry": {
            "side": "buy",
            "condition": {
                "node_type": "event", "id": "entry_1", "op": "above",
                "left": {"source": "price", "field": "last"},
                "right": {"const": "100.5"},
            },
            "order": {"type": "market"},
        },
        "sizing": {"mode": "lots", "value": "10"},
        "risk": {
            "stop_loss": {"condition": {
                "node_type": "event", "id": "sl", "op": "below",
                "left": {"source": "price", "field": "last"}, "right": {"const": "95"}}},
            "take_profit": {"condition": {
                "node_type": "event", "id": "tp", "op": "above",
                "left": {"source": "price", "field": "last"}, "right": {"const": "110"}}},
        },
        "execution_policy": {"max_spread_steps": 5},
    }
    d.update(over)
    return d


def _ctx(status, phase, **kw):
    return AmendContext(status=status, phase=phase, **kw)


# --- changed-field detection ------------------------------------------------

def _mutate(deal, path, value):
    d = copy.deepcopy(deal)
    cur = d
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value
    return d


def test_noop_amend_always_allowed():
    d = _deal_v1()
    dec = evaluate_amend(d, copy.deepcopy(d), _ctx("active", "holding"))
    assert dec.allowed
    assert dec.changed() == []


def test_only_changed_fields_are_judged():
    d = _deal_v1()
    new = _mutate(d, ["risk", "stop_loss", "condition", "right", "const"], "96")
    dec = evaluate_amend(d, new, _ctx("active", "holding"))
    changed = {v.field for v in dec.changed()}
    assert changed == {"stop_loss"}


# --- entry-defining fields freeze once a position exists --------------------

@pytest.mark.parametrize("phase,allowed", [
    ("idle", True),            # published, not activated
    ("awaiting_entry", True),
    ("entry_working", True),   # no fill yet -> cancel+replace
    ("holding", False),
    ("exit_working", False),
])
def test_entry_level_by_phase(phase, allowed):
    d = _deal_v1()
    new = _mutate(d, ["entry", "condition", "right", "const"], "101.5")
    dec = evaluate_amend(d, new, _ctx("active" if phase != "idle" else "published", phase))
    assert dec.allowed is allowed


@pytest.mark.parametrize("phase,allowed", [
    ("awaiting_entry", True), ("entry_working", True),
    ("holding", False), ("exit_working", False),
])
def test_side_by_phase(phase, allowed):
    d = _deal_v1()
    new = _mutate(d, ["entry", "side"], "sell")
    assert is_amend_allowed(d, new, _ctx("active", phase)) is allowed


def test_v1_direction_change_detected_when_entry_side_absent():
    """Transitional afb.deal.v1: entry.side is optional when the deal-level
    `direction` is set — the "side" amend field must fall back to it."""
    d = _deal_v1()
    del d["entry"]["side"]
    d["direction"] = "long"
    new = copy.deepcopy(d)
    new["direction"] = "short"
    dec = evaluate_amend(d, new, _ctx("active", "holding"))
    assert dec.allowed is False
    assert "side" in {v.field for v in dec.rejected()}


def test_v1_entry_side_wins_over_direction_when_both_present():
    d = _deal_v1()
    d["direction"] = "long"
    new = copy.deepcopy(d)
    new["direction"] = "short"  # direction changes, but entry.side (governing) does not
    dec = evaluate_amend(d, new, _ctx("active", "holding"))
    assert dec.allowed is True
    assert dec.changed() == []


def test_instrument_immutable_once_active():
    d = _deal_v1()
    new = _mutate(d, ["target", "instrument", "ticker"], "GAZP")
    assert is_amend_allowed(d, new, _ctx("published", "idle")) is True
    for phase in ("awaiting_entry", "entry_working", "holding", "exit_working"):
        assert is_amend_allowed(d, new, _ctx("active", phase)) is False


# --- sizing: editable only before entry -------------------------------------

def test_sizing_free_before_entry():
    d = _deal_v1()
    bigger = _mutate(d, ["sizing", "value"], "20")
    smaller = _mutate(d, ["sizing", "value"], "5")
    for phase in ("awaiting_entry", "entry_working"):
        assert is_amend_allowed(d, bigger, _ctx("active", phase)) is True
        assert is_amend_allowed(d, smaller, _ctx("active", phase)) is True


@pytest.mark.parametrize("phase", ["holding", "exit_working"])
def test_sizing_frozen_after_entry(phase):
    d = _deal_v1()
    for value in ("20", "4"):  # neither increase nor decrease is allowed
        new = _mutate(d, ["sizing", "value"], value)
        dec = evaluate_amend(d, new, _ctx("active", phase))
        assert dec.allowed is False
        assert "size_immutable_after_entry" in dec.reasons()


# --- protective levels stay editable ----------------------------------------

@pytest.mark.parametrize("phase", ["awaiting_entry", "entry_working", "holding"])
def test_stop_loss_editable_through_lifecycle(phase):
    d = _deal_v1()
    new = _mutate(d, ["risk", "stop_loss", "condition", "right", "const"], "97")
    assert is_amend_allowed(d, new, _ctx("active", phase)) is True


def test_stop_loss_in_exit_allowed_with_warning():
    d = _deal_v1()
    new = _mutate(d, ["risk", "stop_loss", "condition", "right", "const"], "97")
    dec = evaluate_amend(d, new, _ctx("active", "exit_working"))
    assert dec.allowed is True
    assert any(w.field == "stop_loss" for w in dec.warnings())


def test_take_profit_editable_while_holding():
    d = _deal_v1()
    new = _mutate(d, ["risk", "take_profit", "condition", "right", "const"], "115")
    assert is_amend_allowed(d, new, _ctx("active", "holding")) is True


# --- terminal & multi-field -------------------------------------------------

@pytest.mark.parametrize("status", ["closed", "cancelled", "orphaned"])
def test_terminal_immutable(status):
    d = _deal_v1()
    new = _mutate(d, ["risk", "stop_loss", "condition", "right", "const"], "97")
    dec = evaluate_amend(d, new, _ctx(status, "idle"))
    assert dec.allowed is False
    assert "terminal_immutable" in dec.reasons()


def test_mixed_amend_denied_if_any_field_denied():
    d = _deal_v1()
    # move SL (allowed in holding) AND change entry level (denied in holding)
    new = _mutate(d, ["risk", "stop_loss", "condition", "right", "const"], "97")
    new = _mutate(new, ["entry", "condition", "right", "const"], "102")
    dec = evaluate_amend(d, new, _ctx("active", "holding"))
    assert dec.allowed is False
    rejected = {v.field for v in dec.rejected()}
    assert rejected == {"entry"}


# --- v2 schema --------------------------------------------------------------

def _deal_v2():
    return {
        "schema": "afb.deal.v2",
        "deal_id": "deal-y:bf1",
        "revision": 1,
        "target": _deal_v1()["target"],
        "direction": "long",
        "entry": [
            {"percent": "100",
             "condition": {"node_type": "event", "id": "e1", "op": "above",
                           "left": {"source": "price", "field": "last"}, "right": {"const": "100"}}},
        ],
        "stop_loss": [{"percent": "100", "condition": {
            "node_type": "event", "id": "sl", "op": "below",
            "left": {"source": "price", "field": "last"}, "right": {"const": "95"}}}],
        "take_profit": [],
        "sizing": {"mode": "lots", "value": "10"},
    }


def test_v2_stop_loss_change_detected_and_allowed_while_holding():
    d = _deal_v2()
    new = copy.deepcopy(d)
    new["stop_loss"][0]["condition"]["right"]["const"] = "96"
    dec = evaluate_amend(d, new, _ctx("active", "holding"))
    assert dec.allowed is True
    assert {v.field for v in dec.changed()} == {"stop_loss"}


def test_v2_entry_change_denied_while_holding():
    d = _deal_v2()
    new = copy.deepcopy(d)
    new["entry"][0]["condition"]["right"]["const"] = "101"
    assert is_amend_allowed(d, new, _ctx("active", "holding")) is False


@pytest.mark.parametrize("phase,allowed", [
    ("awaiting_entry", True), ("entry_working", True),
    ("holding", False), ("exit_working", False),
])
def test_v2_direction_by_phase(phase, allowed):
    """direction (long/short) is deal-level in v2 (no per-leg side) but is
    governed by the same "side" amend-matrix row as v1's entry.side."""
    d = _deal_v2()
    new = copy.deepcopy(d)
    new["direction"] = "short"
    dec = evaluate_amend(d, new, _ctx("active", phase))
    assert dec.allowed is allowed
    assert {v.field for v in dec.changed()} == {"side"}


# --- v2 right-expression conditions -----------------------------------------
# afb.deal.v2 conditions may compare an indicator/dataset expression against
# another expression instead of a plain `const` — the matrix-governed fields
# must detect that as a change (and gate it by phase) exactly like a const edit.

def test_v2_stop_loss_right_expression_change_detected_and_gated():
    d = _deal_v2()
    d["stop_loss"][0]["condition"] = {
        "node_type": "event", "id": "sl", "op": "below",
        "left": {"source": "indicator", "type": "wma"},
        "right": {"const": "95"},
    }
    new = copy.deepcopy(d)
    new["stop_loss"][0]["condition"]["right"] = {"source": "indicator", "type": "kama"}

    dec_holding = evaluate_amend(d, new, _ctx("active", "holding"))
    assert dec_holding.allowed is True
    assert {v.field for v in dec_holding.changed()} == {"stop_loss"}

    dec_terminal = evaluate_amend(d, new, _ctx("closed", "idle"))
    assert dec_terminal.allowed is False
    assert "stop_loss" in {v.field for v in dec_terminal.rejected()}


def test_v2_entry_right_expression_change_denied_while_holding():
    d = _deal_v2()
    d["entry"][0]["condition"] = {
        "node_type": "event", "id": "e1", "op": "above",
        "left": {"source": "dataset", "field": "x"},
        "right": {"const": "100"},
    }
    new = copy.deepcopy(d)
    new["entry"][0]["condition"]["right"] = {"source": "dataset", "field": "y"}
    assert is_amend_allowed(d, new, _ctx("active", "holding")) is False
    assert is_amend_allowed(d, new, _ctx("active", "awaiting_entry")) is True
