"""afbws/catalog.channel.v1.json — manager-only catalog channel (AFB backend<->AFB frontend only).
Validated as dict literals against the channel schema's $defs."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

CATALOG_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/catalog.channel.v1.json"
EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "catalog_channel"


def _validator(def_name: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{CATALOG_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


def _root(registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": CATALOG_CHANNEL_ID}, registry=registry)


def _msg(op: str, **extra):
    return {"channel": "catalog", "schema": f"afbws.catalog.{op}.v1", **extra}


def _bad(v, doc):
    with pytest.raises(Exception):
        v.validate(doc)


_LISTING = {
    "instrument_key": "MISX:TQBR:SBER", "mic": "MISX", "board": "TQBR", "market": "stock", "ticker": "SBER",
    "name": "Сбербанк", "source": "moex", "lot_size": 10, "price_step": "0.01", "decimals": 2, "currency": "RUB",
}
_SOURCE = {"source": "finam", "title": "Finam", "available": True, "state": "ready", "pending": False,
           "last_refresh_at": "2026-10-03T17:18:00+03:00", "symbols": 283194, "listings": 12, "unlinked": 0}
_ROW = {"ref": "CL@XNYM", "kind": "listing", "ticker": "CL", "name": "Crude Oil", "market": "futures",
        "mic": "XNYM", "archived": False, "in_catalog": None, "addable": True}


def test_capability_id_declared():
    from afb_bf_protocol import CATALOG_CHANNEL_V1

    assert CATALOG_CHANNEL_V1 == "afbws.catalog.channel.v1"


def test_snapshot_request_and_response(registry):
    v = _validator("snapshot", registry)
    v.validate(_msg("snapshot", request_id="r1"))
    v.validate(_msg(
        "snapshot", request_id="r1", revision=7,
        collections=[{"id": "c1", "name": "Нефть", "parent_id": None, "icon_color": "blue"}],
        sets=[{"id": "s1", "name": "Топ", "type": "asset", "visibility_tier": "user", "asset_ids": ["a1"]}],
        assets=[{"id": "a1", "name": "Сбер", "collection_id": "c1", "members": [{"kind": "listing", "ref": "MISX:TQBR:SBER"}]}],
        listings=[_LISTING], derivatives=[{"code": "MISX:IMOEXF", "kind": "perpetual", "name": "IMOEX", "source": "moex"}],
        sources=[_SOURCE],
    ))


def test_snapshot_rejects_request_with_extra_and_partial_response(registry):
    v = _validator("snapshot", registry)
    _bad(v, _msg("snapshot", request_id="r1", limit=5))
    _bad(v, _msg("snapshot", request_id="r1", revision=1))
    _bad(v, _msg("snapshot"))


def test_symbols_request_and_response(registry):
    v = _validator("symbols", registry)
    v.validate(_msg("symbols", request_id="r1", source="finam"))
    v.validate(_msg("symbols", request_id="r1", source="finam", query="CL", kind="listing", market="futures",
                    include_archived=False, unassigned=True, limit=100, cursor="abc"))
    v.validate(_msg("symbols", request_id="r1", source="finam", total=1, next_cursor=None,
                    fetched_at="2026-10-03T17:18:00+03:00", items=[_ROW]))
    v.validate(_msg("symbols", request_id="r1", source="moex", total=1, next_cursor="n", fetched_at=None,
                    items=[{**_ROW, "addable": False, "reason": "unsupported_type"}]))


@pytest.mark.parametrize("patch", [
    {"limit": 101}, {"limit": 0}, {"source": "bf"}, {"kind": "series"}, {"market": "bond"}, {"cursor": ""},
])
def test_symbols_request_rejects(registry, patch):
    _bad(_validator("symbols", registry), _msg("symbols", request_id="r1", **{"source": "finam", **patch}))


def test_symbols_response_capped_at_100(registry):
    v = _validator("symbols", registry)
    base = dict(request_id="r1", source="finam", total=101, next_cursor="n", fetched_at=None)
    v.validate(_msg("symbols", items=[_ROW] * 100, **base))
    _bad(v, _msg("symbols", items=[_ROW] * 101, **base))
    _bad(v, _msg("symbols", request_id="r1", source="finam", items=[_ROW]))  # no total/cursor/fetched_at


def test_commit_request_and_response(registry):
    v = _validator("commit", registry)
    v.validate(_msg("commit", request_id="r1", base_revision=7))
    v.validate(_msg(
        "commit", request_id="r1", base_revision=7, reason="import",
        collections=[{"id": "c1", "name": "Нефть", "parent_id": None, "asset_ids": ["a1"]}], collection_order=["c1"],
        sets=[{"id": "s1", "name": "Топ", "type": "instrument", "instrument_keys": ["MISX:TQBR:SBER"]}], set_order=["s1"],
        assets=[{"id": "a1", "name": "Нефть", "collection_id": "c1", "members": [
            {"kind": "listing", "ref": "MISX:TQBR:SBER"},
            {"kind": "derivative", "ref": "MISX:IMOEXF"},
            {"kind": "listing", "source": "finam", "ref": "CL@XNYM"},
        ]}],
        remove_assets=["a0"], remove_collections=["c0"], remove_sets=["s0"],
        archive=[{"instrument_key": "MISX:TQBR:OLD", "reason": "manual"}],
    ))
    v.validate(_msg("commit", request_id="r1", revision=8,
                    created=[{"source": "finam", "ref": "CL@XNYM", "instrument_key": "XNYM:futures:CL"},
                             {"source": "finam", "ref": "BZ@IFEU", "derivative": "IFEU:BZ"}]))


def test_commit_requires_base_revision(registry):
    v = _validator("commit", registry)
    _bad(v, _msg("commit", request_id="r1"))
    _bad(v, _msg("commit", request_id="r1", assets=[]))
    _bad(v, _msg("commit", request_id="r1", base_revision=-1))
    _bad(v, _msg("commit", base_revision=1))


def test_commit_member_forms(registry):
    v = _validator("commit", registry)

    def with_member(member):
        return _msg("commit", request_id="r1", base_revision=1, assets=[{"id": "a", "name": "A", "members": [member]}])

    _bad(v, with_member({"ref": "MISX:TQBR:SBER"}))  # no kind
    _bad(v, with_member({"kind": "listing"}))  # no ref
    _bad(v, with_member({"kind": "listing", "source": "bf", "ref": "X"}))  # unknown source
    _bad(v, with_member({"kind": "instrument", "ref": "X"}))  # unknown kind
    # a new member never carries listing data
    for extra in ({"ticker": "CL"}, {"mic": "XNYM"}, {"lot_size": 1}, {"listing": {"ticker": "CL"}}):
        _bad(v, with_member({"kind": "listing", "source": "finam", "ref": "CL@XNYM", **extra}))
    _bad(v, with_member({"kind": "listing", "ref": "X", "ticker": "CL"}))


def test_commit_rejects_legacy_instrument_channel_fields(registry):
    v = _validator("commit", registry)
    for legacy in ("listings", "series", "asset_sets", "set_members", "collection_members", "archive_listings", "items"):
        _bad(v, _msg("commit", request_id="r1", base_revision=1, **{legacy: []}))


def test_commit_response_cannot_carry_base_revision(registry):
    _bad(_validator("commit", registry), _msg("commit", request_id="r1", base_revision=1, revision=2, created=[]))


def test_refresh_request_response_push(registry):
    v = _validator("refresh", registry)
    v.validate(_msg("refresh", request_id="r1"))
    v.validate(_msg("refresh", request_id="r1", sources=["moex", "finam"]))
    v.validate(_msg("refresh", request_id="r1", queued=["moex"], already_queued=["finam"],
                    rejected=[{"source": "finam", "code": "source_unavailable", "message": "токен не read-only"}]))
    v.validate(_msg("refresh", source="finam", state="done", finished_at="2026-10-03T17:18:00+03:00",
                    received=283194, summary="добавлено 12", error=None, revision=9, states=[_SOURCE]))
    v.validate(_msg("refresh", source="moex", state="failed", finished_at="2026-10-03T17:18:00+03:00", error="ISS timeout"))


def test_refresh_rejects(registry):
    v = _validator("refresh", registry)
    _bad(v, _msg("refresh"))  # neither request nor push
    _bad(v, _msg("refresh", request_id="r1", sources=["bf"]))
    _bad(v, _msg("refresh", request_id="r1", sources=["moex", "moex"]))
    _bad(v, _msg("refresh", request_id="r1", dry_run=True))
    # a push never carries a request_id
    _bad(v, _msg("refresh", request_id="r1", source="finam", state="done", finished_at="2026-10-03T17:18:00+03:00"))
    _bad(v, _msg("refresh", source="finam", state="running", finished_at="2026-10-03T17:18:00+03:00"))


def test_error(registry):
    v = _validator("error", registry)
    v.validate(_msg("error", request_id="r1", code="conflict", message="stale", details={"catalog_revision": 9}))
    v.validate(_msg("error", code="unsupported_type", message="x",
                    details={"refs": [{"source": "finam", "ref": "BRNX26@IFEU", "code": "unsupported_type", "message": "срочный"}]}))
    _bad(v, _msg("error", code="boom", message="x"))
    _bad(v, _msg("error", code="forbidden", message=""))


def test_root_dispatches_every_message(registry):
    root = _root(registry)
    root.validate(_msg("snapshot", request_id="r1"))
    root.validate(_msg("symbols", request_id="r1", source="moex"))
    root.validate(_msg("commit", request_id="r1", base_revision=1))
    root.validate(_msg("refresh", request_id="r1"))
    root.validate(_msg("error", code="forbidden", message="x"))
    _bad(root, _msg("resolve", request_id="r1"))
    _bad(root, {**_msg("snapshot", request_id="r1"), "channel": "instrument"})


def test_examples_validate(registry):
    root = _root(registry)
    files = sorted(EXAMPLES.glob("*.json"))
    assert files, "examples/catalog_channel is empty"
    for path in files:
        root.validate(json.loads(path.read_text(encoding="utf-8")))
