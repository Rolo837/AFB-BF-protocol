"""afb.notification.expiration.v1 — AFB-side MQTT notification about an expiring
contract the user works with (предэкспирационный блок политики экспирации)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES

NOTIFICATION_EXAMPLES = sorted((EXAMPLES / "notifications").glob("expiration.*.json"))
assert NOTIFICATION_EXAMPLES, "no expiration notification examples found"

NOTIFICATION_ID = (
    "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/notification.expiration.v1.json"
)


def _validator(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator(registry[NOTIFICATION_ID].contents, registry=registry)


@pytest.mark.parametrize("path", NOTIFICATION_EXAMPLES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    _validator(registry).validate(json.loads(path.read_text()))


def test_rejects_unknown_stage_and_negative_days(registry):
    from jsonschema import ValidationError

    base = json.loads((EXAMPLES / "notifications" / "expiration.warn.json").read_text())
    for patch in ({"stage": "d5"}, {"days_left": -1}, {"usage": {"alarms": 1}}):
        with pytest.raises(ValidationError):
            _validator(registry).validate({**base, **patch})


def test_payload_validation_accepts_it():
    from afb_bf_protocol.payload_validation import validate_notification

    payload = json.loads((EXAMPLES / "notifications" / "expiration.warn.json").read_text())
    assert validate_notification(payload) == "afb.notification.expiration.v1"
