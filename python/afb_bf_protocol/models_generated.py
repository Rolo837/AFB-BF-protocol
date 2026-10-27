# DO NOT EDIT BY HAND — generated from spec/schemas/ (via
# spec/.generated/bundled-schema.json) by datamodel-codegen, invoked from
# tools/generate.py. Run `afb-bf-protocol-generate` to regenerate.
# source-hash: 96b3bbf0c27bb434c68ecb2dcc86aace70cc2c8211e1e4e7c9c26103e8c1fe0a

from __future__ import annotations

from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

AccountV2AccountId: TypeAlias = str


AccountV2BfId: TypeAlias = str


class AccountV2Error(TypedDict):
    channel: Literal["account"]
    schema: Literal["afbws.account.error.v2"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]


class AccountV2EventRecord(TypedDict):
    logged_at: str
    bf_id: AccountV2BfId
    deal_id: NotRequired[str | None]
    category: Literal["deal", "order", "position", "condition"]
    event: str
    data: NotRequired[dict[str, Any] | None]


class AccountV2Events(TypedDict):
    """
    Request (`request_id`, no `items`): `bf_id` required, `date` (YYYY-MM-DD market date) omitted = today (market_today()). Response (same `request_id`, with `items`): `bf_id`, `date`, `items[]`. There is NO server push for events: `request_id` is always required.
    """

    channel: Literal["account"]
    schema: Literal["afbws.account.events.v2"]
    request_id: AfbwsCommonV1RequestId
    bf_id: AccountV2BfId
    date: NotRequired[str]
    items: NotRequired[list[AccountV2EventRecord]]


class AccountV2List(TypedDict):
    """
    Request (`request_id`, no `items`): optional `bf_id` (only that connector's accounts; omitted = every account of every accessible connector), optional `account_id` (a single account; use together with `bf_id`; replaces v1 `get`), optional `force` (bypass the cached BfRuntimeState.accounts snapshot and re-fetch from BF). Response (same `request_id`, with `items`): only `request_id` + `items[]` (accountSnapshot, possibly empty). Push (no `request_id`, server-initiated): the full account list of ONE `bf_id` — `bf_id`, `default_account_id`, `items[]` (BF's broker.accounts is a full snapshot, never a delta; the virtual account is pushed the same way). A request carrying `items`/`default_account_id` or a response/push carrying request-only fields is invalid.
    """

    channel: Literal["account"]
    schema: Literal["afbws.account.list.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    bf_id: NotRequired[AccountV2BfId]
    account_id: NotRequired[AccountV2AccountId]
    force: NotRequired[bool]
    default_account_id: NotRequired[AccountV2AccountId]
    items: NotRequired[list[AccountV2Snapshot]]


class AccountV2Order(TypedDict):
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


class AccountV2Orders(TypedDict):
    """
    Request (`request_id`, no `items`): `bf_id` required; `account_id` omitted = the connector's default (trading) account (the only account order history is available for, see payloads/broker.orders.json). Response (same `request_id`, with `items`): `bf_id`, `account_id`, `items[]`. Push (no `request_id`, server-initiated): `bf_id`, `account_id`, `items[]` for the default (trading) account.
    """

    channel: Literal["account"]
    schema: Literal["afbws.account.orders.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    bf_id: AccountV2BfId
    account_id: NotRequired[AccountV2AccountId]
    items: NotRequired[list[AccountV2Order]]


AccountChannelV2Message: TypeAlias = (
    AccountV2List | AccountV2Orders | AccountV2Events | AccountV2Error
)


class AccountV2Snapshot(TypedDict):
    bf_id: AccountV2BfId
    account_id: AccountV2AccountId
    tradable: bool
    readonly: bool
    status: Literal["ok", "stale", "error"]
    equity: str | None
    cash: list[PayloadsBrokerAccountsCashBalance]
    positions: list[AfbwsAccountChannelV2Position]
    as_of: NotRequired[str]


class AfbwsAccountChannelV2Position(TypedDict):
    quantity: int
    average_price: str
    current_price: NotRequired[str | None]
    unrealized_pnl: NotRequired[str | None]
    instrument: NotRequired[dict[str, Any]]
    broker_ref: NotRequired[dict[str, Any]]


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
    "not_paired",
    "superseded",
    "busy",
]


AfbwsCommonV1InstrumentKey: TypeAlias = str


AfbwsCommonV1RequestId: TypeAlias = str


AfbwsCommonV1Root: TypeAlias = Any


class AfbwsInstrumentChannelV2AccountDetail(TypedDict):
    bf_id: str
    account_id: str
    status: Literal["ok", "unavailable", "error"]
    scope: NotRequired[Literal["account", "connector"]]
    broker_instrument: NotRequired[dict[str, Any]]
    error: NotRequired[Error]


class AfbwsInstrumentChannelV2AccountRef(TypedDict):
    """
    A broker account (or the virtual one) of the caller. `account_id` is what the trading parameters depend on; `bf_id` accompanies it while an account id is unique only within a connector.
    """

    bf_id: str
    account_id: str


class AfbwsInstrumentChannelV2Asset(TypedDict):
    id: str
    name: str
    collection_id: str | None
    members: list[AfbwsInstrumentChannelV2Member]


class AfbwsInstrumentChannelV2Catalog1(TypedDict):
    """
    Request: only `request_id`. Response (same `request_id`): what the caller may see — ordered `collections`, `sets` (global sets published for the caller's tier plus the caller's own `personal` ones, in display order), `assets` with members, the active `listings` the caller may see and the `derivatives` axis. Completeness is applied by the backend from the caller's role (a manager also sees unassigned assets). `revision` is the global catalog revision (`catalog_revision` of `sets`), `user_revision` the revision of the caller's personal sets aggregate. Any authenticated caller.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.catalog.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    revision: NotRequired[int]
    user_revision: NotRequired[int]
    collections: NotRequired[list[AfbwsInstrumentChannelV2Collection]]
    sets: NotRequired[list[AfbwsInstrumentChannelV2Set]]
    assets: NotRequired[list[AfbwsInstrumentChannelV2Asset]]
    listings: NotRequired[list[AfbwsInstrumentChannelV2Listing]]
    derivatives: NotRequired[list[AfbwsInstrumentChannelV2Derivative]]


class AfbwsInstrumentChannelV2Catalog2(TypedDict):
    """
    Request: only `request_id`. Response (same `request_id`): what the caller may see — ordered `collections`, `sets` (global sets published for the caller's tier plus the caller's own `personal` ones, in display order), `assets` with members, the active `listings` the caller may see and the `derivatives` axis. Completeness is applied by the backend from the caller's role (a manager also sees unassigned assets). `revision` is the global catalog revision (`catalog_revision` of `sets`), `user_revision` the revision of the caller's personal sets aggregate. Any authenticated caller.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.catalog.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    revision: int
    user_revision: int
    collections: list[AfbwsInstrumentChannelV2Collection]
    sets: list[AfbwsInstrumentChannelV2Set]
    assets: list[AfbwsInstrumentChannelV2Asset]
    listings: list[AfbwsInstrumentChannelV2Listing]
    derivatives: list[AfbwsInstrumentChannelV2Derivative]


AfbwsInstrumentChannelV2Catalog: TypeAlias = (
    AfbwsInstrumentChannelV2Catalog1 | AfbwsInstrumentChannelV2Catalog2
)


class AfbwsInstrumentChannelV2Collection(TypedDict):
    """
    A node of the category tree; its position in `collections[]` is the display order. `asset_ids` is the ordered composition (assets filed into it).
    """

    id: str
    name: str
    parent_id: NotRequired[str | None]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV2FavoriteColor | None]
    asset_ids: list[str]


class AfbwsInstrumentChannelV2Derivative(TypedDict):
    code: str
    kind: Literal["perpetual", "series", "options"]
    name: str
    underlying_key: NotRequired[AfbwsCommonV1InstrumentKey | None]
    source: str


class AfbwsInstrumentChannelV2Detail1(TypedDict):
    """
    Request: `instrument_key` and optionally `accounts[]` to narrow the answer; by default ALL accounts of the caller, the virtual one included. The tradeplan editor asks once when it opens (and when the instrument changes) and picks the selected account from `items[]`. Response (same `request_id`): `items[]` — one entry per account; a failure of one account is that entry's `status`/`error`, the others are unaffected. A whole-request error (`not_found` for an unknown key, `forbidden`, `unavailable` when there are no accounts) is `afbws.instrument.error.v2`. Any authenticated caller.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.detail.v2"]
    request_id: AfbwsCommonV1RequestId
    instrument_key: AfbwsCommonV1InstrumentKey
    accounts: NotRequired[list[AfbwsInstrumentChannelV2AccountRef]]
    items: NotRequired[list[AfbwsInstrumentChannelV2AccountDetail]]


class AfbwsInstrumentChannelV2Detail2(TypedDict):
    """
    Request: `instrument_key` and optionally `accounts[]` to narrow the answer; by default ALL accounts of the caller, the virtual one included. The tradeplan editor asks once when it opens (and when the instrument changes) and picks the selected account from `items[]`. Response (same `request_id`): `items[]` — one entry per account; a failure of one account is that entry's `status`/`error`, the others are unaffected. A whole-request error (`not_found` for an unknown key, `forbidden`, `unavailable` when there are no accounts) is `afbws.instrument.error.v2`. Any authenticated caller.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.detail.v2"]
    request_id: AfbwsCommonV1RequestId
    instrument_key: AfbwsCommonV1InstrumentKey
    accounts: NotRequired[list[AfbwsInstrumentChannelV2AccountRef]]
    items: list[AfbwsInstrumentChannelV2AccountDetail]


AfbwsInstrumentChannelV2Detail: TypeAlias = (
    AfbwsInstrumentChannelV2Detail1 | AfbwsInstrumentChannelV2Detail2
)


class AfbwsInstrumentChannelV2Error(TypedDict):
    """
    `details`: `catalog_revision` / `user_revision` for `conflict`; `set_ids` / `asset_ids` / `instrument_keys` naming the rows at fault for `forbidden` / `validation_error`; `limit` for a tier-limit overflow.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.error.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    code: Literal[
        "forbidden",
        "invalid_schema",
        "invalid_channel",
        "unsupported_action",
        "validation_error",
        "not_found",
        "conflict",
        "bf_offline",
        "internal_error",
    ]
    message: str
    details: NotRequired[Details]


class AfbwsInstrumentChannelV2Expiration1(TypedDict):
    """
    Request: only `request_id`. Response: `items[]` nearest expiration first. The SAME schema is the server push: a message WITHOUT `request_id` carries the caller's full current list, which REPLACES the client's copy (an empty list clears the card).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.expiration.v2"]
    request_id: AfbwsCommonV1RequestId
    items: NotRequired[list[AfbwsInstrumentChannelV2ExpirationNotice]]


class AfbwsInstrumentChannelV2Expiration2(TypedDict):
    """
    Request: only `request_id`. Response: `items[]` nearest expiration first. The SAME schema is the server push: a message WITHOUT `request_id` carries the caller's full current list, which REPLACES the client's copy (an empty list clears the card).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.expiration.v2"]
    request_id: AfbwsCommonV1RequestId
    items: list[AfbwsInstrumentChannelV2ExpirationNotice]


class AfbwsInstrumentChannelV2Expiration3(TypedDict):
    """
    Request: only `request_id`. Response: `items[]` nearest expiration first. The SAME schema is the server push: a message WITHOUT `request_id` carries the caller's full current list, which REPLACES the client's copy (an empty list clears the card).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.expiration.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    items: list[AfbwsInstrumentChannelV2ExpirationNotice]


