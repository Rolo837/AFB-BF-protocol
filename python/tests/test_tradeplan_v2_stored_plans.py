"""Every real stored plan of the local AFB checkout must satisfy the AFB-internal
storage schema tradeplan.v2.json (the closed one: additionalProperties:false at
the root and on legs/conditions). Reads AFB's `state/` (live plans in
`tradeplans/<user>/*.yaml`, archived in `archive/<user>/<year>/<month>/tradeplan-*.yaml`)
without modifying it. Skipped when the AFB checkout is not next to this repo
(CI); point AFB_STATE_DIR at another `state/` to run it elsewhere.

Pre-v2 archived files (the `new_at`/`entry_condition`/`quantity_*` shape, no
`schema`) are not afb.tradeplan.v2 plans: AFB cannot parse them either
(TradePlanV2.from_dict needs `entries`) and never serves them (list_ skips
archive, get returns them untouched only if asked by id) — they are recognised
explicitly and excluded, not validated.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from conftest import REPO_ROOT

yaml = pytest.importorskip("yaml")

_STATE = Path(os.environ.get("AFB_STATE_DIR") or REPO_ROOT.parent / "AFB" / "state")
_PLAN_FILES = sorted(_STATE.glob("tradeplans/*/*.yaml")) + sorted(_STATE.glob("archive/*/*/*/tradeplan-*.yaml"))

pytestmark = pytest.mark.skipif(not _PLAN_FILES, reason=f"no stored tradeplans under {_STATE}")

_STORAGE_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/tradeplan.v2.json"
_LEGACY_MARKERS = {"entry_condition", "quantity_value", "quantity_mode", "new_at"}


def _load(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), path
    return data


def _is_pre_v2(plan: dict) -> bool:
    return "schema" not in plan and bool(_LEGACY_MARKERS & plan.keys())


def test_stored_plans_validate_against_storage_schema(registry):
    from jsonschema import Draft202012Validator

    validator = Draft202012Validator({"$ref": _STORAGE_ID}, registry=registry)
    checked = 0
    failures = []
    for path in _PLAN_FILES:
        plan = _load(path)
        if _is_pre_v2(plan):
            continue
        checked += 1
        for error in validator.iter_errors(plan):
            where = "/".join(str(p) for p in error.absolute_path) or "<root>"
            failures.append(f"{path.relative_to(_STATE)}: {error.message[:160]} (at {where})")
    assert not failures, "\n".join(failures)
    assert checked, "every stored plan was classified as pre-v2"


def test_only_pre_v2_files_lack_schema():
    """A file without `schema` must be a recognisable pre-v2 plan, not a silently skipped new one."""
    for path in _PLAN_FILES:
        plan = _load(path)
        if "schema" not in plan:
            assert _is_pre_v2(plan), f"{path.relative_to(_STATE)}: no `schema` and not a pre-v2 plan"
        else:
            assert plan["schema"] == "afb.tradeplan.v2", path
