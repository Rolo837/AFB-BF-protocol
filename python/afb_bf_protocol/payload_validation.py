"""Structural validation of deal and trade-plan payloads against the packaged
JSON Schemas.

This is the declarative counterpart to the deep business validation BF does in
``belphegor.protocol.validation`` — it only checks *shape* (schema version
dispatch, required fields, left/right pairing on condition nodes, decimal
string patterns), the same rules ``python/tests/test_fixtures_schema.py``
enforces on the fixtures. Deal payloads are also messages on the AFB<->BF wire;
trade-plan templates are AFB-only and never cross that wire — see
``docs/PROTOCOL.md``.

Requires the ``validation`` extra (``pip install afb-bf-protocol[validation]``)
for ``jsonschema``; importing this module without it installed is fine, only
calling the ``validate_*`` functions raises.
"""
from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

from .validation import ProtocolValidationError

__all__ = [
    "PayloadValidationError",
    "validate_deal",
    "validate_tradeplan",
    "resolve_tradeplan_schema",
    "validate_alarm",
    "validate_notification",
    "validate_user_settings_file",
]

_DEAL_SCHEMAS = {"afb.deal.v1", "afb.deal.v2"}
_TRADEPLAN_SCHEMAS = {"afb.tradeplan.v1", "afb.tradeplan.v2"}
_DEFAULT_TRADEPLAN_SCHEMA = "afb.tradeplan.v1"
_ALARM_SCHEMAS = {"afb.alarm.v1"}
_NOTIFICATION_SCHEMAS = {"afb.notification.alarm.v1", "afb.notification.deal.v1"}
_USER_SETTINGS_FILE_SCHEMA = "settings/user_file.v1.json"


def _schema_filename(schema_id: str) -> str:
    # "afb.deal.v1" -> "deal.v1.json" (matches spec/schemas/*.json on disk).
    return f"{schema_id.removeprefix('afb.')}.json"


class PayloadValidationError(ProtocolValidationError):
    """A deal or trade-plan payload does not match its declared schema."""


def _import_jsonschema() -> Any:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise ImportError(
            "afb_bf_protocol.payload_validation requires jsonschema; "
            "install with `pip install afb-bf-protocol[validation]`"
        ) from exc
    return Draft202012Validator


@lru_cache(maxsize=1)
def _registry() -> Any:
    from referencing import Registry, Resource

    schemas_root = resources.files("afb_bf_protocol") / "schemas"
    resources_list: list[tuple[str, Any]] = []
    for path in _iter_schema_files(schemas_root):
        doc = json.loads(path.read_text())
        resources_list.append((doc["$id"], Resource.from_contents(doc)))
    return Registry().with_resources(resources_list)


def _iter_schema_files(root: Any) -> list[Path]:
    out: list[Path] = []
    for entry in root.iterdir():
        if entry.is_dir():
            out.extend(_iter_schema_files(entry))
        elif entry.name.endswith(".json"):
            out.append(entry)
    return out


@lru_cache(maxsize=None)
def _schema_doc(filename: str) -> dict[str, Any]:
    text = (resources.files("afb_bf_protocol") / "schemas" / filename).read_text()
    return json.loads(text)


def _validate(obj: dict[str, Any], *, schema_filename: str, what: str) -> None:
    Draft202012Validator = _import_jsonschema()
    from jsonschema import ValidationError

    schema = _schema_doc(schema_filename)
    try:
        Draft202012Validator(schema, registry=_registry()).validate(obj)
    except ValidationError as exc:
        path = "/".join(str(p) for p in exc.absolute_path)
        raise PayloadValidationError(
            "invalid_schema", f"{what}: {exc.message} (at {path or '<root>'})"
        ) from exc


