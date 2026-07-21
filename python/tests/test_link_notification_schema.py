from __future__ import annotations

import json

import pytest

LINK_NOTIFICATION_ID = (
    "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/notification.link.v1.json"
)


def _root_validator(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator(registry[LINK_NOTIFICATION_ID].contents, registry=registry)


def test_link_notification_examples_validate(repo_root, registry):
    root = _root_validator(registry)
    examples_dir = repo_root / "examples" / "notifications"
    for name in ("link.degrade.json", "link.recover.json", "link.disconnect.json"):
        root.validate(json.loads((examples_dir / name).read_text()))


def test_link_notification_requires_display(registry):
    from jsonschema import ValidationError

    payload = {
        "schema": "afb.notification.link.v1",
        "notification_id": "n1",
        "event": "daemon.suspended",
        "bf_id": "bf-1",
        "connected": True,
        "daemon_state": "suspended",
        "broker_connected": False,
        "severity": "critical",
        "user": {
            "name": "Trader",
            "telegram": "@trader",
            "email": "trader@test",
            "notify_telegram": True,
            "notify_email": False,
        },
    }
    with pytest.raises(ValidationError):
        _root_validator(registry).validate(payload)


def test_link_notification_rejects_unknown_event(registry):
    from jsonschema import ValidationError

    payload = {
        "schema": "afb.notification.link.v1",
        "notification_id": "n1",
        "event": "link.unknown",
        "bf_id": "bf-1",
        "connected": True,
        "daemon_state": "recovering",
        "broker_connected": False,
        "severity": "warning",
        "display": {"connector_label": "BF One", "title": "x"},
        "user": {
            "name": "Trader",
            "telegram": "@trader",
            "email": "trader@test",
            "notify_telegram": True,
            "notify_email": False,
        },
    }
    with pytest.raises(ValidationError):
        _root_validator(registry).validate(payload)
