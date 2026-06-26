"""Every example envelope validates against the envelope schema, and its payload
validates against the per-type payload schema."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import EXAMPLES, SPEC_SCHEMAS

EXAMPLE_FILES = sorted(EXAMPLES.glob("*.json"))
assert EXAMPLE_FILES, "no example envelopes generated"

ENVELOPE_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/envelope.json"


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.stem)
def test_example_validates(path: Path, registry):
    from jsonschema import Draft202012Validator

    env = json.loads(path.read_text())

    envelope_schema = json.loads((SPEC_SCHEMAS / "envelope.json").read_text())
    Draft202012Validator(envelope_schema, registry=registry).validate(env)

    payload_schema_path = SPEC_SCHEMAS / "payloads" / f"{path.stem}.json"
    assert payload_schema_path.exists(), f"missing payload schema for {path.stem}"
    payload_schema = json.loads(payload_schema_path.read_text())
    Draft202012Validator(payload_schema, registry=registry).validate(env["payload"])
