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

# --- federated catalog: assets / series fixtures ----------------------------

_SERIES_MAP = {"Si": {"name": "Доллар США", "underlying_ticker": None}}

# --- assets (the level between a listing and a set) fixtures ----------------

_CATALOG_MEMBER_BR = {"kind": "series", "code": "BR", "label": "Нефть Brent", "market": "futures"}
_CATALOG_MEMBER_BRM = {"kind": "series", "code": "BRM", "label": "Нефть Brent mini", "market": "futures"}
_CATALOG_MEMBER_SBER = {"kind": "listing", "code": "SBER", "label": "Сбер", "market": "stock"}

_ASSET = {
    "asset_id": "asset-brent",
    "name": "Нефть Brent",
    "reference_series_code": "BR",
    "members": [_CATALOG_MEMBER_BR, _CATALOG_MEMBER_BRM],
}
_SBER_ASSET = {
    "asset_id": "asset-sber",
    "name": "Сбербанк",
    "reference_series_code": None,
    "members": [_CATALOG_MEMBER_SBER],
}
_SNAPSHOT = {
    "catalog_revision": 17,
    "assets": [_ASSET, _SBER_ASSET],
    "items": [_ITEM],
    "series": _SERIES_MAP,
}

# --- catalog sources / on-demand refresh fixtures ---------------------------

_SOURCE = {
    "source_id": "moex",
    "kind": "moex",
    "title": "MOEX ISS",
    "available": True,
    "last_refresh_at": "2026-08-14T03:15:00Z",
    "listing_count": 540,
}
_REPORT = {
    "applied": True,
    "revision_before": 17,
    "revision_after": 18,
    "added": ["MISX:RFUD:BRV6"],
    "updated": ["MISX:TQBR:SBER"],
    "resurrected": [],
    "archived": [{"key": "MISX:RFUD:BRU6", "reason": "expired"}],
    "new_series": ["BRM"],
    "absent_from_catalog": ["MISX:TQBR:OZON"],
    "rows_without_series": ["MISX:RFUD:ZZU6"],
}

# --- catalog reorg (collections / asset_sets / inventory / suggestions) ------

_COLLECTION = {
    "collection_id": "col-stocks",
    "parent_id": None,
    "name": "Акции",
    "pending": False,
}
_ASSET_SET_GLOBAL = {
    "set_id": "set-blue",
    "scope": "global",
    "name": "Голубые",
    "asset_ids": ["asset-sber"],
    "visibility_tier": "manager",
}
_ASSET_SET_USER = {
    "set_id": "set-mine",
    "scope": "user",
    "name": "Мои",
    "owner_user_id": "u-42",
    "asset_ids": ["asset-sber"],
}
# The caller's own sets, carrying their membership inline.
_USER_STATE = {
    "revision": 3,
    "asset_sets": [_ASSET_SET_USER],
}
_INVENTORY_LISTING = {
    "kind": "listing",
    "instrument_type": "stock",
    "instrument_key": "MISX:TQBR:SBER",
    "ticker": "SBER",
    "exchange": "MOEX",
    "board": "TQBR",
    "market": "stock",
    "source": "moex",
}
_INVENTORY_SERIES = {
    "kind": "series",
    "instrument_type": "series",
    "series_code": "BR",
    "source": "moex",
    "market": "futures",
}
_SUGGESTION = {
    "suggestion_id": "sug-1",
    "subject_type": "series",
    "subject_ref": "BRM",
    "reason": "new_series",
    "status": "pending",
}