AfbwsInstrumentChannelV2Expiration: TypeAlias = (
    AfbwsInstrumentChannelV2Expiration1
    | AfbwsInstrumentChannelV2Expiration2
    | AfbwsInstrumentChannelV2Expiration3
)


class AfbwsInstrumentChannelV2ExpirationCandidate(TypedDict):
    instrument_key: AfbwsCommonV1InstrumentKey
    ticker: str
    expiration: str
    shortname: NotRequired[str]


class AfbwsInstrumentChannelV2ExpirationNotice(TypedDict):
    """
    One expiring contract the caller uses, ready for the replace card (computed by the server). `ticker` is display only.
    """

    instrument_key: AfbwsCommonV1InstrumentKey
    ticker: str
    shortname: NotRequired[str]
    expiration: str
    days_left: int
    usage: AfbwsInstrumentChannelV2ExpirationUsage
    candidates: list[AfbwsInstrumentChannelV2ExpirationCandidate]


class AfbwsInstrumentChannelV2ExpirationUsage(TypedDict):
    alarms: int
    primitives: int
    sets: int
    favorites: int


AfbwsInstrumentChannelV2FavoriteColor: TypeAlias = Literal[
    "yellow", "red", "blue", "green", "gray", "orange", "cyan", "purple", "pink", "teal"
]


class AfbwsInstrumentChannelV2FavoriteEntry(TypedDict):
    kind: Literal["instrument", "asset"]
    key: str
    color: AfbwsInstrumentChannelV2FavoriteColor


class AfbwsInstrumentChannelV2FavoriteRef(TypedDict):
    """
    `key` is an `instrument_key` for kind `instrument` and an `asset_id` for kind `asset`.
    """

    kind: Literal["instrument", "asset"]
    key: str


class AfbwsInstrumentChannelV2Favorites(TypedDict):
    """
    Request: only `request_id`. Response: `favorites` in display order (array position is the order).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.favorites.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    favorites: NotRequired[list[AfbwsInstrumentChannelV2FavoriteEntry]]


class AfbwsInstrumentChannelV2Listing(TypedDict):
    """
    An active catalog listing. `instrument_key` is the identity; `ticker` is a display attribute only (for non-MISX it is `MIC:TICKER`) and is never an address in this channel.
    """

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


class AfbwsInstrumentChannelV2Member(TypedDict):
    """
    One ordered member of an asset: `listing` (ref = instrument_key) or `derivative` (ref = derivative code `MIC:CODE`).
    """

    kind: Literal["listing", "derivative"]
    ref: str


class AfbwsInstrumentChannelV2Paint(TypedDict):
    """
    No CAS: `mark` (paint or repaint), `unmark` (idempotent removal) and `order` (REPLACES the whole display order) are idempotent. Request: any of `mark`/`unmark`/`order`. Response: `marked`/`unmarked`/`order` — only the sections that were present in the request; `unmarked` lists only refs that really were favorites. A response is recognised by `marked`/`unmarked`; an `order`-only request and its echo have the same shape.
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.paint.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    mark: NotRequired[list[AfbwsInstrumentChannelV2FavoriteEntry]]
    unmark: NotRequired[list[AfbwsInstrumentChannelV2FavoriteRef]]
    order: NotRequired[list[AfbwsInstrumentChannelV2FavoriteRef]]
    marked: NotRequired[list[AfbwsInstrumentChannelV2FavoriteEntry]]
    unmarked: NotRequired[list[AfbwsInstrumentChannelV2FavoriteRef]]


class AfbwsInstrumentChannelV2Replace1(TypedDict):
    """
    Request: `from_key`, `to_key` (an ACTIVE contract of the same derivative) and optional `kinds` (default all four). Prices and levels are never adjusted. Partial results are normal: what could not be moved is in `rejected[]`. Idempotent. Response: the same keys plus `replaced` (counts), `rejected[]` and the refreshed `items[]` (as a fresh `expiration`).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.replace.v2"]
    request_id: AfbwsCommonV1RequestId
    from_key: AfbwsCommonV1InstrumentKey
    to_key: AfbwsCommonV1InstrumentKey
    kinds: NotRequired[list[AfbwsInstrumentChannelV2ReplaceKind]]
    replaced: NotRequired[AfbwsInstrumentChannelV2ExpirationUsage]
    rejected: NotRequired[list[AfbwsInstrumentChannelV2ReplaceRejection]]
    items: NotRequired[list[AfbwsInstrumentChannelV2ExpirationNotice]]


class AfbwsInstrumentChannelV2Replace2(TypedDict):
    """
    Request: `from_key`, `to_key` (an ACTIVE contract of the same derivative) and optional `kinds` (default all four). Prices and levels are never adjusted. Partial results are normal: what could not be moved is in `rejected[]`. Idempotent. Response: the same keys plus `replaced` (counts), `rejected[]` and the refreshed `items[]` (as a fresh `expiration`).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.replace.v2"]
    request_id: AfbwsCommonV1RequestId
    from_key: AfbwsCommonV1InstrumentKey
    to_key: AfbwsCommonV1InstrumentKey
    kinds: NotRequired[list[AfbwsInstrumentChannelV2ReplaceKind]]
    replaced: AfbwsInstrumentChannelV2ExpirationUsage
    rejected: list[AfbwsInstrumentChannelV2ReplaceRejection]
    items: list[AfbwsInstrumentChannelV2ExpirationNotice]


AfbwsInstrumentChannelV2Replace: TypeAlias = (
    AfbwsInstrumentChannelV2Replace1 | AfbwsInstrumentChannelV2Replace2
)


AfbwsInstrumentChannelV2ReplaceKind: TypeAlias = Literal[
    "alarms", "primitives", "sets", "favorites"
]


class AfbwsInstrumentChannelV2ReplaceRejection(TypedDict):
    kind: AfbwsInstrumentChannelV2ReplaceKind
    id: str
    code: Literal[
        "not_found", "validation_error", "conflict", "forbidden", "internal_error"
    ]
    message: NotRequired[str]


class AfbwsInstrumentChannelV2Set(TypedDict):
    """
    A named set of assets (`asset_ids[]`) or of instruments (`instrument_keys[]`), by `type`; exactly the list of its own type is present, always the WHOLE composition in display order. `type` is decided on create and cannot change afterwards.
    """

    id: str
    name: str
    type: Literal["asset", "instrument"]
    visibility: AfbwsInstrumentChannelV2Visibility
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV2FavoriteColor | None]
    asset_ids: NotRequired[list[str]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]


class AfbwsInstrumentChannelV2SetEdit(TypedDict):
    """
    A set inside `sets` (request / response). Request: `type` (default `asset` on create; on update must equal the stored one) and `visibility` (default `personal` on create; unchanged on update) are optional; the composition list of the set's own type, when present, is the WHOLE composition in final order. Response: every field of `set` is present.
    """

    id: str
    name: str
    type: NotRequired[Literal["asset", "instrument"]]
    visibility: NotRequired[AfbwsInstrumentChannelV2Visibility]
    icon_id: NotRequired[str | None]
    icon_color: NotRequired[AfbwsInstrumentChannelV2FavoriteColor | None]
    asset_ids: NotRequired[list[str]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]


