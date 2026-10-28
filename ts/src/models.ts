/**
 * DO NOT EDIT BY HAND — generated from spec/schemas/ (all *.json files) by
 * ts/tools/generate-models.mjs (invoked via `afb-bf-protocol-generate`).
 * source-hash: 78cfe2bf3a742bfcbb3216b195ee16d6eb93da33888ab08e7b1c1e731bff6fad
 */

/**
 * Negotiated via auth.support (capability id afbws.access.channel.v1). Freemium access model: tier (who) x capabilities (personal permissions) x mode (what is available now), see common.v1.json#/$defs/access. Messages mirror the backend's access database (tables tiers, members, users, subscriptions). Same convention as afbws.link/afbws.screener: ONE schema id per operation (`afbws.access.<op>.v1`, no .request/.response suffixes); the same schema is the request and its response (echoes `request_id`); response-only fields are forbidden in a request. `request_id` is required in every client request. Operations (manager only, others get error `forbidden`): `roles.get`/`roles.set` (tiers and members; replace the config-channel op `roles`), `users.list`, `user.set` (trial end / manual grant), `stats` (weekly conversion). Server-initiated: push `afbws.access.state.v1` (no `request_id`) and `afbws.access.denied.v1` — the gate's refusal of a request of ANY channel (sent on the refused request's channel, with its `request_id`). Whole-request failures of this channel: `afbws.access.error.v1`. See AFB/docs/ws/access.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessChannelV1Message".
 */
export type AccessChannelV1Message =
  | AccessV1RolesGet
  | AccessV1RolesSet
  | AccessV1UsersList
  | AccessV1UserSet
  | AccessV1Stats
  | AccessV1State
  | AccessV1Denied
  | AccessV1Error;
/**
 * Client-generated correlation id (e.g. uuid4), echoed verbatim in the matching response.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCommonV1_RequestId".
 */
export type AfbwsCommonV1_RequestId = string;
/**
 * Tier name (axis 1 of the access model): who the user is. An open set defined by DATA (rows of the backend's `tiers` table: e.g. `manager`, `user`, `guest`, a new paid tier `lite`), NOT an enum: a new tier needs no protocol change. Only `manager` is reserved by code (staff, manager functions gated on `tier == manager` independently of `mode`). Comes from tier members (GetCourse groups, user ids) in the backend's access database; the tier with the minimal rank is the default for users not matched by any member.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessTier".
 */
export type AccessTier = string;
/**
 * Three independent axes. (1) `tier` — WHO the user is (a tier name, open set defined by data; manager functions are gated on `tier == manager` only). (2) `capabilities` — personal permissions granted by a manager, orthogonal to tier (`trade` — real trading through BF, `virtual`, `screener`, `local`); holding `trade` ALWAYS yields `mode: full` (`reason: subscription`): real trading is never held because of a window, a trial or an ended subscription. (3) `mode` — WHAT is available NOW (`full`/`basic`); logic is decided only by `mode`, while `reason` and `until` are for display (refusal texts, indicator) and statistics. `until` is the moment of the next mode change known to the server (end of trial/grant/window, start of the next window), null when none is scheduled; the server pushes afbws.access.state.v1 when the mode actually changes.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "Access".
 */
export type Access = {
  [k: string]: unknown;
} & {
  tier: AccessTier;
  /**
   * Personal capability names (`trade`, `virtual`, `screener`, `local`; the set is defined by the backend code).
   */
  capabilities: string[];
  limits: AccessLimits;
  mode: AccessMode;
  reason: AccessReason;
  /**
   * Next known mode change, ISO-8601 with offset; null — none scheduled.
   */
  until: string | null;
};
/**
 * What is available right now (axis 3 of the access model): `full` — paid features work; `basic` — paid features are refused with afbws.access.denied.v1 and the user's alarms/trade plans are held (not evaluated). ALL access logic is decided by `mode` alone; `reason`/`until` are display/statistics only.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessMode".
 */
export type AccessMode = 'full' | 'basic';
/**
 * Why the current `mode` holds — display/statistics only, never used for logic. `subscription` — paid tier or the `trade` capability (or a tier without a mode policy); `grant` — manual extension by a manager; `trial` — trial period; `window` — inside the workday/weekend time window of the tier policy; `none` — no reason for `full` (always so in `basic`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessReason".
 */
export type AccessReason = 'subscription' | 'grant' | 'trial' | 'window' | 'none';
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.account.channel.v2). Same convention as afbws.alarm.v2/afbws.market: ONE schema id per message (`afbws.account.<op>.v2`, no .request/.response/.push suffixes); the same schema is the request, its response (echoes `request_id`) and, for `list`/`orders`, the server push (a message WITHOUT `request_id`). `events` has no push; `error` is the single typed error. Operations: list, orders, events, error; `list` takes `bf_id` + `account_id`. `items` are explicit allow-list projections built by backend/trade/public_views.py (never a verbatim proxy of a BF broker.* payload); $defs accountSnapshot/order/eventRecord are this file's own strict shapes , reusing only the field-level $defs of payloads/broker.accounts.json. A multi-currency account is expressed through cash[] (one entry per currency); the virtual account fills `as_of`. `account` means a broker account (one bf_id may have more than one), not the connector itself.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountChannelV2Message".
 */
export type AccountChannelV2Message = AccountV2List | AccountV2Orders | AccountV2Events | AccountV2Error;
/**
 * Request (`request_id`, no `items`): optional `bf_id` (only that connector's accounts; omitted = every account of every accessible connector), optional `account_id` (a single account; use together with `bf_id`; replaces v1 `get`), optional `force` (bypass the cached BfRuntimeState.accounts snapshot and re-fetch from BF). Response (same `request_id`, with `items`): only `request_id` + `items[]` (accountSnapshot, possibly empty). Push (no `request_id`, server-initiated): the full account list of ONE `bf_id` — `bf_id`, `default_account_id`, `items[]` (BF's broker.accounts is a full snapshot, never a delta; the virtual account is pushed the same way). A request carrying `items`/`default_account_id` or a response/push carrying request-only fields is invalid.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2List".
 */
export type AccountV2List = {
  [k: string]: unknown;
} & {
  channel: 'account';
  schema: 'afbws.account.list.v2';
  request_id?: AfbwsCommonV1_RequestId;
  bf_id?: AccountV2BfId;
  account_id?: AccountV2AccountId;
  /**
   * Request only: bypass the cached accounts snapshot and re-fetch from BF.
   */
  force?: boolean;
  default_account_id?: AccountV2AccountId;
  items?: AccountV2Snapshot[];
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2BfId".
 */
export type AccountV2BfId = string;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2AccountId".
 */
export type AccountV2AccountId = string;
/**
 * Request (`request_id`, no `items`): `bf_id` required; `account_id` omitted = the connector's default (trading) account (the only account order history is available for, see payloads/broker.orders.json). Response (same `request_id`, with `items`): `bf_id`, `account_id`, `items[]`. Push (no `request_id`, server-initiated): `bf_id`, `account_id`, `items[]` for the default (trading) account.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2Orders".
 */
export type AccountV2Orders = {
  [k: string]: unknown;
} & {
  channel: 'account';
  schema: 'afbws.account.orders.v2';
  request_id?: AfbwsCommonV1_RequestId;
  bf_id: AccountV2BfId;
  account_id?: AccountV2AccountId;
  items?: AccountV2Order[];
};
/**
 * Request (`request_id`, no `items`): `bf_id` required, `date` (YYYY-MM-DD market date) omitted = today (market_today()). Response (same `request_id`, with `items`): `bf_id`, `date`, `items[]`. There is NO server push for events: `request_id` is always required.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2Events".
 */
export type AccountV2Events = {
  [k: string]: unknown;
} & {
  channel: 'account';
  schema: 'afbws.account.events.v2';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: AccountV2BfId;
  /**
   * YYYY-MM-DD market date; omitted in a request means today (market_today()).
   */
  date?: string;
  items?: AccountV2EventRecord[];
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCommonV1_ErrorCode".
 */
export type AfbwsCommonV1_ErrorCode =
  | 'not_found'
  | 'invalid_schema'
  | 'invalid_channel'
  | 'validation_error'
  | 'conflict'
  | 'internal_error'
  | 'forbidden'
  | 'bf_offline'
  | 'unsupported_action'
  | 'not_paired'
  | 'superseded'
  | 'busy';
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.alarm.channel.v2). Items are afb.alarm.v2 (`instrument_key` instead of `ticker`). Same convention as afbws.market: ONE schema id per message (`afbws.alarm.<op>.v2`, no .request/.response/.push suffixes); the same schema is the request and its response (a response echoes `request_id`). Collections are arrays (`items[]`, `ids[]`, `instrument_keys[]`), so bulk operations are single messages; partial failures come back in `rejected[]`. `triggered` is the only server push (no `request_id`). See AFB/docs/ENTITY_WS_PROTOCOL.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmChannelV2Message".
 */
export type AlarmChannelV2Message =
  AlarmV2List | AlarmV2Set | AlarmV2Delete | AlarmV2Ack | AlarmV2Triggered | AlarmV2Error;
/**
 * Full composite key identifying one catalog listing or derivative: `<MIC>[:<board|market>]:<ticker>` (e.g. `MISX:TQBR:SBER`, `MISX:RFUD:IMOEXF`), or the venueless 2-segment derivative form `<MIC>:<code>` (e.g. `MISX:IMOEXF`) where the wire explicitly identifies a derivative rather than a listing. Case-sensitive, never normalized (`.lower()`/`.upper()`) on either side of the AFB backend<->frontend channel.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCommonV1_InstrumentKey".
 */
export type AfbwsCommonV1_InstrumentKey = string;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2_AlarmConditionNode".
 */
export type AlarmV2_AlarmConditionNode =
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op?: 'touch';
    }
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op: 'breakout' | 'breakdown' | 'crossing';
      timeframe: ConditionV1_Timeframe;
    }
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op: ConditionV1_PriceLevelOp;
    }
  | {
      left?: AlarmV2_AlarmIndicatorExpr;
      right?: ConditionV1_RightConst | AlarmV2_AlarmIndicatorExpr;
      op: ConditionV1_ScalarOp;
    }
  | {
      left?: ConditionV1_DatasetExpr;
      right?: ConditionV1_RightConst | ConditionV1_DatasetExpr;
      op: ConditionV1_ScalarOp;
    };
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DecimalString".
 */
export type DecimalString = string;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_Timeframe".
 */
export type ConditionV1_Timeframe = '5min' | '10min' | '15min' | '30min' | '1h' | '2h' | '4h' | '1d';
/**
 * Price level check (inclusive): above fires when cur >= level; below when cur <= level.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_PriceLevelOp".
 */
export type ConditionV1_PriceLevelOp = 'above' | 'below';
/**
 * indicator/dataset: above cur > thr, below cur < thr. crosses_above: prev <= prev_thr AND cur > thr. crosses_below: prev >= prev_thr AND cur < thr. crossing: crosses_above OR crosses_below. Price above/below use evaluate_price_level_op (inclusive >= / <=) — see the price level operator branch.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_ScalarOp".
 */
export type ConditionV1_ScalarOp = 'above' | 'below' | 'crosses_above' | 'crosses_below' | 'crossing';
/**
 * Request (`request_id` present): `items[]` — upsert by `item.id`, batched. Response (same `request_id`): applied `items[]` (authoritative records, possibly empty) + `rejected[]` for items that were not applied. Push (no `request_id`, server-initiated): `items[]` (at least one) are authoritative afb.alarm.v2 records that the server created or changed on its own (e.g. alarms moved to another contract by the expiration replace) — upsert by id on the client, never a snapshot; `rejected` is not allowed. Removal is conveyed by `afbws.alarm.delete.v2` without `request_id`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2Set".
 */
export type AlarmV2Set = {
  [k: string]: unknown;
} & {
  channel: 'alarm';
  schema: 'afbws.alarm.set.v2';
  request_id?: AfbwsCommonV1_RequestId;
  items: AlarmV2[];
  rejected?: AlarmV2Rejection[];
};
/**
 * Request (`request_id` present): `ids[]` and/or `instrument_keys[]` (at least one; `instrument_keys` = every alarm of those instruments). Response (same `request_id`): `ids[]` actually removed (possibly empty) + `rejected[]`. Push (no `request_id`): `ids[]` (at least one) removed by the server on its own (e.g. alarms of an expired contract cleaned by the expiration policy); `instrument_keys`/`rejected` are not allowed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2Delete".
 */
export type AlarmV2Delete = {
  [k: string]: unknown;
} & {
  channel: 'alarm';
  schema: 'afbws.alarm.delete.v2';
  request_id?: AfbwsCommonV1_RequestId;
  ids?: string[];
  /**
   * @minItems 1
   */
  instrument_keys?: [AfbwsCommonV1_InstrumentKey, ...AfbwsCommonV1_InstrumentKey[]];
  rejected?: AlarmV2Rejection[];
};
/**
 * Request: `events[]` (afb.alarm.trigger_ack.v2), at least one. Response (same `request_id`): `results[]` — one per event, `status` ok | not_found. A request carrying `results` is invalid.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2Ack".
 */
export type AlarmV2Ack = {
  [k: string]: unknown;
} & {
  channel: 'alarm';
  schema: 'afbws.alarm.ack.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  events?: [AlarmV2AckEvent, ...AlarmV2AckEvent[]];
  results?: AlarmV2AckResultItem[];
};
/**
 * First message of every AFB WebSocket connection, replacing the legacy `{type: "auth"}` / `{type: "auth_ok"}` / `{type: "auth_error"}`. Same convention as the other schema-first afbws channels: routed by `channel` (`auth`) then by a mandatory `schema` id, no `type` field. There is no `request_id`: the handshake is exactly one request and one answer. Negotiation caveat: `support` is learned only from auth.ok, i.e. AFTER the client has already chosen the form of its first message — so the frontend ALWAYS sends afbws.auth.request.v1, and the backend accepts BOTH the legacy `type: "auth"` and this schema, answering in the form of the request (legacy request -> legacy auth_ok/auth_error; schema request -> afbws.auth.ok.v1 / afbws.auth.error.v1). The backend still lists `afbws.auth.v1` in `support` so a client can tell that the backend understands the new form. Removal of the legacy form is a separate decision. See AFB/docs/API_REGISTRY.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AuthV1Message".
 */
export type AuthV1Message = AuthV1Request | AuthV1Ok | AuthV1Error;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BfsRegistryEntry".
 */
export type BfsRegistryEntry = BfRegistryEntry & {
  connected: boolean;
  dry_run: boolean;
  /**
   * @deprecated
   * Deprecated: use dry_run (effective session value) instead.
   */
  dry_run_afb?: boolean;
  /**
   * @deprecated
   * Deprecated: use dry_run (effective session value) instead.
   */
  dry_run_bf?: boolean;
  /**
   * From connected BF's session.hello capabilities; display-only.
   */
  account_id?: string;
  capabilities?: {
    [k: string]: unknown;
  };
  daemon?: {
    [k: string]: unknown;
  };
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.catalog.channel.v1). The asset manager's own channel; replaces the manager half of afbws.instrument (`catalog`, `pool`, `inventory`, `commit`, `refresh`, `sources`), which is left untouched. Same convention as afbws.alarm/afbws.gp/afbws.config: ONE schema id per message (`afbws.catalog.<op>.v1`), the same schema is the request, its response and, for `refresh`, a server push; a message WITHOUT `request_id` is a server push; a failed request is answered with `afbws.catalog.error.v1`. Every non-manager request -> error `forbidden`. Any list is capped at 100 items. Operations: `snapshot`, `symbols`, `support`, `commit`, `refresh`. See AFB/docs/ws/catalog.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Root".
 */
export type AfbwsCatalogChannelV1_Root =
  | AfbwsCatalogChannelV1_Snapshot
  | AfbwsCatalogChannelV1_Symbols
  | AfbwsCatalogChannelV1_Support
  | AfbwsCatalogChannelV1_Commit
  | AfbwsCatalogChannelV1_Refresh
  | AfbwsCatalogChannelV1_Error;
/**
 * Request: only `request_id`. Response (same `request_id`): the state the asset manager edits — ordered collections, global sets, assets with their members, and ONLY the listings / derivatives referenced by assets and global instrument sets (unassigned listings are found through `symbols`). `revision` is the `base_revision` for `commit`. Manager only.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Snapshot".
 */
export type AfbwsCatalogChannelV1_Snapshot = {
  channel: 'catalog';
  schema: 'afbws.catalog.snapshot.v1';
  request_id: AfbwsCommonV1_RequestId;
  revision?: number;
  collections?: AfbwsCatalogChannelV1_Collection[];
  sets?: AfbwsCatalogChannelV1_Set[];
  assets?: AfbwsCatalogChannelV1_SnapshotAsset[];
  listings?: AfbwsCatalogChannelV1_Listing[];
  derivatives?: AfbwsCatalogChannelV1_Derivative[];
  sources?: AfbwsCatalogChannelV1_SourceStatus[];
} & AfbwsCatalogChannelV1_Snapshot1;
/**
 * Same list and order as afbws.instrument.channel.v2 favoriteColor (kept in lockstep; no cross-reference on purpose).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_FavoriteColor".
 */
export type AfbwsCatalogChannelV1_FavoriteColor =
  'yellow' | 'red' | 'blue' | 'green' | 'gray' | 'orange' | 'cyan' | 'purple' | 'pink' | 'teal';
/**
 * Catalog source a symbol list / a new member comes from.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Source".
 */
export type AfbwsCatalogChannelV1_Source = 'moex' | 'finam';
export type AfbwsCatalogChannelV1_Snapshot1 = {
  [k: string]: unknown;
};
/**
 * ONE operation for both sources, answered only from the source's own catalog (Finam: the `finam.db` mirror, MOEX: the pool snapshot) — the broker / exchange is never called. Request: `source`, optional `query` (symbol or name, case-insensitive), `mic`, `kind`, `market`, `include_archived`, `unassigned` (server-side, over the stored state), `limit` (1..100, default 50) and `offset` (default 0): a window of `limit` rows starting at `offset` of the filtered list. Response: `source`, `total` (rows in the whole filtered list), `offset`, `fetched_at`, `items[]` (<=100).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Symbols".
 */
export type AfbwsCatalogChannelV1_Symbols = {
  channel: 'catalog';
  schema: 'afbws.catalog.symbols.v1';
  request_id: AfbwsCommonV1_RequestId;
  source: AfbwsCatalogChannelV1_Source;
  query?: string;
  kind?: 'listing' | 'derivative';
  market?: 'stock' | 'currency' | 'index' | 'futures' | 'other';
  include_archived?: boolean;
  unassigned?: boolean;
  limit?: number;
  total?: number;
  fetched_at?: string | null;
  /**
   * @maxItems 100
   */
  items?: AfbwsCatalogChannelV1_SymbolRow[];
  /**
   * Index of the first requested row in the filtered list (0-based). The client asks for the window that contains the page it shows; there is no cursor.
   */
  offset?: number;
  /**
   * Only rows of this exchange (MIC). Case-sensitive.
   */
  mic?: string;
} & AfbwsCatalogChannelV1_Symbols1;
export type AfbwsCatalogChannelV1_Symbols1 = {
  [k: string]: unknown;
};
/**
 * Request: only `request_id`. Response: `sources` — for each source a dictionary MIC -> categories (`market` values of `symbols`) built from the source's own catalog (Finam: the mirror's active symbols; MOEX: the pool). MOEX is a single exchange (`MISX`). A source that is unavailable is absent. Manager only.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Support".
 */
export type AfbwsCatalogChannelV1_Support = {
  channel: 'catalog';
  schema: 'afbws.catalog.support.v1';
  request_id: AfbwsCommonV1_RequestId;
  sources?: {
    [k: string]: {
      [k: string]: ('stock' | 'currency' | 'index' | 'futures' | 'other')[];
    };
  };
} & AfbwsCatalogChannelV1_Support1;
export type AfbwsCatalogChannelV1_Support1 = {
  [k: string]: unknown;
};
/**
 * Request: the delta relative to the last `snapshot` plus `base_revision` for CAS (stale -> error `conflict`, `details.catalog_revision`). Every array is an upsert by id; `assets[].members` and `sets[].asset_ids|instrument_keys` are the WHOLE composition in final order; `collection_order` / `set_order` are the whole final order of ids. New members are `{kind, source, ref}` only: the backend fetches listing data itself (Finam: GetAsset via the detail cache, at most 20 new Finam instruments per commit). If any new member cannot be accepted NOTHING is applied and the error (`unsupported_type`, `no_market_data`, `not_found`, `source_unavailable`) lists the rows in `details.refs[]`. Response: `revision` and `created[]` (what the new members became); the client re-reads `snapshot`. Manager only.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Commit".
 */
export type AfbwsCatalogChannelV1_Commit = {
  channel: 'catalog';
  schema: 'afbws.catalog.commit.v1';
  request_id: AfbwsCommonV1_RequestId;
  base_revision?: number;
  collections?: AfbwsCatalogChannelV1_Collection[];
  collection_order?: string[];
  remove_collections?: string[];
  sets?: AfbwsCatalogChannelV1_Set[];
  set_order?: string[];
  remove_sets?: string[];
  assets?: AfbwsCatalogChannelV1_Asset[];
  remove_assets?: string[];
  archive?: AfbwsCatalogChannelV1_ArchiveItem[];
  reason?: string;
  revision?: number;
  created?: AfbwsCatalogChannelV1_Created[];
} & AfbwsCatalogChannelV1_Commit1;
/**
 * Three forms. Existing listing `{kind:'listing', ref:<instrument_key>}`; existing derivative `{kind:'derivative', ref:<code>}`; NEW member `{kind, source, ref}` where `ref` is the `ref` of a `symbols` row. A new member NEVER carries listing data: the backend fetches everything itself from the source at commit time.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Member".
 */
export type AfbwsCatalogChannelV1_Member = AfbwsCatalogChannelV1_MemberExisting | AfbwsCatalogChannelV1_MemberNew;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Created".
 */
export type AfbwsCatalogChannelV1_Created = AfbwsCatalogChannelV1_Created1 & {
  source: AfbwsCatalogChannelV1_Source;
  ref: string;
  instrument_key?: AfbwsCommonV1_InstrumentKey;
  derivative?: string;
};
export type AfbwsCatalogChannelV1_Created1 = {
  [k: string]: unknown;
};
export type AfbwsCatalogChannelV1_Commit1 = {
  [k: string]: unknown;
};
/**
 * Does NOT refresh immediately: puts the source into the daily-cycle queue (the same path for `moex` and `finam`). Request: optional `sources[]` (omitted = every available source). Response (same `request_id`): `queued[]`, `already_queued[]`, `rejected[]`. Push (NO `request_id`, manager connections with the capability): the outcome per source — `source`, `state` (`done`|`failed`), `finished_at`, `received`, `summary`, `error`, `revision`, and `states[]` = fresh source statuses (named `states`, not `sources`, to keep the request field unambiguous).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Refresh".
 */
export type AfbwsCatalogChannelV1_Refresh = {
  channel: 'catalog';
  schema: 'afbws.catalog.refresh.v1';
  request_id?: AfbwsCommonV1_RequestId;
  sources?: AfbwsCatalogChannelV1_Source[];
  queued?: AfbwsCatalogChannelV1_Source[];
  already_queued?: AfbwsCatalogChannelV1_Source[];
  rejected?: AfbwsCatalogChannelV1_Rejection[];
  source?: AfbwsCatalogChannelV1_Source;
  state?: 'done' | 'failed';
  finished_at?: string;
  received?: number | null;
  summary?: string | null;
  error?: string | null;
  revision?: number | null;
  states?: AfbwsCatalogChannelV1_SourceStatus[];
} & AfbwsCatalogChannelV1_Refresh1;
export type AfbwsCatalogChannelV1_Refresh1 = {
  [k: string]: unknown;
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.config.channel.v1). Replaces the legacy `settings`, `help` and `setup` channels (no fallback). Same convention as afbws.market/afbws.gp: ONE schema id per message (`afbws.config.<op>.v1`, no .request/.response/.push suffixes); the same schema is the request, its response and, where documented, a server push. A message WITHOUT `request_id` is a server push. A failed request is answered with `afbws.config.error.v1`; a refused mutation of settings/defaults carries the authoritative current state in `error.item` (the client must apply it and show `message`) — there is no `rejected` flag. Operations: `settings` (user settings), `defaults` (platform defaults; write is manager only), `help` (rendered markdown section), `roles` (manager only), `token` (manager only: MOEX / GetCourse API tokens, write-only). After `auth_ok` the server pushes `defaults` and `settings` without `request_id`. See AFB/docs/ws/config.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigChannelV1Message".
 */
export type ConfigChannelV1Message =
  ConfigSettings | ConfigDefaultsMessage | ConfigHelp | ConfigRoles | ConfigToken | ConfigError;
/**
 * Request without `settings` = read. Request with `settings` = partial write (blocks `profile`/`interface`/`dataset`/`dashboard` deep-merged, `trade` replaced whole; `profile.notify_system` from a non-manager is ignored). The response (same `request_id`) always carries the full stored `settings`. Push (no `request_id`) carries the full `settings`, sent right after `auth_ok`; `settings` is required there. Refusal: `afbws.config.error.v1` with `item` = current settings.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigSettings".
 */
export type ConfigSettings = {
  [k: string]: unknown;
} & {
  channel: 'config';
  schema: 'afbws.config.settings.v1';
  request_id?: AfbwsCommonV1_RequestId;
  settings?: ConfigSettingsV1;
};
/**
 * Request without `defaults` = read (any user). Request with `defaults` = write (manager only, else error `forbidden`); `defaults.dataset` is required on write. The response always carries the full stored `defaults`. Push (no `request_id`) is sent right after `auth_ok`; `defaults` is required there.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigDefaultsMessage".
 */
export type ConfigDefaultsMessage = {
  [k: string]: unknown;
} & {
  channel: 'config';
  schema: 'afbws.config.defaults.v1';
  request_id?: AfbwsCommonV1_RequestId;
  defaults?: ConfigDefaults;
};
/**
 * Request carries `kind` and `token`; the server validates the token against the service (MOEX / GetCourse / Finam; a Finam token must be read-only, a trading token is rejected with `validation_error` and never stored), stores it in the plain-text secrets/*.token file and applies it at runtime. The response carries `kind` and `ok: true` and NEVER the token. Failure: error `validation_error` (token rejected by the service) or `internal_error`; non-manager: `forbidden`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigToken".
 */
export type ConfigToken = {
  channel: 'config';
  schema: 'afbws.config.token.v1';
  request_id: AfbwsCommonV1_RequestId;
  kind: 'moex' | 'getcourse' | 'finam';
  token?: string;
  ok?: true;
} & ConfigToken1;
export type ConfigToken1 = {
  [k: string]: unknown;
};
/**
 * One entry of the `connector` channel (list/get/create/update responses). Owner view (capability trade, user_id in allowed_users) gets everything except the manager-only block; manager gets all fields. See BFRegistryEntry.to_owner_dict()/to_manager_dict() (AFB/backend/trade/models.py) and connector_policy.py for execution_policy validation.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConnectorRecord".
 */