def _validator(def_name: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- get ---------------------------------------------------------------

def test_get_request_and_response_valid(registry):
    req = {"channel": "instrument", "schema": "afbws.instrument.get.request.v1", "request_id": "r1", "ticker": "SBER"}
    _validator("getRequest", registry).validate(req)  # does not raise
    resp = {"channel": "instrument", "schema": "afbws.instrument.get.response.v1", "request_id": "r1", "item": _ITEM}
    _validator("getResponse", registry).validate(resp)  # does not raise


# --- pool (manager only, paged MOEX universe) --------------------------------

def test_pool_request_minimal_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1"}
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_request_source_moex_optional(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "source": "moex",
    }
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_request_bf_id_rejected(registry):
    """Broker/BF pool is not served — a bf_id must fail schema, not just the handler."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "source": "arena",
    }
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


def test_pool_request_full_filters_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "source": "moex", "query": "sber", "kind": "listing", "market": "stock",
        "limit": 50, "cursor": "page-2",
    }
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_request_rejects_exchange(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "exchange": "MOEX", "market": "stock",
    }
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


@pytest.mark.parametrize("limit", [0, -1, 201])
def test_pool_request_limit_bounds_rejected(registry, limit):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "limit": limit,
    }
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


@pytest.mark.parametrize("limit", [1, 50, 200])
def test_pool_request_limit_bounds_accepted(registry, limit):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "limit": limit,
    }
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_request_empty_cursor_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "cursor": "",
    }
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


def test_pool_limit_schema_default_and_bounds():
    limit = _channel_doc()["$defs"]["poolRequest"]["properties"]["limit"]
    assert limit["default"] == 50
    assert limit["minimum"] == 1
    assert limit["maximum"] == 200


def test_pool_cursor_and_total_semantics_are_documented():
    """Cursor binding and total-after-filters cannot be encoded as cursor bytes;
    the schema states the contract the backend must enforce."""
    defs = _channel_doc()["$defs"]
    cursor = defs["poolRequest"]["properties"]["cursor"]["description"].lower()
    for needle in ("query", "kind", "market", "snapshot", "conflict"):
        assert needle in cursor, needle
    assert "validation_error" in cursor
    total = defs["poolResponse"]["properties"]["total"]["description"].lower()
    assert "filter" in total
    assert "before paging" in total
    next_cursor = defs["poolResponse"]["properties"]["next_cursor"]["description"].lower()
    assert "fetched_at" in next_cursor
    req = defs["poolRequest"]["description"].lower()
    assert "defaults to 50" in req
    assert "capped at 200" in req


def test_pool_request_query_too_long_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "query": "x" * 201,
    }
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


def test_pool_request_listing_cannot_ask_for_futures(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "kind": "listing", "market": "futures",
    }
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


def test_pool_request_series_cannot_ask_for_stock(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "kind": "series", "market": "stock",
    }
    with pytest.raises(ValidationError):
        _validator("poolRequest", registry).validate(msg)


def test_pool_request_series_with_futures_market_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.request.v1", "request_id": "r1",
        "kind": "series", "market": "futures",
    }
    _validator("poolRequest", registry).validate(msg)  # does not raise


def test_pool_response_page_valid(registry):
    listing = {"kind": "listing", "listing": {**_ITEM, "group": None}}
    series = {
        "kind": "series", "code": "BR", "name": "Нефть Brent",
        "source": "moex", "market": "futures", "underlying": "BR",
    }
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "fetched_at": "2026-08-16T12:00:00Z",
        "total": 2, "next_cursor": "next", "entries": [listing, series],
    }
    _validator("poolResponse", registry).validate(msg)  # does not raise


def test_pool_response_last_page_null_cursor(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "fetched_at": "2026-08-16T12:00:00Z",
        "total": 0, "next_cursor": None, "entries": [],
    }
    _validator("poolResponse", registry).validate(msg)  # does not raise


def test_pool_response_rejects_legacy_meta_shape(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "exchanges": ["MOEX"], "markets": [{"exchange": "MOEX", "market": "stock"}],
    }
    with pytest.raises(ValidationError):
        _validator("poolResponse", registry).validate(msg)


def test_pool_response_rejects_legacy_slice_shape(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "exchange": "MOEX", "market": "stock", "items": [_POOL_ITEM],
    }
    with pytest.raises(ValidationError):
        _validator("poolResponse", registry).validate(msg)


def test_pool_response_requires_page_fields(registry):
    from jsonschema import ValidationError

    base = {
        "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
        "source": "moex", "fetched_at": "2026-08-16T12:00:00Z",
        "total": 0, "next_cursor": None, "entries": [],
    }
    for missing in ("source", "fetched_at", "total", "next_cursor", "entries"):
        with pytest.raises(ValidationError):
            _validator("poolResponse", registry).validate({k: v for k, v in base.items() if k != missing})


def test_pool_listing_entry_rejects_futures_market(registry):
    from jsonschema import ValidationError

    future_listing = {
        **_ITEM, "ticker": "BRV6", "market": "futures", "group": None, "board": "RFUD",
    }
    future_listing.pop("isin", None)
    with pytest.raises(ValidationError):
        _validator("poolListingEntry", registry).validate({"kind": "listing", "listing": future_listing})


def test_pool_listing_entry_stock_valid(registry):
    _validator("poolListingEntry", registry).validate(
        {"kind": "listing", "listing": {**_ITEM, "group": None}}
    )


def test_pool_series_entry_requires_code_and_futures_market(registry):
    from jsonschema import ValidationError

    valid = {
        "kind": "series", "code": "BR", "name": "Нефть Brent",
        "source": "moex", "market": "futures",
    }
    _validator("poolSeriesEntry", registry).validate(valid)
    with pytest.raises(ValidationError):
        _validator("poolSeriesEntry", registry).validate({k: v for k, v in valid.items() if k != "code"})
    with pytest.raises(ValidationError):
        _validator("poolSeriesEntry", registry).validate({**valid, "market": "stock"})
    with pytest.raises(ValidationError):
        _validator("poolSeriesEntry", registry).validate({**valid, "source": "arena"})


def test_pool_entry_discriminator_rejects_unknown_kind(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("poolEntry", registry).validate({"kind": "contract", "code": "BRV6"})
    with pytest.raises(ValidationError):
        _validator("poolEntry", registry).validate({"kind": "listing"})
    with pytest.raises(ValidationError):
        _validator("poolResponse", registry).validate({
            "channel": "instrument", "schema": "afbws.instrument.pool.response.v1", "request_id": "r1",
            "source": "moex", "fetched_at": "2026-08-16T12:00:00Z",
            "total": 1, "next_cursor": None,
            "entries": [{"kind": "listing", "code": "SBER", "name": "Сбер", "source": "moex", "market": "stock"}],
        })


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


# --- catalogAsset / catalogAssetMember --------------------------------------

def test_catalog_asset_valid(registry):
    _validator("catalogAsset", registry).validate(_ASSET)  # does not raise
    _validator("catalogAsset", registry).validate(_SBER_ASSET)  # null reference series


def test_catalog_asset_requires_identity_name_and_members(registry):
    from jsonschema import ValidationError

    for missing in ("asset_id", "name", "members"):
        payload = {k: v for k, v in _ASSET.items() if k != missing}
        with pytest.raises(ValidationError):
            _validator("catalogAsset", registry).validate(payload)


def test_catalog_asset_reference_series_is_optional(registry):
    payload = {k: v for k, v in _ASSET.items() if k != "reference_series_code"}
    _validator("catalogAsset", registry).validate(payload)  # does not raise


def test_catalog_asset_has_no_scope_or_owner(registry):
    """Assets are always global — personal sets reuse the very same ones."""
    from jsonschema import ValidationError

    for extra in ({"scope": "user"}, {"owner_user_id": "u-42"}):
        with pytest.raises(ValidationError):
            _validator("catalogAsset", registry).validate({**_ASSET, **extra})


def test_catalog_asset_member_valid_for_both_kinds(registry):
    for member in (_CATALOG_MEMBER_BR, _CATALOG_MEMBER_BRM, _CATALOG_MEMBER_SBER):
        _validator("catalogAssetMember", registry).validate(member)  # does not raise


def test_catalog_asset_member_series_must_be_futures(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogAssetMember", registry).validate(
            {**_CATALOG_MEMBER_BR, "market": "stock"}
        )


def test_catalog_asset_member_listing_cannot_be_futures(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogAssetMember", registry).validate(
            {**_CATALOG_MEMBER_SBER, "market": "futures"}
        )


def test_catalog_asset_member_requires_every_field(registry):
    from jsonschema import ValidationError

    for missing in ("kind", "code", "label", "market"):
        payload = {k: v for k, v in _CATALOG_MEMBER_SBER.items() if k != missing}
        with pytest.raises(ValidationError):
            _validator("catalogAssetMember", registry).validate(payload)


def test_catalog_asset_member_rejects_old_edge_fields(registry):
    from jsonschema import ValidationError

    for extra in ({"asset_id": "asset-sber"}, {"sort_order": 0}, {"member_type": "listing"}, {"member_ref": "SBER"}):
        with pytest.raises(ValidationError):
            _validator("catalogAssetMember", registry).validate({**_CATALOG_MEMBER_SBER, **extra})


def test_catalog_series_and_map_valid(registry):
    _validator("catalogSeries", registry).validate({"name": None})  # does not raise
    _validator("catalogSeriesMap", registry).validate(_SERIES_MAP)  # does not raise
    _validator("catalogSeriesMap", registry).validate({})  # does not raise


def test_catalog_series_requires_name(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSeries", registry).validate({"underlying_ticker": None})


def test_catalog_series_map_rejects_unknown_property_in_value(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSeriesMap", registry).validate({"Si": {"name": "Si", "asset": "USD"}})


def test_user_state_valid(registry):
    _validator("userState", registry).validate(_USER_STATE)  # does not raise


def test_user_state_sets_carry_their_membership_inline(registry):
    """The overlay states membership as asset_sets[].asset_ids — assetSetView,
    the same object the global catalog uses. There is no parallel edge array."""
    from jsonschema import ValidationError

    _validator("userState", registry).validate(
        {**_USER_STATE, "asset_sets": [{**_ASSET_SET_USER, "asset_ids": ["asset-sber", "asset-brent"]}]}
    )  # does not raise
    with pytest.raises(ValidationError):
        _validator("userState", registry).validate({**_USER_STATE, "memberships": []})
    with pytest.raises(ValidationError):
        _validator("userState", registry).validate(
            {**_USER_STATE, "asset_sets": [{k: v for k, v in _ASSET_SET_USER.items() if k != "asset_ids"}]}
        )


def test_user_state_requires_every_section(registry):
    from jsonschema import ValidationError

    for missing in ("revision", "asset_sets"):
        payload = {k: v for k, v in _USER_STATE.items() if k != missing}
        with pytest.raises(ValidationError):
            _validator("userState", registry).validate(payload)


def test_user_state_revision_not_negative(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("userState", registry).validate({**_USER_STATE, "revision": -1})


# --- catalog (the curated snapshot) -----------------------------------------

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


def test_catalog_request_is_documented_as_role_aware_same_form():
    catalog_request = _channel_doc()["$defs"]["catalogRequest"]
    text = " ".join(
        (catalog_request.get("title", ""), catalog_request.get("description", ""))
    ).lower()
    assert "any authenticated" in text
    assert "identical for a user and a manager" in text
    assert "manager-only" not in text


def test_catalog_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT,
    }
    _validator("catalogResponse", registry).validate(msg)  # does not raise


def test_catalog_response_has_no_legacy_sets_section(registry):
    """Named sets live in `asset_sets` only — the old shadow `sets` section is
    gone, and a snapshot that still carries one is rejected outright."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT, "sets": [_ASSET_SET_GLOBAL],
    }
    with pytest.raises(ValidationError):
        _validator("catalogResponse", registry).validate(msg)