class AfbwsInstrumentChannelV2Sets1(TypedDict):
    """
    ONE command for all authenticated callers; the only difference between a user and a manager is the `visibility` of the set, checked by the backend. Request: `sets[]` — upsert by `id`, each with its WHOLE composition in final order (omit the list to leave a set's composition untouched); the order of `sets[]` is the display order of the sets (personal ones and global ones are ordered separately); `remove_sets[]` — ids to delete. `visibility` `personal` (default for a new set) is open to everybody within the tier limit `max_sets`; `guest|user|manager` (global set) is manager-only (`forbidden`, `details.set_ids`). A set keeps its scope: switching between `personal` and a global visibility is `validation_error`. CAS: `user_revision` guards the personal sets, `catalog_revision` the global ones; each is required when the request touches that area (stale -> `conflict` with the current revisions in `details`). The request is atomic: if anything is rejected nothing is applied. Response (same `request_id`): both revisions and `sets[]` — the caller's visible sets after the change, in display order (same form as `catalog.sets`).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.sets.v2"]
    request_id: AfbwsCommonV1RequestId
    user_revision: NotRequired[int]
    catalog_revision: NotRequired[int]
    sets: NotRequired[list[AfbwsInstrumentChannelV2SetEdit]]
    remove_sets: NotRequired[list[str]]
    applied: NotRequired[Literal[True]]


class AfbwsInstrumentChannelV2Sets2(TypedDict):
    """
    ONE command for all authenticated callers; the only difference between a user and a manager is the `visibility` of the set, checked by the backend. Request: `sets[]` — upsert by `id`, each with its WHOLE composition in final order (omit the list to leave a set's composition untouched); the order of `sets[]` is the display order of the sets (personal ones and global ones are ordered separately); `remove_sets[]` — ids to delete. `visibility` `personal` (default for a new set) is open to everybody within the tier limit `max_sets`; `guest|user|manager` (global set) is manager-only (`forbidden`, `details.set_ids`). A set keeps its scope: switching between `personal` and a global visibility is `validation_error`. CAS: `user_revision` guards the personal sets, `catalog_revision` the global ones; each is required when the request touches that area (stale -> `conflict` with the current revisions in `details`). The request is atomic: if anything is rejected nothing is applied. Response (same `request_id`): both revisions and `sets[]` — the caller's visible sets after the change, in display order (same form as `catalog.sets`).
    """

    channel: Literal["instrument"]
    schema: Literal["afbws.instrument.sets.v2"]
    request_id: AfbwsCommonV1RequestId
    user_revision: int
    catalog_revision: int
    sets: list[AfbwsInstrumentChannelV2SetEdit]
    remove_sets: NotRequired[list[str]]
    applied: Literal[True]


AfbwsInstrumentChannelV2Sets: TypeAlias = (
    AfbwsInstrumentChannelV2Sets1 | AfbwsInstrumentChannelV2Sets2
)


AfbwsInstrumentChannelV2Root: TypeAlias = (
    AfbwsInstrumentChannelV2Catalog
    | AfbwsInstrumentChannelV2Sets
    | AfbwsInstrumentChannelV2Favorites
    | AfbwsInstrumentChannelV2Paint
    | AfbwsInstrumentChannelV2Expiration
    | AfbwsInstrumentChannelV2Replace
    | AfbwsInstrumentChannelV2Detail
    | AfbwsInstrumentChannelV2Error
)


AfbwsInstrumentChannelV2Visibility: TypeAlias = Literal[
    "personal", "guest", "user", "manager"
]


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


AfbwsScreenerChannelV1ExportId: TypeAlias = str


AfbwsScreenerChannelV1ExportKind: TypeAlias = Literal["night", "intraday"]


AfbwsScreenerChannelV1ExportRef: TypeAlias = str


AfbwsScreenerChannelV1FavoriteColor: TypeAlias = Literal[
    "yellow", "red", "blue", "green", "gray", "orange", "cyan", "purple", "pink", "teal"
]


class AfbwsScreenerChannelV1ListItem(TypedDict):
    id: AfbwsScreenerChannelV1ExportId
    kind: AfbwsScreenerChannelV1ExportKind
    trading_day: str
    asof: str
    generated_at: str
    size: int


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


class Alarms1(TypedDict):
    confirm_delete: NotRequired[bool]


class Backstop(TypedDict):
    """
    Per-deal overrides for the hybrid-mode server-side backstop order; unset fields fall back to the executing BF's own config defaults. Meaningful only when execution_mode is `hybrid`.
    """

    offset_steps: NotRequired[int]
    stop_price: NotRequired[DecimalString]
    max_loss_steps: NotRequired[int]
    take_profit: NotRequired[bool]


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


class BrokerAccountsPayload(TypedDict):
    """
    Response to broker.get_accounts and unsolicited push after every reconcile pass (see belphegor/reporting/account_directory.py::AccountDirectory, engine.py::_publish_broker_snapshots) — full list of accounts visible to BF's broker token. `accounts[].account_id` is the ONLY account identifier — no broker_account_id split, by design. Positions carry only `broker_ref {broker, symbol}`: BF has no instrument catalog, AFB maps the symbol to its own instrument (instrument_key) itself. Only `default_account_id` (BF's own trading account, self._account_id) is tradable in this phase — see brokers/port.py::account_id docstring; the rest are read-only until a later multi-account execution phase.
    """

    default_account_id: str
    as_of: str
    accounts: list[PayloadsBrokerAccountsAccount]


class BrokerErrorPayload(TypedDict):
    """
    NACK for any broker.* command (get_accounts/get_orders/resolve_instrument). Correlated to the request via correlation_id.
    """

    at: NotRequired[str]
    code: str
    command_type: str
    message: NotRequired[str]


class BrokerGetAccountsPayload(TypedDict):
    """
    Request the full list of accounts visible to BF's broker token (not just its own trading account) — see belphegor/reporting/account_directory.py::AccountDirectory. AFB always sends an empty payload today; account_ids is reserved for a future partial-refresh use and is not currently read by BF.
    """

    account_ids: NotRequired[list[str]]


class BrokerGetOrdersPayload(TypedDict):
    """
    AFB always sends an empty payload; no filters exist today.
    """


class BrokerInstrument(TypedDict):
    """
    BF trading params of the resolved instrument (initial margin, tradable/longable/shortable, lot size, price_step, price_type, ...) — see InstrumentInfo.to_broker_instrument_dict(). With `account_id` in the request the values are the account's own.
    """

    price_type: NotRequired[Literal["UNKNOWN", "POSITIVE", "NON_NEGATIVE", "ANY"]]


class BrokerInstrument1(TypedDict):
    price_type: NotRequired[Literal["UNKNOWN", "POSITIVE", "NON_NEGATIVE", "ANY"]]
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


class BrokerInstrumentResolvedPayload(TypedDict):
    """
    Response to broker.resolve_instrument (deal-instrument pre-flight resolution). Deliberately permissive (additionalProperties: true throughout) — both objects are BF-owned shapes; this is a PATCH-level description of existing wire behavior, not a new constraint on it.
    """

    binding: dict[str, Any]
    broker_instrument: BrokerInstrument


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


class BrokerRef(TypedDict):
    broker: str
    symbol: str


class BrokerResolveInstrumentPayload(TypedDict):
    """
    Deal-instrument pre-flight (AFB's afbws.instrument.channel.v2 `detail`, and the tradeplan publish path) — `deal` is a compiled ExecutionDeal (afb.deal.v2), the same shape deal.publish carries, sent here purely for its target/instrument fields; BF does not persist it from this command.
    """

    deal: DealV2
    account_id: NotRequired[str]


class BrokerSizing(TypedDict):
    account_id: NotRequired[str]
    deal_notional: NotRequired[str]
    lots: NotRequired[int]
    required_cash: NotRequired[str]
    required_cash_basis: NotRequired[str]
    sizing_mode: NotRequired[str]
    estimated: NotRequired[bool]


class Bubble(TypedDict):
    """
    Selected axes of the bubble chart.
    """

    x: NotRequired[str]
    y: NotRequired[str]


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
    deal_seq: NotRequired[int]
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
    settings_storage: NotRequired[Literal["server", "local"]]
    chart_type: NotRequired[Literal["candles", "bars"]]
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
    Canon of the user settings carried by `afbws.config.settings.v1` (root = the `settings` object) and of the platform defaults carried by `afbws.config.defaults.v1` (`$defs/defaults`). Replaces the parked `draft/` schemas and the legacy `settings` channel payload. Every property is optional: the on-disk user file stores only what the user overrode and a write is a partial patch (blocks `profile`/`interface`/`dataset`/`dashboard`/`form`/`participants` are deep-merged (arrays such as `participants.columns` are replaced whole), `trade` is replaced whole). Not part of the payload any more: `limits` (travels in `auth_ok`), `favorites` (channel `instrument`), `indicators`/`primitives` (channel `gp`), alarms/tradeplans (their own channels). Booleans are real JSON booleans.
    """

    profile: NotRequired[ConfigProfile]
    interface: NotRequired[ConfigInterface]
    dataset: NotRequired[ConfigDataset]
    dashboard: NotRequired[ConfigDashboard]
    trade: NotRequired[ConfigTrade]
    form: NotRequired[ConfigV1Form]
    participants: NotRequired[ConfigV1Participants]


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

    default_connector: NotRequired[str]
    default_capital: NotRequired[float]
    default_risk_pct: NotRequired[float]
    notify: NotRequired[ConfigV1TradeNotify]
    chart_deal_markers: NotRequired[bool]


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


class ConfigV1Form(TypedDict):
    """
    Stored here when `interface.settings_storage` is `server`; otherwise the same keys (`form.<service>.<name>`) live in localStorage.
    """

    alarms: NotRequired[Alarms1]
    primitives: NotRequired[Primitives]
    plans: NotRequired[Plans1]
    participants: NotRequired[Participants]


class ConfigV1Participants(TypedDict):
    """
    Stored here when `interface.settings_storage` is `server`; otherwise the same structure lives in localStorage. Sort and bubble axes are kept always; `columns` order applies only when `form.participants.use_recommended` is false.
    """

    columns: NotRequired[list[Column]]
    widths: NotRequired[dict[str, int]]
    sort: NotRequired[Sort]
    bubble: NotRequired[Bubble]


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
    broker_instrument: NotRequired[BrokerInstrument1]
    broker_sizing: NotRequired[BrokerSizing]
    command_type: str
    deal_id: str
    revision: int
    target_instrument_patch: NotRequired[dict[str, Any]]
    validation: NotRequired[Validation]


class DealAmendPayload(TypedDict):
    """
    Re-define an existing deal in place. `deal` is the full new definition (its `revision` must be `base_revision` + 1, same `deal_id`). BF gates the change against the allowed-edit matrix (amend_rules) using the deal's live execution phase, then lets reconcile bring broker orders to the new desired state. Unlike deal.publish, the deal's status and observed execution state (orders/positions/phase) are preserved.
    """

    deal_id: str
    base_revision: int
    deal: DealV2
    definition_hash: NotRequired[str]


class DealArchivedPayload(TypedDict):
    archived_at: NotRequired[str]
    at: NotRequired[str]
    deal_id: str
    reason: str
    revision: int


DealExecutionPhase: TypeAlias = Literal[
    "idle", "awaiting_entry", "entry_working", "holding", "exit_working"
]


class DealExecutionPolicy(TypedDict):
    on_afb_disconnect: NotRequired[str]
    max_spread_steps: NotRequired[int]
    margin_trading: NotRequired[bool]
    execution_mode: NotRequired[Literal["client", "hybrid", "server"]]
    backstop: NotRequired[Backstop]


class DealInstrument(TypedDict):
    exchange: str
    board: str
    ticker: str
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    broker_symbol: NotRequired[str]
    market: NotRequired[Literal["stock", "futures", "currency"]]
    price_step: NotRequired[DecimalString]
    step_price: NotRequired[DecimalString]


class DealOperationPayload(TypedDict):
    operations: NotRequired[list[Operation]]


class DealPositionsSyncedPayload(TypedDict):
    deal_seq: NotRequired[int]
    at: NotRequired[str]
    changed: NotRequired[list[ChangedItem]]
    deal_id: str


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
    leg_id: NotRequired[LegId]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: DealV2ConditionNode
    source: NotRequired[DealV2LegSource]


DealPublicExitList: TypeAlias = list[DealPublicExitListItem]


class DealPublicSource(TypedDict):
    tradeplan_id: str


DealPublicV1: TypeAlias = DealPublicDealV2


class DealPublishPayload(TypedDict):
    deal: DealV2
    definition_hash: NotRequired[str]


class DealRejectedPayload(TypedDict):
    at: NotRequired[str]
    code: str
    command_type: NotRequired[str]
    deal_id: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]
    message: NotRequired[str]
    broker_error: NotRequired[PayloadsDealRejectedBrokerError]


class DealReportPayload(TypedDict):
    """
    Report attached to deal.status_changed(closed) with the trade-based fill log for the just-closed deal. It may be sent again for the same deal as a PATCH (same fills, enriched with data the broker books later, e.g. `fills[].exchange_fee`; every send gets a new `deal_seq` and idempotency key) — a consumer merges by `trade_id` and must not treat the repeat as a second close. `trade_id` is not required — tolerant of older BF versions that predate it. The `summary` block (entry/exit_avg_price, realized_pnl, total_commission) was removed in v2.0.10: it had no consumers (AFB computes realized PnL itself from fills/order events), was never in `required`, and `additionalProperties: true` keeps old and new payloads mutually valid — a PATCH, not a breaking change. `fills[].commission` was removed in the same step for the same reason; it is replaced by the optional per-trade `fills[].exchange_fee` (a real consumer exists now: realized P&L after exchange fee) — BROKER commission is intentionally not carried per deal.
    """

    deal_seq: NotRequired[int]
    at: NotRequired[str]
    close_reason: NotRequired[str]
    deal_id: str
    revision: int
    status: str
    fills: NotRequired[list[Fill]]


class DealSizing(TypedDict):
    mode: Literal["lots", "margin", "risk_currency", "risk_factor", "balance_pct"]
    value: DecimalString


class DealSnapshotPayload(TypedDict):
    deal_seq: NotRequired[int]
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


DealStatus: TypeAlias = Literal[
    "draft",
    "publishing",
    "published",
    "active",
    "paused",
    "closed",
    "cancelled",
    "orphaned",
]


class DealStatusChangedPayload(TypedDict):
    deal_seq: NotRequired[int]
    at: NotRequired[str]
    deal_id: str
    execution_phase: NotRequired[str]
    last_price: NotRequired[str]
    quantity: NotRequired[int]
    revision: int
    status: str


class DealTarget(TypedDict):
    bf_id: str
    broker: str
    instrument: DealInstrument
    binding: NotRequired[dict[str, Any]]
    account_id: NotRequired[str]


