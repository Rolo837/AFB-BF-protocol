"""Every example envelope validates against the envelope schema, and its payload
validates against the per-type payload schema."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES, SPEC_SCHEMAS

EXAMPLE_FILES = sorted(EXAMPLES.glob("*.json"))
assert EXAMPLE_FILES, "no example envelopes generated"

ENVELOPE_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/envelope.json"


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    from jsonschema import Draft202012Validator

    env = json.loads(path.read_text())

    envelope_schema = json.loads((SPEC_SCHEMAS / "envelope.json").read_text())
    Draft202012Validator(envelope_schema, registry=registry).validate(env)

    # A stem may carry a "__variant" suffix (e.g. deal.publish__v2) when a
    # message type needs more than one example; the payload schema is keyed by
    # the message type only (the part before "__").
    msg_type = path.stem.split("__", 1)[0]
    payload_schema_path = SPEC_SCHEMAS / "payloads" / f"{msg_type}.json"
    assert payload_schema_path.exists(), f"missing payload schema for {msg_type}"
    payload_schema = json.loads(payload_schema_path.read_text())
    Draft202012Validator(payload_schema, registry=registry).validate(env["payload"])


def test_legacy_entry_side_and_order_rejected_since_v2_0_0(registry):
    """v2.0.0 removed `entry.side` (legacy buy/sell — superseded by the
    deal-level `direction`) and `entry.order` (deprecated since 1.11.0, BF
    always ignored it) from afb.deal.v1. `direction` is now required."""
    from jsonschema import Draft202012Validator, ValidationError

    deal_schema = json.loads((SPEC_SCHEMAS / "deal.v1.json").read_text())
    deal = {
        "schema": "afb.deal.v1",
        "deal_id": "deal-legacy:bf1",
        "revision": 1,
        "target": {
            "bf_id": "bf1",
            "broker": "finam-arena",
            "instrument": {"exchange": "MOEX", "board": "TQBR", "ticker": "SBER"},
        },
        "entry": {
            "side": "buy",
            "condition": {
                "node_type": "event", "id": "e1", "op": "above",
                "left": {"source": "price", "field": "last"},
                "right": {"const": "100.5"},
            },
            "order": {"type": "market", "limit_offset_steps": 1, "time_in_force": "day"},
        },
        "sizing": {"mode": "lots", "value": "1"},
    }
    with pytest.raises(ValidationError):
        Draft202012Validator(deal_schema, registry=registry).validate(deal)

    deal["direction"] = "long"
    del deal["entry"]["side"]
    del deal["entry"]["order"]
    Draft202012Validator(deal_schema, registry=registry).validate(deal)  # does not raise
