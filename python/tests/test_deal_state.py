"""DealState: configurable timestamp provider, field set, and roundtrip."""
from __future__ import annotations

from afb_bf_protocol import deal_state as ds
from afb_bf_protocol import DealState, set_now_iso


def _mk(**kw):
    base = dict(deal_id="d:bf1", revision=1, owner_user_id="u", status="published",
                deal={"target": {"bf_id": "bf1"}})
    base.update(kw)
    return DealState(**base)


def test_now_provider_is_configurable():
    set_now_iso(lambda: "2026-01-01T00:00:00+03:00")
    try:
        d = _mk()
        assert d.created_at == "2026-01-01T00:00:00+03:00"
        d.append_status_history("active", source="bf")
        assert d.status_history[-1]["at"] == "2026-01-01T00:00:00+03:00"
    finally:
        set_now_iso(ds._utc_now_iso)


def test_to_dict_field_order_and_observed():
    d = _mk(created_at="t0", updated_at="t1")
    keys = list(d.to_dict().keys())
    assert keys == [
        "deal_id", "revision", "owner_user_id", "status", "deal", "source_refs",
        "status_history", "orders", "positions", "event_journal", "observed",
        "execution_phase", "created_at", "updated_at",
    ]


def test_from_dict_roundtrip():
    d = _mk(created_at="t0", updated_at="t1", observed={"position": {"qty": 0}})
    again = DealState.from_dict(d.to_dict())
    assert again.to_dict() == d.to_dict()


def test_bf_id_and_resync_payload():
    d = _mk()
    assert d.bf_id() == "bf1"
    assert d.to_resync_payload()["deal_id"] == "d:bf1"
