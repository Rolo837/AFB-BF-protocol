# DO NOT EDIT BY HAND — generated from spec/schemas/ (via
# spec/.generated/bundled-schema.json) by datamodel-codegen, invoked from
# tools/generate.py. Run `afb-bf-protocol-generate` to regenerate.
# source-hash: 6b45e599fdea60f92e744827921d0f9652a131370c7d0789faaae37ec54e1d06

from __future__ import annotations

from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

AccountAccountId: TypeAlias = str


AccountBfId: TypeAlias = str


class AccountErrorResponse(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.error.response.v1"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]


class AccountEventRecord(TypedDict):
    logged_at: str
    bf_id: AccountBfId
    deal_id: NotRequired[str | None]
    category: Literal["deal", "order", "position", "condition"]
    event: str
    data: NotRequired[dict[str, Any] | None]


class AccountEventsRequest(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.events.request.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: AccountBfId
    date: NotRequired[str]


class AccountEventsResponse(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.events.response.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: AccountBfId
    date: str
    items: list[AccountEventRecord]


class AccountGetRequest(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.get.request.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: AccountBfId
    account_id: NotRequired[AccountAccountId]
    force: NotRequired[bool]


class AccountGetResponse(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.get.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: AccountSnapshot


class AccountListRequest(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.list.request.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: NotRequired[AccountBfId]
    force: NotRequired[bool]


class AccountListResponse(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.list.response.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[AccountSnapshot]


class AccountOrder(TypedDict):
    order_id: str
    deal_id: NotRequired[str]
    symbol: NotRequired[str]
    side: NotRequired[str]
    role: NotRequired[str]
    status: NotRequired[str]
    quantity: NotRequired[int]
    filled_quantity: NotRequired[int]
    leg_index: NotRequired[int]
    limit_price: NotRequired[str | None]
    average_price: NotRequired[str | None]
    client_order_id: NotRequired[str]
    cancel_source: NotRequired[Literal["system", "broker"]]
    updated_at: NotRequired[str]
    error_code: NotRequired[str | None]
    error_message: NotRequired[str | None]


class AccountOrdersPush(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.orders.push.v1"]
    bf_id: AccountBfId
    account_id: AccountAccountId
    items: list[AccountOrder]


class AccountOrdersRequest(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.orders.request.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: AccountBfId
    account_id: NotRequired[AccountAccountId]


class AccountOrdersResponse(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.orders.response.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: AccountBfId
    account_id: AccountAccountId
    items: list[AccountOrder]


class AccountSnapshot(TypedDict):
    bf_id: AccountBfId
    account_id: AccountAccountId
    tradable: bool
    readonly: bool
    status: Literal["ok", "stale", "error"]
    equity: str | None
    cash: list[PayloadsBrokerAccountsCashBalance]
    positions: list[PayloadsBrokerAccountsPosition]
    as_of: NotRequired[str]


class AccountSnapshotPush(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.snapshot.push.v1"]
    bf_id: AccountBfId
    default_account_id: AccountAccountId
    items: list[AccountSnapshot]


AccountChannelV1Message: TypeAlias = (
    AccountListRequest
    | AccountListResponse
    | AccountGetRequest
    | AccountGetResponse
    | AccountOrdersRequest
    | AccountOrdersResponse
    | AccountEventsRequest
    | AccountEventsResponse
    | AccountErrorResponse
    | AccountSnapshotPush
    | AccountOrdersPush
)


class AfbwsCatalogChannelV1ArchiveItem(TypedDict):
    instrument_key: AfbwsCommonV1InstrumentKey
    reason: NotRequired[str]


class AfbwsCatalogChannelV1Asset(TypedDict):
    """
    `members`, when present, is the WHOLE composition in its final order (no add/remove form). Omit to leave it untouched; `[]` empties the asset. In a snapshot `members` and `collection_id` are always present.
    """

    id: str
    name: str
    collection_id: NotRequired[str | None]
    members: NotRequired[list[AfbwsCatalogChannelV1Member]]


class AfbwsCatalogChannelV1Collection(TypedDict):
    """
    `asset_ids`, when present, is the WHOLE ordered composition of the collection (the assets filed into it); an asset lives in at most one collection, so naming it here moves it. In a snapshot `asset_ids` is always present. Omit in a commit to leave the composition untouched.
    """

    id: str
    name: str
    parent_id: NotRequired[str | None]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsCatalogChannelV1FavoriteColor | None]
    asset_ids: NotRequired[list[str]]


class AfbwsCatalogChannelV1Commit1(TypedDict):
    """
    Request: the delta relative to the last `snapshot` plus `base_revision` for CAS (stale -> error `conflict`, `details.catalog_revision`). Every array is an upsert by id; `assets[].members` and `sets[].asset_ids|instrument_keys` are the WHOLE composition in final order; `collection_order` / `set_order` are the whole final order of ids. New members are `{kind, source, ref}` only: the backend fetches listing data itself (Finam: GetAsset via the detail cache, at most 20 new Finam instruments per commit). If any new member cannot be accepted NOTHING is applied and the error (`unsupported_type`, `no_market_data`, `not_found`, `source_unavailable`) lists the rows in `details.refs[]`. Response: `revision` and `created[]` (what the new members became); the client re-reads `snapshot`. Manager only.
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.commit.v1"]
    request_id: AfbwsCommonV1RequestId
    base_revision: int
    collections: NotRequired[list[AfbwsCatalogChannelV1Collection]]
    collection_order: NotRequired[list[str]]
    remove_collections: NotRequired[list[str]]
    sets: NotRequired[list[AfbwsCatalogChannelV1Set]]
    set_order: NotRequired[list[str]]
    remove_sets: NotRequired[list[str]]
    assets: NotRequired[list[AfbwsCatalogChannelV1Asset]]
    remove_assets: NotRequired[list[str]]
    archive: NotRequired[list[AfbwsCatalogChannelV1ArchiveItem]]
    reason: NotRequired[str]
    revision: NotRequired[int]
    created: NotRequired[list[AfbwsCatalogChannelV1Created]]


class AfbwsCatalogChannelV1Commit2(TypedDict):
    """
    Request: the delta relative to the last `snapshot` plus `base_revision` for CAS (stale -> error `conflict`, `details.catalog_revision`). Every array is an upsert by id; `assets[].members` and `sets[].asset_ids|instrument_keys` are the WHOLE composition in final order; `collection_order` / `set_order` are the whole final order of ids. New members are `{kind, source, ref}` only: the backend fetches listing data itself (Finam: GetAsset via the detail cache, at most 20 new Finam instruments per commit). If any new member cannot be accepted NOTHING is applied and the error (`unsupported_type`, `no_market_data`, `not_found`, `source_unavailable`) lists the rows in `details.refs[]`. Response: `revision` and `created[]` (what the new members became); the client re-reads `snapshot`. Manager only.
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.commit.v1"]
    request_id: AfbwsCommonV1RequestId
    base_revision: NotRequired[int]
    collections: NotRequired[list[AfbwsCatalogChannelV1Collection]]
    collection_order: NotRequired[list[str]]
    remove_collections: NotRequired[list[str]]
    sets: NotRequired[list[AfbwsCatalogChannelV1Set]]
    set_order: NotRequired[list[str]]
    remove_sets: NotRequired[list[str]]
    assets: NotRequired[list[AfbwsCatalogChannelV1Asset]]
    remove_assets: NotRequired[list[str]]
    archive: NotRequired[list[AfbwsCatalogChannelV1ArchiveItem]]
    reason: NotRequired[str]
    revision: int
    created: list[AfbwsCatalogChannelV1Created]


AfbwsCatalogChannelV1Commit: TypeAlias = (
    AfbwsCatalogChannelV1Commit1 | AfbwsCatalogChannelV1Commit2
)


class AfbwsCatalogChannelV1Created1(TypedDict):
    source: AfbwsCatalogChannelV1Source
    ref: str
    instrument_key: AfbwsCommonV1InstrumentKey
    derivative: NotRequired[str]


class AfbwsCatalogChannelV1Created2(TypedDict):
    source: AfbwsCatalogChannelV1Source
    ref: str
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    derivative: str


AfbwsCatalogChannelV1Created: TypeAlias = (
    AfbwsCatalogChannelV1Created1 | AfbwsCatalogChannelV1Created2
)


class AfbwsCatalogChannelV1Derivative(TypedDict):
    code: str
    kind: str
    name: str
    underlying_key: NotRequired[AfbwsCommonV1InstrumentKey | None]
    source: str


class AfbwsCatalogChannelV1Error(TypedDict):
    """
    `details`: `catalog_revision` for `conflict`; `refs[]` (`{source, ref, code, message}`) naming the rejected new members of a commit; `source` for `source_unavailable`.
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.error.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    code: Literal[
        "forbidden",
        "invalid_schema",
        "invalid_channel",
        "unsupported_action",
        "validation_error",
        "not_found",
        "conflict",
        "internal_error",
        "unsupported_type",
        "no_market_data",
        "source_unavailable",
    ]
    message: str
    details: NotRequired[dict[str, Any]]


AfbwsCatalogChannelV1FavoriteColor: TypeAlias = Literal[
    "yellow", "red", "blue", "green", "gray", "orange", "cyan", "purple", "pink", "teal"
]


class AfbwsCatalogChannelV1Listing(TypedDict):
    instrument_key: AfbwsCommonV1InstrumentKey
    mic: str
    board: NotRequired[str | None]
    market: str
    ticker: str
    name: str
    shortname: NotRequired[str | None]
    currency: NotRequired[str | None]
    decimals: NotRequired[int | None]
    lot_size: NotRequired[int | None]
    price_step: NotRequired[str | None]
    step_price: NotRequired[str | None]
    expiration: NotRequired[str | None]
    isin: NotRequired[str | None]
    derivative: NotRequired[str | None]
    source: str


class AfbwsCatalogChannelV1MemberExisting(TypedDict):
    kind: Literal["listing", "derivative"]
    ref: str


class AfbwsCatalogChannelV1MemberNew(TypedDict):
    kind: Literal["listing", "derivative"]
    source: AfbwsCatalogChannelV1Source
    ref: str


AfbwsCatalogChannelV1Member: TypeAlias = (
    AfbwsCatalogChannelV1MemberExisting | AfbwsCatalogChannelV1MemberNew
)


class AfbwsCatalogChannelV1Refresh1(TypedDict):
    """
    Does NOT refresh immediately: puts the source into the daily-cycle queue (the same path for `moex` and `finam`). Request: optional `sources[]` (omitted = every available source). Response (same `request_id`): `queued[]`, `already_queued[]`, `rejected[]`. Push (NO `request_id`, manager connections with the capability): the outcome per source — `source`, `state` (`done`|`failed`), `finished_at`, `received`, `summary`, `error`, `revision`, and `states[]` = fresh source statuses (named `states`, not `sources`, to keep the request field unambiguous).
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.refresh.v1"]
    request_id: AfbwsCommonV1RequestId
    sources: NotRequired[list[AfbwsCatalogChannelV1Source]]
    queued: NotRequired[list[AfbwsCatalogChannelV1Source]]
    already_queued: NotRequired[list[AfbwsCatalogChannelV1Source]]
    rejected: NotRequired[list[AfbwsCatalogChannelV1Rejection]]
    source: NotRequired[AfbwsCatalogChannelV1Source]
    state: NotRequired[Literal["done", "failed"]]
    finished_at: NotRequired[str]
    received: NotRequired[int | None]
    summary: NotRequired[str | None]
    error: NotRequired[str | None]
    revision: NotRequired[int | None]
    states: NotRequired[list[AfbwsCatalogChannelV1SourceStatus]]


class AfbwsCatalogChannelV1Refresh2(TypedDict):
    """
    Does NOT refresh immediately: puts the source into the daily-cycle queue (the same path for `moex` and `finam`). Request: optional `sources[]` (omitted = every available source). Response (same `request_id`): `queued[]`, `already_queued[]`, `rejected[]`. Push (NO `request_id`, manager connections with the capability): the outcome per source — `source`, `state` (`done`|`failed`), `finished_at`, `received`, `summary`, `error`, `revision`, and `states[]` = fresh source statuses (named `states`, not `sources`, to keep the request field unambiguous).
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.refresh.v1"]
    request_id: AfbwsCommonV1RequestId
    sources: NotRequired[list[AfbwsCatalogChannelV1Source]]
    queued: list[AfbwsCatalogChannelV1Source]
    already_queued: list[AfbwsCatalogChannelV1Source]
    rejected: list[AfbwsCatalogChannelV1Rejection]
    source: NotRequired[AfbwsCatalogChannelV1Source]
    state: NotRequired[Literal["done", "failed"]]
    finished_at: NotRequired[str]
    received: NotRequired[int | None]
    summary: NotRequired[str | None]
    error: NotRequired[str | None]
    revision: NotRequired[int | None]
    states: NotRequired[list[AfbwsCatalogChannelV1SourceStatus]]


class AfbwsCatalogChannelV1Refresh3(TypedDict):
    """
    Does NOT refresh immediately: puts the source into the daily-cycle queue (the same path for `moex` and `finam`). Request: optional `sources[]` (omitted = every available source). Response (same `request_id`): `queued[]`, `already_queued[]`, `rejected[]`. Push (NO `request_id`, manager connections with the capability): the outcome per source — `source`, `state` (`done`|`failed`), `finished_at`, `received`, `summary`, `error`, `revision`, and `states[]` = fresh source statuses (named `states`, not `sources`, to keep the request field unambiguous).
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.refresh.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    sources: NotRequired[list[AfbwsCatalogChannelV1Source]]
    queued: NotRequired[list[AfbwsCatalogChannelV1Source]]
    already_queued: NotRequired[list[AfbwsCatalogChannelV1Source]]
    rejected: NotRequired[list[AfbwsCatalogChannelV1Rejection]]
    source: AfbwsCatalogChannelV1Source
    state: Literal["done", "failed"]
    finished_at: str
    received: NotRequired[int | None]
    summary: NotRequired[str | None]
    error: NotRequired[str | None]
    revision: NotRequired[int | None]
    states: NotRequired[list[AfbwsCatalogChannelV1SourceStatus]]


AfbwsCatalogChannelV1Refresh: TypeAlias = (
    AfbwsCatalogChannelV1Refresh1
    | AfbwsCatalogChannelV1Refresh2
    | AfbwsCatalogChannelV1Refresh3
)


class AfbwsCatalogChannelV1RefreshResult(TypedDict):
    source: AfbwsCatalogChannelV1Source
    state: Literal["done", "failed"]
    finished_at: str
    received: NotRequired[int | None]
    summary: NotRequired[str | None]
    error: NotRequired[str | None]
    revision: NotRequired[int | None]


class AfbwsCatalogChannelV1Rejection(TypedDict):
    source: AfbwsCatalogChannelV1Source
    code: Literal["source_unavailable", "forbidden"]
    message: NotRequired[str]


class AfbwsCatalogChannelV1Set(TypedDict):
    """
    `type` is decided on create (default `asset`); on update it must equal the stored one. A set of type `asset` carries `asset_ids[]`, of type `instrument` carries `instrument_keys[]`; the list, when present, is the WHOLE composition in its final order.
    """

    id: str
    name: str
    type: NotRequired[Literal["asset", "instrument"]]
    visibility_tier: NotRequired[Literal["manager", "user", "guest"]]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsCatalogChannelV1FavoriteColor | None]
    asset_ids: NotRequired[list[str]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]


class AfbwsCatalogChannelV1Snapshot1(TypedDict):
    """
    Request: only `request_id`. Response (same `request_id`): the state the asset manager edits — ordered collections, global sets, assets with their members, and ONLY the listings / derivatives referenced by assets and global instrument sets (unassigned listings are found through `symbols`). `revision` is the `base_revision` for `commit`. Manager only.
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.snapshot.v1"]
    request_id: AfbwsCommonV1RequestId
    revision: NotRequired[int]
    collections: NotRequired[list[AfbwsCatalogChannelV1Collection]]
    sets: NotRequired[list[AfbwsCatalogChannelV1Set]]
    assets: NotRequired[list[AfbwsCatalogChannelV1SnapshotAsset]]
    listings: NotRequired[list[AfbwsCatalogChannelV1Listing]]
    derivatives: NotRequired[list[AfbwsCatalogChannelV1Derivative]]
    sources: NotRequired[list[AfbwsCatalogChannelV1SourceStatus]]


class AfbwsCatalogChannelV1Snapshot2(TypedDict):
    """
    Request: only `request_id`. Response (same `request_id`): the state the asset manager edits — ordered collections, global sets, assets with their members, and ONLY the listings / derivatives referenced by assets and global instrument sets (unassigned listings are found through `symbols`). `revision` is the `base_revision` for `commit`. Manager only.
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.snapshot.v1"]
    request_id: AfbwsCommonV1RequestId
    revision: int
    collections: list[AfbwsCatalogChannelV1Collection]
    sets: list[AfbwsCatalogChannelV1Set]
    assets: list[AfbwsCatalogChannelV1SnapshotAsset]
    listings: list[AfbwsCatalogChannelV1Listing]
    derivatives: list[AfbwsCatalogChannelV1Derivative]
    sources: list[AfbwsCatalogChannelV1SourceStatus]


AfbwsCatalogChannelV1Snapshot: TypeAlias = (
    AfbwsCatalogChannelV1Snapshot1 | AfbwsCatalogChannelV1Snapshot2
)


class AfbwsCatalogChannelV1SnapshotAsset(TypedDict):
    id: str
    name: str
    collection_id: str | None
    members: list[AfbwsCatalogChannelV1MemberExisting]


AfbwsCatalogChannelV1Source: TypeAlias = Literal["moex", "finam"]


class AfbwsCatalogChannelV1SourceStatus(TypedDict):
    source: AfbwsCatalogChannelV1Source
    available: bool
    state: str
    pending: bool
    last_refresh_at: NotRequired[str | None]
    last_error: NotRequired[str | None]
    symbols: NotRequired[int | None]
    listings: NotRequired[int | None]
    unlinked: NotRequired[int | None]


class AfbwsCatalogChannelV1Support1(TypedDict):
    """
    Request: only `request_id`. Response: `sources` — for each source a dictionary MIC -> categories (`market` values of `symbols`) built from the source's own catalog (Finam: the mirror's active symbols; MOEX: the pool). MOEX is a single exchange (`MISX`). A source that is unavailable is absent. Manager only.
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.support.v1"]
    request_id: AfbwsCommonV1RequestId
    sources: NotRequired[
        dict[
            Literal["moex", "finam"],
            dict[str, list[Literal["stock", "currency", "index", "futures", "other"]]],
        ]
    ]


class AfbwsCatalogChannelV1Support2(TypedDict):
    """
    Request: only `request_id`. Response: `sources` — for each source a dictionary MIC -> categories (`market` values of `symbols`) built from the source's own catalog (Finam: the mirror's active symbols; MOEX: the pool). MOEX is a single exchange (`MISX`). A source that is unavailable is absent. Manager only.
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.support.v1"]
    request_id: AfbwsCommonV1RequestId
    sources: dict[
        Literal["moex", "finam"],
        dict[str, list[Literal["stock", "currency", "index", "futures", "other"]]],
    ]


AfbwsCatalogChannelV1Support: TypeAlias = (
    AfbwsCatalogChannelV1Support1 | AfbwsCatalogChannelV1Support2
)


class AfbwsCatalogChannelV1SymbolRow(TypedDict):
    ref: str
    kind: Literal["listing", "derivative"]
    ticker: str
    name: str
    market: Literal["stock", "currency", "index", "futures", "other"]
    mic: NotRequired[str | None]
    archived: bool
    in_catalog: NotRequired[AfbwsCommonV1InstrumentKey | None]
    addable: bool
    reason: NotRequired[Literal["unsupported_type", "archived"] | None]


class AfbwsCatalogChannelV1Symbols1(TypedDict):
    """
    ONE operation for both sources, answered only from the source's own catalog (Finam: the `finam.db` mirror, MOEX: the pool snapshot) — the broker / exchange is never called. Request: `source`, optional `query` (symbol or name, case-insensitive), `mic`, `kind`, `market`, `include_archived`, `unassigned` (server-side, over the stored state), `limit` (1..100, default 50) and `offset` (default 0): a window of `limit` rows starting at `offset` of the filtered list. Response: `source`, `total` (rows in the whole filtered list), `offset`, `fetched_at`, `items[]` (<=100).
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.symbols.v1"]
    request_id: AfbwsCommonV1RequestId
    source: AfbwsCatalogChannelV1Source
    query: NotRequired[str]
    kind: NotRequired[Literal["listing", "derivative"]]
    market: NotRequired[Literal["stock", "currency", "index", "futures", "other"]]
    include_archived: NotRequired[bool]
    unassigned: NotRequired[bool]
    limit: NotRequired[int]
    total: NotRequired[int]
    fetched_at: NotRequired[str | None]
    items: NotRequired[list[AfbwsCatalogChannelV1SymbolRow]]
    offset: NotRequired[int]
    mic: NotRequired[str]


class AfbwsCatalogChannelV1Symbols2(TypedDict):
    """
    ONE operation for both sources, answered only from the source's own catalog (Finam: the `finam.db` mirror, MOEX: the pool snapshot) — the broker / exchange is never called. Request: `source`, optional `query` (symbol or name, case-insensitive), `mic`, `kind`, `market`, `include_archived`, `unassigned` (server-side, over the stored state), `limit` (1..100, default 50) and `offset` (default 0): a window of `limit` rows starting at `offset` of the filtered list. Response: `source`, `total` (rows in the whole filtered list), `offset`, `fetched_at`, `items[]` (<=100).
    """

    channel: Literal["catalog"]
    schema: Literal["afbws.catalog.symbols.v1"]
    request_id: AfbwsCommonV1RequestId
    source: AfbwsCatalogChannelV1Source
    query: NotRequired[str]
    kind: NotRequired[Literal["listing", "derivative"]]
    market: NotRequired[Literal["stock", "currency", "index", "futures", "other"]]
    include_archived: NotRequired[bool]
    unassigned: NotRequired[bool]
    limit: NotRequired[int]
    total: int
    fetched_at: str | None
    items: list[AfbwsCatalogChannelV1SymbolRow]
    offset: int
    mic: NotRequired[str]


AfbwsCatalogChannelV1Symbols: TypeAlias = (
    AfbwsCatalogChannelV1Symbols1 | AfbwsCatalogChannelV1Symbols2
)


AfbwsCatalogChannelV1Root: TypeAlias = (
    AfbwsCatalogChannelV1Snapshot
    | AfbwsCatalogChannelV1Symbols
    | AfbwsCatalogChannelV1Support
    | AfbwsCatalogChannelV1Commit
    | AfbwsCatalogChannelV1Refresh
    | AfbwsCatalogChannelV1Error
)


AfbwsCommonV1ErrorCode: TypeAlias = Literal[
    "not_found",
    "invalid_schema",
    "invalid_channel",
    "validation_error",
    "conflict",
    "internal_error",
    "forbidden",
    "bf_offline",
    "unsupported_action",
    "superseded",
    "busy",
]


AfbwsCommonV1InstrumentKey: TypeAlias = str


AfbwsCommonV1RequestId: TypeAlias = str


AfbwsCommonV1Root: TypeAlias = Any


class AfbwsDealChannelV1DealOpenPosition(TypedDict):
    qty: int
    avg_price: str
    as_of: str


class AfbwsDealChannelV1DealRealizedPnl(TypedDict):
    value: str | None
    degraded: Literal["missing_price", "missing_step_price"] | None


class AfbwsGpChannelV1SyncPush(TypedDict):
    """
    items[] — upsert by id (bind: tradeplan_id set on publish/amend; release: tradeplan_id cleared on plan physical delete), full authoritative afb.gp.v1 record, same shape as set.response. Never a snapshot. Primitive deletion (archival freeze) is NOT conveyed by this push — a dropped primitive was, by construction, bound to a plan and only rendered while that plan is selected; the plan's own afbws.tradeplan.sync.push.v1 (status: archived, frozen numeric conditions) already replaces its on-chart representation.
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.sync.push.v1"]
    items: list[GpV1]


class AfbwsInstrumentChannelV1CatalogDerivative(TypedDict):
    """
    One row per derivative: a serial futures, a perpetual futures, or (reserved) an option. Carries no contract list — the contract↔derivative link lives on the contract, as `items[].derivative` pointing back at `derivative` here; a client expands a `kind=derivative` asset member by `member.derivative -> this.derivative -> items[] where item.derivative == that`. The word `series` also names a `poolEntry.kind` and one value of this `kind` — independent namespaces. Read side only — the write form is still `commitRequest.series[]` / `seriesUpsert`; there is deliberately no `commitRequest.derivatives`.
    """

    derivative: str
    kind: Literal["perpetual", "series", "options"]
    underlying: str | None
    name: NotRequired[str | None]


class AfbwsInstrumentChannelV1ExpirationCandidate(TypedDict):
    instrument_key: AfbwsCommonV1InstrumentKey
    ticker: str
    expiration: str
    shortname: NotRequired[str]


class AfbwsInstrumentChannelV1ExpirationListRequest(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.expiration.list.request.v1"]
    request_id: AfbwsCommonV1RequestId


class AfbwsInstrumentChannelV1ExpirationListResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.expiration.list.response.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[AfbwsInstrumentChannelV1ExpirationNotice]


class AfbwsInstrumentChannelV1ExpirationNotice(TypedDict):
    """
    Present while `0 <= days_left <= <the caller's `interface.futures_days_to_expiration`>` (0 disables the notice entirely) and the caller uses the contract (`usage` is not all-zero). `candidates[]` are the other ACTIVE contracts of the same derivative that expire AFTER this one, ordered by expiration then key; the FIRST is the default proposal (the nearest by expiration). Empty when no later contract exists.
    """

    instrument_key: AfbwsCommonV1InstrumentKey
    ticker: str
    shortname: NotRequired[str]
    expiration: str
    days_left: int
    usage: AfbwsInstrumentChannelV1ExpirationUsage
    candidates: list[AfbwsInstrumentChannelV1ExpirationCandidate]


class AfbwsInstrumentChannelV1ExpirationPush(TypedDict):
    """
    Sent by the daily expiration job to connected users when a new notice stage is reached, so the card appears without a reload. An empty `items[]` clears the card.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.expiration.push.v1"]
    items: list[AfbwsInstrumentChannelV1ExpirationNotice]


class AfbwsInstrumentChannelV1ExpirationUsage(TypedDict):
    """
    Trade plans and deals are deliberately not listed: they carry only a bare `ticker`, are level-sensitive and are never replaced by the contract-roll flow — after expiration they are archived by the server's expiration policy.
    """

    alarms: int
    primitives: int
    sets: int
    favorites: int


AfbwsInstrumentChannelV1FavoriteColor: TypeAlias = Literal[
    "yellow", "red", "blue", "green", "gray", "orange", "cyan", "purple", "pink", "teal"
]


class AfbwsInstrumentChannelV1FavoriteEntry(TypedDict):
    kind: Literal["instrument", "asset"]
    key: str
    color: AfbwsInstrumentChannelV1FavoriteColor


class AfbwsInstrumentChannelV1FavoriteRef(TypedDict):
    """
    `key` is `instrument_key` for kind "instrument" and `asset_id` for kind "asset" — different identifier spaces, hence a dedicated field name rather than catalogAssetMember's `code`, which would invite the wrong join.
    """

    kind: Literal["instrument", "asset"]
    key: str


class AfbwsInstrumentChannelV1FavoritesRequest(TypedDict):
    """
    Carries no data beyond the envelope; there is no way to set or replace favorites through this operation — that is `paint`. Legal at any time, including right after a `paint` to read back the merged result.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.favorites.request.v1"]
    request_id: AfbwsCommonV1RequestId


class AfbwsInstrumentChannelV1FavoritesResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.favorites.response.v1"]
    request_id: AfbwsCommonV1RequestId
    favorites: list[AfbwsInstrumentChannelV1FavoriteEntry]


class AfbwsInstrumentChannelV1PaintRequest(TypedDict):
    """
    Every section is optional and a list; an empty request is legal and a no-op — reading favorites back is `favorites`, not `paint`. `mark` paints one or more refs (repainting an already-favorited ref is legal — that is how its color changes); a ref repeated within the same `mark` list is applied in order, the last color wins. `unmark` removes one or more refs, idempotently — unmarking a ref that is not a favorite is a no-op, not an error. `order` REPLACES the caller's whole display order, the same idiom as commit's `asset_set_order` — not a partial reshuffle.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.paint.request.v1"]
    request_id: AfbwsCommonV1RequestId
    mark: NotRequired[list[AfbwsInstrumentChannelV1FavoriteEntry]]
    unmark: NotRequired[list[AfbwsInstrumentChannelV1FavoriteRef]]
    order: NotRequired[list[AfbwsInstrumentChannelV1FavoriteRef]]


class AfbwsInstrumentChannelV1PaintResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.paint.response.v1"]
    request_id: AfbwsCommonV1RequestId
    marked: NotRequired[list[AfbwsInstrumentChannelV1FavoriteEntry]]
    unmarked: NotRequired[list[AfbwsInstrumentChannelV1FavoriteRef]]
    order: NotRequired[list[AfbwsInstrumentChannelV1FavoriteRef]]


class AfbwsInstrumentChannelV1RefreshMarketReport(TypedDict):
    """
    Turns a silently-obsolete column mapping into a visible diagnostic instead of quietly-empty fields. `status: "failed"` means the market's rows were NOT applied — a missing required column, an empty answer, or a network error all count as failed, since a partial answer must not look like a complete one.
    """

    market: str
    status: Literal["ok", "failed"]
    missing_required: NotRequired[list[str]]
    missing_optional: NotRequired[list[str]]
    type_mismatch: NotRequired[list[str]]
    malformed_rows: NotRequired[int]
    board_conflicts: NotRequired[list[dict[str, Any]]]
    error: NotRequired[str]


AfbwsInstrumentChannelV1ReplaceKind: TypeAlias = Literal[
    "alarms", "primitives", "sets", "favorites"
]


class AfbwsInstrumentChannelV1ReplaceRejection(TypedDict):
    kind: AfbwsInstrumentChannelV1ReplaceKind
    id: str
    code: AfbwsCommonV1ErrorCode
    message: NotRequired[str]


class AfbwsInstrumentChannelV1ReplaceRequest(TypedDict):
    """
    `to_key` must be an ACTIVE contract of the same derivative as `from_key` (the server validates; the card offers `expirationNotice.candidates[]`, the first being the default). `kinds` limits what is moved; omitted = all four. Prices and levels are NEVER adjusted — alarm conditions and primitive levels are copied as they are. Partial results are normal: what could not be moved is listed in `rejected[]`, the rest is applied. Idempotent: repeating the request moves nothing more.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.replace.request.v1"]
    request_id: AfbwsCommonV1RequestId
    from_key: AfbwsCommonV1InstrumentKey
    to_key: AfbwsCommonV1InstrumentKey
    kinds: NotRequired[list[AfbwsInstrumentChannelV1ReplaceKind]]


class AfbwsInstrumentChannelV1ReplaceResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.replace.response.v1"]
    request_id: AfbwsCommonV1RequestId
    from_key: AfbwsCommonV1InstrumentKey
    to_key: AfbwsCommonV1InstrumentKey
    replaced: AfbwsInstrumentChannelV1ExpirationUsage
    rejected: list[AfbwsInstrumentChannelV1ReplaceRejection]
    items: list[AfbwsInstrumentChannelV1ExpirationNotice]


class AfbwsMarketChannelV1DataStatus(TypedDict):
    """
    Present on a `series` message only when it is NOT a normal fresh fetch: either the `moex` source's circuit breaker was open when this was built (data served from `market_cache` only — no network at all; a `candles` table may be missing entirely since candles have no persistent cache, see AFB `backend/market/tables.py::build_series_tables_cache_only`) or AFB's freshness detector found this instrument's calendar section/kind lagging behind a live market (`backend/sources/freshness.py`) while the underlying fetch itself still nominally succeeded. Absent on `data_status` means a normal, fresh answer.
    """

    state: Literal["stale", "partial"]
    source: str
    reason: str
    since: str


class AfbwsMarketChannelV1SourceStatus(TypedDict):
    """
    Unsolicited push, no `request_id`: sent to every connection that negotiated this channel on each health-state transition of an external source (plan стабильности AFB, Этап 3 — `backend/sources/health.py`'s circuit breaker/degraded-window states) and once as a full snapshot right after this channel's first `subscribe`/`get`. Replaces the removed legacy `stream/loop_status`. `sources` lists every source AFB currently tracks (`moex`/`getcourse`); a source absent from the list has never reported a call yet — treat as "ok".
    """

    channel: Literal["market"]
    schema: Literal["afbws.market.source_status.v1"]
    sources: list[AfbwsMarketChannelV1SourceStatusEntry]


class AfbwsMarketChannelV1SourceStatusEntry(TypedDict):
    source: str
    state: Literal["ok", "degraded", "down"]
    since: str
    reason: NotRequired[str]


class AfbwsTradeplanChannelV1ArchiveRequest(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.archive.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class AfbwsTradeplanChannelV1ArchiveResponse(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.archive.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: TradeplanEntity


class AlarmAckEvent(TypedDict):
    schema: Literal["afb.alarm.trigger_ack.v1"]
    alarm_id: str
    triggered_at: str


class AlarmAckRequest(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.ack.request.v1"]
    request_id: AfbwsCommonV1RequestId
    events: list[AlarmAckEvent]


class AlarmAckResponse(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.ack.response.v1"]
    request_id: AfbwsCommonV1RequestId
    results: list[AlarmAckResultItem]


class AlarmAckResultItem(TypedDict):
    schema: Literal["afbws.alarm.ack_result.v1"]
    alarm_id: str
    triggered_at: str
    status: Literal["ok", "not_found"]


class AlarmDeleteRequest(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.delete.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class AlarmDeleteResponse(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.delete.response.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class AlarmErrorResponse(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.error.response.v1"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]


class AlarmGetRequest(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.get.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class AlarmGetResponse(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.get.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: AlarmV1


class AlarmListRequest(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.list.request.v1"]
    request_id: AfbwsCommonV1RequestId
    ticker: NotRequired[str]


class AlarmListResponse(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.list.response.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[AlarmV1]


class AlarmSetRequest(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.set.request.v1"]
    request_id: AfbwsCommonV1RequestId
    item: AlarmV1


class AlarmSetResponse(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.set.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: AlarmV1


class AlarmTriggerEvent(TypedDict):
    schema: Literal["afb.alarm.trigger.v1"]
    alarm_id: str
    triggered_at: str
    alarm: AlarmV1
    current_price: NotRequired[float]


class AlarmTriggeredPush(TypedDict):
    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.triggered.push.v1"]
    events: list[AlarmTriggerEvent]


AlarmChannelV1Message: TypeAlias = (
    AlarmGetRequest
    | AlarmGetResponse
    | AlarmListRequest
    | AlarmListResponse
    | AlarmSetRequest
    | AlarmSetResponse
    | AlarmDeleteRequest
    | AlarmDeleteResponse
    | AlarmErrorResponse
    | AlarmTriggeredPush
    | AlarmAckRequest
    | AlarmAckResponse
)


class AlarmV1(TypedDict):
    """
    AFB-side user alarm — like afb.tradeplan.v2, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel; it is documented here (rather than only in AFB) because it shares condition.v1.json's operator vocabulary with deal.v2 and tradeplan.v2. Replaces the legacy YAML shape (condition_type/trigger_type/value_type/value/value_ref flat fields, break_up/break_down operator names) with a conditionNode. Legacy alarms are read via a lazy converter (see docs/PROTOCOL.md 'Алармы' mapping table) and rewritten in this format on next save/reactivation; the API layer only accepts/emits this format going forward. `period` is the alarm's overall computation timeframe (legacy default '10min'); when `condition` is a price candle operator, `condition.timeframe` carries the candle timeframe and by construction equals `period`.
    """

    schema: Literal["afb.alarm.v1"]
    id: str
    ticker: str
    condition: AlarmV1AlarmConditionNode
    period: NotRequired[ConditionV1Timeframe]
    trigger_frequency: NotRequired[Literal["once", "every_candle", "daily"]]
    status: NotRequired[Literal["active", "triggered", "expired"]]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]
    triggered_at: NotRequired[str]
    delivery_at: NotRequired[str]
    trigger_count: NotRequired[int]


class AlarmV1AlarmConditionNode1(TypedDict):
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: NotRequired[Literal["touch"]]


class AlarmV1AlarmConditionNode2(TypedDict):
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: Literal["breakout", "breakdown", "crossing"]
    timeframe: ConditionV1Timeframe


class AlarmV1AlarmConditionNode3(TypedDict):
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: ConditionV1PriceLevelOp


class AlarmV1AlarmConditionNode4(TypedDict):
    left: AlarmV1AlarmIndicatorExpr
    right: ConditionV1RightConst | AlarmV1AlarmIndicatorExpr
    op: ConditionV1ScalarOp


class AlarmV1AlarmConditionNode5(TypedDict):
    left: ConditionV1DatasetExpr
    right: ConditionV1RightConst | ConditionV1DatasetExpr
    op: ConditionV1ScalarOp


AlarmV1AlarmConditionNode: TypeAlias = (
    AlarmV1AlarmConditionNode1
    | AlarmV1AlarmConditionNode2
    | AlarmV1AlarmConditionNode3
    | AlarmV1AlarmConditionNode4
    | AlarmV1AlarmConditionNode5
)


class AlarmV1AlarmIndicatorExpr(TypedDict):
    """
    Unlike condition.v1.json#/$defs/indicatorExpr, only `source`+`id` are required: AFB resolves `type`/`field`/`params` from the user's saved indicator settings by `id` rather than carrying them inline.
    """

    source: Literal["indicator"]
    id: str
    type: NotRequired[Literal["wma", "kama", "psar"]]
    field: NotRequired[str]
    params: NotRequired[dict[str, Any]]


class AlarmV2(TypedDict):
    """
    v2 of afb.alarm.v1 (full copy): the only difference is that the instrument is identified by the full composite `instrument_key` (<MIC>[:<board|market>]:<ticker>, case-sensitive, never normalized — see afbws/common.v1.json#/$defs/instrumentKey) instead of the short `ticker`. v1 stays supported for frontends that did not negotiate afbws.alarm.channel.v2; the backend stores v2 and converts v1<->v2 at the channel boundary. AFB-side entity, NOT an AsyncAPI wire message, never crosses the AFB<->BF channel. it is documented here (rather than only in AFB) because it shares condition.v1.json's operator vocabulary with deal.v2 and tradeplan.v2. Replaces the legacy YAML shape (condition_type/trigger_type/value_type/value/value_ref flat fields, break_up/break_down operator names) with a conditionNode. Legacy alarms are read via a lazy converter (see docs/PROTOCOL.md 'Алармы' mapping table) and rewritten in this format on next save/reactivation; the API layer only accepts/emits this format going forward. `period` is the alarm's overall computation timeframe (legacy default '10min'); when `condition` is a price candle operator, `condition.timeframe` carries the candle timeframe and by construction equals `period`.
    """

    schema: Literal["afb.alarm.v2"]
    id: str
    instrument_key: AfbwsCommonV1InstrumentKey
    condition: AlarmV2AlarmConditionNode
    period: NotRequired[ConditionV1Timeframe]
    trigger_frequency: NotRequired[Literal["once", "every_candle", "daily"]]
    status: NotRequired[Literal["active", "triggered", "expired"]]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]
    triggered_at: NotRequired[str]
    delivery_at: NotRequired[str]
    trigger_count: NotRequired[int]


class AlarmV2Ack(TypedDict):
    """
    Request: `events[]` (afb.alarm.trigger_ack.v2), at least one. Response (same `request_id`): `results[]` — one per event, `status` ok | not_found. A request carrying `results` is invalid.
    """

    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.ack.v2"]
    request_id: AfbwsCommonV1RequestId
    events: NotRequired[list[AlarmV2AckEvent]]
    results: NotRequired[list[AlarmV2AckResultItem]]


class AlarmV2AckEvent(TypedDict):
    schema: Literal["afb.alarm.trigger_ack.v2"]
    alarm_id: str
    triggered_at: str


class AlarmV2AckResultItem(TypedDict):
    schema: Literal["afbws.alarm.ack_result.v2"]
    alarm_id: str
    triggered_at: str
    status: Literal["ok", "not_found"]


class AlarmV2AlarmConditionNode1(TypedDict):
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: NotRequired[Literal["touch"]]


class AlarmV2AlarmConditionNode2(TypedDict):
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: Literal["breakout", "breakdown", "crossing"]
    timeframe: ConditionV1Timeframe


class AlarmV2AlarmConditionNode3(TypedDict):
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: ConditionV1PriceLevelOp


class AlarmV2AlarmConditionNode4(TypedDict):
    left: AlarmV2AlarmIndicatorExpr
    right: ConditionV1RightConst | AlarmV2AlarmIndicatorExpr
    op: ConditionV1ScalarOp


class AlarmV2AlarmConditionNode5(TypedDict):
    left: ConditionV1DatasetExpr
    right: ConditionV1RightConst | ConditionV1DatasetExpr
    op: ConditionV1ScalarOp


AlarmV2AlarmConditionNode: TypeAlias = (
    AlarmV2AlarmConditionNode1
    | AlarmV2AlarmConditionNode2
    | AlarmV2AlarmConditionNode3
    | AlarmV2AlarmConditionNode4
    | AlarmV2AlarmConditionNode5
)


class AlarmV2AlarmIndicatorExpr(TypedDict):
    """
    Unlike condition.v1.json#/$defs/indicatorExpr, only `source`+`id` are required: AFB resolves `type`/`field`/`params` from the user's saved indicator settings by `id` rather than carrying them inline.
    """

    source: Literal["indicator"]
    id: str
    type: NotRequired[Literal["wma", "kama", "psar"]]
    field: NotRequired[str]
    params: NotRequired[dict[str, Any]]


class AlarmV2Delete(TypedDict):
    """
    Request (`request_id` present): `ids[]` and/or `instrument_keys[]` (at least one; `instrument_keys` = every alarm of those instruments). Response (same `request_id`): `ids[]` actually removed (possibly empty) + `rejected[]`. Push (no `request_id`): `ids[]` (at least one) removed by the server on its own (e.g. alarms of an expired contract cleaned by the expiration policy); `instrument_keys`/`rejected` are not allowed.
    """

    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.delete.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    ids: NotRequired[list[Id]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]
    rejected: NotRequired[list[AlarmV2Rejection]]


class AlarmV2Error(TypedDict):
    """
    Per-item failures of a batched set/delete are reported in that response's `rejected[]`, not here.
    """

    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.error.v2"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]


class AlarmV2List(TypedDict):
    """
    Request: optional filters `ids[]` and/or `instrument_keys[]` (both = intersection; none = every alarm of the caller). Response (same `request_id`): `items[]` (afb.alarm.v2). There is no separate `get`: use `ids`. A request carrying `items` is invalid.
    """

    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.list.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: NotRequired[list[Id]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]
    items: NotRequired[list[AlarmV2]]


class AlarmV2Rejection(TypedDict):
    id: str
    code: AfbwsCommonV1ErrorCode
    message: NotRequired[str]
    details: NotRequired[dict[str, Any]]


class AlarmV2Set(TypedDict):
    """
    Request (`request_id` present): `items[]` — upsert by `item.id`, batched. Response (same `request_id`): applied `items[]` (authoritative records, possibly empty) + `rejected[]` for items that were not applied. Push (no `request_id`, server-initiated): `items[]` (at least one) are authoritative afb.alarm.v2 records that the server created or changed on its own (e.g. alarms moved to another contract by the expiration replace) — upsert by id on the client, never a snapshot; `rejected` is not allowed. Removal is conveyed by `afbws.alarm.delete.v2` without `request_id`.
    """

    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.set.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    items: list[AlarmV2]
    rejected: NotRequired[list[AlarmV2Rejection]]


class AlarmV2TriggerEvent(TypedDict):
    schema: Literal["afb.alarm.trigger.v2"]
    alarm_id: str
    triggered_at: str
    alarm: AlarmV2
    current_price: NotRequired[float]


class AlarmV2Triggered(TypedDict):
    """
    Server-initiated; `events[]` carry the fired alarm with its authoritative afb.alarm.v2 record.
    """

    channel: Literal["alarm"]
    schema: Literal["afbws.alarm.triggered.v2"]
    events: list[AlarmV2TriggerEvent]


AlarmChannelV2Message: TypeAlias = (
    AlarmV2List
    | AlarmV2Set
    | AlarmV2Delete
    | AlarmV2Ack
    | AlarmV2Triggered
    | AlarmV2Error
)


class Alarms(TypedDict):
    statuses: NotRequired[list[str]]


class Backstop(TypedDict):
    """
    Per-deal overrides for the hybrid-mode server-side backstop order; unset fields fall back to the executing BF's own config defaults. Meaningful only when execution_mode is `hybrid`.
    """

    offset_steps: NotRequired[int]
    stop_price: NotRequired[DecimalString]
    max_loss_steps: NotRequired[int]
    take_profit: NotRequired[bool]


BfId: TypeAlias = str


class BfRegistryEntry(TypedDict):
    """
    Shared public-view basis for `bfs` (registry push) and `connector` (record CRUD) — see BFRegistryEntry.to_public_dict() in AFB/backend/trade/models.py.
    """

    bf_id: str
    name: str
    enabled: bool
    broker: str
    protocol: str


class BfsRegistryEntry(BfRegistryEntry):
    connected: bool
    dry_run: bool
    dry_run_afb: NotRequired[bool]
    dry_run_bf: NotRequired[bool]
    account_id: NotRequired[str]
    capabilities: NotRequired[dict[str, Any]]
    daemon: NotRequired[dict[str, Any]]


class BfsRegistryPush(TypedDict):
    """
    See AFB/docs/WS_EXECUTION_CHANNELS.md#bfs--registry and ExecutionService.accessible_bfs_map (AFB/backend/trade/service.py) — extends the public registry-entry minimum with runtime keys.
    """

    type: Literal["registry"]
    data: Data


class Binding(TypedDict):
    account_id: NotRequired[str]
    symbol: NotRequired[str]


class Breakpoints(TypedDict):
    lg: NotRequired[int]
    xl: NotRequired[int]


class BrokerAccountPayload(TypedDict):
    """
    DEPRECATED: superseded by broker.accounts (see payloads/broker.accounts.json) — kept for wire compatibility with AFB builds that have not negotiated multi_account. Response to broker.get_account, describing only BF's single trading account. Matches belphegor/reporting/broker_snapshots.py::account_snapshot_payload() exactly, including the account_id/broker_account_id split that broker.accounts deliberately drops (see broker.accounts.json). Correlated via correlation_id.
    """

    account_id: str
    broker_account_id: NotRequired[str]
    equity: NotRequired[str | None]
    cash: list[PayloadsBrokerAccountCashBalance]
    positions: list[PayloadsBrokerAccountPosition]


class BrokerAccountsPayload(TypedDict):
    """
    Response to broker.get_accounts and unsolicited push after every reconcile pass (see belphegor/reporting/account_directory.py::AccountDirectory, engine.py::_publish_broker_snapshots) — full list of accounts visible to BF's broker token. Only sent to AFB sessions that advertised session.hello_ack.features.multi_account; a BF instance that has negotiated multi_account with this AFB never sends the deprecated broker.account instead (see broker.account.json). Unlike broker.account, `accounts[].account_id` is the ONLY account identifier — no broker_account_id split, by design (the account_id/broker_account_id duplication in broker.account was judged confusing and deliberately not carried forward). Only `default_account_id` (BF's own trading account, self._account_id) is tradable in this phase — see brokers/port.py::account_id docstring; the rest are read-only until a later multi-account execution phase.
    """

    default_account_id: str
    as_of: str
    accounts: list[PayloadsBrokerAccountsAccount]


class BrokerErrorPayload(TypedDict):
    """
    NACK for any broker.* command (get_account/get_orders/get_catalog/get_instrument/resolve_instrument). Correlated to the request via correlation_id.
    """

    at: NotRequired[str]
    code: str
    command_type: str
    message: NotRequired[str]


class BrokerGetAccountPayload(TypedDict):
    """
    DEPRECATED: superseded by broker.get_accounts (see payloads/broker.get_accounts.json) — kept for wire compatibility with AFB builds that have not negotiated multi_account (see daemon.capabilities.json#/properties/features/properties/multi_account, session.hello_ack.json#/properties/features/properties/multi_account). AFB always sends an empty payload; no fields are read by BF (belphegor/plan_engine/engine.py::_get_account).
    """


class BrokerGetAccountsPayload(TypedDict):
    """
    Request the full list of accounts visible to BF's broker token (not just its own trading account) — see belphegor/reporting/account_directory.py::AccountDirectory. Only sent by AFB after the BF instance advertised daemon.capabilities.features.multi_account (see daemon.capabilities.json). AFB always sends an empty payload today; account_ids is reserved for a future partial-refresh use and is not currently read by BF.
    """

    account_ids: NotRequired[list[str]]


class BrokerGetCatalogPayload1(TypedDict):
    """
    Empty payload requests the meta form (exchanges/markets pairs) of the broker.catalog reply; {exchange,market} together request the slice form (instrument rows) for that market. AFB never sends exchange without market or vice versa (backend/trade/ws_handlers.py::handle_account).
    """

    exchange: str
    market: str


BrokerGetCatalogPayload: TypeAlias = dict[str, Any] | BrokerGetCatalogPayload1


class BrokerGetInstrumentPayload(TypedDict):
    """
    DEPRECATED: superseded by broker.resolve_instrument (see payloads/broker.resolve_instrument.json), which AFB's afbws.instrument.channel.v1 canal uses exclusively for detail lookups. Kept for wire compatibility; belphegor/plan_engine/engine.py::_get_symbol_info still serves it.
    """

    symbol: str


class BrokerGetOrdersPayload(TypedDict):
    """
    AFB always sends an empty payload; no filters exist today.
    """


class BrokerInstrument(TypedDict):
    asset_type: NotRequired[str]
    bond_details: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    decimals: NotRequired[int]
    expiration_date: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    future_details: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    long_initial_margin: NotRequired[str]
    long_risk_rate: NotRequired[str]
    longable: NotRequired[bool]
    lot_size: NotRequired[int]
    market: NotRequired[str]
    mic: NotRequired[str]
    min_step_raw: NotRequired[int]
    name: NotRequired[str]
    price_step: NotRequired[str]
    quote_currency: NotRequired[str]
    short_initial_margin: NotRequired[str]
    short_risk_rate: NotRequired[str]
    shortable: NotRequired[bool]
    tradable: NotRequired[bool]
    updated_at: NotRequired[str]


class BrokerInstrumentPayload(TypedDict):
    """
    Response to broker.get_instrument — the enriched instrument (belphegor/domain/instruments.py InstrumentInfo), unlike broker.catalog's brief CatalogEntry rows. Broker-agnostic explicit allow-list, not an asdict()-based dump: broker-native/Finam-specific fields (asset_type, min_step_raw, long_risk_rate, short_risk_rate, future_details, bond_details) never reach this wire — AFB doesn't read them and admitting them would make this canon description implicitly Finam-shaped (belphegor/reporting/broker_snapshots.py::instrument_resolved_payload builds this explicitly, not via InstrumentInfo.to_broker_instrument_dict(), which a different wire field — deal.accepted's broker_instrument — still uses unchanged). `symbol`/`currency` are the canon names on this wire — they map from InstrumentInfo's own internal `symbol`/`quote_currency` attributes, which are unchanged BF-side. additionalProperties stays true so a future broker plugin can add fields without breaking AFB's validation; required kept to `symbol`. This is a PATCH-level description of existing wire behavior, not a new constraint on it.
    """

    symbol: str
    exchange: NotRequired[str]
    board: NotRequired[str]
    ticker: NotRequired[str]
    mic: NotRequired[str]
    name: NotRequired[str]
    market: NotRequired[str]
    decimals: NotRequired[int]
    price_step: NotRequired[str]
    lot_size: NotRequired[int]
    currency: NotRequired[str]
    expiration_date: NotRequired[str | None]
    tradable: NotRequired[bool]
    longable: NotRequired[bool]
    shortable: NotRequired[bool]
    long_initial_margin: NotRequired[str | None]
    short_initial_margin: NotRequired[str | None]
    updated_at: NotRequired[str | None]


class BrokerInstrumentResolvedPayload(TypedDict):
    """
    Response to broker.resolve_instrument (deal-instrument pre-flight resolution). Deliberately permissive (additionalProperties: true throughout) — both objects are BF-owned shapes; this is a PATCH-level description of existing wire behavior, not a new constraint on it.
    """

    binding: dict[str, Any]
    broker_instrument: dict[str, Any]


class BrokerOrdersPayload(TypedDict):
    """
    Response to broker.get_orders and unsolicited push after every reconcile pass. Matches belphegor/reporting/broker_snapshots.py::stored_orders_payload()/stored_order_to_dict() exactly — orders BF itself placed and is tracking, always for BF's own trading account (see broker.accounts.json — order history for non-default accounts is not available in this phase). `symbol` and `client_order_id` are NOT part of this wire shape; AFB synthesizes/displays without them.
    """

    account_id: str
    orders: list[PayloadsBrokerOrdersOrder]


class BrokerPositionLedgerPayload(TypedDict):
    account_id: str
    entries: list[Entry]
    residual_by_symbol: dict[str, int]


class BrokerResolveInstrumentPayload(TypedDict):
    """
    Deal-instrument pre-flight (AFB's afbws.instrument.channel.v1 `resolve`/`detail`, and the tradeplan publish path) — `deal` is a compiled ExecutionDeal (afb.deal.v1 or afb.deal.v2), the same shape deal.publish carries, sent here purely for its target/instrument fields; BF does not persist it from this command.
    """

    deal: DealV1 | DealV2


class BrokerSizing(TypedDict):
    account_id: NotRequired[str]
    deal_notional: NotRequired[str]
    lots: NotRequired[int]
    required_cash: NotRequired[str]
    required_cash_basis: NotRequired[str]
    sizing_mode: NotRequired[str]
    estimated: NotRequired[bool]


class CalendarUpdatePayload(TypedDict):
    """
    AFB-pushed MOEX trading calendar snapshot, so BF can gate execution and background polling on real trading-session boundaries (holidays, weekend sessions, per-board session phases) instead of a fixed off-hours window. SNAPSHOT SEMANTICS: `sections` is the FULL current calendar this AFB wants this BF to hold, never a diff — on receipt BF REPLACES its entire calendar cache for the connection with this array (replace-all, not merge); a section/day/window absent from a later calendar.update is gone, not merely unchanged. Sent only to a BF that has declared `features.market_calendar` in `daemon.capabilities` (see payloads/daemon.capabilities.json) — a BF that has not declared it never receives this message and continues to gate on its own local config.
    """

    as_of: str
    stale_after_sec: int
    horizon_until: str
    sections: list[Section]


Change = TypedDict(
    "Change",
    {
        "point": NotRequired[str],
        "from": NotRequired[str],
        "to": NotRequired[str],
    },
)


class ChangedItem(TypedDict):
    average_price: NotRequired[str]
    quantity: NotRequired[int]
    symbol: NotRequired[str]


Column: TypeAlias = str


CommonV1Root: TypeAlias = Any


class ConditionNode1(TypedDict):
    """
    Level touched when min(prev, cur) <= level <= max(prev, cur). `op` may be omitted (accepted on read for wire back-compat with pre-touch-op deals/plans) or given explicitly as "touch" (what AFB now always sends). Executed by BF as a LIMIT order.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: NotRequired[Literal["touch"]]


class ConditionNode2(TypedDict):
    """
    breakout: last CLOSED candle of `timeframe` has open < level AND close > level. breakdown: open > level AND close < level. crossing: breakout OR breakdown. Evaluated only on candle close, never intra-bar. Executed by BF as a MARKET order.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: Literal["breakout", "breakdown", "crossing"]
    timeframe: ConditionV1Timeframe


class ConditionNode3(TypedDict):
    """
    Inclusive price level: above = cur >= level, below = cur <= level. Optional `duration` (real continuous seconds on BF's monotonic clock) for protective-time debounce. Executed by BF as a MARKET order.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: ConditionV1PriceLevelOp
    duration: NotRequired[ConditionV1Duration]


class ConditionNode4(TypedDict):
    """
    Scalar comparison (see #/$defs/scalarOp) of an indicator against a constant or another indicator expression. `timeframe` is optional at the schema level (this same conditionNode is reused by afb.alarm.v1, where the timeframe lives on the alarm itself, not the node) but is REQUIRED by the BF executor for afb.deal.v2/afb.tradeplan.v2 indicator conditions — see condition_semantics module docstring. When present, it applies to BOTH sides of the comparison: left and right are evaluated on the same bar series. Indicator values are a (previous CLOSED bar, current FORMING bar) pair, matching evaluate_scalar_op's cur/prev semantics.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1IndicatorExpr
    right: ConditionV1RightConst | ConditionV1IndicatorExpr
    op: ConditionV1ScalarOp
    timeframe: NotRequired[ConditionV1Timeframe]


class ConditionNode5(TypedDict):
    """
    Scalar comparison (see #/$defs/scalarOp) of a dataset value (position.*, orders, hhi, trades) against a constant or another dataset expression of the same dataset_id.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1DatasetExpr
    right: ConditionV1RightConst | ConditionV1DatasetExpr
    op: ConditionV1ScalarOp


class ConditionNode6(TypedDict):
    """
    Fires as soon as a live price exists — no price level of its own. Replaces the pre-2.0.9 sentinel of a price/touch-or-above condition against a zero const (still accepted on read indefinitely for deals/tradeplans already persisted in that shape — see condition_semantics module docstring). `op` and `right` are placeholders required only for structural symmetry with the other branches; their VALUE carries no meaning and must never be read by any consumer — dispatch on `left.source == "immediate"` alone. Meaningful only on an entry leg (BF/AFB reject it on stop_loss/take_profit — a condition that is always true would close a position instantly); `duration` is inapplicable and rejected by consumers, not by this schema (matching this vocabulary's existing convention: role/field applicability that depends on where the node sits, not on the node's own shape, is enforced by consumers, e.g. protocol/validation.py).
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1ImmediateExpr
    right: ConditionV1RightConst
    op: Literal["above"]


ConditionNode: TypeAlias = (
    ConditionNode1
    | ConditionNode2
    | ConditionNode3
    | ConditionNode4
    | ConditionNode5
    | ConditionNode6
)


class ConditionTriggeredPayload(TypedDict):
    at: NotRequired[str]
    condition_id: str
    deal_id: str
    phase: NotRequired[str]
    price: NotRequired[str]


class ConditionV1DatasetExpr(TypedDict):
    """
    position.* / orders / hhi / trades datasets share this shape; dataset_id=volume is declared here but temporarily unsupported by AFB/BF backends (see condition_semantics module docstring) and not offered by the UI.
    """

    source: Literal["dataset"]
    field: str
    dataset_id: NotRequired[str]
    params: NotRequired[dict[str, Any]]


ConditionV1Duration: TypeAlias = int


class ConditionV1ImmediateExpr(TypedDict):
    source: Literal["immediate"]


class ConditionV1IndicatorExpr(TypedDict):
    """
    AFB resolves alarm indicators by `id`, BF by `type`+`params`.
    """

    source: Literal["indicator"]
    type: Literal["wma", "kama", "psar"]
    params: NotRequired[dict[str, Any]]
    id: NotRequired[str]


class ConditionV1PriceExpr(TypedDict):
    source: Literal["price"]


ConditionV1PriceLevelOp: TypeAlias = Literal["above", "below"]


class ConditionV1RightConst(TypedDict):
    const: DecimalString


ConditionV1ScalarOp: TypeAlias = Literal[
    "above", "below", "crosses_above", "crosses_below", "crossing"
]


ConditionV1Timeframe: TypeAlias = Literal[
    "5min", "10min", "15min", "30min", "1h", "2h", "4h", "1d"
]


class ConfigDashboard(TypedDict):
    """
    `cols` is clamped 8-24 by the frontend normalizer rather than enforced here.
    """

    cols: NotRequired[int]
    breakpoints: NotRequired[Breakpoints]
    layouts: NotRequired[Layouts]
    widgets: NotRequired[dict[str, Widgets]]


class ConfigDataset(TypedDict):
    """
    Freeform per-series style config (color/style/panel triplets, e.g. positions.longColor, trades.tradesBColor). Keys vary per series and grow as new series are added — deliberately open string/number maps rather than enumerating dozens of purely presentational keys.
    """

    positions: NotRequired[dict[str, str | float]]
    trades: NotRequired[dict[str, str | float]]
    hhi: NotRequired[dict[str, str | float]]
    orders: NotRequired[dict[str, str | float]]


class ConfigDefaults(TypedDict):
    """
    Merged under every user's own settings. A write (manager only) requires `dataset`.
    """

    interface: NotRequired[ConfigInterface]
    dataset: NotRequired[ConfigDataset]
    dashboard: NotRequired[ConfigDashboard]


class ConfigDefaultsMessage(TypedDict):
    """
    Request without `defaults` = read (any user). Request with `defaults` = write (manager only, else error `forbidden`); `defaults.dataset` is required on write. The response always carries the full stored `defaults`. Push (no `request_id`) is sent right after `auth_ok`; `defaults` is required there.
    """

    channel: Literal["config"]
    schema: Literal["afbws.config.defaults.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    defaults: NotRequired[ConfigDefaults]


class ConfigError(TypedDict):
    """
    `item` is populated on a refused settings/defaults mutation: the authoritative current server state (a `settings` object for afbws.config.settings.v1, a `defaults` object for afbws.config.defaults.v1); the client applies it and shows `message`.
    """

    channel: Literal["config"]
    schema: Literal["afbws.config.error.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    code: AfbwsCommonV1ErrorCode
    message: str
    item: NotRequired[dict[str, Any]]


class ConfigHelp(TypedDict):
    """
    Available to every connection. Request carries `section` (basename of a markdown file, `[A-Za-z0-9]+`); the response echoes `section` and adds `content` (HTML rendered from the markdown). Unknown section: error `not_found`; bad name: `validation_error`.
    """

    channel: Literal["config"]
    schema: Literal["afbws.config.help.v1"]
    request_id: AfbwsCommonV1RequestId
    section: str
    content: NotRequired[str]


class ConfigInterface(TypedDict):
    layout: NotRequired[ConfigLayout]
    snow_mode: NotRequired[bool]
    confirm_delete: NotRequired[bool]
    smart_alarms: NotRequired[bool]
    preset_timeframes: NotRequired[PresetTimeframes]
    chart_toolbar: NotRequired[ConfigV1ChartToolbar]
    services_filters: NotRequired[ConfigV1ServicesFilters]
    trade_plan_default_capital_rub: NotRequired[float]
    futures_days_to_expiration: NotRequired[int]


class ConfigLayout(TypedDict):
    offset_right: NotRequired[int]
    offset_top: NotRequired[int]
    debug_mode: NotRequired[bool]


class ConfigProfile(TypedDict):
    name: NotRequired[str]
    email: NotRequired[str]
    telegram: NotRequired[str]
    notify_telegram: NotRequired[bool]
    notify_email: NotRequired[bool]
    notify_system: NotRequired[bool]
    sound: NotRequired[str]


class ConfigRoleTier(TypedDict):
    limits: NotRequired[dict[str, int]]
    members: NotRequired[list[str]]


class ConfigRoles(TypedDict):
    """
    Request without `tiers`/`capabilities` = read; with both = write (saved into roles.yaml, runtime reloaded). The response always carries the full snapshot. Non-manager: error `forbidden`.
    """

    channel: Literal["config"]
    schema: Literal["afbws.config.roles.v1"]
    request_id: AfbwsCommonV1RequestId
    tiers: NotRequired[dict[str, ConfigRoleTier]]
    capabilities: NotRequired[dict[str, Any]]
    default_tier: NotRequired[str]
    groups_yaml: NotRequired[list[dict[str, Any]]]
    getcourse_groups: NotRequired[list[dict[str, Any]]]
    getcourse_groups_error: NotRequired[str | None]
    limits_template: NotRequired[LimitsTemplate]


class ConfigSettings(TypedDict):
    """
    Request without `settings` = read. Request with `settings` = partial write (blocks `profile`/`interface`/`dataset`/`dashboard` deep-merged, `trade` replaced whole; `profile.notify_system` from a non-manager is ignored). The response (same `request_id`) always carries the full stored `settings`. Push (no `request_id`) carries the full `settings`, sent right after `auth_ok`; `settings` is required there. Refusal: `afbws.config.error.v1` with `item` = current settings.
    """

    channel: Literal["config"]
    schema: Literal["afbws.config.settings.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    settings: NotRequired[ConfigSettingsV1]


class ConfigSettingsV1(TypedDict):
    """
    Canon of the user settings carried by `afbws.config.settings.v1` (root = the `settings` object) and of the platform defaults carried by `afbws.config.defaults.v1` (`$defs/defaults`). Replaces the parked `draft/` schemas and the legacy `settings` channel payload. Every property is optional: the on-disk user file stores only what the user overrode and a write is a partial patch (blocks `profile`/`interface`/`dataset`/`dashboard` are deep-merged, `trade` is replaced whole). Not part of the payload any more: `limits` (travels in `auth_ok`), `favorites` (channel `instrument`), `indicators`/`primitives` (channel `gp`), alarms/tradeplans (their own channels). Booleans are real JSON booleans.
    """

    profile: NotRequired[ConfigProfile]
    interface: NotRequired[ConfigInterface]
    dataset: NotRequired[ConfigDataset]
    dashboard: NotRequired[ConfigDashboard]
    trade: NotRequired[ConfigTrade]


class ConfigToken1(TypedDict):
    """
    Request carries `kind` and `token`; the server validates the token against the service (MOEX / GetCourse / Finam; a Finam token must be read-only, a trading token is rejected with `validation_error` and never stored), stores it in the plain-text secrets/*.token file and applies it at runtime. The response carries `kind` and `ok: true` and NEVER the token. Failure: error `validation_error` (token rejected by the service) or `internal_error`; non-manager: `forbidden`.
    """

    channel: Literal["config"]
    schema: Literal["afbws.config.token.v1"]
    request_id: AfbwsCommonV1RequestId
    kind: Literal["moex", "getcourse", "finam"]
    token: str
    ok: NotRequired[Literal[True]]


class ConfigToken2(TypedDict):
    """
    Request carries `kind` and `token`; the server validates the token against the service (MOEX / GetCourse / Finam; a Finam token must be read-only, a trading token is rejected with `validation_error` and never stored), stores it in the plain-text secrets/*.token file and applies it at runtime. The response carries `kind` and `ok: true` and NEVER the token. Failure: error `validation_error` (token rejected by the service) or `internal_error`; non-manager: `forbidden`.
    """

    channel: Literal["config"]
    schema: Literal["afbws.config.token.v1"]
    request_id: AfbwsCommonV1RequestId
    kind: Literal["moex", "getcourse", "finam"]
    token: NotRequired[str]
    ok: Literal[True]


ConfigToken: TypeAlias = ConfigToken1 | ConfigToken2


ConfigChannelV1Message: TypeAlias = (
    ConfigSettings
    | ConfigDefaultsMessage
    | ConfigHelp
    | ConfigRoles
    | ConfigToken
    | ConfigError
)


class ConfigTrade(TypedDict):
    """
    `default_capital` is persisted by the server into the user's virtual account, not into the settings file; reads return the live value.
    """

    auto_execute: NotRequired[bool]
    default_connector: NotRequired[str]
    default_capital: NotRequired[float]
    default_risk_pct: NotRequired[float]
    notify: NotRequired[ConfigV1TradeNotify]
    chart_deal_markers: NotRequired[bool]
    plan_editor_placement: NotRequired[str]


class ConfigV1ChartToolbar(TypedDict):
    favorite_timeframes: NotRequired[list[str]]
    favorite_datasets: NotRequired[list[str]]
    favorite_primitives: NotRequired[list[str]]


class ConfigV1DashboardLayoutItem(TypedDict):
    widget: NotRequired[str]
    i: NotRequired[str]
    x: NotRequired[int]
    y: NotRequired[int]
    w: NotRequired[int]
    h: NotRequired[int]


class ConfigV1ServicesFilters(TypedDict):
    instruments: NotRequired[Instruments]
    alarms: NotRequired[Alarms]
    plans: NotRequired[Plans]


class ConfigV1TradeNotify(TypedDict):
    trigger: NotRequired[bool]
    order_placed: NotRequired[bool]
    order_executed: NotRequired[bool]
    position: NotRequired[bool]
    close: NotRequired[bool]
    link: NotRequired[bool]


class ConnectorBackstop(TypedDict):
    offset_steps: NotRequired[int]
    max_loss_steps: NotRequired[int]


class ConnectorExecutionPolicy(TypedDict):
    max_spread_steps: NotRequired[int]
    execution_mode: NotRequired[Literal["client", "hybrid"]]
    backstop: NotRequired[ConnectorBackstop]


class ConnectorListData(TypedDict):
    """
    See ExecutionService.list_connectors_for_user (AFB/backend/trade/service.py).
    """

    connectors: list[ConnectorRecord]
    meta: Meta


class ConnectorRecord(BfRegistryEntry):
    """
    One entry of the `connector` channel (list/get/create/update responses). Owner view (capability trade, user_id in allowed_users) gets everything except the manager-only block; manager gets all fields. See BFRegistryEntry.to_owner_dict()/to_manager_dict() (AFB/backend/trade/models.py) and connector_policy.py for execution_policy validation.
    """

    dry_run: bool | None
    margin_trading: bool | None
    execution_policy: ConnectorExecutionPolicy
    paired: bool
    pairing_pending: bool
    pairing_expires_at: str | None
    connected: NotRequired[bool]
    public_key_id: NotRequired[str]
    public_key_file: NotRequired[str]
    allowed_users: NotRequired[list[str]]


class DaemonCapabilitiesPayload(TypedDict):
    bf_id: str
    broker: NotRequired[str]
    protocol: str
    software_version: NotRequired[str]
    markets: NotRequired[list[str]]
    order_types: NotRequired[list[str]]
    time_in_force: NotRequired[list[Literal["day", "gtc", "ioc"]]]
    sizing_modes: NotRequired[list[str]]
    condition_ops: NotRequired[list[str]]
    condition_nodes: NotRequired[list[str]]
    account_id: NotRequired[str]
    account_aliases: NotRequired[list[str]]
    market_data: NotRequired[MarketData]
    features: NotRequired[Features]


class DaemonCapabilitiesQueryPayload(TypedDict):
    pass


class DaemonStatusPayload(TypedDict):
    active: NotRequired[bool]
    bf_id: str
    broker_connected: NotRequired[bool]
    code: str
    reason: str
    state: NotRequired[str]
    severity: NotRequired[Literal["ok", "warning", "critical"]]
    health: NotRequired[Health]
    changes: NotRequired[list[Change]]


class Data(TypedDict):
    bfs: list[BfsRegistryEntry]


class Data1(TypedDict):
    unrealized: str
    currency: str
    qty: int
    avg_price: str
    last_price: str
    as_of: str


class Dataset(TypedDict):
    dataset_id: Literal["positions", "orders", "hhi", "trades"]
    instrument: DealInstrument
    as_of: str
    stale_after_sec: float
    current: dict[str, float]
    previous: NotRequired[dict[str, float]]


class DatasetSubscribePayload(TypedDict):
    """
    RESERVED — not implemented: this message lets a BF ask AFB for an additional dataset subscription. AFB today derives the full set of needed (dataset_id, instrument) pairs itself from the dataset conditions on deals published to a given BF (see dataset.update.json) and pushes accordingly, so no BF currently sends dataset.subscribe and AFB is not obligated to act on it if received. The shape is reserved on the wire for a future BF-initiated use case (e.g. a BF wanting a dataset ahead of publishing a deal that needs it). Neither BF nor AFB implement this today.
    """

    subscriptions: list[Subscription]


class DatasetUpdatePayload(TypedDict):
    """
    AFB-pushed feed of MOEX/Algopack dataset snapshots (positions/orders/hhi/trades) so BF can evaluate `condition.v1.json`'s dataset operator itself — BF has no exchange/Algopack access of its own and never will (the Algopack token is IP-bound to AFB). SNAPSHOT SEMANTICS: `datasets` is the FULL current set of records this AFB wants this BF to hold, never a diff — on receipt BF REPLACES its entire dataset cache for the connection with this array (replace-all, not merge); a record absent from a later dataset.update is gone, not merely unchanged. An empty `datasets` array is valid and means 'nothing needed' (clears the cache). AFB derives which (dataset_id, instrument) pairs are needed from the dataset conditions on deals currently published to this BF (every leg — entry/stop_loss/take_profit, both left and right sides of the comparison) and resolves exchange-side keying itself (e.g. a futures position dataset is keyed by the underlying asset, not the contract code) — BF must not attempt to re-derive or re-key this.
    """

    datasets: list[Dataset]


class Day(TypedDict):
    date: str
    is_traded: bool
    kind: Literal["N", "W", "H"]
    trade_session_date: str | None


class DealAcceptedPayload(TypedDict):
    at: NotRequired[str]
    binding: NotRequired[Binding]
    broker_instrument: NotRequired[BrokerInstrument]
    broker_sizing: NotRequired[BrokerSizing]
    command_type: str
    deal_id: str
    revision: int
    target_instrument_patch: NotRequired[dict[str, Any]]
    validation: NotRequired[Validation]


class DealAckEvent(TypedDict):
    schema: Literal["afb.deal.trigger_ack.v1"]
    notification_id: str


class DealAckRequest(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.ack.request.v1"]
    request_id: AfbwsCommonV1RequestId
    events: list[DealAckEvent]


class DealAckResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.ack.response.v1"]
    request_id: AfbwsCommonV1RequestId
    results: list[DealAckResultItem]


class DealAckResultItem(TypedDict):
    schema: Literal["afbws.deal.ack_result.v1"]
    notification_id: str
    status: Literal["ok", "not_found"]


DealAmendField: TypeAlias = Literal[
    "entry", "sizing", "stop_loss", "take_profit", "execution_policy"
]


class DealAmendPayload(TypedDict):
    """
    Re-define an existing deal in place. `deal` is the full new definition (its `revision` must be `base_revision` + 1, same `deal_id`). BF gates the change against the allowed-edit matrix (amend_rules) using the deal's live execution phase, then lets reconcile bring broker orders to the new desired state. Unlike deal.publish, the deal's status and observed execution state (orders/positions/phase) are preserved.
    """

    deal_id: str
    base_revision: int
    deal: DealV1 | DealV2


class DealAmendRequest(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.amend.request.v1"]
    request_id: AfbwsCommonV1RequestId
    deal_id: DealId
    deal_edit: NotRequired[DealEdit]
    base_revision: NotRequired[int]


class DealAmendResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.amend.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: DealDetail
    revision: int
    status: str
    accepted: bool


class DealArchivedPayload(TypedDict):
    archived_at: NotRequired[str]
    at: NotRequired[str]
    deal_id: str
    reason: str
    revision: int


class DealDetail(TypedDict):
    deal_id: DealId
    revision: int
    status: str
    execution_phase: str
    bf_id: BfId
    tradeplan_id: str
    ticker: str
    market: NotRequired[Literal["stock", "futures", "currency"]]
    direction: Literal["long", "short"]
    sizing: NotRequired[DealSizing]
    execution_policy: NotRequired[DealExecutionPolicy]
    broker_sizing: NotRequired[DealSizingDisplay]
    realized_pnl: NotRequired[AfbwsDealChannelV1DealRealizedPnl]
    position: NotRequired[AfbwsDealChannelV1DealOpenPosition]
    created_at: str
    updated_at: str
    deal: DealPublicV1
    editable_fields: list[DealAmendField]


class DealEdit(TypedDict):
    entry: NotRequired[DealRoleEdit]
    stop_loss: NotRequired[DealRoleEdit]
    take_profit: NotRequired[DealRoleEdit]
    sizing: NotRequired[DealSizing]
    execution_policy: NotRequired[DealExecutionPolicy]


class DealErrorResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.error.response.v1"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]
    item: NotRequired[DealSummary | DealDetail]


class DealEventPush(TypedDict):
    """
    See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--event. `data` shape depends on category/event — deliberately untyped here, full typing of every BF event payload is out of scope for this migration. Known event/data shapes: `created`/`amended` carry a full deal snapshot (frontend must treat `amended` as an authoritative upsert, same as `created` — previously received but dropped); `status_changed` carries a status delta; BF `deal.archived` arrives to the frontend translated as `status_changed` with `status: "deleted"`; anything else is the raw translated BF envelope payload.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.event.push.v1"]
    deal_id: DealId
    bf_id: BfId
    category: Literal["deal", "order", "position", "condition"]
    event: str
    logged_at: str
    data: dict[str, Any]


class DealExecutionPolicy(TypedDict):
    on_afb_disconnect: NotRequired[str]
    max_spread_steps: NotRequired[int]
    margin_trading: NotRequired[bool]
    execution_mode: NotRequired[Literal["client", "hybrid", "server"]]
    backstop: NotRequired[Backstop]


class DealGetRequest(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.get.request.v1"]
    request_id: AfbwsCommonV1RequestId
    deal_id: DealId


class DealGetResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.get.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: DealDetail


DealId: TypeAlias = str


class DealInstrument(TypedDict):
    exchange: str
    board: str
    ticker: str
    market: NotRequired[Literal["stock", "futures", "currency"]]
    price_step: NotRequired[DecimalString]
    step_price: NotRequired[DecimalString]


class DealLegEdit(TypedDict):
    index: int
    condition: NotRequired[DealV2ConditionNode]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]


class DealListRequest(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.list.request.v1"]
    request_id: AfbwsCommonV1RequestId


class DealListResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.list.response.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[DealSummary]


class DealNewLeg(TypedDict):
    condition: DealV2ConditionNode
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]


class DealOperationItem(TypedDict):
    deal_id: DealId
    action: Literal["activate", "pause", "resume", "cancel", "reconcile", "delete"]
    revision: NotRequired[int]
    cancel_open_orders: NotRequired[bool]


class DealOperationPayload(TypedDict):
    operations: NotRequired[list[Operation]]


class DealOperationRequest(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.operation.request.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[DealOperationItem]


class DealOperationResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.operation.response.v1"]
    request_id: AfbwsCommonV1RequestId
    results: list[DealResult]
    accepted: bool


class DealPnlPush(TypedDict):
    """
    See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--pnl. Periodic unrealized-P&L push, not persisted. `trend` is deliberately absent — it is a frontend-only projection computed from consecutive pushes, never sent by the backend.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.pnl.push.v1"]
    deal_id: DealId
    bf_id: BfId
    data: Data1


class DealPositionsSyncedPayload(TypedDict):
    at: NotRequired[str]
    changed: NotRequired[list[ChangedItem]]
    deal_id: str


class DealPublicDealV1(TypedDict):
    schema: Literal["afb.deal.v1"]
    deal_id: str
    revision: int
    target: DealTarget
    direction: Literal["long", "short"]
    entry: DealV1Entry
    sizing: DealSizing
    risk: NotRequired[Risk]
    execution_policy: NotRequired[DealExecutionPolicy]
    source: DealPublicSource


class DealPublicDealV2(TypedDict):
    schema: Literal["afb.deal.v2"]
    deal_id: str
    revision: int
    target: DealTarget
    direction: Literal["long", "short"]
    entry: list[EntryItem]
    stop_loss: NotRequired[DealPublicExitList]
    take_profit: NotRequired[DealPublicExitList]
    sizing: DealSizing
    execution_policy: NotRequired[DealExecutionPolicy]
    source: DealPublicSource


class DealPublicExitListItem(TypedDict):
    leg_id: NotRequired[TradeplanV2LegId]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: DealV2ConditionNode
    source: NotRequired[DealV2LegSource]


DealPublicExitList: TypeAlias = list[DealPublicExitListItem]


class DealPublicSource(TypedDict):
    tradeplan_id: str


DealPublicV1: TypeAlias = DealPublicDealV1 | DealPublicDealV2


class DealPublishPayload(TypedDict):
    deal: DealV1 | DealV2


class DealPublishRequest(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.publish.request.v1"]
    request_id: AfbwsCommonV1RequestId
    tradeplan_id: str
    bf_id: BfId


class DealPublishResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.publish.response.v1"]
    request_id: AfbwsCommonV1RequestId
    results: list[DealResult]
    accepted: bool


class DealRebindRequest(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.rebind.request.v1"]
    request_id: AfbwsCommonV1RequestId
    deal_id: DealId
    bf_id: BfId


class DealRebindResponse(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.rebind.response.v1"]
    request_id: AfbwsCommonV1RequestId
    results: list[DealResult]
    accepted: bool


class DealRecordPush(TypedDict):
    """
    Authoritative REPLACE of the public deal projection identified by deal_id — the frontend must overwrite its cached copy, never merge partial fields from thin `event` pushes, and never merge-patch this either. `item` is the same public projection as afbws.deal.get.response.v1's item (deal.channel.v1.json#/$defs/dealDetail) — an explicit allow-list built by backend/trade/public_views.py, NOT a serialization of the persisted DealState file (deal_state.v2.json): source_refs, status_history, event_journal, raw orders/positions and observed never appear here.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.record.push.v1"]
    deal_id: DealId
    bf_id: BfId
    item: DealDetail


class DealRejectedPayload(TypedDict):
    at: NotRequired[str]
    code: str
    command_type: str
    deal_id: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]
    message: NotRequired[str]


class DealReportPayload(TypedDict):
    """
    Report attached to deal.status_changed(closed) with the trade-based fill log for the just-closed deal. `trade_id` is not required — tolerant of older BF versions that predate it. The `summary` block (entry/exit_avg_price, realized_pnl, total_commission) was removed in v2.0.10: it had no consumers (AFB computes realized PnL itself from fills/order events), was never in `required`, and `additionalProperties: true` keeps old and new payloads mutually valid — a PATCH, not a breaking change. `fills[].commission` was removed in the same step for the same reason.
    """

    at: NotRequired[str]
    close_reason: NotRequired[str]
    deal_id: str
    revision: int
    status: str
    fills: NotRequired[list[Fill]]


class DealResult(TypedDict):
    deal_id: DealId
    bf_id: BfId
    status: str
    accepted: bool
    revision: NotRequired[int]
    item: NotRequired[DealSummary | DealDetail]
    code: NotRequired[str]
    message: NotRequired[str]


class DealRoleEdit(TypedDict):
    edited: NotRequired[list[DealLegEdit]]
    removed_indices: NotRequired[list[int]]
    reset_indices: NotRequired[list[int]]
    new_legs: NotRequired[list[DealNewLeg]]


class DealSizing(TypedDict):
    mode: Literal["lots", "margin", "risk_currency", "risk_factor", "balance_pct"]
    value: DecimalString


class DealSizingDisplay(TypedDict):
    lots: NotRequired[int]
    required_cash: NotRequired[str]
    resolved_lots: NotRequired[int]


class DealSnapshotPayload(TypedDict):
    deal_id: str
    execution_phase: NotRequired[str]
    observed: NotRequired[dict[str, Any]]
    positions: NotRequired[list[Position]]
    quantity: NotRequired[int]
    status: NotRequired[str]


class DealSource(TypedDict):
    """
    Provenance of this deal's compiled definition. The AFB compiler writes only `tradeplan_id` — the single source of truth for deal->tradeplan linkage (see the tradeplan/deal separation plan). `kind`/`draft_id` are a deprecated pre-separation pair: new AFB never writes them, they may still appear on persisted records created before the deal-channel-migration offline backfill ran. Left open (no additionalProperties restriction, matching the rest of this wire schema) since AFB may carry extra compile metadata here (e.g. `compiled_at`, `primitive_snapshot`, and — Фаза B2 — `leg_ids` [{entry,stop_loss,take_profit}: [leg_id|null, ...], parallel to the matching deal.v2.json leg array] and `removed_plan_leg_ids` [string[], tombstoned plan leg_ids]) that BF does not interpret; AFB's own public projection reduces this object to `tradeplan_id` alone (afbws/deal.public.v1.json#/$defs/source) — the only piece that survives elsewhere is `leg_ids`, re-projected per leg as `leg_id` on the public v2 legs (afbws/deal.public.v1.json#/$defs/legId), never as part of `source`.
    """

    tradeplan_id: NotRequired[str]
    kind: NotRequired[str]
    draft_id: NotRequired[str]


class DealStateV2(TypedDict):
    """
    Shared per-deal YAML/JSON state, identical on AFB and BF. orders[]/positions[] are the authoritative observed facts; observed{} and execution_phase are derived.
    """

    deal_id: str
    revision: int
    owner_user_id: NotRequired[str]
    status: Literal[
        "draft",
        "publishing",
        "published",
        "active",
        "paused",
        "closed",
        "cancelled",
        "orphaned",
    ]
    execution_phase: NotRequired[
        Literal["idle", "awaiting_entry", "entry_working", "holding", "exit_working"]
    ]
    deal: dict[str, Any]
    orders: NotRequired[list[DealStateV2Order]]
    positions: NotRequired[list[DealStateV2Position]]
    observed: NotRequired[dict[str, Any]]
    source_refs: NotRequired[dict[str, Any]]
    status_history: NotRequired[list[dict[str, Any]]]
    event_journal: NotRequired[list[Any]]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


class DealStateV2Order(TypedDict):
    order_id: NotRequired[str]
    side: NotRequired[Literal["buy", "sell"]]
    role: NotRequired[
        Literal["entry", "stop_loss", "take_profit", "cancel_close", "backstop"]
    ]
    status: NotRequired[
        Literal[
            "new",
            "partially_filled",
            "filled",
            "cancelled",
            "rejected",
            "watching",
            "expired",
        ]
    ]
    quantity: NotRequired[int]
    filled_quantity: NotRequired[int]
    leg_index: NotRequired[int]
    limit_price: NotRequired[str | None]
    average_price: NotRequired[str | None]
    stop_price: NotRequired[str | None]
    broker_order_id: NotRequired[str]
    updated_at: NotRequired[str]


class DealStateV2Position(TypedDict):
    instrument: NotRequired[dict[str, Any]]
    symbol: NotRequired[str]
    quantity: NotRequired[int]
    average_price: NotRequired[str | None]
    broker_ref: NotRequired[dict[str, Any]]


class DealStatusChangedPayload(TypedDict):
    at: NotRequired[str]
    deal_id: str
    execution_phase: NotRequired[str]
    last_price: NotRequired[str]
    quantity: NotRequired[int]
    revision: int
    status: str


class DealSummary(TypedDict):
    deal_id: DealId
    revision: int
    status: str
    execution_phase: str
    bf_id: BfId
    tradeplan_id: str
    ticker: str
    market: NotRequired[Literal["stock", "futures", "currency"]]
    direction: Literal["long", "short"]
    sizing: NotRequired[DealSizing]
    execution_policy: NotRequired[DealExecutionPolicy]
    broker_sizing: NotRequired[DealSizingDisplay]
    realized_pnl: NotRequired[AfbwsDealChannelV1DealRealizedPnl]
    position: NotRequired[AfbwsDealChannelV1DealOpenPosition]
    created_at: str
    updated_at: str


class DealTarget(TypedDict):
    bf_id: str
    broker: str
    instrument: DealInstrument
    binding: NotRequired[dict[str, Any]]
    account_id: NotRequired[str]


class DealTriggerEvent(TypedDict):
    schema: Literal["afb.deal.trigger.v1"]
    notification_id: str
    deal_id: DealId
    bf_id: BfId
    event: str
    created_at: str
    data: dict[str, Any]


class DealTriggeredPush(TypedDict):
    channel: Literal["deal"]
    schema: Literal["afbws.deal.triggered.push.v1"]
    events: list[DealTriggerEvent]


DealChannelV1Message: TypeAlias = (
    DealGetRequest
    | DealGetResponse
    | DealListRequest
    | DealListResponse
    | DealPublishRequest
    | DealPublishResponse
    | DealRebindRequest
    | DealRebindResponse
    | DealOperationRequest
    | DealOperationResponse
    | DealAmendRequest
    | DealAmendResponse
    | DealErrorResponse
    | DealRecordPush
    | DealPnlPush
    | DealEventPush
    | DealTriggeredPush
    | DealAckRequest
    | DealAckResponse
)


class DealV1(TypedDict):
    """
    Single-entry / single-exit deal. All prices, steps, sizing values and thresholds are decimal STRINGS. The deal-level `direction` (long/short, same vocabulary as afb.deal.v2) is the single source of truth for position bias. Shared $defs (decimalString/instrument/target/sizing/executionPolicy/source) live in common.v1.json — this file keeps only what's v1-specific (conditionNode/entry/exitBlock); see common.v1.json's description for why.
    """

    schema: Literal["afb.deal.v1"]
    deal_id: str
    revision: int
    owner: NotRequired[Owner]
    target: DealTarget
    direction: Literal["long", "short"]
    entry: DealV1Entry
    sizing: DealSizing
    risk: NotRequired[Risk]
    execution_policy: NotRequired[DealExecutionPolicy]
    archive_reason: NotRequired[str]
    source: NotRequired[DealSource]


class DealV1ConditionNode(TypedDict):
    node_type: Literal["event"]
    id: NotRequired[str]
    op: Literal["above", "below", "crosses_above", "crosses_below", "crossing"]
    left: Left
    right: Right


class DealV1Entry(TypedDict):
    condition: DealV1ConditionNode


class DealV1ExitBlock(TypedDict):
    condition: NotRequired[DealV1ConditionNode]


class DealV2(TypedDict):
    """
    Multi-entry / multi-exit deal. entry, stop_loss, take_profit are root-level lists; each element may carry an optional `percent` (decimal string) and an optional `logic` (`#/$defs/legJoin`) joining it to the PRECEDING element in the same list — see `legJoin` for the full grammar (groups/buckets, `and`/`or` precedence, `percent` placement). Sum of percents per bucket resolves to 100. The deal-level `direction` (long/short) is the single source of truth for position bias — entry legs no longer carry a per-leg `side`, which would let 'buy' and 'sell' legs coexist in the same deal with no defined semantics (a deal is one position, not a basket of unrelated orders). The broker-facing buy/sell of each leg is derived from `direction` and its role: long entry / short exit -> buy; short entry / long exit -> sell. Reuses order/sizing/target defs from deal.v1.json; conditionNode is condition.v1.json's shared vocabulary (see that schema for the full price/indicator/dataset operator semantics) plus the wire-only `node_type` marker. Unlike afb.deal.v1 (fixed above/below/crosses_*/crossing vocabulary), afb.deal.v2 price conditions use condition.v1.json's full operator vocabulary — touch, above/below (inclusive level, no timeframe) and breakout/breakdown/crossing (closed-candle, requires timeframe) — or compare indicator/dataset expressions against a constant or (for indicator/dataset) against another expression of the same kind.
    """

    schema: Literal["afb.deal.v2"]
    deal_id: str
    revision: int
    owner: NotRequired[dict[str, Any]]
    target: DealTarget
    direction: Literal["long", "short"]
    entry: list[EntryItem1]
    stop_loss: NotRequired[DealV2ExitList]
    take_profit: NotRequired[DealV2ExitList]
    sizing: DealSizing
    execution_policy: NotRequired[DealExecutionPolicy]
    archive_reason: NotRequired[str]
    source: NotRequired[DealSource]


class DealV2ConditionNode1(TypedDict):
    """
    Level touched when min(prev, cur) <= level <= max(prev, cur). `op` may be omitted (accepted on read for wire back-compat with pre-touch-op deals/plans) or given explicitly as "touch" (what AFB now always sends). Executed by BF as a LIMIT order.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: NotRequired[Literal["touch"]]


class DealV2ConditionNode2(TypedDict):
    """
    breakout: last CLOSED candle of `timeframe` has open < level AND close > level. breakdown: open > level AND close < level. crossing: breakout OR breakdown. Evaluated only on candle close, never intra-bar. Executed by BF as a MARKET order.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: Literal["breakout", "breakdown", "crossing"]
    timeframe: ConditionV1Timeframe


class DealV2ConditionNode3(TypedDict):
    """
    Inclusive price level: above = cur >= level, below = cur <= level. Optional `duration` (real continuous seconds on BF's monotonic clock) for protective-time debounce. Executed by BF as a MARKET order.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1PriceExpr
    right: ConditionV1RightConst
    op: ConditionV1PriceLevelOp
    duration: NotRequired[ConditionV1Duration]


class DealV2ConditionNode4(TypedDict):
    """
    Scalar comparison (see #/$defs/scalarOp) of an indicator against a constant or another indicator expression. `timeframe` is optional at the schema level (this same conditionNode is reused by afb.alarm.v1, where the timeframe lives on the alarm itself, not the node) but is REQUIRED by the BF executor for afb.deal.v2/afb.tradeplan.v2 indicator conditions — see condition_semantics module docstring. When present, it applies to BOTH sides of the comparison: left and right are evaluated on the same bar series. Indicator values are a (previous CLOSED bar, current FORMING bar) pair, matching evaluate_scalar_op's cur/prev semantics.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1IndicatorExpr
    right: ConditionV1RightConst | ConditionV1IndicatorExpr
    op: ConditionV1ScalarOp
    timeframe: NotRequired[ConditionV1Timeframe]


class DealV2ConditionNode5(TypedDict):
    """
    Scalar comparison (see #/$defs/scalarOp) of a dataset value (position.*, orders, hhi, trades) against a constant or another dataset expression of the same dataset_id.
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1DatasetExpr
    right: ConditionV1RightConst | ConditionV1DatasetExpr
    op: ConditionV1ScalarOp


class DealV2ConditionNode6(TypedDict):
    """
    Fires as soon as a live price exists — no price level of its own. Replaces the pre-2.0.9 sentinel of a price/touch-or-above condition against a zero const (still accepted on read indefinitely for deals/tradeplans already persisted in that shape — see condition_semantics module docstring). `op` and `right` are placeholders required only for structural symmetry with the other branches; their VALUE carries no meaning and must never be read by any consumer — dispatch on `left.source == "immediate"` alone. Meaningful only on an entry leg (BF/AFB reject it on stop_loss/take_profit — a condition that is always true would close a position instantly); `duration` is inapplicable and rejected by consumers, not by this schema (matching this vocabulary's existing convention: role/field applicability that depends on where the node sits, not on the node's own shape, is enforced by consumers, e.g. protocol/validation.py).
    """

    node_type: NotRequired[Literal["event"]]
    id: NotRequired[str]
    left: ConditionV1ImmediateExpr
    right: ConditionV1RightConst
    op: Literal["above"]


class DealV2ConditionNode7(TypedDict):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """

    node_type: Literal["event"]


class DealV2ConditionNode10(DealV2ConditionNode3, DealV2ConditionNode7):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode11(DealV2ConditionNode4, DealV2ConditionNode7):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode12(DealV2ConditionNode5, DealV2ConditionNode7):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode13(DealV2ConditionNode6, DealV2ConditionNode7):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode8(DealV2ConditionNode1, DealV2ConditionNode7):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode9(DealV2ConditionNode2, DealV2ConditionNode7):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


DealV2ConditionNode: TypeAlias = (
    DealV2ConditionNode8
    | DealV2ConditionNode9
    | DealV2ConditionNode10
    | DealV2ConditionNode11
    | DealV2ConditionNode12
    | DealV2ConditionNode13
)


"""
Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
"""


class DealV2ExitListItem(TypedDict):
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: DealV2ConditionNode
    source: NotRequired[DealV2LegSource]


DealV2ExitList: TypeAlias = list[DealV2ExitListItem]


DealV2LegJoin: TypeAlias = Literal["split", "and", "or"]


DealV2LegSource: TypeAlias = Literal["tradeplan", "deal"]


class Deals(TypedDict):
    revision: int
    status: str
    execution_phase: NotRequired[str]
    archived: bool


DecimalString: TypeAlias = str


class Display(TypedDict):
    instrument_label: str
    condition_op: str
    condition_description: str
    condition_text: str


class Display1(TypedDict):
    instrument_label: str
    text: NotRequired[str]


class Display2(TypedDict):
    connector_label: str
    text: NotRequired[str]


class Entry(TypedDict):
    entry_id: str
    account_id: NotRequired[str]
    symbol: str
    qty: int
    avg_price: NotRequired[str | None]
    origin: Literal[
        "bootstrap",
        "orphan_residual",
        "deal_archived",
        "external_close",
        "entry_only_release",
    ]
    source_deal_id: NotRequired[str | None]
    note: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


class Entry1(TypedDict):
    leg_id: NotRequired[TradeplanV2LegId]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: TradeplanV2TpConditionNode


class EntryItem(TypedDict):
    leg_id: NotRequired[TradeplanV2LegId]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: DealV2ConditionNode
    source: NotRequired[DealV2LegSource]


class EntryItem1(TypedDict):
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: DealV2ConditionNode
    source: NotRequired[DealV2LegSource]


class Envelope(TypedDict):
    """
    Signed transport envelope for afb.execution.v1. Every wire message is one of these. payload_hash and signature are computed over canonical JSON (sort_keys, separators=(',',':'), UTF-8); signing string is '{protocol}|{type}|{message_id}|{created_at}|{payload_hash}'.
    """

    protocol: Literal["afb.execution.v1"]
    message_id: str
    correlation_id: NotRequired[str | None]
    causation_id: NotRequired[str | None]
    sender: str
    recipient: str
    type: str
    created_at: str
    expires_at: str
    idempotency_key: NotRequired[str]
    payload_hash: str
    payload: dict[str, Any]
    signature: EnvelopeSignature


class EnvelopeSignature(TypedDict):
    alg: Literal["Ed25519"]
    key_id: str
    value: str


class Features(TypedDict):
    dry_run: NotRequired[bool]
    server_sltp: NotRequired[bool]
    execution_modes: NotRequired[list[Literal["client", "hybrid", "server"]]]
    reports_api: NotRequired[bool]
    catalog: NotRequired[bool]
    multi_account: NotRequired[bool]
    market_calendar: NotRequired[bool]


class Features1(TypedDict):
    """
    AFB-side capability flags for this session — read by BF's afb_client (see afb_client/ws_client.py, alongside dry_run/margin_trading above) to decide what it may send this AFB.
    """

    multi_account: NotRequired[bool]


class Fill(TypedDict):
    trade_id: NotRequired[str]
    order_id: str
    price: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]
    quantity: NotRequired[int]
    role: str
    side: str
    timestamp: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]


class GpDeleteRequest(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.delete.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class GpDeleteResponse(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.delete.response.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class GpErrorDetails(TypedDict):
    tradeplan_ids: NotRequired[list[str]]
    deal_ids: NotRequired[list[str]]
    locked_scopes: NotRequired[list[Literal["entry", "stop_loss", "take_profit"]]]


class GpErrorResponse(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.error.response.v1"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    item: NotRequired[GpV1]
    details: NotRequired[GpErrorDetails]


class GpGetRequest(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.get.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class GpGetResponse(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.get.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: GpV1


class GpListRequest(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.list.request.v1"]
    request_id: AfbwsCommonV1RequestId
    ticker: NotRequired[str]


class GpListResponse(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.list.response.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[GpV1]


class GpSetRequest(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.set.request.v1"]
    request_id: AfbwsCommonV1RequestId
    item: GpV1


class GpSetResponse(TypedDict):
    channel: Literal["gp"]
    schema: Literal["afbws.gp.set.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: GpV1


GpChannelV1Message: TypeAlias = (
    GpGetRequest
    | GpGetResponse
    | GpListRequest
    | GpListResponse
    | GpSetRequest
    | GpSetResponse
    | GpDeleteRequest
    | GpDeleteResponse
    | AfbwsGpChannelV1SyncPush
    | GpErrorResponse
)


class GpV1(TypedDict):
    """
    AFB-side chart primitive (line/line_enter/line_sl/line_tp/note/zone/ruler) — like afb.alarm.v1, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel. Promotes the parked settings.primitives[secid][] draft (draft/primitive.v1.json) into a strict canonical entity: `ticker` becomes an explicit required field instead of an implicit dict key, so get(id)/list(ticker) work on a flat collection. Whether a primitive is REFERENCED BY a tradeplan's condition is still derived fresh from the tradeplans themselves on every read, never persisted here. OWNERSHIP is different and is persisted — see `tradeplan_id`. `stop` is a second anchor point required only for zone/ruler (forbidden for every other kind, enforced by the `allOf` below, not just by convention); `text` is accepted only for `note` (optional even there).
    """

    schema: Literal["afb.gp.v1"]
    id: str
    ticker: str
    kind: Literal["line", "line_enter", "line_sl", "line_tp", "note", "zone", "ruler"]
    start: GpV1Point
    stop: NotRequired[GpV1Point]
    text: NotRequired[str]
    tradeplan_id: NotRequired[str]


class GpV1Point(TypedDict):
    time: int
    price: float


class GpV2(TypedDict):
    """
    v2 of afb.gp.v1 with differences: (1) the instrument is identified by the full composite `instrument_key` (afbws/common.v1.json#/$defs/instrumentKey) instead of the short `ticker`; (2) new kinds `trendline` and `fibonacci` — both two-anchor primitives; their rendering is not specified yet; (3) the primitive's own parameters (`start`, `stop`, `text`) live in the `settings` dictionary, not at the root, so a kind can gain parameters without touching the envelope. ROOT = identity and server-side ownership: `schema`, `id`, `instrument_key`, `kind`, `tradeplan_id` (all other parameters go to `settings`). `settings` is REQUIRED and strictly typed by `kind` (enforced by the `allOf` below, each branch is additionalProperties:false): line/line_enter/line_sl/line_tp → `primitiveSettingsLine` {start}; note → `primitiveSettingsNote` {start, text? (≤160)}; zone/ruler/trendline/fibonacci → `primitiveSettingsTwoPoint` {start, stop}. v1 (`afb.gp.v1`, flat start/stop/text) stays supported for frontends without afbws.gp.channel.v2; v1 clients never receive trendline/fibonacci. Promotes the parked settings.primitives[secid][] draft (draft/primitive.v1.json) into a strict canonical entity. Whether a primitive is REFERENCED BY a tradeplan's condition is still derived fresh from the tradeplans themselves on every read, never persisted here. OWNERSHIP is different and is persisted — see `tradeplan_id`.
    """

    schema: Literal["afb.gp.v2"]
    id: str
    instrument_key: AfbwsCommonV1InstrumentKey
    kind: Literal[
        "line",
        "line_enter",
        "line_sl",
        "line_tp",
        "note",
        "zone",
        "ruler",
        "trendline",
        "fibonacci",
    ]
    settings: (
        GpV2PrimitiveSettingsLine
        | GpV2PrimitiveSettingsNote
        | GpV2PrimitiveSettingsTwoPoint
    )
    tradeplan_id: NotRequired[str]


class GpV2Delete(TypedDict):
    """
    Request (`request_id` present): `ids[]` and/or `instrument_keys[]` (at least one; `instrument_keys` = every FREE primitive of those instruments in one call). Primitives owned by a tradeplan (`tradeplan_id`) are never removed here — they come back in `rejected[]` with `code: conflict` and `details` (linked plans/deals). Response (same `request_id`): `ids[]` = ids actually removed (possibly empty), `rejected[]`. Push (no `request_id`): `ids[]` removed by the server; `instrument_keys`/`rejected` are not allowed.
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.delete.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    ids: NotRequired[list[Id]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]
    rejected: NotRequired[list[GpV2Rejection]]


class GpV2Error(TypedDict):
    """
    Used when the request as a whole fails (invalid_schema, forbidden channel, internal_error, ...). Per-item failures of a batched set/delete/indicator.* are reported in that response's `rejected[]`, not here. `details` is populated on `conflict`.
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.error.v2"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[GpV2ErrorDetails]


class GpV2ErrorDetails(TypedDict):
    tradeplan_ids: NotRequired[list[str]]
    deal_ids: NotRequired[list[str]]
    locked_scopes: NotRequired[list[Literal["entry", "stop_loss", "take_profit"]]]


class GpV2Indicator(TypedDict):
    """
    `scope: shared` indicators are common to all users and editable only by a manager; `personal` belong to the caller. `settings` carry the parameters. Whether an indicator is shown on the chart is not part of the protocol (per-device view setting kept in the client's localStorage). Type `cot` is chart-only; alarm indicator conditions support wma/kama/psar.
    """

    id: str
    type: Literal["wma", "kama", "psar", "cot"]
    settings: GpV2IndicatorSettings
    scope: Literal["shared", "personal"]


class GpV2IndicatorDelete(TypedDict):
    """
    Request: `ids[]` (shared ones: manager only, otherwise rejected with `forbidden`; unknown id: `not_found`). Response (same `request_id`): `ids[]` actually removed + `rejected[]`. Push (no `request_id`): shared indicators deleted by a manager (`ids[]`, `rejected` not allowed).
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.indicator.delete.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    ids: list[Id]
    rejected: NotRequired[list[GpV2IndicatorRejection]]


class GpV2IndicatorList(TypedDict):
    """
    Request: only `request_id`. Response (same `request_id`): `items[]` — the caller's merged list (shared + personal).
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.indicator.list.v2"]
    request_id: AfbwsCommonV1RequestId
    items: NotRequired[list[GpV2Indicator]]


class GpV2IndicatorRejection(TypedDict):
    id: str
    code: AfbwsCommonV1ErrorCode
    message: NotRequired[str]


class GpV2IndicatorSet(TypedDict):
    """
    Request: upsert by `id`, batched. Personal indicators for everyone; `scope: shared` only for a manager (otherwise that item is rejected with `forbidden`). Response (same `request_id`): applied `items[]` (possibly empty) + `rejected[]`. Push (no `request_id`): changed SHARED indicators to every connection with this capability (full authoritative records); personal ones are never pushed. Whether an indicator is drawn on the chart is NOT part of the protocol — it is a per-device view setting kept in the client's localStorage.
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.indicator.set.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    items: list[GpV2Indicator]
    rejected: NotRequired[list[GpV2IndicatorRejection]]


class GpV2IndicatorSettings(TypedDict):
    """
    Display + calculation settings. Common: color/lineWidth/lineStyle; period (wma, cot); erPeriod/fastPeriod/slowPeriod (kama); start/maximum/increment (psar). Mirrors IndicatorInstance.settings of the frontend chart and `indicators[].settings` of config/_default_.yaml, without the on/off flag.
    """

    color: str
    lineWidth: float
    lineStyle: Literal["Solid", "Dots"]
    period: NotRequired[int]
    erPeriod: NotRequired[int]
    fastPeriod: NotRequired[int]
    slowPeriod: NotRequired[int]
    start: NotRequired[float]
    maximum: NotRequired[float]
    increment: NotRequired[float]


class GpV2List(TypedDict):
    """
    Request: optional filters `ids[]` and/or `instrument_keys[]` (both given = intersection; none = every primitive the caller owns). Response: same `request_id`, `items[]` (afb.gp.v2) — possibly empty, never an error for a missing id. There is no separate `get`: use `ids`. `items` is response-only; a request carrying `items` together with a filter is invalid.
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.list.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: NotRequired[list[Id]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]
    items: NotRequired[list[GpV2]]


class GpV2Point(TypedDict):
    time: int
    price: float


class GpV2PrimitiveKindStyle(TypedDict):
    color: str
    lineWidth: Literal[1, 2, 3, 4]
    lineStyle: int


class GpV2PrimitiveSettingsLine(TypedDict):
    """
    line, line_enter, line_sl, line_tp.
    """

    start: GpV2Point


class GpV2PrimitiveSettingsNote(TypedDict):
    """
    note.
    """

    start: GpV2Point
    text: NotRequired[str]


class GpV2PrimitiveSettingsTwoPoint(TypedDict):
    """
    zone, ruler, trendline, fibonacci.
    """

    start: GpV2Point
    stop: GpV2Point


class GpV2PrimitiveStyles(TypedDict):
    """
    Keys are primitive kinds; a kind that is absent has no stored override (the client falls back to its defaults).
    """

    line: NotRequired[GpV2PrimitiveKindStyle]
    line_enter: NotRequired[GpV2PrimitiveKindStyle]
    line_sl: NotRequired[GpV2PrimitiveKindStyle]
    line_tp: NotRequired[GpV2PrimitiveKindStyle]
    note: NotRequired[GpV2PrimitiveKindStyle]
    zone: NotRequired[GpV2PrimitiveKindStyle]
    ruler: NotRequired[GpV2PrimitiveKindStyle]
    trendline: NotRequired[GpV2PrimitiveKindStyle]
    fibonacci: NotRequired[GpV2PrimitiveKindStyle]


class GpV2Rejection(TypedDict):
    """
    `item` carries the authoritative current record when the client should see it (a rejected move restores the server's version, not the client's optimistic one). `details` is populated on `conflict` (linked tradeplans/deals, locked scopes).
    """

    id: str
    code: AfbwsCommonV1ErrorCode
    message: NotRequired[str]
    item: NotRequired[GpV2]
    details: NotRequired[GpV2ErrorDetails]


class GpV2Set(TypedDict):
    """
    Request (`request_id` present, `items` = what the client wants stored): upsert by `item.id`, batched (each item carries `settings`; `settings` is replaced as a whole; a client-sent `tradeplan_id` is ignored in favour of the stored one); moving a primitive is the same request as creating or editing one. Response (same `request_id`): `items` = the authoritative stored records that were applied (possibly empty), `rejected[]` = items that were NOT applied, each with a typed reason (partial failure never fails the whole message; the backend alone decides whether a move is safe against linked tradeplans). Push (no `request_id`, server-initiated): ownership delta by id — `items[]` are authoritative afb.gp.v2 records (bind: `tradeplan_id` set on publish/amend; release: `tradeplan_id` cleared on plan physical delete); never a snapshot, `rejected` is not allowed. Primitive removal is conveyed by `afbws.gp.delete.v2` without `request_id`.
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.set.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    items: list[GpV2]
    rejected: NotRequired[list[GpV2Rejection]]


class GpV2Style(TypedDict):
    """
    Per-user chart styling of primitives by kind (replaces the legacy `settings.interface.primitive_styles`). Request without `styles` = read. Request with `styles` = write: the supplied kinds replace the stored ones, kinds not supplied are left as they are. Response (same `request_id`) always carries the full stored `styles`. Push (no `request_id`) delivers the full `styles` to the user's other connections after a write; `styles` is required there.
    """

    channel: Literal["gp"]
    schema: Literal["afbws.gp.style.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    styles: NotRequired[GpV2PrimitiveStyles]


GpChannelV2Message: TypeAlias = (
    GpV2List
    | GpV2Set
    | GpV2Delete
    | GpV2IndicatorList
    | GpV2IndicatorSet
    | GpV2IndicatorDelete
    | GpV2Style
    | GpV2Error
)


class Health(TypedDict):
    overall: NotRequired[Literal["ok", "warning", "critical"]]
    points: NotRequired[dict[str, Any]]


Id: TypeAlias = str


class Instrument(TypedDict):
    shortname: NotRequired[str]
    secname: NotRequired[str]


class Instrument2(TypedDict):
    broker_symbol: str
    exchange: NotRequired[str]
    board: NotRequired[str]
    ticker: NotRequired[str]
    name: NotRequired[str]
    market: NotRequired[str]


class InstrumentAcceptSuggestion(TypedDict):
    suggestion_id: str
    asset_id: str
    collection_id: NotRequired[str | None]


class InstrumentAssetMemberInput(TypedDict):
    """
    Same discriminator and identity as catalogAssetMember: `kind` plus exactly one key — `instrument_key` for `kind=listing`, `derivative` for `kind=derivative`. `code`/`label`/`market` are display-only and are never written; the server derives them from items/derivatives. A contract listed here whose derivative is also listed is rejected.
    """

    kind: Literal["listing", "derivative"]
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    derivative: NotRequired[str]


class InstrumentAssetSetView(TypedDict):
    """
    DEPRECATED: the legacy view behind `asset_sets[]`, superseded by `setView`/`sets[]`; it is removed once every frontend reads `sets[]`. `asset_sets[]` carries only the sets of type `asset` (a set of instruments is never listed here, so an old frontend does not see it). True asset set (Наборы): metadata plus ordered `asset_ids`. The set's own display position is its position in `asset_sets[]` (and in `userState.sets[]` for a personal set) — there is no order field on the wire; a commit restates that order wholesale through `commitRequest.asset_set_order`. For scope=global, `visibility_tier` is required; for scope=user, `visibility_tier` is forbidden and `owner_user_id` is required.
    """

    set_id: str
    scope: Literal["global", "user"]
    name: str
    owner_user_id: NotRequired[str | None]
    asset_ids: list[str]
    visibility_tier: NotRequired[Literal["manager", "user", "guest"]]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV1FavoriteColor | None]


class InstrumentAssetSuggestion(TypedDict):
    suggestion_id: str
    subject_type: Literal["listing", "series"]
    subject_ref: str
    reason: str
    status: Literal["pending", "accepted", "rejected", "stale"]
    proposed_name: NotRequired[str]
    proposed_collection_id: NotRequired[str | None]
    fingerprint: NotRequired[str]
    created_at: NotRequired[str]
    last_seen_at: NotRequired[str]
    resolved_asset_id: NotRequired[str]


class InstrumentAssetUpsert(TypedDict):
    """
    The client mints `asset_id` itself (same generateId style as deal/primitive ids; for a non-empty asset the first block is the bare code of its first `members[]` entry). Scalars otherwise behave as a patch — an omitted field keeps its stored value — while `members`, when present, is the WHOLE composition in its final order, exactly like membersEdit.order. Composition has no add/remove form on purpose: an asset holds a handful of members that a manager edits as one picture, and a full statement removes any question about what an absent element means. Omit `members` to leave the composition untouched; send `[]` to empty the asset without deleting it.
    """

    asset_id: str
    name: str
    members: NotRequired[list[InstrumentAssetMemberInput]]
    collection_id: NotRequired[str | None]


class InstrumentCatalogAsset(TypedDict):
    """
    An asset is a small bundle of instruments that share a pricing source and therefore tell one economic story: "Brent oil" is the BR-* and BRM-* series together, "Sberbank" is the share plus its futures series. Two jobs justify the level. It is the unit sets are built from, so a set survives expirations without being re-edited; and it is the carrier of reference data (MOEX positions, HHI), so analytics have one place to attach to instead of guessing which contract of which series to read. Assets are always global — the personal sets of phase 3 are assembled from the same manager-curated assets, which is what keeps that phase thin. An asset that is in no set is a normal state: it shows up as unassigned for a manager and is omitted from a user's catalog snapshot. Composition is nested as ordered `members` on the asset itself; array position is the order.
    """

    asset_id: str
    name: str
    members: list[InstrumentCatalogAssetMember]
    collection_id: NotRequired[str | None]


class InstrumentCatalogAssetMember(TypedDict):
    """
    Array position is the display order. The identity is `kind` plus exactly one key: `instrument_key` for `kind=listing` (join to `items[]`), `derivative` for `kind=derivative` (join to `derivatives[]` by `catalogDerivative.derivative`, and on to the contracts through the `items[].derivative` backreference). Both keys share the one `MIC:...` grammar. `code`, `label` and `market` are denormalized display only — the server forms them, the client just renders; none of the three is ever an identity or a join key. A derivative member is whole: for a serial future every expiration belongs to the asset. `kind=listing` is a single instrument: a stock, currency, or index. The server rejects a futures contract as a listing member of an asset that already contains its derivative. This `kind` (`listing`/`derivative`) is unrelated to `catalogDerivative.kind` (`perpetual`/`series`/`options`) and `poolEntry.kind` — independent namespaces.
    """

    kind: Literal["listing", "derivative"]
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    derivative: NotRequired[str]
    code: NotRequired[str]
    label: NotRequired[str]
    market: NotRequired[Literal["stock", "futures", "currency", "index", "options"]]


class InstrumentCatalogRequest(TypedDict):
    """
    The wire form is identical for a user and a manager; completeness (unassigned assets) is applied server-side from the caller's role — sets/assets no longer carry an archived flag, so the only completeness axis left is whether an asset belongs to any set. `catalog` is the Assets-modal snapshot and the only read of the curated catalog.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.catalog.request.v1"]
    request_id: AfbwsCommonV1RequestId


class InstrumentCatalogResponse(TypedDict):
    """
    Same form for every authenticated caller; the backend varies completeness (a manager sees unassigned assets too, a user sees only live sets and the assets that belong to them — sets/assets have no archived flag, so this is purely about assets that are in no set). Set membership is `sets[].asset_ids` / `sets[].instrument_keys` (by `set_type`) in display order; `asset_sets[]` is the deprecated legacy view of the asset-type sets. Composition is `assets[].members` (`kind` plus `instrument_key`/`derivative`, with `code`/`label`/`market` for display) in display order. Order is always array position — no entity on this wire carries an order field. `items` are the canonical instrument records (including materialized futures contracts); `derivatives` is the derivatives axis. `catalog_revision` is the CAS token to send back as commitRequest.base_revision. The `group` field inside `items[]` is a legacy leftover and must not be read as membership. Dangling levels are normal: an asset in no set stays in `assets` (manager) and is absent from every `sets[].asset_ids`.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.catalog.response.v1"]
    request_id: AfbwsCommonV1RequestId
    catalog_revision: int
    assets: list[InstrumentCatalogAsset]
    items: list[InstrumentV1]
    derivatives: NotRequired[list[AfbwsInstrumentChannelV1CatalogDerivative]]
    collections: NotRequired[list[InstrumentCollection]]
    sets: NotRequired[list[InstrumentSetView]]
    asset_sets: NotRequired[list[InstrumentAssetSetView]]
    suggestions: NotRequired[list[InstrumentAssetSuggestion]]
    user: NotRequired[InstrumentUserState]


class InstrumentCatalogSource(TypedDict):
    """
    The registry is assembled, not stored: the MOEX/ISS entry comes from the market-source configuration, broker entries from the connectors currently registered. An unavailable source is still listed — the point of the operation is to show WHY nothing is updating (ISS unreachable, connector offline) rather than to hide the row.
    """

    source_id: str
    kind: Literal["moex", "broker"]
    available: bool
    last_refresh_at: str | None
    listing_count: int
    inventory_count: NotRequired[int]
    last_error: NotRequired[str]
    inventory_revision: NotRequired[int]


class InstrumentCollection(TypedDict):
    """
    Order is carried by array position: `collections[]` already arrives in the order the tree is drawn in (the children of one `parent_id` follow one another), so there is no order field on the wire. A commit restates that order wholesale through `commitRequest.collection_order`.
    """

    collection_id: str
    parent_id: NotRequired[str | None]
    name: str
    pending: NotRequired[bool]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV1FavoriteColor | None]


class InstrumentCollectionMembersEdit(TypedDict):
    """
    An asset lives in at most ONE collection, so `add` here also states membership: an asset added to a collection leaves the one it was in. Assets that fall out of a collection without being added to another end up with no collection (`collection_id: null`) — a legal, normal state, same as an instrument with no asset. `order`, when present, must list the collection's full membership after add/remove.
    """

    collection_id: str
    add: NotRequired[list[str]]
    remove: NotRequired[list[str]]
    order: NotRequired[list[str]]


class InstrumentCollectionUpsert(TypedDict):
    """
    Identity and naming only — position is not stated here; send `commitRequest.collection_order` to fix the order of the tree.
    """

    collection_id: str
    parent_id: NotRequired[str | None]
    name: str
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV1FavoriteColor | None]


class InstrumentCommitRequest(TypedDict):
    """
    Compare-and-set: if the server's current catalog revision differs from `base_revision` the whole commit is rejected with `conflict` and errorResponse.details.catalog_revision carries the current one — the client re-fetches `catalog`, re-applies its edits and retries. Every section is optional; an empty commit is legal (and is a cheap way to read the current revision back). All sections are applied in one transaction, in this order: `modify_sets`, `remove_sets`, `assets`, `remove_assets`, `set_members`, `listings`/`archive_listings`, `series`, `collections`, `remove_collections`, `collection_members`. The server plans the whole delta before applying, so a listing or series upserted in this same request may be referenced from `assets[].members` even though those sections are written later — that is how a pending pool entry and the asset composition that contains it travel atomically. A set created here can be filled by `set_members` in the same request — with assets or, for a set of type `instrument`, with instruments (a listing upserted in this same request may be named by its `instrument_key`) — and an asset created here can be put into a set of type `asset`, because both exist by the time `set_members` runs — `set_members`/other same-commit references use the same client-minted `set_id`/`asset_id` the `setUpsert`/`assetUpsert` entry carries. Order is never a field on an entity: `set_order`, `collection_order`, and the `order` of `set_members`/`collection_members` each state a FULL final order, and every read snapshot carries order as array position. `set_id` and `asset_id` are always client-minted opaque ids (setUpsert/assetUpsert), never generated by the server (setUpsert/assetUpsert): a `set_id`/`asset_id` absent from the base snapshot is an INSERT, one already present is an UPDATE, and the server never rewrites an id it is given.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.commit.request.v1"]
    request_id: AfbwsCommonV1RequestId
    base_revision: int
    assets: NotRequired[list[InstrumentAssetUpsert]]
    remove_assets: NotRequired[list[str]]
    listings: NotRequired[list[InstrumentV1]]
    archive_listings: NotRequired[list[InstrumentListingArchival]]
    series: NotRequired[list[InstrumentSeriesUpsert]]
    collections: NotRequired[list[InstrumentCollectionUpsert]]
    remove_collections: NotRequired[list[str]]
    collection_order: NotRequired[list[str]]
    collection_members: NotRequired[list[InstrumentCollectionMembersEdit]]
    modify_sets: NotRequired[list[InstrumentSetUpsert]]
    remove_sets: NotRequired[list[str]]
    set_members: NotRequired[list[InstrumentMembersEdit]]
    set_order: NotRequired[list[str]]
    asset_sets: NotRequired[list[InstrumentSetUpsert]]
    remove_asset_sets: NotRequired[list[str]]
    asset_set_members: NotRequired[list[InstrumentMembersEdit]]
    asset_set_order: NotRequired[list[str]]
    accept_suggestions: NotRequired[list[InstrumentAcceptSuggestion]]
    reject_suggestions: NotRequired[list[str]]
    reason: NotRequired[str]


class InstrumentCommitResponse(TypedDict):
    """
    `catalog_revision` is already the new one. A rejected commit is an errorResponse instead — there is no partially-applied outcome.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.commit.response.v1"]
    request_id: AfbwsCommonV1RequestId
    catalog_revision: int
    assets: list[InstrumentCatalogAsset]
    items: list[InstrumentV1]
    derivatives: NotRequired[list[AfbwsInstrumentChannelV1CatalogDerivative]]
    collections: NotRequired[list[InstrumentCollection]]
    sets: NotRequired[list[InstrumentSetView]]
    asset_sets: NotRequired[list[InstrumentAssetSetView]]
    suggestions: NotRequired[list[InstrumentAssetSuggestion]]
    applied: NotRequired[dict[str, int]]
    user: NotRequired[InstrumentUserState]


class InstrumentDetailRequest(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.detail.request.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: str
    ticker: str


class InstrumentDetailResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.detail.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: InstrumentV1
    binding: dict[str, Any]
    broker_instrument: dict[str, Any]


class InstrumentErrorDetails(TypedDict):
    """
    Populated on `conflict` (stale base_revision: `catalog_revision` for commit, `user_revision` for user — re-fetch, re-apply, retry) and on `validation_error` (`set_ids`/`asset_ids`/`tickers`/`instrument_keys` name the offending rows — one list per level, since a rejected edit can be about a set, an asset or a listing; `limit` is populated instead when the rejection is a tier-limit overflow). Absent for errors that carry no such context.
    """

    catalog_revision: NotRequired[int]
    user_revision: NotRequired[int]
    set_ids: NotRequired[list[str]]
    asset_ids: NotRequired[list[str]]
    tickers: NotRequired[list[str]]
    collection_ids: NotRequired[list[str]]
    suggestion_ids: NotRequired[list[str]]
    instrument_keys: NotRequired[list[str]]
    limit: NotRequired[Limit]


class InstrumentErrorResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.error.response.v1"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[InstrumentErrorDetails]


class InstrumentGetRequest(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.get.request.v1"]
    request_id: AfbwsCommonV1RequestId
    ticker: str


class InstrumentGetResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.get.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: InstrumentV1


class InstrumentInventoryListingEntry(TypedDict):
    kind: Literal["listing"]
    instrument_type: Literal["stock", "currency", "index", "futures", "option"]
    instrument_key: AfbwsCommonV1InstrumentKey
    ticker: str
    exchange: str
    board: str
    market: Literal["stock", "futures", "currency", "index"]
    source: str
    name: NotRequired[str | None]
    shortname: NotRequired[str | None]
    lifecycle: NotRequired[str]
    series_code: NotRequired[str]


class InstrumentInventoryRequest(TypedDict):
    """
    Filterable, paged browse of the complete MOEX (or other source) instrument universe — distinct from the curated `pool` candidate list. `limit` defaults to 50, capped at 200.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.inventory.request.v1"]
    request_id: AfbwsCommonV1RequestId
    source: NotRequired[str]
    market: NotRequired[Literal["stock", "futures", "currency", "index"]]
    board: NotRequired[str]
    instrument_type: NotRequired[
        Literal["stock", "currency", "index", "futures", "option", "series"]
    ]
    query: NotRequired[str]
    limit: NotRequired[int]
    cursor: NotRequired[str]


class InstrumentInventoryResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.inventory.response.v1"]
    request_id: AfbwsCommonV1RequestId
    total: int
    next_cursor: str | None
    inventory_revision: int
    entries: list[InstrumentInventoryEntry]
    source: NotRequired[str]
    fetched_at: NotRequired[str]


class InstrumentInventorySeriesEntry(TypedDict):
    kind: Literal["series"]
    instrument_type: Literal["series"]
    series_code: str
    source: str
    market: Literal["futures"]
    name: NotRequired[str | None]
    underlying: NotRequired[str | None]


InstrumentInventoryEntry: TypeAlias = (
    InstrumentInventoryListingEntry | InstrumentInventorySeriesEntry
)


class InstrumentListingArchival(TypedDict):
    ticker: str
    reason: NotRequired[str]


class InstrumentMembersEdit(TypedDict):
    """
    Members are named by the set's own type: `asset_id` for a set of type `asset`, `instrument_key` for a set of type `instrument`; a value of the other kind is rejected with `validation_error`. Without `order`, every newly added member goes to the END of the set, in the order listed in `add`; the members already there keep their relative order.
    """

    set_id: str
    add: NotRequired[list[str]]
    remove: NotRequired[list[str]]
    order: NotRequired[list[str]]


class InstrumentPoolListingEntry(TypedDict):
    """
    Wraps the canonical listing so a pending draft copies `listing` into commitRequest.listings unchanged (send `group: null`). Futures do not appear here — they are poolSeriesEntry rows. `listing.market` must not be `futures`.
    """

    kind: Literal["listing"]
    listing: InstrumentV1


class InstrumentPoolRequest(TypedDict):
    """
    Source is MOEX-only in this revision: omit `source` or send "moex". A bf_id is invalid — broker pool is not served. `kind` selects listing vs series rows; `market` filters by class. `kind=listing` cannot be paired with `market=futures` (futures are series rows); `kind=series` cannot be paired with a non-futures market. `limit` defaults to 50 and is capped at 200. `cursor` is an opaque token bound to the same `query`/`kind`/`market` filter tuple and to the pool snapshot that produced it (see `fetched_at`); a mismatched or stale cursor is `validation_error` or `conflict`, not a silent restart at the first page.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.pool.request.v1"]
    request_id: AfbwsCommonV1RequestId
    source: NotRequired[Literal["moex"]]
    query: NotRequired[str]
    kind: NotRequired[Literal["listing", "series"]]
    market: NotRequired[Literal["stock", "futures", "currency", "index"]]
    limit: NotRequired[int]
    cursor: NotRequired[str]


class InstrumentPoolResponse(TypedDict):
    """
    Replaces the former meta/slice pair. `entries` is a mixed listing|series page. `total` is the match count AFTER `query`/`kind`/`market` filters and BEFORE paging (`entries.length` ≤ `limit`, never a substitute for `total`). `next_cursor` is bound to the same filter tuple and to the snapshot identified by `fetched_at`; null means this page is the last. `fetched_at` is when the backend snapshot was taken, not when this page was built.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.pool.response.v1"]
    request_id: AfbwsCommonV1RequestId
    source: Literal["moex"]
    fetched_at: str
    total: int
    next_cursor: str | None
    entries: list[InstrumentPoolEntry]


class InstrumentPoolSeriesEntry(TypedDict):
    """
    Maps to seriesUpsert on commit: `code` → `series_code`, `underlying` → `underlying_ticker`. The backend materializes active contracts from the MOEX snapshot in the same commit that upserts the series.
    """

    kind: Literal["series"]
    code: str
    derivative: NotRequired[str]
    name: str | None
    source: Literal["moex"]
    market: Literal["futures"]
    underlying: NotRequired[str | None]


InstrumentPoolEntry: TypeAlias = InstrumentPoolListingEntry | InstrumentPoolSeriesEntry


class InstrumentRefreshArchivedEntry(TypedDict):
    """
    Archival is the part of a refresh that a manager cannot undo by re-running it, so the reason travels with the key instead of being left in the server log.
    """

    key: str
    reason: str


class InstrumentRefreshReport(TypedDict):
    """
    Lists rather than counts, because the interesting cases are individually reviewable: which contracts got archived, which rows the source offered that the catalog does not carry. Every element is a catalog instrument key in its composite form (`MIC:BOARD:TICKER`) — the wire `ticker` of instrument.v1 collapses to the bare local symbol for MOEX and could not tell two boards apart, and a report is precisely where that ambiguity is unacceptable. `new_series` holds series_codes instead. The three trailing lists are diagnostics, not changes: they say what the refresh deliberately did NOT do.
    """

    applied: bool
    revision_before: int
    revision_after: int
    added: list[str]
    updated: list[str]
    resurrected: list[str]
    archived: list[InstrumentRefreshArchivedEntry]
    new_series: list[str]
    absent_from_catalog: list[str]
    rows_without_series: list[str]
    changes: NotRequired[dict[str, int]]
    suggestion_ids: NotRequired[list[str]]
    inventory_revision_before: NotRequired[int]
    inventory_revision_after: NotRequired[int]
    markets: NotRequired[list[AfbwsInstrumentChannelV1RefreshMarketReport]]


class InstrumentRefreshRequest(TypedDict):
    """
    `dry_run` exists because the planning step is already separate from the write: a preview runs the very same planner and returns the very same report, it just never commits. That is the only difference between the two modes — a manager can always look before archiving a few dozen expired contracts.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.refresh.request.v1"]
    request_id: AfbwsCommonV1RequestId
    source_id: str
    dry_run: NotRequired[bool]


class InstrumentRefreshResponse(TypedDict):
    """
    A refresh that could not run at all (unknown or offline source, stale catalog under a concurrent commit) is an errorResponse instead — a report always describes a plan that was built successfully.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.refresh.response.v1"]
    request_id: AfbwsCommonV1RequestId
    source_id: str
    dry_run: bool
    report: InstrumentRefreshReport


class InstrumentResolveRequest(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.resolve.request.v1"]
    request_id: AfbwsCommonV1RequestId
    bf_id: str
    tradeplan_id: NotRequired[str]
    draft: NotRequired[dict[str, Any]]


class InstrumentResolveResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.resolve.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: InstrumentV1
    binding: dict[str, Any]
    broker_instrument: dict[str, Any]


class InstrumentSeriesUpsert(TypedDict):
    """
    Write form for a pool series row: copy `code` → `series_code`, `name` → `name`, `underlying` → `underlying_ticker`. The write form carries no order — a serial future's expirations are materialized by the backend.
    """

    series_code: str
    name: NotRequired[str | None]
    underlying_ticker: NotRequired[str | None]


InstrumentSetType: TypeAlias = Literal["asset", "instrument"]


class InstrumentSetUpsert(TypedDict):
    """
    Server derives scope/owner — client sends set_id, name, the optional `set_type` and an optional visibility_tier (default on server: user). Position is not stated here; send `set_order` to fix the order of the sets. `set_type` is decided when the set is created: omitted on create means `asset` (what a frontend that predates typed sets creates); on update it may be omitted, and a value that differs from the stored type is rejected with `validation_error`.
    """

    set_id: str
    name: str
    set_type: NotRequired[InstrumentSetType]
    visibility_tier: NotRequired[Literal["manager", "user", "guest"]]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV1FavoriteColor | None]


class InstrumentSetView(TypedDict):
    """
    True set (Наборы): metadata plus its ordered members. `set_type` says what the members are and is fixed when the set is created: `asset` — the members are `asset_ids`; `instrument` — the members are `instrument_keys` (single listings, never derivatives). Exactly the member list of the set's own type is present; the other one is forbidden. The set's own display position is its position in `sets[]` (and in `userState.sets[]` for a personal set) — there is no order field on the wire; a commit restates that order wholesale through `commitRequest.set_order`. For scope=global, `visibility_tier` is required; for scope=user, `visibility_tier` is forbidden and `owner_user_id` is required.
    """

    set_id: str
    scope: Literal["global", "user"]
    name: str
    owner_user_id: NotRequired[str | None]
    set_type: InstrumentSetType
    asset_ids: NotRequired[list[str]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]
    visibility_tier: NotRequired[Literal["manager", "user", "guest"]]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV1FavoriteColor | None]


class InstrumentSourcesRequest(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.sources.request.v1"]
    request_id: AfbwsCommonV1RequestId


class InstrumentSourcesResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.sources.response.v1"]
    request_id: AfbwsCommonV1RequestId
    sources: list[InstrumentCatalogSource]


class InstrumentUserRequest(TypedDict):
    """
    `base_revision` here is the revision of the PERSONAL aggregate (userState.revision), not the global catalog_revision — personal edits never conflict with a manager's commit. Sets created through this operation are implicitly scope: "user" and owned by the caller; a `set_id` naming a global set is rejected. An empty request is legal and just reads the current personal state back.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.user.request.v1"]
    request_id: AfbwsCommonV1RequestId
    base_revision: int
    modify_sets: NotRequired[list[InstrumentSetUpsert]]
    remove_sets: NotRequired[list[str]]
    set_members: NotRequired[list[InstrumentMembersEdit]]
    set_order: NotRequired[list[str]]
    asset_sets: NotRequired[list[InstrumentSetUpsert]]
    remove_asset_sets: NotRequired[list[str]]
    asset_set_members: NotRequired[list[InstrumentMembersEdit]]
    asset_set_order: NotRequired[list[str]]


class InstrumentUserResponse(TypedDict):
    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.user.response.v1"]
    request_id: AfbwsCommonV1RequestId
    user_revision: int
    user: InstrumentUserState


InstrumentChannelV1Message: TypeAlias = (
    InstrumentGetRequest
    | InstrumentGetResponse
    | InstrumentPoolRequest
    | InstrumentPoolResponse
    | InstrumentResolveRequest
    | InstrumentResolveResponse
    | InstrumentDetailRequest
    | InstrumentDetailResponse
    | InstrumentCatalogRequest
    | InstrumentCatalogResponse
    | InstrumentCommitRequest
    | InstrumentCommitResponse
    | InstrumentUserRequest
    | InstrumentUserResponse
    | AfbwsInstrumentChannelV1FavoritesRequest
    | AfbwsInstrumentChannelV1FavoritesResponse
    | AfbwsInstrumentChannelV1PaintRequest
    | AfbwsInstrumentChannelV1PaintResponse
    | InstrumentSourcesRequest
    | InstrumentSourcesResponse
    | InstrumentRefreshRequest
    | InstrumentRefreshResponse
    | InstrumentInventoryRequest
    | InstrumentInventoryResponse
    | AfbwsInstrumentChannelV1ExpirationListRequest
    | AfbwsInstrumentChannelV1ExpirationListResponse
    | AfbwsInstrumentChannelV1ExpirationPush
    | AfbwsInstrumentChannelV1ReplaceRequest
    | AfbwsInstrumentChannelV1ReplaceResponse
    | InstrumentErrorResponse
)


class InstrumentUserState(TypedDict):
    """
    The caller's personal overlay, served next to the global catalog. `sets[]` are full setView objects — every entry has scope "user" and carries its own membership inline (ordered `asset_ids` or `instrument_keys`, by `set_type`); there is no parallel membership array. `asset_sets[]` is the deprecated legacy view of the asset-type subset. Set order is the order of this array. Personal sets are assembled from the same global assets a manager curates: a user never owns an asset of their own.
    """

    revision: int
    sets: NotRequired[list[InstrumentSetView]]
    asset_sets: list[InstrumentAssetSetView]


class InstrumentV1(TypedDict):
    """
    AFB-side canonical instrument — like afb.gp.v1/afb.alarm.v1, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel. One broker-agnostic shape for every market class (stock/futures/currency/index); class-specific fields are gated by `market` via the `allOf`/`if` blocks below (forbidden, not just absent, for classes they don't apply to), but the wire type stays a single schema. `ticker` is the canonical identity: bare SECID for MOEX (e.g. "SBER"), `EXCHANGE:TICKER` for everything else (e.g. "XNAS:AAPL") — `exchange`/`board`/`market` are still carried as explicit fields so nothing but one shared parser (AFB backend/instruments/identity.py, frontend utils/instrumentId.ts) ever splits the string. `group`/`asset` place the instrument in the curated catalog tree (config/instruments.yaml) that AFB users actually see — `group: null` means not yet distributed into a group, the flat-list replacement for the old `lost` bucket. `source` says who refreshes this record's trading params ("moex" for the daily ISS refresh, a broker id like "finam" for instruments obtained from that broker's catalog) — it is NOT a broker binding: which connector can actually trade this instrument, and under what broker-native symbol, is resolved at publish time (see deal.v1.json's target.instrument + BF's own catalog), never persisted here.
    """

    schema: Literal["afb.instrument.v1"]
    ticker: str
    instrument_key: NotRequired[str]
    exchange: str
    board: str
    market: Literal["stock", "futures", "currency", "index", "options"]
    name: NotRequired[str | None]
    shortname: NotRequired[str | None]
    asset: NotRequired[str | None]
    group: NotRequired[str | None]
    lot_size: NotRequired[int | None]
    price_step: NotRequired[DecimalString]
    decimals: NotRequired[int | None]
    currency: NotRequired[str | None]
    prev_close: NotRequired[DecimalString]
    expiration: NotRequired[str]
    step_price: NotRequired[DecimalString]
    margin: NotRequired[DecimalString]
    futoi_code: NotRequired[str]
    derivative: NotRequired[str]
    isin: NotRequired[str]
    source: str


class Instruments(TypedDict):
    markets: NotRequired[list[str]]


IssIssColumnsV1Root: TypeAlias = Any


class IssMarketsCurrencyRoot(TypedDict):
    securities: Securities


class IssMarketsFuturesRoot(TypedDict):
    securities: Securities


class IssMarketsFuturesSeriesRoot(TypedDict):
    """
    The actual series channel — asset_code groups contracts (e.g. RTS-9.26/RTS-12.26 -> RTS), name and underlying_asset are what plan_refresh writes onto futures_series.name/underlying_key instead of leaving them null. underlying_asset is legitimately blank for part of the universe (e.g. commodity futures with no single spot underlying); series_refresh.py must not treat that as a parse failure.
    """

    series: Series


class IssMarketsIndexRoot(TypedDict):
    """
    The only market with more than one enabled board today: IMOEX/IMOEX2/RGBI trade on SNDX, RTSI on RTSI. A listing born from this market therefore carries no single board, and its catalog key omits the venue block entirely (MISX:<ticker>, not MISX:<board>:<ticker>) — see catalog_model.Listing.key and the v9->v10 migration notes in catalog_schema.py.
    """

    securities: Securities


class IssMarketsOptionsRoot(TypedDict):
    """
    Architecture only — disabled by default (config/market_source.yaml options.enabled=false). ISS returns ~37k rows / ~13MB for this market (one row per strike per expiration), which the daily refresh, the in-memory pool and the frontend cannot absorb without pagination and a strike filter; that is separate follow-up work. Written now so instrument_type='option' and the options_series channel have a real shape to target instead of a guess.
    """

    securities: Securities


class IssMarketsOptionsSeriesRoot(TypedDict):
    """
    Architecture only — disabled until options.json itself is enabled (see its own description). Mirrors futures_series.json's shape; ISS additionally carries strike-range and settlement fields here that the current parser has no target for.
    """

    series: Series


class IssMarketsStockRoot(TypedDict):
    securities: Securities


class Layouts(TypedDict):
    lg: NotRequired[list[ConfigV1DashboardLayoutItem]]


class Left(TypedDict):
    """
    afb.deal.v1 conditions compare against the last traded price, or (entry only — see executor-side validation) fire immediately with no price level of its own. quote/indicator/dataset sources are afb.deal.v2-only.
    """

    source: Literal["price", "immediate"]
    field: NotRequired[Literal["last"]]


class Limit(TypedDict):
    key: str
    allowed: int
    requested: int


class LimitsTemplate(TypedDict):
    """
    Response only.
    """

    keys: list[str]
    defaults: dict[str, int]


class LinkDeleteRequest(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.delete.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class LinkDeleteResponse(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.delete.response.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class LinkErrorResponse(TypedDict):
    """
    `code` is an open string, not an enum — at least not_found/forbidden/validation_error/conflict/bf_offline/not_paired/unsupported_action (see AFB/docs/ENTITY_WS_PROTOCOL.md) plus the generic invalid_schema/invalid_channel/internal_error every afbws error response can carry, but nothing here enforces that set at the schema level.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.error.response.v1"]
    request_id: AfbwsCommonV1RequestId
    code: str
    message: str
    details: NotRequired[dict[str, Any]]
    item: NotRequired[LinkEntity]


class LinkGetRequest(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.get.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class LinkGetResponse(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.get.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: LinkEntity


class LinkListRequest(TypedDict):
    """
    scope omitted or "usable": enabled connectors the caller may trade on (allowed_users ACL) plus virtual when permitted — never a manager bypass. scope "admin": full registry as admin views; managers only (backend rejects otherwise). Side-effect status.sync.push after list.response uses the same scope.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.list.request.v1"]
    request_id: AfbwsCommonV1RequestId
    scope: NotRequired[Literal["usable", "admin"]]


class LinkListResponse(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.list.response.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[LinkEntity]


class LinkPairRequest(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.pair.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class LinkPairResponse(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.pair.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: LinkEntity
    pairing_string: str
    expires_at: str


class LinkRestartRequest(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.restart.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class LinkRestartResponse(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.restart.response.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class LinkSession(TypedDict):
    account_id: str
    dry_run: bool | None
    capabilities: dict[str, Any]


class LinkSetInputShared(TypedDict):
    """
    Owner-editable connector fields plus bf_id. Admin setInput composes this with broker/ACL/margin extras.
    """

    bf_id: NotRequired[str]
    name: NotRequired[str]
    enabled: NotRequired[bool]
    description: NotRequired[str]
    dry_run: NotRequired[bool | None]
    execution_policy: NotRequired[ConnectorExecutionPolicy]


class LinkAdminSetInput(LinkSetInputShared):
    """
    Manager upsert: composes link.user.v1.json#/$defs/setInputShared with admin-only extras. `bf_id` omitted means create (backend assigns/validates id and requires broker + defaults); `bf_id` present and already registered means update. Backend enforces which combination is valid, not this schema.
    """

    broker: NotRequired[str]
    protocol: NotRequired[str]
    margin_trading: NotRequired[bool | None]
    allowed_users: NotRequired[list[str]]


class LinkSetRequest(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.set.request.v1"]
    request_id: AfbwsCommonV1RequestId
    item: LinkSetInput


class LinkSetResponse(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.set.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: LinkEntity


class LinkSharedFields(TypedDict):
    description: NotRequired[str]
    dry_run: bool | None
    margin_trading: bool | None
    execution_policy: ConnectorExecutionPolicy
    paired: bool
    pairing_pending: bool
    pairing_expires_at: str | None
    kind: Literal["connector", "virtual"]
    editable: bool


class LinkAdminV1(BfRegistryEntry, LinkSharedFields):
    """
    Manager view of a BF connector config record — reuses link.user.v1.json#/$defs/sharedFields (via $ref, not redeclared, so the two views can't drift apart) plus ACL/key management fields. Never carries `connected`/`daemon`/session runtime — see link.status.v1.json.
    """

    schema: Literal["afbws.link.admin.v1"]
    allowed_users: list[str]
    public_key_id: str | None
    public_key_file: str | None


class LinkStatusPush(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.status.push.v1"]
    item: LinkStatusV1


class LinkStatusSyncPush(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.status.sync.push.v1"]
    items: list[LinkStatusV1]


class LinkStatusV1(TypedDict):
    """
    Runtime-only BF status — never carries name/broker/ACL/keys/policy/config overrides, see link.user.v1.json/link.admin.v1.json for that. Sourced from BF register/unregister, daemon.capabilities, daemon.status and session.heartbeat handling in AFB — `updated_at` mirrors the triggering envelope's `created_at`. `daemon` is null until the first daemon.status after connect; `session` is null whenever `connected` is false (disconnect resets both). Heartbeat fields are AFB-derived display/runtime metadata, not part of the afb.execution.v1 wire itself.
    """

    schema: Literal["afbws.link.status.v1"]
    bf_id: str
    connected: bool
    updated_at: str
    last_heartbeat_at: NotRequired[str | None]
    heartbeat_interval_sec: NotRequired[int]
    heartbeat_stale: NotRequired[bool]
    daemon: DaemonStatusPayload | None
    session: LinkSession | None


class LinkSyncPush(TypedDict):
    channel: Literal["link"]
    schema: Literal["afbws.link.sync.push.v1"]
    items: list[LinkEntity]


LinkChannelV1Message: TypeAlias = (
    LinkGetRequest
    | LinkGetResponse
    | LinkListRequest
    | LinkListResponse
    | LinkSetRequest
    | LinkSetResponse
    | LinkDeleteRequest
    | LinkDeleteResponse
    | LinkPairRequest
    | LinkPairResponse
    | LinkRestartRequest
    | LinkRestartResponse
    | LinkErrorResponse
    | LinkSyncPush
    | LinkStatusSyncPush
    | LinkStatusPush
)


class LinkUserSetInput(LinkSetInputShared):
    """
    A non-manager caller may adjust name/enabled/description/dry_run/execution_policy on their own already-existing connector — never broker/protocol/allowed_*/margin_trading, and never create a new entry (bf_id must already exist and be owned by the caller; enforced by the backend, not this schema).
    """

    bf_id: str


LinkSetInput: TypeAlias = LinkUserSetInput | LinkAdminSetInput


class LinkUserV1(BfRegistryEntry, LinkSharedFields):
    """
    Caller-scoped BF connector config record for a non-manager viewer (owner: capability trade + user_id in allowed_users, or role-only access — role-only is read-only, enforced by the backend, not this schema). Never carries `connected`/`daemon`/session runtime — see link.status.v1.json for that, delivered on a separate push. The synthetic `virtual` pseudo-connector also uses this exact shape (kind:"virtual") — see link.channel.v1.json. `$defs/sharedFields` is the single source of the fields link.admin.v1.json reuses (via $ref) so the two views can't drift apart independently. `$defs/setInputShared` is the same for set() payloads.
    """

    schema: Literal["afbws.link.user.v1"]


LinkEntity: TypeAlias = LinkUserV1 | LinkAdminV1


class Market(TypedDict):
    exchange: NotRequired[str]
    market: NotRequired[str]


class MarketData(TypedDict):
    """
    What market data this BF instance can serve, and on which wire timeframes (see condition.v1.json#/$defs/timeframe) — used by AFB to validate indicator/price-candle condition timeframes before publish.
    """

    quotes: NotRequired[bool]
    candles: NotRequired[bool]
    orderbook: NotRequired[bool]
    timeframes: NotRequired[list[ConditionV1Timeframe]]


class MarketErrorResponse(TypedDict):
    """
    Two client-avalanche-protection codes (plan стабильности AFB, Этап 2), both replying to the superseded/rejected `get`'s own `request_id`, not a push: `superseded` — a live `get target=series` (see `$defs/get`) was cancelled because a newer live `get` on the same connection replaced it before it finished; the client should discard the pending request silently, its chart already moved on. `busy` — the connection's concurrent heavy-`get` limit (history+live `target=series`) was exceeded, or the server is under memory pressure; carries `retry_after_sec`, the client may retry once after that delay.
    """

    channel: Literal["market"]
    schema: Literal["afbws.market.error.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]
    retry_after_sec: NotRequired[float]


class MarketGet(TypedDict):
    """
    Reply is `series` (target=series) or `snapshot` (target=snapshot) with the same `request_id`, or `error`. For target=series, `get` doubles as the subscription request: a connection has at most one live series subscription (instrument_key, period, kinds), there is no separate subscribe message for it. If `end_date` is absent, or not earlier than "today" in the instrument's market `tz`, this request ALSO becomes that live subscription, replacing whatever the connection was previously subscribed to — the server then pushes `series` (mode:"merge") for it as new data arrives; the reply and subsequent pushes may also carry `future_times` (see `$defs/series`) — there is no separate calendar lookup. A target=series request with `end_date` strictly before today (history paging, e.g. scrolling a chart back) is a pure history fetch and leaves the live subscription untouched.
    """

    channel: Literal["market"]
    schema: Literal["afbws.market.get.v1"]
    request_id: AfbwsCommonV1RequestId
    target: Literal["series", "snapshot"]
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    period: NotRequired[MarketPeriod]
    kinds: NotRequired[list[str]]
    start_date: NotRequired[str]
    end_date: NotRequired[str]
    base: NotRequired[str]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]


MarketPeriod: TypeAlias = Literal[
    "1min", "5min", "10min", "15min", "30min", "1h", "2h", "4h", "1d"
]


class MarketSnapshot(TypedDict):
    """
    Reply to `get` (target=snapshot) when `request_id` is present; unsolicited push to the `quotes` or `futures` subscription scope when it is absent (see `scope`).
    """

    channel: Literal["market"]
    schema: Literal["afbws.market.snapshot.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    scope: Literal["quotes", "futures", "get"]
    tz: str
    received_at: str
    mode: Literal["full", "update"]
    tables: list[MarketSnapshotTable]


class MarketSubscribe(TypedDict):
    """
    The client states its whole desired subscription scope every time; the server does not diff against a previous `subscribe`. `quotes` is the favorites price-plaque scope: `instrument_keys` to track. `futures` opts into the futures screener scope: a full quote+oi+oi_daily snapshot of every futures instrument (no per-instrument list — it's all-or-nothing). Neither controls the series (candles/dataset) subscription — that one is driven entirely by `get` (target=series), see its description. An empty body — neither `quotes` nor `futures` present — unsubscribes from both. Reply is `subscription` with the same `request_id`, immediately followed by `snapshot` push(es) with `mode:"full"` for each accepted scope.
    """

    channel: Literal["market"]
    schema: Literal["afbws.market.subscribe.v1"]
    request_id: AfbwsCommonV1RequestId
    quotes: NotRequired[MarketSubscriptionQuotesSpec]
    futures: NotRequired[bool]


class MarketSubscription(TypedDict):
    """
    `quotes` is the accepted subset of what was requested (same shape as subscribe.v1's `quotes`; absent means the quotes scope is empty/unsubscribed). `futures` always reflects the accepted state (true/false), even when the request omitted it. `rejected` lists `quotes.instrument_keys` that could not be resolved/subscribed, with a reason code. Always followed by `snapshot` push(es) with `mode:"full"` for each accepted scope.
    """

    channel: Literal["market"]
    schema: Literal["afbws.market.subscription.v1"]
    request_id: AfbwsCommonV1RequestId
    quotes: NotRequired[MarketSubscriptionQuotesSpec]
    futures: bool
    rejected: list[MarketSubscriptionRejection]


class MarketSubscriptionQuotesSpec(TypedDict):
    instrument_keys: list[AfbwsCommonV1InstrumentKey]


class MarketSubscriptionRejection(TypedDict):
    instrument_key: AfbwsCommonV1InstrumentKey
    code: AfbwsCommonV1ErrorCode
    message: NotRequired[str]


class MarketTable(TypedDict):
    """
    `rows` are keyed by their first column: `time` (UTC unix seconds) for the series kinds (candles/positions/trades/hhi/orders), `instrument_key` for the snapshot kinds (quote/oi/oi_daily). Beyond that first column, `columns` may list any subset of the kind's allowed fields in any order — a client reads by column name, never by positional index — so the server can add a field later without a schema bump, as long as it stays inside the per-kind enum below. `rows` elements are `number | string | null`; a source value that is NaN is sent as `null`, never as the string "NaN" or JSON NaN. In a `series` message, non-candle dataset rows (positions/trades/hhi/orders) exist only at the timestamps of that same message's `candles` table — the server aligns them: `positions` is snapped to the bucket `[t, next candle)` and carries the candle's `t`; `trades`/`orders`/`hhi` require an exact `time` match. There are no rows outside trading hours (no forward-filled/stale values).
    """

    kind: Literal[
        "candles", "positions", "trades", "hhi", "orders", "quote", "oi", "oi_daily"
    ]
    columns: list[Column]
    rows: list[list[float | str | None]]


class MarketSeriesTable(MarketTable):
    kind: NotRequired[Literal["candles", "positions", "trades", "hhi", "orders"]]


MarketSeries = TypedDict(
    "MarketSeries",
    {
        "channel": Literal["market"],
        "schema": Literal["afbws.market.series.v1"],
        "request_id": NotRequired[AfbwsCommonV1RequestId],
        "instrument_key": AfbwsCommonV1InstrumentKey,
        "period": MarketPeriod,
        "tz": str,
        "received_at": str,
        "mode": Literal["replace", "merge"],
        "from": NotRequired[str],
        "to": NotRequired[str],
        "source": NotRequired[Literal["broker", "cache"]],
        "message": NotRequired[str],
        "future_times": NotRequired[list[int]],
        "data_status": NotRequired[AfbwsMarketChannelV1DataStatus],
        "tables": list[MarketSeriesTable],
    },
)


MarketChannelV1Message: TypeAlias = (
    MarketSubscribe
    | MarketSubscription
    | MarketGet
    | MarketSeries
    | MarketSnapshot
    | AfbwsMarketChannelV1SourceStatus
    | MarketErrorResponse
)


class MarketSnapshotTable(MarketTable):
    kind: NotRequired[Literal["quote", "oi", "oi_daily"]]


class Meta(TypedDict):
    brokers: list[str]


Model: TypeAlias = Any


class NextContract(TypedDict):
    """
    The default replacement proposal — the nearest ACTIVE contract of the same derivative expiring after this one. Absent when there is none.
    """

    instrument_key: str
    ticker: str
    expiration: str


class NotificationAlarmV1(TypedDict):
    """
    AFB-side MQTT notification payload published to <topic_base>/alarms/<user_id> when a user alarm triggers. Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time. `display` carries human-readable strings pre-rendered by AFB backend (mirrors frontend alarm cards).
    """

    schema: Literal["afb.notification.alarm.v1"]
    alarm_id: str
    ticker: str
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    instrument: NotRequired[Instrument]
    condition: AlarmV1AlarmConditionNode
    period: NotRequired[ConditionV1Timeframe]
    trigger_frequency: NotRequired[Literal["once", "every_candle", "daily"]]
    triggered_value: NotRequired[float | str]
    instrument_price: NotRequired[float]
    display: Display
    context: NotRequired[dict[str, Any]]
    user: User
    timestamp: NotRequired[str]


class NotificationDealV1(TypedDict):
    """
    AFB-side MQTT notification payload published to <topic_base>/deals/<user_id> for a deal lifecycle event the user opted into (Настройки → Торговля). Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time; `at` (when present) is the BF event-occurrence time carried through from the underlying order.*/position.*/deal.* payload. `display` carries human-readable strings pre-rendered by AFB backend, mirroring the alarm notification design.
    """

    schema: Literal["afb.notification.deal.v1"]
    event: Literal[
        "condition.triggered",
        "order.created",
        "order.filled",
        "order.partially_filled",
        "position.opened",
        "position.changed",
        "position.closed",
        "deal.report",
    ]
    category: Literal["trigger", "order_placed", "order_executed", "position", "close"]
    deal_id: str
    bf_id: NotRequired[str]
    ticker: NotRequired[str]
    instrument: NotRequired[Instrument]
    direction: NotRequired[Literal["long", "short"]]
    side: NotRequired[Literal["buy", "sell"]]
    price: NotRequired[float | str]
    quantity: NotRequired[int]
    filled_quantity: NotRequired[int]
    realized_pnl: NotRequired[float | str]
    currency: NotRequired[str]
    close_reason: NotRequired[str]
    at: NotRequired[str]
    display: Display1
    user: User
    timestamp: NotRequired[str]


class NotificationExpirationV1Root(TypedDict):
    """
    AFB-side MQTT notification payload published to <topic_base>/system/<user_id> when a futures contract the user works with (alarms, free primitives, personal-set memberships, favorites) is about to expire. Consumed by the AFB informer daemon (Telegram/email) exactly like alarm/deal/link/system notifications — informer never reads AFB settings, the recipient and channels come only from `user`. Sent at most once per (user, contract, `stage`). Not sent when the user's `interface.futures_days_to_expiration` is 0. NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time.
    """

    schema: Literal["afb.notification.expiration.v1"]
    notification_id: str
    instrument_key: str
    ticker: str
    shortname: NotRequired[str]
    expiration: str
    days_left: int
    stage: Literal["warn", "d1", "d0"]
    usage: Usage
    next_contract: NotRequired[NextContract]
    user: User
    timestamp: NotRequired[str]


class NotificationLinkV1(TypedDict):
    """
    AFB-side MQTT notification payload published to <topic_base>/links/<user_id> for a BF connectivity/runtime incident or recovery the user opted into. Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time; `at` is the AFB-observed transition time. `display` carries human-readable strings pre-rendered by AFB backend.
    """

    schema: Literal["afb.notification.link.v1"]
    notification_id: str
    event: Literal[
        "link.disconnected",
        "link.recovered",
        "broker.degraded",
        "broker.recovered",
        "daemon.suspended",
        "daemon.recovered",
    ]
    bf_id: str
    connected: bool
    daemon_state: str
    previous_state: NotRequired[str]
    broker_connected: bool
    severity: Literal["ok", "warning", "critical"]
    previous_severity: NotRequired[Literal["ok", "warning", "critical"]]
    reason: NotRequired[str]
    code: NotRequired[str]
    at: NotRequired[str]
    incident_started_at: NotRequired[str]
    health: NotRequired[dict[str, Any]]
    display: Display2
    user: User
    timestamp: NotRequired[str]


class NotificationSystemV1Root(TypedDict):
    """
    AFB-side MQTT notification payload published to <topic_base>/system/<user_id> for a backend stability event (source health, data freshness, resource watchdog, startup) that a manager opted into via `me.notify_system`. Consumed by the AFB informer daemon (Telegram/email) exactly like alarm/deal/link notifications — informer never reads AFB settings, the recipient and channels come only from `user`. NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time; `since` is the AFB-observed time the reported state began.
    """

    schema: Literal["afb.notification.system.v1"]
    notification_id: str
    kind: Literal["source_state", "stale_data", "resource", "startup"]
    source: str
    state: str
    prev_state: NotRequired[str]
    since: str
    severity: Literal["info", "warning", "critical"]
    detail: NotRequired[str]
    user: User
    timestamp: NotRequired[str]


class Operation(TypedDict):
    deal_id: str
    revision: int
    op: NotRequired[str]


class OrderCreatedPayload(TypedDict):
    at: NotRequired[str]
    deal_id: str
    order_id: str
    broker_order_id: NotRequired[str]
    price: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]
    quantity: NotRequired[int]
    role: str
    side: str
    status: str


class OrderFilledPayload(TypedDict):
    at: NotRequired[str]
    deal_id: str
    filled_quantity: NotRequired[int]
    leg_index: NotRequired[int]
    order_id: str
    price: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]
    quantity: NotRequired[int]
    role: str
    side: str
    status: str


class Owner(TypedDict):
    user_id: NotRequired[str]


class PayloadsBrokerAccountCashBalance(TypedDict):
    currency: str
    value: str


class PayloadsBrokerAccountPosition(TypedDict):
    quantity: int
    average_price: str
    current_price: NotRequired[str | None]
    unrealized_pnl: NotRequired[str | None]
    instrument: NotRequired[dict[str, Any]]
    broker_ref: NotRequired[dict[str, Any]]


class PayloadsBrokerAccountsAccount(TypedDict):
    account_id: str
    tradable: bool
    readonly: bool
    status: Literal["ok", "stale", "error"]
    equity: str | None
    cash: list[PayloadsBrokerAccountsCashBalance]
    positions: list[PayloadsBrokerAccountsPosition]


class PayloadsBrokerAccountsCashBalance(TypedDict):
    currency: str
    value: str


class PayloadsBrokerAccountsPosition(TypedDict):
    quantity: int
    average_price: str
    current_price: NotRequired[str | None]
    unrealized_pnl: NotRequired[str | None]
    instrument: NotRequired[dict[str, Any]]
    broker_ref: NotRequired[dict[str, Any]]


class PayloadsBrokerCatalogMeta(TypedDict):
    session_date: NotRequired[str | None]
    revision: NotRequired[int]
    broker: str
    exchanges: list[str]
    markets: list[Market]


class PayloadsBrokerCatalogSlice(TypedDict):
    session_date: NotRequired[str | None]
    revision: NotRequired[int]
    broker: str
    exchange: str
    market: str
    instruments: list[Instrument2]


BrokerCatalogPayload: TypeAlias = PayloadsBrokerCatalogMeta | PayloadsBrokerCatalogSlice


class PayloadsBrokerOrdersOrder(TypedDict):
    deal_id: str
    order_id: str
    side: str
    role: str
    status: str
    quantity: int
    filled_quantity: int
    leg_index: int
    limit_price: NotRequired[str | None]
    average_price: NotRequired[str | None]
    updated_at: NotRequired[str]
    error_code: NotRequired[str | None]
    error_message: NotRequired[str | None]


class Plans(TypedDict):
    statuses: NotRequired[list[str]]


class Position(TypedDict):
    symbol: NotRequired[str]
    quantity: NotRequired[int]
    average_price: NotRequired[str]
    updated_at: NotRequired[str]


class PositionOpenedPayload(TypedDict):
    at: NotRequired[str]
    average_price: NotRequired[str]
    deal_id: str
    quantity: NotRequired[int]
    realized_pnl: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    symbol: NotRequired[str]


class PresetTimeframes(TypedDict):
    positions: NotRequired[str]
    trades: NotRequired[str]
    hhi: NotRequired[str]
    orders: NotRequired[str]


class Publish(TypedDict):
    """
    Параметры публикации плана (используется ТОЛЬКО при публикации, не хранит связь с сделкой). bf_id — коннектор по умолчанию для UI; истина при публикации — bf_id из afbws.deal.publish.request.v1. account_id пусто/отсутствует — дефолтный (торговый) счёт коннектора, резолвится на лету (ExecutionService.resolve_plan_account).
    """

    bf_id: NotRequired[str]
    account_id: NotRequired[str]


class Right(TypedDict):
    const: DecimalString


class Risk(TypedDict):
    take_profit: NotRequired[DealV1ExitBlock]
    stop_loss: NotRequired[DealV1ExitBlock]


class Section(TypedDict):
    exchange: str
    section: Literal["stock", "futures", "currency"]
    days: list[Day]
    windows: list[Window]


class Securities(TypedDict):
    columns: list[str]
    data: list[Any]


class Series(TypedDict):
    columns: list[str]
    data: list[Any]


class SessionEnrollRequestPayload(TypedDict):
    bf_id: str
    client_nonce: str
    bf_public_key: str
    mac: str
    protocol: str


class SessionEnrollResponsePayload(TypedDict):
    bf_id: str
    server_nonce: str
    afb_public_key: str
    mac: str
    protocol: str
    bf_name: NotRequired[str]


class SessionHeartbeatPayload(TypedDict):
    bf_id: str
    broker_connected: NotRequired[bool]
    uptime_sec: NotRequired[int]
    health: NotRequired[Health]


class SessionHelloAckPayload(TypedDict):
    server_nonce: NotRequired[str]
    heartbeat_interval_sec: NotRequired[int]
    protocol: str
    accepted_protocol: NotRequired[str]
    dry_run: NotRequired[bool]
    dry_run_afb: NotRequired[bool]
    dry_run_bf: NotRequired[bool]
    margin_trading: NotRequired[bool]
    margin_trading_afb: NotRequired[bool]
    margin_trading_bf: NotRequired[bool]
    features: NotRequired[Features1]


class SessionHelloPayload(TypedDict):
    bf_id: str
    dry_run: NotRequired[bool]
    margin_trading: NotRequired[bool]
    heartbeat_interval_sec: NotRequired[int]
    nonce: str
    protocol: str
    version: NotRequired[str]


class SessionReenrollRequestPayload(TypedDict):
    bf_id: str
    reason: NotRequired[str]


class SessionResyncRequestPayload(TypedDict):
    deals: NotRequired[dict[str, Deals]]
    active_deal_ids: NotRequired[list[str]]
    deal_archived: NotRequired[dict[str, str]]
    deal_revisions: NotRequired[dict[str, int]]


class SessionResyncResponsePayload(TypedDict):
    deals: NotRequired[dict[str, Deals]]
    deal_revisions: NotRequired[dict[str, int]]
    deal_statuses: NotRequired[dict[str, str]]


class Subscription(TypedDict):
    dataset_id: Literal["positions", "orders", "hhi", "trades"]
    instrument: DealInstrument


class TradePlanV1(TypedDict):
    """
    AFB-side single-entry / single-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v1. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `schema` is optional: its absence means afb.tradeplan.v1 (compatibility with frontends older than the tradeplan schema itself).
    """

    id: str
    ticker: str
    status: NotRequired[Literal["draft", "published", "completed", "archived"]]
    direction: NotRequired[Literal["long", "short"]]
    schema: NotRequired[Literal["afb.tradeplan.v1"]]
    activated_at: NotRequired[str]
    closed_at: NotRequired[str]
    archived_at: NotRequired[str]
    instrument_missing: NotRequired[bool]
    entry_condition: TradeplanV1EntryCondition
    quantity_value: NotRequired[float | None]
    quantity_mode: NotRequired[
        Literal["lots", "margin", "balance_pct", "risk_currency", "risk_factor"]
    ]
    take_profit: NotRequired[TradeplanV1Condition | None]
    stop_loss: NotRequired[TradeplanV1Condition | None]
    publish: NotRequired[Publish]
    delivery_at: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


class TradePlanV2(TypedDict):
    """
    AFB-side multi-entry / multi-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v2. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `direction` (long/short) is the single source of truth for position bias, at plan level — entry legs do not carry a per-leg side (a list of entries with independent buy/sell sides has no defined execution semantics for one deal). Conditions are deal.v2-compatible nodes — price legs carry an explicit `op` (touch/above/below/breakout/breakdown/crossing), `op` omitted on a price leg means touch (accepted for back-compat with old plans); indicator legs may omit `op`, derived from direction/scope at compile time — with two extensions beyond condition.v1.json's plain vocabulary: (1) the `right` side of a condition may be a `primitiveRef` (`{"primitive_id": "..."}`), a reference to a chart line primitive that AFB resolves to a decimal `const` at compile time; (2) an entry leg's `left` may be `condition.v1.json#/$defs/immediateExpr` (`{"source": "immediate"}`) for a market entry — `right`/`op` are structural placeholders in that case, same convention as the compiled deal (see deal.v2.json's conditionNode, immediate branch of condition.v1.json#/$defs/conditionNode): dispatch on `left.source == "immediate"` alone, never read `right`/`op`. Meaningful only on entries — AFB/BF reject it on stop_loss/take_profit. The full left/right pairing matrix (price/quote const-only, indicator/dataset const-or-same-kind) is enforced after compilation by deal.v2.json and by BF, not here — this schema deliberately stays loose to accommodate primitiveRef and immediateExpr. Each leg additionally carries an optional `logic` (`split`/`and`/`or`, see deal.v2.json#/$defs/legJoin for the full grammar) joining it to the preceding leg; AFB carries the field through compilation unchanged onto the corresponding deal.v2 leg.
    """

    id: str
    ticker: str
    status: NotRequired[Literal["draft", "published", "completed", "archived"]]
    editor: NotRequired[Literal["simple", "advanced"]]
    direction: Literal["long", "short"]
    schema: Literal["afb.tradeplan.v2"]
    activated_at: NotRequired[str]
    closed_at: NotRequired[str]
    archived_at: NotRequired[str]
    instrument_missing: NotRequired[bool]
    entries: list[Entry1]
    stop_loss: NotRequired[TradeplanV2TpExitList]
    take_profit: NotRequired[TradeplanV2TpExitList]
    sizing: DealSizing
    publish: NotRequired[Publish]
    delivery_at: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


class TradeplanAmendResultItem(TypedDict):
    schema: Literal["afbws.tradeplan.amend_result.v1"]
    deal_id: str
    accepted: bool
    revision: NotRequired[str | int | None]
    status: NotRequired[str | None]
    message: NotRequired[str | None]
    code: NotRequired[str | None]


class TradeplanDeleteRequest(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.delete.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class TradeplanDeleteResponse(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.delete.response.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class TradeplanEntityV1(TradePlanV1):
    pass


TradeplanEntity: TypeAlias = TradeplanEntityV1 | TradePlanV2


class TradeplanErrorResponse(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.error.response.v1"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]
    item: NotRequired[TradeplanEntity]


class TradeplanGetRequest(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.get.request.v1"]
    request_id: AfbwsCommonV1RequestId
    id: str


class TradeplanGetResponse(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.get.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: TradeplanEntity


class TradeplanListRequest(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.list.request.v1"]
    request_id: AfbwsCommonV1RequestId
    ticker: NotRequired[str]


class TradeplanListResponse(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.list.response.v1"]
    request_id: AfbwsCommonV1RequestId
    items: list[TradeplanEntity]


class TradeplanSetRequest(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.set.request.v1"]
    request_id: AfbwsCommonV1RequestId
    item: TradeplanEntity


class TradeplanSetResponse(TypedDict):
    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.set.response.v1"]
    request_id: AfbwsCommonV1RequestId
    item: TradeplanEntity
    amend_results: list[TradeplanAmendResultItem]


class TradeplanSyncPush(TypedDict):
    """
    items[] is a DELTA, not a snapshot: the client upserts plans in its own list by matching id and leaves everything else untouched. May contain a single element. The authoritative full list comes only from afbws.tradeplan.list.request.v1. Plan deletion is NOT conveyed by this push.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.sync.push.v1"]
    items: list[TradeplanEntity]


TradeplanChannelV1Message: TypeAlias = (
    TradeplanGetRequest
    | TradeplanGetResponse
    | TradeplanListRequest
    | TradeplanListResponse
    | TradeplanSetRequest
    | TradeplanSetResponse
    | TradeplanDeleteRequest
    | TradeplanDeleteResponse
    | AfbwsTradeplanChannelV1ArchiveRequest
    | AfbwsTradeplanChannelV1ArchiveResponse
    | TradeplanErrorResponse
    | TradeplanSyncPush
)


class TradeplanV1MarketOrPriceCondition(TypedDict):
    condition_type: NotRequired[Literal["price"]]
    price_value: NotRequired[float | None]


class TradeplanV1PriceCondition(TypedDict):
    condition_type: NotRequired[Literal["price"]]
    price_value: float


class TradeplanV1PrimitiveCondition(TypedDict):
    condition_type: Literal["primitive"]
    primitive_id: str
    price_value: NotRequired[float | None]


TradeplanV1Condition: TypeAlias = (
    TradeplanV1PriceCondition | TradeplanV1PrimitiveCondition
)


TradeplanV1EntryCondition: TypeAlias = (
    TradeplanV1MarketOrPriceCondition | TradeplanV1PrimitiveCondition
)


TradeplanV2LegId: TypeAlias = str


class TradeplanV2PrimitiveRef(TypedDict):
    primitive_id: str


class TradeplanV2TpConditionNode(TypedDict):
    id: NotRequired[str]
    op: NotRequired[
        Literal[
            "touch",
            "above",
            "below",
            "crosses_above",
            "crosses_below",
            "crossing",
            "breakout",
            "breakdown",
        ]
    ]
    timeframe: NotRequired[ConditionV1Timeframe]
    left: (
        ConditionV1PriceExpr
        | ConditionV1IndicatorExpr
        | ConditionV1DatasetExpr
        | ConditionV1ImmediateExpr
    )
    right: (
        ConditionV1RightConst
        | ConditionV1IndicatorExpr
        | ConditionV1DatasetExpr
        | TradeplanV2PrimitiveRef
    )


class TradeplanV2TpExitListItem(TypedDict):
    leg_id: NotRequired[TradeplanV2LegId]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: TradeplanV2TpConditionNode


TradeplanV2TpExitList: TypeAlias = list[TradeplanV2TpExitListItem]


class Usage(TypedDict):
    alarms: int
    primitives: int
    sets: int
    favorites: int


class User(TypedDict):
    name: str
    telegram: str
    email: str
    notify_telegram: bool
    notify_email: bool


class Validation(TypedDict):
    account_id: NotRequired[str]
    side: str
    sizing_mode: NotRequired[str]
    sizing_value: NotRequired[str]
    symbol: NotRequired[str]
    quantity_lots: NotRequired[int]
    entry_price: NotRequired[str]
    required_cash: NotRequired[str]


class Widgets(TypedDict):
    bf_id: NotRequired[str]
    order_filter: NotRequired[str]
    deal_status_filters: NotRequired[list[str]]
    exchange: NotRequired[str]
    market: NotRequired[str]
    events_date: NotRequired[str]


class Window(TypedDict):
    board: NotRequired[str]
    secid: NotRequired[str]
    start: str
    end: str
    phase: str
    estimated: bool