class DealV2(TypedDict):
    """
    Multi-entry / multi-exit deal. entry, stop_loss, take_profit are root-level lists; each element may carry an optional `percent` (decimal string) and an optional `logic` (`#/$defs/legJoin`) joining it to the PRECEDING element in the same list — see `legJoin` for the full grammar (groups/buckets, `and`/`or` precedence, `percent` placement). Sum of percents per bucket resolves to 100. The deal-level `direction` (long/short) is the single source of truth for position bias — entry legs no longer carry a per-leg `side`, which would let 'buy' and 'sell' legs coexist in the same deal with no defined semantics (a deal is one position, not a basket of unrelated orders). The broker-facing buy/sell of each leg is derived from `direction` and its role: long entry / short exit -> buy; short entry / long exit -> sell. Reuses order/sizing/target defs from common.v1.json; conditionNode is condition.v1.json's shared vocabulary (see that schema for the full price/indicator/dataset operator semantics) plus the wire-only `node_type` marker. Unlike afb.deal.v1 (fixed above/below/crosses_*/crossing vocabulary), afb.deal.v2 price conditions use condition.v1.json's full operator vocabulary — touch, above/below (inclusive level, no timeframe) and breakout/breakdown/crossing (closed-candle, requires timeframe) — or compare indicator/dataset expressions against a constant or (for indicator/dataset) against another expression of the same kind.
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


class DealV2AcceptedData(TypedDict):
    """
    BF-only fields (`broker_instrument`, `validation`, `broker_sizing`, `binding`, `target_instrument_patch`) are not forwarded.
    """

    command_type: str
    revision: NotRequired[int]
    at: NotRequired[str]


class DealV2Ack(TypedDict):
    """
    Request: `events[]` (afb.deal.trigger_ack.v2), at least one. Response (same `request_id`): `results[]` — one per event, `status` ok | not_found. Exactly one of `events` / `results`.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.ack.v2"]
    request_id: AfbwsCommonV1RequestId
    events: NotRequired[list[DealV2AckEvent]]
    results: NotRequired[list[DealV2AckResultItem]]


class DealV2AckEvent(TypedDict):
    schema: Literal["afb.deal.trigger_ack.v2"]
    notification_id: str


class DealV2AckResultItem(TypedDict):
    schema: Literal["afbws.deal.ack_result.v2"]
    notification_id: str
    status: Literal["ok", "not_found"]


class DealV2Amend(TypedDict):
    """
    Request: `items[]` (at least one) of `{deal_id, deal_edit?, base_revision?}`. Response (same `request_id`): `results[]` (amendResult, one per item; a rejected or conflicting row never fails the batch) and `accepted` (any row accepted). Distinguished by `items` vs `results`.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.amend.v2"]
    request_id: AfbwsCommonV1RequestId
    items: NotRequired[list[DealV2AmendItem]]
    results: NotRequired[list[DealV2AmendResult]]
    accepted: NotRequired[bool]


DealV2AmendField: TypeAlias = Literal[
    "entry", "sizing", "stop_loss", "take_profit", "execution_policy"
]


class DealV2AmendItem(TypedDict):
    """
    Optional `deal_edit` (only the legs/fields overridden on the deal side; anything omitted keeps following the linked tradeplan) and optional `base_revision` (optimistic concurrency: a mismatch rejects this row with `conflict` and the current `item`).
    """

    deal_id: DealV2Id
    deal_edit: NotRequired[DealV2Edit]
    base_revision: NotRequired[int]


class DealV2AmendResult(TypedDict):
    """
    accepted=true: `revision` (the new revision), `status` and `item` (the authoritative record) are set; no message/code. accepted=false: the deal is unchanged, `message` says why and `code` is the machine-readable reason when there is one; `item` (the authoritative current record) is present only with `conflict` — a stale `base_revision` — so the client can adopt it instead of retrying blind. The outcome of the BF confirmation arrives later as `outcome` and `event` pushes.
    """

    deal_id: DealV2Id
    accepted: bool
    revision: NotRequired[int]
    status: NotRequired[DealStatus]
    item: NotRequired[DealV2Detail]
    message: NotRequired[str]
    code: NotRequired[AfbwsCommonV1ErrorCode]


class DealV2AmendedData(TypedDict):
    """
    Light, no snapshot (state: `afbws.deal.record.v2`; BF confirmation: `accepted`/`rejected` events and `afbws.deal.outcome.v2`). Produced by AFB (no `at`).
    """

    revision: int


DealV2BfId: TypeAlias = str


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


class DealV2ConditionTriggeredData(TypedDict):
    condition_id: str
    price: NotRequired[str | None]
    phase: DealV2OrderRole
    at: NotRequired[str]


class DealV2CreatedData(TypedDict):
    """
    Light, no snapshot: the full state arrives as `afbws.deal.record.v2`. Produced by AFB (no `at`).
    """

    revision: int


class DealV2DeletedData(TypedDict):
    reason: NotRequired[str]
    archived_at: NotRequired[str]
    revision: NotRequired[int]
    at: NotRequired[str]


class DealV2Detail(TypedDict):
    """
    Allow-list built by backend/trade/public_views.py::deal_detail. `deal` is the public afb.deal.v2 projection (deal.public.v1.json). `editable_fields` lists what the current status/execution_phase allows to amend.
    """

    deal_id: DealV2Id
    revision: int
    status: DealStatus
    execution_phase: DealExecutionPhase
    bf_id: DealV2BfId
    tradeplan_id: TradeplanId
    ticker: str
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    market: NotRequired[Literal["stock", "futures", "currency"]]
    direction: Literal["long", "short"]
    sizing: NotRequired[DealSizing]
    execution_policy: NotRequired[DealExecutionPolicy]
    broker_sizing: NotRequired[DealV2SizingDisplay]
    realized_pnl: NotRequired[DealV2RealizedPnl]
    position: NotRequired[DealV2OpenPosition]
    created_at: str
    updated_at: str
    deal: DealPublicV1
    editable_fields: list[DealV2AmendField]


class DealV2Edit(TypedDict):
    entry: NotRequired[DealV2RoleEdit]
    stop_loss: NotRequired[DealV2RoleEdit]
    take_profit: NotRequired[DealV2RoleEdit]
    sizing: NotRequired[DealSizing]
    execution_policy: NotRequired[DealExecutionPolicy]


class DealV2Error(TypedDict):
    """
    Only for a whole request (invalid_schema, invalid_channel, forbidden, internal_error, ...). Per-deal failures of a batched publish/rebind/operation/amend are rows with accepted=false in that response's `results[]` (a stale `base_revision` is `code: conflict` with the current `item` there); no code carries `item` or `details`.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.error.v2"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str


class DealV2Event(TypedDict):
    """
    `events[]` (at least one) in order of occurrence, each a typed eventItem (a thin, allow-listed fact — never a state snapshot or a raw BF payload).
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.event.v2"]
    events: list[DealV2EventItem]


class DealV2EventConditionTriggered(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["condition"]
    event: Literal["triggered"]
    logged_at: str
    data: DealV2ConditionTriggeredData


class DealV2EventDealAccepted(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["accepted"]
    logged_at: str
    data: DealV2AcceptedData


class DealV2EventDealAmended(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["amended"]
    logged_at: str
    data: DealV2AmendedData


class DealV2EventDealCreated(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["created"]
    logged_at: str
    data: DealV2CreatedData


class DealV2EventDealDeleted(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["deleted"]
    logged_at: str
    data: DealV2DeletedData


class DealV2EventDealOrdersSynced(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["orders_synced"]
    logged_at: str
    data: DealV2OrdersSyncedData


class DealV2EventDealPositionsSynced(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["positions_synced"]
    logged_at: str
    data: DealV2PositionsSyncedData


class DealV2EventDealRejected(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["rejected"]
    logged_at: str
    data: DealV2RejectedData


class DealV2EventDealReport(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["report"]
    logged_at: str
    data: DealV2ReportData


class DealV2EventDealStatusChanged(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["deal"]
    event: Literal["status_changed"]
    logged_at: str
    data: DealV2StatusChangedData


class DealV2EventOrderCancelled(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["order"]
    event: Literal["cancelled"]
    logged_at: str
    data: DealV2OrderData


class DealV2EventOrderCreated(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["order"]
    event: Literal["created"]
    logged_at: str
    data: DealV2OrderCreatedData


class DealV2EventOrderFilled(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["order"]
    event: Literal["filled"]
    logged_at: str
    data: DealV2OrderData


class DealV2EventOrderPartiallyFilled(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["order"]
    event: Literal["partially_filled"]
    logged_at: str
    data: DealV2OrderData


class DealV2EventOrderRejected(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["order"]
    event: Literal["rejected"]
    logged_at: str
    data: DealV2OrderData


class DealV2EventPositionChanged(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["position"]
    event: Literal["changed"]
    logged_at: str
    data: DealV2PositionData


class DealV2EventPositionClosed(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["position"]
    event: Literal["closed"]
    logged_at: str
    data: DealV2PositionData


class DealV2EventPositionOpened(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId
    category: Literal["position"]
    event: Literal["opened"]
    logged_at: str
    data: DealV2PositionData


DealV2EventItem: TypeAlias = (
    DealV2EventDealCreated
    | DealV2EventDealAmended
    | DealV2EventDealAccepted
    | DealV2EventDealRejected
    | DealV2EventDealStatusChanged
    | DealV2EventDealDeleted
    | DealV2EventDealReport
    | DealV2EventDealOrdersSynced
    | DealV2EventDealPositionsSynced
    | DealV2EventOrderCreated
    | DealV2EventOrderFilled
    | DealV2EventOrderPartiallyFilled
    | DealV2EventOrderCancelled
    | DealV2EventOrderRejected
    | DealV2EventPositionOpened
    | DealV2EventPositionChanged
    | DealV2EventPositionClosed
    | DealV2EventConditionTriggered
)


class DealV2ExitListItem(TypedDict):
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: DealV2ConditionNode
    source: NotRequired[DealV2LegSource]


DealV2ExitList: TypeAlias = list[DealV2ExitListItem]


DealV2Id: TypeAlias = str


class DealV2Item(TypedDict):
    """
    Same allow-list as dealSummary (see there); with `detail: true` each row additionally carries `deal` (the public afb.deal.v2 projection) and `editable_fields` — together, i.e. a dealDetail. Rows of a list without `detail` never carry them.
    """

    deal_id: DealV2Id
    revision: int
    status: DealStatus
    execution_phase: DealExecutionPhase
    bf_id: DealV2BfId
    tradeplan_id: TradeplanId
    ticker: str
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    market: NotRequired[Literal["stock", "futures", "currency"]]
    direction: Literal["long", "short"]
    sizing: NotRequired[DealSizing]
    execution_policy: NotRequired[DealExecutionPolicy]
    broker_sizing: NotRequired[DealV2SizingDisplay]
    realized_pnl: NotRequired[DealV2RealizedPnl]
    position: NotRequired[DealV2OpenPosition]
    created_at: str
    updated_at: str
    deal: NotRequired[DealPublicV1]
    editable_fields: NotRequired[list[DealV2AmendField]]


class DealV2LegEdit(TypedDict):
    index: int
    condition: NotRequired[DealV2ConditionNode]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]


DealV2LegJoin: TypeAlias = Literal["split", "and", "or"]


DealV2LegSource: TypeAlias = Literal["tradeplan", "deal"]


class DealV2List(TypedDict):
    """
    Request: optional filters `ids[]`, `instrument_keys[]` and/or `tradeplan_ids[]` (all given = intersection; none = every deal of the caller) and optional `detail` (true = rows carry the full editor payload `deal` + `editable_fields`, i.e. a dealDetail; default false = summary rows). Response (same `request_id`): `items[]` (dealItem). There is no separate `get`: use `ids` with `detail: true`. A request carrying `items` is invalid, as is a response carrying a filter.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.list.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: NotRequired[list[DealV2Id]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]
    tradeplan_ids: NotRequired[list[TradeplanId]]
    detail: NotRequired[bool]
    items: NotRequired[list[DealV2Item]]


