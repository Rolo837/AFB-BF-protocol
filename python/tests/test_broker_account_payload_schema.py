"""payloads/broker.account.json, broker.accounts.json, broker.orders.json,
broker.get_accounts.json, broker.get_catalog.json, broker.resolve_instrument.json
— see the account-channel migration plan, P0.1/P0.6. Fixtures below mirror
belphegor/reporting/broker_snapshots.py::account_snapshot_payload()/
stored_orders_payload() exactly."""
from __future__ import annotations

import pytest

ACCOUNT_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.account.json"
ACCOUNTS_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.accounts.json"
ORDERS_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.orders.json"
GET_ACCOUNTS_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.get_accounts.json"
GET_CATALOG_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.get_catalog.json"
RESOLVE_INSTRUMENT_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.resolve_instrument.json"


def _validator(schema_id, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": schema_id}, registry=registry)


# --- broker.account (deprecated, legacy single-account form) --------------

def test_account_shape_valid(registry):
    msg = {
        "account_id": "bf-account", "broker_account_id": "1899011",
        "equity": "152340.11", "cash": [{"currency": "RUB", "value": "12000"}],
        "positions": [{"quantity": 10, "average_price": "280.5", "current_price": "281.0", "unrealized_pnl": "5.0"}],
    }
    _validator(ACCOUNT_ID, registry).validate(msg)  # does not raise


def test_account_requires_positions_and_cash(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(ACCOUNT_ID, registry).validate({"account_id": "bf-account"})


# --- broker.accounts (new multi-account form) ------------------------------

def test_accounts_shape_valid(registry):
    msg = {
        "default_account_id": "1899011",
        "as_of": "2026-08-01T06:33:00Z",
        "accounts": [
            {
                "account_id": "1899011", "tradable": True, "readonly": False, "status": "ok",
                "equity": "152340.11", "cash": [{"currency": "RUB", "value": "12000"}],
                "positions": [{"quantity": 10, "average_price": "280.5"}],
            },
            {
                "account_id": "1899012", "tradable": False, "readonly": True, "status": "stale",
                "equity": None, "cash": [], "positions": [],
            },
        ],
    }
    _validator(ACCOUNTS_ID, registry).validate(msg)  # does not raise


def test_accounts_rejects_broker_account_id():
    """The one deliberate divergence from broker.account — see decision 2 of
    the account-channel migration plan: no account_id/broker_account_id
    duplication in the new type."""
    import json
    from pathlib import Path

    doc = json.loads(
        (Path(__file__).resolve().parents[2] / "spec" / "schemas" / "payloads" / "broker.accounts.json").read_text()
    )
    account_def = doc["$defs"]["account"]
    assert account_def["additionalProperties"] is False
    assert "broker_account_id" not in account_def["properties"]


def test_accounts_account_rejects_extra_field(registry):
    from jsonschema import ValidationError

    msg = {
        "default_account_id": "1899011",
        "as_of": "2026-08-01T06:33:00Z",
        "accounts": [
            {
                "account_id": "1899011", "tradable": True, "readonly": False, "status": "ok",
                "equity": None, "cash": [], "positions": [],
                "broker_account_id": "1899011",
            }
        ],
    }
    with pytest.raises(ValidationError):
        _validator(ACCOUNTS_ID, registry).validate(msg)


def test_accounts_requires_default_account_id_and_as_of(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(ACCOUNTS_ID, registry).validate({"accounts": []})


def test_accounts_status_enum(registry):
    from jsonschema import ValidationError

    base = {"default_account_id": "1899011", "as_of": "2026-08-01T06:33:00Z", "accounts": [
        {"account_id": "1899011", "tradable": True, "readonly": False, "status": "not_a_real_status",
         "equity": None, "cash": [], "positions": []}
    ]}
    with pytest.raises(ValidationError):
        _validator(ACCOUNTS_ID, registry).validate(base)


# --- broker.orders -----------------------------------------------------

def test_orders_shape_valid(registry):
    msg = {
        "account_id": "bf-account",
        "orders": [
            {
                "deal_id": "deal-1", "order_id": "ord-1", "side": "buy", "role": "entry",
                "status": "filled", "quantity": 10, "filled_quantity": 10, "leg_index": 0,
                "limit_price": "280.5", "average_price": "280.5", "updated_at": "2026-01-01T00:00:00Z",
                "error_code": None, "error_message": None,
            }
        ],
    }
    _validator(ORDERS_ID, registry).validate(msg)  # does not raise


def test_orders_requires_account_id_and_orders(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(ORDERS_ID, registry).validate({})


# --- broker.get_accounts ------------------------------------------------

def test_get_accounts_empty_payload_valid(registry):
    _validator(GET_ACCOUNTS_ID, registry).validate({})  # does not raise


def test_get_accounts_with_account_ids_valid(registry):
    _validator(GET_ACCOUNTS_ID, registry).validate({"account_ids": ["1899011", "1899012"]})  # does not raise


# --- broker.get_catalog (meta xor slice) --------------------------------

def test_get_catalog_empty_is_meta_form(registry):
    _validator(GET_CATALOG_ID, registry).validate({})  # does not raise


def test_get_catalog_exchange_and_market_together_is_slice_form(registry):
    _validator(GET_CATALOG_ID, registry).validate({"exchange": "MOEX", "market": "stock"})  # does not raise


def test_get_catalog_exchange_without_market_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(GET_CATALOG_ID, registry).validate({"exchange": "MOEX"})


def test_get_catalog_market_without_exchange_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(GET_CATALOG_ID, registry).validate({"market": "stock"})


# --- broker.resolve_instrument (deal v1/v2 union) -----------------------

def test_resolve_instrument_accepts_v1_deal(registry):
    deal = {
        "schema": "afb.deal.v1", "deal_id": "deal-1", "revision": 1,
        "target": {"bf_id": "bf-main", "broker": "finam", "instrument": {"exchange": "MOEX", "board": "TQBR", "ticker": "SBER"}},
        "direction": "long",
        "entry": {"condition": {"node_type": "event", "op": "above", "left": {"source": "price", "field": "last"}, "right": {"const": "100"}}},
        "sizing": {"mode": "lots", "value": "1"},
    }
    _validator(RESOLVE_INSTRUMENT_ID, registry).validate({"deal": deal})  # does not raise


def test_resolve_instrument_requires_deal(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(RESOLVE_INSTRUMENT_ID, registry).validate({})
