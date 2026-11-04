"""afbws/instrument.channel.v2.json — one schema id per message, push without request_id.
Validated as dict literals against the channel schema's $defs and the shipped examples."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/instrument.channel.v2.json"
EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "instrument_channel_v2"


def _validator(registry, def_name: str | None = None):
    from jsonschema import Draft202012Validator

    ref = ID if def_name is None else f"{ID}#/$defs/{def_name}"
    return Draft202012Validator({"$ref": ref}, registry=registry)


def _msg(op: str, **extra):
    return {"channel": "instrument", "schema": f"afbws.instrument.{op}.v2", **extra}


def _bad(v, doc):
    with pytest.raises(Exception):
        v.validate(doc)


_SET = {"id": "p1", "name": "Мои", "type": "instrument", "visibility": "personal", "instrument_keys": ["MISX:TQBR:SBER"]}
_NOTICE = {"instrument_key": "MISX:RFUD:SiZ6", "ticker": "SiZ6", "expiration": "2026-12-15", "days_left": 5,
           "usage": {"alarms": 0, "primitives": 0, "sets": 1, "favorites": 0}, "candidates": []}


def test_capability_id_declared():
    from afb_bf_protocol import INSTRUMENT_CHANNEL_V2

    assert INSTRUMENT_CHANNEL_V2 == "afbws.instrument.channel.v2"


def test_examples_validate(registry):
    root = _validator(registry)
    files = sorted(EXAMPLES.glob("*.json"))
    assert len(files) >= 18
    for path in files:
        root.validate(json.loads(path.read_text(encoding="utf-8")))


def test_catalog_request_and_response(registry):
    v = _validator(registry, "catalog")
    v.validate(_msg("catalog", request_id="r1"))
    v.validate(_msg("catalog", request_id="r1", revision=1, user_revision=0, collections=[], sets=[_SET], assets=[], listings=[], derivatives=[]))
    _bad(v, _msg("catalog", request_id="r1", revision=1))  # partial response
    _bad(v, _msg("catalog", request_id="r1", extra=1))


def test_sets_request_response_and_rules(registry):
    v = _validator(registry, "sets")
    v.validate(_msg("sets", request_id="r", user_revision=1, sets=[{"id": "p1", "name": "A"}], remove_sets=["x"]))
    v.validate(_msg("sets", request_id="r", catalog_revision=2, sets=[{"id": "g1", "name": "G", "visibility": "guest", "type": "asset", "asset_ids": ["a1"]}]))
    v.validate(_msg("sets", request_id="r", applied=True, user_revision=1, catalog_revision=2, sets=[_SET]))
    # mixed composition lists, asset set with instrument_keys, unknown visibility, no id
    _bad(v, _msg("sets", request_id="r", sets=[{"id": "a", "name": "A", "asset_ids": ["a1"], "instrument_keys": ["MISX:TQBR:SBER"]}]))
    _bad(v, _msg("sets", request_id="r", sets=[{"id": "a", "name": "A", "type": "asset", "instrument_keys": ["MISX:TQBR:SBER"]}]))
    _bad(v, _msg("sets", request_id="r", sets=[{"id": "a", "name": "A", "visibility": "admin"}]))
    _bad(v, _msg("sets", request_id="r", sets=[{"name": "A"}]))
    # a response must carry everything; the request must not claim `applied`
    _bad(v, _msg("sets", request_id="r", applied=True, sets=[_SET]))
    _bad(v, _msg("sets", applied=True, user_revision=1, catalog_revision=2, sets=[_SET]))
    _bad(v, _msg("sets", request_id="r", set_members=[]))  # no v1 leftovers


def test_favorites_and_paint(registry):
    v = _validator(registry, "favorites")
    v.validate(_msg("favorites", request_id="r"))
    v.validate(_msg("favorites", request_id="r", favorites=[{"kind": "asset", "key": "a1", "color": "teal"}]))
    _bad(v, _msg("favorites", request_id="r", favorites=[{"kind": "asset", "key": "a1", "color": "pinkish"}]))
    p = _validator(registry, "paint")
    p.validate(_msg("paint", request_id="r", mark=[{"kind": "instrument", "key": "MISX:TQBR:SBER", "color": "red"}], order=[{"kind": "asset", "key": "a1"}]))
    p.validate(_msg("paint", request_id="r", marked=[], unmarked=[]))
    _bad(p, _msg("paint", request_id="r", mark=[{"kind": "ticker", "key": "SBER", "color": "red"}]))
    # bond is an ordinary instrument keyed by instrument_key; kind=bond does not exist
    bk = "MISX:TQCB:RU000A10A3Z4"
    v.validate(_msg("favorites", request_id="r", favorites=[{"kind": "instrument", "key": bk, "color": "green"}]))
    p.validate(_msg("paint", request_id="r", mark=[{"kind": "instrument", "key": bk, "color": "red"}],
                    unmark=[{"kind": "instrument", "key": bk}], order=[{"kind": "instrument", "key": bk}]))
    _bad(v, _msg("favorites", request_id="r", favorites=[{"kind": "bond", "key": bk, "color": "green"}]))
    _bad(p, _msg("paint", request_id="r", mark=[{"kind": "bond", "key": bk, "color": "red"}]))
    _bad(p, _msg("paint", request_id="r", unmark=[{"kind": "bond", "key": bk}]))
    _bad(p, _msg("paint", request_id="r", order=[{"kind": "bond", "key": bk}]))
    _bad(p, _msg("paint", request_id="r", marked=[{"kind": "bond", "key": bk, "color": "red"}]))


def test_expiration_is_request_response_and_push(registry):
    v = _validator(registry, "expiration")
    v.validate(_msg("expiration", request_id="r"))
    v.validate(_msg("expiration", request_id="r", items=[_NOTICE]))
    v.validate(_msg("expiration", items=[_NOTICE]))  # push: no request_id
    v.validate(_msg("expiration", items=[]))  # an empty push clears the card
    _bad(v, _msg("expiration"))
    _bad(v, _msg("expiration", items=[{**_NOTICE, "days_left": -1}]))


def test_replace(registry):
    v = _validator(registry, "replace")
    v.validate(_msg("replace", request_id="r", from_key="MISX:RFUD:SiZ6", to_key="MISX:RFUD:SiH7", kinds=["alarms"]))
    v.validate(_msg("replace", request_id="r", from_key="MISX:RFUD:SiZ6", to_key="MISX:RFUD:SiH7",
                    replaced={"alarms": 1, "primitives": 0, "sets": 0, "favorites": 0}, rejected=[], items=[]))
    _bad(v, _msg("replace", request_id="r", from_key="MISX:RFUD:SiZ6"))
    _bad(v, _msg("replace", request_id="r", from_key="MISX:RFUD:SiZ6", to_key="MISX:RFUD:SiH7", kinds=[]))
    _bad(v, _msg("replace", request_id="r", from_key="MISX:RFUD:SiZ6", to_key="MISX:RFUD:SiH7", replaced={"alarms": 1, "primitives": 0, "sets": 0, "favorites": 0}))


def test_detail_is_addressed_by_instrument_key_only(registry):
    v = _validator(registry, "detail")
    v.validate(_msg("detail", request_id="r", instrument_key="XNYM:futures:CL"))
    v.validate(_msg("detail", request_id="r", instrument_key="XNYM:futures:CL", accounts=[{"bf_id": "finam-1", "account_id": "A1"}]))
    _bad(v, _msg("detail", request_id="r", ticker="CL"))
    _bad(v, _msg("detail", request_id="r", instrument_key="XNYM:futures:CL", bf_id="finam-1"))
    _bad(v, _msg("detail", request_id="r", instrument_key="XNYM:futures:CL", accounts=[]))
    ok = {"bf_id": "b", "account_id": "A", "status": "ok", "scope": "account", "broker_instrument": {"tradable": True}}
    v.validate(_msg("detail", request_id="r", instrument_key="XNYM:futures:CL", items=[ok]))
    # ok without parameters / failed with parameters / failed without error
    _bad(v, _msg("detail", request_id="r", instrument_key="XNYM:futures:CL", items=[{**ok, "broker_instrument": None}]))
    _bad(v, _msg("detail", request_id="r", instrument_key="XNYM:futures:CL", items=[{"bf_id": "b", "account_id": "A", "status": "error"}]))
    _bad(v, _msg("detail", request_id="r", instrument_key="XNYM:futures:CL", items=[
        {"bf_id": "b", "account_id": "A", "status": "error", "error": {"code": "bf_offline", "message": "x"}, "broker_instrument": {}}]))
    # a response cannot echo accounts
    _bad(v, _msg("detail", request_id="r", instrument_key="XNYM:futures:CL", accounts=[{"bf_id": "b", "account_id": "A"}], items=[ok]))


def test_error(registry):
    v = _validator(registry, "error")
    v.validate(_msg("error", code="conflict", message="m", details={"user_revision": 3, "catalog_revision": 4}))
    v.validate(_msg("error", request_id="r", code="forbidden", message="m", details={"set_ids": ["g1"]}))
    _bad(v, _msg("error", code="bogus", message="m"))
    _bad(v, _msg("error", code="conflict", message="m", details={"tickers": ["SBER"]}))


def test_root_rejects_v1_schema_ids_and_other_channels(registry):
    root = _validator(registry)
    _bad(root, {"channel": "instrument", "schema": "afbws.instrument.user.request.v1", "request_id": "r"})
    _bad(root, {"channel": "instrument", "schema": "afbws.instrument.detail.request.v2", "request_id": "r"})
    _bad(root, {**_msg("catalog", request_id="r"), "channel": "catalog"})


_TRAITS = {"price_unit": "money", "charts": True, "primitives": True, "alarms": True, "datasets": True, "plans": True, "virtual_trading": True}
_CARD = {"instrument_key": "MISX:TQBR:SBER", "class": "stock", "mic": "MISX", "market": "stock", "ticker": "SBER", "name": "Сбербанк",
         "source": "moex", "lifecycle": "active", "archived_reason": None, "traits": _TRAITS}


def test_instrument_card_and_traits(registry):
    v = _validator(registry, "instrumentCard")
    v.validate(_CARD)
    v.validate({**_CARD, "class": "bond", "lifecycle": "archived", "archived_reason": "matured", "traits": {**_TRAITS, "price_unit": "percent_of_face", "charts": False}})
    for k in ("class", "lifecycle", "archived_reason", "traits"):
        _bad(v, {x: y for x, y in _CARD.items() if x != k})
    _bad(v, {**_CARD, "class": "etf"})
    _bad(v, {**_CARD, "lifecycle": "deleted"})
    _bad(v, {**_CARD, "traits": {k: v_ for k, v_ in _TRAITS.items() if k != "plans"}})
    _bad(v, {**_CARD, "traits": {**_TRAITS, "extra": True}})
    _bad(v, {**_CARD, "traits": {**_TRAITS, "price_unit": "points"}})


def test_lookup_request_response(registry):
    v = _validator(registry, "lookup")
    v.validate(_msg("lookup", request_id="r", instrument_keys=["MISX:TQBR:SBER", "MISX:TQCB:RU000A10A3Z4"]))
    v.validate(_msg("lookup", request_id="r", items=[_CARD], missing=[{"instrument_key": "MISX:TQBR:XX", "code": "not_found"}, {"instrument_key": "MISX:TQCB:B1", "code": "forbidden"}]))
    _bad(v, _msg("lookup", request_id="r", instrument_keys=[]))
    _bad(v, _msg("lookup", request_id="r", instrument_keys=["MISX:TQBR:SBER", "MISX:TQBR:SBER"]))
    _bad(v, _msg("lookup", request_id="r", instrument_keys=[f"MISX:TQBR:T{i}" for i in range(101)]))
    _bad(v, _msg("lookup", request_id="r", items=[_CARD]))  # partial response
    _bad(v, _msg("lookup", request_id="r", items=[], missing=[{"instrument_key": "MISX:TQBR:XX", "code": "archived"}]))
    _bad(v, _msg("lookup", instrument_keys=["MISX:TQBR:SBER"]))


def test_not_supported_error_code(registry):
    v = _validator(registry, "error")
    v.validate(_msg("error", request_id="r", code="not_supported", message="bond has no detail").copy() | {"schema": "afbws.instrument.error.v2"})
