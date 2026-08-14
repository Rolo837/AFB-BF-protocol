"""afbws/instrument.channel.v1.json — schema-first `instrument` channel
(AFB backend<->AFB frontend only). Negotiated via auth.support/auth_ok.support;
not part of the afb.execution.v1 AFB<->BF wire. Replaces legacy
`securities/list`, `setup/markets`+`get_assign`+`set_assign`, and
`account/get_catalog`+`get_instrument`+`resolve_instrument`."""
from __future__ import annotations

import json

import pytest

CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/instrument.channel.v1.json"

_ITEM = {
    "schema": "afb.instrument.v1",
    "ticker": "SBER",
    "exchange": "MOEX",
    "board": "TQBR",
    "market": "stock",
    "group": "Stocks",
    "source": "moex",
}

_POOL_ITEM = {**_ITEM, "group": None, "source": "arena"}

# --- phase 2 (federated catalog: sets/memberships/series) fixtures ----------

_SET = {
    "set_id": "set-blue-chips",
    "key": "blue-chips",
    "scope": "global",
    "name": "Голубые фишки",
    "sort_order": 10,
    "archived": False,
}
_USER_SET = {
    "set_id": "set-mine",
    "key": "mine",
    "scope": "user",
    "name": "Мои",
    "sort_order": 0,
    "archived": False,
    "owner_user_id": "u-42",
}
_MEMBERSHIP = {"set_id": "set-blue-chips", "ticker": "SBER", "sort_order": 0}
_SERIES_MAP = {"Si": {"name": "Доллар США", "sort_order": 1, "underlying_ticker": None}}
_USER_STATE = {
    "revision": 3,
    "sets": [_USER_SET],
    "memberships": [{"set_id": "set-mine", "ticker": "SBER", "sort_order": 0}],
    "hidden_set_ids": ["set-blue-chips"],
    "order": ["set-mine", "set-blue-chips"],
}
_SNAPSHOT = {
    "catalog_revision": 17,
    "items": [_ITEM],
    "sets": [_SET],
    "memberships": [_MEMBERSHIP],
    "series": _SERIES_MAP,
}


def _validator(def_name: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- list ------------------------------------------------------------------

def test_list_request_no_filters(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.list.request.v1", "request_id": "r1"}
    _validator("listRequest", registry).validate(msg)  # does not raise


def test_list_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.list.response.v1", "request_id": "r1",
        "items": [_ITEM],
        "groups": [{"key": "Stocks", "name": "Акции", "order": 3}],
        "assets": {"SBER": {"name": "Сбербанк"}},
    }
    _validator("listResponse", registry).validate(msg)  # does not raise


def test_list_response_missing_groups_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.list.response.v1", "request_id": "r1",
        "items": [_ITEM], "assets": {},
    }
    with pytest.raises(ValidationError):
        _validator("listResponse", registry).validate(msg)


# --- get ---------------------------------------------------------------

def test_get_request_and_response_valid(registry):
    req = {"channel": "instrument", "schema": "afbws.instrument.get.request.v1", "request_id": "r1", "ticker": "SBER"}
    _validator("getRequest", registry).validate(req)  # does not raise
    resp = {"channel": "instrument", "schema": "afbws.instrument.get.response.v1", "request_id": "r1", "item": _ITEM}
    _validator("getResponse", registry).validate(resp)  # does not raise


# --- pool (manager only, meta vs slice) -------------------------------------

def test_pool_request_source_required(registry):
    from jsonschema import ValidationError

    msg = {"channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1"}
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


def test_pool_request_moex_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1", "source": "moex"}
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_request_bf_id_with_exchange_market(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "source": "arena", "exchange": "MOEX", "market": "stock", "query": "sber",
    }
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_response_meta_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "exchanges": ["MOEX"], "markets": [{"exchange": "MOEX", "market": "stock"}],
    }
    _validator("poolResponse", registry).validate(msg)  # does not raise