export type ConnectorRecord = BfRegistryEntry & {
  dry_run: boolean | null;
  margin_trading: boolean | null;
  execution_policy: ConnectorExecutionPolicy;
  paired: boolean;
  pairing_pending: boolean;
  pairing_expires_at: string | null;
  /**
   * Merged in by list_connectors_for_user/get_connector_for_user, not part of BFRegistryEntry itself.
   */
  connected?: boolean;
  /**
   * Manager-only.
   */
  public_key_id?: string;
  /**
   * Manager-only.
   */
  public_key_file?: string;
  /**
   * Manager-only.
   */
  allowed_users?: string[];
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.deal.channel.v2). Same convention as afbws.alarm/account/tradeplan v2: ONE schema id per message (`afbws.deal.<op>.v2`, no .request/.response/.push suffixes); the same schema is the request and its response (a response echoes `request_id`); server pushes (`record`, `outcome`, `event`, `pnl`, `triggered`) are the same kind of message without `request_id`. Collections are arrays (`items[]`, `ids[]`, `results[]`, `events[]`), so bulk operations and pushes are single messages (one batch mutation / one tick = one push); a per-deal failure of a batch is a row with accepted=false in `results[]`, `error` is only for a whole request. There is no separate `get`: use `list` with `ids` and `detail: true`. State and facts are split: `record` is the authoritative state of a deal, `outcome` the result of a command, `event` a thin allow-listed fact for the feed (typed per event, see $defs/event), `pnl` the periodic unrealized P&L, `triggered` the guaranteed notifications (acked with `ack`). Strict (additionalProperties:false), no legacy forms: `status`/`execution_phase` are the shared enums (common.v1.json#/$defs/dealStatus, executionPhase), `error.details` does not exist (the server populates none). `item`/`items`/`results[].item` never carry the persisted DealState file shape (source_refs, status_history, event_journal, raw orders/positions, observed) — see $defs/dealSummary and $defs/dealDetail, explicit allow-list projections built by backend/trade/public_views.py. publish/rebind/amend resolve the source tradeplan only via the deal's own link (deal.public.v1.json source.tradeplan_id); they never accept an inline plan-like draft. See AFB/docs/ws/deal.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealChannelV2Message".
 */
export type DealChannelV2Message =
  | DealV2List
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
  | DealV2Triggered;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Id".
 */
export type DealV2Id = string;
/**
 * Id of an AFB tradeplan (state/tradeplans/<user_id>/<id>.yaml). Opaque, case-sensitive. Shared by tradeplan.v2.json, afbws/tradeplan.channel.v2.json and gp.v2.json (`tradeplan_id`, the owning plan of a primitive).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanId".
 */
export type TradeplanId = string;
/**
 * Deal status — the single vocabulary of deal_state.v2.json `status` (kept equal by a test) used by the afbws deal/tradeplan channels. Deletion is not a status.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealStatus".
 */
export type DealStatus =
  'draft' | 'publishing' | 'published' | 'active' | 'paused' | 'closed' | 'cancelled' | 'orphaned';
/**
 * Execution phase of a deal — the single vocabulary of deal_state.v2.json `execution_phase` (kept equal by a test).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealExecutionPhase".
 */
export type DealExecutionPhase = 'idle' | 'awaiting_entry' | 'entry_working' | 'holding' | 'exit_working';
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2BfId".
 */
export type DealV2BfId = string;
/**
 * Stable identity of a tradeplan leg across edits — the key overrides/carry-over (tradeplan/deal separation Фаза B2) use to match a plan leg to its compiled deal leg, never array position. Assigned once when a leg is created and never reused/reassigned. Shared by tradeplan.v2.json (stored/channel legs) and afbws/deal.public.v1.json (the plan-leg identity projected onto deal legs). Legacy synthetic ids (`legacy:{role}:{index}`) are NOT part of the contract: a plan leg without `leg_id` exists only in an input message (the server assigns one on save) or in an old stored file (the server back-fills it on the next write).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LegId".
 */
export type LegId = string;
/**
 * Infix operator joining THIS leg to the PRECEDING leg in the same role's list (entry/stop_loss/take_profit) — not a per-role mode. Omitted (on read) is equivalent to "split", today's behavior, unaffected by this field's existence — old deals/tradeplans persisted without it keep working as-is. The FIRST leg of a role never carries a meaningful `logic` (nothing precedes it) — a producer must omit it there or send `split`; consumers ignore it if present. Grammar, applied left to right over the role's leg list, `and` binding tighter than `or` (`split` always starts a new top-level term, so `a, b:or, c:and` parses as `a OR (b AND c)`): consecutive legs joined by `and` form a GROUP (evaluated as gating sub-conditions of a single order for the group's full volume — the group fires only when every leg in it is true in the same evaluation pass); consecutive groups joined by `or` form a BUCKET (each group remains an independent order, but the whole bucket shares one common volume budget — first fill exhausts the budget, the rest are withdrawn); `split` starts a new bucket, and buckets divide the role's total volume via `percent`. `percent` belongs to the BUCKET and is only meaningful on its first leg (the one whose own `logic` is absent/`split`); it MUST be absent on any leg joined via `and`/`or`. A leg is a bucket of one group of one leg when nothing after it continues it — behaves identically to today regardless of this field's value. NOTE: this schema does not itself enforce leg position (first-leg-has-no-logic) or bucket/role-level homogeneity constraints a consumer may currently apply — those, like other position-dependent rules in this vocabulary, are consumer-side (see BF `protocol/validation.py`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2_LegJoin".
 */
export type DealV2_LegJoin = 'split' | 'and' | 'or';
/**
 * Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2_ConditionNode".
 */
export type DealV2_ConditionNode = ConditionNode & {
  node_type: 'event';
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionNode".
 */
export type ConditionNode = {
  node_type?: 'event';
  id?: string;
} & ConditionNode1;
export type ConditionNode1 =
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op?: 'touch';
    }
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op: 'breakout' | 'breakdown' | 'crossing';
      timeframe: ConditionV1_Timeframe;
    }
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op: ConditionV1_PriceLevelOp;
      duration?: ConditionV1_Duration;
    }
  | {
      left?: ConditionV1_IndicatorExpr;
      right?: ConditionV1_RightConst | ConditionV1_IndicatorExpr;
      op: ConditionV1_ScalarOp;
      timeframe?: ConditionV1_Timeframe;
    }
  | {
      left?: ConditionV1_DatasetExpr;
      right?: ConditionV1_RightConst | ConditionV1_DatasetExpr;
      op: ConditionV1_ScalarOp;
    }
  | {
      left?: ConditionV1_ImmediateExpr;
      right?: ConditionV1_RightConst;
      op: 'above';
    };
/**
 * Optional protective time in seconds: the condition must remain continuously true for this many real seconds (BF monotonic clock) before firing. False, evaluate gaps, amend/pause/cancel and BF restart reset progress; progress is not persisted. AFB draft emulation and alarms ignore it. Only meaningful with price above/below (producer converts touch to above/below before wire); multi-leg plans may carry duration independently per leg.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_Duration".
 */
export type ConditionV1_Duration = number;
/**
 * AFB-side provenance of this leg's condition — which side last set it: `tradeplan` (still following the linked plan, default when absent) or `deal` (overridden directly on the deal, decoupled from further plan edits to this leg). BF does not interpret this field — round-trip only (persist as received, echo back unchanged); it exists purely for AFB's per-leg amend/override UI (tradeplan/deal separation Фаза B2).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2_LegSource".
 */
export type DealV2_LegSource = 'tradeplan' | 'deal';
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicExitList".
 */
export type DealPublicExitList = {
  leg_id?: LegId;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
  condition: DealV2_ConditionNode;
  source?: DealV2_LegSource;
}[];
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2AmendField".
 */
export type DealV2AmendField = 'entry' | 'sizing' | 'stop_loss' | 'take_profit' | 'execution_policy';
/**
 * Status in an operation/publish result row: the deal status after the command, or `deleted` right after `delete` (the deal is archived and no longer exists as a record).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2ResultStatus".
 */
export type DealV2ResultStatus = DealStatus | 'deleted';
/**
 * Request: `events[]` (afb.deal.trigger_ack.v2), at least one. Response (same `request_id`): `results[]` — one per event, `status` ok | not_found. Exactly one of `events` / `results`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Ack".
 */
export type DealV2Ack = {
  [k: string]: unknown;
} & {
  channel: 'deal';
  schema: 'afbws.deal.ack.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  events?: [DealV2AckEvent, ...DealV2AckEvent[]];
  results?: DealV2AckResultItem[];
};
/**
 * A thin, allow-listed event for the event feed, the order/position patches and the chart markers — never a state snapshot (state: `afbws.deal.record.v2`) and never a raw BF payload: only the fields a consumer reads or that make up the meaning of the event are listed, everything else BF sends (`broker_instrument`, `validation`, `execution_legs`, `target_instrument_patch`, `binding`, `snapshot`, `observed`, `deal.snapshot` altogether) is dropped. `data` is determined by `event` within `category`; `category` is fixed per event.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventItem".
 */
export type DealV2EventItem =
  | DealV2EventDealCreated
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
  | DealV2EventConditionTriggered;
/**
 * Role of an order / of the leg whose condition fired. Superset of deal_state.v2 order.role: `external_close` is the synthetic order BF records when the position was closed outside the deal (it emits order.* for it too).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OrderRole".
 */
export type DealV2OrderRole = 'entry' | 'stop_loss' | 'take_profit' | 'cancel_close' | 'backstop' | 'external_close';
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OrderSide".
 */
export type DealV2OrderSide = 'buy' | 'sell';
/**
 * Order status carried by an order.* event: deal_state.v2 order.status plus `unknown` (a broker answer BF could not map; BF then verifies the order against the broker).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OrderEventStatus".
 */
export type DealV2OrderEventStatus =
  'new' | 'partially_filled' | 'filled' | 'cancelled' | 'rejected' | 'watching' | 'expired' | 'unknown';
/**
 * Schema analogue of the legacy TriggeredDealItem — not the MQTT notification.deal.v1 payload (different transport). `notification_id` is the idempotency key the client acks.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2TriggerEvent".
 */
