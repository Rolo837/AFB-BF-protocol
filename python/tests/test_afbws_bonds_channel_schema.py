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


_TRADE = {"trade_id": "t1", "instrument_key": "MISX:TQOB:SU26238RMFS4", "trade_date": "2026-10-15", "quantity": 10, "price_pct": 97.5}
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
    assert not [f for f in files if f.name.startswith('copy.')]
    for path in files:
        root.validate(json.loads(path.read_text(encoding="utf-8")))


def test_every_message_has_a_distinct_schema_const():
    doc = json.loads(SCHEMA_PATH.read_text())
    consts = []
    for ref in doc["oneOf"]:
        d = doc["$defs"][ref["$ref"].split("/")[-1]]
        consts.append(d["properties"]["schema"]["const"])
    assert len(consts) == len(set(consts)) == 13
    assert "afbws.bonds.error.v1" in consts


def test_search(registry):
    v = _validator(registry, "search")
    v.validate(_msg("search", request_id="r"))
    v.validate(_msg("search", request_id="r", query="ОФ", sort="yield", sort_direction="desc", limit=100, offset=0))
    for srt in ("name", "matdate", "yield"):
        for d in ("asc", "desc"):
            v.validate(_msg("search", request_id="r", sort=srt, sort_direction=d))
    v.validate(_msg("search", request_id="r", offset=250))
    v.validate(_ex("search.response"))
    _bad(v, _msg("search", request_id="r", cursor="abc"))  # no cursors
    _bad(v, _msg("search", request_id="r", offset=-1))
    _bad(v, _msg("search", request_id="r", limit=0))
    resp = _ex("search.response")
    del resp["total"]
    _bad(v, resp)  # total is required in a response
    resp = _ex("search.response")
    del resp["offset"]
    _bad(v, resp)
    resp = _ex("search.response")
    resp["next_cursor"] = None
    _bad(v, resp)
    _bad(v, _msg("search", request_id="r", query="О"))  # < 2 chars
    _bad(v, _msg("search", request_id="r", limit=101))
    _bad(v, _msg("search", request_id="r", sort="price"))
    _bad(v, _msg("search", request_id="r", sort="coupon"))  # removed
    _bad(v, _msg("search", request_id="r", sort_direction="up"))
    _bad(v, _msg("search", request_id="r", sort_direction=None))
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


def test_bond_card_passport_and_emitter_block(registry):
    v = _validator(registry, "bondMsg")
    resp = _ex("bond.response")
    # the card carries the issuer ONLY as one `emitter` object, not as flat emitter_* fields
    assert not [k for k in resp["bond"] if k.startswith("emitter_")]
    v.validate(resp)
    v.validate(_ex("bond_floater.response"))
    for field, value in (("emitter_id", 1), ("emitter_title", "Минфин России"), ("emitter_inn", "7710168360")):
        resp = _ex("bond.response")
        resp["bond"][field] = value
        _bad(v, resp)
    for field in ("coupon_kind", "redemption_kind", "liquidity", "emitter", "current_yield", "is_collateral", "passport_at"):
        resp = _ex("bond.response")
        del resp["bond"][field]
        _bad(v, resp)
    resp = _ex("bond.response")
    resp["bond"]["emitter"] = None
    resp["bond"]["liquidity"] = None
    v.validate(resp)
    resp["bond"]["coupon_kind"] = "floating"
    _bad(v, resp)
    resp = _ex("bond.response")
    resp["bond"]["emitter"]["rating_group"] = "AAAA"
    _bad(v, resp)
    resp = _ex("bond.response")
    del resp["schedule"]["coupons"][0]["projected"]
    _bad(v, resp)


def test_market_block_nullable(registry):
    v = _validator(registry, "bondRow")
    row = _ex("search.response")["items"][0]
    v.validate(row)
    v.validate({**row, "market": None})
    _bad(v, {**row, "market": {**row["market"], "ytm_kind": "ytc"}})
    _bad(v, {**row, "category": "unknown"})


def test_bond_row_name_replaces_isin_and_emitter(registry):
    v = _validator(registry, "bondRow")
    row = _ex("search.response")["items"][0]
    assert "isin" not in row and "emitter_title" not in row
    v.validate({**row, "name": None})
    no_name = {k: x for k, x in row.items() if k != "name"}
    _bad(v, no_name)
    _bad(v, {**row, "isin": "RU000A1038V6"})
    _bad(v, {**row, "emitter_title": "Минфин России"})


