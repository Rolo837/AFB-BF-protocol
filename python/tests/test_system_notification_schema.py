"""afb.notification.system.v1 — AFB-side MQTT system notification schema
(план стабильности AFB, Этап 5: source_state/stale_data/resource/startup)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES

NOTIFICATION_EXAMPLES = sorted((EXAMPLES / "notifications").glob("system.*.json"))
assert NOTIFICATION_EXAMPLES, "no system notification examples found"

NOTIFICATION_V1_ID = (
    "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/notification.system.v1.json"
)


def _validator(registry):
    from jsonschema import Draft202012Validator

    resolved = registry[NOTIFICATION_V1_ID]
    return Draft202012Validator(resolved.contents, registry=registry)


@pytest.mark.parametrize("path", NOTIFICATION_EXAMPLES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    data = json.loads(path.read_text())
    _validator(registry).validate(data)


def test_rejects_unknown_kind(registry):
    from jsonschema import ValidationError

    data = json.loads((EXAMPLES / "notifications" / "system.source_down.json").read_text())
    data["kind"] = "not_a_kind"
    with pytest.raises(ValidationError):
        _validator(registry).validate(data)


def test_rejects_missing_since(registry):
    from jsonschema import ValidationError

    data = json.loads((EXAMPLES / "notifications" / "system.source_down.json").read_text())
    del data["since"]
    with pytest.raises(ValidationError):
        _validator(registry).validate(data)


def test_prev_state_optional(registry):
    """startup notifications legitimately have no prev_state (first-ever observation)."""
    data = json.loads((EXAMPLES / "notifications" / "system.startup_unclean.json").read_text())
    assert "prev_state" not in data
    _validator(registry).validate(data)