class DealV2NewLeg(TypedDict):
    condition: DealV2ConditionNode
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]


class DealV2OpenPosition(TypedDict):
    """
    Absent entirely means flat (no open position) or not yet known — distinct from a present qty of 0, which is never emitted.
    """

    qty: int
    avg_price: str
    as_of: str


class DealV2Operation(TypedDict):
    """
    Request: `items[]` (at least one). Response (same `request_id`): `results[]` (one per item, partial failures are rows with accepted=false) and `accepted`. Distinguished by `items` vs `results`.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.operation.v2"]
    request_id: AfbwsCommonV1RequestId
    items: NotRequired[list[DealV2OperationItem]]
    results: NotRequired[list[DealV2Result]]
    accepted: NotRequired[bool]


class DealV2OperationItem(TypedDict):
    deal_id: DealV2Id
    action: Literal["activate", "pause", "resume", "cancel", "reconcile", "delete"]
    cancel_open_orders: NotRequired[bool]


class DealV2OrderCreatedData(TypedDict):
    order_id: str
    side: DealV2OrderSide
    role: DealV2OrderRole
    quantity: NotRequired[int]
    price: NotRequired[str | None]
    status: DealV2OrderEventStatus
    at: NotRequired[str]
    broker_order_id: NotRequired[str]


class DealV2OrderData(TypedDict):
    order_id: str
    side: DealV2OrderSide
    role: DealV2OrderRole
    quantity: NotRequired[int]
    price: NotRequired[str | None]
    status: DealV2OrderEventStatus
    at: NotRequired[str]
    filled_quantity: NotRequired[int]
    leg_index: NotRequired[int]


DealV2OrderEventStatus: TypeAlias = Literal[
    "new",
    "partially_filled",
    "filled",
    "cancelled",
    "rejected",
    "watching",
    "expired",
    "unknown",
]


DealV2OrderRole: TypeAlias = Literal[
    "entry", "stop_loss", "take_profit", "cancel_close", "backstop", "external_close"
]


DealV2OrderSide: TypeAlias = Literal["buy", "sell"]


class DealV2OrdersSyncedData(TypedDict):
    """
    Marker event: the changed orders arrive as separate order.* events and in the record.
    """

    at: NotRequired[str]


class DealV2Outcome(TypedDict):
    """
    A separate push, so the client does not need the whole record just to show a toast; `items[]` (at least one), each is an independent outcome (see outcomeItem).
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.outcome.v2"]
    items: list[DealV2OutcomeItem]


class DealV2OutcomeItem(TypedDict):
    """
    A separate push, so the client does not need the whole record just to show a toast. AFB composes no user-facing texts: it passes through what BF returned, the text is built on the frontend. result=rejected: any BF rejection (`code` required). result=accepted: only the confirmation of `deal.amend` (the one accepted outcome the server reports), without code/message/broker_error.
    """

    deal_id: DealV2Id
    bf_id: DealV2BfId
    command: str | None
    result: Literal["accepted", "rejected"]
    code: NotRequired[str]
    message: NotRequired[str | None]
    broker_error: NotRequired[PayloadsDealRejectedBrokerError]


class DealV2Pnl(TypedDict):
    """
    Not persisted. ONE push per tick for all open deals of the user: `items[]` (at least one).
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.pnl.v2"]
    items: list[DealV2PnlItem]


class DealV2PnlItem(TypedDict):
    """
    `trend` is deliberately absent — a frontend-only projection computed from consecutive pushes.
    """

    deal_id: DealV2Id
    bf_id: DealV2BfId
    unrealized: str
    currency: str
    qty: int
    avg_price: str
    last_price: str
    as_of: str


class DealV2PositionData(TypedDict):
    symbol: str
    quantity: int
    average_price: NotRequired[str | None]
    at: NotRequired[str]


class DealV2PositionsSyncedData(TypedDict):
    """
    Marker event (declared by the BF protocol; current BF versions do not emit it).
    """

    at: NotRequired[str]


class DealV2Publish(TypedDict):
    """
    Request: `items[]` (at least one) of `{tradeplan_id, bf_id}` (no inline plan draft, 1:1 per row). Response (same `request_id`): `results[]` (one per item; a failed row is accepted=false) and `accepted`. Distinguished by `items` vs `results`.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.publish.v2"]
    request_id: AfbwsCommonV1RequestId
    items: NotRequired[list[DealV2PublishItem]]
    results: NotRequired[list[DealV2Result]]
    accepted: NotRequired[bool]


class DealV2PublishItem(TypedDict):
    tradeplan_id: TradeplanId
    bf_id: DealV2BfId


class DealV2RealizedPnl(TypedDict):
    """
    Absent entirely means no ledger yet (deal predates it, or has not had an exit fill) — distinct from a present-but-degraded value.
    """

    value: str | None
    degraded: Literal["missing_price", "missing_step_price"] | None


class DealV2Rebind(TypedDict):
    """
    Request: `items[]` (at least one) of `{deal_id, bf_id}` (the backend resolves the source tradeplan via the deal's own link). Response (same `request_id`): `results[]` and `accepted`; if the new target changes a deal id, that row's `deal_id`/`item` carry the NEW id. Distinguished by `items` vs `results`.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.rebind.v2"]
    request_id: AfbwsCommonV1RequestId
    items: NotRequired[list[DealV2RebindItem]]
    results: NotRequired[list[DealV2Result]]
    accepted: NotRequired[bool]


class DealV2RebindItem(TypedDict):
    deal_id: DealV2Id
    bf_id: DealV2BfId


class DealV2Record(TypedDict):
    """
    REPLACE per deal: for every item the client overwrites its cached copy identified by `item.deal_id`, never merges. One mutation (one batch command) = ONE push carrying all deals it changed. It carries NO command outcome — that is `afbws.deal.outcome.v2`; and no thin events are merged into it — see `afbws.deal.event.v2`.
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.record.v2"]
    items: list[DealV2Detail]


class DealV2RejectedData(TypedDict):
    code: str
    message: NotRequired[str]
    command_type: NotRequired[str]
    broker_error: NotRequired[PayloadsDealRejectedBrokerError]
    at: NotRequired[str]


class DealV2ReportData(TypedDict):
    status: DealStatus
    close_reason: NotRequired[str]
    fills: NotRequired[list[DealV2ReportFill]]
    at: NotRequired[str]


class DealV2ReportFill(TypedDict):
    trade_id: NotRequired[str]
    order_id: str
    role: DealV2OrderRole
    side: DealV2OrderSide
    price: NotRequired[str | None]
    quantity: NotRequired[int]
    timestamp: NotRequired[str | None]


class DealV2Result(TypedDict):
    """
    accepted=true: `bf_id` and `status` are set (status is `deleted` after a delete), `revision` is the deal's revision and `item` the authoritative record when the deal still exists. accepted=false: only `message` (why) — the command did not touch the deal, so there is no status/revision. When a rebind changes the deal id, `deal_id`/`item` carry the NEW id — the client must drop the old cache key.
    """

    deal_id: DealV2Id
    bf_id: NotRequired[DealV2BfId]
    status: NotRequired[DealV2ResultStatus]
    accepted: bool
    revision: NotRequired[int]
    item: NotRequired[DealV2Detail]
    message: NotRequired[str]


DealV2ResultStatus: TypeAlias = DealStatus | Literal["deleted"]


class DealV2RoleEdit(TypedDict):
    """
    Indices refer to the CURRENT deal's leg array for that role at base_revision — never a tradeplan's, never leg_id. edited/removed_indices/reset_indices apply to existing legs; new_legs are appended after them. See AFB backend tradeplans/overrides.py::apply_deal_edit for the exact merge order.
    """

    edited: NotRequired[list[DealV2LegEdit]]
    removed_indices: NotRequired[list[int]]
    reset_indices: NotRequired[list[int]]
    new_legs: NotRequired[list[DealV2NewLeg]]


class DealV2SizingDisplay(TypedDict):
    lots: NotRequired[int]
    required_cash: NotRequired[str]
    resolved_lots: NotRequired[int]


class DealV2StatusChangedData(TypedDict):
    """
    Deletion/archival is NOT a status: it is the `deleted` event.
    """

    status: DealStatus
    execution_phase: NotRequired[DealExecutionPhase]
    last_price: NotRequired[str]
    cancel_reason: NotRequired[str]
    quantity: NotRequired[int]
    at: NotRequired[str]


class DealV2Summary(TypedDict):
    """
    Explicit allow-list built by backend/trade/public_views.py::deal_summary, never a serialization of the persisted DealState (source_refs, status_history, event_journal, raw orders/positions, observed, owner_user_id never appear). `sizing` is the user-set {mode,value} from the «Риск и объём» block — NOT the broker_sizing projection, see `broker_sizing`.
    """

    deal_id: DealV2Id
    revision: int
    status: DealStatus
    execution_phase: DealExecutionPhase
    bf_id: DealV2BfId
    tradeplan_id: TradeplanId
    ticker: str
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    market: NotRequired[Literal["stock", "futures", "currency"]]
    direction: Literal["long", "short"]
    sizing: NotRequired[DealSizing]
    execution_policy: NotRequired[DealExecutionPolicy]
    broker_sizing: NotRequired[DealV2SizingDisplay]
    realized_pnl: NotRequired[DealV2RealizedPnl]
    position: NotRequired[DealV2OpenPosition]
    created_at: str
    updated_at: str


class DealV2TriggerRejected(TypedDict):
    schema: Literal["afb.deal.trigger.v2"]
    notification_id: str
    deal_id: DealV2Id
    bf_id: DealV2BfId
    event: Literal["rejected"]
    created_at: str
    data: DealV2RejectedData


class DealV2TriggerReport(TypedDict):
    schema: Literal["afb.deal.trigger.v2"]
    notification_id: str
    deal_id: DealV2Id
    bf_id: DealV2BfId
    event: Literal["report"]
    created_at: str
    data: DealV2TriggerReportData


class DealV2TriggerReportData(TypedDict):
    status: DealStatus
    close_reason: NotRequired[str]


class DealV2TriggerStatusChanged(TypedDict):
    schema: Literal["afb.deal.trigger.v2"]
    notification_id: str
    deal_id: DealV2Id
    bf_id: DealV2BfId
    event: Literal["status_changed"]
    created_at: str
    data: DealV2StatusChangedData


DealV2TriggerEvent: TypeAlias = (
    DealV2TriggerStatusChanged | DealV2TriggerRejected | DealV2TriggerReport
)


class DealV2Triggered(TypedDict):
    """
    Server-initiated; same ack discipline as alarms: a reconnect redelivers events that were not acked (afbws.deal.ack.v2).
    """

    channel: Literal["deal"]
    schema: Literal["afbws.deal.triggered.v2"]
    events: list[DealV2TriggerEvent]


DealChannelV2Message: TypeAlias = (
    DealV2List
    | DealV2Publish
    | DealV2Rebind
    | DealV2Operation
    | DealV2Amend
    | DealV2Ack
    | DealV2Error
    | DealV2Record
    | DealV2Outcome
    | DealV2Event
    | DealV2Pnl
    | DealV2Triggered
)