def test_pool_response_slice_valid_with_null_group(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "arena", "exchange": "MOEX", "market": "stock", "items": [_POOL_ITEM],
    }
    _validator("poolResponse", registry).validate(msg)  # does not raise


def test_pool_response_cannot_mix_meta_and_slice_shapes(registry):
    """oneOf(meta, slice) — a message can't satisfy both at once."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "exchanges": ["MOEX"], "markets": [],
        "exchange": "MOEX", "market": "stock", "items": [],
    }
    with pytest.raises(ValidationError):
        _validator("poolResponse", registry).validate(msg)


# --- apply (manager only, bulk-replace) -------------------------------------

def test_apply_request_and_response_valid(registry):
    payload = {
        "items": [_ITEM],
        "groups": [{"key": "Stocks", "name": "Акции"}],
        "assets": {"SBER": {"name": "Сбербанк"}},
    }
    req = {
        "channel": "instrument", "schema": "afbws.instrument.apply.request.v1", "request_id": "r1",
        **payload,
    }
    _validator("applyRequest", registry).validate(req)  # does not raise
    resp = {
        "channel": "instrument", "schema": "afbws.instrument.apply.response.v1", "request_id": "r1",
        **payload,
    }
    _validator("applyResponse", registry).validate(resp)  # does not raise


def test_apply_request_unassigned_item_null_group(registry):
    payload = {
        "items": [{**_ITEM, "group": None}],
        "groups": [{"key": "Stocks", "name": "Акции"}],
        "assets": {},
    }
    req = {"channel": "instrument", "schema": "afbws.instrument.apply.request.v1", "request_id": "r1", **payload}
    _validator("applyRequest", registry).validate(req)  # does not raise


# --- resolve -----------------------------------------------------------

def test_resolve_request_draft_or_tradeplan_id(registry):
    by_draft = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.request.v1", "request_id": "r1",
        "bf_id": "arena", "draft": {"ticker": "SBER"},
    }
    _validator("resolveRequest", registry).validate(by_draft)  # does not raise
    by_id = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.request.v1", "request_id": "r1",
        "bf_id": "arena", "tradeplan_id": "tp-1",
    }
    _validator("resolveRequest", registry).validate(by_id)  # does not raise


def test_resolve_request_bf_id_required(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.request.v1", "request_id": "r1",
        "tradeplan_id": "tp-1",
    }
    with pytest.raises(ValidationError):
        _validator("resolveRequest", registry).validate(msg)


def test_resolve_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.resolve.response.v1", "request_id": "r1",
        "item": _ITEM,
        "binding": {"account_id": "1000316", "symbol": "SBER@MISX"},
        "broker_instrument": {"lot_size": 10, "tradable": True},
    }
    _validator("resolveResponse", registry).validate(msg)  # does not raise


# --- detail (lightweight live broker lookup, no draft/plan) ----------------

def test_detail_request_requires_bf_id_and_ticker(registry):
    from jsonschema import ValidationError

    msg = {"channel": "instrument", "schema": "afbws.instrument.detail.request.v1", "request_id": "r1", "bf_id": "arena"}
    with pytest.raises(ValidationError):
        _validator("detailRequest", registry).validate(msg)


def test_detail_request_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.detail.request.v1", "request_id": "r1",
        "bf_id": "arena", "ticker": "SBER",
    }
    _validator("detailRequest", registry).validate(msg)  # does not raise


def test_detail_response_valid(registry):
    """Same shape as resolveResponse, incl. a `broker_instrument` without a
    `symbol` key — to_broker_instrument_dict() strips it (lives in binding)."""
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.detail.response.v1", "request_id": "r1",
        "item": _ITEM,
        "binding": {"account_id": "1000316", "symbol": "SBER@MISX"},
        "broker_instrument": {"lot_size": 10, "tradable": True, "long_initial_margin": "3574.4"},
    }
    _validator("detailResponse", registry).validate(msg)  # does not raise


def test_detail_response_missing_broker_instrument_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.detail.response.v1", "request_id": "r1",
        "item": _ITEM, "binding": {},
    }
    with pytest.raises(ValidationError):
        _validator("detailResponse", registry).validate(msg)


# --- phase 2: catalogSetEntry / setMembership / series / userState ---------

def test_catalog_set_entry_global_and_user_valid(registry):
    _validator("catalogSetEntry", registry).validate(_SET)  # does not raise
    _validator("catalogSetEntry", registry).validate(_USER_SET)  # does not raise


def test_catalog_set_entry_scope_system_rejected(registry):
    """The system/global division is gone — only global|user exist in this form."""
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSetEntry", registry).validate({**_SET, "scope": "system"})


def test_catalog_set_entry_requires_archived_and_sort_order(registry):
    from jsonschema import ValidationError

    for missing in ("set_id", "key", "scope", "name", "sort_order", "archived"):
        payload = {k: v for k, v in _SET.items() if k != missing}
        with pytest.raises(ValidationError):
            _validator("catalogSetEntry", registry).validate(payload)


def test_catalog_set_entry_rejects_unknown_property(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSetEntry", registry).validate({**_SET, "parent_id": "x"})


def test_catalog_set_entry_owner_user_id_nullable(registry):
    _validator("catalogSetEntry", registry).validate({**_SET, "owner_user_id": None})  # does not raise


def test_set_membership_valid(registry):
    _validator("setMembership", registry).validate(_MEMBERSHIP)  # does not raise


def test_set_membership_requires_sort_order(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("setMembership", registry).validate({"set_id": "set-blue-chips", "ticker": "SBER"})


def test_set_membership_rejects_unknown_property(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("setMembership", registry).validate({**_MEMBERSHIP, "group": "Stocks"})


def test_catalog_series_and_map_valid(registry):
    _validator("catalogSeries", registry).validate({"name": None})  # does not raise
    _validator("catalogSeriesMap", registry).validate(_SERIES_MAP)  # does not raise
    _validator("catalogSeriesMap", registry).validate({})  # does not raise


def test_catalog_series_requires_name(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSeries", registry).validate({"sort_order": 1})


def test_catalog_series_map_rejects_unknown_property_in_value(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSeriesMap", registry).validate({"Si": {"name": "Si", "asset": "USD"}})


def test_user_state_valid(registry):
    _validator("userState", registry).validate(_USER_STATE)  # does not raise


def test_user_state_requires_every_section(registry):
    from jsonschema import ValidationError

    for missing in ("revision", "sets", "memberships", "hidden_set_ids", "order"):
        payload = {k: v for k, v in _USER_STATE.items() if k != missing}
        with pytest.raises(ValidationError):
            _validator("userState", registry).validate(payload)


def test_user_state_revision_not_negative(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("userState", registry).validate({**_USER_STATE, "revision": -1})


# --- phase 2: catalog (snapshot in the set-based form) ----------------------

def test_catalog_request_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.catalog.request.v1", "request_id": "r1"}
    _validator("catalogRequest", registry).validate(msg)  # does not raise


def test_catalog_request_rejects_filters(registry):
    """No filters, no paging — the snapshot is whole or nothing."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.request.v1", "request_id": "r1",
        "set_id": "set-blue-chips",
    }
    with pytest.raises(ValidationError):
        _validator("catalogRequest", registry).validate(msg)