def validate_deal(obj: dict[str, Any]) -> str:
    """Validate a deal payload against afb.deal.v1 or afb.deal.v2 (dispatched on
    ``obj["schema"]``). Returns the resolved schema id."""
    if not isinstance(obj, dict):
        raise PayloadValidationError("invalid_schema", "deal must be an object")
    schema = obj.get("schema")
    if schema not in _DEAL_SCHEMAS:
        raise PayloadValidationError("invalid_schema", f"unknown deal schema: {schema!r}")
    _validate(obj, schema_filename=_schema_filename(schema), what="deal")
    return schema


def resolve_tradeplan_schema(obj: dict[str, Any]) -> str:
    """The trade-plan schema id ``obj`` declares, defaulting to afb.tradeplan.v1
    when the ``schema`` field is absent (compatibility with frontends older
    than the tradeplan schema itself)."""
    if not isinstance(obj, dict):
        raise PayloadValidationError("invalid_schema", "trade plan must be an object")
    schema = obj.get("schema")
    if schema is None:
        return _DEFAULT_TRADEPLAN_SCHEMA
    if schema not in _TRADEPLAN_SCHEMAS:
        raise PayloadValidationError("invalid_schema", f"unknown tradeplan schema: {schema!r}")
    return schema


def validate_tradeplan(obj: dict[str, Any]) -> str:
    """Validate a trade-plan template against afb.tradeplan.v1 or
    afb.tradeplan.v2 (dispatched on ``obj.get("schema")``, missing ⇒ v1).
    Returns the resolved schema id."""
    schema = resolve_tradeplan_schema(obj)
    _validate(obj, schema_filename=_schema_filename(schema), what="tradeplan")
    return schema


def validate_alarm(obj: dict[str, Any]) -> str:
    """Validate an AFB alarm against afb.alarm.v1 (dispatched on
    ``obj["schema"]``). Returns the resolved schema id. Like trade plans,
    alarms never cross the AFB<->BF wire."""
    if not isinstance(obj, dict):
        raise PayloadValidationError("invalid_schema", "alarm must be an object")
    schema = obj.get("schema")
    if schema not in _ALARM_SCHEMAS:
        raise PayloadValidationError("invalid_schema", f"unknown alarm schema: {schema!r}")
    _validate(obj, schema_filename=_schema_filename(schema), what="alarm")
    return schema


def validate_notification(obj: dict[str, Any]) -> str:
    """Validate an AFB MQTT notification against afb.notification.alarm.v1 or
    afb.notification.deal.v1 (dispatched on ``obj["schema"]``). Returns the
    resolved schema id. Like alarms, notifications never cross the AFB<->BF
    wire."""
    if not isinstance(obj, dict):
        raise PayloadValidationError("invalid_schema", "notification must be an object")
    schema = obj.get("schema")
    if schema not in _NOTIFICATION_SCHEMAS:
        raise PayloadValidationError("invalid_schema", f"unknown notification schema: {schema!r}")
    _validate(obj, schema_filename=_schema_filename(schema), what="notification")
    return schema


def validate_user_settings_file(obj: dict[str, Any]) -> list[str]:
    """Structurally validate a user settings file (config/users/*.yaml,
    on-disk shape) against settings/user_file.v1.json. Returns a list of
    human-readable error strings (empty if valid) instead of raising — this
    is a diagnostic check (AFB logs warnings on load, does not block reads),
    unlike validate_deal/validate_tradeplan/validate_alarm which validate
    wire-bound payloads and raise on the first mismatch. additionalProperties
    is permissive (true) on this schema in v1, so drift shows up as type/enum
    mismatches on known fields (e.g. legacy flat alarm condition), not as
    unknown-key noise."""
    if not isinstance(obj, dict):
        return ["user settings file must be an object"]
    Draft202012Validator = _import_jsonschema()
    schema = _schema_doc(_USER_SETTINGS_FILE_SCHEMA)
    validator = Draft202012Validator(schema, registry=_registry())
    errors: list[str] = []
    for exc in validator.iter_errors(obj):
        path = "/".join(str(p) for p in exc.absolute_path)
        errors.append(f"{exc.message} (at {path or '<root>'})")
    return errors