class Deals(TypedDict):
    revision: int
    status: str
    execution_phase: NotRequired[str]
    definition_hash: NotRequired[str]
    deal_seq: NotRequired[int]
    archived: bool


class Deals1(TypedDict):
    revision: int
    status: str
    execution_phase: NotRequired[str]
    definition_hash: NotRequired[str]
    applied_deal_seq: NotRequired[int]
    archived: bool


DecimalString: TypeAlias = str


class Details(TypedDict):
    catalog_revision: NotRequired[int]
    user_revision: NotRequired[int]
    set_ids: NotRequired[list[str]]
    asset_ids: NotRequired[list[str]]
    instrument_keys: NotRequired[list[str]]
    limit: NotRequired[Limit]


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


class Document(TypedDict):
    """
    Response only. Screener export content as is; see AFB/docs/SCREENER_RESULTS.md.
    """

    contract_version: NotRequired[int]


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


class EntryItem(TypedDict):
    leg_id: NotRequired[LegId]
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


class Error(TypedDict):
    code: Literal[
        "not_found", "bf_offline", "unsupported_action", "internal_error", "unavailable"
    ]
    message: str


class ExchangeFee(TypedDict):
    """
    Exchange fee (Finam `AccountTrade.commission`, the BUYSELLFEE part) charged for this very trade. The broker books it after clearing, so it is absent in the closing report and arrives later in a repeated deal.report (same fills, new `deal_seq`) — consumers merge it by `trade_id`. The BROKER commission is deliberately NOT part of this payload: it depends on the tariff (per contract, % of daily turnover, side-dependent) and cannot be attributed to a single deal; it travels per account in broker.accounts `broker_fees`.
    """

    value: str
    currency: str


class Features(TypedDict):
    dry_run: NotRequired[bool]
    server_sltp: NotRequired[bool]
    execution_modes: NotRequired[list[Literal["client", "hybrid", "server"]]]
    reports_api: NotRequired[bool]
    market_calendar: NotRequired[bool]


class Fill(TypedDict):
    trade_id: NotRequired[str]
    order_id: str
    price: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]
    quantity: NotRequired[int]
    exchange_fee: NotRequired[ExchangeFee]
    role: str
    side: str
    timestamp: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]


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
    tradeplan_id: NotRequired[TradeplanId]


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


LegId: TypeAlias = str


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
    Manager view of a BF connector config record — reuses link.user.v1.json#/$defs/sharedFields (via $ref, not redeclared, so the two views can't drift apart) plus ACL/key management fields. Never carries `connected`/`daemon`/session runtime — see link.channel.v2.json#/$defs/statusItem.
    """

    schema: Literal["afbws.link.admin.v1"]
    allowed_users: list[str]
    public_key_id: str | None
    public_key_file: str | None


class LinkUserSetInput(LinkSetInputShared):
    """
    A non-manager caller may adjust name/enabled/description/dry_run/execution_policy on their own already-existing connector — never broker/protocol/allowed_*/margin_trading, and never create a new entry (bf_id must already exist and be owned by the caller; enforced by the backend, not this schema).
    """

    bf_id: str


class LinkUserV1(BfRegistryEntry, LinkSharedFields):
    """
    Caller-scoped BF connector config record for a non-manager viewer (owner: capability trade + user_id in allowed_users, or role-only access — role-only is read-only, enforced by the backend, not this schema). Never carries `connected`/`daemon`/session runtime — see link.channel.v2.json#/$defs/statusItem for that, delivered on a separate push. The synthetic `virtual` pseudo-connector also uses this exact shape (kind:"virtual") — see link.channel.v2.json. `$defs/sharedFields` is the single source of the fields link.admin.v1.json reuses (via $ref) so the two views can't drift apart independently. `$defs/setInputShared` is the same for set() payloads.
    """

    schema: Literal["afbws.link.user.v1"]


class LinkV2Delete(TypedDict):
    """
    Request (`request_id`, no `rejected`): `ids[]`, at least one. Response (same `request_id`, `rejected` present): `ids[]` actually removed (possibly empty) + `rejected[]`. Push (no `request_id`): `ids[]` (at least one) removed from the registry — drop by `bf_id`; `rejected` is not allowed.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.delete.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    ids: list[Id]
    rejected: NotRequired[list[LinkV2Rejection]]


LinkV2Entity: TypeAlias = LinkUserV1 | LinkAdminV1


class LinkV2Error(TypedDict):
    """
    Per-element failures of a batched operation are reported in that response's `rejected[]`, not here. `code` is the closed common errorCode set.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.error.v2"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str
    details: NotRequired[dict[str, Any]]


class LinkV2List(TypedDict):
    """
    Request (`request_id`, no `items`): optional `scope` (usable = default, working accounts the caller may trade on incl. virtual; admin = full registry as admin views, managers only) and `ids[]` filter (none = all of the scope). Response (same `request_id`): `items[]` (afbws.link.user.v1 | afbws.link.admin.v1, role-chosen). Push (no `request_id`, server-initiated): `items[]` (at least one) created/changed connectors — upsert by `bf_id`, never a snapshot; removal is `afbws.link.delete.v2` push. The first list/status request subscribes the connection to link pushes. There is no separate `get`: use `ids`.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.list.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    scope: NotRequired[Literal["usable", "admin"]]
    ids: NotRequired[list[Id]]
    items: NotRequired[list[LinkV2Entity]]


class LinkV2Pair1(TypedDict):
    """
    Request: `ids[]`, at least one (manager or owner; the virtual connector is rejected with `unsupported_action`). Response (same `request_id`): `items[]` — one `{id, item, pairing_string, expires_at}` per started pairing + `rejected[]`. No server push.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.pair.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: list[Id]
    items: NotRequired[list[LinkV2PairItem]]
    rejected: NotRequired[list[LinkV2Rejection]]


class LinkV2Pair2(TypedDict):
    """
    Request: `ids[]`, at least one (manager or owner; the virtual connector is rejected with `unsupported_action`). Response (same `request_id`): `items[]` — one `{id, item, pairing_string, expires_at}` per started pairing + `rejected[]`. No server push.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.pair.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: NotRequired[list[Id]]
    items: list[LinkV2PairItem]
    rejected: list[LinkV2Rejection]


LinkV2Pair: TypeAlias = LinkV2Pair1 | LinkV2Pair2


class LinkV2PairItem(TypedDict):
    id: str
    item: LinkV2Entity
    pairing_string: str
    expires_at: str


class LinkV2Rejection(TypedDict):
    """
    `item` (the current authoritative record) is only allowed with code `conflict`.
    """

    id: str
    code: AfbwsCommonV1ErrorCode
    message: NotRequired[str]
    details: NotRequired[dict[str, Any]]
    item: NotRequired[LinkV2Entity]


class LinkV2Restart(TypedDict):
    """
    Request: explicit `ids[]`, at least one — never implicitly picks the first accessible BF. Response (same `request_id`): `ids[]` for which the restart command was sent + `rejected[]`. No server push.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.restart.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: list[Id]
    rejected: NotRequired[list[LinkV2Rejection]]


class LinkV2Session(TypedDict):
    account_id: str
    dry_run: bool | None
    capabilities: dict[str, Any]


class LinkV2Set(TypedDict):
    """
    Request (`request_id`, no `rejected`): `items[]` of role-chosen set input, at least one. Response (same `request_id`, `rejected` present): applied `items[]` (authoritative records, possibly empty) + `rejected[]` (per-item failures; `conflict` carries the current `item`). Push (no `request_id`): `items[]` (at least one) created/changed on the server's own initiative — upsert by `bf_id`; `rejected` is not allowed.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.set.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    items: list[LinkV2Entity | LinkV2SetInput]
    rejected: NotRequired[list[LinkV2Rejection]]


LinkV2SetInput: TypeAlias = LinkUserSetInput | LinkAdminSetInput


