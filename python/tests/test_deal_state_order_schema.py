"""deal_state.v2.json $defs.order — Фаза 3, этап C/D (RESILIENCE.md): the
backstop role/statuses/fields added for hybrid execution mode."""
from __future__ import annotations

import pytest

DEAL_STATE_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/deal_state.json"


def _validator(registry):
    from jsonschema import Draft202012Validator

    resolved = registry[DEAL_STATE_ID]
    order_schema = resolved.contents["$defs"]["order"]
    return Draft202012Validator(order_schema, registry=registry)


def _validates(registry, order) -> bool:
    from jsonschema import ValidationError

    try:
        _validator(registry).validate(order)
        return True
    except ValidationError:
        return False


def test_backstop_role_and_watching_status_valid(registry):
    order = {
        "order_id": "backstop:0",
        "side": "sell",
        "role": "backstop",
        "status": "watching",
        "quantity": 1,
        "filled_quantity": 0,
        "stop_price": "90.5",
        "broker_order_id": "12345",
    }
    assert _validates(registry, order)


def test_expired_status_valid(registry):
    assert _validates(registry, {"role": "backstop", "status": "expired"})


@pytest.mark.parametrize("role", ["entry", "stop_loss", "take_profit", "cancel_close", "backstop"])
def test_all_roles_valid(registry, role):
    assert _validates(registry, {"role": role})


def test_unknown_role_rejected(registry):
    assert not _validates(registry, {"role": "trailing_stop"})


def test_unknown_status_rejected(registry):
    assert not _validates(registry, {"status": "triggered"})


def test_stop_price_and_broker_order_id_optional(registry):
    assert _validates(registry, {"role": "stop_loss", "status": "new"})
