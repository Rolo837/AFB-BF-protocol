"""The committed ts/src/taxonomy.ts and ts/src/index.ts must match what the
spec-driven renderer produces (mirrors test_taxonomy_spec_sync.py for Python)."""
from __future__ import annotations

from pathlib import Path

from afb_bf_protocol.tools.generate import (
    parse_spec_registry,
    render_taxonomy_ts,
    render_ts_index,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ts_taxonomy_is_up_to_date():
    rendered = render_taxonomy_ts(parse_spec_registry())
    on_disk = (_repo_root() / "ts" / "src" / "taxonomy.ts").read_text()
    assert rendered == on_disk, "run `afb-bf-protocol-generate` and commit ts/src/taxonomy.ts"


def test_ts_index_is_up_to_date():
    rendered = render_ts_index()
    on_disk = (_repo_root() / "ts" / "src" / "index.ts").read_text()
    assert rendered == on_disk, "run `afb-bf-protocol-generate` and commit ts/src/index.ts"