def test_catalog_response_listing_without_membership_is_valid(registry):
    """A listing in no asset, and an asset in no set, are normal states — both
    stay in the manager snapshot. Nested arrays are empty rather than omitted."""
    empty_asset = {**_SBER_ASSET, "members": []}
    empty_set = {**_ASSET_SET_GLOBAL, "asset_ids": []}
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT, "items": [{**_ITEM, "group": None}], "assets": [empty_asset],
        "asset_sets": [empty_set],
    }
    _validator("catalogResponse", registry).validate(msg)  # does not raise


def test_catalog_response_requires_nested_assets_not_parallel_edges(registry):
    from jsonschema import ValidationError

    for missing in ("assets",):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
            **{k: v for k, v in _SNAPSHOT.items() if k != missing},
        }
        with pytest.raises(ValidationError):
            _validator("catalogResponse", registry).validate(msg)


def test_catalog_response_rejects_parallel_membership_arrays(registry):
    from jsonschema import ValidationError

    for extra in ({"asset_members": []}, {"memberships": []}):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
            **_SNAPSHOT, **extra,
        }
        with pytest.raises(ValidationError):
            _validator("catalogResponse", registry).validate(msg)


def test_catalog_response_optional_user_overlay(registry):
    """The personal overlay rides along with the global snapshot."""
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


def test_catalog_response_rejects_legacy_groups(registry):
    """The legacy group projection has no place in the new form."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT, "groups": [{"key": "Stocks", "name": "Акции"}],
    }
    with pytest.raises(ValidationError):
        _validator("catalogResponse", registry).validate(msg)


def test_catalog_response_assets_is_not_the_legacy_asset_map(registry):
    """The name is reused for a different level: `assets` here is the array of
    curated assets, not the old series_code -> {name} map of `list`."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT, "assets": {"BR": {"name": "Нефть"}},
    }
    with pytest.raises(ValidationError):
        _validator("catalogResponse", registry).validate(msg)


# --- commit (manager-only CAS delta) ----------------------------------------

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


def test_commit_request_atomic_pending_pool_and_composition(registry):
    """A pending pool listing/series and the asset that contains them travel in
    one CAS commit. seriesUpsert stays the write form; listing is instrument.v1."""
    listing = {**_ITEM, "group": None}
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17,
        "listings": [listing],
        "series": [{"series_code": "BR", "name": "Нефть Brent", "underlying_ticker": "BR"}],
        "assets": [{
            "asset_id": "BR-41d4-a716",
            "name": "Нефть Brent",
            "members": [
                {"kind": "listing", "code": "SBER"},
                {"kind": "series", "code": "BR"},
            ],
        }],
    }
    _validator("commitRequest", registry).validate(msg)  # does not raise


def test_commit_request_full_delta_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17,
        "asset_sets": [
            {"set_id": "set-new", "name": "Новая подборка"},
            {"set_id": "set-blue-chips", "name": "Голубые фишки", "visibility_tier": "user"},
        ],
        "remove_asset_sets": ["set-old"],
        "asset_set_order": ["set-blue-chips", "set-new"],
        "assets": [
            {"asset_id": "asset-brent-new", "name": "Нефть Brent"},
            {
                "asset_id": "asset-brent", "name": "Нефть Brent",
                "reference_series_code": "BR",
                "members": [
                    {"kind": "series", "code": "BR"},
                    {"kind": "series", "code": "BRM"},
                ],
            },
        ],
        "remove_assets": ["asset-obsolete"],
        "asset_set_members": [
            {
                "set_id": "set-blue-chips", "add": ["asset-gazp"], "remove": ["asset-lkoh"],
                "order": ["asset-sber", "asset-gazp"],
            }
        ],
        "collections": [{"collection_id": "col-commodities", "name": "Сырьё"}],
        "remove_collections": ["col-old"],
        "collection_order": ["col-stocks", "col-commodities"],
        "collection_members": [
            {
                "collection_id": "col-commodities", "add": ["asset-brent"], "remove": ["asset-gold"],
                "order": ["asset-brent"],
            }
        ],
        "listings": [{**_ITEM, "group": None}],
        "archive_listings": [{"ticker": "SIU5", "reason": "expired"}],
        "series": [{"series_code": "Si", "name": "Доллар США", "underlying_ticker": None}],
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


def test_asset_set_upsert_requires_a_client_minted_set_id(registry):
    """set_id is always client-minted — an upsert without one (the old
    server-generates-on-create shape) is rejected, not treated as a create."""
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("assetSetUpsert", registry).validate({"name": "Новая"})
    _validator("assetSetUpsert", registry).validate(
        {"set_id": "set-new", "name": "Новая"}
    )  # does not raise — server INSERTs since set-new is unknown in the base snapshot
    _validator("assetSetUpsert", registry).validate(
        {"set_id": "set-blue-chips", "name": "Голубые фишки"}
    )  # does not raise — server UPDATEs since set-blue-chips is known


