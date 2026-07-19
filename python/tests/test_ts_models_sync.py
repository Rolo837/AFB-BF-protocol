"""The committed ts/src/models.ts must match what ts/tools/generate-models.mjs
would produce from spec/schemas/ right now.

Two layers, so this still catches drift even without Node installed:
- a source-hash check (pure Python, always runs): the sha256 over
  spec/schemas/**/*.json recorded in the models.ts banner must match the
  schemas on disk.
- a full regeneration + diff (skipped if node/node_modules aren't available).
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from pathlib import Path

import pytest


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _models_path() -> Path:
    return _repo_root() / "ts" / "src" / "models.ts"


def _source_hash() -> str:
    schemas_dir = _repo_root() / "spec" / "schemas"
    files = sorted(
        (
            p
            for p in schemas_dir.rglob("*.json")
            if p.relative_to(schemas_dir).parts[0] != "draft"
        ),
        key=lambda p: p.relative_to(schemas_dir).as_posix(),
    )
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.read_bytes())
    return digest.hexdigest()


def test_models_ts_source_hash_matches_schemas():
    on_disk = _models_path().read_text()
    match = re.search(r"source-hash: ([0-9a-f]{64})", on_disk)
    assert match, "ts/src/models.ts is missing its source-hash banner comment"
    assert match.group(1) == _source_hash(), (
        "spec/schemas/ changed since ts/src/models.ts was generated — run "
        "`npm ci && afb-bf-protocol-generate` (or `npm run generate:models`) and commit the result"
    )


@pytest.mark.skipif(
    shutil.which("node") is None or not (_repo_root() / "node_modules").exists(),
    reason="Node / node_modules not available — models.ts regeneration can't be verified here",
)
def test_models_ts_regeneration_is_idempotent():
    root = _repo_root()
    before = _models_path().read_text()
    subprocess.run(
        ["node", str(root / "ts" / "tools" / "generate-models.mjs")],
        cwd=root,
        check=True,
    )
    after = _models_path().read_text()
    assert after == before, "run `npm run generate:models` and commit ts/src/models.ts"
