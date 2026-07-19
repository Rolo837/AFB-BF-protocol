"""The schemas packaged inside afb_bf_protocol (for runtime payload_validation)
must be byte-identical to spec/schemas — the single canon. Same pattern as
test_taxonomy_spec_sync.py for taxonomy.py.

``spec/schemas/draft/`` is parked and intentionally excluded from the package
(and from model generation).
"""
from __future__ import annotations

from pathlib import Path

from afb_bf_protocol.tools.generate import sync_packaged_schemas
from conftest import REPO_ROOT, SPEC_SCHEMAS


def _read_tree(root: Path, *, skip_draft: bool = False) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in root.rglob("*.json"):
        rel = p.relative_to(root)
        if skip_draft and rel.parts and rel.parts[0] == "draft":
            continue
        out[str(rel)] = p.read_text()
    return out


def test_packaged_schemas_match_spec():
    packaged_root = REPO_ROOT / "python" / "afb_bf_protocol" / "schemas"
    assert _read_tree(packaged_root) == _read_tree(SPEC_SCHEMAS, skip_draft=True), (
        "run `afb-bf-protocol-generate` and commit python/afb_bf_protocol/schemas/"
    )


def test_sync_is_idempotent(tmp_path):
    fake_root = tmp_path
    (fake_root / "spec" / "schemas").mkdir(parents=True)
    for src in SPEC_SCHEMAS.rglob("*.json"):
        rel = src.relative_to(SPEC_SCHEMAS)
        dst = fake_root / "spec" / "schemas" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text())
    (fake_root / "python" / "afb_bf_protocol").mkdir(parents=True)

    dst1, count1 = sync_packaged_schemas(fake_root)
    tree1 = _read_tree(dst1)
    dst2, count2 = sync_packaged_schemas(fake_root)
    tree2 = _read_tree(dst2)

    assert count1 == count2
    assert tree1 == tree2
    assert not any(k.startswith("draft/") for k in tree1)
