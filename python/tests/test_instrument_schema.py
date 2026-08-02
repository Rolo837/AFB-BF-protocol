"""afb.instrument.v1 — AFB-side canonical catalog instrument. Broker-agnostic:
one shape for every market class (stock/futures/currency/index), class-specific
fields gated by `market` via allOf/if, never a wire message (AFB<->BF)."""
from __future__ import annotations

import pytest

INSTRUMENT_V1_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/instrument.v1.json"


def _stock(**overrides):
    item = {
        "schema": "afb.instrument.v1",
        "ticker": "SBER",
        "exchange": "MOEX",
        "board": "TQBR",
        "market": "stock",
        "group": "Stocks",
        "source": "moex",
        "isin": "RU0007661625",
        "lot_size": 10,
        "price_step": "0.01",
        "decimals": 2,
        "currency": "RUB",
    }
    item.update(overrides)
    return item


def _futures(**overrides):
    item = {
        "schema": "afb.instrument.v1",
        "ticker": "GZH7",
        "exchange": "MOEX",
        "board": "RFUD",
        "market": "futures",
        "group": "Stocks",
        "source": "moex",
        "asset": "GAZR",
        "expiration": "2027-03-18",
        "step_price": "1.0",
        "margin": "1927.24",
        "futoi_code": "GZ",
        "lot_size": 100,
        "price_step": "1.0",
        "decimals": 0,
    }
    item.update(overrides)
    return item


def _validator(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": INSTRUMENT_V1_ID}, registry=registry)


def test_stock_valid(registry):
    _validator(registry).validate(_stock())  # does not raise


def test_futures_valid(registry):
    _validator(registry).validate(_futures())  # does not raise


def test_unassigned_group_is_null(registry):
    _validator(registry).validate(_stock(group=None))  # does not raise


def test_extended_ticker_for_non_moex(registry):
    item = _stock(ticker="XNAS:AAPL", exchange="XNAS", board="", group=None, source="finam")
    del item["isin"]
    _validator(registry).validate(item)  # does not raise


def test_index_omits_trading_params(registry):
    item = {
        "schema": "afb.instrument.v1", "ticker": "IMOEX", "exchange": "MOEX", "board": "",
        "market": "index", "group": "Indices", "source": "moex",
    }
    _validator(registry).validate(item)  # does not raise


def test_isin_forbidden_on_non_stock(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_futures(isin="RU0007661625"))


def test_futures_only_fields_forbidden_on_stock(registry):
    from jsonschema import ValidationError

    for field, value in (
        ("expiration", "2027-03-18"),
        ("step_price", "1.0"),
        ("margin", "100.0"),
        ("futoi_code", "GZ"),
    ):
        with pytest.raises(ValidationError):
            _validator(registry).validate(_stock(**{field: value}))


def test_missing_group_key_rejected(registry):
    from jsonschema import ValidationError

    item = {k: v for k, v in _stock().items() if k != "group"}
    with pytest.raises(ValidationError):
        _validator(registry).validate(item)


def test_no_broker_binding_fields(registry):
    """The canonical instrument never carries a broker binding — that lives
    only in resolve's binding/broker_instrument response, not the entity."""
    for field in ("bindings", "venues", "bf_id", "broker_symbol", "binding"):
        assert field not in _stock()


def test_extra_field_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator(registry).validate(_stock(unexpected="nope"))