def test_catalog_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT,
    }
    _validator("catalogResponse", registry).validate(msg)  # does not raise


def test_catalog_response_listing_without_membership_is_valid(registry):
    """A listing in no set at all is normal — it stays visible to a manager."""
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT, "items": [{**_ITEM, "group": None}], "memberships": [],
    }
    _validator("catalogResponse", registry).validate(msg)  # does not raise


def test_catalog_response_optional_user_overlay(registry):
    """Declared now, not emitted by the phase 2 backend — but it must validate."""
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT, "user": _USER_STATE,
    }
    _validator("catalogResponse", registry).validate(msg)  # does not raise


def test_catalog_response_requires_catalog_revision(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **{k: v for k, v in _SNAPSHOT.items() if k != "catalog_revision"},
    }
    with pytest.raises(ValidationError):
        _validator("catalogResponse", registry).validate(msg)


def test_catalog_response_rejects_legacy_groups_assets(registry):
    """The legacy group/asset projection has no place in the new form."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT, "groups": [{"key": "Stocks", "name": "Акции"}], "assets": {},
    }
    with pytest.raises(ValidationError):
        _validator("catalogResponse", registry).validate(msg)


# --- phase 2: commit (manager-only CAS delta) -------------------------------

def test_commit_request_minimal_is_just_a_base_revision(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17,
    }
    _validator("commitRequest", registry).validate(msg)  # does not raise


def test_commit_request_without_base_revision_rejected(registry):
    """No CAS guard -> not a commit: the whole point over legacy `apply`."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "sets": [{"name": "Новая"}],
    }
    with pytest.raises(ValidationError):
        _validator("commitRequest", registry).validate(msg)


