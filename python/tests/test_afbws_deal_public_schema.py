"""afbws/deal.public.v1.json — explicit allow-list projection of afb.deal.v1/v2
for the schema-first deal channel. Never a serialization of the persisted
DealState/deal_state.v2.json file: source_refs, status_history, event_journal,
raw orders/positions, observed, owner, archive_reason and legacy
source.kind/draft_id must all be rejected."""
from __future__ import annotations

import pytest

DEAL_PUBLIC_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/deal.public.v1.json"

_TARGET = {
    "bf_id": "bf-main",
    "broker": "finam",
    "instrument": {"exchange": "MOEX", "board": "TQBR", "ticker": "SBER"},
}

_GOOD_V1 = {
    "schema": "afb.deal.v1",
    "deal_id": "deal-1",
    "revision": 1,
    "target": _TARGET,
    "direction": "long",
    "entry": {"condition": {"node_type": "event", "op": "above", "left": {"source": "price", "field": "last"}, "right": {"const": "100"}}},
    "sizing": {"mode": "lots", "value": "1"},
    "source": {"tradeplan_id": "tp-1"},
}

_GOOD_V2 = {
    "schema": "afb.deal.v2",
    "deal_id": "deal-2",
    "revision": 1,
    "target": _TARGET,
    "direction": "long",
    "entry": [{"condition": {"node_type": "event", "op": "touch", "left": {"source": "price"}, "right": {"const": "100"}}}],
    "sizing": {"mode": "lots", "value": "1"},
    "source": {"tradeplan_id": "tp-2"},
}


def _validator(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": DEAL_PUBLIC_ID}, registry=registry)


def test_v1_valid(registry):
    _validator(registry).validate(_GOOD_V1)  # does not raise


def test_v2_valid(registry):
    _validator(registry).validate(_GOOD_V2)  # does not raise


def test_missing_source_rejected(registry):
    from jsonschema import ValidationError

    bad = {k: v for k, v in _GOOD_V1.items() if k != "source"}
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_source_without_tradeplan_id_rejected(registry):
    from jsonschema import ValidationError

    bad = {**_GOOD_V1, "source": {}}
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_legacy_source_kind_rejected(registry):
    """The old kind='tradeplan_draft' discriminator never appears in the
    public projection, even though it's still accepted (deprecated) on the
    AFB<->BF wire schema itself."""
    from jsonschema import ValidationError

    bad = {**_GOOD_V1, "source": {"tradeplan_id": "tp-1", "kind": "tradeplan_draft"}}
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_legacy_source_draft_id_rejected(registry):
    from jsonschema import ValidationError

    bad = {**_GOOD_V1, "source": {"tradeplan_id": "tp-1", "draft_id": "tp-1"}}
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_owner_rejected(registry):
    """owner (just {user_id}) is redundant — the caller already knows whose
    deal this is via ownership/RBAC — and must not leak into the public shape."""
    from jsonschema import ValidationError

    bad = {**_GOOD_V1, "owner": {"user_id": "u1"}}
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_archive_reason_rejected(registry):
    from jsonschema import ValidationError

    bad = {**_GOOD_V1, "archive_reason": "user request"}
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_compile_metadata_rejected(registry):
    """primitive_snapshot/compiled_at are AFB compile bookkeeping inside the
    wire schema's `source`, not part of the strict public source."""
    from jsonschema import ValidationError

    bad = {**_GOOD_V1, "source": {"tradeplan_id": "tp-1", "compiled_at": "2026-01-01T00:00:00Z"}}
    with pytest.raises(ValidationError):
        _validator(registry).validate(bad)


def test_v2_stop_loss_take_profit_valid(registry):
    item = {
        **_GOOD_V2,
        "stop_loss": [{"condition": {"node_type": "event", "op": "below", "left": {"source": "price"}, "right": {"const": "90"}}}],
        "take_profit": [{"condition": {"node_type": "event", "op": "above", "left": {"source": "price"}, "right": {"const": "110"}}}],
    }
    _validator(registry).validate(item)  # does not raise


# --- entry/exit leg `source` (tradeplan/deal separation Фаза B2) ------------

def test_v2_leg_source_tradeplan_and_deal_valid(registry):
    item = {
        **_GOOD_V2,
        "entry": [{**_GOOD_V2["entry"][0], "source": "tradeplan"}],
        "stop_loss": [{"condition": {"node_type": "event", "op": "below", "left": {"source": "price"}, "right": {"const": "90"}}, "source": "deal"}],
    }
    _validator(registry).validate(item)  # does not raise


def test_v2_leg_source_unknown_value_rejected(registry):
    from jsonschema import ValidationError

    item = {**_GOOD_V2, "entry": [{**_GOOD_V2["entry"][0], "source": "bogus"}]}
    with pytest.raises(ValidationError):
        _validator(registry).validate(item)