def test_bond_row_coupon_kind_and_spread(registry):
    v = _validator(registry, "bondRow")
    row = _ex("search.response")["items"][0]
    assert row["coupon_kind"] == "fixed" and row["coupon_spread_pct"] is None
    v.validate({**row, "coupon_kind": "key_rate", "coupon_percent": None, "coupon_spread_pct": 3.5})
    v.validate({**row, "coupon_kind": "unknown"})
    for key in ("coupon_kind", "coupon_spread_pct"):
        _bad(v, {k: x for k, x in row.items() if k != key})
    _bad(v, {**row, "coupon_kind": "floating"})
    _bad(v, {**row, "coupon_spread_pct": "3.5"})
    _bad(v, {**row, "coupon_benchmark": "RREFKEYR"})  # base code is not in the row
    for name in ("portfolios.response", "portfolios.push", "portfolios_set.response"):
        for item in _ex(name)["bonds"]:
            v.validate(item)
            assert "coupon_kind" in item and "coupon_spread_pct" in item
    card = _ex("bond.response")["bond"]
    assert {"coupon_kind", "coupon_spread_pct"} <= card.keys()
    _validator(registry, "bond").validate(card)


def test_portfolios_list_request_response_push(registry):
    v = _validator(registry, "portfolios")
    v.validate(_ex("portfolios.request"))
    v.validate(_ex("portfolios.response"))
    v.validate(_ex("portfolios.push"))
    _bad(v, _msg("portfolios"))  # neither request nor push
    _bad(v, _msg("portfolios", request_id="r", portfolios=[{**_REF, "visibility": "admin"}], bonds=[]))
    resp = _ex("portfolios.response")
    assert "summary" not in resp["portfolios"][0] and isinstance(resp["portfolios"][0]["instrument_keys"], list)
    for key in ("bonds", "portfolios"):
        broken = _ex("portfolios.response")
        del broken[key]
        _bad(v, broken)  # a response carries both
    push = _ex("portfolios.push")
    del push["bonds"]
    _bad(v, push)
    v.validate(_msg("portfolios", portfolios=[], bonds=[]))  # empty list push
    v.validate(_msg("portfolios", request_id="r", portfolios=[{**_REF, "instrument_keys": []}], bonds=[]))  # empty portfolio
    ref = _validator(registry, "portfolioRef")
    ref.validate(_REF)
    no_keys = {k: x for k, x in _REF.items() if k != "instrument_keys"}
    _bad(ref, no_keys)
    _bad(ref, {**_REF, "summary": {"market_value_rub": None, "ytm": None, "duration_days": None, "positions": 0}})
    _bad(ref, {**_REF, "instrument_keys": ["A", "A"]})
    _bad(ref, {**_REF, "instrument_keys": [f"S{i}" for i in range(201)]})
    ref.validate({**_REF, "instrument_keys": [f"S{i}" for i in range(200)]})
    _bad(ref, {**_REF, "instrument_keys": [""]})


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
    assert "summary" not in _ex("portfolio.response")["portfolio"]
    # a bond of the composition without purchases: purchase-based fields are null
    resp = _ex("portfolio.response")
    row = resp["positions"][0]
    row.update({"quantity": None, "avg_price_pct": None, "invested": None, "market_value": None,
                "market_value_rub": None, "current_yield": None, "ytm_purchase": None, "received": None,
                "flags": ["no_trades"]})
    v.validate(resp)
    resp["portfolio"]["summary"] = {"market_value_rub": None, "ytm": None, "duration_days": None, "positions": 0}
    _bad(v, resp)


