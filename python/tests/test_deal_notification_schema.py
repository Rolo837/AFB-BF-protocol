"""afb.notification.deal.v1 — AFB-side MQTT deal notification schema."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES

DEAL_NOTIFICATION_EXAMPLES = sorted((EXAMPLES / "notifications").glob("deal.*.json"))
assert DEAL_NOTIFICATION_EXAMPLES, "no deal notification examples found"

DEAL_NOTIFICATION_V1_ID = (
    "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/notification.deal.v1.json"
)


def _validator(registry):
    from jsonschema import Draft202012Validator

    resolved = registry[DEAL_NOTIFICATION_V1_ID]
    return Draft202012Validator(resolved.contents, registry=registry)


@pytest.mark.parametrize("path", DEAL_NOTIFICATION_EXAMPLES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    data = json.loads(path.read_text())
    _validator(registry).validate(data)


def test_rejects_missing_display(registry):
    from jsonschema import ValidationError

    data = json.loads((EXAMPLES / "notifications" / "deal.order_executed.json").read_text())
    del data["display"]
    with pytest.raises(ValidationError):
        _validator(registry).validate(data)


def test_rejects_unknown_category(registry):
    from jsonschema import ValidationError

    data = json.loads((EXAMPLES / "notifications" / "deal.order_executed.json").read_text())
    data["category"] = "unknown_category"
    with pytest.raises(ValidationError):
        _validator(registry).validate(data)


def test_rejects_unknown_schema(registry):
    from jsonschema import ValidationError

    data = json.loads((EXAMPLES / "notifications" / "deal.order_executed.json").read_text())
    data["schema"] = "afb.notification.deal.v2"
    with pytest.raises(ValidationError):
        _validator(registry).validate(data)
