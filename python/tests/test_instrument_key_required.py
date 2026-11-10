"""common.v1.json#/$defs/instrument vs #/$defs/instrumentAddress.

`instrument` is the object AFB forms (deal `target.instrument`, a
dataset.update record): the catalog `instrument_key` is its identity and is
mandatory; exchange/board/ticker is only the venue address. BF has no catalog
and does not know the key, so whatever BF forms itself must stay valid without
it — that is `instrumentAddress` (payloads/dataset.subscribe.json) and the
bf2afb payloads, none of which reference `instrument`.
"""
from __future__ import annotations

import copy
import json

import pytest

from afb_bf_protocol import MESSAGE_REGISTRY

from conftest import EXAMPLES, SPEC_SCHEMAS

BASE = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/"
_ADDRESS = {"exchange": "MISX", "board": "TQBR", "ticker": "SBER"}
_KEYED = {**_ADDRESS, "instrument_key": "MISX:TQBR:SBER"}


def _v(ref, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": BASE + ref}, registry=registry)


def _deal(instrument):
    return {
        "schema": "afb.deal.v2", "deal_id": "deal-1", "revision": 1,
        "target": {"bf_id": "bf-1", "broker": "finam", "instrument": instrument},
        "direction": "long",
        "entry": [{"condition": {"node_type": "event", "id": "e1", "left": {"source": "price"},
                                 "right": {"const": "300"}, "op": "touch"}}],
        "sizing": {"mode": "lots", "value": "1"},
    }


def _dataset_update(instrument):
    return {"datasets": [{"dataset_id": "hhi", "instrument": instrument, "as_of": "2026-07-25T10:35:00+03:00",
                          "stale_after_sec": 900, "current": {"hhi_agressive_buy": 0.08}}]}


def test_instrument_def_requires_key_and_venue_triple(registry):
    v = _v("common.v1.json#/$defs/instrument", registry)
    v.validate(_KEYED)
    v.validate({**_KEYED, "board": ""})  # a venue without boards still states the (empty) board
    for field in ("exchange", "board", "ticker", "instrument_key"):
        assert list(v.iter_errors({k: val for k, val in _KEYED.items() if k != field})), field
    assert list(v.iter_errors({**_KEYED, "instrument_key": ""}))


def test_instrument_address_def_has_no_key_requirement(registry):
    v = _v("common.v1.json#/$defs/instrumentAddress", registry)
    v.validate(_ADDRESS)
    v.validate(_KEYED)  # open object: extra fields are not rejected
    for field in ("exchange", "board", "ticker"):
        assert list(v.iter_errors({k: val for k, val in _ADDRESS.items() if k != field})), field


@pytest.mark.parametrize("name,wrap", [
    ("deal.publish", lambda deal: {"deal": deal}),
    ("deal.amend", lambda deal: {"deal_id": "deal-1", "base_revision": 1, "deal": {**deal, "revision": 2}}),
    ("broker.resolve_instrument", lambda deal: {"deal": deal}),
])
def test_afb2bf_deal_messages_require_instrument_key(name, wrap, registry):
    assert MESSAGE_REGISTRY[name].direction == "afb2bf"
    v = _v(f"payloads/{name}.json", registry)
    v.validate(wrap(_deal(_KEYED)))
    errors = list(v.iter_errors(wrap(_deal(_ADDRESS))))
    assert errors and any("instrument_key" in e.message for e in errors)


def test_dataset_update_requires_instrument_key(registry):
    assert MESSAGE_REGISTRY["dataset.update"].direction == "afb2bf"
    v = _v("payloads/dataset.update.json", registry)
    v.validate(_dataset_update(_KEYED))
    v.validate({"datasets": []})
    assert list(v.iter_errors(_dataset_update(_ADDRESS)))


def test_bf2afb_dataset_subscribe_valid_without_key(registry):
    """BF forms this message and does not know instrument_key."""
    assert MESSAGE_REGISTRY["dataset.subscribe"].direction == "bf2afb"
    v = _v("payloads/dataset.subscribe.json", registry)
    v.validate({"subscriptions": [{"dataset_id": "positions", "instrument": _ADDRESS}]})
    assert list(v.iter_errors({"subscriptions": [{"dataset_id": "positions", "instrument": {"ticker": "SBER"}}]}))


def test_no_bf2afb_payload_references_keyed_instrument():
    """Guard: a schema of a message BF sends must never pull in the keyed
    `instrument`/`target`/deal.v2 — BF code does not produce instrument_key."""
    for name, meta in MESSAGE_REGISTRY.items():
        if meta.direction != "bf2afb":
            continue
        path = SPEC_SCHEMAS / "payloads" / f"{name}.json"
        if not path.exists():
            continue
        text = path.read_text()
        for ref in ("#/$defs/instrument\"", "#/$defs/target\"", "deal.v2.json\""):
            assert ref not in text, (name, ref)


def test_bf2afb_fixtures_carry_no_instrument_key_and_stay_valid(registry):
    """Every committed BF-originated example (real BF wire data, see
    examples/README.md) validates as is, without the key anywhere."""
    checked = 0
    for pf in sorted((EXAMPLES / "_payloads").glob("*.json")):
        name = pf.stem.split("__", 1)[0]
        meta = MESSAGE_REGISTRY.get(name)
        if meta is None or meta.direction != "bf2afb":
            continue
        schema = SPEC_SCHEMAS / "payloads" / f"{name}.json"
        if not schema.exists():
            continue
        payload = json.loads(pf.read_text())
        assert "instrument_key" not in json.dumps(payload), pf.name
        _v(f"payloads/{name}.json", registry).validate(payload)
        checked += 1
    assert checked >= 10


def test_deal_fixture_without_key_is_rejected(registry):
    payload = json.loads((EXAMPLES / "_payloads" / "deal.publish.json").read_text())
    v = _v("payloads/deal.publish.json", registry)
    v.validate(payload)
    assert payload["deal"]["target"]["instrument"]["exchange"] == "MISX"
    broken = copy.deepcopy(payload)
    del broken["deal"]["target"]["instrument"]["instrument_key"]
    assert list(v.iter_errors(broken))
