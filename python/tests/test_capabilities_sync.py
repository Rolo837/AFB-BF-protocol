"""Capability-id constants (python/afb_bf_protocol/capabilities.py,
ts/src/capabilities.ts, ts/src/index.ts) must match what a fresh render of
spec/schemas/afbws/*.json's `x-afbws-support-id` produces."""
from __future__ import annotations

from pathlib import Path

from afb_bf_protocol import ALARM_CHANNEL_V1, ALL_CAPABILITY_IDS, TRADEPLAN_CHANNEL_V1
from afb_bf_protocol.capabilities import __file__ as capabilities_file
from afb_bf_protocol.tools.generate import (
    collect_afbws_capability_ids,
    render_capabilities,
    render_capabilities_ts,
    render_ts_index,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_capability_ids_match_schema_declarations():
    assert collect_afbws_capability_ids() == {
        ALARM_CHANNEL_V1: "ALARM_CHANNEL_V1",
        TRADEPLAN_CHANNEL_V1: "TRADEPLAN_CHANNEL_V1",
    }
    assert ALL_CAPABILITY_IDS == {ALARM_CHANNEL_V1, TRADEPLAN_CHANNEL_V1}


def test_capabilities_py_is_up_to_date():
    rendered = render_capabilities(collect_afbws_capability_ids())
    on_disk = open(capabilities_file).read()
    assert rendered == on_disk, "run `afb-bf-protocol-generate` and commit capabilities.py"


def test_capabilities_ts_is_up_to_date():
    rendered = render_capabilities_ts(collect_afbws_capability_ids())
    on_disk = (_repo_root() / "ts" / "src" / "capabilities.ts").read_text()
    assert rendered == on_disk, "run `afb-bf-protocol-generate` and commit ts/src/capabilities.ts"


def test_ts_index_reexports_capabilities():
    rendered = render_ts_index()
    on_disk = (_repo_root() / "ts" / "src" / "index.ts").read_text()
    assert rendered == on_disk, "run `afb-bf-protocol-generate` and commit ts/src/index.ts"