export type DealV2TriggerEvent = DealV2TriggerStatusChanged | DealV2TriggerRejected | DealV2TriggerReport;
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.gp.channel.v2). Items are afb.gp.v2 (`instrument_key`, kinds trendline/fibonacci; primitive parameters `start`/`stop`/`text` live in the `settings` dictionary, strictly typed by `kind`). Same convention as afbws.market: ONE schema id per message (`afbws.gp.<op>.v2`, no .request/.response/.push suffixes); the same schema is the request, its response and, where documented, a server push. Requests and responses are told apart by direction and fields (a response echoes the request's `request_id`); a message WITHOUT `request_id` is a server push. Collections are always arrays (`items[]`, `ids[]`, `instrument_keys[]`), so bulk operations are single messages; partial failures come back in `rejected[]`. Chart-indicator management (replaces legacy settings/{get,set,get_default,set_default} `indicators`) is `indicator.list|set|delete`; shared indicators are changed by a manager only and pushed to everyone via `indicator.set`/`indicator.delete` without `request_id`. Primitive display settings: `style`. See AFB/docs/ENTITY_WS_PROTOCOL.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpChannelV2Message".
 */
export type GpChannelV2Message =
  GpV2List | GpV2Set | GpV2Delete | GpV2IndicatorList | GpV2IndicatorSet | GpV2IndicatorDelete | GpV2Style | GpV2Error;
/**
 * v2 of afb.gp.v1 with differences: (1) the instrument is identified by the full composite `instrument_key` (afbws/common.v1.json#/$defs/instrumentKey) instead of the short `ticker`; (2) new kinds `trendline` and `fibonacci` — both two-anchor primitives; their rendering is not specified yet; (3) the primitive's own parameters (`start`, `stop`, `text`) live in the `settings` dictionary, not at the root, so a kind can gain parameters without touching the envelope. ROOT = identity and server-side ownership: `schema`, `id`, `instrument_key`, `kind`, `tradeplan_id` (all other parameters go to `settings`). `settings` is REQUIRED and strictly typed by `kind` (enforced by the `allOf` below, each branch is additionalProperties:false): line/line_enter/line_sl/line_tp → `primitiveSettingsLine` {start}; note → `primitiveSettingsNote` {start, text? (≤160)}; zone/ruler/trendline/fibonacci → `primitiveSettingsTwoPoint` {start, stop}. v1 (`afb.gp.v1`, flat start/stop/text) stays supported for frontends without afbws.gp.channel.v2; v1 clients never receive trendline/fibonacci. Promotes the parked settings.primitives[secid][] draft (draft/primitive.v1.json) into a strict canonical entity. Whether a primitive is REFERENCED BY a tradeplan's condition is still derived fresh from the tradeplans themselves on every read, never persisted here. OWNERSHIP is different and is persisted — see `tradeplan_id`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2".
 */
export type GpV2 = {
  [k: string]: unknown;
} & {
  schema: 'afb.gp.v2';
  id: string;
  instrument_key: AfbwsCommonV1_InstrumentKey;
  kind: 'line' | 'line_enter' | 'line_sl' | 'line_tp' | 'note' | 'zone' | 'ruler' | 'trendline' | 'fibonacci';
  /**
   * Primitive parameters, strictly typed by `kind` (see root description). Replaced as a whole on `set`.
   */
  settings: GpV2PrimitiveSettingsLine | GpV2PrimitiveSettingsNote | GpV2PrimitiveSettingsTwoPoint;
  /**
   * Id of an AFB tradeplan (state/tradeplans/<user_id>/<id>.yaml). Opaque, case-sensitive. Shared by tradeplan.v2.json, afbws/tradeplan.channel.v2.json and gp.v2.json (`tradeplan_id`, the owning plan of a primitive).
   */
  tradeplan_id?: string;
};
/**
 * Request (`request_id` present, `items` = what the client wants stored): upsert by `item.id`, batched (each item carries `settings`; `settings` is replaced as a whole; a client-sent `tradeplan_id` is ignored in favour of the stored one); moving a primitive is the same request as creating or editing one. Response (same `request_id`): `items` = the authoritative stored records that were applied (possibly empty), `rejected[]` = items that were NOT applied, each with a typed reason (partial failure never fails the whole message; the backend alone decides whether a move is safe against linked tradeplans). Push (no `request_id`, server-initiated): ownership delta by id — `items[]` are authoritative afb.gp.v2 records (bind: `tradeplan_id` set on publish/amend; release: `tradeplan_id` cleared on plan physical delete); never a snapshot, `rejected` is not allowed. Primitive removal is conveyed by `afbws.gp.delete.v2` without `request_id`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2Set".
 */
export type GpV2Set = {
  [k: string]: unknown;
} & {
  channel: 'gp';
  schema: 'afbws.gp.set.v2';
  request_id?: AfbwsCommonV1_RequestId;
  items: GpV2[];
  rejected?: GpV2Rejection[];
};
/**
 * Request (`request_id` present): `ids[]` and/or `instrument_keys[]` (at least one; `instrument_keys` = every FREE primitive of those instruments in one call). Primitives owned by a tradeplan (`tradeplan_id`) are never removed here — they come back in `rejected[]` with `code: conflict` and `details` (linked plans/deals). Response (same `request_id`): `ids[]` = ids actually removed (possibly empty), `rejected[]`. Push (no `request_id`): `ids[]` removed by the server; `instrument_keys`/`rejected` are not allowed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2Delete".
 */
export type GpV2Delete = {
  [k: string]: unknown;
} & {
  channel: 'gp';
  schema: 'afbws.gp.delete.v2';
  request_id?: AfbwsCommonV1_RequestId;
  ids?: string[];
  /**
   * @minItems 1
   */
  instrument_keys?: [AfbwsCommonV1_InstrumentKey, ...AfbwsCommonV1_InstrumentKey[]];
  rejected?: GpV2Rejection[];
};
/**
 * Request: upsert by `id`, batched. Personal indicators for everyone; `scope: shared` only for a manager (otherwise that item is rejected with `forbidden`). Response (same `request_id`): applied `items[]` (possibly empty) + `rejected[]`. Push (no `request_id`): changed SHARED indicators to every connection with this capability (full authoritative records); personal ones are never pushed. Whether an indicator is drawn on the chart is NOT part of the protocol — it is a per-device view setting kept in the client's localStorage.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2IndicatorSet".
 */
export type GpV2IndicatorSet = {
  [k: string]: unknown;
} & {
  channel: 'gp';
  schema: 'afbws.gp.indicator.set.v2';
  request_id?: AfbwsCommonV1_RequestId;
  items: GpV2Indicator[];
  rejected?: GpV2IndicatorRejection[];
};
/**
 * Request: `ids[]` (shared ones: manager only, otherwise rejected with `forbidden`; unknown id: `not_found`). Response (same `request_id`): `ids[]` actually removed + `rejected[]`. Push (no `request_id`): shared indicators deleted by a manager (`ids[]`, `rejected` not allowed).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2IndicatorDelete".
 */
export type GpV2IndicatorDelete = {
  [k: string]: unknown;
} & {
  channel: 'gp';
  schema: 'afbws.gp.indicator.delete.v2';
  request_id?: AfbwsCommonV1_RequestId;
  ids: string[];
  rejected?: GpV2IndicatorRejection[];
};
/**
 * Per-user chart styling of primitives by kind (replaces the legacy `settings.interface.primitive_styles`). Request without `styles` = read. Request with `styles` = write: the supplied kinds replace the stored ones, kinds not supplied are left as they are. Response (same `request_id`) always carries the full stored `styles`. Push (no `request_id`) delivers the full `styles` to the user's other connections after a write; `styles` is required there.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2Style".
 */
export type GpV2Style = {
  [k: string]: unknown;
} & {
  channel: 'gp';
  schema: 'afbws.gp.style.v2';
  request_id?: AfbwsCommonV1_RequestId;
  styles?: GpV2PrimitiveStyles;
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.instrument.channel.v2). Provides only the operations the project uses and that afbws.catalog.channel.v1 does not already cover. Same convention as afbws.catalog/afbws.alarm.v2/afbws.gp.v2: ONE schema id per message (`afbws.instrument.<op>.v2`), the same schema is the request, its response and, for `expiration`, the server push; a message WITHOUT `request_id` is a server push; a failed request is answered with `afbws.instrument.error.v2`. Operations: `catalog`, `sets`, `favorites`, `paint`, `expiration`, `replace`, `detail`. Instruments are addressed ONLY by `instrument_key`; `ticker` appears solely as a display attribute of a listing / notice. All operations are open to any authenticated caller; manager rights (global sets) are checked by the backend per `visibility`. See AFB/docs/ws/instrument.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Root".
 */
export type AfbwsInstrumentChannelV2_Root =
  | AfbwsInstrumentChannelV2_Catalog
  | AfbwsInstrumentChannelV2_Sets
  | AfbwsInstrumentChannelV2_Favorites
  | AfbwsInstrumentChannelV2_Paint
  | AfbwsInstrumentChannelV2_Expiration
  | AfbwsInstrumentChannelV2_Replace
  | AfbwsInstrumentChannelV2_Detail
  | AfbwsInstrumentChannelV2_Error;
/**
 * Request: only `request_id`. Response (same `request_id`): what the caller may see — ordered `collections`, `sets` (global sets published for the caller's tier plus the caller's own `personal` ones, in display order), `assets` with members, the active `listings` the caller may see and the `derivatives` axis. Completeness is applied by the backend from the caller's role (a manager also sees unassigned assets). `revision` is the global catalog revision (`catalog_revision` of `sets`), `user_revision` the revision of the caller's personal sets aggregate. Any authenticated caller.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Catalog".
 */
export type AfbwsInstrumentChannelV2_Catalog = {
  channel: 'instrument';
  schema: 'afbws.instrument.catalog.v2';
  request_id?: AfbwsCommonV1_RequestId;
  revision?: number;
  user_revision?: number;
  collections?: AfbwsInstrumentChannelV2_Collection[];
  sets?: AfbwsInstrumentChannelV2_Set[];
  assets?: AfbwsInstrumentChannelV2_Asset[];
  listings?: AfbwsInstrumentChannelV2_Listing[];
  derivatives?: AfbwsInstrumentChannelV2_Derivative[];
} & AfbwsInstrumentChannelV2_Catalog1;
/**
 * Same list and order as afbws.catalog.channel.v1 (kept in lockstep; no cross-reference on purpose).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_FavoriteColor".
 */
export type AfbwsInstrumentChannelV2_FavoriteColor =
  'yellow' | 'red' | 'blue' | 'green' | 'gray' | 'orange' | 'cyan' | 'purple' | 'pink' | 'teal';
/**
 * A named set of assets (`asset_ids[]`) or of instruments (`instrument_keys[]`), by `type`; exactly the list of its own type is present, always the WHOLE composition in display order. `type` is decided on create and cannot change afterwards.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Set".
 */
export type AfbwsInstrumentChannelV2_Set = {
  [k: string]: unknown;
} & {
  id: string;
  name: string;
  type: 'asset' | 'instrument';
  visibility: AfbwsInstrumentChannelV2_Visibility;
  /**
   * Opaque icon key. Omitted in a request: unchanged; null: clears.
   */
  icon_id?: string | null;
  /**
   * Omitted in a request: unchanged; null: clears.
   */
  icon_color?: AfbwsInstrumentChannelV2_FavoriteColor | null;
  asset_ids?: string[];
  instrument_keys?: AfbwsCommonV1_InstrumentKey[];
};
/**
 * Who sees a set. `personal` — only its owner (any authenticated caller may create these, within the tier limit `max_sets`). `guest`/`user`/`manager` — a GLOBAL set published for callers whose tier is at least that one; creating, changing or deleting a global set is manager-only (backend gate, `forbidden` otherwise).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Visibility".
 */
export type AfbwsInstrumentChannelV2_Visibility = 'personal' | 'guest' | 'user' | 'manager';
export type AfbwsInstrumentChannelV2_Catalog1 = {
  [k: string]: unknown;
};
/**
 * ONE command for all authenticated callers; the only difference between a user and a manager is the `visibility` of the set, checked by the backend. Request: `sets[]` — upsert by `id`, each with its WHOLE composition in final order (omit the list to leave a set's composition untouched); the order of `sets[]` is the display order of the sets (personal ones and global ones are ordered separately); `remove_sets[]` — ids to delete. `visibility` `personal` (default for a new set) is open to everybody within the tier limit `max_sets`; `guest|user|manager` (global set) is manager-only (`forbidden`, `details.set_ids`). A set keeps its scope: switching between `personal` and a global visibility is `validation_error`. CAS: `user_revision` guards the personal sets, `catalog_revision` the global ones; each is required when the request touches that area (stale -> `conflict` with the current revisions in `details`). The request is atomic: if anything is rejected nothing is applied. Response (same `request_id`): both revisions and `sets[]` — the caller's visible sets after the change, in display order (same form as `catalog.sets`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Sets".
 */
export type AfbwsInstrumentChannelV2_Sets = {
  channel: 'instrument';
  schema: 'afbws.instrument.sets.v2';
  request_id?: AfbwsCommonV1_RequestId;
  user_revision?: number;
  catalog_revision?: number;
  sets?: AfbwsInstrumentChannelV2_SetEdit[];
  remove_sets?: string[];
  /**
   * Present (true) only in the response.
   */
  applied?: true;
} & AfbwsInstrumentChannelV2_Sets1;
/**
 * A set inside `sets` (request / response). Request: `type` (default `asset` on create; on update must equal the stored one) and `visibility` (default `personal` on create; unchanged on update) are optional; the composition list of the set's own type, when present, is the WHOLE composition in final order. Response: every field of `set` is present.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_SetEdit".
 */
export type AfbwsInstrumentChannelV2_SetEdit = {
  [k: string]: unknown;
} & {
  id: string;
  name: string;
  type?: 'asset' | 'instrument';
  visibility?: AfbwsInstrumentChannelV2_Visibility;
  /**
   * Opaque icon key. Omitted in a request: unchanged; null: clears.
   */
  icon_id?: string | null;
  /**
   * Omitted in a request: unchanged; null: clears.
   */
  icon_color?: AfbwsInstrumentChannelV2_FavoriteColor | null;
  asset_ids?: string[];
  instrument_keys?: AfbwsCommonV1_InstrumentKey[];
};
export type AfbwsInstrumentChannelV2_Sets1 = {
  [k: string]: unknown;
};
/**
 * Request: only `request_id`. Response: `items[]` nearest expiration first. The SAME schema is the server push: a message WITHOUT `request_id` carries the caller's full current list, which REPLACES the client's copy (an empty list clears the card).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Expiration".
 */
export type AfbwsInstrumentChannelV2_Expiration = {
  channel: 'instrument';
  schema: 'afbws.instrument.expiration.v2';
  request_id?: AfbwsCommonV1_RequestId;
  items?: AfbwsInstrumentChannelV2_ExpirationNotice[];
} & AfbwsInstrumentChannelV2_Expiration1;
export type AfbwsInstrumentChannelV2_Expiration1 = {
  [k: string]: unknown;
};
/**
 * Request: `from_key`, `to_key` (an ACTIVE contract of the same derivative) and optional `kinds` (default all four). Prices and levels are never adjusted. Partial results are normal: what could not be moved is in `rejected[]`. Idempotent. Response: the same keys plus `replaced` (counts), `rejected[]` and the refreshed `items[]` (as a fresh `expiration`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Replace".
 */
export type AfbwsInstrumentChannelV2_Replace = {
  channel: 'instrument';
  schema: 'afbws.instrument.replace.v2';
  request_id?: AfbwsCommonV1_RequestId;
  from_key: AfbwsCommonV1_InstrumentKey;
  to_key: AfbwsCommonV1_InstrumentKey;
  /**
   * @minItems 1
   */
  kinds?: [AfbwsInstrumentChannelV2_ReplaceKind, ...AfbwsInstrumentChannelV2_ReplaceKind[]];
  replaced?: AfbwsInstrumentChannelV2_ExpirationUsage;
  rejected?: AfbwsInstrumentChannelV2_ReplaceRejection[];
  items?: AfbwsInstrumentChannelV2_ExpirationNotice[];
} & AfbwsInstrumentChannelV2_Replace1;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_ReplaceKind".
 */
export type AfbwsInstrumentChannelV2_ReplaceKind = 'alarms' | 'primitives' | 'sets' | 'favorites';
export type AfbwsInstrumentChannelV2_Replace1 = {
  [k: string]: unknown;
};
/**
 * Request: `instrument_key` and optionally `accounts[]` to narrow the answer; by default ALL accounts of the caller, the virtual one included. The tradeplan editor asks once when it opens (and when the instrument changes) and picks the selected account from `items[]`. Response (same `request_id`): `items[]` — one entry per account; a failure of one account is that entry's `status`/`error`, the others are unaffected. A whole-request error (`not_found` for an unknown key, `forbidden`, `unavailable` when there are no accounts) is `afbws.instrument.error.v2`. Any authenticated caller.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Detail".
 */
export type AfbwsInstrumentChannelV2_Detail = {
  channel: 'instrument';
  schema: 'afbws.instrument.detail.v2';
  request_id?: AfbwsCommonV1_RequestId;
  instrument_key: AfbwsCommonV1_InstrumentKey;
  /**
   * @minItems 1
   */
  accounts?: [AfbwsInstrumentChannelV2_AccountRef, ...AfbwsInstrumentChannelV2_AccountRef[]];
  items?: AfbwsInstrumentChannelV2_AccountDetail[];
} & AfbwsInstrumentChannelV2_Detail1;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_AccountDetail".
 */
export type AfbwsInstrumentChannelV2_AccountDetail = {
  [k: string]: unknown;
} & {
  bf_id: string;
  account_id: string;
  status: 'ok' | 'unavailable' | 'error';
  /**
   * `account` — the values are those of this very account; `connector` — the connector (BF) answered without account granularity, the values are connector-level.
   */
  scope?: 'account' | 'connector';
  /**
   * Trading parameters (tradable, longable, shortable, initial margins, price_type …) — BF-owned shape for real accounts, computed by AFB for the virtual one. Present when status is `ok`.
   */
  broker_instrument?: {
    [k: string]: unknown;
  };
  error?: {
    code: 'not_found' | 'bf_offline' | 'unsupported_action' | 'internal_error' | 'unavailable';
    message: string;
  };
};
export type AfbwsInstrumentChannelV2_Detail1 = {
  [k: string]: unknown;
};
/**
 * Manager view of a BF connector config record — reuses link.user.v1.json#/$defs/sharedFields (via $ref, not redeclared, so the two views can't drift apart) plus ACL/key management fields. Never carries `connected`/`daemon`/session runtime — see link.channel.v2.json#/$defs/statusItem.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkAdminV1".
 */
export type LinkAdminV1 = BfRegistryEntry &
  LinkSharedFields & {
    schema: 'afbws.link.admin.v1';
    allowed_users: string[];
    public_key_id: string | null;
    public_key_file: string | null;
  };
/**
 * Manager upsert: composes link.user.v1.json#/$defs/setInputShared with admin-only extras. `bf_id` omitted means create (backend assigns/validates id and requires broker + defaults); `bf_id` present and already registered means update. Backend enforces which combination is valid, not this schema.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkAdminSetInput".
 */
export type LinkAdminSetInput = LinkSetInputShared & {
  broker?: string;
  protocol?: string;
  margin_trading?: boolean | null;
  allowed_users?: string[];
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.link.channel.v2). Same convention as afbws.alarm.channel.v2: ONE schema id per message (`afbws.link.<op>.v2`, no .request/.response/.push suffixes); the same schema is the request, its response (echoes `request_id`) and the server push (no `request_id`). Collections are arrays (`items[]`, `ids[]`), so bulk operations are single messages; per-element failures come back in `rejected[]` (only with `request_id`), a whole-request failure is `afbws.link.error.v2`. Config records are afbws.link.user.v1 / afbws.link.admin.v1 (role-chosen by the backend); runtime status records (`afbws.link.state.v2`, `status` operation) are separate and never mixed into config items. Pushes are deltas: list/set push = upsert by `bf_id`, delete push = removal, status push = only changed statuses (repeated heartbeats without change are silent). See AFB/docs/ws/link.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkChannelV2Message".
 */
export type LinkChannelV2Message =
  LinkV2List | LinkV2Set | LinkV2Delete | LinkV2Pair | LinkV2Restart | LinkV2Status | LinkV2Error;
/**
 * Request (`request_id`, no `items`): optional `scope` (usable = default, working accounts the caller may trade on incl. virtual; admin = full registry as admin views, managers only) and `ids[]` filter (none = all of the scope). Response (same `request_id`): `items[]` (afbws.link.user.v1 | afbws.link.admin.v1, role-chosen). Push (no `request_id`, server-initiated): `items[]` (at least one) created/changed connectors — upsert by `bf_id`, never a snapshot; removal is `afbws.link.delete.v2` push. The first list/status request subscribes the connection to link pushes. There is no separate `get`: use `ids`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2List".
 */
export type LinkV2List = {
  [k: string]: unknown;
} & {
  channel: 'link';
  schema: 'afbws.link.list.v2';
  request_id?: AfbwsCommonV1_RequestId;
  scope?: 'usable' | 'admin';
  /**
   * @minItems 1
   */
  ids?: [string, ...string[]];
  items?: LinkV2Entity[];
};
/**
 * Role-chosen config view — afbws.link.user.v1 (non-manager, including the synthetic virtual pseudo-connector) or afbws.link.admin.v1 (manager). The backend chooses which, never the client.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Entity".
 */
export type LinkV2Entity = LinkUserV1 | LinkAdminV1;
/**
 * Caller-scoped BF connector config record for a non-manager viewer (owner: capability trade + user_id in allowed_users, or role-only access — role-only is read-only, enforced by the backend, not this schema). Never carries `connected`/`daemon`/session runtime — see link.channel.v2.json#/$defs/statusItem for that, delivered on a separate push. The synthetic `virtual` pseudo-connector also uses this exact shape (kind:"virtual") — see link.channel.v2.json. `$defs/sharedFields` is the single source of the fields link.admin.v1.json reuses (via $ref) so the two views can't drift apart independently. `$defs/setInputShared` is the same for set() payloads.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkUserV1".
 */
export type LinkUserV1 = BfRegistryEntry &
  LinkSharedFields & {
    schema: 'afbws.link.user.v1';
  };
/**
 * Request (`request_id`, no `rejected`): `items[]` of role-chosen set input, at least one. Response (same `request_id`, `rejected` present): applied `items[]` (authoritative records, possibly empty) + `rejected[]` (per-item failures; `conflict` carries the current `item`). Push (no `request_id`): `items[]` (at least one) created/changed on the server's own initiative — upsert by `bf_id`; `rejected` is not allowed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Set".
 */
export type LinkV2Set = {
  [k: string]: unknown;
} & {
  channel: 'link';
  schema: 'afbws.link.set.v2';
  request_id?: AfbwsCommonV1_RequestId;
  items: (LinkV2Entity | LinkV2SetInput)[];
  rejected?: LinkV2Rejection[];
};
/**
 * Role-chosen set() item shape — the backend selects which by the authenticated caller's role, never by a client-declared schema id. anyOf, not oneOf: neither shape carries a discriminating `schema` field, and a minimal payload (e.g. {bf_id, dry_run}) is structurally valid under both. The backend, not this schema, decides which fields a given caller may actually use.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2SetInput".
 */
export type LinkV2SetInput = LinkUserSetInput | LinkAdminSetInput;
/**
 * A non-manager caller may adjust name/enabled/description/dry_run/execution_policy on their own already-existing connector — never broker/protocol/allowed_* /margin_trading, and never create a new entry (bf_id must already exist and be owned by the caller; enforced by the backend, not this schema).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkUserSetInput".
 */
export type LinkUserSetInput = LinkSetInputShared;
/**
 * Request (`request_id`, no `rejected`): `ids[]`, at least one. Response (same `request_id`, `rejected` present): `ids[]` actually removed (possibly empty) + `rejected[]`. Push (no `request_id`): `ids[]` (at least one) removed from the registry — drop by `bf_id`; `rejected` is not allowed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Delete".
 */
export type LinkV2Delete = {
  [k: string]: unknown;
} & {
  channel: 'link';
  schema: 'afbws.link.delete.v2';
  request_id?: AfbwsCommonV1_RequestId;
  ids: string[];
  rejected?: LinkV2Rejection[];
};
/**
 * Request: `ids[]`, at least one (manager or owner; the virtual connector is rejected with `unsupported_action`). Response (same `request_id`): `items[]` — one `{id, item, pairing_string, expires_at}` per started pairing + `rejected[]`. No server push.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Pair".
 */
export type LinkV2Pair = {
  channel: 'link';
  schema: 'afbws.link.pair.v2';
  request_id: AfbwsCommonV1_RequestId;
  ids?: string[];
  items?: LinkV2PairItem[];
  rejected?: LinkV2Rejection[];
} & LinkV2Pair1;
export type LinkV2Pair1 =
  | {
      ids: {
        [k: string]: unknown;
      };
    }
  | {
      [k: string]: unknown;
    };
/**
 * Request: explicit `ids[]`, at least one — never implicitly picks the first accessible BF. Response (same `request_id`): `ids[]` for which the restart command was sent + `rejected[]`. No server push.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Restart".
 */
export type LinkV2Restart = {
  [k: string]: unknown;
} & {
  channel: 'link';
  schema: 'afbws.link.restart.v2';
  request_id: AfbwsCommonV1_RequestId;
  ids: string[];
  rejected?: LinkV2Rejection[];
};
/**
 * Request (`request_id`, no `items`): optional `ids[]` (none = every connector visible in the caller's usable view). Response (same `request_id`): `items[]` of status records (afbws.link.state.v2). Push (no `request_id`): `items[]` (at least one) of ONLY the statuses that changed — repeated heartbeats without a state change produce no push. `updated_at` of a record is the moment of its last state change. The first list/status request subscribes the connection to pushes.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Status".
 */
export type LinkV2Status = {
  [k: string]: unknown;
} & {
  channel: 'link';
  schema: 'afbws.link.status.v2';
  request_id?: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  ids?: [string, ...string[]];
  items?: LinkV2StatusItem[];
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.market.channel.v1). Replaces the legacy `candles` channel (klines + background datasets positions/trades/hhi/orders), `stream/favorites`, `stream/positions`, and `securities/marketdata|futures|positions` for clients that negotiated this capability; legacy stays available as fallback for clients that did not — this migration carries no version-gated behaviour, negotiation is purely by `auth.support`/`auth_ok.support`. Every instrument is addressed by the catalog's full `instrument_key` (see common.v1.json#/$defs/instrumentKey), not a bare SECID. Two data templates cover the subscribable/pushable payload shapes: `series` (candles and every background dataset, keyed by `time`) and `snapshot` (a cross-instrument slice, keyed by `instrument_key`), both columnar (`$defs/table`: `columns` + `rows`). The same schema id serves both as the reply to a `get` (carries `request_id`) and as an unsolicited push to a live subscription (no `request_id`) — deliberately no `.request`/`.response`/`.push` suffix on schema ids. Every data message carries `received_at` (when AFB received the data from its source) and `tz` (the trading venue's IANA zone that row-level `time`/day boundaries are aligned to). Two independent subscription mechanisms exist, deliberately not unified: `subscribe` is explicit and replace-all for the `quotes` (favorites) and `futures` (screener) snapshot scopes — the client states its whole desired scope every time, the server does not diff against a previous statement; the series (candles/dataset) subscription has no separate message at all — a connection has at most one, and it is simply whatever `get` (target=series) was last sent with a live `end_date` (see `get`'s description). There is no client-side calendar lookup at all: a live `series` (`$defs/series`) itself carries an optional `future_times` — AFB derives future (whitespace) bar slots for the chart server-side from its own trading-calendar state and includes them directly in the series answer/push, so the frontend never has to ask separately. `NaN` never appears on the wire — sources that produce it are converted to `null`. Two more optional pieces cover degraded external sources (plan стабильности AFB, Этап 3): `series.data_status` (`$defs/dataStatus`) flags a single reply/push as stale/partial when it did not come from a normal fresh fetch, and `source_status` (`$defs/sourceStatus`, unsolicited push) is a channel-wide health snapshot of AFB's external sources (`moex`/`getcourse`), replacing the removed legacy `stream/loop_status`. See AFB/docs/ws/market.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketChannelV1Message".
 */
export type MarketChannelV1Message =
  | MarketSubscribe
  | MarketSubscription
  | MarketGet
  | MarketSeries
  | MarketSnapshot
  | AfbwsMarketChannelV1_SourceStatus
  | MarketErrorResponse;
/**
 * Reply is `series` (target=series) or `snapshot` (target=snapshot) with the same `request_id`, or `error`. For target=series, `get` doubles as the subscription request: a connection has at most one live series subscription (instrument_key, period, kinds), there is no separate subscribe message for it. If `end_date` is absent, or not earlier than "today" in the instrument's market `tz`, this request ALSO becomes that live subscription, replacing whatever the connection was previously subscribed to — the server then pushes `series` (mode:"merge") for it as new data arrives; the reply and subsequent pushes may also carry `future_times` (see `$defs/series`) — there is no separate calendar lookup. A target=series request with `end_date` strictly before today (history paging, e.g. scrolling a chart back) is a pure history fetch and leaves the live subscription untouched.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketGet".
 */
export type MarketGet = {
  [k: string]: unknown;
} & {
  channel: 'market';
  schema: 'afbws.market.get.v1';
  request_id: AfbwsCommonV1_RequestId;
  target: 'series' | 'snapshot';
  instrument_key?: AfbwsCommonV1_InstrumentKey;
  period?: MarketPeriod;
  /**
   * @minItems 1
   */
  kinds?: [string, ...string[]];
  /**
   * target=series only: first date to fetch, YYYY-MM-DD in the instrument's market tz.
   */
  start_date?: string;
  /**
   * target=series only: last date to fetch, YYYY-MM-DD; omitted means up to the latest available. Also decides whether this request becomes the connection's live series subscription — see the parent description.
   */
  end_date?: string;
  /**
   * target=series only: opaque provider/period hint (candle base), passed through unchanged.
   */
  base?: string;
  /**
   * target=snapshot only: instruments to fetch; omitted means every instrument with cached data (used by TickersList).
   *
   * @maxItems 2000
   */
  instrument_keys?: AfbwsCommonV1_InstrumentKey[];
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketPeriod".
 */
export type MarketPeriod = '1min' | '5min' | '10min' | '15min' | '30min' | '1h' | '2h' | '4h' | '1d';
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSeriesTable".
 */
export type MarketSeriesTable = MarketTable & {
  kind?: 'candles' | 'positions' | 'trades' | 'hhi' | 'orders';
};
/**
 * `rows` are keyed by their first column: `time` (UTC unix seconds) for the series kinds (candles/positions/trades/hhi/orders), `instrument_key` for the snapshot kinds (quote/oi/oi_daily). Beyond that first column, `columns` may list any subset of the kind's allowed fields in any order — a client reads by column name, never by positional index — so the server can add a field later without a schema bump, as long as it stays inside the per-kind enum below. `rows` elements are `number | string | null`; a source value that is NaN is sent as `null`, never as the string "NaN" or JSON NaN. In a `series` message, non-candle dataset rows (positions/trades/hhi/orders) exist only at the timestamps of that same message's `candles` table — the server aligns them: `positions` is snapped to the bucket `[t, next candle)` and carries the candle's `t`; `trades`/`orders`/`hhi` require an exact `time` match. There are no rows outside trading hours (no forward-filled/stale values).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketTable".
 */
export type MarketTable = {
  [k: string]: unknown;
} & {
  kind: 'candles' | 'positions' | 'trades' | 'hhi' | 'orders' | 'quote' | 'oi' | 'oi_daily';
  /**
   * @minItems 1
   */
  columns: [string, ...string[]];
  /**
   * Each row has the same length and column order as `columns`.
   */
  rows: (number | string | null)[][];
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSnapshotTable".
 */
export type MarketSnapshotTable = MarketTable & {
  kind?: 'quote' | 'oi' | 'oi_daily';
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.screener.channel.v1). Read-only access to the screener's published JSON exports (contract v1, see AFB/docs/SCREENER_RESULTS.md); the backend never opens the screener database. Same convention as afbws.market/afbws.config: ONE schema id per message (`afbws.screener.<op>.v1`, no .request/.response suffixes); the same schema is the request and its response. `request_id` is required in every client request. The only server push is `afbws.screener.participants.v1` without `request_id` (see its description); the other operations are answered on demand. A failed request is answered with `afbws.screener.error.v1`. Operations: `list` (available exports, newest first, content not read), `get` (one export by id) and `participants` (market participants snapshot: four lists now/d1/d2/w1 of derivatives with fiz/yur positions, open interest and volume, computed by the backend from market_cache). Export ids: `night:YYYY-MM-DD` (night result of a trading day), `intraday:YYYY-MM-DDTHHMM` (intraday snapshot), or the aliases `latest` (newest night export) and `intraday_latest` (newest intraday snapshot). Access requires the `screener` capability of the user's role; otherwise `forbidden`. The exported document is intentionally an open object: only `contract_version` is relied upon; the screener's fields (signals, reliability, models, errors) evolve and are described in AFB/docs/SCREENER_RESULTS.md. A document with an unsupported `contract_version` is answered with `unsupported_action`. See AFB/docs/ws/screener.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerChannelV1Message".
 */
export type ScreenerChannelV1Message = ScreenerV1List | ScreenerV1Get | ScreenerV1Participants | ScreenerV1Error;
/**
 * Request carries only optional filters. Response carries `items` (newest first) and the ids of the newest exports: `latest` (newest night export) and `intraday_latest` (newest intraday snapshot), each null when there is none. Both are computed from file names, not from the screener's latest*.json copies.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerV1List".
 */
export type ScreenerV1List = {
  [k: string]: unknown;
} & {
  channel: 'screener';
  schema: 'afbws.screener.list.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * Request: only exports of this kind.
   */
  kind?: 'night' | 'intraday';
  /**
   * Request: at most this many newest items.
   */
  limit?: number;
  /**
   * Response only.
   */
  items?: AfbwsScreenerChannelV1_ListItem[];
  /**
   * Response only.
   */
  latest?: string | null;
  /**
   * Response only.
   */
  intraday_latest?: string | null;
};
/**
 * Concrete export id: `night:YYYY-MM-DD` or `intraday:YYYY-MM-DDTHHMM` (trading day and MSK moment, no separators in the time).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsScreenerChannelV1_ExportId".
 */
export type AfbwsScreenerChannelV1_ExportId = string;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsScreenerChannelV1_ExportKind".
 */
export type AfbwsScreenerChannelV1_ExportKind = 'night' | 'intraday';
/**
 * Request carries `id` (export id or alias). Response echoes the concrete `id` (aliases resolved) and `kind`, and carries `document`: the export content as is (contract v1), an open object. Unknown export: error `not_found`; malformed id: `invalid_schema`; unreadable file: `internal_error`; unsupported `contract_version`: `unsupported_action`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerV1Get".
 */
export type ScreenerV1Get = {
  [k: string]: unknown;
} & {
  channel: 'screener';
  schema: 'afbws.screener.get.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * Request: export id or alias. Response: concrete export id.
   */
  id: string;
  /**
   * Response only.
   */
  kind?: 'night' | 'intraday';
  /**
   * Response only. Screener export content as is; see AFB/docs/SCREENER_RESULTS.md.
   */
  document?: {
    contract_version?: number;
    [k: string]: unknown;
  };
};
/**
 * Request is an empty command (no parameters in this version; `request_id` is required). Response carries `received_at`, `tz`, `collections`, `derivatives` (reference table) and `lists` (four columnar snapshots: now, d1, d2, w1). Server push: after each refresh of the FORTS positions (about every 5 minutes) the backend sends the same message with the full body and WITHOUT `request_id` to every connection that has requested `participants` at least once; there is no unsubscribe, the subscription ends with the connection. Access: tier `manager` or `user`, otherwise `forbidden`. Non-manager sees only derivatives visible to their tier.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerV1Participants".
 */
export type ScreenerV1Participants = {
  [k: string]: unknown;
} & {
  channel: 'screener';
  schema: 'afbws.screener.participants.v1';
  request_id?: AfbwsCommonV1_RequestId;
  /**
   * Response only.
   */
  received_at?: string;
  /**
   * Response only. Time zone of asof, e.g. Europe/Moscow.
   */
  tz?: string;
  /**
   * Response only.
   */
  collections?: ScreenerV1ParticipantsCollection[];
  derivatives?: ScreenerV1ParticipantsDerivatives;
  /**
   * Response only.
   */
  lists?: ScreenerV1ParticipantsList[];
};
/**
 * Same list and order as afbws.instrument.channel.v2 favoriteColor (kept in lockstep; no cross-reference on purpose).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsScreenerChannelV1_FavoriteColor".
 */
export type AfbwsScreenerChannelV1_FavoriteColor =
  'yellow' | 'red' | 'blue' | 'green' | 'gray' | 'orange' | 'cyan' | 'purple' | 'pink' | 'teal';
/**
 * Export id or alias: `latest` (newest night export) / `intraday_latest` (newest intraday snapshot).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsScreenerChannelV1_ExportRef".
 */
export type AfbwsScreenerChannelV1_ExportRef = string;
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.tradeplan.channel.v2). Same convention as afbws.alarm/account/market v2: ONE schema id per message (`afbws.tradeplan.<op>.v2`, no .request/.response/.push suffixes); the same schema is the request and its response (a response echoes `request_id`), and the server push `sync` is the same kind of message without `request_id`. Collections are arrays (`items[]`, `ids[]`, `instrument_keys[]`), so bulk operations are single messages; per-plan failures of a batch come back in `rejected[]`, `error` is only for a whole request. There is no separate `get`: use `list` with `ids`. Two plan shapes: `planInput` (what the client sends in `set` — the plan the user edits, NOT server-owned fields) and `planItem` (what the server returns — the stored plan minus `delivery_at`/`archived_components`/`archived_at`/`editor`, plus `instrument_missing`). Both are projections of the AFB-internal storage schema `../tradeplan.v2.json` (afb.tradeplan.v2), which stays the single source for the condition vocabulary; this channel schema is strict (additionalProperties:false) and carries no legacy forms: `leg_id` is never the synthetic `legacy:{role}:{index}`, `op` is mandatory on every condition, `schema` is mandatory, `instrument_key` is mandatory on input and on output either present or replaced by `instrument_missing:true`. See AFB/docs/ENTITY_WS_PROTOCOL.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanChannelV2Message".
 */
export type TradeplanChannelV2Message =
  TradeplanV2List | TradeplanV2Set | TradeplanV2Delete | TradeplanV2Archive | TradeplanV2Sync | TradeplanV2Error;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_ConditionOp".
 */
export type TradeplanV2_ConditionOp =
  'touch' | 'above' | 'below' | 'crosses_above' | 'crosses_below' | 'crossing' | 'breakout' | 'breakdown';
/**
 * `condition.v1.json#/$defs/immediateExpr` (market entry) is valid only on an entry leg — enforced after compilation by deal.v2.json/BF, not here, same as the rest of this schema's left/right pairing.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_ConditionLeft".
 */
export type TradeplanV2_ConditionLeft =
  ConditionV1_PriceExpr | ConditionV1_IndicatorExpr | ConditionV1_DatasetExpr | ConditionV1_ImmediateExpr;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_ConditionRight".
 */
export type TradeplanV2_ConditionRight =
  ConditionV1_RightConst | ConditionV1_IndicatorExpr | ConditionV1_DatasetExpr | TradeplanV2_PrimitiveRef;
/**
 * Request: `ids[]` (at least one). Response (same `request_id`): `items[]` — the archived plans (status `archived`) — and `rejected[]` (a plan with a live deal that already entered a position is rejected with `conflict` and its current `item`). Exactly one of `ids` / `items`. Archival is also delivered as a single `sync` push (all archived plans in one message) to the user's other connections.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2Archive".
 */
export type TradeplanV2Archive = {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.archive.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  ids?: [TradeplanId, ...TradeplanId[]];
  items?: TradeplanV2PlanItem[];
  rejected?: TradeplanV2Rejection[];
} & TradeplanV2Archive1;
export type TradeplanV2Archive1 = {
  [k: string]: unknown;
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV1_AlarmConditionNode".
 */
export type AlarmV1_AlarmConditionNode =
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op?: 'touch';
    }
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op: 'breakout' | 'breakdown' | 'crossing';
      timeframe: ConditionV1_Timeframe;
    }
  | {
      left?: ConditionV1_PriceExpr;
      right?: ConditionV1_RightConst;
      op: ConditionV1_PriceLevelOp;
    }
  | {
      left?: AlarmV1_AlarmIndicatorExpr;
      right?: ConditionV1_RightConst | AlarmV1_AlarmIndicatorExpr;
      op: ConditionV1_ScalarOp;
    }
  | {
      left?: ConditionV1_DatasetExpr;
      right?: ConditionV1_RightConst | ConditionV1_DatasetExpr;
      op: ConditionV1_ScalarOp;
    };
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2_ExitList".
 */
export type DealV2_ExitList = {
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
  condition: DealV2_ConditionNode;
  source?: DealV2_LegSource;
}[];
/**
 * AFB-side chart primitive (line/line_enter/line_sl/line_tp/note/zone/ruler) — like afb.alarm.v1, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel. Promotes the parked settings.primitives[secid][] draft (draft/primitive.v1.json) into a strict canonical entity: `ticker` becomes an explicit required field instead of an implicit dict key, so get(id)/list(ticker) work on a flat collection. Whether a primitive is REFERENCED BY a tradeplan's condition is still derived fresh from the tradeplans themselves on every read, never persisted here. OWNERSHIP is different and is persisted — see `tradeplan_id`. `stop` is a second anchor point required only for zone/ruler (forbidden for every other kind, enforced by the `allOf` below, not just by convention); `text` is accepted only for `note` (optional even there).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV1".
 */
export type GpV1 = {
  [k: string]: unknown;
};
/**
 * AFB-side multi-entry / multi-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v2. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `direction` (long/short) is the single source of truth for position bias, at plan level — entry legs do not carry a per-leg side (a list of entries with independent buy/sell sides has no defined execution semantics for one deal). Conditions are deal.v2-compatible nodes — price legs carry an explicit `op` (touch/above/below/breakout/breakdown/crossing), `op` omitted on a price leg means touch (accepted for back-compat with old plans); indicator legs may omit `op`, derived from direction/scope at compile time — with two extensions beyond condition.v1.json's plain vocabulary: (1) the `right` side of a condition may be a `primitiveRef` (`{"primitive_id": "..."}`), a reference to a chart line primitive that AFB resolves to a decimal `const` at compile time; (2) an entry leg's `left` may be `condition.v1.json#/$defs/immediateExpr` (`{"source": "immediate"}`) for a market entry — `right`/`op` are structural placeholders in that case, same convention as the compiled deal (see deal.v2.json's conditionNode, immediate branch of condition.v1.json#/$defs/conditionNode): dispatch on `left.source == "immediate"` alone, never read `right`/`op`. Meaningful only on entries — AFB/BF reject it on stop_loss/take_profit. The full left/right pairing matrix (price/quote const-only, indicator/dataset const-or-same-kind) is enforced after compilation by deal.v2.json and by BF, not here — this schema deliberately stays loose to accommodate primitiveRef and immediateExpr. Each leg additionally carries an optional `logic` (`split`/`and`/`or`, see deal.v2.json#/$defs/legJoin for the full grammar) joining it to the preceding leg; AFB carries the field through compilation unchanged onto the corresponding deal.v2 leg.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradePlanV2".
 */
export type TradePlanV2 = {
  [k: string]: unknown;
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_TpExitList".
 */
export type TradeplanV2_TpExitList = TradeplanV2_TpLeg[];

/**
 * Request: only `request_id`. Response: `tiers[]`, `members[]`, `capabilities[]`, `getcourse_groups[]`, `getcourse_groups_error`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1RolesGet".
 */
export interface AccessV1RolesGet {
  channel: 'access';
  schema: 'afbws.access.roles.get.v1';
  request_id: AfbwsCommonV1_RequestId;
  tiers?: AccessV1TierRow[];
  members?: AccessV1Member[];
  /**
   * Response only: capability names (the set is defined by the backend code).
   */
  capabilities?: string[];
  /**
   * Response only: GetCourse groups (hints for choosing a `gc:` token).
   */
  getcourse_groups?: AccessV1GetcourseGroup[];
  /**
   * Response only: why GetCourse groups could not be fetched; null — fetched.
   */
  getcourse_groups_error?: string | null;
}
/**
 * One tier (one row of the `tiers` table).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1TierRow".
 */
export interface AccessV1TierRow {
  tier: AccessTier;
  /**
   * Label shown in the manager UI.
   */
  title: string;
  /**
   * Priority when a user matches several tiers (higher wins); unique among tiers. The tier with the minimal rank is the default for users not matched by any member.
   */
  rank: number;
  /**
   * Paid subscription: subscription periods are logged on login, the tier counts in conversion.
   */
  paid: boolean;
  limits: AccessLimits;
  /**
   * Mode policy; null — always `full` with its own limits.
   */
  policy: null | AccessV1Policy;
}
/**
 * Effective per-user limits (enforced only when ADDING objects; existing objects above a limit are never deleted or truncated). Keys mirror AFB backend/users/roles_loader.py LIMIT_KEYS.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessLimits".
 */
export interface AccessLimits {
  max_favorites_tickers: number;
  max_primitives_per_user: number;
  max_sets: number;
  max_favorite_colors: number;
}
/**
 * Mode policy of a tier (`tiers.policy` in the backend's access database). A tier WITH a policy is `full` (with the limits of `as_tier`) while a manual grant, the trial, a time window (stage 3: a showcase instrument) is active, otherwise `basic` with its own limits. A tier without a policy (null) is always `full` with its own limits. The `trade` capability and a paid tier are always `full`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Policy".
 */
export interface AccessV1Policy {
  as_tier: AccessTier;
  /**
   * Trial length in days; 0 or absent = no trial.
   */
  trial_days?: number;
  /**
   * Window of a trading day (MOEX calendar); null or absent = no window.
   */
  workday?: null | AccessV1Window;
  /**
   * Window of a non-trading day (MOEX calendar); null or absent = no window.
   */
  weekend?: null | AccessV1Window;
  showcase?: AccessV1Showcase;
}
/**
 * Daily time window, Moscow time: `from` — start, `to` — end. `to` < `from` = across midnight (e.g. 22:00-02:00).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Window".
 */
export interface AccessV1Window {
  from: string;
  to: string;
}
/**
 * Instrument showcase (stage 3): instruments of the global catalog collection `collection` work as in `full`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Showcase".
 */
export interface AccessV1Showcase {
  enabled: boolean;
  /**
   * Id of a global catalog collection; null — not chosen.
   */
  collection: string | null;
}
/**
 * Who gets a tier or a capability (one row of the `members` table).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Member".
 */
export interface AccessV1Member {
  /**
   * A tier name (from `tiers`) or a capability name (set defined by the backend code).
   */
  role: string;
  /**
   * `id_<id>` — local user, `gc_<id>` — GetCourse user, `gc:<group id>` — GetCourse group.
   */
  token: string;
}
/**
 * GetCourse group (a member token references it as `gc:<id>`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1GetcourseGroup".
 */
export interface AccessV1GetcourseGroup {
  id: string;
  title: string;
}
/**
 * Request: `tiers[]` (at least one; `tier` names must be unique — checked by the server) and `members[]` — replace-all of both tables. Response: the saved snapshot, as afbws.access.roles.get.v1.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1RolesSet".
 */
export interface AccessV1RolesSet {
  channel: 'access';
  schema: 'afbws.access.roles.set.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * Tier names must be unique (JSON Schema cannot express uniqueness by key — the server rejects duplicates with validation_error).
   *
   * @minItems 1
   */
  tiers: [AccessV1TierRow, ...AccessV1TierRow[]];
  members: AccessV1Member[];
  /**
   * Response only: capability names (the set is defined by the backend code).
   */
  capabilities?: string[];
  /**
   * Response only: GetCourse groups (hints for choosing a `gc:` token).
   */
  getcourse_groups?: AccessV1GetcourseGroup[];
  /**
   * Response only: why GetCourse groups could not be fetched; null — fetched.
   */
  getcourse_groups_error?: string | null;
}
/**
 * Request: only `request_id`. Response: `items[]` — every user who has logged in at least once (no server-side filtering or paging).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1UsersList".
 */
export interface AccessV1UsersList {
  channel: 'access';
  schema: 'afbws.access.users.list.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * Response only.
   */
  items?: AccessV1UserRow[];
}
/**
 * One user who has logged in at least once (row of the `users` table + resolved tier/capabilities + the last subscription period).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1UserRow".
 */
export interface AccessV1UserRow {
  user_id: string;
  display_name: string | null;
  tier: AccessTier;
  capabilities: string[];
  first_seen_at: string;
  last_seen_at: string;
  /**
   * null — the trial has never been given.
   */
  trial_started_at: string | null;
  /**
   * `full` until this moment (trial).
   */
  trial_ends_at: string | null;
  /**
   * Manual extension: `full` until this moment; null — none.
   */
  grant_until: string | null;
  /**
   * The last paid subscription period; null — never subscribed.
   */
  subscription: null | AccessV1Subscription;
}
/**
 * One paid subscription period (row of the `subscriptions` table).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Subscription".
 */
export interface AccessV1Subscription {
  tier: AccessTier;
  started_at: string;
  /**
   * null — active.
   */
  ended_at: string | null;
}
/**
 * Request: `user_id` + `trial_ends_at` and/or `grant_until` (at least one; null removes). The first `trial_ends_at` for a user without a trial (`trial_started_at` null) also sets `trial_started_at` = now. Response: `user_id` + `item` — the updated row. Unknown user -> error `not_found`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1UserSet".
 */
export interface AccessV1UserSet {
  channel: 'access';
  schema: 'afbws.access.user.set.v1';
  request_id: AfbwsCommonV1_RequestId;
  user_id: string;
  /**
   * Request only: new trial end; null — remove the trial end.
   */
  trial_ends_at?: string | null;
  /**
   * Request only: manual grant until; null — remove the grant.
   */
  grant_until?: string | null;
  item?: AccessV1UserRow;
}
/**
 * Request: `from`, `to` (dates, inclusive, Moscow). Response echoes `from`/`to` and carries `weeks[]` (oldest first), one per calendar week intersecting the range. `new_users` — users whose `first_seen_at` falls in the week; `trials_started` — users whose `trial_started_at` falls in the week; `converted` — paid subscription periods started in the week; `active` — users whose `last_seen_at` falls in the week.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Stats".
 */
export interface AccessV1Stats {
  channel: 'access';
  schema: 'afbws.access.stats.v1';
  request_id: AfbwsCommonV1_RequestId;
  from: string;
  to: string;
  /**
   * Response only.
   */
  weeks?: AccessV1StatsWeek[];
}
/**
 * One calendar week of conversion statistics.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1StatsWeek".
 */
export interface AccessV1StatsWeek {
  /**
   * Monday of the week.
   */
  week: string;
  new_users: number;
  trials_started: number;
  converted: number;
  active: number;
}
/**
 * Sent without `request_id` when the effective access changes (mode switch at `until`, a manager's change of tiers/members/trial/grant). Carries the whole new `access` block; the client replaces the one from auth.ok.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1State".
 */
export interface AccessV1State {
  channel: 'access';
  schema: 'afbws.access.state.v1';
  access: Access;
}
/**
 * Answer to a request of any schema-first channel that the current `mode` does not allow. `channel` is the channel of the REFUSED request and `request_id` echoes it, so the per-channel request/response client rejects the pending request. `reason`: `basic` — feature not available in basic mode; `showcase` — basic mode with showcase, the instrument is not in the showcase; `held` — activation of an alarm/trade plan while the owner's objects are held. `feature` — gate feature id (e.g. `datasets`, `participants`, `virtual`, `screener`, `alarm.activate`). `until` — when `full` becomes available (next window/trial), null if unknown. `message` — ready-to-show text.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Denied".
 */
export interface AccessV1Denied {
  /**
   * Channel of the refused request.
   */
  channel: string;
  schema: 'afbws.access.denied.v1';
  request_id: AfbwsCommonV1_RequestId;
  reason: 'basic' | 'showcase' | 'held';
  feature: string;
  until: string | null;
  message: string;
}
/**
 * `code` is a closed subset of common errorCode: `forbidden` (not a manager), `validation_error`, `not_found` (unknown user), `invalid_channel`, `invalid_schema`, `internal_error`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccessV1Error".
 */
export interface AccessV1Error {
  channel: 'access';
  schema: 'afbws.access.error.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: 'forbidden' | 'validation_error' | 'not_found' | 'invalid_channel' | 'invalid_schema' | 'internal_error';
  message: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2Snapshot".
 */
export interface AccountV2Snapshot {
  bf_id: AccountV2BfId;
  account_id: AccountV2AccountId;
  /**
   * True only for this bf_id's default (trading) account.
   */
  tradable: boolean;
  readonly: boolean;
  status: 'ok' | 'stale' | 'error';
  equity: string | null;
  cash: PayloadsBrokerAccounts_CashBalance[];
  positions: AfbwsAccountChannelV2_Position[];
  as_of?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerAccounts_CashBalance".
 */
export interface PayloadsBrokerAccounts_CashBalance {
  currency: string;
  value: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsAccountChannelV2_Position".
 */
export interface AfbwsAccountChannelV2_Position {
  quantity: number;
  average_price: string;
  current_price?: string | null;
  unrealized_pnl?: string | null;
  /**
   * Instrument block restored by AFB; optional.
   */
  instrument?: {};
  broker_ref?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2Order".
 */
export interface AccountV2Order {
  order_id: string;
  deal_id?: string;
  symbol?: string;
  side?: string;
  role?: string;
  status?: string;
  quantity?: number;
  filled_quantity?: number;
  leg_index?: number;
  limit_price?: string | null;
  average_price?: string | null;
  client_order_id?: string;
  cancel_source?: 'system' | 'broker';
  updated_at?: string;
  error_code?: string | null;
  error_message?: string | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2EventRecord".
 */
export interface AccountV2EventRecord {
  logged_at: string;
  bf_id: AccountV2BfId;
  deal_id?: string | null;
  category: 'deal' | 'order' | 'position' | 'condition';
  event: string;
  data?: {} | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountV2Error".
 */
export interface AccountV2Error {
  channel: 'account';
  schema: 'afbws.account.error.v2';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
}
/**
 * Request: optional filters `ids[]` and/or `instrument_keys[]` (both = intersection; none = every alarm of the caller). Response (same `request_id`): `items[]` (afb.alarm.v2). There is no separate `get`: use `ids`. A request carrying `items` is invalid.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2List".
 */
export interface AlarmV2List {
  channel: 'alarm';
  schema: 'afbws.alarm.list.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  ids?: [string, ...string[]];
  /**
   * @minItems 1
   */
  instrument_keys?: [AfbwsCommonV1_InstrumentKey, ...AfbwsCommonV1_InstrumentKey[]];
  items?: AlarmV2[];
}
/**
 * v2 of afb.alarm.v1 (full copy): the only difference is that the instrument is identified by the full composite `instrument_key` (<MIC>[:<board|market>]:<ticker>, case-sensitive, never normalized — see afbws/common.v1.json#/$defs/instrumentKey) instead of the short `ticker`. v1 stays supported for frontends that did not negotiate afbws.alarm.channel.v2; the backend stores v2 and converts v1<->v2 at the channel boundary. AFB-side entity, NOT an AsyncAPI wire message, never crosses the AFB<->BF channel. it is documented here (rather than only in AFB) because it shares condition.v1.json's operator vocabulary with deal.v2 and tradeplan.v2. Replaces the legacy YAML shape (condition_type/trigger_type/value_type/value/value_ref flat fields, break_up/break_down operator names) with a conditionNode. Legacy alarms are read via a lazy converter (see docs/PROTOCOL.md 'Алармы' mapping table) and rewritten in this format on next save/reactivation; the API layer only accepts/emits this format going forward. `period` is the alarm's overall computation timeframe (legacy default '10min'); when `condition` is a price candle operator, `condition.timeframe` carries the candle timeframe and by construction equals `period`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2".
 */
export interface AlarmV2 {
  schema: 'afb.alarm.v2';
  id: string;
  instrument_key: AfbwsCommonV1_InstrumentKey;
  condition: AlarmV2_AlarmConditionNode;
  period?: ConditionV1_Timeframe;
  trigger_frequency?: 'once' | 'every_candle' | 'daily';
  status?: 'active' | 'triggered' | 'expired';
  created_at?: string;
  updated_at?: string;
  triggered_at?: string;
  delivery_at?: string;
  trigger_count?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_PriceExpr".
 */
export interface ConditionV1_PriceExpr {
  source: 'price';
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_RightConst".
 */
export interface ConditionV1_RightConst {
  const: DecimalString;
}
/**
 * Unlike condition.v1.json#/$defs/indicatorExpr, only `source`+`id` are required: AFB resolves `type`/`field`/`params` from the user's saved indicator settings by `id` rather than carrying them inline.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2_AlarmIndicatorExpr".
 */
export interface AlarmV2_AlarmIndicatorExpr {
  source: 'indicator';
  id: string;
  type?: 'wma' | 'kama' | 'psar';
  field?: string;
  params?: {};
}
/**
 * position.* / orders / hhi / trades datasets share this shape; dataset_id=volume is declared here but temporarily unsupported by AFB/BF backends (see condition_semantics module docstring) and not offered by the UI.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_DatasetExpr".
 */
export interface ConditionV1_DatasetExpr {
  source: 'dataset';
  field: string;
  dataset_id?: string;
  params?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2Rejection".
 */
export interface AlarmV2Rejection {
  id: string;
  code: AfbwsCommonV1_ErrorCode;
  message?: string;
  details?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2AckEvent".
 */
export interface AlarmV2AckEvent {
  schema: 'afb.alarm.trigger_ack.v2';
  alarm_id: string;
  triggered_at: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2AckResultItem".
 */
export interface AlarmV2AckResultItem {
  schema: 'afbws.alarm.ack_result.v2';
  alarm_id: string;
  triggered_at: string;
  status: 'ok' | 'not_found';
}
/**
 * Server-initiated; `events[]` carry the fired alarm with its authoritative afb.alarm.v2 record.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2Triggered".
 */
export interface AlarmV2Triggered {
  channel: 'alarm';
  schema: 'afbws.alarm.triggered.v2';
  /**
   * @minItems 1
   */
  events: [AlarmV2TriggerEvent, ...AlarmV2TriggerEvent[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2TriggerEvent".
 */
export interface AlarmV2TriggerEvent {
  schema: 'afb.alarm.trigger.v2';
  alarm_id: string;
  triggered_at: string;
  alarm: AlarmV2;
  current_price?: number;
}
/**
 * Per-item failures of a batched set/delete are reported in that response's `rejected[]`, not here.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV2Error".
 */
export interface AlarmV2Error {
  channel: 'alarm';
  schema: 'afbws.alarm.error.v2';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
}
/**
 * The session is taken from the `afb_session` cookie, or from `session_id` when the cookie is absent/invalid. `version` (frontend build) is logged for monitoring only — never parsed, compared or used to gate behaviour; all behaviour is gated on `support` alone. `demo: true` = demo login (guest profile, GetCourse skipped).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AuthV1Request".
 */
export interface AuthV1Request {
  channel: 'auth';
  schema: 'afbws.auth.request.v1';
  /**
   * Frontend build version, logged only.
   */
  version: string;
  demo?: boolean;
  /**
   * afbws capability ids the client supports (x-afbws-support-id values).
   */
  support: string[];
  /**
   * HTTP session id, used when the cookie is unavailable.
   */
  session_id?: string;
}
/**
 * `support` — the backend's own declared afbws capability ids (not the intersection; the client computes it). `brokers` — known broker ids for the link connector-create form, sent unconditionally. `access` — effective access of this connection (tier / capabilities / limits / mode ...), see common.v1.json#/$defs/access; later changes arrive as afbws.access.state.v1 pushes.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AuthV1Ok".
 */
export interface AuthV1Ok {
  channel: 'auth';
  schema: 'afbws.auth.ok.v1';
  user_id: string;
  /**
   * IANA timezone name of the platform (e.g. `Europe/Moscow`).
   */
  timezone: string;
  support: string[];
  brokers: string[];
  access: Access;
}
/**
 * `unauthorized` — no valid session (close code 4001); `session_invalid` — the session exists but its access profile could not be resolved (close code 4001); `invalid_request` — the first message is not a valid auth request (close code 4000).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AuthV1Error".
 */
export interface AuthV1Error {
  channel: 'auth';
  schema: 'afbws.auth.error.v1';
  code: 'unauthorized' | 'invalid_request' | 'session_invalid';
  message: string;
}
/**
 * Shared public-view basis for `bfs` (registry push) and `connector` (record CRUD) — see BFRegistryEntry.to_public_dict() in AFB/backend/trade/models.py.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BfRegistryEntry".
 */
export interface BfRegistryEntry {
  bf_id: string;
  name: string;
  enabled: boolean;
  broker: string;
  protocol: string;
}
/**
 * See AFB/docs/WS_EXECUTION_CHANNELS.md#bfs--registry and ExecutionService.accessible_bfs_map (AFB/backend/trade/service.py) — extends the public registry-entry minimum with runtime keys.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BfsRegistryPush".
 */
export interface BfsRegistryPush {
  type: 'registry';
  data: {
    bfs: BfsRegistryEntry[];
  };
}
/**
 * `asset_ids`, when present, is the WHOLE ordered composition of the collection (the assets filed into it); an asset lives in at most one collection, so naming it here moves it. In a snapshot `asset_ids` is always present. Omit in a commit to leave the composition untouched.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Collection".
 */
export interface AfbwsCatalogChannelV1_Collection {
  id: string;
  name: string;
  parent_id?: string | null;
  /**
   * Omitted: unchanged. null: clears the icon.
   */
  icon_id?: string | null;
  /**
   * Omitted: unchanged. null: clears the color.
   */
  icon_color?: AfbwsCatalogChannelV1_FavoriteColor | null;
  asset_ids?: string[];
}
/**
 * `type` is decided on create (default `asset`); on update it must equal the stored one. A set of type `asset` carries `asset_ids[]`, of type `instrument` carries `instrument_keys[]`; the list, when present, is the WHOLE composition in its final order.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Set".
 */
export interface AfbwsCatalogChannelV1_Set {
  id: string;
  name: string;
  type?: 'asset' | 'instrument';
  visibility_tier?: 'manager' | 'user' | 'guest';
  /**
   * Omitted: unchanged. null: clears the icon.
   */
  icon_id?: string | null;
  /**
   * Omitted: unchanged. null: clears the color.
   */
  icon_color?: AfbwsCatalogChannelV1_FavoriteColor | null;
  asset_ids?: string[];
  instrument_keys?: AfbwsCommonV1_InstrumentKey[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_SnapshotAsset".
 */
export interface AfbwsCatalogChannelV1_SnapshotAsset {
  id: string;
  name: string;
  collection_id: string | null;
  members: AfbwsCatalogChannelV1_MemberExisting[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_MemberExisting".
 */
export interface AfbwsCatalogChannelV1_MemberExisting {
  kind: 'listing' | 'derivative';
  ref: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Listing".
 */
export interface AfbwsCatalogChannelV1_Listing {
  instrument_key: AfbwsCommonV1_InstrumentKey;
  mic: string;
  board?: string | null;
  market: string;
  ticker: string;
  name: string;
  shortname?: string | null;
  currency?: string | null;
  decimals?: number | null;
  lot_size?: number | null;
  /**
   * Decimal string, never a float.
   */
  price_step?: string | null;
  /**
   * Decimal string, never a float.
   */
  step_price?: string | null;
  expiration?: string | null;
  isin?: string | null;
  derivative?: string | null;
  source: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Derivative".
 */
export interface AfbwsCatalogChannelV1_Derivative {
  code: string;
  kind: string;
  name: string;
  underlying_key?: AfbwsCommonV1_InstrumentKey | null;
  source: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_SourceStatus".
 */
export interface AfbwsCatalogChannelV1_SourceStatus {
  source: AfbwsCatalogChannelV1_Source;
  title: string;
  available: boolean;
  state: string;
  /**
   * A refresh of this source is already queued for the daily cycle.
   */
  pending: boolean;
  last_refresh_at?: string | null;
  last_error?: string | null;
  symbols?: number | null;
  listings?: number | null;
  unlinked?: number | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_SymbolRow".
 */
export interface AfbwsCatalogChannelV1_SymbolRow {
  ref: string;
  kind: 'listing' | 'derivative';
  ticker: string;
  name: string;
  market: 'stock' | 'currency' | 'index' | 'futures' | 'other';
  mic?: string | null;
  archived: boolean;
  in_catalog?: AfbwsCommonV1_InstrumentKey | null;
  addable: boolean;
  reason?: 'unsupported_type' | 'archived' | null;
}
/**
 * `members`, when present, is the WHOLE composition in its final order (no add/remove form). Omit to leave it untouched; `[]` empties the asset. In a snapshot `members` and `collection_id` are always present.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Asset".
 */
export interface AfbwsCatalogChannelV1_Asset {
  id: string;
  name: string;
  collection_id?: string | null;
  members?: AfbwsCatalogChannelV1_Member[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_MemberNew".
 */
export interface AfbwsCatalogChannelV1_MemberNew {
  kind: 'listing' | 'derivative';
  source: AfbwsCatalogChannelV1_Source;
  ref: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_ArchiveItem".
 */
export interface AfbwsCatalogChannelV1_ArchiveItem {
  instrument_key: AfbwsCommonV1_InstrumentKey;
  reason?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Rejection".
 */
export interface AfbwsCatalogChannelV1_Rejection {
  source: AfbwsCatalogChannelV1_Source;
  code: 'source_unavailable' | 'forbidden';
  message?: string;
}
/**
 * `details`: `catalog_revision` for `conflict`; `refs[]` (`{source, ref, code, message}`) naming the rejected new members of a commit; `source` for `source_unavailable`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_Error".
 */
export interface AfbwsCatalogChannelV1_Error {
  channel: 'catalog';
  schema: 'afbws.catalog.error.v1';
  request_id?: AfbwsCommonV1_RequestId;
  code:
    | 'forbidden'
    | 'invalid_schema'
    | 'invalid_channel'
    | 'unsupported_action'
    | 'validation_error'
    | 'not_found'
    | 'conflict'
    | 'internal_error'
    | 'unsupported_type'
    | 'no_market_data'
    | 'source_unavailable';
  message: string;
  details?: {
    [k: string]: unknown;
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCatalogChannelV1_RefreshResult".
 */
export interface AfbwsCatalogChannelV1_RefreshResult {
  source: AfbwsCatalogChannelV1_Source;
  state: 'done' | 'failed';
  finished_at: string;
  received?: number | null;
  summary?: string | null;
  error?: string | null;
  revision?: number | null;
}
/**
 * Shared building blocks for the schema-first afbws channels introduced alongside `deal`/`connector`/`bfs`/`account` (see afbws/README convention in CLAUDE.md): a request/response correlation id and a typed error vocabulary. Unlike the legacy afbws channels (discriminated by a `type` const), schema-first channels are routed by `channel` then by a mandatory top-level `schema` id — no `type` field.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCommonV1_Root".
 */
export interface AfbwsCommonV1_Root {
  [k: string]: unknown;
}
/**
 * Canon of the user settings carried by `afbws.config.settings.v1` (root = the `settings` object) and of the platform defaults carried by `afbws.config.defaults.v1` (`$defs/defaults`). Replaces the parked `draft/` schemas and the legacy `settings` channel payload. Every property is optional: the on-disk user file stores only what the user overrode and a write is a partial patch (blocks `profile`/`interface`/`dataset`/`dashboard`/`form`/`participants` are deep-merged (arrays such as `participants.columns` are replaced whole), `trade` is replaced whole). Not part of the payload any more: `limits` (travels in `auth_ok`), `favorites` (channel `instrument`), `indicators`/`primitives` (channel `gp`), alarms/tradeplans (their own channels). Booleans are real JSON booleans.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigSettingsV1".
 */
export interface ConfigSettingsV1 {
  profile?: ConfigProfile;
  interface?: ConfigInterface;
  dataset?: ConfigDataset;
  dashboard?: ConfigDashboard;
  trade?: ConfigTrade;
  form?: ConfigV1_Form;
  participants?: ConfigV1_Participants;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigProfile".
 */
export interface ConfigProfile {
  /**
   * Read-only display name (server-side source: user registry). Present in responses/pushes when set; a client write is ignored.
   */
  name?: string;
  email?: string;
  telegram?: string;
  notify_telegram?: boolean;
  notify_email?: boolean;
  /**
   * System stability notifications (afb.notification.system.v1) — manager role only; a write from any other role is ignored by the server.
   */
  notify_system?: boolean;
  /**
   * Notification sound id, e.g. 'game/coin'.
   */
  sound?: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigInterface".
 */
export interface ConfigInterface {
  layout?: ConfigLayout;
  snow_mode?: boolean;
  /**
   * Where the per-service form switches (`settings.form.*`) are stored: `server` — in the user file (default), `local` — in the browser's localStorage under identical `form.*` keys. This value itself is always stored on the server.
   */
  settings_storage?: 'server' | 'local';
  /**
   * Exchange chart rendering: `candles` — Japanese candlesticks (default), `bars` — OHLC bars.
   */
  chart_type?: 'candles' | 'bars';
  smart_alarms?: boolean;
  preset_timeframes?: {
    positions?: string;
    trades?: string;
    hhi?: string;
    orders?: string;
    [k: string]: unknown;
  };
  chart_toolbar?: ConfigV1_ChartToolbar;
  services_filters?: ConfigV1_ServicesFilters;
  trade_plan_default_capital_rub?: number;
  /**
   * Days-to-expiration threshold the frontend uses to pick the front futures contract of a derivative: the member with the minimum expiration not earlier than today + N. Default 2, matching `securities.days_to_expiration` in AFB's `config/afb.yaml`.
   */
  futures_days_to_expiration?: number;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigLayout".
 */
export interface ConfigLayout {
  offset_right?: number;
  offset_top?: number;
  debug_mode?: boolean;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigV1_ChartToolbar".
 */
export interface ConfigV1_ChartToolbar {
  favorite_timeframes?: string[];
  /**
   * Elements are either `dataset-<preset>` keys or indicator ids.
   */
  favorite_datasets?: string[];
  /**
   * Primitive kind values (gp.v2.json).
   */
  favorite_primitives?: string[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigV1_ServicesFilters".
 */
export interface ConfigV1_ServicesFilters {
  instruments?: {
    markets?: string[];
    [k: string]: unknown;
  };
  alarms?: {
    statuses?: string[];
    [k: string]: unknown;
  };
  plans?: {
    statuses?: string[];
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * Freeform per-series style config (color/style/panel triplets, e.g. positions.longColor, trades.tradesBColor). Keys vary per series and grow as new series are added — deliberately open string/number maps rather than enumerating dozens of purely presentational keys.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigDataset".
 */
export interface ConfigDataset {
  positions?: {
    [k: string]: string | number;
  };
  trades?: {
    [k: string]: string | number;
  };
  hhi?: {
    [k: string]: string | number;
  };
  orders?: {
    [k: string]: string | number;
  };
  [k: string]: unknown;
}
/**
 * `cols` is clamped 8-24 by the frontend normalizer rather than enforced here.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigDashboard".
 */
export interface ConfigDashboard {
  cols?: number;
  breakpoints?: {
    lg?: number;
    xl?: number;
    [k: string]: unknown;
  };
  layouts?: {
    lg?: ConfigV1_DashboardLayoutItem[];
    [k: string]: unknown;
  };
  widgets?: {
    [k: string]: {
      bf_id?: string;
      order_filter?: string;
      deal_status_filters?: string[];
      exchange?: string;
      market?: string;
      events_date?: string;
      [k: string]: unknown;
    };
  };
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigV1_DashboardLayoutItem".
 */
export interface ConfigV1_DashboardLayoutItem {
  widget?: string;
  /**
   * Accepted wire synonym of `widget`.
   */
  i?: string;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
  [k: string]: unknown;
}
/**
 * `default_capital` is persisted by the server into the user's virtual account, not into the settings file; reads return the live value.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigTrade".
 */
export interface ConfigTrade {
  default_connector?: string;
  default_capital?: number;
  /**
   * Default risk_factor (%) for a newly created trade plan.
   */
  default_risk_pct?: number;
  notify?: ConfigV1_TradeNotify;
  chart_deal_markers?: boolean;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigV1_TradeNotify".
 */
export interface ConfigV1_TradeNotify {
  trigger?: boolean;
  order_placed?: boolean;
  order_executed?: boolean;
  position?: boolean;
  close?: boolean;
  link?: boolean;
  [k: string]: unknown;
}
/**
 * Stored here when `interface.settings_storage` is `server`; otherwise the same keys (`form.<service>.<name>`) live in localStorage.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigV1_Form".
 */
export interface ConfigV1_Form {
  alarms?: {
    /**
     * Ask for confirmation before deleting an alarm (default true).
     */
    confirm_delete?: boolean;
  };
  primitives?: {
    /**
     * Ask for confirmation before deleting a graphic primitive (default true).
     */
    confirm_delete?: boolean;
  };
  plans?: {
    /**
     * Activate the deal automatically after a plan is published (default false).
     */
    auto_execute?: boolean;
    /**
     * Plan editor is placed beside the list (left) instead of over it (default true).
     */
    editor_left?: boolean;
    /**
     * Hide commercial information when opening the plan description for copying (default false).
     */
    hide_on_share?: boolean;
    /**
     * Show the 'Risk and volume' section first in the plan modal (default true).
     */
    risk_top?: boolean;
  };
  participants?: {
    /**
     * Use the recommended column set and order in the 'Market participants' service (default true); when false the user's `participants.columns` and `participants.widths` apply.
     */
    use_recommended?: boolean;
    /**
     * Bubble chart of the 'Market participants' service: true - bubbles use the colour of their catalog collection; false (default) - each collection gets its own colour from the project palette in order.
     */
    collection_colors?: boolean;
    /**
     * Bubble chart of the 'Market participants' service: true (default) - bubble size is the traded volume; false - all bubbles have one size.
     */
    size_by_volume?: boolean;
  };
}
/**
 * Stored here when `interface.settings_storage` is `server`; otherwise the same structure lives in localStorage. Sort and bubble axes are kept always; `columns` order applies only when `form.participants.use_recommended` is false.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigV1_Participants".
 */
export interface ConfigV1_Participants {
  /**
   * Visible table columns in display order (column ids of `afbws.screener.participants.v1`).
   */
  columns?: string[];
  /**
   * Table column widths in px by column id (deep-merged). Applies only when `form.participants.use_recommended` is false.
   */
  widths?: {
    [k: string]: number;
  };
  sort?: {
    column?: string;
    direction?: 'asc' | 'desc';
  };
  /**
   * Selected axes of the bubble chart.
   */
  bubble?: {
    x?: string;
    y?: string;
  };
}
/**
 * Merged under every user's own settings. A write (manager only) requires `dataset`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigDefaults".
 */
export interface ConfigDefaults {
  interface?: ConfigInterface;
  dataset?: ConfigDataset;
  dashboard?: ConfigDashboard;
}
/**
 * Available to every connection. Request carries `section` (basename of a markdown file, `[A-Za-z0-9]+`); the response echoes `section` and adds `content` (HTML rendered from the markdown). Unknown section: error `not_found`; bad name: `validation_error`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigHelp".
 */
export interface ConfigHelp {
  channel: 'config';
  schema: 'afbws.config.help.v1';
  request_id: AfbwsCommonV1_RequestId;
  section: string;
  content?: string;
}
/**
 * Request without `tiers`/`capabilities` = read; with both = write (saved into roles.yaml, runtime reloaded). The response always carries the full snapshot. Non-manager: error `forbidden`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigRoles".
 */
export interface ConfigRoles {
  channel: 'config';
  schema: 'afbws.config.roles.v1';
  request_id: AfbwsCommonV1_RequestId;
  tiers?: {
    [k: string]: ConfigRoleTier;
  };
  capabilities?: {
    [k: string]: unknown;
  };
  default_tier?: string;
  /**
   * Response only: `groups` list from groups.yaml.
   */
  groups_yaml?: {
    [k: string]: unknown;
  }[];
  /**
   * Response only: GetCourse groups.
   */
  getcourse_groups?: {
    [k: string]: unknown;
  }[];
  /**
   * Response only: why GetCourse groups could not be fetched.
   */
  getcourse_groups_error?: string | null;
  /**
   * Response only.
   */
  limits_template?: {
    keys: string[];
    defaults: {
      [k: string]: number;
    };
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigRoleTier".
 */
export interface ConfigRoleTier {
  title?: string;
  limits?: {
    [k: string]: number;
  };
  members?: string[];
  [k: string]: unknown;
}
/**
 * `item` is populated on a refused settings/defaults mutation: the authoritative current server state (a `settings` object for afbws.config.settings.v1, a `defaults` object for afbws.config.defaults.v1); the client applies it and shows `message`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConfigError".
 */
export interface ConfigError {
  channel: 'config';
  schema: 'afbws.config.error.v1';
  request_id?: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  item?: {
    [k: string]: unknown;
  };
}
/**
 * See ExecutionService.list_connectors_for_user (AFB/backend/trade/service.py).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConnectorListData".
 */
export interface ConnectorListData {
  connectors: ConnectorRecord[];
  meta: {
    brokers: string[];
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConnectorExecutionPolicy".
 */
export interface ConnectorExecutionPolicy {
  max_spread_steps?: number;
  execution_mode?: 'client' | 'hybrid';
  backstop?: ConnectorBackstop;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConnectorBackstop".
 */
export interface ConnectorBackstop {
  offset_steps?: number;
  max_loss_steps?: number;
}
/**
 * Request: optional filters `ids[]`, `instrument_keys[]` and/or `tradeplan_ids[]` (all given = intersection; none = every deal of the caller) and optional `detail` (true = rows carry the full editor payload `deal` + `editable_fields`, i.e. a dealDetail; default false = summary rows). Response (same `request_id`): `items[]` (dealItem). There is no separate `get`: use `ids` with `detail: true`. A request carrying `items` is invalid, as is a response carrying a filter.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2List".
 */
export interface DealV2List {
  channel: 'deal';
  schema: 'afbws.deal.list.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  ids?: [DealV2Id, ...DealV2Id[]];
  /**
   * @minItems 1
   */
  instrument_keys?: [AfbwsCommonV1_InstrumentKey, ...AfbwsCommonV1_InstrumentKey[]];
  /**
   * @minItems 1
   */
  tradeplan_ids?: [TradeplanId, ...TradeplanId[]];
  detail?: boolean;
  items?: DealV2Item[];
}
/**
 * Same allow-list as dealSummary (see there); with `detail: true` each row additionally carries `deal` (the public afb.deal.v2 projection) and `editable_fields` — together, i.e. a dealDetail. Rows of a list without `detail` never carry them.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Item".
 */
export interface DealV2Item {
  deal_id: DealV2Id;
  revision: number;
  status: DealStatus;
  execution_phase: DealExecutionPhase;
  bf_id: DealV2BfId;
  tradeplan_id: TradeplanId;
  ticker: string;
  /**
   * Full composite key identifying one catalog listing or derivative: `<MIC>[:<board|market>]:<ticker>` (e.g. `MISX:TQBR:SBER`, `MISX:RFUD:IMOEXF`), or the venueless 2-segment derivative form `<MIC>:<code>` (e.g. `MISX:IMOEXF`) where the wire explicitly identifies a derivative rather than a listing. Case-sensitive, never normalized (`.lower()`/`.upper()`) on either side of the AFB backend<->frontend channel.
   */
  instrument_key?: string;
  market?: 'stock' | 'futures' | 'currency';
  direction: 'long' | 'short';
  sizing?: DealSizing;
  execution_policy?: DealExecutionPolicy;
  broker_sizing?: DealV2SizingDisplay;
  realized_pnl?: DealV2RealizedPnl;
  position?: DealV2OpenPosition;
  created_at: string;
  updated_at: string;
  deal?: DealPublicV1;
  editable_fields?: DealV2AmendField[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealSizing".
 */
export interface DealSizing {
  mode: 'lots' | 'margin' | 'risk_currency' | 'risk_factor' | 'balance_pct';
  value: DecimalString;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealExecutionPolicy".
 */
export interface DealExecutionPolicy {
  on_afb_disconnect?: string;
  max_spread_steps?: number;
  margin_trading?: boolean;
  /**
   * How exit protection is executed. Absent means `client` (condition engine only, current behaviour). `hybrid` additionally places a server-side SLTP backstop order once a position opens. `server` is reserved — not yet implemented by any BF, always rejected at publish. See RESILIENCE.md, Фаза 3/5.
   */
  execution_mode?: 'client' | 'hybrid' | 'server';
  /**
   * Per-deal overrides for the hybrid-mode server-side backstop order; unset fields fall back to the executing BF's own config defaults. Meaningful only when execution_mode is `hybrid`.
   */
  backstop?: {
    offset_steps?: number;
    stop_price?: DecimalString;
    max_loss_steps?: number;
    /**
     * Reserved for a future server-side take-profit leg (OCO). Always rejected as true for now — the backstop is protection-only in this phase.
     */
    take_profit?: boolean;
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2SizingDisplay".
 */
export interface DealV2SizingDisplay {
  lots?: number;
  required_cash?: string;
  /**
   * BF-resolved actual order quantity (lots), fixed once at entry-trigger time — distinct from `lots`, which stays the pre-trade publish estimate. Present only once BF has reported it (`status_changed.quantity`).
   */
  resolved_lots?: number;
}
/**
 * Absent entirely means no ledger yet (deal predates it, or has not had an exit fill) — distinct from a present-but-degraded value.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2RealizedPnl".
 */
export interface DealV2RealizedPnl {
  /**
   * Decimal string, rubles. Null exactly when degraded is set — a fill's money multiplier (step_price/price_step or lot_size) could not be resolved.
   */
  value: string | null;
  degraded: null | 'missing_price' | 'missing_step_price';
}
/**
 * Absent entirely means flat (no open position) or not yet known — distinct from a present qty of 0, which is never emitted.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OpenPosition".
 */
export interface DealV2OpenPosition {
  /**
   * Signed net quantity (positive long, negative short).
   */
  qty: number;
  /**
   * Decimal string — weighted-average open entry price.
   */
  avg_price: string;
  /**
   * ISO-8601 timestamp this snapshot was computed at.
   */
  as_of: string;
}
/**
 * Explicit allow-list projector output over afb.deal.v2 (../deal.v2.json), built by backend/trade/public_views.py — never a serialization of the persisted DealState file. Deliberately NOT an allOf+$ref extension of the whole wire root: those wire schemas declare `owner`/`archive_reason` in their own `properties` with no `additionalProperties: false`, so those fields would count as already-'evaluated' and survive an outer `unevaluatedProperties: false` — the only way to actually drop them is to define this object's own shape directly and reuse the wire schemas' field-level $defs (target, sizing, conditions, execution policy) rather than their root. `source` is strict and requires `tradeplan_id` — the single public link back to the owning tradeplan; `source.kind`/`draft_id`, compile snapshots and raw phase-B overrides never appear here. The one internal field that IS projected — per-leg, not on `source` — is `leg_id` (v2 legs only), the plan-leg identity the frontend needs to tell which deal leg still tracks which plan leg.
 */
export interface DealPublicV1 {
  schema: 'afb.deal.v2';
  deal_id: string;
  revision: number;
  target: DealTarget;
  direction: 'long' | 'short';
  /**
   * @minItems 1
   */
  entry: [
    {
      leg_id?: LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    },
    ...{
      leg_id?: LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    }[]
  ];
  stop_loss?: DealPublicExitList;
  take_profit?: DealPublicExitList;
  sizing: DealSizing;
  execution_policy?: DealExecutionPolicy;
  source: DealPublicSource;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealTarget".
 */
export interface DealTarget {
  bf_id: string;
  broker: string;
  instrument: DealInstrument;
  /**
   * broker-native locator added by BF after publish
   */
  binding?: {};
  /**
   * Broker account this deal is published against. Optional on the wire — absent means BF's own trading account (brokers/port.py::account_id). AFB compiles it from the owning tradeplan's publish.account_id (see tradeplan.v2.json publish), resolving empty/absent to the connector's default account before publish (ExecutionService.resolve_plan_account). BF validates it against its own account (plan_engine/plan_validation.py: wrong_account_id) when present.
   */
  account_id?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealInstrument".
 */
export interface DealInstrument {
  exchange: string;
  board: string;
  ticker: string;
  /**
   * Full composite key identifying one catalog listing or derivative: `<MIC>[:<board|market>]:<ticker>` (e.g. `MISX:TQBR:SBER`, `MISX:RFUD:IMOEXF`), or the venueless 2-segment derivative form `<MIC>:<code>` (e.g. `MISX:IMOEXF`) where the wire explicitly identifies a derivative rather than a listing. Case-sensitive, never normalized (`.lower()`/`.upper()`) on either side of the AFB backend<->frontend channel.
   */
  instrument_key?: string;
  /**
   * Opaque broker locator of the instrument, e.g. `TICKER@MIC`. AFB takes it from its listing_link (finam.db); BF resolves the instrument ONLY by it (no BF-side catalog). Not part of the instrument identity: amend identity is decided by instrument_key (or exchange/board/ticker), see amend_rules. Absent => BF rejects with instrument_unresolvable unless the deal binding already carries a symbol.
   */
  broker_symbol?: string;
  market?: 'stock' | 'futures' | 'currency';
  price_step?: DecimalString;
  step_price?: DecimalString;
}
/**
 * AFB resolves alarm indicators by `id`, BF by `type`+`params`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_IndicatorExpr".
 */
export interface ConditionV1_IndicatorExpr {
  source: 'indicator';
  type: 'wma' | 'kama' | 'psar';
  params?: {};
  id?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_ImmediateExpr".
 */
export interface ConditionV1_ImmediateExpr {
  source: 'immediate';
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicSource".
 */
export interface DealPublicSource {
  tradeplan_id: string;
}
/**
 * Request: `items[]` (at least one) of `{tradeplan_id, bf_id}` (no inline plan draft, 1:1 per row). Response (same `request_id`): `results[]` (one per item; a failed row is accepted=false) and `accepted`. Distinguished by `items` vs `results`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Publish".
 */
export interface DealV2Publish {
  channel: 'deal';
  schema: 'afbws.deal.publish.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  items?: [DealV2PublishItem, ...DealV2PublishItem[]];
  results?: DealV2Result[];
  /**
   * any(result.accepted for result in results)
   */
  accepted?: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2PublishItem".
 */
export interface DealV2PublishItem {
  tradeplan_id: TradeplanId;
  bf_id: DealV2BfId;
}
/**
 * accepted=true: `bf_id` and `status` are set (status is `deleted` after a delete), `revision` is the deal's revision and `item` the authoritative record when the deal still exists. accepted=false: only `message` (why) — the command did not touch the deal, so there is no status/revision. When a rebind changes the deal id, `deal_id`/`item` carry the NEW id — the client must drop the old cache key.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Result".
 */
export interface DealV2Result {
  deal_id: DealV2Id;
  bf_id?: DealV2BfId;
  status?: DealV2ResultStatus;
  accepted: boolean;
  revision?: number;
  item?: DealV2Detail;
  message?: string;
}
/**
 * Allow-list built by backend/trade/public_views.py::deal_detail. `deal` is the public afb.deal.v2 projection (deal.public.v1.json). `editable_fields` lists what the current status/execution_phase allows to amend.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Detail".
 */
export interface DealV2Detail {
  deal_id: DealV2Id;
  revision: number;
  status: DealStatus;
  execution_phase: DealExecutionPhase;
  bf_id: DealV2BfId;
  tradeplan_id: TradeplanId;
  ticker: string;
  /**
   * Full composite key identifying one catalog listing or derivative: `<MIC>[:<board|market>]:<ticker>` (e.g. `MISX:TQBR:SBER`, `MISX:RFUD:IMOEXF`), or the venueless 2-segment derivative form `<MIC>:<code>` (e.g. `MISX:IMOEXF`) where the wire explicitly identifies a derivative rather than a listing. Case-sensitive, never normalized (`.lower()`/`.upper()`) on either side of the AFB backend<->frontend channel.
   */
  instrument_key?: string;
  market?: 'stock' | 'futures' | 'currency';
  direction: 'long' | 'short';
  sizing?: DealSizing;
  execution_policy?: DealExecutionPolicy;
  broker_sizing?: DealV2SizingDisplay;
  realized_pnl?: DealV2RealizedPnl;
  position?: DealV2OpenPosition;
  created_at: string;
  updated_at: string;
  deal: DealPublicV1;
  editable_fields: DealV2AmendField[];
}
/**
 * Request: `items[]` (at least one) of `{deal_id, bf_id}` (the backend resolves the source tradeplan via the deal's own link). Response (same `request_id`): `results[]` and `accepted`; if the new target changes a deal id, that row's `deal_id`/`item` carry the NEW id. Distinguished by `items` vs `results`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Rebind".
 */
export interface DealV2Rebind {
  channel: 'deal';
  schema: 'afbws.deal.rebind.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  items?: [DealV2RebindItem, ...DealV2RebindItem[]];
  results?: DealV2Result[];
  /**
   * any(result.accepted for result in results)
   */
  accepted?: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2RebindItem".
 */
export interface DealV2RebindItem {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
}
/**
 * Request: `items[]` (at least one). Response (same `request_id`): `results[]` (one per item, partial failures are rows with accepted=false) and `accepted`. Distinguished by `items` vs `results`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Operation".
 */
export interface DealV2Operation {
  channel: 'deal';
  schema: 'afbws.deal.operation.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  items?: [DealV2OperationItem, ...DealV2OperationItem[]];
  results?: DealV2Result[];
  /**
   * any(result.accepted for result in results)
   */
  accepted?: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OperationItem".
 */
export interface DealV2OperationItem {
  deal_id: DealV2Id;
  action: 'activate' | 'pause' | 'resume' | 'cancel' | 'reconcile' | 'delete';
  /**
   * Only meaningful for action='cancel'.
   */
  cancel_open_orders?: boolean;
}
/**
 * Request: `items[]` (at least one) of `{deal_id, deal_edit?, base_revision?}`. Response (same `request_id`): `results[]` (amendResult, one per item; a rejected or conflicting row never fails the batch) and `accepted` (any row accepted). Distinguished by `items` vs `results`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Amend".
 */
export interface DealV2Amend {
  channel: 'deal';
  schema: 'afbws.deal.amend.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  items?: [DealV2AmendItem, ...DealV2AmendItem[]];
  results?: DealV2AmendResult[];
  /**
   * any(result.accepted for result in results)
   */
  accepted?: boolean;
}
/**
 * Optional `deal_edit` (only the legs/fields overridden on the deal side; anything omitted keeps following the linked tradeplan) and optional `base_revision` (optimistic concurrency: a mismatch rejects this row with `conflict` and the current `item`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2AmendItem".
 */
export interface DealV2AmendItem {
  deal_id: DealV2Id;
  deal_edit?: DealV2Edit;
  base_revision?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Edit".
 */
export interface DealV2Edit {
  entry?: DealV2RoleEdit;
  stop_loss?: DealV2RoleEdit;
  take_profit?: DealV2RoleEdit;
  sizing?: DealSizing;
  execution_policy?: DealExecutionPolicy;
}
/**
 * Indices refer to the CURRENT deal's leg array for that role at base_revision — never a tradeplan's, never leg_id. edited/removed_indices/reset_indices apply to existing legs; new_legs are appended after them. See AFB backend tradeplans/overrides.py::apply_deal_edit for the exact merge order.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2RoleEdit".
 */
export interface DealV2RoleEdit {
  edited?: DealV2LegEdit[];
  removed_indices?: number[];
  /**
   * Drop this leg's deal-level override (source reverts to tradeplan) — the leg re-adopts whatever the linked plan currently holds for the matching leg_id.
   */
  reset_indices?: number[];
  new_legs?: DealV2NewLeg[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2LegEdit".
 */
export interface DealV2LegEdit {
  index: number;
  condition?: DealV2_ConditionNode;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2NewLeg".
 */
export interface DealV2NewLeg {
  condition: DealV2_ConditionNode;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
}
/**
 * accepted=true: `revision` (the new revision), `status` and `item` (the authoritative record) are set; no message/code. accepted=false: the deal is unchanged, `message` says why and `code` is the machine-readable reason when there is one; `item` (the authoritative current record) is present only with `conflict` — a stale `base_revision` — so the client can adopt it instead of retrying blind. The outcome of the BF confirmation arrives later as `outcome` and `event` pushes.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2AmendResult".
 */
export interface DealV2AmendResult {
  deal_id: DealV2Id;
  accepted: boolean;
  revision?: number;
  status?: DealStatus;
  item?: DealV2Detail;
  message?: string;
  code?: AfbwsCommonV1_ErrorCode;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2AckEvent".
 */
export interface DealV2AckEvent {
  schema: 'afb.deal.trigger_ack.v2';
  notification_id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2AckResultItem".
 */
export interface DealV2AckResultItem {
  schema: 'afbws.deal.ack_result.v2';
  notification_id: string;
  status: 'ok' | 'not_found';
}
/**
 * Only for a whole request (invalid_schema, invalid_channel, forbidden, internal_error, ...). Per-deal failures of a batched publish/rebind/operation/amend are rows with accepted=false in that response's `results[]` (a stale `base_revision` is `code: conflict` with the current `item` there); no code carries `item` or `details`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Error".
 */
export interface DealV2Error {
  channel: 'deal';
  schema: 'afbws.deal.error.v2';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
}
/**
 * REPLACE per deal: for every item the client overwrites its cached copy identified by `item.deal_id`, never merges. One mutation (one batch command) = ONE push carrying all deals it changed. It carries NO command outcome — that is `afbws.deal.outcome.v2`; and no thin events are merged into it — see `afbws.deal.event.v2`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Record".
 */
export interface DealV2Record {
  channel: 'deal';
  schema: 'afbws.deal.record.v2';
  /**
   * @minItems 1
   */
  items: [DealV2Detail, ...DealV2Detail[]];
}
/**
 * A separate push, so the client does not need the whole record just to show a toast; `items[]` (at least one), each is an independent outcome (see outcomeItem).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Outcome".
 */
export interface DealV2Outcome {
  channel: 'deal';
  schema: 'afbws.deal.outcome.v2';
  /**
   * @minItems 1
   */
  items: [DealV2OutcomeItem, ...DealV2OutcomeItem[]];
}
/**
 * A separate push, so the client does not need the whole record just to show a toast. AFB composes no user-facing texts: it passes through what BF returned, the text is built on the frontend. result=rejected: any BF rejection (`code` required). result=accepted: only the confirmation of `deal.amend` (the one accepted outcome the server reports), without code/message/broker_error.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OutcomeItem".
 */
export interface DealV2OutcomeItem {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  /**
   * Command type this outcome refers to (`deal.amend`, `deal.publish`, `deal.operation`, `deal.resync`, ...), null for an outcome not caused by a command (an execution rejection).
   */
  command: string | null;
  result: 'accepted' | 'rejected';
  /**
   * Rejection code from BF `deal.rejected.code`. Only with result=rejected.
   */
  code?: string;
  /**
   * Message exactly as received from BF. Only with result=rejected.
   */
  message?: string | null;
  broker_error?: PayloadsDealRejected_BrokerError;
}
/**
 * Structured broker error behind the rejection. BF sends it only for USER-kind errors (those that must reach the user). Dictionary of `kind` is part of the contract: the frontend picks the user text by it. DAEMON-kind errors (unavailable, timeout, rate_limited, session_closed, trading_halted, auction_only, auth_expired) are handled by the BF daemon itself, never become a rejection and are never sent here. `native_code`/`native_message` are exactly as the broker returned them, unprocessed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsDealRejected_BrokerError".
 */
export interface PayloadsDealRejected_BrokerError {
  /**
   * BF error dictionary (USER kinds): `insufficient_funds`, `invalid_order`, `instrument_not_found`, `instrument_not_tradable`, `permission_denied`, `auth_failed`, `rejected` (broker refused for an unknown reason), `unknown`. The set may grow: a consumer MUST tolerate an unknown value (show native_message, fall back to `code`/`message`).
   */
  kind: string;
  /**
   * Broker's own error code as a string (e.g. `145`), null if the broker gave none.
   */
  native_code?: string | null;
  /**
   * Broker's own error text, unprocessed; null if none.
   */
  native_message?: string | null;
  [k: string]: unknown;
}
/**
 * `events[]` (at least one) in order of occurrence, each a typed eventItem (a thin, allow-listed fact — never a state snapshot or a raw BF payload).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Event".
 */
export interface DealV2Event {
  channel: 'deal';
  schema: 'afbws.deal.event.v2';
  /**
   * @minItems 1
   */
  events: [DealV2EventItem, ...DealV2EventItem[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealCreated".
 */
export interface DealV2EventDealCreated {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'created';
  logged_at: string;
  data: DealV2CreatedData;
}
/**
 * Light, no snapshot: the full state arrives as `afbws.deal.record.v2`. Produced by AFB (no `at`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2CreatedData".
 */
export interface DealV2CreatedData {
  revision: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealAmended".
 */
export interface DealV2EventDealAmended {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'amended';
  logged_at: string;
  data: DealV2AmendedData;
}
/**
 * Light, no snapshot (state: `afbws.deal.record.v2`; BF confirmation: `accepted`/`rejected` events and `afbws.deal.outcome.v2`). Produced by AFB (no `at`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2AmendedData".
 */
export interface DealV2AmendedData {
  revision: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealAccepted".
 */
export interface DealV2EventDealAccepted {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'accepted';
  logged_at: string;
  data: DealV2AcceptedData;
}
/**
 * BF-only fields (`broker_instrument`, `validation`, `broker_sizing`, `binding`, `target_instrument_patch`) are not forwarded.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2AcceptedData".
 */
export interface DealV2AcceptedData {
  /**
   * Type of the accepted AFB command (`deal.publish`, `deal.operation`, `deal.amend`, `deal.resync`, ...).
   */
  command_type: string;
  revision?: number;
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealRejected".
 */
export interface DealV2EventDealRejected {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'rejected';
  logged_at: string;
  data: DealV2RejectedData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2RejectedData".
 */
export interface DealV2RejectedData {
  /**
   * Machine-readable rejection code (BF `deal.rejected.code`).
   */
  code: string;
  /**
   * Message exactly as received from BF.
   */
  message?: string;
  /**
   * Absent for rejections not caused by an AFB command (the broker rejected the entry order).
   */
  command_type?: string;
  broker_error?: PayloadsDealRejected_BrokerError;
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealStatusChanged".
 */
export interface DealV2EventDealStatusChanged {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'status_changed';
  logged_at: string;
  data: DealV2StatusChangedData;
}
/**
 * Deletion/archival is NOT a status: it is the `deleted` event.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2StatusChangedData".
 */
export interface DealV2StatusChangedData {
  status: DealStatus;
  execution_phase?: DealExecutionPhase;
  /**
   * Decimal string.
   */
  last_price?: string;
  /**
   * Why the deal was cancelled/paused (BF user-kind or `execution_error`, ...). Only with a cancelling status.
   */
  cancel_reason?: string;
  /**
   * Resolved order quantity (lots), fixed once by BF at entry-trigger time.
   */
  quantity?: number;
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealDeleted".
 */
export interface DealV2EventDealDeleted {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'deleted';
  logged_at: string;
  data: DealV2DeletedData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2DeletedData".
 */
export interface DealV2DeletedData {
  /**
   * Archive reason: `user_delete`, `instrument_delisted`, `no_binding`, ...
   */
  reason?: string;
  archived_at?: string;
  revision?: number;
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealReport".
 */
export interface DealV2EventDealReport {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'report';
  logged_at: string;
  data: DealV2ReportData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2ReportData".
 */
export interface DealV2ReportData {
  status: DealStatus;
  close_reason?: string;
  /**
   * The chart-marker source (one element per broker trade). The realized P&L is NOT here: it is `realized_pnl` of the deal record (AFB ledger).
   */
  fills?: DealV2ReportFill[];
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2ReportFill".
 */
export interface DealV2ReportFill {
  trade_id?: string;
  order_id: string;
  role: DealV2OrderRole;
  side: DealV2OrderSide;
  /**
   * Decimal string, null when unknown.
   */
  price?: string | null;
  quantity?: number;
  /**
   * ISO-8601 fill time, null for legacy BF versions.
   */
  timestamp?: string | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealOrdersSynced".
 */
export interface DealV2EventDealOrdersSynced {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'orders_synced';
  logged_at: string;
  data: DealV2OrdersSyncedData;
}
/**
 * Marker event: the changed orders arrive as separate order.* events and in the record.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OrdersSyncedData".
 */
export interface DealV2OrdersSyncedData {
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventDealPositionsSynced".
 */
export interface DealV2EventDealPositionsSynced {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'deal';
  event: 'positions_synced';
  logged_at: string;
  data: DealV2PositionsSyncedData;
}
/**
 * Marker event (declared by the BF protocol; current BF versions do not emit it).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2PositionsSyncedData".
 */
export interface DealV2PositionsSyncedData {
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventOrderCreated".
 */
export interface DealV2EventOrderCreated {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'order';
  event: 'created';
  logged_at: string;
  data: DealV2OrderCreatedData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OrderCreatedData".
 */
export interface DealV2OrderCreatedData {
  /**
   * BF's own client_order_id — the identity to match orders by.
   */
  order_id: string;
  side: DealV2OrderSide;
  role: DealV2OrderRole;
  quantity?: number;
  /**
   * Limit/stop price, or the average fill price once filled. Decimal string, null when unknown.
   */
  price?: string | null;
  status: DealV2OrderEventStatus;
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
  /**
   * The broker's own exchange order id, when known.
   */
  broker_order_id?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventOrderFilled".
 */
export interface DealV2EventOrderFilled {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'order';
  event: 'filled';
  logged_at: string;
  data: DealV2OrderData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2OrderData".
 */
export interface DealV2OrderData {
  /**
   * BF's own client_order_id — the identity to match orders by.
   */
  order_id: string;
  side: DealV2OrderSide;
  role: DealV2OrderRole;
  quantity?: number;
  /**
   * Limit/stop price, or the average fill price once filled. Decimal string, null when unknown.
   */
  price?: string | null;
  status: DealV2OrderEventStatus;
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
  filled_quantity?: number;
  leg_index?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventOrderPartiallyFilled".
 */
export interface DealV2EventOrderPartiallyFilled {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'order';
  event: 'partially_filled';
  logged_at: string;
  data: DealV2OrderData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventOrderCancelled".
 */
export interface DealV2EventOrderCancelled {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'order';
  event: 'cancelled';
  logged_at: string;
  data: DealV2OrderData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventOrderRejected".
 */
export interface DealV2EventOrderRejected {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'order';
  event: 'rejected';
  logged_at: string;
  data: DealV2OrderData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventPositionOpened".
 */
export interface DealV2EventPositionOpened {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'position';
  event: 'opened';
  logged_at: string;
  data: DealV2PositionData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2PositionData".
 */
export interface DealV2PositionData {
  /**
   * Instrument symbol of the position (the key of the client's per-deal position map): the broker symbol, else the bare ticker.
   */
  symbol: string;
  /**
   * Signed net quantity after the change; 0 on closed.
   */
  quantity: number;
  /**
   * Decimal string, null when unknown.
   */
  average_price?: string | null;
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventPositionChanged".
 */
export interface DealV2EventPositionChanged {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'position';
  event: 'changed';
  logged_at: string;
  data: DealV2PositionData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventPositionClosed".
 */
export interface DealV2EventPositionClosed {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'position';
  event: 'closed';
  logged_at: string;
  data: DealV2PositionData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2EventConditionTriggered".
 */
export interface DealV2EventConditionTriggered {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  category: 'condition';
  event: 'triggered';
  logged_at: string;
  data: DealV2ConditionTriggeredData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2ConditionTriggeredData".
 */
export interface DealV2ConditionTriggeredData {
  condition_id: string;
  /**
   * Decimal string, null when unknown.
   */
  price?: string | null;
  /**
   * Role of an order / of the leg whose condition fired. Superset of deal_state.v2 order.role: `external_close` is the synthetic order BF records when the position was closed outside the deal (it emits order.* for it too).
   */
  phase: 'entry' | 'stop_loss' | 'take_profit' | 'cancel_close' | 'backstop' | 'external_close';
  /**
   * ISO-8601 BF event-occurrence time (BF `at`). Absent on events produced by AFB itself.
   */
  at?: string;
}
/**
 * Not persisted. ONE push per tick for all open deals of the user: `items[]` (at least one).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Pnl".
 */
export interface DealV2Pnl {
  channel: 'deal';
  schema: 'afbws.deal.pnl.v2';
  /**
   * @minItems 1
   */
  items: [DealV2PnlItem, ...DealV2PnlItem[]];
}
/**
 * `trend` is deliberately absent — a frontend-only projection computed from consecutive pushes.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2PnlItem".
 */
export interface DealV2PnlItem {
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  /**
   * Decimal string
   */
  unrealized: string;
  currency: string;
  qty: number;
  /**
   * Decimal string
   */
  avg_price: string;
  /**
   * Decimal string
   */
  last_price: string;
  as_of: string;
}
/**
 * Server-initiated; same ack discipline as alarms: a reconnect redelivers events that were not acked (afbws.deal.ack.v2).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Triggered".
 */
export interface DealV2Triggered {
  channel: 'deal';
  schema: 'afbws.deal.triggered.v2';
  /**
   * @minItems 1
   */
  events: [DealV2TriggerEvent, ...DealV2TriggerEvent[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2TriggerStatusChanged".
 */
export interface DealV2TriggerStatusChanged {
  schema: 'afb.deal.trigger.v2';
  notification_id: string;
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  event: 'status_changed';
  created_at: string;
  data: DealV2StatusChangedData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2TriggerRejected".
 */
export interface DealV2TriggerRejected {
  schema: 'afb.deal.trigger.v2';
  notification_id: string;
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  event: 'rejected';
  created_at: string;
  data: DealV2RejectedData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2TriggerReport".
 */
export interface DealV2TriggerReport {
  schema: 'afb.deal.trigger.v2';
  notification_id: string;
  deal_id: DealV2Id;
  bf_id: DealV2BfId;
  event: 'report';
  created_at: string;
  data: DealV2TriggerReportData;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2TriggerReportData".
 */
export interface DealV2TriggerReportData {
  status: DealStatus;
  close_reason?: string;
}
/**
 * Explicit allow-list built by backend/trade/public_views.py::deal_summary, never a serialization of the persisted DealState (source_refs, status_history, event_journal, raw orders/positions, observed, owner_user_id never appear). `sizing` is the user-set {mode,value} from the «Риск и объём» block — NOT the broker_sizing projection, see `broker_sizing`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2Summary".
 */
export interface DealV2Summary {
  deal_id: DealV2Id;
  revision: number;
  status: DealStatus;
  execution_phase: DealExecutionPhase;
  bf_id: DealV2BfId;
  tradeplan_id: TradeplanId;
  ticker: string;
  /**
   * Full composite key identifying one catalog listing or derivative: `<MIC>[:<board|market>]:<ticker>` (e.g. `MISX:TQBR:SBER`, `MISX:RFUD:IMOEXF`), or the venueless 2-segment derivative form `<MIC>:<code>` (e.g. `MISX:IMOEXF`) where the wire explicitly identifies a derivative rather than a listing. Case-sensitive, never normalized (`.lower()`/`.upper()`) on either side of the AFB backend<->frontend channel.
   */
  instrument_key?: string;
  market?: 'stock' | 'futures' | 'currency';
  direction: 'long' | 'short';
  sizing?: DealSizing;
  execution_policy?: DealExecutionPolicy;
  broker_sizing?: DealV2SizingDisplay;
  realized_pnl?: DealV2RealizedPnl;
  position?: DealV2OpenPosition;
  created_at: string;
  updated_at: string;
}
/**
 * Explicit allow-list projector output over afb.deal.v2 (../deal.v2.json), built by backend/trade/public_views.py — never a serialization of the persisted DealState file. Deliberately NOT an allOf+$ref extension of the whole wire root: those wire schemas declare `owner`/`archive_reason` in their own `properties` with no `additionalProperties: false`, so those fields would count as already-'evaluated' and survive an outer `unevaluatedProperties: false` — the only way to actually drop them is to define this object's own shape directly and reuse the wire schemas' field-level $defs (target, sizing, conditions, execution policy) rather than their root. `source` is strict and requires `tradeplan_id` — the single public link back to the owning tradeplan; `source.kind`/`draft_id`, compile snapshots and raw phase-B overrides never appear here. The one internal field that IS projected — per-leg, not on `source` — is `leg_id` (v2 legs only), the plan-leg identity the frontend needs to tell which deal leg still tracks which plan leg.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicV1".
 */
export interface DealPublicDealV2 {
  schema: 'afb.deal.v2';
  deal_id: string;
  revision: number;
  target: DealTarget;
  direction: 'long' | 'short';
  /**
   * @minItems 1
   */
  entry: [
    {
      leg_id?: LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    },
    ...{
      leg_id?: LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    }[]
  ];
  stop_loss?: DealPublicExitList;
  take_profit?: DealPublicExitList;
  sizing: DealSizing;
  execution_policy?: DealExecutionPolicy;
  source: DealPublicSource;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicDealV2".
 */
export interface DealPublicDealV21 {
  schema: 'afb.deal.v2';
  deal_id: string;
  revision: number;
  target: DealTarget;
  direction: 'long' | 'short';
  /**
   * @minItems 1
   */
  entry: [
    {
      leg_id?: LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    },
    ...{
      leg_id?: LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    }[]
  ];
  stop_loss?: DealPublicExitList;
  take_profit?: DealPublicExitList;
  sizing: DealSizing;
  execution_policy?: DealExecutionPolicy;
  source: DealPublicSource;
}
/**
 * Request: optional filters `ids[]` and/or `instrument_keys[]` (both given = intersection; none = every primitive the caller owns). Response: same `request_id`, `items[]` (afb.gp.v2) — possibly empty, never an error for a missing id. There is no separate `get`: use `ids`. `items` is response-only; a request carrying `items` together with a filter is invalid.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2List".
 */
export interface GpV2List {
  channel: 'gp';
  schema: 'afbws.gp.list.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  ids?: [string, ...string[]];
  /**
   * @minItems 1
   */
  instrument_keys?: [AfbwsCommonV1_InstrumentKey, ...AfbwsCommonV1_InstrumentKey[]];
  items?: GpV2[];
}
/**
 * line, line_enter, line_sl, line_tp.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2PrimitiveSettingsLine".
 */
export interface GpV2PrimitiveSettingsLine {
  start: GpV2Point;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2Point".
 */
export interface GpV2Point {
  /**
   * Unix seconds, as in klines.
   */
  time: number;
  price: number;
}
/**
 * note.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2PrimitiveSettingsNote".
 */
export interface GpV2PrimitiveSettingsNote {
  start: GpV2Point;
  text?: string;
}
/**
 * zone, ruler, trendline, fibonacci.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2PrimitiveSettingsTwoPoint".
 */
export interface GpV2PrimitiveSettingsTwoPoint {
  start: GpV2Point;
  stop: GpV2Point;
}
/**
 * `item` carries the authoritative current record when the client should see it (a rejected move restores the server's version, not the client's optimistic one). `details` is populated on `conflict` (linked tradeplans/deals, locked scopes).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2Rejection".
 */
export interface GpV2Rejection {
  id: string;
  code: AfbwsCommonV1_ErrorCode;
  message?: string;
  item?: GpV2;
  details?: GpV2ErrorDetails;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2ErrorDetails".
 */
export interface GpV2ErrorDetails {
  tradeplan_ids?: string[];
  deal_ids?: string[];
  locked_scopes?: ('entry' | 'stop_loss' | 'take_profit')[];
}
/**
 * Request: only `request_id`. Response (same `request_id`): `items[]` — the caller's merged list (shared + personal).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2IndicatorList".
 */
export interface GpV2IndicatorList {
  channel: 'gp';
  schema: 'afbws.gp.indicator.list.v2';
  request_id: AfbwsCommonV1_RequestId;
  items?: GpV2Indicator[];
}
/**
 * `scope: shared` indicators are common to all users and editable only by a manager; `personal` belong to the caller. `settings` carry the parameters. Whether an indicator is shown on the chart is not part of the protocol (per-device view setting kept in the client's localStorage). Type `cot` is chart-only; alarm indicator conditions support wma/kama/psar.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2Indicator".
 */
export interface GpV2Indicator {
  id: string;
  type: 'wma' | 'kama' | 'psar' | 'cot';
  settings: GpV2IndicatorSettings;
  scope: 'shared' | 'personal';
}
/**
 * Display + calculation settings. Common: color/lineWidth/lineStyle; period (wma, cot); erPeriod/fastPeriod/slowPeriod (kama); start/maximum/increment (psar). Mirrors IndicatorInstance.settings of the frontend chart and `indicators[].settings` of config/_default_.yaml, without the on/off flag.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2IndicatorSettings".
 */
export interface GpV2IndicatorSettings {
  color: string;
  lineWidth: number;
  lineStyle: 'Solid' | 'Dots';
  period?: number;
  erPeriod?: number;
  fastPeriod?: number;
  slowPeriod?: number;
  start?: number;
  maximum?: number;
  increment?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2IndicatorRejection".
 */
export interface GpV2IndicatorRejection {
  id: string;
  code: AfbwsCommonV1_ErrorCode;
  message?: string;
}
/**
 * Keys are primitive kinds; a kind that is absent has no stored override (the client falls back to its defaults).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2PrimitiveStyles".
 */
export interface GpV2PrimitiveStyles {
  line?: GpV2PrimitiveKindStyle;
  line_enter?: GpV2PrimitiveKindStyle;
  line_sl?: GpV2PrimitiveKindStyle;
  line_tp?: GpV2PrimitiveKindStyle;
  note?: GpV2PrimitiveKindStyle;
  zone?: GpV2PrimitiveKindStyle;
  ruler?: GpV2PrimitiveKindStyle;
  trendline?: GpV2PrimitiveKindStyle;
  fibonacci?: GpV2PrimitiveKindStyle;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2PrimitiveKindStyle".
 */
export interface GpV2PrimitiveKindStyle {
  /**
   * hex colour; for `note` the callout line / frame / text colour.
   */
  color: string;
  lineWidth: 1 | 2 | 3 | 4;
  /**
   * lightweight-charts LineStyle: 0 Solid, 1 Dotted, 2 Dashed, 3 LargeDashed, 4 SparseDotted.
   */
  lineStyle: number;
}
/**
 * Used when the request as a whole fails (invalid_schema, forbidden channel, internal_error, ...). Per-item failures of a batched set/delete/indicator.* are reported in that response's `rejected[]`, not here. `details` is populated on `conflict`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV2Error".
 */
export interface GpV2Error {
  channel: 'gp';
  schema: 'afbws.gp.error.v2';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: GpV2ErrorDetails;
}
/**
 * A node of the category tree; its position in `collections[]` is the display order. `asset_ids` is the ordered composition (assets filed into it).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Collection".
 */
export interface AfbwsInstrumentChannelV2_Collection {
  id: string;
  name: string;
  parent_id?: string | null;
  /**
   * Opaque icon key. Omitted in a request: unchanged; null: clears.
   */
  icon_id?: string | null;
  /**
   * Omitted in a request: unchanged; null: clears.
   */
  icon_color?: AfbwsInstrumentChannelV2_FavoriteColor | null;
  asset_ids: string[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Asset".
 */
export interface AfbwsInstrumentChannelV2_Asset {
  id: string;
  name: string;
  collection_id: string | null;
  members: AfbwsInstrumentChannelV2_Member[];
}
/**
 * One ordered member of an asset: `listing` (ref = instrument_key) or `derivative` (ref = derivative code `MIC:CODE`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Member".
 */
export interface AfbwsInstrumentChannelV2_Member {
  kind: 'listing' | 'derivative';
  ref: string;
}
/**
 * An active catalog listing. `instrument_key` is the identity; `ticker` is a display attribute only (for non-MISX it is `MIC:TICKER`) and is never an address in this channel.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Listing".
 */
export interface AfbwsInstrumentChannelV2_Listing {
  instrument_key: AfbwsCommonV1_InstrumentKey;
  mic: string;
  board?: string | null;
  market: string;
  ticker: string;
  name: string;
  shortname?: string | null;
  currency?: string | null;
  decimals?: number | null;
  lot_size?: number | null;
  /**
   * Decimal string, never a float.
   */
  price_step?: string | null;
  /**
   * Decimal string, never a float.
   */
  step_price?: string | null;
  expiration?: string | null;
  isin?: string | null;
  derivative?: string | null;
  source: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Derivative".
 */
export interface AfbwsInstrumentChannelV2_Derivative {
  code: string;
  kind: 'perpetual' | 'series' | 'options';
  name: string;
  underlying_key?: AfbwsCommonV1_InstrumentKey | null;
  source: string;
}
/**
 * Request: only `request_id`. Response: `favorites` in display order (array position is the order).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Favorites".
 */
export interface AfbwsInstrumentChannelV2_Favorites {
  channel: 'instrument';
  schema: 'afbws.instrument.favorites.v2';
  request_id?: AfbwsCommonV1_RequestId;
  favorites?: AfbwsInstrumentChannelV2_FavoriteEntry[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_FavoriteEntry".
 */
export interface AfbwsInstrumentChannelV2_FavoriteEntry {
  kind: 'instrument' | 'asset';
  key: string;
  color: AfbwsInstrumentChannelV2_FavoriteColor;
}
/**
 * No CAS: `mark` (paint or repaint), `unmark` (idempotent removal) and `order` (REPLACES the whole display order) are idempotent. Request: any of `mark`/`unmark`/`order`. Response: `marked`/`unmarked`/`order` — only the sections that were present in the request; `unmarked` lists only refs that really were favorites. A response is recognised by `marked`/`unmarked`; an `order`-only request and its echo have the same shape.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Paint".
 */
export interface AfbwsInstrumentChannelV2_Paint {
  channel: 'instrument';
  schema: 'afbws.instrument.paint.v2';
  request_id?: AfbwsCommonV1_RequestId;
  mark?: AfbwsInstrumentChannelV2_FavoriteEntry[];
  unmark?: AfbwsInstrumentChannelV2_FavoriteRef[];
  order?: AfbwsInstrumentChannelV2_FavoriteRef[];
  marked?: AfbwsInstrumentChannelV2_FavoriteEntry[];
  unmarked?: AfbwsInstrumentChannelV2_FavoriteRef[];
}
/**
 * `key` is an `instrument_key` for kind `instrument` and an `asset_id` for kind `asset`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_FavoriteRef".
 */
export interface AfbwsInstrumentChannelV2_FavoriteRef {
  kind: 'instrument' | 'asset';
  key: string;
}
/**
 * One expiring contract the caller uses, ready for the replace card (computed by the server). `ticker` is display only.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_ExpirationNotice".
 */
export interface AfbwsInstrumentChannelV2_ExpirationNotice {
  instrument_key: AfbwsCommonV1_InstrumentKey;
  ticker: string;
  shortname?: string;
  expiration: string;
  days_left: number;
  usage: AfbwsInstrumentChannelV2_ExpirationUsage;
  candidates: AfbwsInstrumentChannelV2_ExpirationCandidate[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_ExpirationUsage".
 */
export interface AfbwsInstrumentChannelV2_ExpirationUsage {
  alarms: number;
  primitives: number;
  sets: number;
  favorites: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_ExpirationCandidate".
 */
export interface AfbwsInstrumentChannelV2_ExpirationCandidate {
  instrument_key: AfbwsCommonV1_InstrumentKey;
  ticker: string;
  expiration: string;
  shortname?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_ReplaceRejection".
 */
export interface AfbwsInstrumentChannelV2_ReplaceRejection {
  kind: AfbwsInstrumentChannelV2_ReplaceKind;
  id: string;
  code: 'not_found' | 'validation_error' | 'conflict' | 'forbidden' | 'internal_error';
  message?: string;
}
/**
 * A broker account (or the virtual one) of the caller. `account_id` is what the trading parameters depend on; `bf_id` accompanies it while an account id is unique only within a connector.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_AccountRef".
 */
export interface AfbwsInstrumentChannelV2_AccountRef {
  bf_id: string;
  account_id: string;
}
/**
 * `details`: `catalog_revision` / `user_revision` for `conflict`; `set_ids` / `asset_ids` / `instrument_keys` naming the rows at fault for `forbidden` / `validation_error`; `limit` for a tier-limit overflow.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsInstrumentChannelV2_Error".
 */
export interface AfbwsInstrumentChannelV2_Error {
  channel: 'instrument';
  schema: 'afbws.instrument.error.v2';
  request_id?: AfbwsCommonV1_RequestId;
  code:
    | 'forbidden'
    | 'invalid_schema'
    | 'invalid_channel'
    | 'unsupported_action'
    | 'validation_error'
    | 'not_found'
    | 'conflict'
    | 'bf_offline'
    | 'internal_error';
  message: string;
  details?: {
    catalog_revision?: number;
    user_revision?: number;
    set_ids?: string[];
    asset_ids?: string[];
    instrument_keys?: string[];
    limit?: {
      key: string;
      allowed: number;
      requested: number;
    };
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkSharedFields".
 */
export interface LinkSharedFields {
  /**
   * Optional free-text note shown as a tooltip in the AFB UI.
   */
  description?: string;
  dry_run: boolean | null;
  margin_trading: boolean | null;
  execution_policy: ConnectorExecutionPolicy;
  paired: boolean;
  pairing_pending: boolean;
  pairing_expires_at: string | null;
  /**
   * connector: real BF entry from trading_bf.yaml. virtual: synthetic pseudo-connector for the no-broker virtual account.
   */
  kind: 'connector' | 'virtual';
  /**
   * Whether this caller may set() this record.
   */
  editable: boolean;
}
/**
 * Owner-editable connector fields plus bf_id. Admin setInput composes this with broker/ACL/margin extras.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkSetInputShared".
 */
export interface LinkSetInputShared {
  bf_id?: string;
  name?: string;
  enabled?: boolean;
  description?: string;
  dry_run?: boolean | null;
  execution_policy?: ConnectorExecutionPolicy;
}
/**
 * `item` (the current authoritative record) is only allowed with code `conflict`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Rejection".
 */
export interface LinkV2Rejection {
  id: string;
  code: AfbwsCommonV1_ErrorCode;
  message?: string;
  details?: {};
  item?: LinkV2Entity;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2PairItem".
 */
export interface LinkV2PairItem {
  id: string;
  item: LinkV2Entity;
  pairing_string: string;
  expires_at: string;
}
/**
 * Runtime-only BF status — never carries name/broker/ACL/keys/policy/config, see link.user.v1.json/link.admin.v1.json for that. `updated_at` is the moment of the LAST STATE CHANGE (connected, heartbeat_stale, broker/daemon/session state), NOT of the last heartbeat: repeated session.heartbeat without any change neither move `updated_at` nor produce a push. There are no heartbeat timestamp/interval fields — the client only needs `heartbeat_stale`. `daemon` is null until the first daemon.status after connect; `session` is null whenever `connected` is false (disconnect resets both).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2StatusItem".
 */
export interface LinkV2StatusItem {
  schema: 'afbws.link.state.v2';
  bf_id: string;
  connected: boolean;
  /**
   * AFB-derived stale flag (no heartbeat within 3x the negotiated interval).
   */
  heartbeat_stale: boolean;
  /**
   * ISO timestamp of the last change of this status record (not of the last heartbeat).
   */
  updated_at: string;
  daemon: null | DaemonStatusPayload;
  session: null | LinkV2Session;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DaemonStatusPayload".
 */
export interface DaemonStatusPayload {
  active?: boolean;
  bf_id: string;
  broker_connected?: boolean;
  code: string;
  reason: string;
  state?: string;
  severity?: 'ok' | 'warning' | 'critical';
  health?: {
    overall?: 'ok' | 'warning' | 'critical';
    points?: {};
    [k: string]: unknown;
  };
  changes?: {
    point?: string;
    from?: string;
    to?: string;
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Session".
 */
export interface LinkV2Session {
  account_id: string;
  /**
   * Effective value for this session (AFB override if set, else BF's own).
   */
  dry_run: boolean | null;
  capabilities: {
    [k: string]: unknown;
  };
}
/**
 * Per-element failures of a batched operation are reported in that response's `rejected[]`, not here. `code` is the closed common errorCode set.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkV2Error".
 */
export interface LinkV2Error {
  channel: 'link';
  schema: 'afbws.link.error.v2';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
}
/**
 * The client states its whole desired subscription scope every time; the server does not diff against a previous `subscribe`. `quotes` is the favorites price-plaque scope: `instrument_keys` to track. `futures` opts into the futures screener scope: a full quote+oi+oi_daily snapshot of every futures instrument (no per-instrument list — it's all-or-nothing). Neither controls the series (candles/dataset) subscription — that one is driven entirely by `get` (target=series), see its description. An empty body — neither `quotes` nor `futures` present — unsubscribes from both. Reply is `subscription` with the same `request_id`, immediately followed by `snapshot` push(es) with `mode:"full"` for each accepted scope.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSubscribe".
 */
export interface MarketSubscribe {
  channel: 'market';
  schema: 'afbws.market.subscribe.v1';
  request_id: AfbwsCommonV1_RequestId;
  quotes?: MarketSubscriptionQuotesSpec;
  /**
   * True to subscribe to the futures screener scope (all futures instruments); omitted or false leaves/unsubscribes it.
   */
  futures?: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSubscriptionQuotesSpec".
 */
export interface MarketSubscriptionQuotesSpec {
  /**
   * @maxItems 2000
   */
  instrument_keys: AfbwsCommonV1_InstrumentKey[];
}
/**
 * `quotes` is the accepted subset of what was requested (same shape as subscribe.v1's `quotes`; absent means the quotes scope is empty/unsubscribed). `futures` always reflects the accepted state (true/false), even when the request omitted it. `rejected` lists `quotes.instrument_keys` that could not be resolved/subscribed, with a reason code. Always followed by `snapshot` push(es) with `mode:"full"` for each accepted scope.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSubscription".
 */
export interface MarketSubscription {
  channel: 'market';
  schema: 'afbws.market.subscription.v1';
  request_id: AfbwsCommonV1_RequestId;
  quotes?: MarketSubscriptionQuotesSpec;
  futures: boolean;
  rejected: MarketSubscriptionRejection[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSubscriptionRejection".
 */
export interface MarketSubscriptionRejection {
  instrument_key: AfbwsCommonV1_InstrumentKey;
  code: AfbwsCommonV1_ErrorCode;
  message?: string;
}
/**
 * Reply to `get` (target=series) when `request_id` is present — `mode:"replace"`, the full requested range. Unsolicited push to the connection's live series subscription (see `get`'s description for how a request becomes that subscription) when `request_id` is absent — `mode:"merge"`: `tables` carries rows only at the timestamp(s) of the latest candle(s) (the just-closed bar plus the new one, on a period rollover), for every `kind` of the live subscription, not the whole history.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSeries".
 */
export interface MarketSeries {
  channel: 'market';
  schema: 'afbws.market.series.v1';
  request_id?: AfbwsCommonV1_RequestId;
  instrument_key: AfbwsCommonV1_InstrumentKey;
  period: MarketPeriod;
  /**
   * IANA timezone of the trading venue (e.g. "Europe/Moscow") that bar boundaries and trading-day edges are aligned to. Not the client's local timezone.
   */
  tz: string;
  /**
   * When AFB received this data from its source (broker/cache), ISO-8601 with offset. Distinct from the row-level `time` (UTC unix seconds), which is when the bar/event itself occurred.
   */
  received_at: string;
  /**
   * "replace": this is the full answer to a `get` — the client replaces its local copy of this instrument+period+kind range with `tables`. "merge": this is a live push to the connection's series subscription — `tables` rows are only at the latest candle time(s) (closed bar + new bar on a period rollover); the client upserts them by `time` into its existing copy.
   */
  mode: 'replace' | 'merge';
  /**
   * Start of the range actually covered by `tables`, YYYY-MM-DD in `tz`.
   */
  from?: string;
  /**
   * End of the range actually covered by `tables`, YYYY-MM-DD in `tz`.
   */
  to?: string;
  /**
   * Where this data came from, when known.
   */
  source?: 'broker' | 'cache';
  /**
   * Optional human-readable note (e.g. partial coverage, provider fallback).
   */
  message?: string;
  /**
   * Optional, live series only: UTC unix seconds of the opening tick of each future (not-yet-formed) `period` bar after the last candle in `tables`, per MOEX's trading calendar — strictly increasing, no duplicates. AFB computes this server-side from its own trading-calendar state; there is no client-side calendar lookup. Present on the `mode:"replace"` reply to a live `get` (target=series, see `get`'s description) and re-sent on a `mode:"merge"` push only when the list actually changed (the remaining count ran low or the trading day rolled over) — a `merge` push without `future_times` means it is unchanged, the client keeps what it already has. Never present on a pure history fetch (`end_date` strictly before today). The frontend renders these as whitespace bar slots past the last real candle.
   */
  future_times?: number[];
  data_status?: AfbwsMarketChannelV1_DataStatus;
  tables: MarketSeriesTable[];
}
/**
 * Present on a `series` message only when it is NOT a normal fresh fetch: either the `moex` source's circuit breaker was open when this was built (data served from `market_cache` only — no network at all; a `candles` table may be missing entirely since candles have no persistent cache, see AFB `backend/market/tables.py::build_series_tables_cache_only`) or AFB's freshness detector found this instrument's calendar section/kind lagging behind a live market (`backend/sources/freshness.py`) while the underlying fetch itself still nominally succeeded. Absent on `data_status` means a normal, fresh answer.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsMarketChannelV1_DataStatus".
 */
export interface AfbwsMarketChannelV1_DataStatus {
  /**
   * "partial": at least one requested `kind` could not be served at all (e.g. `candles`, breaker open). "stale": every requested `kind` is present in `tables` but may lag behind the live market.
   */
  state: 'stale' | 'partial';
  /**
   * Which source this is attributed to, e.g. "moex".
   */
  source: string;
  /**
   * Human-readable cause (breaker cooldown, freshness lag, ...).
   */
  reason: string;
  /**
   * When this degraded condition started, ISO-8601 with offset.
   */
  since: string;
}
/**
 * Reply to `get` (target=snapshot) when `request_id` is present; unsolicited push to the `quotes` or `futures` subscription scope when it is absent (see `scope`).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketSnapshot".
 */
export interface MarketSnapshot {
  channel: 'market';
  schema: 'afbws.market.snapshot.v1';
  request_id?: AfbwsCommonV1_RequestId;
  /**
   * Which client-side cache this snapshot replaces/updates. "quotes": the favorites subscription (accepted `subscribe.quotes`) — `mode:"full"` right after `subscribe`, then `mode:"update"` with only the quote rows that changed. "futures": the futures screener scope (accepted `subscribe.futures`) — always `mode:"full"`, `tables` covering quote + oi + oi_daily for every futures instrument; sent right after `subscribe` and again on every futures-positions (futoi) refresh from the broker (~5 min). "get": the reply to a one-shot `get` (target=snapshot) — carries `request_id`.
   */
  scope: 'quotes' | 'futures' | 'get';
  /**
   * IANA timezone of the trading venue, used to align `oi_daily`'s midnight `time` to the trading day.
   */
  tz: string;
  /**
   * When AFB received this data from its source, ISO-8601 with offset.
   */
  received_at: string;
  /**
   * "full": the complete answer to a `get`, or a full refresh of a subscription scope — the client replaces its local snapshot for that `scope`. "update": a live push carrying only the rows that changed since the last full/update — see `scope` for which scopes ever send `update`.
   */
  mode: 'full' | 'update';
  tables: MarketSnapshotTable[];
}
/**
 * Unsolicited push, no `request_id`: sent to every connection that negotiated this channel on each health-state transition of an external source (plan стабильности AFB, Этап 3 — `backend/sources/health.py`'s circuit breaker/degraded-window states) and once as a full snapshot right after this channel's first `subscribe`/`get`. Replaces the removed legacy `stream/loop_status`. `sources` lists every source AFB currently tracks (`moex`/`getcourse`); a source absent from the list has never reported a call yet — treat as "ok".
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsMarketChannelV1_SourceStatus".
 */
export interface AfbwsMarketChannelV1_SourceStatus {
  channel: 'market';
  schema: 'afbws.market.source_status.v1';
  sources: AfbwsMarketChannelV1_SourceStatusEntry[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsMarketChannelV1_SourceStatusEntry".
 */
export interface AfbwsMarketChannelV1_SourceStatusEntry {
  /**
   * e.g. "moex", "getcourse" (backend/sources/health.py source names).
   */
  source: string;
  state: 'ok' | 'degraded' | 'down';
  /**
   * When this source entered its CURRENT state, ISO-8601 with offset.
   */
  since: string;
  /**
   * Human-readable cause (window error rate/p90 for degraded, breaker cooldown for down).
   */
  reason?: string;
}
/**
 * Two client-avalanche-protection codes (plan стабильности AFB, Этап 2), both replying to the superseded/rejected `get`'s own `request_id`, not a push: `superseded` — a live `get target=series` (see `$defs/get`) was cancelled because a newer live `get` on the same connection replaced it before it finished; the client should discard the pending request silently, its chart already moved on. `busy` — the connection's concurrent heavy-`get` limit (history+live `target=series`) was exceeded, or the server is under memory pressure; carries `retry_after_sec`, the client may retry once after that delay.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "MarketErrorResponse".
 */
export interface MarketErrorResponse {
  channel: 'market';
  schema: 'afbws.market.error.v1';
  request_id?: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
  /**
   * code=busy only: seconds the client should wait before retrying the same request once.
   */
  retry_after_sec?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsScreenerChannelV1_ListItem".
 */
export interface AfbwsScreenerChannelV1_ListItem {
  id: AfbwsScreenerChannelV1_ExportId;
  kind: AfbwsScreenerChannelV1_ExportKind;
  trading_day: string;
  /**
   * Moment of the export's signals (MSK, no zone), derived from the file name; `night`: 19:00 of trading_day.
   */
  asof: string;
  /**
   * File modification time (ISO 8601 with zone); the content is not read for the list.
   */
  generated_at: string;
  /**
   * File size in bytes.
   */
  size: number;
}
/**
 * Root catalog collection (color source for the bubbles).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerV1ParticipantsCollection".
 */
export interface ScreenerV1ParticipantsCollection {
  id: string;
  name: string;
  color: AfbwsScreenerChannelV1_FavoriteColor | null;
}
/**
 * Derivative reference table (columnar, like afbws.market.series.v1 tables): `columns` start with `derivative` (e.g. `MISX:Si`) and may list any subset of the other fields; read by column name. `name`; `active_instrument_key` = nearest unexpired contract (to open a chart); `collection_id` references `collections[].id` (null = no collection). Shared by all four lists.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerV1ParticipantsDerivatives".
 */
export interface ScreenerV1ParticipantsDerivatives {
  /**
   * @minItems 1
   */
  columns: [
    'derivative' | 'name' | 'active_instrument_key' | 'collection_id',
    ...('derivative' | 'name' | 'active_instrument_key' | 'collection_id')[]
  ];
  /**
   * Each row has the same length and order as `columns`; a missing value is null (never NaN).
   */
  rows: (number | string | null)[][];
}
/**
 * One snapshot. `rows` are columnar (`columns` begin with `derivative`; the other columns are a subset of the fiz_/yur_ position fields, openinterest and volume). Only derivatives that have data in this snapshot get a row; the rest are absent (join with `derivatives` by key). `source`: `intraday` if at least one row is the intraday slot of the day, otherwise `daily`. `price` = price of the derivative's active contract (`derivatives.active_instrument_key`): the last quote for `now` when `trading_day` is today, otherwise the close of the last 5-minute slot of `trading_day`; null when there is no price. The same contract is used in all four lists, so price changes between lists are comparable.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerV1ParticipantsList".
 */
export interface ScreenerV1ParticipantsList {
  /**
   * now = latest trading day that has started (the current session once it has data, otherwise the previous trading day's close); d1 = close of the trading day before `now`; d2 = the one before d1; w1 = last trading day <= (`now` day - 7 calendar days).
   */
  key: 'now' | 'd1' | 'd2' | 'w1';
  trading_day: string;
  /**
   * Moment of the values (MSK, no zone); for `now` the intraday slot.
   */
  asof: string;
  /**
   * `daily`: daily-only derivatives and fallback.
   */
  source: 'intraday' | 'daily';
  /**
   * @minItems 1
   */
  columns: [
    (
      | 'derivative'
      | 'fiz_long'
      | 'fiz_short'
      | 'fiz_net'
      | 'fiz_persons_long'
      | 'fiz_persons_short'
      | 'yur_long'
      | 'yur_short'
      | 'yur_net'
      | 'yur_persons_long'
      | 'yur_persons_short'
      | 'openinterest'
      | 'volume'
      | 'price'
    ),
    ...(
      | 'derivative'
      | 'fiz_long'
      | 'fiz_short'
      | 'fiz_net'
      | 'fiz_persons_long'
      | 'fiz_persons_short'
      | 'yur_long'
      | 'yur_short'
      | 'yur_net'
      | 'yur_persons_long'
      | 'yur_persons_short'
      | 'openinterest'
      | 'volume'
      | 'price'
    )[]
  ];
  /**
   * Each row has the same length and order as `columns`; a missing value is null (never NaN).
   */
  rows: (number | string | null)[][];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ScreenerV1Error".
 */
export interface ScreenerV1Error {
  channel: 'screener';
  schema: 'afbws.screener.error.v1';
  request_id?: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
}
/**
 * Request: optional filters `ids[]` and/or `instrument_keys[]` (both = intersection; none = every non-archived plan of the caller; archived plans are returned only when named in `ids`). Response (same `request_id`): `items[]`. There is no separate `get`: use `ids`. A request carrying `items` is invalid, as is a response carrying a filter.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2List".
 */
export interface TradeplanV2List {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.list.v2';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  ids?: [TradeplanId, ...TradeplanId[]];
  /**
   * @minItems 1
   */
  instrument_keys?: [AfbwsCommonV1_InstrumentKey, ...AfbwsCommonV1_InstrumentKey[]];
  items?: TradeplanV2PlanItem[];
}
/**
 * An allow-list projection of the stored plan. `status` is the plan lifecycle (draft -> published -> completed, + archived manually). `activated_at`/`closed_at`/`created_at`/`updated_at` are market-time ISO strings, `activated_at`/`closed_at` may be empty. Instrument: `instrument_key` is present whenever the server could resolve one; a plan whose instrument is not in the catalog comes with `instrument_missing: true` (and possibly without `ticker`) — at least one of the two is always there. `ticker` is the derived wire ticker. Never returned: `delivery_at`, `archived_components`, `archived_at`, `editor`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2PlanItem".
 */
export interface TradeplanV2PlanItem {
  schema: 'afb.tradeplan.v2';
  id: TradeplanId;
  ticker?: string;
  instrument_key?: AfbwsCommonV1_InstrumentKey;
  /**
   * Overlaid on output only (not persisted): the plan's instrument is not found in the catalog. A reference note, not a lifecycle state. Absent otherwise.
   */
  instrument_missing?: true;
  direction: 'long' | 'short';
  status: 'draft' | 'published' | 'completed' | 'archived';
  /**
   * @minItems 1
   */
  entries: [TradeplanV2LegItem, ...TradeplanV2LegItem[]];
  stop_loss: TradeplanV2LegItem[];
  take_profit: TradeplanV2LegItem[];
  sizing: DealSizing;
  publish?: TradeplanV2_Publish;
  activated_at: string;
  closed_at: string;
  created_at: string;
  updated_at: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2LegItem".
 */
export interface TradeplanV2LegItem {
  leg_id: LegId;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
  condition: TradeplanV2Condition;
}
/**
 * Same vocabulary as ../tradeplan.v2.json#/$defs/tpConditionNode (price/indicator/dataset/immediate left side, const/indicator/dataset/primitive_id right side, timeframe, duration — the same shared defs) with `op` required: the storage schema tolerates a price leg without `op` (old stored files; means `touch`), the channel does not — the frontend always sends `op`, the server fills `touch` on output for such stored legs.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2Condition".
 */
export interface TradeplanV2Condition {
  id?: string;
  op: TradeplanV2_ConditionOp;
  timeframe?: ConditionV1_Timeframe;
  duration?: ConditionV1_Duration;
  left: TradeplanV2_ConditionLeft;
  right: TradeplanV2_ConditionRight;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_PrimitiveRef".
 */
export interface TradeplanV2_PrimitiveRef {
  primitive_id: string;
}
/**
 * Параметры публикации плана (используется ТОЛЬКО при публикации, не хранит связь с сделкой). bf_id — коннектор по умолчанию для UI; истина при публикации — bf_id из afbws.deal.publish.request.v1. account_id пусто/отсутствует — дефолтный (торговый) счёт коннектора, резолвится на лету (ExecutionService.resolve_plan_account).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_Publish".
 */
export interface TradeplanV2_Publish {
  bf_id?: string;
  account_id?: string;
}
/**
 * Request: `items[]` (at least one) of `planInput` — create or update by `item.id`, batched. Response (same `request_id`): `items[]` the applied authoritative `planItem`s (possibly empty), `rejected[]` for plans that were not applied (a stale/conflicting plan carries its current `planItem` in `rejected[].item`), and `amend_results[]` — the per-deal outcome of re-amending the live deals of every applied plan (empty for creates only; each row names its `tradeplan_id`). Distinguished by `amend_results`: present => response, absent => request. A failing plan never fails the batch. There is no push on set.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2Set".
 */
export interface TradeplanV2Set {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.set.v2';
  request_id: AfbwsCommonV1_RequestId;
  items: (TradeplanV2PlanInput | TradeplanV2PlanItem)[];
  rejected?: TradeplanV2Rejection[];
  amend_results?: TradeplanV2AmendResultItem[];
}
/**
 * Deliberately has NO server-owned fields: `status` (lifecycle is driven by the plan's deals), `activated_at`, `closed_at`, `archived_at`, `created_at`, `updated_at`, `delivery_at`, `archived_components`, `instrument_missing`; the server keeps them from its own storage (a create starts as `draft`). `ticker` is not accepted either: it is derived by the server from `instrument_key`, the authoritative instrument reference (case-sensitive, never normalized). `editor` (frontend editor-mode hint) is not part of the channel: the current frontend neither sends nor reads it.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2PlanInput".
 */
export interface TradeplanV2PlanInput {
  schema: 'afb.tradeplan.v2';
  id: TradeplanId;
  instrument_key: AfbwsCommonV1_InstrumentKey;
  direction: 'long' | 'short';
  /**
   * @minItems 1
   */
  entries: [TradeplanV2LegInput, ...TradeplanV2LegInput[]];
  stop_loss: TradeplanV2LegInput[];
  take_profit: TradeplanV2LegInput[];
  sizing: DealSizing;
  publish?: TradeplanV2_Publish;
}
/**
 * `leg_id` is optional on input: a new leg has none, the server assigns one on save (existing ids are never reassigned). `percent`/`logic` — see ../deal.v2.json#/$defs/legJoin.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2LegInput".
 */
export interface TradeplanV2LegInput {
  leg_id?: LegId;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
  condition: TradeplanV2Condition;
}
/**
 * `id` is the plan id from the request, `code` a whole-request error code reused per plan (`not_found`, `validation_error`, `conflict`, ...), `message` the human-readable reason. `item` is the authoritative current plan and is present only with `conflict` (a stale or blocked plan: archive/delete blocked by a live deal that already entered a position, `set` over a primitive owned by another plan), so the client can adopt it without a separate read; a `conflict` may also come without it.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2Rejection".
 */
export interface TradeplanV2Rejection {
  id: TradeplanId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  item?: TradeplanV2PlanItem;
}
/**
 * One row per deal of an applied plan; `tradeplan_id` names that plan, so a batch `set` response can be matched without guessing. accepted=true: the deal was amended, `revision` is its new revision (integer; null only if the deal did not report one) and `status` its status after the amend. accepted=false: the deal is unchanged, `message` says why (a human-readable gate/validation text) and `code` is set only for the one machine-readable case the server distinguishes: `tradeplan_missing` (the deal's own tradeplan no longer exists — an orphaned deal). `revision`/`status` never appear on a rejection.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2AmendResultItem".
 */
export interface TradeplanV2AmendResultItem {
  schema: 'afbws.tradeplan.amend_result.v2';
  tradeplan_id: TradeplanId;
  deal_id: string;
  accepted: boolean;
  revision?: number | null;
  status?: DealStatus;
  message?: string;
  code?: 'tradeplan_missing';
}
/**
 * Request: `ids[]` (at least one). Response (same `request_id`): `ids[]` actually deleted (possibly empty) + `rejected[]`. Allowed only for a plan that never had a deal; otherwise that plan is rejected with `conflict` (use archive). The deletion is NOT pushed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2Delete".
 */
export interface TradeplanV2Delete {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.delete.v2';
  request_id: AfbwsCommonV1_RequestId;
  ids: TradeplanId[];
  rejected?: TradeplanV2Rejection[];
}
/**
 * `items[]` (at least one) is a DELTA, not a snapshot: the client upserts plans in its own list by matching id and leaves everything else untouched. The authoritative full list comes only from afbws.tradeplan.list.v2. Sent on plan lifecycle changes (status derived from its deals) and archival (one push per batch). Plan deletion and `set` are NOT conveyed by this push. Never a request: `request_id` is not allowed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2Sync".
 */
export interface TradeplanV2Sync {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.sync.v2';
  /**
   * @minItems 1
   */
  items: [TradeplanV2PlanItem, ...TradeplanV2PlanItem[]];
}
/**
 * Per-plan failures of a batched set/delete/archive are reported in that response's `rejected[]`, not here.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2Error".
 */
export interface TradeplanV2Error {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.error.v2';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
}
/**
 * AFB-side user alarm — like afb.tradeplan.v2, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel; it is documented here (rather than only in AFB) because it shares condition.v1.json's operator vocabulary with deal.v2 and tradeplan.v2. Replaces the legacy YAML shape (condition_type/trigger_type/value_type/value/value_ref flat fields, break_up/break_down operator names) with a conditionNode. Legacy alarms are read via a lazy converter (see docs/PROTOCOL.md 'Алармы' mapping table) and rewritten in this format on next save/reactivation; the API layer only accepts/emits this format going forward. `period` is the alarm's overall computation timeframe (legacy default '10min'); when `condition` is a price candle operator, `condition.timeframe` carries the candle timeframe and by construction equals `period`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV1".
 */
export interface AlarmV1 {
  schema: 'afb.alarm.v1';
  id: string;
  ticker: string;
  condition: AlarmV1_AlarmConditionNode;
  period?: ConditionV1_Timeframe;
  trigger_frequency?: 'once' | 'every_candle' | 'daily';
  status?: 'active' | 'triggered' | 'expired';
  created_at?: string;
  updated_at?: string;
  triggered_at?: string;
  delivery_at?: string;
  trigger_count?: number;
}
/**
 * Unlike condition.v1.json#/$defs/indicatorExpr, only `source`+`id` are required: AFB resolves `type`/`field`/`params` from the user's saved indicator settings by `id` rather than carrying them inline.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmV1_AlarmIndicatorExpr".
 */
export interface AlarmV1_AlarmIndicatorExpr {
  source: 'indicator';
  id: string;
  type?: 'wma' | 'kama' | 'psar';
  field?: string;
  params?: {};
}
/**
 * Building blocks reused across deal.v2.json/tradeplan.v2.json/condition.v1.json/instrument.v1.json and payloads/dataset.*.json. Extracted from the former deal.v1.json (2026-08-11); deal.v1/tradeplan.v1 have since been removed.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "CommonV1_Root".
 */
export interface CommonV1_Root {
  [k: string]: unknown;
}
/**
 * Provenance of this deal's compiled definition. The AFB compiler writes only `tradeplan_id` — the single source of truth for deal->tradeplan linkage (see the tradeplan/deal separation plan). `kind`/`draft_id` are a deprecated pre-separation pair: new AFB never writes them, they may still appear on persisted records created before the deal-channel-migration offline backfill ran. Left open (no additionalProperties restriction, matching the rest of this wire schema) since AFB may carry extra compile metadata here (e.g. `compiled_at`, `primitive_snapshot`, and — Фаза B2 — `leg_ids` [{entry,stop_loss,take_profit}: [leg_id|null, ...], parallel to the matching deal.v2.json leg array] and `removed_plan_leg_ids` [string[], tombstoned plan leg_ids]) that BF does not interpret; AFB's own public projection reduces this object to `tradeplan_id` alone (afbws/deal.public.v1.json#/$defs/source) — the only piece that survives elsewhere is `leg_ids`, re-projected per leg as `leg_id` on the public v2 legs (afbws/deal.public.v1.json#/$defs/legId), never as part of `source`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealSource".
 */
export interface DealSource {
  /**
   * Id of the AFB tradeplan (state/tradeplans/<user_id>/<id>.yaml) that compiled this deal.
   */
  tradeplan_id?: string;
  /**
   * @deprecated
   * Deprecated legacy discriminator (always 'tradeplan_draft'). New AFB never writes this.
   */
  kind?: string;
  /**
   * @deprecated
   * Deprecated alias of tradeplan_id predating the tradeplan/deal separation. New AFB never writes this.
   */
  draft_id?: string;
}
/**
 * Multi-entry / multi-exit deal. entry, stop_loss, take_profit are root-level lists; each element may carry an optional `percent` (decimal string) and an optional `logic` (`#/$defs/legJoin`) joining it to the PRECEDING element in the same list — see `legJoin` for the full grammar (groups/buckets, `and`/`or` precedence, `percent` placement). Sum of percents per bucket resolves to 100. The deal-level `direction` (long/short) is the single source of truth for position bias — entry legs no longer carry a per-leg `side`, which would let 'buy' and 'sell' legs coexist in the same deal with no defined semantics (a deal is one position, not a basket of unrelated orders). The broker-facing buy/sell of each leg is derived from `direction` and its role: long entry / short exit -> buy; short entry / long exit -> sell. Reuses order/sizing/target defs from common.v1.json; conditionNode is condition.v1.json's shared vocabulary (see that schema for the full price/indicator/dataset operator semantics) plus the wire-only `node_type` marker. Unlike afb.deal.v1 (fixed above/below/crosses_* /crossing vocabulary), afb.deal.v2 price conditions use condition.v1.json's full operator vocabulary — touch, above/below (inclusive level, no timeframe) and breakout/breakdown/crossing (closed-candle, requires timeframe) — or compare indicator/dataset expressions against a constant or (for indicator/dataset) against another expression of the same kind.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2".
 */
export interface DealV2 {
  schema: 'afb.deal.v2';
  deal_id: string;
  revision: number;
  owner?: {};
  target: DealTarget;
  direction: 'long' | 'short';
  /**
   * @minItems 1
   */
  entry: [
    {
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    },
    ...{
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    }[]
  ];
  stop_loss?: DealV2_ExitList;
  take_profit?: DealV2_ExitList;
  sizing: DealSizing;
  execution_policy?: DealExecutionPolicy;
  archive_reason?: string;
  source?: DealSource;
}
/**
 * Shared per-deal YAML/JSON state, identical on AFB and BF. orders[]/positions[] are the authoritative observed facts; observed{} and execution_phase are derived.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealStateV2".
 */
export interface DealStateV2 {
  deal_id: string;
  revision: number;
  owner_user_id?: string;
  status: 'draft' | 'publishing' | 'published' | 'active' | 'paused' | 'closed' | 'cancelled' | 'orphaned';
  execution_phase?: 'idle' | 'awaiting_entry' | 'entry_working' | 'holding' | 'exit_working';
  deal: {};
  orders?: DealStateV2_Order[];
  positions?: DealStateV2_Position[];
  observed?: {};
  source_refs?: {};
  status_history?: {}[];
  event_journal?: unknown[];
  created_at?: string;
  updated_at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealStateV2_Order".
 */
export interface DealStateV2_Order {
  order_id?: string;
  side?: 'buy' | 'sell';
  role?: 'entry' | 'stop_loss' | 'take_profit' | 'cancel_close' | 'backstop';
  status?: 'new' | 'partially_filled' | 'filled' | 'cancelled' | 'rejected' | 'watching' | 'expired';
  quantity?: number;
  filled_quantity?: number;
  leg_index?: number;
  limit_price?: string | null;
  average_price?: string | null;
  /**
   * Server-side SLTP backstop trigger price (Фаза 3, этап E) — set only for role=backstop orders.
   */
  stop_price?: string | null;
  /**
   * Exchange-assigned order id from the broker's own snapshot, distinct from order_id (BF's client_order_id) — see RESILIENCE.md, этап C.
   */
  broker_order_id?: string;
  updated_at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealStateV2_Position".
 */
export interface DealStateV2_Position {
  instrument?: {};
  symbol?: string;
  quantity?: number;
  average_price?: string | null;
  broker_ref?: {};
}
/**
 * Signed transport envelope for afb.execution.v1. Every wire message is one of these. payload_hash and signature are computed over canonical JSON (sort_keys, separators=(',',':'), UTF-8); signing string is '{protocol}|{type}|{message_id}|{created_at}|{payload_hash}'.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "Envelope".
 */
export interface Envelope {
  protocol: 'afb.execution.v1';
  /**
   * UUID, unique per sender
   */
  message_id: string;
  /**
   * Links a reply to the command message_id
   */
  correlation_id?: string | null;
  /**
   * Prior event that caused this message
   */
  causation_id?: string | null;
  /**
   * 'afb' or a bf_id
   */
  sender: string;
  /**
   * target bf_id or 'afb'
   */
  recipient: string;
  /**
   * category.event (see taxonomy)
   */
  type: string;
  created_at: string;
  expires_at: string;
  /**
   * Stable dedup key; required for commands
   */
  idempotency_key?: string;
  /**
   * SHA-256 hex of canonical payload
   */
  payload_hash: string;
  payload: {};
  signature: Envelope_Signature;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "Envelope_Signature".
 */
export interface Envelope_Signature {
  alg: 'Ed25519';
  key_id: string;
  /**
   * base64url (no padding) signature
   */
  value: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV1_Point".
 */
export interface GpV1_Point {
  /**
   * Unix seconds, as in klines.
   */
  time: number;
  price: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssIssColumnsV1_Root".
 */
export interface IssIssColumnsV1_Root {
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssMarketsCurrency_Root".
 */
export interface IssMarketsCurrency_Root {
  securities: {
    columns: string[];
    data: unknown[];
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssMarketsFutures_Root".
 */
export interface IssMarketsFutures_Root {
  securities: {
    columns: string[];
    data: unknown[];
  };
}
/**
 * The actual series channel — asset_code groups contracts (e.g. RTS-9.26/RTS-12.26 -> RTS), name and underlying_asset are what plan_refresh writes onto futures_series.name/underlying_key instead of leaving them null. underlying_asset is legitimately blank for part of the universe (e.g. commodity futures with no single spot underlying); series_refresh.py must not treat that as a parse failure.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssMarketsFuturesSeries_Root".
 */
export interface IssMarketsFuturesSeries_Root {
  series: {
    columns: string[];
    data: unknown[];
  };
}
/**
 * The only market with more than one enabled board today: IMOEX/IMOEX2/RGBI trade on SNDX, RTSI on RTSI. A listing born from this market therefore carries no single board, and its catalog key omits the venue block entirely (MISX:<ticker>, not MISX:<board>:<ticker>) — see catalog_model.Listing.key and the v9->v10 migration notes in catalog_schema.py.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssMarketsIndex_Root".
 */
export interface IssMarketsIndex_Root {
  securities: {
    columns: string[];
    data: unknown[];
  };
}
/**
 * Architecture only — disabled by default (config/market_source.yaml options.enabled=false). ISS returns ~37k rows / ~13MB for this market (one row per strike per expiration), which the daily refresh, the in-memory pool and the frontend cannot absorb without pagination and a strike filter; that is separate follow-up work. Written now so instrument_type='option' and the options_series channel have a real shape to target instead of a guess.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssMarketsOptions_Root".
 */
export interface IssMarketsOptions_Root {
  securities: {
    columns: string[];
    data: unknown[];
  };
}
/**
 * Architecture only — disabled until options.json itself is enabled (see its own description). Mirrors futures_series.json's shape; ISS additionally carries strike-range and settlement fields here that the current parser has no target for.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssMarketsOptionsSeries_Root".
 */
export interface IssMarketsOptionsSeries_Root {
  series: {
    columns: string[];
    data: unknown[];
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "IssMarketsStock_Root".
 */
export interface IssMarketsStock_Root {
  securities: {
    columns: string[];
    data: unknown[];
  };
}
/**
 * AFB-side MQTT notification payload published to <topic_base>/alarms/<user_id> when a user alarm triggers. Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time. `display` carries human-readable strings pre-rendered by AFB backend (mirrors frontend alarm cards).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "NotificationAlarmV1".
 */
export interface NotificationAlarmV1 {
  schema: 'afb.notification.alarm.v1';
  alarm_id: string;
  ticker: string;
  /**
   * Full composite key identifying one catalog listing or derivative: `<MIC>[:<board|market>]:<ticker>` (e.g. `MISX:TQBR:SBER`, `MISX:RFUD:IMOEXF`), or the venueless 2-segment derivative form `<MIC>:<code>` (e.g. `MISX:IMOEXF`) where the wire explicitly identifies a derivative rather than a listing. Case-sensitive, never normalized (`.lower()`/`.upper()`) on either side of the AFB backend<->frontend channel.
   */
  instrument_key?: string;
  instrument?: {
    shortname?: string;
    secname?: string;
  };
  condition: AlarmV1_AlarmConditionNode;
  period?: ConditionV1_Timeframe;
  trigger_frequency?: 'once' | 'every_candle' | 'daily';
  /**
   * Value that met the condition (price, indicator, or dataset field).
   */
  triggered_value?: number | string;
  /**
   * Instrument last price at trigger time (price_data.last).
   */
  instrument_price?: number;
  display: {
    instrument_label: string;
    condition_op: string;
    condition_description: string;
    condition_text: string;
  };
  context?: {};
  user: {
    name: string;
    telegram: string;
    email: string;
    notify_telegram: boolean;
    notify_email: boolean;
  };
  /**
   * ISO-8601 publish time; added by MQTTPublisher, not by build_alarm_notification.
   */
  timestamp?: string;
}
/**
 * AFB-side MQTT notification payload published to <topic_base>/deals/<user_id> for a deal lifecycle event the user opted into (Настройки → Торговля). Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time; `at` (when present) is the BF event-occurrence time carried through from the underlying order.* /position.* /deal.* payload. `display` carries human-readable strings pre-rendered by AFB backend, mirroring the alarm notification design.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "NotificationDealV1".
 */
export interface NotificationDealV1 {
  schema: 'afb.notification.deal.v1';
  /**
   * Raw BF/AFB wire event type this notification was built from (traceability/debugging).
   */
  event:
    | 'condition.triggered'
    | 'order.created'
    | 'order.filled'
    | 'order.partially_filled'
    | 'position.opened'
    | 'position.changed'
    | 'position.closed'
    | 'deal.report';
  /**
   * Notification category matching the user-facing toggles in Настройки → Торговля.
   */
  category: 'trigger' | 'order_placed' | 'order_executed' | 'position' | 'close';
  deal_id: string;
  bf_id?: string;
  ticker?: string;
  instrument?: {
    shortname?: string;
    secname?: string;
  };
  direction?: 'long' | 'short';
  side?: 'buy' | 'sell';
  /**
   * Order/fill price (decimal string on the wire).
   */
  price?: number | string;
  quantity?: number;
  filled_quantity?: number;
  /**
   * Financial result on deal/position close (decimal string on the wire).
   */
  realized_pnl?: number | string;
  currency?: string;
  close_reason?: string;
  /**
   * ISO-8601 BF event-occurrence time, carried through from the source order.* /position.* /deal.* payload's `at` field, when present.
   */
  at?: string;
  display: {
    instrument_label: string;
    title: string;
    text?: string;
  };
  user: {
    name: string;
    telegram: string;
    email: string;
    notify_telegram: boolean;
    notify_email: boolean;
  };
  /**
   * ISO-8601 publish time; added by MQTTPublisher, not by build_deal_notification.
   */
  timestamp?: string;
}
/**
 * AFB-side MQTT notification payload published to <topic_base>/system/<user_id> when a futures contract the user works with (alarms, free primitives, personal-set memberships, favorites) is about to expire. Consumed by the AFB informer daemon (Telegram/email) exactly like alarm/deal/link/system notifications — informer never reads AFB settings, the recipient and channels come only from `user`. Sent at most once per (user, contract, `stage`). Not sent when the user's `interface.futures_days_to_expiration` is 0. NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "NotificationExpirationV1_Root".
 */
export interface NotificationExpirationV1_Root {
  schema: 'afb.notification.expiration.v1';
  /**
   * Stable per-(user, contract, stage) id for informer-side deduplication (like notification.link.v1).
   */
  notification_id: string;
  /**
   * Full catalog key of the expiring contract, e.g. `MISX:RFUD:SRU6`. Case-sensitive.
   */
  instrument_key: string;
  ticker: string;
  shortname?: string;
  /**
   * `YYYY-MM-DD`.
   */
  expiration: string;
  /**
   * Calendar days from the market date of the notice to `expiration` (0 on the expiration day).
   */
  days_left: number;
  /**
   * `warn` — the user's threshold (`futures_days_to_expiration`) was reached; `d1` — one day left (only when the threshold is above 1); `d0` — the expiration day, the last chance.
   */
  stage: 'warn' | 'd1' | 'd0';
  usage: {
    alarms: number;
    primitives: number;
    sets: number;
    favorites: number;
  };
  /**
   * The default replacement proposal — the nearest ACTIVE contract of the same derivative expiring after this one. Absent when there is none.
   */
  next_contract?: {
    instrument_key: string;
    ticker: string;
    expiration: string;
  };
  user: {
    name: string;
    telegram: string;
    email: string;
    notify_telegram: boolean;
    notify_email: boolean;
  };
  /**
   * ISO-8601 publish time; added by MQTTPublisher, not by the notification builder.
   */
  timestamp?: string;
}
/**
 * AFB-side MQTT notification payload published to <topic_base>/links/<user_id> for a BF connectivity/runtime incident or recovery the user opted into. Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time; `at` is the AFB-observed transition time. `display` carries human-readable strings pre-rendered by AFB backend.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "NotificationLinkV1".
 */
export interface NotificationLinkV1 {
  schema: 'afb.notification.link.v1';
  /**
   * Stable per-incident event id for informer-side deduplication.
   */
  notification_id: string;
  /**
   * Normalized AFB-side incident/recovery event.
   */
  event:
    | 'link.disconnected'
    | 'link.recovered'
    | 'broker.degraded'
    | 'broker.recovered'
    | 'daemon.suspended'
    | 'daemon.recovered';
  bf_id: string;
  connected: boolean;
  /**
   * Current BF runtime state as normalized by AFB (for example: active, off_hours, degraded, recovering, suspended).
   */
  daemon_state: string;
  previous_state?: string;
  broker_connected: boolean;
  severity: 'ok' | 'warning' | 'critical';
  previous_severity?: 'ok' | 'warning' | 'critical';
  reason?: string;
  code?: string;
  /**
   * ISO-8601 time when AFB observed the transition and emitted this notification payload.
   */
  at?: string;
  /**
   * ISO-8601 time when the tracked incident originally started, useful on recovery notifications.
   */
  incident_started_at?: string;
  /**
   * Optional subset or full copy of the current daemon health payload for richer informer formatting.
   */
  health?: {
    [k: string]: unknown;
  };
  display: {
    connector_label: string;
    title: string;
    text?: string;
  };
  user: {
    name: string;
    telegram: string;
    email: string;
    notify_telegram: boolean;
    notify_email: boolean;
  };
  /**
   * ISO-8601 publish time; added by MQTTPublisher, not by the link notification builder.
   */
  timestamp?: string;
}
/**
 * AFB-side MQTT notification payload published to <topic_base>/system/<user_id> for a backend stability event (source health, data freshness, resource watchdog, startup) that a manager opted into via `me.notify_system`. Consumed by the AFB informer daemon (Telegram/email) exactly like alarm/deal/link notifications — informer never reads AFB settings, the recipient and channels come only from `user`. NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time; `since` is the AFB-observed time the reported state began.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "NotificationSystemV1_Root".
 */
export interface NotificationSystemV1_Root {
  schema: 'afb.notification.system.v1';
  /**
   * Stable per-event id for informer-side deduplication (like notification.link.v1).
   */
  notification_id: string;
  /**
   * Category of backend stability event this notification reports.
   */
  kind: 'source_state' | 'stale_data' | 'resource' | 'startup';
  /**
   * What the event is about, meaning depends on `kind`: source_state -> source id (moex_iss, moex_apim, getcourse); stale_data -> "<section>:<candles|positions>"; resource -> watchdog event (loop_blocked, rss_step, memory_pressure); startup -> "backend".
   */
  source: string;
  /**
   * Current state, meaning depends on `kind`: source_state -> ok|degraded|down; stale_data -> fresh|stale; resource -> event-specific (blocked, step_300mb, on, off); startup -> unclean.
   */
  state: string;
  /**
   * State before this transition, when known (omitted on the very first observation for a key).
   */
  prev_state?: string;
  /**
   * ISO-8601 time AFB observed this state begin (market_iso_from_naive/market_now_naive, same convention as source_health/freshness `since`).
   */
  since: string;
  severity: 'info' | 'warning' | 'critical';
  /**
   * Human-readable extra detail (window stats, lag minutes, RSS, etc.), pre-rendered by AFB backend.
   */
  detail?: string;
  user: {
    name: string;
    telegram: string;
    email: string;
    notify_telegram: boolean;
    notify_email: boolean;
  };
  /**
   * ISO-8601 publish time; added by MQTTPublisher, not by the system notification builder.
   */
  timestamp?: string;
}
/**
 * Response to broker.get_accounts and unsolicited push after every reconcile pass (see belphegor/reporting/account_directory.py::AccountDirectory, engine.py::_publish_broker_snapshots) — full list of accounts visible to BF's broker token. `accounts[].account_id` is the ONLY account identifier — no broker_account_id split, by design. Positions carry only `broker_ref {broker, symbol}`: BF has no instrument catalog, AFB maps the symbol to its own instrument (instrument_key) itself. Only `default_account_id` (BF's own trading account, self._account_id) is tradable in this phase — see brokers/port.py::account_id docstring; the rest are read-only until a later multi-account execution phase.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerAccountsPayload".
 */
export interface BrokerAccountsPayload {
  /**
   * BF's single trading account (brokers/port.py::account_id) — the only account this BF instance executes orders on.
   */
  default_account_id: string;
  /**
   * ISO timestamp this snapshot was assembled at.
   */
  as_of: string;
  accounts: PayloadsBrokerAccounts_Account[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerAccounts_Account".
 */
export interface PayloadsBrokerAccounts_Account {
  account_id: string;
  /**
   * True only for the account matching default_account_id — see brokers/port.py::account_id docstring. Read-only mode does not change execution; it only reflects the broker token's own readonly flag (TokenDetails.readonly).
   */
  tradable: boolean;
  /**
   * TokenDetails.readonly for the broker token this account belongs to.
   */
  readonly: boolean;
  /**
   * 'ok': freshly polled. 'stale': last known snapshot, a more recent poll failed. 'error': never successfully polled — cash/positions/equity are placeholders.
   */
  status: 'ok' | 'stale' | 'error';
  equity: string | null;
  cash: PayloadsBrokerAccounts_CashBalance[];
  positions: PayloadsBrokerAccounts_Position[];
  /**
   * Broker commission booked on this account per trading day, a ROLLING WINDOW of the most recent days (a complete snapshot, not a delta — a lost push is healed by the next one; AFB upserts by (account_id, date) and keeps the older history itself). Absent: BF does not collect it (or the broker has no such data yet). The tariff-dependent broker commission cannot be attributed to a single deal (per contract, % of daily turnover, side-dependent), so it is account-level only; the per-trade exchange fee travels in deal.report `fills[].exchange_fee`.
   */
  broker_fees?: PayloadsBrokerAccounts_BrokerFee[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerAccounts_Position".
 */
export interface PayloadsBrokerAccounts_Position {
  quantity: number;
  average_price: string;
  current_price?: string | null;
  unrealized_pnl?: string | null;
  broker_ref: {
    /**
     * BF connector/broker id (e.g. finam).
     */
    broker: string;
    /**
     * Broker-side instrument locator (e.g. TICKER@MIC); the same value deals carry as target.instrument.broker_symbol.
     */
    symbol: string;
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerAccounts_BrokerFee".
 */
export interface PayloadsBrokerAccounts_BrokerFee {
  /**
   * Trading day, YYYY-MM-DD in BF's market.timezone (derived from the broker transaction timestamp).
   */
  date: string;
  /**
   * Decimal string; positive = charged to the client (the broker's COMMISSION transactions are negative changes — BF flips the sign).
   */
  value: string;
  currency: string;
  /**
   * Broker transaction id when the day is a single transaction; omitted when several were summed.
   */
  transaction_id?: string;
}
/**
 * NACK for any broker.* command (get_accounts/get_orders/resolve_instrument). Correlated to the request via correlation_id.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerErrorPayload".
 */
export interface BrokerErrorPayload {
  /**
   * ISO-8601 BF event-occurrence time.
   */
  at?: string;
  /**
   * Machine-readable error code (e.g. broker_disconnected). For broker.resolve_instrument also the instrument-resolution codes: instrument_unresolvable, instrument_mismatch, instrument_delisted, unsupported (same meaning as in deal.rejected.code).
   */
  code: string;
  /**
   * The broker.* command that failed (e.g. broker.get_accounts).
   */
  command_type: string;
  /**
   * Human-readable error detail.
   */
  message?: string;
  [k: string]: unknown;
}
/**
 * Request the full list of accounts visible to BF's broker token (not just its own trading account) — see belphegor/reporting/account_directory.py::AccountDirectory. AFB always sends an empty payload today; account_ids is reserved for a future partial-refresh use and is not currently read by BF.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerGetAccountsPayload".
 */
export interface BrokerGetAccountsPayload {
  /**
   * Reserved: filter to specific account ids. Absent/empty means all accounts.
   */
  account_ids?: string[];
  [k: string]: unknown;
}
/**
 * AFB always sends an empty payload; no filters exist today.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerGetOrdersPayload".
 */
export interface BrokerGetOrdersPayload {
  [k: string]: unknown;
}
/**
 * Response to broker.resolve_instrument (deal-instrument pre-flight resolution). Deliberately permissive (additionalProperties: true throughout) — both objects are BF-owned shapes; this is a PATCH-level description of existing wire behavior, not a new constraint on it.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerInstrumentResolvedPayload".
 */
export interface BrokerInstrumentResolvedPayload {
  /**
   * Broker-native locator applied to the deal at publish time (belphegor/plan_engine/deal_binding.py apply_publish_binding) — e.g. account_id, symbol.
   */
  binding: {
    [k: string]: unknown;
  };
  /**
   * BF trading params of the resolved instrument (initial margin, tradable/longable/shortable, lot size, price_step, price_type, ...) — see InstrumentInfo.to_broker_instrument_dict(). With `account_id` in the request the values are the account's own.
   */
  broker_instrument: {
    /**
     * Which order/trigger prices the instrument allows (Finam AssetParams.price_type): POSITIVE = strictly > 0; NON_NEGATIVE = >= 0; ANY = negative prices allowed (e.g. some futures); UNKNOWN = the broker did not say. Optional — absent means UNKNOWN.
     */
    price_type?: 'UNKNOWN' | 'POSITIVE' | 'NON_NEGATIVE' | 'ANY';
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * Response to broker.get_orders and unsolicited push after every reconcile pass. Matches belphegor/reporting/broker_snapshots.py::stored_orders_payload()/stored_order_to_dict() exactly — orders BF itself placed and is tracking, always for BF's own trading account (see broker.accounts.json — order history for non-default accounts is not available in this phase). `symbol` and `client_order_id` are NOT part of this wire shape; AFB synthesizes/displays without them.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerOrdersPayload".
 */
export interface BrokerOrdersPayload {
  account_id: string;
  orders: PayloadsBrokerOrders_Order[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerOrders_Order".
 */
export interface PayloadsBrokerOrders_Order {
  deal_id: string;
  order_id: string;
  side: string;
  role: string;
  status: string;
  quantity: number;
  filled_quantity: number;
  leg_index: number;
  limit_price?: string | null;
  average_price?: string | null;
  updated_at?: string;
  error_code?: string | null;
  error_message?: string | null;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerPositionLedgerPayload".
 */
export interface BrokerPositionLedgerPayload {
  account_id: string;
  entries: {
    entry_id: string;
    account_id?: string;
    symbol: string;
    /**
     * Signed net qty this entry represents: positive = long, negative = short.
     */
    qty: number;
    avg_price?: string | null;
    origin: 'bootstrap' | 'orphan_residual' | 'deal_archived' | 'external_close' | 'entry_only_release';
    source_deal_id?: string | null;
    note?: string;
    created_at?: string;
    updated_at?: string;
    [k: string]: unknown;
  }[];
  /**
   * Sum of entries[].qty per symbol, keyed by symbol — a convenience projection of entries.
   */
  residual_by_symbol: {
    [k: string]: number;
  };
  [k: string]: unknown;
}
/**
 * Deal-instrument pre-flight (AFB's afbws.instrument.channel.v2 `detail`, and the tradeplan publish path) — `deal` is a compiled ExecutionDeal (afb.deal.v2), the same shape deal.publish carries, sent here purely for its target/instrument fields; BF does not persist it from this command.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerResolveInstrumentPayload".
 */
export interface BrokerResolveInstrumentPayload {
  deal: DealV2;
  /**
   * Optional broker account whose trading parameters (initial margin, tradable/longable/shortable, price_type) are wanted — they depend on the account's tariff. Sent by AFB's afbws.instrument.channel.v2 `detail`. BF answers with the values of THAT account (broker_instrument in broker.instrument_resolved); absent means BF's own trading account (default_account_id). The instrument is located solely by deal.target.instrument.broker_symbol (or binding.symbol).
   */
  account_id?: string;
  [k: string]: unknown;
}
/**
 * AFB-pushed MOEX trading calendar snapshot, so BF can gate execution and background polling on real trading-session boundaries (holidays, weekend sessions, per-board session phases) instead of a fixed off-hours window. SNAPSHOT SEMANTICS: `sections` is the FULL current calendar this AFB wants this BF to hold, never a diff — on receipt BF REPLACES its entire calendar cache for the connection with this array (replace-all, not merge); a section/day/window absent from a later calendar.update is gone, not merely unchanged. Sent only to a BF that has declared `features.market_calendar` in `daemon.capabilities` (see payloads/daemon.capabilities.json) — a BF that has not declared it never receives this message and continues to gate on its own local config.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "CalendarUpdatePayload".
 */
export interface CalendarUpdatePayload {
  /**
   * ISO-8601 time (with offset) this snapshot was assembled by AFB. Not the exchange-side publication time of any one underlying MOEX calendar/session response — those differ per section/endpoint; this is the single freshness anchor for the whole snapshot.
   */
  as_of: string;
  /**
   * TTL in seconds. The snapshot is usable while now <= as_of + stale_after_sec. Once stale, BF MUST fail-safe: stop trusting this snapshot and fall back to its own local config (off-hours window / trading-day rule) for gating and polling decisions, rather than freezing the last-known calendar as if it were still current. AFB re-pushes calendar.update well inside this TTL under normal operation; a stale snapshot on BF signals a lost/degraded AFB<->BF link, not an intentionally frozen calendar.
   */
  stale_after_sec: number;
  /**
   * Last calendar date (YYYY-MM-DD, inclusive) covered by `sections[].days`/`windows` in this snapshot — currently "today + 7 days" on the AFB side, but BF must not hardcode that and should instead read this field. Any date at or before `horizon_until` that is missing from a section's `days` should be treated as unknown/non-trading by BF, not extrapolated; AFB is expected to always cover the horizon it declares.
   */
  horizon_until: string;
  /**
   * Full replacement set of per-exchange-section calendar data for this BF; an empty array is valid and means 'nothing to gate on' (BF falls back to its own config, same as on staleness).
   */
  sections: {
    /**
     * Exchange MIC this section belongs to, e.g. "MISX" (Moscow Exchange — equities/currency board group; futures/derivatives currently share the same MIC on MOEX). Opaque to BF beyond matching it against the deal's own instrument.
     */
    exchange: string;
    /**
     * MOEX trading section this calendar/session data was fetched for — matches the deal-resolution grouping BF/AFB already use elsewhere for market/engine classification (stock includes indices).
     */
    section: 'stock' | 'futures' | 'currency';
    /**
     * Per-calendar-day trading status for this section, one entry per date, typically covering [today - lookback, horizon_until]. Source: MOEX ISS `calendars/{section}.json` off_days block.
     */
    days: {
      /**
       * Calendar date (YYYY-MM-DD) this entry describes.
       */
      date: string;
      /**
       * Whether this section trades at all on this date. False for `kind: H` (holiday); true for `kind: N` (normal day) and `kind: W` (weekend session).
       */
      is_traded: boolean;
      /**
       * N = normal trading day. W = weekend/holiday session (exchange trades on a nominally non-working day; MOEX settles it into a following trading day via `trade_session_date`). H = holiday, not traded.
       */
      kind: 'N' | 'W' | 'H';
      /**
       * The trading-session date this calendar date's activity settles/reports into. For `kind: N` this equals `date` itself. For `kind: W` this is the next trading day (usually the following Monday) whose session this weekend day's trades belong to — this is how BF should bucket a W day's daily bar/session accounting. For `kind: H` (not traded) this is null.
       */
      trade_session_date: string | null;
      [k: string]: unknown;
    }[];
    /**
     * Trading-session and auction time windows for this section (BOTH categories — see `phase`'s own description), resolved to concrete UTC-offset instants. Resolution order when BF looks up a window for a specific instrument is secid -> board -> section: a window carrying `secid` applies only to that instrument; a window carrying `board` (no `secid`) applies to every instrument on that board; a window carrying neither applies to the whole section. AFB may send multiple overlapping windows at different specificity for the same day/phase (e.g. a section-wide default plus a board-specific override) — BF picks the most specific one that matches the instrument it is gating, per that resolution order. Source: MOEX ISS `calendars/{section}/session.json` (today only) for the near term, projected forward via `estimated` for days beyond what the exchange has actually published.
     */
    windows: {
      /**
       * Board this window applies to (e.g. "TQBR"); omitted means the window applies to the whole `section` regardless of board. Ignored when `secid` is present (secid is the more specific match).
       */
      board?: string;
      /**
       * Single instrument (MOEX SECID) this window applies to; omitted means the window applies at the `board` (or, absent that too, `section`) level instead. Never normalized to a different case on either side of the wire — MOEX tickers/secids are case-sensitive.
       */
      secid?: string;
      /**
       * Window start, ISO-8601 with UTC offset (the exchange's local offset, e.g. +03:00 for Moscow).
       */
      start: string;
      /**
       * Window end, ISO-8601 with UTC offset. Inclusive of the last tradable second (e.g. a window ending at 18:59:59 means trading stops at that second, not 19:00:00 sharp).
       */
      end: string;
      /**
       * Session phase label. Two categories: CONTINUOUS TRADING ("morning", "main", "evening", "weekend", "closing_price" — trades actually happen) and AUCTION ("opening_auction", "closing_auction" — an order-collection period: orders can already be booked, but no trades occur until the auction resolves). `closing_price` is synthetic (AFB-side only, not a raw MOEX session type): the few minutes of continuous trading MOEX's session.json leaves unlabeled right after `closing_auction` and before the evening session. A free-form string (not a closed enum) so AFB can introduce a new phase label without a protocol change; an UNRECOGNIZED phase must be treated as ordinary continuous trading (fail-open), not as an auction or as closed — only the two auction labels above should ever gate differently from plain trading. BF's entry gate (order placement) treats both categories as "open" (an auction already accepts orders); a liveness/no-false-reset check (e.g. a stream watchdog, which must not be fooled by an auction moving the book without trades) should treat only the continuous-trading category as "open".
       */
      phase: string;
      /**
       * True when this window was projected from a learned/default template rather than read from MOEX's official same-day session schedule (MOEX's session.json only ever returns today's schedule — everything beyond today is necessarily a projection). BF may use `estimated: true` windows for gating the same way as observed ones, but should not treat them as authoritative for anything requiring exchange confirmation.
       */
      estimated: boolean;
      [k: string]: unknown;
    }[];
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionTriggeredPayload".
 */
export interface ConditionTriggeredPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  condition_id: string;
  deal_id: string;
  phase?: string;
  price?: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DaemonCapabilitiesPayload".
 */
export interface DaemonCapabilitiesPayload {
  bf_id: string;
  broker?: string;
  protocol: string;
  software_version?: string;
  markets?: string[];
  order_types?: string[];
  /**
   * Order lifetimes this BF instance can place, ordered by operator preference (first = default pick). `day` = до конца дня, `gtc` = до отмены, `ioc` = исполнить сразу (also used declaratively by brokers whose API has no time_in_force field at all, e.g. market-only REST APIs).
   */
  time_in_force?: ('day' | 'gtc' | 'ioc')[];
  sizing_modes?: string[];
  condition_ops?: string[];
  condition_nodes?: string[];
  /**
   * BF's single trading account (brokers/port.py::account_id) — the account this BF instance executes orders on. The full account list/snapshots are fetched separately via broker.get_accounts (always supported), not from this field.
   */
  account_id?: string;
  account_aliases?: string[];
  /**
   * What market data this BF instance can serve, and on which wire timeframes (see condition.v1.json#/$defs/timeframe) — used by AFB to validate indicator/price-candle condition timeframes before publish.
   */
  market_data?: {
    quotes?: boolean;
    candles?: boolean;
    orderbook?: boolean;
    timeframes?: ConditionV1_Timeframe[];
    [k: string]: unknown;
  };
  features?: {
    dry_run?: boolean;
    /**
     * Alias kept for backward compatibility — equivalent to `hybrid` being present in execution_modes.
     */
    server_sltp?: boolean;
    /**
     * Deal execution modes this BF instance supports (see deal.v2.json#/$defs/executionPolicy/properties/execution_mode). AFB/UI use this to offer only modes the BF can actually run.
     */
    execution_modes?: ('client' | 'hybrid' | 'server')[];
    reports_api?: boolean;
    /**
     * This BF build accepts calendar.update (see payloads/calendar.update.json) — a replace-all MOEX trading calendar snapshot (holidays/weekend sessions, per-board session windows) it uses to gate execution and background broker polling on real trading-session boundaries instead of its own static off-hours config. AFB gates sending calendar.update on this flag being true; absent/false means the BF is never sent a calendar snapshot and keeps gating on its own local config.
     */
    market_calendar?: boolean;
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DaemonCapabilitiesQueryPayload".
 */
export interface DaemonCapabilitiesQueryPayload {
  [k: string]: unknown;
}
/**
 * RESERVED — not implemented: this message lets a BF ask AFB for an additional dataset subscription. AFB today derives the full set of needed (dataset_id, instrument) pairs itself from the dataset conditions on deals published to a given BF (see dataset.update.json) and pushes accordingly, so no BF currently sends dataset.subscribe and AFB is not obligated to act on it if received. The shape is reserved on the wire for a future BF-initiated use case (e.g. a BF wanting a dataset ahead of publishing a deal that needs it). Neither BF nor AFB implement this today.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DatasetSubscribePayload".
 */
export interface DatasetSubscribePayload {
  subscriptions: {
    /**
     * Same vocabulary as dataset.update.json#/properties/datasets/items/properties/dataset_id.
     */
    dataset_id: 'positions' | 'orders' | 'hhi' | 'trades';
    instrument: DealInstrument;
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * AFB-pushed feed of MOEX/Algopack dataset snapshots (positions/orders/hhi/trades) so BF can evaluate `condition.v1.json`'s dataset operator itself — BF has no exchange/Algopack access of its own and never will (the Algopack token is IP-bound to AFB). SNAPSHOT SEMANTICS: `datasets` is the FULL current set of records this AFB wants this BF to hold, never a diff — on receipt BF REPLACES its entire dataset cache for the connection with this array (replace-all, not merge); a record absent from a later dataset.update is gone, not merely unchanged. An empty `datasets` array is valid and means 'nothing needed' (clears the cache). AFB derives which (dataset_id, instrument) pairs are needed from the dataset conditions on deals currently published to this BF (every leg — entry/stop_loss/take_profit, both left and right sides of the comparison) and resolves exchange-side keying itself (e.g. a futures position dataset is keyed by the underlying asset, not the contract code) — BF must not attempt to re-derive or re-key this.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DatasetUpdatePayload".
 */
export interface DatasetUpdatePayload {
  /**
   * Full replacement set of dataset records for this BF; [] means none needed.
   */
  datasets: {
    /**
     * Same vocabulary as condition.v1.json#/$defs/datasetExpr/dataset_id, except `volume` — declared in condition.v1.json but not computed by AFB or BF and never pushed here.
     */
    dataset_id: 'positions' | 'orders' | 'hhi' | 'trades';
    instrument: DealInstrument1;
    /**
     * ISO-8601 exchange-side snapshot time (when this data was true on MOEX), not the time AFB sent the message.
     */
    as_of: string;
    /**
     * TTL in seconds set by AFB from its knowledge of the source update cadence. The record is usable while now <= as_of + stale_after_sec; once stale, BF must treat it as ABSENT (dataset condition evaluates to false, fail-safe — no entry), not as a frozen last-known value. Not hardcoded on BF: MOEX currently republishes this statistics about every 5 minutes, a move to 1-minute cadence is planned, and stale_after_sec is how AFB communicates the current cadence without a protocol change.
     */
    stale_after_sec: number;
    /**
     * Dataset field name -> numeric value for the current snapshot (e.g. {"long": "..."} is wrong — values are numbers, not decimal strings, unlike price/sizing fields elsewhere in this protocol). A field absent here is simply not included, never sent as null.
     */
    current: {
      [k: string]: number;
    };
    /**
     * Same shape as `current`, for the prior snapshot. Optional — a previous snapshot may not exist yet (e.g. right after (re)subscription/session start). Needed only for the cross-* operators (crosses_above/crosses_below/crossing) in condition_semantics, which compare a prev/cur pair on both sides; plain above/below only need `current`.
     */
    previous?: {
      [k: string]: number;
    };
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * Deal-level instrument this record is keyed by. AFB has already resolved exchange-side nomenclature quirks (e.g. positions for a futures instrument are keyed by the underlying asset on MOEX, not the contract ticker) — BF matches condition legs to records by this field as-is.
 */
export interface DealInstrument1 {
  exchange: string;
  board: string;
  ticker: string;
  /**
   * Full composite key identifying one catalog listing or derivative: `<MIC>[:<board|market>]:<ticker>` (e.g. `MISX:TQBR:SBER`, `MISX:RFUD:IMOEXF`), or the venueless 2-segment derivative form `<MIC>:<code>` (e.g. `MISX:IMOEXF`) where the wire explicitly identifies a derivative rather than a listing. Case-sensitive, never normalized (`.lower()`/`.upper()`) on either side of the AFB backend<->frontend channel.
   */
  instrument_key?: string;
  /**
   * Opaque broker locator of the instrument, e.g. `TICKER@MIC`. AFB takes it from its listing_link (finam.db); BF resolves the instrument ONLY by it (no BF-side catalog). Not part of the instrument identity: amend identity is decided by instrument_key (or exchange/board/ticker), see amend_rules. Absent => BF rejects with instrument_unresolvable unless the deal binding already carries a symbol.
   */
  broker_symbol?: string;
  market?: 'stock' | 'futures' | 'currency';
  price_step?: DecimalString;
  step_price?: DecimalString;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAcceptedPayload".
 */
export interface DealAcceptedPayload {
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  binding?: {
    account_id?: string;
    symbol?: string;
    [k: string]: unknown;
  };
  broker_instrument?: {
    /**
     * Which order/trigger prices the instrument allows (Finam AssetParams.price_type): POSITIVE = strictly > 0; NON_NEGATIVE = >= 0; ANY = negative prices allowed (e.g. some futures); UNKNOWN = the broker did not say. Optional — absent means UNKNOWN.
     */
    price_type?: 'UNKNOWN' | 'POSITIVE' | 'NON_NEGATIVE' | 'ANY';
    asset_type?: string;
    bond_details?: string | number | boolean | {} | unknown[] | null;
    decimals?: number;
    expiration_date?: string | number | boolean | {} | unknown[] | null;
    future_details?: string | number | boolean | {} | unknown[] | null;
    long_initial_margin?: string;
    long_risk_rate?: string;
    longable?: boolean;
    lot_size?: number;
    market?: string;
    mic?: string;
    min_step_raw?: number;
    name?: string;
    price_step?: string;
    quote_currency?: string;
    short_initial_margin?: string;
    short_risk_rate?: string;
    shortable?: boolean;
    tradable?: boolean;
    updated_at?: string;
    [k: string]: unknown;
  };
  broker_sizing?: {
    account_id?: string;
    deal_notional?: string;
    lots?: number;
    required_cash?: string;
    required_cash_basis?: string;
    sizing_mode?: string;
    /**
     * True when lots/required_cash were computed from estimate-only prices (live last instead of an indicator entry condition's price, and/or an indicator stop condition's current value instead of a fixed stop price) rather than the deal's actual condition prices. The final sizing is recomputed when the entry condition fires.
     */
    estimated?: boolean;
    [k: string]: unknown;
  };
  command_type: string;
  deal_id: string;
  revision: number;
  target_instrument_patch?: {
    [k: string]: unknown;
  };
  validation?: {
    account_id?: string;
    side: string;
    sizing_mode?: string;
    sizing_value?: string;
    symbol?: string;
    quantity_lots?: number;
    entry_price?: string;
    required_cash?: string;
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * Re-define an existing deal in place. `deal` is the full new definition (its `revision` must be `base_revision` + 1, same `deal_id`). BF gates the change against the allowed-edit matrix (amend_rules) using the deal's live execution phase, then lets reconcile bring broker orders to the new desired state. Unlike deal.publish, the deal's status and observed execution state (orders/positions/phase) are preserved.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAmendPayload".
 */
export interface DealAmendPayload {
  deal_id: string;
  base_revision: number;
  deal: DealV2;
  /**
   * SHA-256 (hex) of the canonical JSON of the deal DEFINITION as AFB defined it — computed ONLY by AFB, over an AFB-owned allowlist (see docs/PROTOCOL.md, 'definition_hash'). BF stores the received value verbatim and never recomputes it (BF enriches the deal body — broker_instrument, broker_sizing, binding — so a BF-side hash would differ without any lost message); it echoes it in session.resync_request so AFB can see 'same revision, different content'. Optional: an older AFB omits it.
   */
  definition_hash?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealArchivedPayload".
 */
export interface DealArchivedPayload {
  archived_at?: string;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`; equal to `archived_at` for this event).
   */
  at?: string;
  deal_id: string;
  reason: string;
  revision: number;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealOperationPayload".
 */
export interface DealOperationPayload {
  operations?: {
    deal_id: string;
    revision: number;
    op?: string;
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPositionsSyncedPayload".
 */
export interface DealPositionsSyncedPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  changed?: {
    average_price?: string;
    quantity?: number;
    symbol?: string;
    [k: string]: unknown;
  }[];
  deal_id: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublishPayload".
 */
export interface DealPublishPayload {
  deal: DealV2;
  /**
   * SHA-256 (hex) of the canonical JSON of the deal DEFINITION as AFB defined it — computed ONLY by AFB, over an AFB-owned allowlist (see docs/PROTOCOL.md, 'definition_hash'). BF stores the received value verbatim and never recomputes it (BF enriches the deal body — broker_instrument, broker_sizing, binding — so a BF-side hash would differ without any lost message); it echoes it in session.resync_request so AFB can see 'same revision, different content'. Optional: an older AFB omits it.
   */
  definition_hash?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealRejectedPayload".
 */
export interface DealRejectedPayload {
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  /**
   * Machine-readable rejection code. Instrument-resolution codes: `instrument_unresolvable` (no broker symbol in the binding or target.instrument.broker_symbol, or the broker does not know it), `instrument_mismatch` (the broker asset behind broker_symbol disagrees with the deal's exchange/board/ticker), `instrument_delisted` (the instrument was delisted/archived at the broker), `unsupported` (the BF/connector cannot execute this deal, e.g. an unsupported mode/market).
   */
  code: string;
  /**
   * Command type of the AFB command that was rejected. Absent for rejections not caused by an AFB command (e.g. execution: the broker rejected the entry order).
   */
  command_type?: string;
  deal_id?: string | number | boolean | {} | unknown[] | null;
  message?: string;
  broker_error?: PayloadsDealRejected_BrokerError;
  [k: string]: unknown;
}
/**
 * Report attached to deal.status_changed(closed) with the trade-based fill log for the just-closed deal. It may be sent again for the same deal as a PATCH (same fills, enriched with data the broker books later, e.g. `fills[].exchange_fee`; every send gets a new `deal_seq` and idempotency key) — a consumer merges by `trade_id` and must not treat the repeat as a second close. `trade_id` is not required — tolerant of older BF versions that predate it. The `summary` block (entry/exit_avg_price, realized_pnl, total_commission) was removed in v2.0.10: it had no consumers (AFB computes realized PnL itself from fills/order events), was never in `required`, and `additionalProperties: true` keeps old and new payloads mutually valid — a PATCH, not a breaking change. `fills[].commission` was removed in the same step for the same reason; it is replaced by the optional per-trade `fills[].exchange_fee` (a real consumer exists now: realized P&L after exchange fee) — BROKER commission is intentionally not carried per deal.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealReportPayload".
 */
export interface DealReportPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  close_reason?: string;
  deal_id: string;
  revision: number;
  status: string;
  /**
   * Trade-based fill log: one element per broker trade, not per order — an order filled in several trades (e.g. Finam SubscribeTrades) yields one element per trade, all sharing the same order_id. `order_id` remains the reference to the parent order (for role/leg); `summary` and the aggregate commission fields are not part of this payload (removed in v2.0.10, see below); the per-trade exchange fee is the optional `exchange_fee`.
   */
  fills?: {
    /**
     * Broker trade identifier. For brokers without a native trade concept, a synthetic id derived from order_id (e.g. `synth-{order_id}`).
     */
    trade_id?: string;
    order_id: string;
    price?: string | number | boolean | {} | unknown[] | null;
    quantity?: number;
    /**
     * Exchange fee (Finam `AccountTrade.commission`, the BUYSELLFEE part) charged for this very trade. The broker books it after clearing, so it is absent in the closing report and arrives later in a repeated deal.report (same fills, new `deal_seq`) — consumers merge it by `trade_id`. The BROKER commission is deliberately NOT part of this payload: it depends on the tariff (per contract, % of daily turnover, side-dependent) and cannot be attributed to a single deal; it travels per account in broker.accounts `broker_fees`.
     */
    exchange_fee?: {
      /**
       * Decimal string, positive = charged.
       */
      value: string;
      currency: string;
    };
    role: string;
    side: string;
    /**
     * ISO-8601 fill time (order's last status-transition time on BF); may be null for legacy BF versions predating this field.
     */
    timestamp?: string | number | boolean | {} | unknown[] | null;
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealSnapshotPayload".
 */
export interface DealSnapshotPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  deal_id: string;
  execution_phase?: string;
  observed?: {};
  positions?: {
    symbol?: string;
    quantity?: number;
    average_price?: string;
    updated_at?: string;
    [k: string]: unknown;
  }[];
  /**
   * Resolved order quantity (lots), fixed once by BF at entry-trigger time (`resolved_quantity`). Present only once known — never present before the entry order is placed, never cleared afterward.
   */
  quantity?: number;
  status?: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealStatusChangedPayload".
 */
export interface DealStatusChangedPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  deal_id: string;
  execution_phase?: string;
  last_price?: string;
  /**
   * Resolved order quantity (lots), fixed once by BF at entry-trigger time (`resolved_quantity`). Present only once known — never present before the entry order is placed, never cleared afterward.
   */
  quantity?: number;
  revision: number;
  status: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "OrderCreatedPayload".
 */
export interface OrderCreatedPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  deal_id: string;
  /**
   * BF's own client_order_id (cid) — the same identifier every order.* /position.* event for this order carries, and the one to match against StoredOrder.order_id. NOT the broker's exchange order id (see broker_order_id below) — Волна 1/2 (deal-457d-4583-a1f7 follow-up): older BF builds put the broker id here, which never matched a fill's order_id and made this event unusable for AFB to learn a fresh order's resolved quantity.
   */
  order_id: string;
  /**
   * The broker's own exchange order id, when known at emission time — opaque to AFB, useful only for cross-referencing with broker-side records/support. Optional: absent for a dry-run/synthetic order, or when the broker never returned one.
   */
  broker_order_id?: string;
  price?: string | number | boolean | {} | unknown[] | null;
  quantity?: number;
  role: string;
  side: string;
  status: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "OrderFilledPayload".
 */
export interface OrderFilledPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  deal_id: string;
  filled_quantity?: number;
  leg_index?: number;
  order_id: string;
  price?: string | number | boolean | {} | unknown[] | null;
  quantity?: number;
  role: string;
  side: string;
  status: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PositionOpenedPayload".
 */
export interface PositionOpenedPayload {
  /**
   * Per-deal monotonic event number assigned by BF (persisted with the deal; survives restart). Present on events BF writes to the deal's event journal; a gap seen by AFB means a lost event, healed on the next session.resync (BF replays the journal tail above the `applied_deal_seq` AFB reports). On deal.snapshot it is the last number issued at snapshot time and is not itself consumed. Optional: an older BF omits it, an older AFB ignores it.
   */
  deal_seq?: number;
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  average_price?: string;
  deal_id: string;
  quantity?: number;
  realized_pnl?: string | number | boolean | {} | unknown[] | null;
  symbol?: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionEnrollRequestPayload".
 */
export interface SessionEnrollRequestPayload {
  bf_id: string;
  client_nonce: string;
  bf_public_key: string;
  mac: string;
  protocol: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionEnrollResponsePayload".
 */
export interface SessionEnrollResponsePayload {
  bf_id: string;
  server_nonce: string;
  afb_public_key: string;
  mac: string;
  protocol: string;
  bf_name?: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionHeartbeatPayload".
 */
export interface SessionHeartbeatPayload {
  bf_id: string;
  broker_connected?: boolean;
  uptime_sec?: number;
  health?: {
    overall?: 'ok' | 'warning' | 'critical';
    points?: {};
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionHelloPayload".
 */
export interface SessionHelloPayload {
  bf_id: string;
  dry_run?: boolean;
  margin_trading?: boolean;
  /**
   * BF-proposed heartbeat period (seconds); AFB may clamp in hello_ack.
   */
  heartbeat_interval_sec?: number;
  nonce: string;
  protocol: string;
  version?: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionHelloAckPayload".
 */
export interface SessionHelloAckPayload {
  server_nonce?: string;
  /**
   * Negotiated heartbeat interval (seconds): BF proposal from session.hello, clamped by AFB to connector_defaults.heartbeat_interval_min/max. BF must use this value for session.heartbeat period.
   */
  heartbeat_interval_sec?: number;
  protocol: string;
  accepted_protocol?: string;
  dry_run?: boolean;
  /**
   * @deprecated
   * Deprecated: use dry_run (effective session value) instead.
   */
  dry_run_afb?: boolean;
  /**
   * @deprecated
   * Deprecated: use dry_run (effective session value) instead.
   */
  dry_run_bf?: boolean;
  margin_trading?: boolean;
  /**
   * @deprecated
   * Deprecated: use margin_trading (effective session value) instead.
   */
  margin_trading_afb?: boolean;
  /**
   * @deprecated
   * Deprecated: use margin_trading (effective session value) instead.
   */
  margin_trading_bf?: boolean;
  /**
   * AFB-side capability flags for this session — read by BF's afb_client (see afb_client/ws_client.py, alongside dry_run/margin_trading above). No flags are currently defined: multi-account (broker.get_accounts/broker.accounts) is the only account path and is always supported by both sides (formerly features.multi_account).
   */
  features?: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionReenrollRequestPayload".
 */
export interface SessionReenrollRequestPayload {
  bf_id: string;
  reason?: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionResyncRequestPayload".
 */
export interface SessionResyncRequestPayload {
  /**
   * Canonical per-deal inventory: {deal_id: {revision, status, execution_phase, archived}}
   */
  deals?: {
    [k: string]: {
      revision: number;
      status: string;
      execution_phase?: string;
      /**
       * The definition_hash BF last accepted for this deal (verbatim from deal.publish/deal.amend/deal.resync; absent if AFB never sent one).
       */
      definition_hash?: string;
      /**
       * Last deal_seq BF issued for this deal (0/absent: none).
       */
      deal_seq?: number;
      archived: boolean;
    };
  };
  /**
   * Legacy field — use 'deals' instead.
   */
  active_deal_ids?: string[];
  /**
   * Legacy field — archived deals are now in 'deals' with archived=true.
   */
  deal_archived?: {
    [k: string]: string;
  };
  /**
   * Legacy field — use 'deals' instead.
   */
  deal_revisions?: {
    [k: string]: number;
  };
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "SessionResyncResponsePayload".
 */
export interface SessionResyncResponsePayload {
  /**
   * Canonical per-deal inventory: {deal_id: {revision, status, execution_phase, archived: false}}
   */
  deals?: {
    [k: string]: {
      revision: number;
      status: string;
      execution_phase?: string;
      /**
       * AFB's current definition_hash of this deal (absent: not computed).
       */
      definition_hash?: string;
      /**
       * Highest deal_seq AFB applied for this deal (0/absent: none). BF replays its journal entries above it.
       */
      applied_deal_seq?: number;
      archived: boolean;
    };
  };
  /**
   * Legacy field — use 'deals' instead.
   */
  deal_revisions?: {
    [k: string]: number;
  };
  /**
   * Legacy field — use 'deals' instead.
   */
  deal_statuses?: {
    [k: string]: string;
  };
  [k: string]: unknown;
}
/**
 * Server-owned storage field, written once when the plan is archived: a self-contained snapshot of the chart components the plan used (the plan's own line primitives — physically removed from the live gp store on archive — and the indicators its conditions reference), so an archived plan keeps its historical drawing without depending on gp. Items are copies of AFB's internal gp/indicator storage records, deliberately not formalized here (they are never sent to clients; the channel drops this field). Re-archiving an archived plan carries the snapshot forward unchanged.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_ArchivedComponents".
 */
export interface TradeplanV2_ArchivedComponents {
  primitives: {}[];
  indicators: {}[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_TpLeg".
 */
export interface TradeplanV2_TpLeg {
  /**
   * Stable identity of a tradeplan leg across edits — the key overrides/carry-over (tradeplan/deal separation Фаза B2) use to match a plan leg to its compiled deal leg, never array position. Assigned once when a leg is created and never reused/reassigned. Shared by tradeplan.v2.json (stored/channel legs) and afbws/deal.public.v1.json (the plan-leg identity projected onto deal legs). Legacy synthetic ids (`legacy:{role}:{index}`) are NOT part of the contract: a plan leg without `leg_id` exists only in an input message (the server assigns one on save) or in an old stored file (the server back-fills it on the next write).
   */
  leg_id?: string;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
  condition: TradeplanV2_TpConditionNode;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_TpConditionNode".
 */
export interface TradeplanV2_TpConditionNode {
  id?: string;
  op?: TradeplanV2_ConditionOp;
  /**
   * Required (enforced after compilation, not here) when op is a price candle operator (breakout/breakdown/crossing).
   */
  timeframe?: '5min' | '10min' | '15min' | '30min' | '1h' | '2h' | '4h' | '1d';
  duration?: ConditionV1_Duration;
  left: TradeplanV2_ConditionLeft;
  right: TradeplanV2_ConditionRight;
}