def test_asset_set_upsert_requires_name(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("assetSetUpsert", registry).validate({"set_id": "set-blue-chips"})


def test_asset_set_upsert_states_no_position(registry):
    """Order left the entity: it is stated once, wholesale, in
    commitRequest.asset_set_order."""
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("assetSetUpsert", registry).validate(
            {"set_id": "set-blue-chips", "name": "Голубые фишки", "sort_order": 10}
        )


def test_asset_upsert_requires_asset_id(registry):
    """asset_id is always client-minted — an assetUpsert without one (the old
    server-generates-on-create shape) is rejected, not treated as a create."""
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("assetUpsert", registry).validate({"name": "Нефть Brent"})
    _validator("assetUpsert", registry).validate(
        {"asset_id": "asset-brent-new", "name": "Нефть Brent"}
    )  # does not raise — server INSERTs since asset-brent-new is unknown in the base snapshot
    _validator("assetUpsert", registry).validate(
        {
            "asset_id": "asset-brent", "name": "Нефть Brent",
            "reference_series_code": None, "members": [],
        }
    )  # does not raise — server UPDATEs since asset-brent is known


def test_asset_upsert_requires_name(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("assetUpsert", registry).validate({"asset_id": "asset-brent"})


def test_asset_upsert_members_carry_no_asset_id_or_order(registry):
    """Composition is stated whole: the asset is implied, the position is the
    array index. Identity is kind+code, matching catalogAssetMember."""
    from jsonschema import ValidationError

    for extra in ({"asset_id": "asset-brent"}, {"sort_order": 0}, {"label": "x"}, {"market": "futures"}):
        with pytest.raises(ValidationError):
            _validator("assetMemberInput", registry).validate(
                {"kind": "series", "code": "BR", **extra}
            )


def test_asset_member_input_valid_and_gated_by_kind(registry):
    from jsonschema import ValidationError

    _validator("assetMemberInput", registry).validate({"kind": "listing", "code": "SBER"})
    with pytest.raises(ValidationError):
        _validator("assetMemberInput", registry).validate({"kind": "contract", "code": "BRV6"})
    with pytest.raises(ValidationError):
        _validator("assetMemberInput", registry).validate({"kind": "series"})
    with pytest.raises(ValidationError):
        _validator("assetMemberInput", registry).validate({"member_type": "listing", "member_ref": "SBER"})


def test_asset_upsert_rejects_unknown_property(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("assetUpsert", registry).validate({"name": "Нефть Brent", "set_id": "set-commodities"})


def test_commit_request_remove_assets_is_a_list_of_ids(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17, "remove_assets": ["asset-obsolete"],
    }
    _validator("commitRequest", registry).validate(msg)  # does not raise
    with pytest.raises(ValidationError):
        _validator("commitRequest", registry).validate({**msg, "remove_assets": [{"asset_id": "asset-obsolete"}]})


def test_members_edit_requires_set_id(registry):
    from jsonschema import ValidationError

    _validator("membersEdit", registry).validate({"set_id": "set-blue-chips"})  # does not raise
    with pytest.raises(ValidationError):
        _validator("membersEdit", registry).validate({"add": ["asset-sber"]})


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
        "applied": {"asset_sets_upserted": 2, "asset_set_members_added": 1, "listings_archived": 0},
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

    for missing in ("catalog_revision", "items", "assets", "series"):
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


# --- user (the caller's own personal sets) -----------------------------------

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
        "asset_sets": [{"set_id": "set-mine", "name": "Мои"}],
        "remove_asset_sets": ["set-old-personal"],
        "asset_set_members": [{"set_id": "set-mine", "add": ["asset-sber"]}],
        "asset_set_order": ["set-mine", "set-blue-chips"],
    }
    _validator("userRequest", registry).validate(msg)  # does not raise


def test_user_request_without_base_revision_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.user.request.v1", "request_id": "r1",
        "asset_set_order": ["set-mine"],
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


# --- favorites / paint (the caller's colored favorites) ----------------------

_FAVORITE_ENTRY_SBER = {"kind": "instrument", "key": "MISX:TQBR:SBER", "color": "yellow"}
_FAVORITE_REF_SBER = {"kind": "instrument", "key": "MISX:TQBR:SBER"}


def test_favorites_request_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.favorites.request.v1", "request_id": "r1"}
    _validator("favoritesRequest", registry).validate(msg)  # does not raise


def test_favorites_request_rejects_any_data_field(registry):
    """`favorites` reads only — it cannot be (ab)used to set/replace the list."""
    from jsonschema import ValidationError

    for extra in ({"favorites": [_FAVORITE_ENTRY_SBER]}, {"mark": [_FAVORITE_ENTRY_SBER]}):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.favorites.request.v1", "request_id": "r1",
            **extra,
        }
        with pytest.raises(ValidationError):
            _validator("favoritesRequest", registry).validate(msg)


def test_favorites_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.favorites.response.v1", "request_id": "r1",
        "favorites": [_FAVORITE_ENTRY_SBER, {"kind": "asset", "key": "asset-brent", "color": "gray"}],
    }
    _validator("favoritesResponse", registry).validate(msg)  # does not raise


def test_paint_request_empty_is_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.paint.request.v1", "request_id": "r1"}
    _validator("paintRequest", registry).validate(msg)  # does not raise


def test_paint_request_full_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.paint.request.v1", "request_id": "r1",
        "mark": [_FAVORITE_ENTRY_SBER, {"kind": "asset", "key": "asset-brent", "color": "cyan"}],
        "unmark": [{"kind": "instrument", "key": "MISX:TQBR:GAZP"}],
        "order": [_FAVORITE_REF_SBER],
    }
    _validator("paintRequest", registry).validate(msg)  # does not raise


def test_paint_request_has_no_cas_guard(registry):
    """No base_revision — mark/unmark/order are idempotent and commutative,
    deliberately not compared-and-set against the personal-sets revision."""
    assert "base_revision" not in _channel_doc()["$defs"]["paintRequest"]["properties"]


def test_paint_request_rejects_singular_mark_or_unmark(registry):
    """mark/unmark/order are always lists on the wire, never a bare object."""
    from jsonschema import ValidationError

    for extra in (
        {"mark": _FAVORITE_ENTRY_SBER},
        {"unmark": _FAVORITE_REF_SBER},
    ):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.paint.request.v1", "request_id": "r1",
            **extra,
        }
        with pytest.raises(ValidationError):
            _validator("paintRequest", registry).validate(msg)


