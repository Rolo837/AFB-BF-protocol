"""Shared paths and a referencing registry over spec/schemas."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_SCHEMAS = REPO_ROOT / "spec" / "schemas"
EXAMPLES = REPO_ROOT / "examples"


def _load_registry():
    from referencing import Registry, Resource

    resources = []
    for path in SPEC_SCHEMAS.rglob("*.json"):
        doc = json.loads(path.read_text())
        resources.append((doc["$id"], Resource.from_contents(doc)))
    return Registry().with_resources(resources)


@pytest.fixture(scope="session")
def registry():
    return _load_registry()


@pytest.fixture(scope="session")
def repo_root():
    return REPO_ROOT
