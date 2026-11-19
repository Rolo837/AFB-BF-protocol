"""payloads/dataset.update.json and dataset.subscribe.json — dataset_id vocabulary
(market.v2 registry sources; `orders` kept until legacy removal)."""
from __future__ import annotations

import copy
import json

import pytest

from conftest import EXAMPLES, SPEC_SCHEMAS

_UPDATE = SPEC_SCHEMAS / "payloads" / "dataset.update.json"
_SUBSCRIBE = SPEC_SCHEMAS / "payloads" / "dataset.subscribe.json"


def _validator(path, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": json.loads(path.read_text())["$id"]}, registry=registry)


def _record(dataset_id="depth", **current):
    return {
        "dataset_id": dataset_id,
        "instrument": {"exchange": "MISX", "board": "TQBR", "ticker": "SBER", "instrument_key": "MISX:TQBR:SBER"},
        "as_of": "2026-07-25T10:35:00+03:00",
        "stale_after_sec": 900,
        "current": current or {"bid_depth": 1.0, "offer_depth": 2.0, "delta": -1.0},
    }


@pytest.mark.parametrize("dataset_id", ["positions", "orders", "hhi", "trades", "depth", "obstats"])
def test_dataset_update_dataset_ids(registry, dataset_id):
    _validator(_UPDATE, registry).validate({"datasets": [_record(dataset_id)]})


def test_dataset_update_unknown_id_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(_UPDATE, registry).validate({"datasets": [_record("volume")]})


def test_dataset_update_example_payload(registry):
    payload = json.loads((EXAMPLES / "_payloads" / "dataset.update.json").read_text())
    _validator(_UPDATE, registry).validate(payload)
    ids = {r["dataset_id"] for r in payload["datasets"]}
    assert {"positions", "depth"} <= ids
    positions = next(r for r in payload["datasets"] if r["dataset_id"] == "positions")
    assert {"yur_long", "yur_short", "yur_net"} <= set(positions["current"])


@pytest.mark.parametrize("dataset_id", ["depth", "obstats"])
def test_dataset_subscribe_new_ids(registry, dataset_id):
    doc = {"subscriptions": [{"dataset_id": dataset_id, "instrument": {"exchange": "MISX", "board": "TQBR", "ticker": "SBER"}}]}
    _validator(_SUBSCRIBE, registry).validate(copy.deepcopy(doc))
