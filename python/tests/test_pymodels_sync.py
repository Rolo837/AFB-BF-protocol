"""The committed python/afb_bf_protocol/models_generated.py must match what
datamodel-codegen would produce from spec/schemas/ right now.

Mirrors test_ts_models_sync.py's two-layer approach:
- a source-hash check (pure Python, always runs): the sha256 over
  spec/schemas/**/*.json recorded in the banner must match the schemas on disk
  (and — since both use the same hash algorithm — must match ts/src/models.ts's
  banner hash too, when both are in sync).
- a full regeneration + diff (skipped if node or datamodel-codegen aren't
  available — regeneration needs spec/.generated/bundled-schema.json, which
  only ts/tools/generate-models.mjs produces).
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


def _models_generated_path() -> Path:
    return _repo_root() / "python" / "afb_bf_protocol" / "models_generated.py"


def _source_hash() -> str:
    schemas_dir = _repo_root() / "spec" / "schemas"
    files = sorted(schemas_dir.rglob("*.json"), key=lambda p: p.relative_to(schemas_dir).as_posix())
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.read_bytes())
    return digest.hexdigest()


def test_models_generated_source_hash_matches_schemas():
    on_disk = _models_generated_path().read_text()
    match = re.search(r"source-hash: ([0-9a-f]{64})", on_disk)
    assert match, "models_generated.py is missing its source-hash banner comment"
    assert match.group(1) == _source_hash(), (
        "spec/schemas/ changed since models_generated.py was generated — run "
        "`afb-bf-protocol-generate` and commit the result"
    )


@pytest.mark.skipif(
    shutil.which("node") is None
    or shutil.which("datamodel-codegen") is None
    or not (_repo_root() / "node_modules").exists(),
    reason="Node/node_modules or datamodel-codegen not available — "
    "models_generated.py regeneration can't be verified here",
)
def test_models_generated_regeneration_is_idempotent():
    root = _repo_root()
    before = _models_generated_path().read_text()
    subprocess.run(
        ["node", str(root / "ts" / "tools" / "generate-models.mjs")],
        cwd=root,
        check=True,
    )
    from afb_bf_protocol.tools.generate import generate_pymodels

    generate_pymodels(root)
    after = _models_generated_path().read_text()
    assert after == before, "run `afb-bf-protocol-generate` and commit models_generated.py"