def test_paint_response_echoes_only_sections_present(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.paint.response.v1", "request_id": "r1",
        "marked": [_FAVORITE_ENTRY_SBER],
    }
    _validator("paintResponse", registry).validate(msg)  # does not raise


# --- sources (manager-only registry of catalog feeds) -----------------------

def test_sources_request_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.sources.request.v1", "request_id": "r1"}
    _validator("sourcesRequest", registry).validate(msg)  # does not raise


def test_sources_request_rejects_filters(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.sources.request.v1", "request_id": "r1",
        "kind": "moex",
    }
    with pytest.raises(ValidationError):
        _validator("sourcesRequest", registry).validate(msg)


def test_sources_response_valid(registry):
    broker = {
        "source_id": "arena", "kind": "broker", "title": "Arena", "available": False,
        "last_refresh_at": None, "listing_count": 0,
    }
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.sources.response.v1", "request_id": "r1",
        "sources": [_SOURCE, broker],
    }
    _validator("sourcesResponse", registry).validate(msg)  # does not raise


def test_sources_response_empty_registry_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.sources.response.v1", "request_id": "r1",
        "sources": [],
    }
    _validator("sourcesResponse", registry).validate(msg)  # does not raise


def test_catalog_source_requires_every_state_field(registry):
    """An unavailable source is still listed, so every state field must be
    present — a client must never have to guess why nothing updates."""
    from jsonschema import ValidationError

    for missing in ("source_id", "kind", "title", "available", "last_refresh_at", "listing_count"):
        payload = {k: v for k, v in _SOURCE.items() if k != missing}
        with pytest.raises(ValidationError):
            _validator("catalogSource", registry).validate(payload)


def test_catalog_source_kind_outside_enum_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSource", registry).validate({**_SOURCE, "kind": "iss"})