def test_commit_request_negative_base_revision_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": -1,
    }
    with pytest.raises(ValidationError):
        _validator("commitRequest", registry).validate(msg)


def test_commit_request_full_delta_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17,
        "sets": [
            {"name": "Новая подборка"},
            {"set_id": "set-blue-chips", "key": "blue-chips", "name": "Голубые фишки", "sort_order": 10, "archived": False},
        ],
        "remove_sets": ["set-old"],
        "members": [{"set_id": "set-blue-chips", "add": ["GAZP"], "remove": ["LKOH"], "order": ["SBER", "GAZP"]}],
        "listings": [{**_ITEM, "group": None}],
        "archive_listings": [{"ticker": "SIU5", "reason": "expired"}],
        "series": [{"series_code": "Si", "name": "Доллар США", "sort_order": 1, "underlying_ticker": None}],
        "reason": "Пересборка подборок",
    }
    _validator("commitRequest", registry).validate(msg)  # does not raise


def test_commit_request_rejects_unknown_section(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17, "groups": [{"key": "Stocks", "name": "Акции"}],
    }
    with pytest.raises(ValidationError):
        _validator("commitRequest", registry).validate(msg)


def test_commit_request_listings_keep_instrument_class_gating(registry):
    """Reusing instrument.v1 verbatim is the point: `isin` stays stock-only."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17,
        "listings": [{**_ITEM, "market": "futures", "group": None, "isin": "RU0009029540"}],
    }
    with pytest.raises(ValidationError):
        _validator("commitRequest", registry).validate(msg)


def test_set_upsert_create_without_set_id(registry):
    _validator("setUpsert", registry).validate({"name": "Новая"})  # does not raise
    _validator("setUpsert", registry).validate(
        {"set_id": "set-blue-chips", "key": "blue-chips", "name": "Голубые фишки", "sort_order": 10, "archived": True}
    )  # does not raise


def test_set_upsert_requires_name(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("setUpsert", registry).validate({"set_id": "set-blue-chips", "sort_order": 3})


def test_set_upsert_rejects_scope_and_owner(registry):
    """scope/owner are the server's business, never a client's."""
    from jsonschema import ValidationError

    for extra in ({"scope": "global"}, {"owner_user_id": "u-42"}):
        with pytest.raises(ValidationError):
            _validator("setUpsert", registry).validate({"name": "Новая", **extra})


def test_members_edit_requires_set_id(registry):
    from jsonschema import ValidationError

    _validator("membersEdit", registry).validate({"set_id": "set-blue-chips"})  # does not raise
    with pytest.raises(ValidationError):
        _validator("membersEdit", registry).validate({"add": ["SBER"]})


def test_members_edit_rejects_unknown_property(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("membersEdit", registry).validate({"set_id": "set-blue-chips", "replace": ["SBER"]})


def test_listing_archival_requires_ticker(registry):
    from jsonschema import ValidationError

    _validator("listingArchival", registry).validate({"ticker": "SIU5"})  # does not raise
    with pytest.raises(ValidationError):
        _validator("listingArchival", registry).validate({"reason": "expired"})


def test_series_upsert_requires_series_code(registry):
    from jsonschema import ValidationError

    _validator("seriesUpsert", registry).validate({"series_code": "Si"})  # does not raise
    with pytest.raises(ValidationError):
        _validator("seriesUpsert", registry).validate({"name": "Доллар США"})


def test_series_upsert_rejects_unknown_property(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("seriesUpsert", registry).validate({"series_code": "Si", "archived": True})


def test_commit_response_is_a_full_snapshot(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.response.v1", "request_id": "r1",
        **_SNAPSHOT, "catalog_revision": 18,
        "applied": {"sets_upserted": 2, "memberships_added": 1, "listings_archived": 0},
    }
    _validator("commitResponse", registry).validate(msg)  # does not raise


def test_commit_response_applied_counts_must_be_integers(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.response.v1", "request_id": "r1",
        **_SNAPSHOT, "applied": {"sets_upserted": "2"},
    }
    with pytest.raises(ValidationError):
        _validator("commitResponse", registry).validate(msg)


def test_commit_response_requires_the_whole_snapshot(registry):
    from jsonschema import ValidationError

    for missing in ("catalog_revision", "items", "sets", "memberships", "series"):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.commit.response.v1", "request_id": "r1",
            **{k: v for k, v in _SNAPSHOT.items() if k != missing},
        }
        with pytest.raises(ValidationError):
            _validator("commitResponse", registry).validate(msg)


def test_commit_response_does_not_accept_catalog_schema_id(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT,
    }
    with pytest.raises(ValidationError):
        _validator("commitResponse", registry).validate(msg)


# --- phase 2: user (personal sets/overlay; unsupported_action until phase 3) -

def test_user_request_minimal_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.user.request.v1", "request_id": "r1",
        "base_revision": 0,
    }
    _validator("userRequest", registry).validate(msg)  # does not raise


def test_user_request_full_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.user.request.v1", "request_id": "r1",
        "base_revision": 3,
        "sets": [{"name": "Мои"}],
        "remove_sets": ["set-old-personal"],
        "members": [{"set_id": "set-mine", "add": ["SBER"]}],
        "hidden_set_ids": ["set-blue-chips"],
        "order": ["set-mine", "set-blue-chips"],
    }
    _validator("userRequest", registry).validate(msg)  # does not raise


def test_user_request_without_base_revision_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.user.request.v1", "request_id": "r1",
        "order": ["set-mine"],
    }
    with pytest.raises(ValidationError):
        _validator("userRequest", registry).validate(msg)


def test_user_request_rejects_global_only_sections(registry):
    """No listings/series/reason here — the personal overlay never writes the
    global catalog."""
    from jsonschema import ValidationError

    for extra in ({"listings": [_ITEM]}, {"series": [{"series_code": "Si"}]}, {"reason": "x"}):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.user.request.v1", "request_id": "r1",
            "base_revision": 3, **extra,
        }
        with pytest.raises(ValidationError):
            _validator("userRequest", registry).validate(msg)


def test_user_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.user.response.v1", "request_id": "r1",
        "user_revision": 4, "user": _USER_STATE,
    }
    _validator("userResponse", registry).validate(msg)  # does not raise


def test_user_response_requires_user_state(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.user.response.v1", "request_id": "r1",
        "user_revision": 4,
    }
    with pytest.raises(ValidationError):
        _validator("userResponse", registry).validate(msg)


def test_user_response_carries_no_catalog_revision(registry):
    """The personal write never moves the global catalog."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.user.response.v1", "request_id": "r1",
        "user_revision": 4, "user": _USER_STATE, "catalog_revision": 17,
    }
    with pytest.raises(ValidationError):
        _validator("userResponse", registry).validate(msg)


