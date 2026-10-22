"""Поля протокола из разбора deal-4ba6-4c7a-9517: deal_seq, definition_hash,
fills[].exchange_fee, broker.accounts[].broker_fees. Все поля необязательные —
старые payload'ы остаются валидными (аддитивная правка)."""
from __future__ import annotations

import pytest

BASE = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/"
HASH = "a" * 64


def _v(name, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": BASE + name + ".json"}, registry=registry)


def _deal():
    return {
        "schema": "afb.deal.v2", "deal_id": "deal-1", "revision": 1,
        "target": {"bf_id": "bf-1", "broker": "finam", "instrument": {"exchange": "MISX", "board": "TQBR", "ticker": "SBER", "market": "stock"}},
        "direction": "long",
        "entry": [{"condition": {"node_type": "event", "id": "e1", "left": {"source": "price"}, "right": {"const": "300"}, "op": "touch"}}],
        "sizing": {"mode": "lots", "value": "1"},
    }


@pytest.mark.parametrize("name", [
    "condition.triggered", "deal.status_changed", "order.created", "order.filled",
    "position.opened", "deal.positions_synced", "deal.snapshot",
])
def test_deal_seq_accepted_and_validated(name, registry):
    v = _v(name, registry)
    base = {"deal_id": "deal-1", "revision": 1, "status": "active", "order_id": "o1", "role": "entry", "side": "buy"}
    ok = {**base, "deal_seq": 14}
    assert not [e for e in v.iter_errors(ok) if list(e.path) == ["deal_seq"]]
    for bad in (0, -1, "14", 1.5):
        errs = [e for e in v.iter_errors({**base, "deal_seq": bad}) if list(e.path) == ["deal_seq"]]
        assert errs, (name, bad)


def test_deal_report_exchange_fee(registry):
    v = _v("deal.report", registry)
    report = {
        "deal_id": "deal-1", "revision": 2, "status": "closed", "deal_seq": 9,
        "fills": [
            {"trade_id": "t1", "order_id": "o1", "role": "entry", "side": "buy", "price": "58.23", "quantity": 5,
             "exchange_fee": {"value": "3.2", "currency": "RUB"}},
            {"trade_id": "t2", "order_id": "o2", "role": "stop_loss", "side": "sell", "price": "57.11", "quantity": 5},
        ],
    }
    v.validate(report)
    bad = {**report, "fills": [{**report["fills"][0], "exchange_fee": {"value": "3.2"}}]}
    assert list(v.iter_errors(bad))
    bad = {**report, "fills": [{**report["fills"][0], "exchange_fee": {"value": "3.2", "currency": "RUB", "kind": "x"}}]}
    assert list(v.iter_errors(bad))


def test_deal_report_old_payload_without_new_fields_still_valid(registry):
    _v("deal.report", registry).validate({
        "deal_id": "deal-1", "revision": 1, "status": "closed",
        "fills": [{"order_id": "o1", "role": "entry", "side": "buy"}],
    })


@pytest.mark.parametrize("name,extra", [
    ("deal.publish", {}),
    ("deal.amend", {"deal_id": "deal-1", "base_revision": 1}),
])
def test_definition_hash_in_publish_and_amend(name, extra, registry):
    v = _v(name, registry)
    deal = _deal()
    if name == "deal.amend":
        deal["revision"] = 2
    msg = {"deal": deal, **extra}
    v.validate(msg)
    v.validate({**msg, "definition_hash": HASH})
    for bad in ("xyz", "A" * 64, "a" * 63, 5):
        assert list(v.iter_errors({**msg, "definition_hash": bad})), bad


def test_resync_entries_accept_hash_and_seq(registry):
    req = _v("session.resync_request", registry)
    req.validate({"deals": {"d1": {"revision": 2, "status": "closed", "archived": False,
                                   "definition_hash": HASH, "deal_seq": 31}}})
    req.validate({"deals": {"d1": {"revision": 2, "status": "closed", "archived": False}}})  # старый BF
    resp = _v("session.resync_response", registry)
    resp.validate({"deals": {"d1": {"revision": 2, "status": "active", "archived": False,
                                    "definition_hash": HASH, "applied_deal_seq": 28}}})
    resp.validate({"deals": {"d1": {"revision": 2, "status": "active", "archived": False}}})  # старый AFB
    assert list(resp.iter_errors({"deals": {"d1": {"revision": 2, "status": "active", "archived": False,
                                                    "applied_deal_seq": -1}}}))


def test_broker_fees_window_in_accounts(registry):
    v = _v("broker.accounts", registry)
    acct = {"account_id": "1918978", "tradable": True, "readonly": False, "status": "ok",
            "equity": "42668.97", "cash": [{"currency": "RUB", "value": "42668.97"}], "positions": []}
    msg = {"default_account_id": "1918978", "as_of": "2026-10-22T10:00:00+03:00", "accounts": [acct]}
    v.validate(msg)  # без broker_fees — как раньше
    with_fees = {**msg, "accounts": [{**acct, "broker_fees": [
        {"date": "2026-10-21", "value": "2.25", "currency": "RUB", "transaction_id": "3465910153"},
        {"date": "2026-10-20", "value": "0", "currency": "RUB"},
    ]}]}
    v.validate(with_fees)
    for bad in (
        [{"date": "21.10.2026", "value": "2.25", "currency": "RUB"}],
        [{"date": "2026-10-21", "value": 2.25, "currency": "RUB"}],
        [{"date": "2026-10-21", "value": "2.25"}],
        [{"date": "2026-10-21", "value": "2.25", "currency": "RUB", "kind": "x"}],
    ):
        assert list(v.iter_errors({**msg, "accounts": [{**acct, "broker_fees": bad}]})), bad
