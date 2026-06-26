"""The committed taxonomy must match what the spec declares, and the rendered
output must be stable (idempotent)."""
from __future__ import annotations

from afb_bf_protocol import MESSAGE_REGISTRY
from afb_bf_protocol.taxonomy import __file__ as taxonomy_file
from afb_bf_protocol.tools.generate import parse_spec_registry, render_taxonomy


def test_spec_matches_committed_registry():
    assert parse_spec_registry() == MESSAGE_REGISTRY


def test_render_is_idempotent():
    rendered = render_taxonomy(parse_spec_registry())
    on_disk = open(taxonomy_file).read()
    assert rendered == on_disk, "run `afb-bf-protocol-generate` and commit taxonomy.py"