def test_catalog_source_listing_count_not_negative(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("catalogSource", registry).validate({**_SOURCE, "listing_count": -1})


# --- refresh (on-demand catalog update, with dry run) -----------------------

def test_refresh_request_valid_with_and_without_dry_run(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.refresh.request.v1", "request_id": "r1",
        "source_id": "moex",
    }
    _validator("refreshRequest", registry).validate(msg)  # does not raise
    _validator("refreshRequest", registry).validate({**msg, "dry_run": True})  # does not raise


def test_refresh_request_without_source_id_rejected(registry):
    """There is no implicit default source — the manager picks one."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.refresh.request.v1", "request_id": "r1",
        "dry_run": True,
    }
    with pytest.raises(ValidationError):
        _validator("refreshRequest", registry).validate(msg)


def test_refresh_request_dry_run_must_be_boolean(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.refresh.request.v1", "request_id": "r1",
        "source_id": "moex", "dry_run": "true",
    }
    with pytest.raises(ValidationError):
        _validator("refreshRequest", registry).validate(msg)


def test_refresh_report_valid(registry):
    _validator("refreshReport", registry).validate(_REPORT)  # does not raise
    _validator("refreshReport", registry).validate(
        {**_REPORT, "changes": {"listings_added": 1, "listings_archived": 1}}
    )  # does not raise


def test_refresh_report_requires_every_section(registry):
    from jsonschema import ValidationError

    for missing in _REPORT:
        payload = {k: v for k, v in _REPORT.items() if k != missing}
        with pytest.raises(ValidationError):
            _validator("refreshReport", registry).validate(payload)


def test_refresh_report_dry_run_shape(registry):
    """A preview reports the same plan, just unapplied and with the revision
    standing still."""
    payload = {**_REPORT, "applied": False, "revision_after": 17}
    _validator("refreshReport", registry).validate(payload)  # does not raise


def test_refresh_report_archived_carries_the_reason(registry):
    from jsonschema import ValidationError

    _validator("refreshArchivedEntry", registry).validate({"key": "MISX:RFUD:BRU6", "reason": "expired"})
    for bad in ({"key": "MISX:RFUD:BRU6"}, {"reason": "expired"}, {"key": "MISX:RFUD:BRU6", "reason": ""}):
        with pytest.raises(ValidationError):
            _validator("refreshArchivedEntry", registry).validate(bad)
    with pytest.raises(ValidationError):
        _validator("refreshReport", registry).validate({**_REPORT, "archived": ["MISX:RFUD:BRU6"]})


def test_refresh_report_changes_must_be_integer_counts(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("refreshReport", registry).validate({**_REPORT, "changes": {"listings_added": "1"}})


def test_refresh_report_rejects_dropped_inherited_membership(registry):
    """A series belongs to an asset whole, so refresh no longer guesses set
    membership — the field that reported those guesses is gone."""
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("refreshReport", registry).validate(
            {**_REPORT, "inherited_membership": [["MISX:RFUD:BRV6", "set-commodities"]]}
        )


def test_refresh_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.refresh.response.v1", "request_id": "r1",
        "source_id": "moex", "dry_run": False, "report": _REPORT,
    }
    _validator("refreshResponse", registry).validate(msg)  # does not raise


def test_refresh_response_echoes_the_mode(registry):
    """The echo is what tells a preview from a write — both fields required."""
    from jsonschema import ValidationError

    for missing in ("source_id", "dry_run", "report"):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.refresh.response.v1", "request_id": "r1",
            **{k: v for k, v in {"source_id": "moex", "dry_run": True, "report": _REPORT}.items() if k != missing},
        }
        with pytest.raises(ValidationError):
            _validator("refreshResponse", registry).validate(msg)


def test_refresh_response_does_not_inline_the_report(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.refresh.response.v1", "request_id": "r1",
        "source_id": "moex", "dry_run": False, **_REPORT,
    }
    with pytest.raises(ValidationError):
        _validator("refreshResponse", registry).validate(msg)


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


def test_error_response_unsupported_action_code(registry):
    """An operation the backend does not serve answers with this code."""
    for message in ("this build serves no broker pool", "not available for this caller"):
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
        "asset_ids": ["asset-sber"],
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


def test_support_id_and_message_schema_consts_stay_v1():
    doc = _channel_doc()
    assert doc["x-afbws-support-id"] == "afbws.instrument.channel.v1"
    defs = doc["$defs"]
    for name, const in (
        ("catalogRequest", "afbws.instrument.catalog.request.v1"),
        ("catalogResponse", "afbws.instrument.catalog.response.v1"),
        ("poolRequest", "afbws.instrument.pool.request.v1"),
        ("poolResponse", "afbws.instrument.pool.response.v1"),
        ("commitRequest", "afbws.instrument.commit.request.v1"),
        ("commitResponse", "afbws.instrument.commit.response.v1"),
        ("userRequest", "afbws.instrument.user.request.v1"),
        ("userResponse", "afbws.instrument.user.response.v1"),
        ("favoritesRequest", "afbws.instrument.favorites.request.v1"),
        ("favoritesResponse", "afbws.instrument.favorites.response.v1"),
        ("paintRequest", "afbws.instrument.paint.request.v1"),
        ("paintResponse", "afbws.instrument.paint.response.v1"),
    ):
        assert defs[name]["properties"]["schema"]["const"] == const
    assert "poolMetaResponse" not in defs
    assert "poolSliceResponse" not in defs
    branches = {b["$ref"].rsplit("/", 1)[-1] for b in _channel_doc()["oneOf"]}
    assert {
        "catalogRequest", "catalogResponse",
        "commitRequest", "commitResponse",
        "userRequest", "userResponse",
        "favoritesRequest", "favoritesResponse",
        "paintRequest", "paintResponse",
        "sourcesRequest", "sourcesResponse",
        "refreshRequest", "refreshResponse",
        "inventoryRequest", "inventoryResponse",
    } <= branches


def test_the_asset_level_is_wired_through_both_snapshots():
    """catalog and commit answer with the same nested UI shape — a client that
    can read one can read the other."""
    defs = _channel_doc()["$defs"]
    for name in ("catalogResponse", "commitResponse"):
        required = set(defs[name]["required"])
        assert {"assets", "items", "series", "catalog_revision"} <= required, name
        assert "asset_members" not in required, name
        assert "memberships" not in required, name
        assert "asset_members" not in defs[name]["properties"], name
        assert "memberships" not in defs[name]["properties"], name
        assert "sets" not in defs[name]["properties"], name
        assert defs[name]["properties"]["assets"]["items"]["$ref"] == "#/$defs/catalogAsset", name
        assert defs[name]["properties"]["asset_sets"]["items"]["$ref"] == "#/$defs/assetSetView", name
    assert "members" in defs["catalogAsset"]["required"]
    assert defs["catalogAsset"]["properties"]["members"]["items"]["$ref"] == "#/$defs/catalogAssetMember"
    assert "asset_ids" in defs["assetSetView"]["required"]
    assert defs["userState"]["properties"]["asset_sets"]["items"]["$ref"] == "#/$defs/assetSetView"


def test_the_dead_operations_are_gone():
    """`list` v1/v2 and `apply` were removed, not merely deprecated: nothing
    half-deleted may stay behind in $defs or in the message union."""
    doc = _channel_doc()
    defs = doc["$defs"]
    for name in (
        "listRequest", "listResponse", "listRequestV2", "listResponseV2",
        "listSetV2", "listAssetV2", "publicListing",
        "applyRequest", "applyResponse",
        "group", "asset", "assets", "catalogSet",
        "assetMember", "assetMembers",
        "catalogSetEntry", "catalogSetView", "setUpsert", "setMembership",
    ):
        assert name not in defs, name
    branches = {b["$ref"].rsplit("/", 1)[-1] for b in doc["oneOf"]}
    assert not any(b.startswith(("list", "apply")) for b in branches), branches


def test_no_channel_def_allows_additional_properties():
    defs = _channel_doc()["$defs"]
    for name in (
        "catalogSeries", "userState", "errorDetails",
        "collection", "collectionUpsert", "assetSetView", "assetSetUpsert",
        "inventoryRequest", "inventoryListingEntry", "inventorySeriesEntry", "inventoryResponse",
        "assetSuggestion", "acceptSuggestion",
        "catalogRequest", "catalogResponse", "commitRequest", "commitResponse",
        "membersEdit", "collectionMembersEdit", "listingArchival", "seriesUpsert",
        "userRequest", "userResponse",
        "favoriteRef", "favoriteEntry", "favoritesRequest", "favoritesResponse",
        "paintRequest", "paintResponse",
        "catalogAsset", "catalogAssetMember", "assetMemberInput", "assetUpsert",
        "poolRequest", "poolResponse", "poolListingEntry", "poolSeriesEntry",
        "catalogSource", "sourcesRequest", "sourcesResponse",
        "refreshRequest", "refreshResponse", "refreshReport", "refreshArchivedEntry",
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


# --- catalog reorg: collection / assetSet / inventory / suggestions -----------

def test_collection_valid_and_required(registry):
    _validator("collection", registry).validate(_COLLECTION)  # does not raise
    _validator("collection", registry).validate({k: v for k, v in _COLLECTION.items() if k != "pending"})


def test_collection_missing_required_rejected(registry):
    from jsonschema import ValidationError

    for missing in ("collection_id", "name"):
        with pytest.raises(ValidationError):
            _validator("collection", registry).validate(
                {k: v for k, v in _COLLECTION.items() if k != missing}
            )


def test_collection_rejects_unknown_property(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("collection", registry).validate({**_COLLECTION, "extra": True})


def test_collection_upsert_valid(registry):
    _validator("collectionUpsert", registry).validate(
        {"collection_id": "col-stocks", "name": "Акции", "parent_id": None}
    )


def test_collection_upsert_missing_name_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("collectionUpsert", registry).validate({"collection_id": "col-stocks"})


def test_asset_set_view_global_requires_visibility_tier(registry):
    from jsonschema import ValidationError

    _validator("assetSetView", registry).validate(_ASSET_SET_GLOBAL)
    without = {k: v for k, v in _ASSET_SET_GLOBAL.items() if k != "visibility_tier"}
    with pytest.raises(ValidationError):
        _validator("assetSetView", registry).validate(without)


def test_asset_set_view_user_forbids_visibility_tier(registry):
    from jsonschema import ValidationError

    _validator("assetSetView", registry).validate(_ASSET_SET_USER)
    with pytest.raises(ValidationError):
        _validator("assetSetView", registry).validate({**_ASSET_SET_USER, "visibility_tier": "user"})


def test_asset_set_view_user_requires_owner(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("assetSetView", registry).validate(
            {k: v for k, v in _ASSET_SET_USER.items() if k != "owner_user_id"}
        )


def test_asset_set_upsert_valid(registry):
    _validator("assetSetUpsert", registry).validate({"set_id": "set-new", "name": "Новая"})
    _validator("assetSetUpsert", registry).validate(
        {"set_id": "set-new", "name": "Новая", "visibility_tier": "manager"}
    )


def test_asset_set_upsert_rejects_scope_and_owner(registry):
    """scope/owner are the server's business, never a client's."""
    from jsonschema import ValidationError

    for extra in ({"scope": "global"}, {"owner_user_id": "u-42"}):
        with pytest.raises(ValidationError):
            _validator("assetSetUpsert", registry).validate(
                {"set_id": "set-new", "name": "Новая", **extra}
            )


def test_inventory_request_minimal_valid(registry):
    msg = {"channel": "instrument", "schema": "afbws.instrument.inventory.request.v1", "request_id": "r1"}
    _validator("inventoryRequest", registry).validate(msg)


def test_inventory_request_full_filters_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.inventory.request.v1", "request_id": "r1",
        "source": "moex", "market": "stock", "board": "TQBR", "instrument_type": "stock",
        "query": "sber", "limit": 100, "cursor": "page-2",
    }
    _validator("inventoryRequest", registry).validate(msg)


def test_inventory_request_limit_bounds(registry):
    from jsonschema import ValidationError

    for limit in (0, 201):
        with pytest.raises(ValidationError):
            _validator("inventoryRequest", registry).validate({
                "channel": "instrument", "schema": "afbws.instrument.inventory.request.v1",
                "request_id": "r1", "limit": limit,
            })


def test_inventory_listing_entry_valid(registry):
    _validator("inventoryListingEntry", registry).validate(_INVENTORY_LISTING)
    future = {
        **{k: v for k, v in _INVENTORY_LISTING.items() if k not in ("isin",)},
        "instrument_type": "futures",
        "ticker": "BRV6",
        "market": "futures",
        "board": "RFUD",
    }
    _validator("inventoryListingEntry", registry).validate(future)


def test_inventory_listing_entry_rejects_series_instrument_type(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("inventoryListingEntry", registry).validate(
            {**_INVENTORY_LISTING, "instrument_type": "series"}
        )


def test_inventory_listing_entry_futures_requires_futures_market(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("inventoryListingEntry", registry).validate(
            {**_INVENTORY_LISTING, "instrument_type": "futures", "market": "stock"}
        )


def test_inventory_series_entry_valid(registry):
    _validator("inventorySeriesEntry", registry).validate(_INVENTORY_SERIES)


def test_inventory_series_entry_rejects_wrong_market(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("inventorySeriesEntry", registry).validate({**_INVENTORY_SERIES, "market": "stock"})


def test_inventory_entry_discriminator(registry):
    from jsonschema import ValidationError

    _validator("inventoryEntry", registry).validate(_INVENTORY_LISTING)
    _validator("inventoryEntry", registry).validate(_INVENTORY_SERIES)
    with pytest.raises(ValidationError):
        _validator("inventoryEntry", registry).validate({"kind": "contract"})


def test_inventory_response_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.inventory.response.v1", "request_id": "r1",
        "total": 2, "next_cursor": "next", "inventory_revision": 5,
        "entries": [_INVENTORY_LISTING, _INVENTORY_SERIES],
        "source": "moex", "fetched_at": "2026-08-18T12:00:00Z",
    }
    _validator("inventoryResponse", registry).validate(msg)


def test_inventory_response_requires_revision_and_entries(registry):
    from jsonschema import ValidationError

    base = {
        "channel": "instrument", "schema": "afbws.instrument.inventory.response.v1", "request_id": "r1",
        "total": 0, "next_cursor": None, "inventory_revision": 0, "entries": [],
    }
    for missing in ("inventory_revision", "entries", "total", "next_cursor"):
        with pytest.raises(ValidationError):
            _validator("inventoryResponse", registry).validate(
                {k: v for k, v in base.items() if k != missing}
            )


def test_asset_suggestion_valid(registry):
    _validator("assetSuggestion", registry).validate(_SUGGESTION)
    _validator("assetSuggestion", registry).validate({
        **_SUGGESTION,
        "proposed_name": "Brent mini",
        "proposed_collection_id": None,
        "fingerprint": "abc",
        "created_at": "2026-08-18T10:00:00Z",
        "last_seen_at": "2026-08-18T11:00:00Z",
        "resolved_asset_id": "asset-brm",
    })


def test_asset_suggestion_missing_required_rejected(registry):
    from jsonschema import ValidationError

    for missing in ("suggestion_id", "subject_type", "subject_ref", "reason", "status"):
        with pytest.raises(ValidationError):
            _validator("assetSuggestion", registry).validate(
                {k: v for k, v in _SUGGESTION.items() if k != missing}
            )


def test_accept_suggestion_valid(registry):
    _validator("acceptSuggestion", registry).validate(
        {"suggestion_id": "sug-1", "asset_id": "asset-brm"}
    )
    _validator("acceptSuggestion", registry).validate(
        {"suggestion_id": "sug-1", "asset_id": "asset-brm", "collection_id": "col-commodities"}
    )


def test_accept_suggestion_requires_both_ids(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("acceptSuggestion", registry).validate({"suggestion_id": "sug-1"})


def test_catalog_response_with_collections_asset_sets_suggestions(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT,
        "collections": [_COLLECTION],
        "asset_sets": [_ASSET_SET_GLOBAL],
        "suggestions": [_SUGGESTION],
    }
    _validator("catalogResponse", registry).validate(msg)


def test_catalog_response_without_new_sections_still_valid(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.catalog.response.v1", "request_id": "r1",
        **_SNAPSHOT,
    }
    _validator("catalogResponse", registry).validate(msg)


def test_commit_request_with_asset_sets_and_accept_suggestions(registry):
    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17,
        "asset_sets": [{"set_id": "set-new", "name": "Новая"}],
        "asset_set_members": [{"set_id": "set-new", "add": ["asset-sber"]}],
        "accept_suggestions": [{"suggestion_id": "sug-1", "asset_id": "asset-brm"}],
        "reject_suggestions": ["sug-2"],
        "collections": [{"collection_id": "col-new", "name": "Новая категория"}],
        "remove_collections": ["col-old"],
        "remove_asset_sets": ["set-old"],
    }
    _validator("commitRequest", registry).validate(msg)


def test_commit_request_order_sections_are_full_orders(registry):
    """Position left the entities: a commit states the whole resulting order in
    its own section, the same idiom membersEdit.order already used."""
    from jsonschema import ValidationError

    msg = {
        "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
        "base_revision": 17,
        "asset_set_order": ["set-blue", "set-mine"],
        "collection_order": ["col-stocks", "col-commodities"],
        "collection_members": [{"collection_id": "col-stocks", "order": ["asset-sber"]}],
    }
    _validator("commitRequest", registry).validate(msg)  # does not raise
    for bad in ({"asset_set_order": [""]}, {"collection_order": [7]}, {"asset_set_order": "set-blue"}):
        with pytest.raises(ValidationError):
            _validator("commitRequest", registry).validate({**msg, **bad})


def test_collection_members_edit_shape(registry):
    """Same delta shape as membersEdit, keyed by collection_id and holding
    asset_ids — an asset belongs to exactly one collection."""
    from jsonschema import ValidationError

    _validator("collectionMembersEdit", registry).validate({"collection_id": "col-stocks"})
    _validator("collectionMembersEdit", registry).validate({
        "collection_id": "col-stocks",
        "add": ["asset-gazp"], "remove": ["asset-lkoh"], "order": ["asset-sber", "asset-gazp"],
    })  # does not raise
    with pytest.raises(ValidationError):
        _validator("collectionMembersEdit", registry).validate({"add": ["asset-sber"]})
    with pytest.raises(ValidationError):
        _validator("collectionMembersEdit", registry).validate(
            {"collection_id": "col-stocks", "set_id": "set-blue"}
        )
    with pytest.raises(ValidationError):
        _validator("collectionMembersEdit", registry).validate(
            {"collection_id": "col-stocks", "sort_order": 1}
        )


def test_user_request_speaks_the_asset_set_vocabulary():
    """The personal operation uses the same shapes and section names as commit:
    assetSetUpsert, remove_asset_sets, asset_set_members, asset_set_order."""
    defs = _channel_doc()["$defs"]
    user_request = defs["userRequest"]
    props = user_request["properties"]
    assert props["asset_sets"]["items"]["$ref"] == "#/$defs/assetSetUpsert"
    assert "remove_asset_sets" in props
    assert "asset_set_members" in props
    assert props["asset_set_members"]["items"]["$ref"] == "#/$defs/membersEdit"
    assert props["asset_set_order"]["items"]["type"] == "string"
    for gone in ("sets", "remove_sets", "members", "hidden_set_ids", "order"):
        assert gone not in props, gone
    # visibility_tier is a global-set notion; the personal operation rejects it.
    assert "visibility_tier" in props["asset_sets"]["description"]
    assert "validation_error" in props["asset_sets"]["description"]


def test_user_state_has_no_hide_or_order_overlay():
    """The personal hide/reorder overlay (hidden_set_ids/order, user_catalog_view)
    was judged unnecessary and removed outright — not deferred, not kept
    read-only. Reordering the caller's OWN sets is userRequest.asset_set_order."""
    defs = _channel_doc()["$defs"]
    for gone in ("hidden_set_ids", "order"):
        assert gone not in defs["userState"]["properties"], gone
        assert gone not in defs["userState"]["required"], gone


def test_favorites_request_is_read_only():
    """`favorites` cannot be used to set or replace favorites — only channel/
    schema/request_id are recognized properties."""
    defs = _channel_doc()["$defs"]
    props = defs["favoritesRequest"]["properties"]
    assert set(props) == {"channel", "schema", "request_id"}
    assert defs["favoritesRequest"]["additionalProperties"] is False


def test_paint_request_sections_are_all_lists():
    defs = _channel_doc()["$defs"]
    props = defs["paintRequest"]["properties"]
    for name in ("mark", "unmark", "order"):
        assert props[name]["type"] == "array", name
    assert props["mark"]["items"]["$ref"] == "#/$defs/favoriteEntry"
    assert props["unmark"]["items"]["$ref"] == "#/$defs/favoriteRef"
    assert props["order"]["items"]["$ref"] == "#/$defs/favoriteRef"


def test_favorite_ref_kind_is_instrument_or_asset():
    defs = _channel_doc()["$defs"]
    assert defs["favoriteRef"]["properties"]["kind"]["enum"] == ["instrument", "asset"]
    assert defs["favoriteEntry"]["properties"]["kind"]["enum"] == ["instrument", "asset"]


def test_favorites_and_paint_request_schema_consts_do_not_collide():
    """`...favorites.request.v1` and `...paint.request.v1` differ by more than
    one shared prefix fragment — but the historical trap in this file was
    `favorite`/`favorites` sharing a prefix; guard the actual consts stay
    distinct `$defs`, exact dict lookup, no startswith."""
    defs = _channel_doc()["$defs"]
    assert (
        defs["favoritesRequest"]["properties"]["schema"]["const"]
        != defs["paintRequest"]["properties"]["schema"]["const"]
    )


def test_no_wire_entity_carries_an_order_field():
    """Order is array position everywhere; the only order on the wire is the
    full-order sections of a write."""
    defs = _channel_doc()["$defs"]
    for name, schema in defs.items():
        props = schema.get("properties", {})
        assert "sort_order" not in props, name
        assert "collection_sort_order" not in props, name


def test_every_local_ref_resolves():
    """Nothing half-deleted: every `#/$defs/...` in the document points at a
    $def that exists."""
    doc = _channel_doc()
    names = set(doc["$defs"])
    dangling = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and isinstance(value, str) and value.startswith("#/$defs/"):
                    if value.rsplit("/", 1)[-1] not in names:
                        dangling.append((path, value))
                else:
                    walk(value, f"{path}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}/{index}")

    walk(doc, "")
    assert dangling == []


def test_commit_request_rejects_the_removed_shadow_sections(registry):
    """`sets`/`remove_sets`/`members` were the deprecated twins of the
    asset_set_* sections; a commit that still sends one is rejected."""
    from jsonschema import ValidationError

    for extra in (
        {"sets": [{"set_id": "set-blue-chips", "name": "Голубые фишки"}]},
        {"remove_sets": ["set-old"]},
        {"members": [{"set_id": "set-blue-chips", "add": ["asset-sber"]}]},
    ):
        msg = {
            "channel": "instrument", "schema": "afbws.instrument.commit.request.v1", "request_id": "r1",
            "base_revision": 17, **extra,
        }
        with pytest.raises(ValidationError):
            _validator("commitRequest", registry).validate(msg)


def test_catalog_asset_optional_collection_id_without_a_position(registry):
    """An asset names its collection; where it sits inside it is the order of
    `assets[]`, not a field."""
    from jsonschema import ValidationError

    _validator("catalogAsset", registry).validate(_ASSET)
    _validator("catalogAsset", registry).validate({**_ASSET, "collection_id": "col-commodities"})
    with pytest.raises(ValidationError):
        _validator("catalogAsset", registry).validate({**_ASSET, "collection_sort_order": 3})


def test_refresh_report_optional_suggestion_and_inventory_revisions(registry):
    _validator("refreshReport", registry).validate({
        **_REPORT,
        "suggestion_ids": ["sug-1"],
        "inventory_revision_before": 4,
        "inventory_revision_after": 5,
    })


def test_catalog_source_optional_inventory_fields(registry):
    _validator("catalogSource", registry).validate({
        **_SOURCE,
        "inventory_count": 12000,
        "last_error": "timeout",
        "inventory_revision": 5,
    })


def test_error_details_collection_and_suggestion_ids(registry):
    _validator("errorDetails", registry).validate({
        "collection_ids": ["col-stocks"],
        "suggestion_ids": ["sug-1"],
    })
