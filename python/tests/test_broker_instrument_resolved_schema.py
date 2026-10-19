"""payloads/broker.instrument_resolved.json and deal.accepted.json#broker_instrument —
response shapes for broker.resolve_instrument (and the accepted deal). Deliberately
permissive (additionalProperties: true) except for the typed `price_type`."""
from __future__ import annotations

import pytest

RESOLVED_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/broker.instrument_resolved.json"
ACCEPTED_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/payloads/deal.accepted.json"


def _validator(schema_id, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": schema_id}, registry=registry)


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


@pytest.mark.parametrize("price_type", ["UNKNOWN", "POSITIVE", "NON_NEGATIVE", "ANY"])
def test_instrument_resolved_accepts_price_type(registry, price_type):
    msg = {"binding": {}, "broker_instrument": {"price_type": price_type, "tradable": True}}
    _validator(RESOLVED_ID, registry).validate(msg)  # does not raise


def test_instrument_resolved_rejects_unknown_price_type(registry):
    from jsonschema import ValidationError

    msg = {"binding": {}, "broker_instrument": {"price_type": "NEGATIVE_ONLY"}}
    with pytest.raises(ValidationError):
        _validator(RESOLVED_ID, registry).validate(msg)


def test_deal_accepted_broker_instrument_price_type(registry):
    from jsonschema import ValidationError

    base = {"deal_id": "deal-1", "revision": 1, "broker_instrument": {"price_type": "POSITIVE"}}
    try:
        _validator(ACCEPTED_ID, registry).validate(base)
    except ValidationError as exc:  # only a price_type failure would be a regression
        assert "price_type" not in "/".join(map(str, exc.absolute_path)), exc.message
    bad = {**base, "broker_instrument": {"price_type": "bogus"}}
    with pytest.raises(ValidationError):
        _validator(ACCEPTED_ID, registry).validate(bad)