class LinkV2Status(TypedDict):
    """
    Request (`request_id`, no `items`): optional `ids[]` (none = every connector visible in the caller's usable view). Response (same `request_id`): `items[]` of status records (afbws.link.state.v2). Push (no `request_id`): `items[]` (at least one) of ONLY the statuses that changed — repeated heartbeats without a state change produce no push. `updated_at` of a record is the moment of its last state change. The first list/status request subscribes the connection to pushes.
    """

    channel: Literal["link"]
    schema: Literal["afbws.link.status.v2"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    ids: NotRequired[list[Id]]
    items: NotRequired[list[LinkV2StatusItem]]


LinkChannelV2Message: TypeAlias = (
    LinkV2List
    | LinkV2Set
    | LinkV2Delete
    | LinkV2Pair
    | LinkV2Restart
    | LinkV2Status
    | LinkV2Error
)


class LinkV2StatusItem(TypedDict):
    """
    Runtime-only BF status — never carries name/broker/ACL/keys/policy/config, see link.user.v1.json/link.admin.v1.json for that. `updated_at` is the moment of the LAST STATE CHANGE (connected, heartbeat_stale, broker/daemon/session state), NOT of the last heartbeat: repeated session.heartbeat without any change neither move `updated_at` nor produce a push. There are no heartbeat timestamp/interval fields — the client only needs `heartbeat_stale`. `daemon` is null until the first daemon.status after connect; `session` is null whenever `connected` is false (disconnect resets both).
    """

    schema: Literal["afbws.link.state.v2"]
    bf_id: str
    connected: bool
    heartbeat_stale: bool
    updated_at: str
    daemon: DaemonStatusPayload | None
    session: LinkV2Session | None


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
    deal_seq: NotRequired[int]
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
    deal_seq: NotRequired[int]
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


class Participants(TypedDict):
    use_recommended: NotRequired[bool]
    collection_colors: NotRequired[bool]
    size_by_volume: NotRequired[bool]


class PayloadsBrokerAccountsAccount(TypedDict):
    account_id: str
    tradable: bool
    readonly: bool
    status: Literal["ok", "stale", "error"]
    equity: str | None
    cash: list[PayloadsBrokerAccountsCashBalance]
    positions: list[PayloadsBrokerAccountsPosition]
    broker_fees: NotRequired[list[PayloadsBrokerAccountsBrokerFee]]


class PayloadsBrokerAccountsBrokerFee(TypedDict):
    date: str
    value: str
    currency: str
    transaction_id: NotRequired[str]


class PayloadsBrokerAccountsCashBalance(TypedDict):
    currency: str
    value: str


class PayloadsBrokerAccountsPosition(TypedDict):
    quantity: int
    average_price: str
    current_price: NotRequired[str | None]
    unrealized_pnl: NotRequired[str | None]
    broker_ref: BrokerRef


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


class PayloadsDealRejectedBrokerError(TypedDict):
    """
    Structured broker error behind the rejection. BF sends it only for USER-kind errors (those that must reach the user). Dictionary of `kind` is part of the contract: the frontend picks the user text by it. DAEMON-kind errors (unavailable, timeout, rate_limited, session_closed, trading_halted, auction_only, auth_expired) are handled by the BF daemon itself, never become a rejection and are never sent here. `native_code`/`native_message` are exactly as the broker returned them, unprocessed.
    """

    kind: str
    native_code: NotRequired[str | None]
    native_message: NotRequired[str | None]


class Plans(TypedDict):
    statuses: NotRequired[list[str]]


class Plans1(TypedDict):
    auto_execute: NotRequired[bool]
    editor_left: NotRequired[bool]
    hide_on_share: NotRequired[bool]
    risk_top: NotRequired[bool]


class Position(TypedDict):
    symbol: NotRequired[str]
    quantity: NotRequired[int]
    average_price: NotRequired[str]
    updated_at: NotRequired[str]


class PositionOpenedPayload(TypedDict):
    deal_seq: NotRequired[int]
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


class Primitives(TypedDict):
    confirm_delete: NotRequired[bool]


class ScreenerV1Error(TypedDict):
    channel: Literal["screener"]
    schema: Literal["afbws.screener.error.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    code: AfbwsCommonV1ErrorCode
    message: str


class ScreenerV1Get(TypedDict):
    """
    Request carries `id` (export id or alias). Response echoes the concrete `id` (aliases resolved) and `kind`, and carries `document`: the export content as is (contract v1), an open object. Unknown export: error `not_found`; malformed id: `invalid_schema`; unreadable file: `internal_error`; unsupported `contract_version`: `unsupported_action`.
    """

    channel: Literal["screener"]
    schema: Literal["afbws.screener.get.v1"]
    request_id: AfbwsCommonV1RequestId
    id: AfbwsScreenerChannelV1ExportRef
    kind: NotRequired[AfbwsScreenerChannelV1ExportKind]
    document: NotRequired[Document]


class ScreenerV1List(TypedDict):
    """
    Request carries only optional filters. Response carries `items` (newest first) and the ids of the newest exports: `latest` (newest night export) and `intraday_latest` (newest intraday snapshot), each null when there is none. Both are computed from file names, not from the screener's latest*.json copies.
    """

    channel: Literal["screener"]
    schema: Literal["afbws.screener.list.v1"]
    request_id: AfbwsCommonV1RequestId
    kind: NotRequired[AfbwsScreenerChannelV1ExportKind]
    limit: NotRequired[int]
    items: NotRequired[list[AfbwsScreenerChannelV1ListItem]]
    latest: NotRequired[str | None]
    intraday_latest: NotRequired[str | None]


class ScreenerV1Participants(TypedDict):
    """
    Request is an empty command (no parameters in this version; `request_id` is required). Response carries `received_at`, `tz`, `collections`, `derivatives` (reference table) and `lists` (four columnar snapshots: now, d1, d2, w1). Server push: after each refresh of the FORTS positions (about every 5 minutes) the backend sends the same message with the full body and WITHOUT `request_id` to every connection that has requested `participants` at least once; there is no unsubscribe, the subscription ends with the connection. Access: tier `manager` or `user`, otherwise `forbidden`. Non-manager sees only derivatives visible to their tier.
    """

    channel: Literal["screener"]
    schema: Literal["afbws.screener.participants.v1"]
    request_id: NotRequired[AfbwsCommonV1RequestId]
    received_at: NotRequired[str]
    tz: NotRequired[str]
    collections: NotRequired[list[ScreenerV1ParticipantsCollection]]
    derivatives: NotRequired[ScreenerV1ParticipantsDerivatives]
    lists: NotRequired[list[ScreenerV1ParticipantsList]]


ScreenerChannelV1Message: TypeAlias = (
    ScreenerV1List | ScreenerV1Get | ScreenerV1Participants | ScreenerV1Error
)


class ScreenerV1ParticipantsCollection(TypedDict):
    """
    Root catalog collection (color source for the bubbles).
    """

    id: str
    name: str
    color: AfbwsScreenerChannelV1FavoriteColor | None


class ScreenerV1ParticipantsDerivatives(TypedDict):
    """
    Derivative reference table (columnar, like afbws.market.series.v1 tables): `columns` start with `derivative` (e.g. `MISX:Si`) and may list any subset of the other fields; read by column name. `name`; `active_instrument_key` = nearest unexpired contract (to open a chart); `collection_id` references `collections[].id` (null = no collection). Shared by all four lists.
    """

    columns: list[
        Literal["derivative"]
        | Literal["derivative", "name", "active_instrument_key", "collection_id"]
    ]
    rows: list[list[float | str | None]]


class ScreenerV1ParticipantsList(TypedDict):
    """
    One snapshot. `rows` are columnar (`columns` begin with `derivative`; the other columns are a subset of the fiz_/yur_ position fields, openinterest and volume). Only derivatives that have data in this snapshot get a row; the rest are absent (join with `derivatives` by key). `source`: `intraday` if at least one row is the intraday slot of the day, otherwise `daily`. `price` = price of the derivative's active contract (`derivatives.active_instrument_key`): the last quote for `now` when `trading_day` is today, otherwise the close of the last 5-minute slot of `trading_day`; null when there is no price. The same contract is used in all four lists, so price changes between lists are comparable.
    """

    key: Literal["now", "d1", "d2", "w1"]
    trading_day: str
    asof: str
    source: Literal["intraday", "daily"]
    columns: list[
        Literal["derivative"]
        | Literal[
            "derivative",
            "fiz_long",
            "fiz_short",
            "fiz_net",
            "fiz_persons_long",
            "fiz_persons_short",
            "yur_long",
            "yur_short",
            "yur_net",
            "yur_persons_long",
            "yur_persons_short",
            "openinterest",
            "volume",
            "price",
        ]
    ]
    rows: list[list[float | str | None]]


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
    features: NotRequired[dict[str, Any]]


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
    deals: NotRequired[dict[str, Deals1]]
    deal_revisions: NotRequired[dict[str, int]]
    deal_statuses: NotRequired[dict[str, str]]


class Sort(TypedDict):
    column: NotRequired[str]
    direction: NotRequired[Literal["asc", "desc"]]


class Subscription(TypedDict):
    dataset_id: Literal["positions", "orders", "hhi", "trades"]
    instrument: DealInstrument


class TradePlanV21(TypedDict):
    """
    AFB-side multi-entry / multi-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v2. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `direction` (long/short) is the single source of truth for position bias, at plan level — entry legs do not carry a per-leg side (a list of entries with independent buy/sell sides has no defined execution semantics for one deal). Conditions are deal.v2-compatible nodes — price legs carry an explicit `op` (touch/above/below/breakout/breakdown/crossing), `op` omitted on a price leg means touch (accepted for back-compat with old plans); indicator legs may omit `op`, derived from direction/scope at compile time — with two extensions beyond condition.v1.json's plain vocabulary: (1) the `right` side of a condition may be a `primitiveRef` (`{"primitive_id": "..."}`), a reference to a chart line primitive that AFB resolves to a decimal `const` at compile time; (2) an entry leg's `left` may be `condition.v1.json#/$defs/immediateExpr` (`{"source": "immediate"}`) for a market entry — `right`/`op` are structural placeholders in that case, same convention as the compiled deal (see deal.v2.json's conditionNode, immediate branch of condition.v1.json#/$defs/conditionNode): dispatch on `left.source == "immediate"` alone, never read `right`/`op`. Meaningful only on entries — AFB/BF reject it on stop_loss/take_profit. The full left/right pairing matrix (price/quote const-only, indicator/dataset const-or-same-kind) is enforced after compilation by deal.v2.json and by BF, not here — this schema deliberately stays loose to accommodate primitiveRef and immediateExpr. Each leg additionally carries an optional `logic` (`split`/`and`/`or`, see deal.v2.json#/$defs/legJoin for the full grammar) joining it to the preceding leg; AFB carries the field through compilation unchanged onto the corresponding deal.v2 leg.
    """

    id: TradeplanId
    ticker: str
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    status: NotRequired[Literal["draft", "published", "completed", "archived"]]
    editor: NotRequired[Literal["simple", "advanced"]]
    direction: Literal["long", "short"]
    schema: Literal["afb.tradeplan.v2"]
    activated_at: NotRequired[str]
    closed_at: NotRequired[str]
    archived_at: NotRequired[str]
    instrument_missing: NotRequired[bool]
    entries: list[TradeplanV2TpLeg]
    stop_loss: NotRequired[TradeplanV2TpExitList]
    take_profit: NotRequired[TradeplanV2TpExitList]
    sizing: DealSizing
    publish: NotRequired[TradeplanV2Publish]
    connector: NotRequired[str]
    account_id: NotRequired[str]
    delivery_at: NotRequired[str]
    archived_components: NotRequired[TradeplanV2ArchivedComponents]
    deal_id: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


class TradePlanV22(TypedDict):
    """
    AFB-side multi-entry / multi-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v2. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `direction` (long/short) is the single source of truth for position bias, at plan level — entry legs do not carry a per-leg side (a list of entries with independent buy/sell sides has no defined execution semantics for one deal). Conditions are deal.v2-compatible nodes — price legs carry an explicit `op` (touch/above/below/breakout/breakdown/crossing), `op` omitted on a price leg means touch (accepted for back-compat with old plans); indicator legs may omit `op`, derived from direction/scope at compile time — with two extensions beyond condition.v1.json's plain vocabulary: (1) the `right` side of a condition may be a `primitiveRef` (`{"primitive_id": "..."}`), a reference to a chart line primitive that AFB resolves to a decimal `const` at compile time; (2) an entry leg's `left` may be `condition.v1.json#/$defs/immediateExpr` (`{"source": "immediate"}`) for a market entry — `right`/`op` are structural placeholders in that case, same convention as the compiled deal (see deal.v2.json's conditionNode, immediate branch of condition.v1.json#/$defs/conditionNode): dispatch on `left.source == "immediate"` alone, never read `right`/`op`. Meaningful only on entries — AFB/BF reject it on stop_loss/take_profit. The full left/right pairing matrix (price/quote const-only, indicator/dataset const-or-same-kind) is enforced after compilation by deal.v2.json and by BF, not here — this schema deliberately stays loose to accommodate primitiveRef and immediateExpr. Each leg additionally carries an optional `logic` (`split`/`and`/`or`, see deal.v2.json#/$defs/legJoin for the full grammar) joining it to the preceding leg; AFB carries the field through compilation unchanged onto the corresponding deal.v2 leg.
    """

    id: TradeplanId
    ticker: NotRequired[str]
    instrument_key: AfbwsCommonV1InstrumentKey
    status: NotRequired[Literal["draft", "published", "completed", "archived"]]
    editor: NotRequired[Literal["simple", "advanced"]]
    direction: Literal["long", "short"]
    schema: Literal["afb.tradeplan.v2"]
    activated_at: NotRequired[str]
    closed_at: NotRequired[str]
    archived_at: NotRequired[str]
    instrument_missing: NotRequired[bool]
    entries: list[TradeplanV2TpLeg]
    stop_loss: NotRequired[TradeplanV2TpExitList]
    take_profit: NotRequired[TradeplanV2TpExitList]
    sizing: DealSizing
    publish: NotRequired[TradeplanV2Publish]
    connector: NotRequired[str]
    account_id: NotRequired[str]
    delivery_at: NotRequired[str]
    archived_components: NotRequired[TradeplanV2ArchivedComponents]
    deal_id: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


TradePlanV2: TypeAlias = TradePlanV21 | TradePlanV22


TradeplanId: TypeAlias = str


class TradeplanV2AmendResultItem(TypedDict):
    """
    One row per deal of an applied plan; `tradeplan_id` names that plan, so a batch `set` response can be matched without guessing. accepted=true: the deal was amended, `revision` is its new revision (integer; null only if the deal did not report one) and `status` its status after the amend. accepted=false: the deal is unchanged, `message` says why (a human-readable gate/validation text) and `code` is set only for the one machine-readable case the server distinguishes: `tradeplan_missing` (the deal's own tradeplan no longer exists — an orphaned deal). `revision`/`status` never appear on a rejection.
    """

    schema: Literal["afbws.tradeplan.amend_result.v2"]
    tradeplan_id: TradeplanId
    deal_id: str
    accepted: bool
    revision: NotRequired[int | None]
    status: NotRequired[DealStatus]
    message: NotRequired[str]
    code: NotRequired[Literal["tradeplan_missing"]]


class TradeplanV2Archive1(TypedDict):
    """
    Request: `ids[]` (at least one). Response (same `request_id`): `items[]` — the archived plans (status `archived`) — and `rejected[]` (a plan with a live deal that already entered a position is rejected with `conflict` and its current `item`). Exactly one of `ids` / `items`. Archival is also delivered as a single `sync` push (all archived plans in one message) to the user's other connections.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.archive.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: list[TradeplanId]
    items: NotRequired[list[TradeplanV2PlanItem]]
    rejected: NotRequired[list[TradeplanV2Rejection]]


class TradeplanV2Archive2(TypedDict):
    """
    Request: `ids[]` (at least one). Response (same `request_id`): `items[]` — the archived plans (status `archived`) — and `rejected[]` (a plan with a live deal that already entered a position is rejected with `conflict` and its current `item`). Exactly one of `ids` / `items`. Archival is also delivered as a single `sync` push (all archived plans in one message) to the user's other connections.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.archive.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: NotRequired[list[TradeplanId]]
    items: list[TradeplanV2PlanItem]
    rejected: NotRequired[list[TradeplanV2Rejection]]


TradeplanV2Archive: TypeAlias = TradeplanV2Archive1 | TradeplanV2Archive2


class TradeplanV2ArchivedComponents(TypedDict):
    """
    Server-owned storage field, written once when the plan is archived: a self-contained snapshot of the chart components the plan used (the plan's own line primitives — physically removed from the live gp store on archive — and the indicators its conditions reference), so an archived plan keeps its historical drawing without depending on gp. Items are copies of AFB's internal gp/indicator storage records, deliberately not formalized here (they are never sent to clients; the channel drops this field). Re-archiving an archived plan carries the snapshot forward unchanged.
    """

    primitives: list[dict[str, Any]]
    indicators: list[dict[str, Any]]


class TradeplanV2Condition(TypedDict):
    """
    Same vocabulary as ../tradeplan.v2.json#/$defs/tpConditionNode (price/indicator/dataset/immediate left side, const/indicator/dataset/primitive_id right side, timeframe, duration — the same shared defs) with `op` required: the storage schema tolerates a price leg without `op` (old stored files; means `touch`), the channel does not — the frontend always sends `op`, the server fills `touch` on output for such stored legs.
    """

    id: NotRequired[str]
    op: TradeplanV2ConditionOp
    timeframe: NotRequired[ConditionV1Timeframe]
    duration: NotRequired[ConditionV1Duration]
    left: TradeplanV2ConditionLeft
    right: TradeplanV2ConditionRight


TradeplanV2ConditionLeft: TypeAlias = (
    ConditionV1PriceExpr
    | ConditionV1IndicatorExpr
    | ConditionV1DatasetExpr
    | ConditionV1ImmediateExpr
)


TradeplanV2ConditionOp: TypeAlias = Literal[
    "touch",
    "above",
    "below",
    "crosses_above",
    "crosses_below",
    "crossing",
    "breakout",
    "breakdown",
]


class TradeplanV2Delete(TypedDict):
    """
    Request: `ids[]` (at least one). Response (same `request_id`): `ids[]` actually deleted (possibly empty) + `rejected[]`. Allowed only for a plan that never had a deal; otherwise that plan is rejected with `conflict` (use archive). The deletion is NOT pushed.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.delete.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: list[TradeplanId]
    rejected: NotRequired[list[TradeplanV2Rejection]]


class TradeplanV2Error(TypedDict):
    """
    Per-plan failures of a batched set/delete/archive are reported in that response's `rejected[]`, not here.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.error.v2"]
    request_id: AfbwsCommonV1RequestId
    code: AfbwsCommonV1ErrorCode
    message: str


class TradeplanV2LegInput(TypedDict):
    """
    `leg_id` is optional on input: a new leg has none, the server assigns one on save (existing ids are never reassigned). `percent`/`logic` — see ../deal.v2.json#/$defs/legJoin.
    """

    leg_id: NotRequired[LegId]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: TradeplanV2Condition


class TradeplanV2LegItem(TypedDict):
    leg_id: LegId
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: TradeplanV2Condition


class TradeplanV2List(TypedDict):
    """
    Request: optional filters `ids[]` and/or `instrument_keys[]` (both = intersection; none = every non-archived plan of the caller; archived plans are returned only when named in `ids`). Response (same `request_id`): `items[]`. There is no separate `get`: use `ids`. A request carrying `items` is invalid, as is a response carrying a filter.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.list.v2"]
    request_id: AfbwsCommonV1RequestId
    ids: NotRequired[list[TradeplanId]]
    instrument_keys: NotRequired[list[AfbwsCommonV1InstrumentKey]]
    items: NotRequired[list[TradeplanV2PlanItem]]


class TradeplanV2PlanInput(TypedDict):
    """
    Deliberately has NO server-owned fields: `status` (lifecycle is driven by the plan's deals), `activated_at`, `closed_at`, `archived_at`, `created_at`, `updated_at`, `delivery_at`, `archived_components`, `instrument_missing`; the server keeps them from its own storage (a create starts as `draft`). `ticker` is not accepted either: it is derived by the server from `instrument_key`, the authoritative instrument reference (case-sensitive, never normalized). `editor` (frontend editor-mode hint) is not part of the channel: the current frontend neither sends nor reads it.
    """

    schema: Literal["afb.tradeplan.v2"]
    id: TradeplanId
    instrument_key: AfbwsCommonV1InstrumentKey
    direction: Literal["long", "short"]
    entries: list[TradeplanV2LegInput]
    stop_loss: list[TradeplanV2LegInput]
    take_profit: list[TradeplanV2LegInput]
    sizing: DealSizing
    publish: NotRequired[TradeplanV2Publish]


class TradeplanV2PlanItem(TypedDict):
    """
    An allow-list projection of the stored plan. `status` is the plan lifecycle (draft -> published -> completed, + archived manually). `activated_at`/`closed_at`/`created_at`/`updated_at` are market-time ISO strings, `activated_at`/`closed_at` may be empty. Instrument: `instrument_key` is present whenever the server could resolve one; a plan whose instrument is not in the catalog comes with `instrument_missing: true` (and possibly without `ticker`) — at least one of the two is always there. `ticker` is the derived wire ticker. Never returned: `delivery_at`, `archived_components`, `archived_at`, `editor`.
    """

    schema: Literal["afb.tradeplan.v2"]
    id: TradeplanId
    ticker: NotRequired[str]
    instrument_key: NotRequired[AfbwsCommonV1InstrumentKey]
    instrument_missing: NotRequired[Literal[True]]
    direction: Literal["long", "short"]
    status: Literal["draft", "published", "completed", "archived"]
    entries: list[TradeplanV2LegItem]
    stop_loss: list[TradeplanV2LegItem]
    take_profit: list[TradeplanV2LegItem]
    sizing: DealSizing
    publish: NotRequired[TradeplanV2Publish]
    activated_at: str
    closed_at: str
    created_at: str
    updated_at: str


class TradeplanV2PrimitiveRef(TypedDict):
    primitive_id: str


TradeplanV2ConditionRight: TypeAlias = (
    ConditionV1RightConst
    | ConditionV1IndicatorExpr
    | ConditionV1DatasetExpr
    | TradeplanV2PrimitiveRef
)


class TradeplanV2Publish(TypedDict):
    """
    Параметры публикации плана (используется ТОЛЬКО при публикации, не хранит связь с сделкой). bf_id — коннектор по умолчанию для UI; истина при публикации — bf_id из afbws.deal.publish.request.v1. account_id пусто/отсутствует — дефолтный (торговый) счёт коннектора, резолвится на лету (ExecutionService.resolve_plan_account).
    """

    bf_id: NotRequired[str]
    account_id: NotRequired[str]


class TradeplanV2Rejection(TypedDict):
    """
    `id` is the plan id from the request, `code` a whole-request error code reused per plan (`not_found`, `validation_error`, `conflict`, ...), `message` the human-readable reason. `item` is the authoritative current plan and is present only with `conflict` (a stale or blocked plan: archive/delete blocked by a live deal that already entered a position, `set` over a primitive owned by another plan), so the client can adopt it without a separate read; a `conflict` may also come without it.
    """

    id: TradeplanId
    code: AfbwsCommonV1ErrorCode
    message: str
    item: NotRequired[TradeplanV2PlanItem]


class TradeplanV2Set(TypedDict):
    """
    Request: `items[]` (at least one) of `planInput` — create or update by `item.id`, batched. Response (same `request_id`): `items[]` the applied authoritative `planItem`s (possibly empty), `rejected[]` for plans that were not applied (a stale/conflicting plan carries its current `planItem` in `rejected[].item`), and `amend_results[]` — the per-deal outcome of re-amending the live deals of every applied plan (empty for creates only; each row names its `tradeplan_id`). Distinguished by `amend_results`: present => response, absent => request. A failing plan never fails the batch. There is no push on set.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.set.v2"]
    request_id: AfbwsCommonV1RequestId
    items: list[TradeplanV2PlanInput | TradeplanV2PlanItem]
    rejected: NotRequired[list[TradeplanV2Rejection]]
    amend_results: NotRequired[list[TradeplanV2AmendResultItem]]


class TradeplanV2Sync(TypedDict):
    """
    `items[]` (at least one) is a DELTA, not a snapshot: the client upserts plans in its own list by matching id and leaves everything else untouched. The authoritative full list comes only from afbws.tradeplan.list.v2. Sent on plan lifecycle changes (status derived from its deals) and archival (one push per batch). Plan deletion and `set` are NOT conveyed by this push. Never a request: `request_id` is not allowed.
    """

    channel: Literal["tradeplan"]
    schema: Literal["afbws.tradeplan.sync.v2"]
    items: list[TradeplanV2PlanItem]


TradeplanChannelV2Message: TypeAlias = (
    TradeplanV2List
    | TradeplanV2Set
    | TradeplanV2Delete
    | TradeplanV2Archive
    | TradeplanV2Sync
    | TradeplanV2Error
)


class TradeplanV2TpConditionNode(TypedDict):
    id: NotRequired[str]
    op: NotRequired[TradeplanV2ConditionOp]
    timeframe: NotRequired[ConditionV1Timeframe]
    duration: NotRequired[ConditionV1Duration]
    left: TradeplanV2ConditionLeft
    right: TradeplanV2ConditionRight


class TradeplanV2TpLeg(TypedDict):
    leg_id: NotRequired[LegId]
    percent: NotRequired[DecimalString]
    logic: NotRequired[DealV2LegJoin]
    condition: TradeplanV2TpConditionNode


TradeplanV2TpExitList: TypeAlias = list[TradeplanV2TpLeg]


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

