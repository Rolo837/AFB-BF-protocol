"""afb.notification.bond.v1 — AFB-side MQTT notification about a held bond's event or anomaly."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES

NOTIFICATION_EXAMPLES = sorted((EXAMPLES / "notifications").glob("bond.*.json"))
assert NOTIFICATION_EXAMPLES, "no bond notification examples found"

NOTIFICATION_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/notification.bond.v1.json"


def _validator(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator(registry[NOTIFICATION_ID].contents, registry=registry)


@pytest.mark.parametrize("path", NOTIFICATION_EXAMPLES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    _validator(registry).validate(json.loads(path.read_text()))


def test_rejects_bad_values(registry):
    from jsonschema import ValidationError

    base = json.loads((EXAMPLES / "notifications" / "bond.offer_warn.json").read_text())
    for patch in (
        {"kind": "coupon"},
        {"stage": "d5"},
        {"days_left": -1},
        {"portfolios": []},
        {"amount": {"value": 1}},
        {"stage": "signal"},  # signal only with anomaly
    ):
        with pytest.raises(ValidationError):
            _validator(registry).validate({**base, **patch})
    anomaly = json.loads((EXAMPLES / "notifications" / "bond.anomaly_signal.json").read_text())
    with pytest.raises(ValidationError):
        _validator(registry).validate({**anomaly, "stage": "warn"})


def test_payload_validation_accepts_it():
    from afb_bf_protocol.payload_validation import validate_notification

    for path in NOTIFICATION_EXAMPLES:
        assert validate_notification(json.loads(path.read_text())) == "afb.notification.bond.v1"