def test_portfolios_set(registry):
    v = _validator(registry, "portfoliosSet")
    v.validate(_ex("portfolios_set.request"))
    v.validate(_ex("portfolios_set.response"))
    v.validate(_msg("portfolios.set", request_id="r", remove=["x"]))
    _bad(v, _msg("portfolios.set", request_id="r"))  # nothing to do
    r = _ex("portfolios_set.request")
    assert all("instrument_keys" in x for x in r["portfolios"])
    v.validate(_msg("portfolios.set", request_id="r", portfolios=[{"id": "a", "name": "A", "instrument_keys": []}]))
    v.validate(_msg("portfolios.set", request_id="r", portfolios=[{"id": "a", "name": "A"}]))  # composition untouched
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[{"id": "a", "name": "A", "instrument_keys": [f"S{i}" for i in range(201)]}]))
    v.validate(_msg("portfolios.set", request_id="r", portfolios=[{"id": "a", "name": "A", "instrument_keys": ["X", "X"]}]))  # duplicates are dropped by the backend
    for key in ("bonds", "portfolios"):
        broken = _ex("portfolios_set.response")
        del broken[key]
        _bad(v, broken)
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[{"id": "a"}]))  # no name
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[{"id": "a", "name": "A", "own": True}]))
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[_REF], rejected=[]) | {"portfolios": [{"id": "a", "name": "A"}]})
    _bad(v, _msg("portfolios.set", request_id="r", portfolios=[_REF]) | {"remove": []} | {"portfolios": [_REF]})  # edit item with response fields


def test_trades_set(registry):
    v = _validator(registry, "tradesSet")
    v.validate(_ex("trades_set.request"))
    v.validate(_ex("trades_set.response"))
    assert _ex("trades_set.response")["instrument_keys"]
    resp = _ex("trades_set.response")
    del resp["instrument_keys"]
    _bad(v, resp)
    v.validate(_msg("trades.set", request_id="r", portfolio_id="p", upsert=[_TRADE]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p"))
    _bad(v, _msg("trades.set", request_id="r", upsert=[_TRADE]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "quantity": 0}]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "price_pct": 0}]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "trade_date": "02.11.2026"}]))
    _bad(v, _msg("trades.set", request_id="r", portfolio_id="p", upsert=[{**_TRADE, "extra": 1}]))
    v2 = _validator(registry, "trade")
    v2.validate({**_TRADE, "quantity": -5, "accrued_int": 1.2, "commission": 0})


def test_copy_is_gone(registry):
    doc = json.loads(SCHEMA_PATH.read_text())
    assert "copy" not in doc["$defs"] and "skipped" not in doc["$defs"] and "portfolioSummary" not in doc["$defs"]
    assert "afbws.bonds.copy.v1" not in SCHEMA_PATH.read_text()
    _bad(_validator(registry), _msg("copy", request_id="r", source_id="g", id="p", name="N", amount_rub=1))


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


def test_bond_identity_is_instrument_key_only(registry):
    """R3: `secid` is a display attribute; every identifier on the wire is `instrument_key`."""
    doc = json.loads(SCHEMA_PATH.read_text())
    defs = doc["$defs"]
    for name in ("bondRow", "bond", "position"):
        assert "instrument_key" in defs[name]["required"], name
        assert "secid" in defs[name]["properties"], name  # display field is kept
    for name in ("trade", "payment", "signal", "event"):
        assert "instrument_key" in defs[name]["required"], name
        assert "secid" not in defs[name]["properties"], name
    for name in ("portfolioRef", "portfolioEdit", "tradesSet"):
        assert "secids" not in defs[name]["properties"], name
        assert "instrument_keys" in defs[name]["properties"], name
    assert "secids" not in json.dumps(doc)
    # key is the shared instrumentKey def, no local pattern
    assert defs["trade"]["properties"]["instrument_key"]["$ref"] == "common.v1.json#/$defs/instrumentKey"
    row = _ex("search.response")["items"][0]
    v = _validator(registry, "search")
    broken = {k: x for k, x in row.items() if k != "instrument_key"}
    resp = _ex("search.response")
    resp["items"] = [broken]
    _bad(v, resp)  # a row without the key is not valid even with secid
    only_secid_trade = {k: x for k, x in _TRADE.items() if k != "instrument_key"} | {"secid": "SU26238RMFS4"}
    _bad(_validator(registry, "tradesSet"), _msg("trades.set", request_id="r", portfolio_id="p", upsert=[only_secid_trade]))
    _bad(_validator(registry, "bondMsg"), _msg("bond", request_id="r", secid="SU26238RMFS4"))
    _validator(registry, "bondMsg").validate(_msg("bond", request_id="r", instrument_key="MISX:TQOB:SU26238RMFS4"))


