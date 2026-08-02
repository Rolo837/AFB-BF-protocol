"""payloads/broker.catalog.json, broker.instrument.json,
broker.instrument_resolved.json — response shapes for broker.get_catalog /
broker.get_instrument / broker.resolve_instrument. Deliberately permissive
(additionalProperties: true): these describe what BF's InstrumentRegistry /
InstrumentInfo already emit (belphegor/brokers/catalog_store.py,
belphegor/domain/instruments.py, belphegor/reporting/broker_snapshots.py),
not a new constraint on it — a PATCH, not a MINOR."""
from __future__ import annotations

import pytest

CATALOG_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.catalog.json"
INSTRUMENT_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.instrument.json"
RESOLVED_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.instrument_resolved.json"


def _validator(schema_id, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": schema_id}, registry=registry)


# --- broker.catalog: CatalogMeta.to_dict() / get_catalog_slice() -----------

def test_catalog_meta_shape_valid(registry):
    msg = {
        "session_date": "2026-08-01", "revision": 62, "broker": "finam-arena",
        "exchanges": ["MOEX", "XNAS"],
        "markets": [{"exchange": "MOEX", "market": "stock"}, {"exchange": "MOEX", "market": "futures"}],
    }
    _validator(CATALOG_ID, registry).validate(msg)  # does not raise


def test_catalog_slice_shape_valid(registry):
    msg = {
        "session_date": "2026-08-01", "revision": 62, "broker": "finam-arena",
        "exchange": "MOEX", "market": "stock",
        "instruments": [
            {"broker_symbol": "SBER@MISX", "exchange": "MOEX", "board": "", "ticker": "SBER", "name": "Сбербанк", "market": "stock"},
        ],
    }
    _validator(CATALOG_ID, registry).validate(msg)  # does not raise


def test_catalog_cannot_mix_meta_and_slice(registry):
    from jsonschema import ValidationError

    msg = {
        "broker": "finam-arena", "exchanges": ["MOEX"], "markets": [],
        "exchange": "MOEX", "market": "stock", "instruments": [],
    }
    with pytest.raises(ValidationError):
        _validator(CATALOG_ID, registry).validate(msg)


def test_catalog_slice_requires_broker_symbol_per_row(registry):
    from jsonschema import ValidationError

    msg = {
        "broker": "finam-arena", "exchange": "MOEX", "market": "stock",
        "instruments": [{"ticker": "SBER"}],
    }
    with pytest.raises(ValidationError):
        _validator(CATALOG_ID, registry).validate(msg)


def test_catalog_tolerates_unknown_fields():
    """additionalProperties: true — a third broker adapter can add fields
    without breaking AFB's validation."""
    import json
    from pathlib import Path

    doc = json.loads((Path(__file__).resolve().parents[2] / "spec" / "schemas" / "payloads" / "broker.catalog.json").read_text())
    assert doc.get("$defs", {}).get("meta", {}).get("additionalProperties") is True
    assert doc.get("$defs", {}).get("slice", {}).get("additionalProperties") is True


# --- broker.instrument: instrument_resolved_payload(InstrumentInfo) --------

def test_instrument_full_shape_valid(registry):
    msg = {
        "symbol": "SBER@MISX", "exchange": "MOEX", "board": "", "ticker": "SBER", "mic": "MISX",
        "name": "Сбербанк", "market": "stock",
        "decimals": 2, "price_step": "0.01", "lot_size": 10, "currency": "RUB",
        "expiration_date": None, "tradable": True, "longable": True, "shortable": True,
        "long_initial_margin": "3574.4", "short_initial_margin": "3574.4",
        "updated_at": "2026-08-01T06:33:00Z",
    }
    _validator(INSTRUMENT_ID, registry).validate(msg)  # does not raise


def test_instrument_rejects_finam_specific_fields_only_via_being_absent(registry):
    """additionalProperties stays true (a future broker plugin may add its
    own fields) — but instrument_resolved_payload() itself no longer emits
    these Finam-native ones, so a schema-conformant fixture never needs
    them. This test documents that omission, not a schema constraint."""
    msg = {"symbol": "SBER@MISX", "market": "stock"}
    assert not ({"asset_type", "min_step_raw", "long_risk_rate", "short_risk_rate", "future_details", "bond_details"} & msg.keys())
    _validator(INSTRUMENT_ID, registry).validate(msg)  # does not raise


def test_instrument_minimal_shape_valid(registry):
    """Only symbol required — matches CatalogEntry-derived fallbacks."""
    _validator(INSTRUMENT_ID, registry).validate({"symbol": "SBER@MISX"})  # does not raise


def test_instrument_requires_symbol(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(INSTRUMENT_ID, registry).validate({"ticker": "SBER"})


# --- broker.instrument_resolved: {binding, broker_instrument} --------------

def test_instrument_resolved_shape_valid(registry):
    msg = {
        "binding": {"account_id": "1000316", "symbol": "SBER@MISX"},
        "broker_instrument": {"lot_size": 10, "price_step": "0.01", "tradable": True},
    }
    _validator(RESOLVED_ID, registry).validate(msg)  # does not raise


def test_instrument_resolved_requires_both_keys(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(RESOLVED_ID, registry).validate({"binding": {}})
    with pytest.raises(ValidationError):
        _validator(RESOLVED_ID, registry).validate({"broker_instrument": {}})


def test_instrument_resolved_tolerates_empty_objects(registry):
    """BF always emits both keys, but each can be `{}` (e.g. no binding
    applied yet) — dict(x or {}) on the BF side never omits the key."""
    _validator(RESOLVED_ID, registry).validate({"binding": {}, "broker_instrument": {}})  # does not raise
