"""afbws/bonds.channel.v1.json — one schema id per message, push without request_id.
Validated as dict literals against the channel schema's $defs and the shipped examples."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/bonds.channel.v1.json"
ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "spec" / "schemas" / "afbws" / "bonds.channel.v1.json"
EXAMPLES = ROOT / "examples" / "bonds_channel_v1"


def _validator(registry, def_name: str | None = None):
    from jsonschema import Draft202012Validator

    ref = ID if def_name is None else f"{ID}#/$defs/{def_name}"
    return Draft202012Validator({"$ref": ref}, registry=registry)


def _msg(op: str, **extra):
    return {"channel": "bonds", "schema": f"afbws.bonds.{op}.v1", **extra}


def _bad(v, doc):
    with pytest.raises(Exception):
        v.validate(doc)


def _ex(name: str):
    return json.loads((EXAMPLES / f"{name}.json").read_text(encoding="utf-8"))


_TRADE = {"trade_id": "t1", "secid": "SU26238RMFS4", "trade_date": "2026-10-15", "quantity": 10, "price_pct": 97.5}
_REF = _ex("portfolios.response")["portfolios"][0]


def test_capability_id_declared():
    from afb_bf_protocol import BONDS_CHANNEL_V1

    assert BONDS_CHANNEL_V1 == "afbws.bonds.channel.v1"
    assert json.loads(SCHEMA_PATH.read_text())["x-afbws-support-id"] == BONDS_CHANNEL_V1


def test_no_message_def_declares_a_type_property():
    doc = json.loads(SCHEMA_PATH.read_text())
    for name, d in doc["$defs"].items():
        assert "type" not in d.get("properties", {}), name


def test_examples_validate(registry):
    root = _validator(registry)
    files = sorted(EXAMPLES.glob("*.json"))
    assert len(files) >= 20
    for path in files:
        root.validate(json.loads(path.read_text(encoding="utf-8")))


def test_every_message_has_a_distinct_schema_const():
    doc = json.loads(SCHEMA_PATH.read_text())
    consts = []
    for ref in doc["oneOf"]:
        d = doc["$defs"][ref["$ref"].split("/")[-1]]
        consts.append(d["properties"]["schema"]["const"])
    assert len(consts) == len(set(consts)) == 10
    assert "afbws.bonds.error.v1" in consts


def test_search(registry):
    v = _validator(registry, "search")
    v.validate(_msg("search", request_id="r"))
    v.validate(_msg("search", request_id="r", query="ОФ", sort="coupon", limit=100, cursor="abc"))
    _bad(v, _msg("search", request_id="r", query="О"))  # < 2 chars
    _bad(v, _msg("search", request_id="r", limit=101))
    _bad(v, _msg("search", request_id="r", sort="price"))
    _bad(v, _msg("search", request_id="r", categories=["cb"]))
    _bad(v, _msg("search"))  # request_id required, no body
    _bad(v, _msg("search", request_id="r", items=[]))  # partial response


def test_bond_request_response(registry):
    v = _validator(registry, "bondMsg")
    v.validate(_ex("bond.request"))
    v.validate(_ex("bond.response"))
    _bad(v, _msg("bond", request_id="r"))
    resp = _ex("bond.response")
    del resp["history"]
    _bad(v, resp)
    resp = _ex("bond.response")
    resp["history"]["columns"] = ["date", "close"]
    _bad(v, resp)


def test_market_block_nullable(registry):
    v = _validator(registry, "bondRow")
    row = _ex("search.response")["items"][0]
    v.validate(row)
    v.validate({**row, "market": None})
    _bad(v, {**row, "market": {**row["market"], "ytm_kind": "ytc"}})
    _bad(v, {**row, "category": "unknown"})


def test_portfolios_list_request_response_push(registry):
    v = _validator(registry, "portfolios")
    v.validate(_ex("portfolios.request"))
    v.validate(_ex("portfolios.response"))
    v.validate(_ex("portfolios.push"))
    _bad(v, _msg("portfolios"))  # neither request nor push
    _bad(v, _msg("portfolios", request_id="r", portfolios=[{**_REF, "visibility": "admin"}]))


def test_portfolio_request_response_push(registry):
    v = _validator(registry, "portfolio")
    v.validate(_ex("portfolio.request"))
    v.validate(_ex("portfolio.response"))
    v.validate(_ex("portfolio.push"))
    _bad(v, _msg("portfolio", request_id="r"))  # no id
    push = _ex("portfolio.push")
    del push["totals"]
    _bad(v, push)
    resp = _ex("portfolio.response")
    resp["positions"][0]["flags"] = ["unknown_flag"]
    _bad(v, resp)


def test_portfolios_set(registry):
    v = _validator(registry, "portfoliosSet")
    v.validate(_ex("portfolios_set.request"))
    v.validate(_ex("portfolios_set.response"))
    v.validate(_msg("portfolios.set", request_id="r", remove=["x"]))
    _bad(v, _msg("portfolios.set", request_id="r"))  # nothing to do
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[{"id": "a"}]))  # no name
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[{"id": "a", "name": "A", "own": True}]))
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[_REF], rejected=[]) | {"portfolios": [{"id": "a", "name": "A"}]})
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[_REF]) | {"remove": []} | {"portfolios": [_REF]})  # edit item with response fields


def test_trades_set(registry):
    v = _validator(registry, "tradesSet")
    v.validate(_ex("trades_set.request"))
    v.validate(_ex("trades_set.response"))
    v.validate(_msg("trades.set", request_id="r", portfolio_id="p", upsert=[_TRADE]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p"))
    _bad(v, _msg("trades.set", request_id="r", upsert=[_TRADE]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "quantity": 0}]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "price_pct": 0}]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "trade_date": "02.11.2026"}]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "extra": 1}]))
    v2 = _validator(registry, "trade")
    v2.validate({**_TRADE, "quantity": -5, "accrued_int": 1.2, "commission": 0})


def test_copy(registry):
    v = _validator(registry, "copy")
    v.validate(_ex("copy.request"))
    v.validate(_ex("copy.response"))
    _bad(v, _msg("copy", request_id="r", source_id="g", id="p", name="N"))  # no amount
    _bad(v, _msg("copy", request_id="r", source_id="g", id="p", name="N", amount_rub=0))
    resp = _ex("copy.response")
    resp["skipped"][0]["reason"] = "other"
    _bad(v, resp)


def test_signals_and_events(registry):
    v = _validator(registry, "signals")
    v.validate(_ex("signals.request"))
    v.validate(_ex("signals.response"))
    v.validate(_ex("signals.push"))
    v.validate(_msg("signals", request_id="r"))
    _bad(v, _msg("signals", request_id="r", days=31))
    _bad(v, _msg("signals"))
    e = _validator(registry, "events")
    e.validate(_ex("events.request"))
    e.validate(_ex("events.response"))
    e.validate(_ex("events.push"))
    _bad(e, _msg("events"))
    bad = _ex("events.response")
    bad["items"][0]["kind"] = "coupon"
    _bad(e, bad)


@pytest.mark.parametrize("code", ["forbidden", "not_found", "invalid_schema", "validation_error", "internal_error", "unsupported_action"])
def test_error_valid(registry, code):
    _validator(registry, "error").validate(_msg("error", request_id="r", code=code, message="x"))


def test_error_unknown_code_rejected(registry):
    _bad(_validator(registry, "error"), _msg("error", code="boom", message="x"))


def test_root_dispatches_each_example(registry):
    root = _validator(registry)
    for path in sorted(EXAMPLES.glob("*.json")):
        root.validate(json.loads(path.read_text(encoding="utf-8")))
    _bad(root, _msg("reconcile", request_id="r"))