def test_projected_flag_and_payment(registry):
    v = _validator(registry, "portfolio")
    resp = _ex("portfolio.response")
    resp["flags"] = ["float_assumed", "float_projected"]
    resp["positions"][0]["flags"] = ["float_projected"]
    resp["payments"][0]["projected"] = True
    v.validate(resp)
    del resp["payments"][0]["projected"]
    _bad(v, resp)


def test_portfolio_breakdown_and_calendar(registry):
    v = _validator(registry, "portfolio")
    for name in ("portfolio.response", "portfolio.push"):
        v.validate(_ex(name))
        for key in ("breakdown", "calendar"):
            broken = _ex(name)
            del broken[key]
            _bad(v, broken)
    resp = _ex("portfolio.response")
    resp["breakdown"] = {k: [] for k in resp["breakdown"]}
    resp["calendar"] = []
    v.validate(resp)
    resp["breakdown"]["by_rating"] = [{"key": "A", "market_value_rub": 1, "share": 1, "ytm": None, "positions": 1}]  # label optional
    v.validate(resp)
    resp["breakdown"]["by_rating"][0]["share"] = 1.5
    _bad(v, resp)
    resp = _ex("portfolio.response")
    del resp["breakdown"]["by_emitter"]
    _bad(v, resp)
    resp = _ex("portfolio.response")
    resp["breakdown"]["by_year"] = []
    _bad(v, resp)
    resp = _ex("portfolio.response")
    resp["calendar"][0]["month"] = "2026-1"
    _bad(v, resp)


def _screener_columns():
    return json.loads(SCHEMA_PATH.read_text())["$defs"]["screenerColumns"]["prefixItems"]


def test_screener(registry):
    v = _validator(registry, "screener")
    v.validate(_ex("screener.request"))
    v.validate(_ex("screener.response"))
    v.validate(_ex("screener.push"))
    v.validate(_msg("screener", request_id="r"))  # no filters = all defaults
    v.validate(_msg("screener", request_id="r", filters={}))
    assert [c["const"] for c in _screener_columns()][:3] == ["instrument_key", "secid", "shortname"]
    assert "request_id" not in _ex("screener.push")
    _bad(v, _msg("screener"))  # neither request nor push
    for key in ("asof", "liquidity_days", "total", "emitters", "columns"):  # without `rows` it is a request
        broken = _ex("screener.response")
        del broken[key]
        _bad(v, broken)
    push = _ex("screener.push")
    del push["rows"]
    _bad(v, push)  # a push without request_id carries rows
    bad_filters = [
        {"query": "О"}, {"rating_min": "AAAA"}, {"coupon_kinds": ["floating"]}, {"ytm": {"min": "1"}},
        {"ytm": {"lo": 1}}, {"amortization": "yes"}, {"liquidity_classes": [3]}, {"min_value_avg": -1},
        {"unknown": 1}, {"include_default": "no"}, {"categories": ["cb"]}, {"emitter_id": "1"},
    ]
    for f in bad_filters:
        _bad(v, _msg("screener", request_id="r", filters=f))
    # columns: fixed list and order
    resp = _ex("screener.response")
    resp["columns"] = list(reversed(resp["columns"]))
    _bad(v, resp)
    resp = _ex("screener.response")
    resp["columns"] = resp["columns"][:-1]
    _bad(v, resp)
    # rows: typed per column and of full width
    resp = _ex("screener.response")
    resp["rows"][0] = resp["rows"][0][:-1]
    _bad(v, resp)
    resp = _ex("screener.response")
    resp["rows"][0][resp["columns"].index("coupon_kind")] = "floating"
    _bad(v, resp)
    resp = _ex("screener.response")
    resp["rows"][0][resp["columns"].index("high_risk")] = None
    _bad(v, resp)
    resp = _ex("screener.response")
    resp["emitters"]["abc"] = {"title": "X", "rating_group": None}
    _bad(v, resp)
    resp = _ex("screener.response")
    resp["emitters"]["1234"]["rating_group"] = "ZZ"
    _bad(v, resp)
    resp = _ex("screener.response")
    resp["emitters"]["1234"]["rating_group"] = None
    resp["rows"] = []
    resp["total"] = 0
    v.validate(resp)