# --- error ---------------------------------------------------------------

def test_error_response_minimal_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "not_found", "message": "Instrument not found",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_manager_only_uses_forbidden_code(registry):
    """pool/apply reject non-managers with the shared `forbidden` code —
    exercised at the handler level, just checking the vocabulary here."""
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "forbidden", "message": "manager only",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_bf_offline_code(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "bf_offline", "message": "BF arena is not connected",
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_unknown_code_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "totally_unknown", "message": "x",
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


def test_error_response_conflict_carries_current_catalog_revision(registry):
    """A stale commit.base_revision comes back as `conflict` + the revision to
    rebase onto."""
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "conflict", "message": "catalog moved on",
        "details": {"catalog_revision": 19},
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_unsupported_action_for_apply_and_user(registry):
    """Phase 2: `apply` is no longer served and `user` is not served yet."""
    for message in ("apply is superseded by commit", "user sets arrive in phase 3"):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
            "code": "unsupported_action", "message": message,
        }
        _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_details_full_shape_valid(registry):
    details = {
        "catalog_revision": 19,
        "user_revision": 4,
        "set_ids": ["set-blue-chips"],
        "tickers": ["SBER"],
    }
    _validator("errorDetails", registry).validate(details)  # does not raise
    _validator("errorDetails", registry).validate({})  # does not raise