def test_emitter(registry):
    v = _validator(registry, "emitter")
    v.validate(_ex("emitter.request"))
    v.validate(_ex("emitter.response"))
    _bad(v, _msg("emitter", request_id="r"))  # no emitter_id
    _bad(v, _msg("emitter", request_id="r", emitter_id="1"))
    for key in ("columns", "rows"):  # without `emitter` it is a request
        broken = _ex("emitter.response")
        del broken[key]
        _bad(v, broken)
    resp = _ex("emitter.response")
    resp["emitter"]["outstanding_rub"] = None  # no FX rate
    resp["emitter"]["rating_group"] = None
    resp["emitter"]["inn"] = None
    v.validate(resp)
    del resp["emitter"]["bonds_count"]
    _bad(v, resp)
    # the same columns as the screener
    assert _ex("emitter.response")["columns"] == _ex("screener.response")["columns"]


def test_rates_and_rates_set(registry):
    v = _validator(registry, "rates")
    v.validate(_ex("rates.request"))
    v.validate(_ex("rates.response"))
    v.validate(_ex("rates.push"))
    _bad(v, _msg("rates"))  # neither request nor push
    resp = _ex("rates.response")
    resp["items"][0]["title"] = None
    _bad(v, resp)
    resp = _ex("rates.response")
    del resp["items"][0]["updated_at"]
    _bad(v, resp)
    s = _validator(registry, "ratesSet")
    s.validate(_ex("rates_set.request"))
    s.validate(_ex("rates_set.response"))
    _bad(s, _msg("rates.set", request_id="r"))  # nothing to do
    _bad(s, _msg("rates.set", request_id="r", items=[]))
    _bad(s, _msg("rates.set", request_id="r", items=[{"code": "RUONIA"}]))  # value_pct is required (null clears)
    _bad(s, _msg("rates.set", request_id="r", items=[{"code": "RUONIA", "value_pct": "7"}]))
    _bad(s, _msg("rates.set", request_id="r", items=[{"code": "", "value_pct": 7}]))
    s.validate(_msg("rates.set", request_id="r", items=[{"code": "RUONIA", "value_pct": 7.25}]))
    s.validate(_msg("rates.set", request_id="r", items=[{"code": "RUONIA", "value_pct": None}]))
    resp = _ex("rates_set.response")
    del resp["rejected"]
    _bad(s, resp)  # the request-shaped items would not satisfy rateItem either
    resp = _ex("rates_set.response")
    resp["rejected"] = []
    s.validate(resp)
    resp["rejected"] = [{"code": "X", "reason": "boom"}]
    _bad(s, resp)
    resp["rejected"] = [{"code": "X", "reason": "invalid_value", "message": "ставка вне диапазона"}]
    s.validate(resp)


def test_portfolio_account_id_optional(registry):
    ref = _validator(registry, "portfolioRef")
    ref.validate(_REF)  # old payload without account_id
    ref.validate({**_REF, "account_id": "bond:p-1"})
    ref.validate({**_REF, "account_id": None})
    _bad(ref, {**_REF, "account_id": 5})
    assert "account_id" not in json.loads(SCHEMA_PATH.read_text())["$defs"]["portfolioRef"]["required"]


def test_rejection_reasons(registry):
    pr = _validator(registry, "portfolioRejection")
    base = {"id": "p", "code": "validation_error", "message": "m"}
    pr.validate(base)
    for r in ("no_last_price", "no_fx"):
        pr.validate({**base, "reason": r})
    _bad(pr, {**base, "reason": "x"})
    tr = _validator(registry, "tradeRejection")
    base = {"trade_id": "t", "code": "validation_error", "message": "m"}
    tr.validate(base)
    tr.validate({**base, "reason": "deprecated"})
    _bad(tr, {**base, "reason": "x"})


def test_account_portfolio_example_compat_fields():
    d = _ex("portfolio.response.account")
    assert d["portfolio"]["account_id"] == "bond:p-1"
    assert d["trades"] == [] and d["series"]["rows"] == [] and d["totals"]["xirr"] is None
    # old examples without account_id stay in the set unchanged
    assert "account_id" not in _ex("portfolio.response")["portfolio"]