def test_error_details_rejects_unknown_property(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("errorDetails", registry).validate({"revision": 19})


def test_error_response_details_must_be_typed(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.error.response.v1", "request_id": "r1",
        "code": "conflict", "message": "x", "details": {"catalog_revision": "19"},
    }
    with pytest.raises(ValidationError):
        _validator("errorResponse", registry).validate(msg)


# --- structural sanity ------------------------------------------------------

def _channel_doc():
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "instrument.channel.v1.json"
    )
    return json.loads(schema_path.read_text())


def test_every_phase2_message_is_reachable_from_the_channel_oneof():
    branches = {b["$ref"].rsplit("/", 1)[-1] for b in _channel_doc()["oneOf"]}
    assert {
        "catalogRequest", "catalogResponse",
        "commitRequest", "commitResponse",
        "userRequest", "userResponse",
    } <= branches


def test_legacy_list_and_apply_are_kept_but_marked_deprecated():
    """Additive change: the legacy pair stays in the schema (old frontends keep
    parsing), it is only documented as deprecated."""
    defs = _channel_doc()["$defs"]
    for name in ("listRequest", "listResponse", "applyRequest", "applyResponse"):
        assert name in defs
    for name in ("listRequest", "applyRequest"):
        assert "DEPRECATED" in defs[name].get("description", "")


def test_no_phase2_def_allows_additional_properties():
    defs = _channel_doc()["$defs"]
    for name in (
        "catalogSetEntry", "setMembership", "catalogSeries", "userState", "errorDetails",
        "catalogRequest", "catalogResponse", "commitRequest", "commitResponse",
        "setUpsert", "membersEdit", "listingArchival", "seriesUpsert",
        "userRequest", "userResponse",
    ):
        assert defs[name].get("additionalProperties") is False, name



def test_no_message_def_declares_a_type_property():
    """New channels forbid `type`: routing is channel+schema only."""
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "instrument.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"


def test_no_binding_field_on_the_curated_entity():
    """The plan explicitly forbids broker bindings inside the catalog entity
    itself — binding only ever appears in resolve's response."""
    from pathlib import Path

    schema_path = Path(__file__).resolve().parents[2] / "spec" / "schemas" / "instrument.v1.json"
    doc = json.loads(schema_path.read_text())
    props = set(doc.get("properties", {}))
    assert not (props & {"bindings", "venues", "bf_id", "broker_symbol", "binding"})
