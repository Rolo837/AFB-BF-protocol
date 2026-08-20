/**
 * DO NOT EDIT BY HAND — generated from spec/schemas/ (all *.json files) by
 * ts/tools/generate-models.mjs (invoked via `afb-bf-protocol-generate`).
 * source-hash: 80b8e5eeb7690bff0293524b8478aec26a7235ab558798e4c857d4aa25d887cb
 */

/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.account.channel.v1). Replaces legacy `channel=account, type=get_account|get_orders|get_events` for clients that negotiated this capability; legacy stays available as fallback — same channel name (`account`) for both, discriminated by presence of `schema` vs `type`, never both in the same session. The legacy `get_catalog`/`get_instrument`/`resolve_instrument` commands are NOT part of this migration — they are already superseded by the `instrument` channel (see instrument.channel.v1.json) for negotiated clients. `item`/`items` are explicit allow-list projections built by backend/trade/public_views.py, never a verbatim proxy of a BF broker.* payload — see $defs/accountSnapshot and $defs/order, which independently declare their own strict shape (reusing only the field-level $defs of payloads/broker.accounts.json/broker.orders.json, not their whole root) so this channel never inherits the wire schemas' additionalProperties:true. `account` here means a broker account (one bf_id/connector may have more than one — see broker.get_accounts/broker.accounts on the AFB<->BF wire), not the connector itself. See AFB/docs/ENTITY_WS_PROTOCOL.md and plans/account-channel-migration (account.md).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountChannelV1Message".
 */
export type AccountChannelV1Message =
  | AccountListRequest
  | AccountListResponse
  | AccountGetRequest
  | AccountGetResponse
  | AccountOrdersRequest
  | AccountOrdersResponse
  | AccountEventsRequest
  | AccountEventsResponse
  | AccountErrorResponse
  | AccountSnapshotPush
  | AccountOrdersPush;
/**
 * Client-generated correlation id (e.g. uuid4), echoed verbatim in the matching response.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCommonV1_RequestId".
 */
export type AfbwsCommonV1_RequestId = string;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountBfId".
 */
export type AccountBfId = string;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountAccountId".
 */
export type AccountAccountId = string;
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
  | 'unsupported_action';
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.alarm.channel.v1). Replaces bulk settings/get_alarms+set_alarms and mail/alarms+mail/ack for clients that negotiated this capability; legacy stays available as fallback for clients that did not. See AFB/docs/ENTITY_WS_PROTOCOL.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmChannelV1Message".
 */
export type AlarmChannelV1Message =
  | AlarmGetRequest
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
  | AlarmAckResponse;
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
 * Negotiated via auth.support/auth_ok.support (capability id afbws.deal.channel.v1) — the sole entry point for `channel=deal`, the AFB legacy schema-less transport was removed. `item`/`items`/`results` never carry the persisted DealState file shape (source_refs, status_history, event_journal, raw orders/positions, observed) — see $defs/dealSummary and $defs/dealDetail, built by backend/trade/public_views.py as explicit allow-list projections. The publish/rebind/amend RPCs resolve the source tradeplan only via deal.source.tradeplan_id (deal.public.v1.json); they never accept an inline plan-like draft. See AFB/docs/ws/deal.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealChannelV1Message".
 */
export type DealChannelV1Message =
  | DealGetRequest
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
  | DealAckResponse;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealId".
 */
export type DealId = string;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BfId".
 */
export type BfId = string;
/**
 * Explicit allow-list projector output over afb.deal.v1/v2 (../deal.v1.json, ../deal.v2.json), built by backend/trade/public_views.py — never a serialization of the persisted DealState file. Deliberately NOT an allOf+$ref extension of the whole wire root: those wire schemas declare `owner`/`archive_reason` in their own `properties` with no `additionalProperties: false`, so those fields would count as already-'evaluated' and survive an outer `unevaluatedProperties: false` — the only way to actually drop them is to define this object's own shape directly and reuse the wire schemas' field-level $defs (target, sizing, conditions, execution policy) rather than their root. `source` is strict and requires `tradeplan_id` — the single public link back to the owning tradeplan; `source.kind`/`draft_id`, compile snapshots and raw phase-B overrides never appear here. The one internal field that IS projected — per-leg, not on `source` — is `leg_id` (v2 legs only), the plan-leg identity the frontend needs to tell which deal leg still tracks which plan leg.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicV1".
 */
export type DealPublicV1 = DealPublicDealV1 | DealPublicDealV2;
/**
 * Stable identity of this leg across edits — the key overrides/carry-over (tradeplan/deal separation Фаза B2) use to match a plan leg to its compiled deal leg, never array position. Assigned once when a leg is created and never reused/reassigned; a plan predating this field falls back to a deterministic `legacy:{role}:{index}` synthetic id at compile time (see AFB backend/tradeplans/models.py) until migrated.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_LegId".
 */
export type TradeplanV2_LegId = string;
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
  leg_id?: TradeplanV2_LegId;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
  condition: DealV2_ConditionNode;
  source?: DealV2_LegSource;
}[];
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAmendField".
 */
export type DealAmendField = 'entry' | 'sizing' | 'stop_loss' | 'take_profit' | 'execution_policy';
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealOperationItem".
 */
export type DealOperationItem = {
  [k: string]: unknown;
} & {
  deal_id: DealId;
  action: 'activate' | 'pause' | 'resume' | 'cancel' | 'reconcile' | 'delete';
  revision?: number;
  /**
   * Only meaningful for action='cancel' — see the allOf guard below.
   */
  cancel_open_orders?: boolean;
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.gp.channel.v1). Replaces bulk settings/get_primitives+set_primitives for clients that negotiated this capability; legacy stays available as fallback for clients that did not. `list()` (no ticker) returns every primitive the caller owns across all tickers; `list(ticker)` filters to one canonical SECID. `set` is a plain upsert by item.id — moving a primitive (new start/stop) is the same request as creating or editing one, never a separate command; there is no bulk-set and no confirm/usage RPC — the backend alone decides whether a move/delete is safe against linked tradeplans and answers with a typed conflict (see errorResponse) instead of the client asking first. See AFB/docs/ENTITY_WS_PROTOCOL.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpChannelV1Message".
 */
export type GpChannelV1Message =
  | GpGetRequest
  | GpGetResponse
  | GpListRequest
  | GpListResponse
  | GpSetRequest
  | GpSetResponse
  | GpDeleteRequest
  | GpDeleteResponse
  | AfbwsGpChannelV1_SyncPush
  | GpErrorResponse;
/**
 * AFB-side chart primitive (line/line_enter/line_sl/line_tp/note/zone/ruler) — like afb.alarm.v1, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel. Promotes the parked settings.primitives[secid][] draft (draft/primitive.v1.json) into a strict canonical entity: `ticker` becomes an explicit required field instead of an implicit dict key, so get(id)/list(ticker) work on a flat collection. Whether a primitive is REFERENCED BY a tradeplan's condition is still derived fresh from the tradeplans themselves on every read, never persisted here. OWNERSHIP is different and is persisted — see `tradeplan_id`. `stop` is a second anchor point required only for zone/ruler (forbidden for every other kind, enforced by the `allOf` below, not just by convention); `text` is accepted only for `note` (optional even there).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpV1".
 */
export type GpV1 = {
  [k: string]: unknown;
} & {
  schema: 'afb.gp.v1';
  id: string;
  ticker: string;
  kind: 'line' | 'line_enter' | 'line_sl' | 'line_tp' | 'note' | 'zone' | 'ruler';
  start: GpV1_Point;
  stop?: GpV1_Point;
  /**
   * note only (optional even there).
   */
  text?: string;
  /**
   * Владеющий торговый план. Проставляется сервером при компиляции плана в сделку (публикация/amend); снимается только при физическом удалении плана. Клиент это поле не задаёт и не меняет — в set-запросе оно игнорируется в пользу хранимого значения. Пустое/отсутствующее — свободный примитив, доступный любому плану. При архивации плана его уровни физически удаляются из этого хранилища, но условия плана НЕ переписываются в числа — план сохраняет исходные ссылки на примитивы; полная копия каждого удалённого уровня (kind/координаты/стиль) переносится в archived_components плана и является источником его исторической отрисовки.
   */
  tradeplan_id?: string;
};
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.instrument.channel.v1). Replaces legacy `securities/list`, `setup/markets`+`get_assign`+`set_assign`, and `account/get_catalog`+`get_instrument`+`resolve_instrument` for clients that negotiated this capability; legacy stays available as fallback. `catalog` is the one read snapshot of the curated catalog for any authenticated caller. `get`/`resolve`/`detail` are also open to any authenticated caller (unlike legacy `securities/list`, which allowed anonymous access — that is not carried over). `catalog` is the Assets-modal UI snapshot of the curated catalog — same wire form for every authenticated caller; the backend varies completeness (manager also sees unassigned assets, user sees only live sets and the assets in them — sets/assets carry no archived flag). `commit`/`pool`/`sources`/`refresh` require the manager gate. `pool` pages the backend MOEX universe as discriminated listing|series rows (futures appear as series, not expirations); broker/BF sources are not served in this revision. `inventory` is the full exchange instrument inventory (paged, filterable). `collections` build the Catalog tree (category hierarchy); `asset_sets` are named Sets of assets (not the category tree). `catalog` may carry `suggestions` for pending asset proposals; `commit.accept_suggestions` resolves them. `commit` is the sole write, a CAS-guarded delta against `base_revision`; stale revisions return `conflict` with the current revision in errorResponse.details. Pending pool listings/series and asset full composition travel in that one commit. `user` is the caller's personal-sets/overlay operation and is served. `resolve` keeps the pre-flight semantics of legacy `account/resolve_instrument` (compiles a tradeplan draft and asks the target BF to resolve it) but returns the canonical instrument shape instead of an untyped proxy blob. `detail` is a lighter sibling of `resolve` for the tradeplan editor: given just `bf_id`+`ticker` for an already-catalogued instrument, it fetches live broker-side trading params (margin, tradable/longable/shortable) without compiling a draft — no new AFB<->BF wire message, it drives the same `broker.resolve_instrument` mechanism as `resolve` against a minimal synthetic venue triplet. See AFB/docs/ENTITY_WS_PROTOCOL.md. Federated-catalog phase 2 expresses manager curation as arbitrary, freely overlapping SETS (see assetSetView) instead of the single-parent group tree, plus an independent futures-series axis (catalogSeries) in place of legacy `asset`. Phase 2.5 inserts an ASSET (catalogAsset) between a single listing and a set: an asset is a small bundle of instruments that share one pricing source — "Brent oil" is the BR-* and BRM-* series together — and it, not the ticker, is what a set contains (`asset_sets[].asset_ids`) and what reference data (MOEX positions, HHI) hangs off. A series joins an asset whole, so a contract that arrives with the daily refresh belongs to its sets by definition instead of by a membership heuristic. Catalog and commit snapshots nest membership and composition on the entities themselves — an asset set carries its ordered `asset_ids`, an asset its ordered `members`. Order is carried by array position everywhere on the wire: no entity has an order field, and a write restates a full order through the dedicated `asset_set_order`/`collection_order`/`order` sections of `commit`. The manager-only `sources`/`refresh` pair makes catalog updates explicit: `sources` lists feeds (MOEX/ISS or a broker connector) with availability and last-refresh state, while `refresh` runs one source and returns its change report; `dry_run: true` produces the same report without writing.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentChannelV1Message".
 */
export type InstrumentChannelV1Message =
  | InstrumentGetRequest
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
  | InstrumentSourcesRequest
  | InstrumentSourcesResponse
  | InstrumentRefreshRequest
  | InstrumentRefreshResponse
  | InstrumentInventoryRequest
  | InstrumentInventoryResponse
  | InstrumentErrorResponse;
/**
 * AFB-side canonical instrument — like afb.gp.v1/afb.alarm.v1, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel. One broker-agnostic shape for every market class (stock/futures/currency/index); class-specific fields are gated by `market` via the `allOf`/`if` blocks below (forbidden, not just absent, for classes they don't apply to), but the wire type stays a single schema. `ticker` is the canonical identity: bare SECID for MOEX (e.g. "SBER"), `EXCHANGE:TICKER` for everything else (e.g. "XNAS:AAPL") — `exchange`/`board`/`market` are still carried as explicit fields so nothing but one shared parser (AFB backend/instruments/identity.py, frontend utils/instrumentId.ts) ever splits the string. `group`/`asset` place the instrument in the curated catalog tree (config/instruments.yaml) that AFB users actually see — `group: null` means not yet distributed into a group, the flat-list replacement for the old `lost` bucket. `source` says who refreshes this record's trading params ("moex" for the daily ISS refresh, a broker id like "finam" for instruments obtained from that broker's catalog) — it is NOT a broker binding: which connector can actually trade this instrument, and under what broker-native symbol, is resolved at publish time (see deal.v1.json's target.instrument + BF's own catalog), never persisted here.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentV1".
 */
export type InstrumentV1 = {
  [k: string]: unknown;
} & {
  schema: 'afb.instrument.v1';
  /**
   * Canonical identity: bare SECID for MOEX, "EXCHANGE:TICKER" otherwise.
   */
  ticker: string;
  exchange: string;
  board: string;
  market: 'stock' | 'futures' | 'currency' | 'index';
  name?: string | null;
  shortname?: string | null;
  /**
   * Underlying asset code (futures) or self-grouping code.
   */
  asset?: string | null;
  /**
   * Catalog group key; null = not yet distributed.
   */
  group: string | null;
  lot_size?: number | null;
  price_step?: DecimalString;
  decimals?: number | null;
  currency?: string | null;
  /**
   * Previous trading day's close (MOEX PREVPRICE/PREVWAPRICE), not a live quote.
   */
  prev_close?: string;
  /**
   * Futures only.
   */
  expiration?: string;
  step_price?: DecimalString;
  margin?: DecimalString;
  /**
   * Futures only; FUTOI series/perpetual code.
   */
  futoi_code?: string;
  /**
   * Stock only.
   */
  isin?: string;
  /**
   * "moex" or a broker id (e.g. "finam") — who refreshes this record's trading params.
   */
  source: string;
};
/**
 * Source is MOEX-only in this revision: omit `source` or send "moex". A bf_id is invalid — broker pool is not served. `kind` selects listing vs series rows; `market` filters by class. `kind=listing` cannot be paired with `market=futures` (futures are series rows); `kind=series` cannot be paired with a non-futures market. `limit` defaults to 50 and is capped at 200. `cursor` is an opaque token bound to the same `query`/`kind`/`market` filter tuple and to the pool snapshot that produced it (see `fetched_at`); a mismatched or stale cursor is `validation_error` or `conflict`, not a silent restart at the first page.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentPoolRequest".
 */
export type InstrumentPoolRequest = {
  [k: string]: unknown;
} & {
  channel: 'instrument';
  schema: 'afbws.instrument.pool.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * Only MOEX is served. Omit or send "moex"; any other value (including a bf_id) is invalid.
   */
  source?: 'moex';
  /**
   * Optional substring filter over ticker, short/full name, and series code/name. Applied server-side against the in-memory MOEX snapshot.
   */
  query?: string;
  /**
   * `listing` — non-futures instruments; `series` — futures series rows, not expirations.
   */
  kind?: 'listing' | 'series';
  market?: 'stock' | 'futures' | 'currency' | 'index';
  /**
   * Page size. Default 50 when omitted, maximum 200. Bounds are enforced by this schema.
   */
  limit?: number;
  /**
   * Opaque page cursor from a previous next_cursor of THIS filter (`query`/`kind`/`market`) against the same pool snapshot. Omit on the first page. Reusing a cursor after the snapshot is refreshed, or with a different filter tuple, is `validation_error` or `conflict` — the client must restart from the first page.
   */
  cursor?: string;
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentPoolEntry".
 */
export type InstrumentPoolEntry = InstrumentPoolListingEntry | InstrumentPoolSeriesEntry;
/**
 * Wraps the canonical listing so a pending draft copies `listing` into commitRequest.listings unchanged (send `group: null`). Futures do not appear here — they are poolSeriesEntry rows. `listing.market` must not be `futures`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentPoolListingEntry".
 */
export type InstrumentPoolListingEntry = {
  [k: string]: unknown;
} & {
  kind: 'listing';
  listing: InstrumentV1;
};
/**
 * Array position is the display order. `code` is the canonical ticker for `listing` and the series_code for `series`. `label` and `market` are denormalized for plaques so the Groups/Assets UI does not have to join `items`/`series`. A series member is whole: every expiration belongs to the asset. `kind=listing` is never a futures contract (`market` must not be `futures`); futures join an asset only as `kind=series`. The server still enforces that a futures contract may not be a listing member of an asset that already contains its series.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCatalogAssetMember".
 */
export type InstrumentCatalogAssetMember = {
  [k: string]: unknown;
} & {
  kind: 'listing' | 'series';
  /**
   * Canonical ticker for `listing`, series_code for `series` — case-sensitive, never normalized.
   */
  code: string;
  /**
   * Display label for plaques (shortname/name; backend may fall back to code).
   */
  label: string;
  market: 'stock' | 'futures' | 'currency' | 'index';
};
/**
 * True asset set (Наборы): metadata plus ordered `asset_ids`. The set's own display position is its position in `asset_sets[]` (and in `userState.sets[]` for a personal set) — there is no order field on the wire; a commit restates that order wholesale through `commitRequest.asset_set_order`. For scope=global, `visibility_tier` is required; for scope=user, `visibility_tier` is forbidden and `owner_user_id` is required.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentAssetSetView".
 */
export type InstrumentAssetSetView = {
  [k: string]: unknown;
} & {
  set_id: string;
  scope: 'global' | 'user';
  name: string;
  owner_user_id?: string | null;
  /**
   * Member assets in display order.
   */
  asset_ids: string[];
  visibility_tier?: 'manager' | 'user' | 'guest';
};
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentInventoryEntry".
 */
export type InstrumentInventoryEntry = InstrumentInventoryListingEntry | InstrumentInventorySeriesEntry;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentInventoryListingEntry".
 */
export type InstrumentInventoryListingEntry = {
  [k: string]: unknown;
} & {
  kind: 'listing';
  instrument_type: 'stock' | 'currency' | 'index' | 'futures';
  instrument_key: string;
  ticker: string;
  exchange: string;
  board: string;
  market: 'stock' | 'futures' | 'currency' | 'index';
  source: string;
  name?: string | null;
  shortname?: string | null;
  lifecycle?: string;
  series_code?: string;
};
/**
 * Manager view of a BF connector config record — reuses link.user.v1.json#/$defs/sharedFields (via $ref, not redeclared, so the two views can't drift apart) plus ACL/key management fields. Never carries `connected`/`daemon`/session runtime — see link.status.v1.json.
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
 * Negotiated via auth.support/auth_ok.support (capability id afbws.link.channel.v1). Replaces legacy channels `connector` (config CRUD) and `bfs` (registry push) for clients that negotiated this capability; legacy stays available as fallback. `entity` carries either afbws.link.user.v1 or afbws.link.admin.v1 depending on the caller's role — the backend chooses which, not the client. `pair`/`restart` are explicit per-id actions, not part of the get/list/set/delete CRUD set. Config (this file + link.user.v1.json/link.admin.v1.json) and runtime status (link.status.v1.json) are delivered as separate push types and never mixed into one item. See AFB/docs/ENTITY_WS_PROTOCOL.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkChannelV1Message".
 */
export type LinkChannelV1Message =
  | LinkGetRequest
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
  | LinkStatusPush;
/**
 * Role-chosen config view — afbws.link.user.v1 (non-manager, including the synthetic virtual pseudo-connector) or afbws.link.admin.v1 (manager).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkEntity".
 */
export type LinkEntity = LinkUserV1 | LinkAdminV1;
/**
 * Caller-scoped BF connector config record for a non-manager viewer (owner: capability trade + user_id in allowed_users, or role-only access — role-only is read-only, enforced by the backend, not this schema). Never carries `connected`/`daemon`/session runtime — see link.status.v1.json for that, delivered on a separate push. The synthetic `virtual` pseudo-connector also uses this exact shape (kind:"virtual") — see link.channel.v1.json. `$defs/sharedFields` is the single source of the fields link.admin.v1.json reuses (via $ref) so the two views can't drift apart independently. `$defs/setInputShared` is the same for set() payloads.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkUserV1".
 */
export type LinkUserV1 = BfRegistryEntry &
  LinkSharedFields & {
    schema: 'afbws.link.user.v1';
  };
/**
 * Role-chosen set() item shape — the backend selects which by the authenticated caller's role, never by a client-declared schema id. anyOf, not oneOf: neither shape carries a discriminating `schema` field, and a minimal payload (e.g. {bf_id, dry_run}) is structurally valid under both — oneOf would reject it as ambiguous. The backend, not this schema, decides which fields a given caller is actually allowed to use.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkSetInput".
 */
export type LinkSetInput = LinkUserSetInput | LinkAdminSetInput;
/**
 * A non-manager caller may adjust name/enabled/description/dry_run/execution_policy on their own already-existing connector — never broker/protocol/allowed_* /margin_trading, and never create a new entry (bf_id must already exist and be owned by the caller; enforced by the backend, not this schema).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkUserSetInput".
 */
export type LinkUserSetInput = LinkSetInputShared;
/**
 * Negotiated via auth.support/auth_ok.support (capability id afbws.tradeplan.channel.v1). Replaces bulk settings/get_plans+set_plans and mail/plans for clients that negotiated this capability; legacy stays available as fallback. `entity` carries both afb.tradeplan.v1 and afb.tradeplan.v2 — v1's `schema` is optional in its own canon file (legacy compatibility), so `entityV1` here wraps it with an explicit required-schema layer; v2 already requires `schema`. See AFB/docs/ENTITY_WS_PROTOCOL.md.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanChannelV1Message".
 */
export type TradeplanChannelV1Message =
  | TradeplanGetRequest
  | TradeplanGetResponse
  | TradeplanListRequest
  | TradeplanListResponse
  | TradeplanSetRequest
  | TradeplanSetResponse
  | TradeplanDeleteRequest
  | TradeplanDeleteResponse
  | AfbwsTradeplanChannelV1_ArchiveRequest
  | AfbwsTradeplanChannelV1_ArchiveResponse
  | TradeplanErrorResponse
  | TradeplanSyncPush;
/**
 * afb.tradeplan.v1 (schema required, see entityV1) or afb.tradeplan.v2 (schema already required in its own canon file — referenced directly, no wrapping $def needed).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanEntity".
 */
export type TradeplanEntity = TradeplanEntityV1 | TradePlanV2;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanEntityV1".
 */
export type TradeplanEntityV1 = TradePlanV1 & {
  [k: string]: unknown;
};
/**
 * price_value: null with condition_type price means market entry.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV1_EntryCondition".
 */
export type TradeplanV1_EntryCondition = TradeplanV1_MarketOrPriceCondition | TradeplanV1_PrimitiveCondition;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV1_Condition".
 */
export type TradeplanV1_Condition = TradeplanV1_PriceCondition | TradeplanV1_PrimitiveCondition;
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_TpExitList".
 */
export type TradeplanV2_TpExitList = {
  leg_id?: TradeplanV2_LegId;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
  condition: TradeplanV2_TpConditionNode;
}[];
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
 * Response to broker.get_catalog. Describes the shape BF's InstrumentRegistry/CatalogStore actually emits today (belphegor/brokers/catalog_store.py CatalogMeta.to_dict() for the meta form, get_catalog_slice() for the slice form) — deliberately permissive (additionalProperties: true throughout, required kept to the minimum AFB reads) since BrokerPort.get_catalog_meta()/get_catalog_slice() impose nothing on a broker plugin's exact dict shape. This is a PATCH-level description of existing wire behavior, not a new constraint on it.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerCatalogPayload".
 */
export type BrokerCatalogPayload = PayloadsBrokerCatalog_Meta | PayloadsBrokerCatalog_Slice;
/**
 * Empty payload requests the meta form (exchanges/markets pairs) of the broker.catalog reply; {exchange,market} together request the slice form (instrument rows) for that market. AFB never sends exchange without market or vice versa (backend/trade/ws_handlers.py::handle_account).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerGetCatalogPayload".
 */
export type BrokerGetCatalogPayload =
  | {
      [k: string]: unknown;
    }
  | {
      exchange: string;
      market: string;
    };

/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountListRequest".
 */
export interface AccountListRequest {
  channel: 'account';
  schema: 'afbws.account.list.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id?: AccountBfId;
  /**
   * Bypass the cached BfRuntimeState.accounts snapshot and re-fetch from BF.
   */
  force?: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountListResponse".
 */
export interface AccountListResponse {
  channel: 'account';
  schema: 'afbws.account.list.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  items: AccountSnapshot[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountSnapshot".
 */
export interface AccountSnapshot {
  bf_id: AccountBfId;
  account_id: AccountAccountId;
  /**
   * True only for this bf_id's default (trading) account.
   */
  tradable: boolean;
  readonly: boolean;
  status: 'ok' | 'stale' | 'error';
  equity: string | null;
  cash: PayloadsBrokerAccounts_CashBalance[];
  positions: PayloadsBrokerAccounts_Position[];
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
 * via the `definition` "PayloadsBrokerAccounts_Position".
 */
export interface PayloadsBrokerAccounts_Position {
  quantity: number;
  average_price: string;
  current_price?: string | null;
  unrealized_pnl?: string | null;
  instrument?: {};
  broker_ref?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountGetRequest".
 */
export interface AccountGetRequest {
  channel: 'account';
  schema: 'afbws.account.get.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: AccountBfId;
  account_id?: AccountAccountId;
  force?: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountGetResponse".
 */
export interface AccountGetResponse {
  channel: 'account';
  schema: 'afbws.account.get.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: AccountSnapshot;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountOrdersRequest".
 */
export interface AccountOrdersRequest {
  channel: 'account';
  schema: 'afbws.account.orders.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: AccountBfId;
  account_id?: AccountAccountId;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountOrdersResponse".
 */
export interface AccountOrdersResponse {
  channel: 'account';
  schema: 'afbws.account.orders.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: AccountBfId;
  account_id: AccountAccountId;
  items: AccountOrder[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountOrder".
 */
export interface AccountOrder {
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
 * via the `definition` "AccountEventsRequest".
 */
export interface AccountEventsRequest {
  channel: 'account';
  schema: 'afbws.account.events.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: AccountBfId;
  /**
   * YYYY-MM-DD market date; omitted means today (market_today()).
   */
  date?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountEventsResponse".
 */
export interface AccountEventsResponse {
  channel: 'account';
  schema: 'afbws.account.events.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: AccountBfId;
  date: string;
  items: AccountEventRecord[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountEventRecord".
 */
export interface AccountEventRecord {
  logged_at: string;
  bf_id: AccountBfId;
  deal_id?: string | null;
  category: 'deal' | 'order' | 'position' | 'condition';
  event: string;
  data?: {} | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountErrorResponse".
 */
export interface AccountErrorResponse {
  channel: 'account';
  schema: 'afbws.account.error.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountSnapshotPush".
 */
export interface AccountSnapshotPush {
  channel: 'account';
  schema: 'afbws.account.snapshot.push.v1';
  bf_id: AccountBfId;
  default_account_id: AccountAccountId;
  items: AccountSnapshot[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountOrdersPush".
 */
export interface AccountOrdersPush {
  channel: 'account';
  schema: 'afbws.account.orders.push.v1';
  bf_id: AccountBfId;
  account_id: AccountAccountId;
  items: AccountOrder[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmGetRequest".
 */
export interface AlarmGetRequest {
  channel: 'alarm';
  schema: 'afbws.alarm.get.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmGetResponse".
 */
export interface AlarmGetResponse {
  channel: 'alarm';
  schema: 'afbws.alarm.get.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: AlarmV1;
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
 * via the `definition` "AlarmListRequest".
 */
export interface AlarmListRequest {
  channel: 'alarm';
  schema: 'afbws.alarm.list.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  ticker?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmListResponse".
 */
export interface AlarmListResponse {
  channel: 'alarm';
  schema: 'afbws.alarm.list.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  items: AlarmV1[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmSetRequest".
 */
export interface AlarmSetRequest {
  channel: 'alarm';
  schema: 'afbws.alarm.set.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: AlarmV1;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmSetResponse".
 */
export interface AlarmSetResponse {
  channel: 'alarm';
  schema: 'afbws.alarm.set.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: AlarmV1;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmDeleteRequest".
 */
export interface AlarmDeleteRequest {
  channel: 'alarm';
  schema: 'afbws.alarm.delete.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmDeleteResponse".
 */
export interface AlarmDeleteResponse {
  channel: 'alarm';
  schema: 'afbws.alarm.delete.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmErrorResponse".
 */
export interface AlarmErrorResponse {
  channel: 'alarm';
  schema: 'afbws.alarm.error.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmTriggeredPush".
 */
export interface AlarmTriggeredPush {
  channel: 'alarm';
  schema: 'afbws.alarm.triggered.push.v1';
  /**
   * @minItems 1
   */
  events: [AlarmTriggerEvent, ...AlarmTriggerEvent[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmTriggerEvent".
 */
export interface AlarmTriggerEvent {
  schema: 'afb.alarm.trigger.v1';
  alarm_id: string;
  triggered_at: string;
  alarm: AlarmV1;
  current_price?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmAckRequest".
 */
export interface AlarmAckRequest {
  channel: 'alarm';
  schema: 'afbws.alarm.ack.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  events: [AlarmAckEvent, ...AlarmAckEvent[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmAckEvent".
 */
export interface AlarmAckEvent {
  schema: 'afb.alarm.trigger_ack.v1';
  alarm_id: string;
  triggered_at: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmAckResponse".
 */
export interface AlarmAckResponse {
  channel: 'alarm';
  schema: 'afbws.alarm.ack.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  results: AlarmAckResultItem[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AlarmAckResultItem".
 */
export interface AlarmAckResultItem {
  schema: 'afbws.alarm.ack_result.v1';
  alarm_id: string;
  triggered_at: string;
  status: 'ok' | 'not_found';
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
 * Shared building blocks for the schema-first afbws channels introduced alongside `deal`/`connector`/`bfs`/`account` (see afbws/README convention in CLAUDE.md): a request/response correlation id and a typed error vocabulary. Unlike the legacy afbws channels (discriminated by a `type` const), schema-first channels are routed by `channel` then by a mandatory top-level `schema` id — no `type` field.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCommonV1_Root".
 */
export interface AfbwsCommonV1_Root {
  [k: string]: unknown;
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
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealGetRequest".
 */
export interface DealGetRequest {
  channel: 'deal';
  schema: 'afbws.deal.get.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  deal_id: DealId;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealGetResponse".
 */
export interface DealGetResponse {
  channel: 'deal';
  schema: 'afbws.deal.get.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: DealDetail;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealDetail".
 */
export interface DealDetail {
  deal_id: DealId;
  revision: number;
  status: string;
  execution_phase: string;
  bf_id: BfId;
  tradeplan_id: string;
  ticker: string;
  market?: 'stock' | 'futures' | 'currency';
  direction: 'long' | 'short';
  sizing?: DealSizing;
  execution_policy?: DealExecutionPolicy;
  broker_sizing?: DealSizingDisplay;
  realized_pnl?: AfbwsDealChannelV1_DealRealizedPnl;
  created_at: string;
  updated_at: string;
  deal: DealPublicV1;
  editable_fields: DealAmendField[];
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
 * via the `definition` "DealSizingDisplay".
 */
export interface DealSizingDisplay {
  lots?: number;
  required_cash?: string;
  /**
   * BF-resolved actual order quantity (lots), fixed once at entry-trigger time — distinct from `lots`, which stays the pre-trade publish estimate. Present only once BF has reported it (deal.status_changed/deal.snapshot `quantity`).
   */
  resolved_lots?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsDealChannelV1_DealRealizedPnl".
 */
export interface AfbwsDealChannelV1_DealRealizedPnl {
  /**
   * Decimal string, rubles. Null exactly when degraded is set — a fill's money multiplier (step_price/price_step or lot_size) couldn't be resolved.
   */
  value: string | null;
  degraded: null | 'missing_price' | 'missing_step_price';
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicDealV1".
 */
export interface DealPublicDealV1 {
  schema: 'afb.deal.v1';
  deal_id: string;
  revision: number;
  target: DealTarget;
  direction: 'long' | 'short';
  entry: DealV1_Entry;
  sizing: DealSizing;
  risk?: {
    take_profit?: DealV1_ExitBlock;
    stop_loss?: DealV1_ExitBlock;
  };
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
   * Broker account this deal is published against. Optional on the wire — absent means BF's own trading account (brokers/port.py::account_id). AFB compiles it from the owning tradeplan's publish.account_id (see tradeplan.v1.json#/properties/publish), resolving empty/absent to the connector's default account before publish (ExecutionService.resolve_plan_account). BF validates it against its own account (plan_engine/plan_validation.py: wrong_account_id) when present.
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
  market?: 'stock' | 'futures' | 'currency';
  price_step?: DecimalString;
  step_price?: DecimalString;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV1_Entry".
 */
export interface DealV1_Entry {
  condition: DealV1_ConditionNode;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV1_ConditionNode".
 */
export interface DealV1_ConditionNode {
  node_type: 'event';
  id?: string;
  op: 'above' | 'below' | 'crosses_above' | 'crosses_below' | 'crossing';
  /**
   * afb.deal.v1 conditions compare against the last traded price, or (entry only — see executor-side validation) fire immediately with no price level of its own. quote/indicator/dataset sources are afb.deal.v2-only.
   */
  left: {
    source: 'price' | 'immediate';
    field?: 'last';
  };
  right: {
    const: DecimalString;
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV1_ExitBlock".
 */
export interface DealV1_ExitBlock {
  condition?: DealV1_ConditionNode;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicSource".
 */
export interface DealPublicSource {
  tradeplan_id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublicDealV2".
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
      leg_id?: TradeplanV2_LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: DealV2_ConditionNode;
      source?: DealV2_LegSource;
    },
    ...{
      leg_id?: TradeplanV2_LegId;
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
 * via the `definition` "DealListRequest".
 */
export interface DealListRequest {
  channel: 'deal';
  schema: 'afbws.deal.list.request.v1';
  request_id: AfbwsCommonV1_RequestId;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealListResponse".
 */
export interface DealListResponse {
  channel: 'deal';
  schema: 'afbws.deal.list.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  items: DealSummary[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealSummary".
 */
export interface DealSummary {
  deal_id: DealId;
  revision: number;
  status: string;
  execution_phase: string;
  bf_id: BfId;
  tradeplan_id: string;
  ticker: string;
  market?: 'stock' | 'futures' | 'currency';
  direction: 'long' | 'short';
  sizing?: DealSizing;
  execution_policy?: DealExecutionPolicy;
  broker_sizing?: DealSizingDisplay;
  realized_pnl?: AfbwsDealChannelV1_DealRealizedPnl;
  created_at: string;
  updated_at: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublishRequest".
 */
export interface DealPublishRequest {
  channel: 'deal';
  schema: 'afbws.deal.publish.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  tradeplan_id: string;
  bf_id: BfId;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPublishResponse".
 */
export interface DealPublishResponse {
  channel: 'deal';
  schema: 'afbws.deal.publish.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  results: DealResult[];
  accepted: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealResult".
 */
export interface DealResult {
  deal_id: DealId;
  bf_id: BfId;
  status: string;
  accepted: boolean;
  revision?: number;
  item?: DealSummary | DealDetail;
  code?: string;
  message?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealRebindRequest".
 */
export interface DealRebindRequest {
  channel: 'deal';
  schema: 'afbws.deal.rebind.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  deal_id: DealId;
  bf_id: BfId;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealRebindResponse".
 */
export interface DealRebindResponse {
  channel: 'deal';
  schema: 'afbws.deal.rebind.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  results: DealResult[];
  accepted: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealOperationRequest".
 */
export interface DealOperationRequest {
  channel: 'deal';
  schema: 'afbws.deal.operation.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  items: [DealOperationItem, ...DealOperationItem[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealOperationResponse".
 */
export interface DealOperationResponse {
  channel: 'deal';
  schema: 'afbws.deal.operation.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  results: DealResult[];
  /**
   * any(result.accepted for result in results)
   */
  accepted: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAmendRequest".
 */
export interface DealAmendRequest {
  channel: 'deal';
  schema: 'afbws.deal.amend.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  deal_id: DealId;
  deal_edit?: DealEdit;
  base_revision?: number;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealEdit".
 */
export interface DealEdit {
  entry?: DealRoleEdit;
  stop_loss?: DealRoleEdit;
  take_profit?: DealRoleEdit;
  sizing?: DealSizing;
  execution_policy?: DealExecutionPolicy;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealRoleEdit".
 */
export interface DealRoleEdit {
  edited?: DealLegEdit[];
  removed_indices?: number[];
  /**
   * Drop this leg's deal-level override (source reverts to tradeplan) — the leg immediately re-adopts whatever the linked plan currently holds for the matching leg_id.
   */
  reset_indices?: number[];
  new_legs?: DealNewLeg[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealLegEdit".
 */
export interface DealLegEdit {
  index: number;
  condition?: DealV2_ConditionNode;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealNewLeg".
 */
export interface DealNewLeg {
  condition: DealV2_ConditionNode;
  percent?: DecimalString;
  logic?: DealV2_LegJoin;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAmendResponse".
 */
export interface DealAmendResponse {
  channel: 'deal';
  schema: 'afbws.deal.amend.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: DealDetail;
  revision: number;
  status: string;
  accepted: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealErrorResponse".
 */
export interface DealErrorResponse {
  channel: 'deal';
  schema: 'afbws.deal.error.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
  item?: DealSummary | DealDetail;
}
/**
 * Authoritative REPLACE of the public deal projection identified by deal_id — the frontend must overwrite its cached copy, never merge partial fields from thin `event` pushes, and never merge-patch this either. `item` is the same public projection as afbws.deal.get.response.v1's item (deal.channel.v1.json#/$defs/dealDetail) — an explicit allow-list built by backend/trade/public_views.py, NOT a serialization of the persisted DealState file (deal_state.v2.json): source_refs, status_history, event_journal, raw orders/positions and observed never appear here.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealRecordPush".
 */
export interface DealRecordPush {
  channel: 'deal';
  schema: 'afbws.deal.record.push.v1';
  deal_id: DealId;
  bf_id: BfId;
  item: DealDetail;
}
/**
 * See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--pnl. Periodic unrealized-P&L push, not persisted. `trend` is deliberately absent — it is a frontend-only projection computed from consecutive pushes, never sent by the backend.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPnlPush".
 */
export interface DealPnlPush {
  channel: 'deal';
  schema: 'afbws.deal.pnl.push.v1';
  deal_id: DealId;
  bf_id: BfId;
  data: {
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
  };
}
/**
 * See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--event. `data` shape depends on category/event — deliberately untyped here, full typing of every BF event payload is out of scope for this migration. Known event/data shapes: `created`/`amended` carry a full deal snapshot (frontend must treat `amended` as an authoritative upsert, same as `created` — previously received but dropped); `status_changed` carries a status delta; BF `deal.archived` arrives to the frontend translated as `status_changed` with `status: "deleted"`; anything else is the raw translated BF envelope payload.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealEventPush".
 */
export interface DealEventPush {
  channel: 'deal';
  schema: 'afbws.deal.event.push.v1';
  deal_id: DealId;
  bf_id: BfId;
  category: 'deal' | 'order' | 'position' | 'condition';
  event: string;
  logged_at: string;
  data: {
    [k: string]: unknown;
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealTriggeredPush".
 */
export interface DealTriggeredPush {
  channel: 'deal';
  schema: 'afbws.deal.triggered.push.v1';
  /**
   * @minItems 1
   */
  events: [DealTriggerEvent, ...DealTriggerEvent[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealTriggerEvent".
 */
export interface DealTriggerEvent {
  schema: 'afb.deal.trigger.v1';
  notification_id: string;
  deal_id: DealId;
  bf_id: BfId;
  event: string;
  created_at: string;
  data: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAckRequest".
 */
export interface DealAckRequest {
  channel: 'deal';
  schema: 'afbws.deal.ack.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * @minItems 1
   */
  events: [DealAckEvent, ...DealAckEvent[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAckEvent".
 */
export interface DealAckEvent {
  schema: 'afb.deal.trigger_ack.v1';
  notification_id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAckResponse".
 */
export interface DealAckResponse {
  channel: 'deal';
  schema: 'afbws.deal.ack.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  results: DealAckResultItem[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealAckResultItem".
 */
export interface DealAckResultItem {
  schema: 'afbws.deal.ack_result.v1';
  notification_id: string;
  status: 'ok' | 'not_found';
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpGetRequest".
 */
export interface GpGetRequest {
  channel: 'gp';
  schema: 'afbws.gp.get.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpGetResponse".
 */
export interface GpGetResponse {
  channel: 'gp';
  schema: 'afbws.gp.get.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: GpV1;
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
 * via the `definition` "GpListRequest".
 */
export interface GpListRequest {
  channel: 'gp';
  schema: 'afbws.gp.list.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  ticker?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpListResponse".
 */
export interface GpListResponse {
  channel: 'gp';
  schema: 'afbws.gp.list.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  items: GpV1[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpSetRequest".
 */
export interface GpSetRequest {
  channel: 'gp';
  schema: 'afbws.gp.set.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: GpV1;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpSetResponse".
 */
export interface GpSetResponse {
  channel: 'gp';
  schema: 'afbws.gp.set.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: GpV1;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpDeleteRequest".
 */
export interface GpDeleteRequest {
  channel: 'gp';
  schema: 'afbws.gp.delete.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpDeleteResponse".
 */
export interface GpDeleteResponse {
  channel: 'gp';
  schema: 'afbws.gp.delete.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * items[] — upsert by id (bind: tradeplan_id set on publish/amend; release: tradeplan_id cleared on plan physical delete), full authoritative afb.gp.v1 record, same shape as set.response. Never a snapshot. Primitive deletion (archival freeze) is NOT conveyed by this push — a dropped primitive was, by construction, bound to a plan and only rendered while that plan is selected; the plan's own afbws.tradeplan.sync.push.v1 (status: archived, frozen numeric conditions) already replaces its on-chart representation.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsGpChannelV1_SyncPush".
 */
export interface AfbwsGpChannelV1_SyncPush {
  channel: 'gp';
  schema: 'afbws.gp.sync.push.v1';
  /**
   * @minItems 1
   */
  items: [GpV1, ...GpV1[]];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpErrorResponse".
 */
export interface GpErrorResponse {
  channel: 'gp';
  schema: 'afbws.gp.error.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  item?: GpV1;
  details?: GpErrorDetails;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "GpErrorDetails".
 */
export interface GpErrorDetails {
  tradeplan_ids?: string[];
  deal_ids?: string[];
  locked_scopes?: ('entry' | 'stop_loss' | 'take_profit')[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentGetRequest".
 */
export interface InstrumentGetRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.get.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  ticker: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentGetResponse".
 */
export interface InstrumentGetResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.get.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: InstrumentV1;
}
/**
 * Replaces the former meta/slice pair. `entries` is a mixed listing|series page. `total` is the match count AFTER `query`/`kind`/`market` filters and BEFORE paging (`entries.length` ≤ `limit`, never a substitute for `total`). `next_cursor` is bound to the same filter tuple and to the snapshot identified by `fetched_at`; null means this page is the last. `fetched_at` is when the backend snapshot was taken, not when this page was built.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentPoolResponse".
 */
export interface InstrumentPoolResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.pool.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  source: 'moex';
  /**
   * When the backend MOEX snapshot was fetched, ISO-8601 UTC.
   */
  fetched_at: string;
  /**
   * Count of matches after `query`/`kind`/`market` filters and before paging. Independent of `limit` and of `entries.length`.
   */
  total: number;
  /**
   * Opaque cursor for the next page of THIS filter against the snapshot in `fetched_at`; null when this page is the last. Echo it back only with the same `query`/`kind`/`market`.
   */
  next_cursor: string | null;
  entries: InstrumentPoolEntry[];
}
/**
 * Maps to seriesUpsert on commit: `code` → `series_code`, `underlying` → `underlying_ticker`. The backend materializes active contracts from the MOEX snapshot in the same commit that upserts the series.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentPoolSeriesEntry".
 */
export interface InstrumentPoolSeriesEntry {
  kind: 'series';
  /**
   * series_code. Maps to seriesUpsert.series_code on commit.
   */
  code: string;
  name: string | null;
  source: 'moex';
  market: 'futures';
  /**
   * Underlying ticker when the series has one. Maps to seriesUpsert.underlying_ticker on commit.
   */
  underlying?: string | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentResolveRequest".
 */
export interface InstrumentResolveRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.resolve.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: string;
  tradeplan_id?: string;
  draft?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentResolveResponse".
 */
export interface InstrumentResolveResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.resolve.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: InstrumentV1;
  /**
   * Broker-native locator, BF-owned shape — see broker.instrument_resolved.json.
   */
  binding: {
    [k: string]: unknown;
  };
  /**
   * Broker-owned trading params, BF-owned shape.
   */
  broker_instrument: {
    [k: string]: unknown;
  };
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentDetailRequest".
 */
export interface InstrumentDetailRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.detail.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  bf_id: string;
  /**
   * Canonical ticker of an item already present in the curated catalog (see instrument/get) — not an arbitrary broker-native symbol.
   */
  ticker: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentDetailResponse".
 */
export interface InstrumentDetailResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.detail.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: InstrumentV1;
  /**
   * Broker-native locator, BF-owned shape — see broker.instrument_resolved.json.
   */
  binding: {
    [k: string]: unknown;
  };
  /**
   * Broker-owned trading params, BF-owned shape (InstrumentInfo.to_broker_instrument_dict() — the same deal-publish-shared shape resolveResponse carries, not the narrower broker.instrument.json allow-list; e.g. it has no `symbol` key, that lives in `binding` instead).
   */
  broker_instrument: {
    [k: string]: unknown;
  };
}
/**
 * The wire form is identical for a user and a manager; completeness (unassigned assets) is applied server-side from the caller's role — sets/assets no longer carry an archived flag, so the only completeness axis left is whether an asset belongs to any set. `catalog` is the Assets-modal snapshot and the only read of the curated catalog.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCatalogRequest".
 */
export interface InstrumentCatalogRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.catalog.request.v1';
  request_id: AfbwsCommonV1_RequestId;
}
/**
 * Same form for every authenticated caller; the backend varies completeness (a manager sees unassigned assets too, a user sees only live sets and the assets that belong to them — sets/assets have no archived flag, so this is purely about assets that are in no set). Membership is `asset_sets[].asset_ids` in display order. Composition is `assets[].members` (`kind`/`code`/`label`/`market`) in display order. Order is always array position — no entity on this wire carries an order field. `items` are the canonical instrument records (including materialized futures contracts); `series` is the futures-series axis. `catalog_revision` is the CAS token to send back as commitRequest.base_revision. The `group` field inside `items[]` is a legacy leftover and must not be read as membership. Dangling levels are normal: an asset in no set stays in `assets` (manager) and is absent from every `asset_sets[].asset_ids`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCatalogResponse".
 */
export interface InstrumentCatalogResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.catalog.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * Revision of the global catalog this snapshot was taken at — send it back as commitRequest.base_revision.
   */
  catalog_revision: number;
  /**
   * Curated assets, each with nested `members` in display order.
   */
  assets: InstrumentCatalogAsset[];
  items: InstrumentV1[];
  series: InstrumentCatalogSeriesMap;
  collections?: InstrumentCollection[];
  asset_sets?: InstrumentAssetSetView[];
  suggestions?: InstrumentAssetSuggestion[];
  user?: InstrumentUserState;
}
/**
 * An asset is a small bundle of instruments that share a pricing source and therefore tell one economic story: "Brent oil" is the BR-* and BRM-* series together, "Sberbank" is the share plus its futures series. Two jobs justify the level. It is the unit sets are built from, so a set survives expirations without being re-edited; and it is the carrier of reference data (MOEX positions, HHI), so analytics have one place to attach to instead of guessing which contract of which series to read. Assets are always global — the personal sets of phase 3 are assembled from the same manager-curated assets, which is what keeps that phase thin. An asset that is in no set is a normal state: it shows up as unassigned for a manager and is omitted from a user's catalog snapshot. Composition is nested as ordered `members` on the asset itself; array position is the order.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCatalogAsset".
 */
export interface InstrumentCatalogAsset {
  /**
   * Opaque id, minted by the client on create and never rewritten by the server — the only handle set membership, members and edits refer to.
   */
  asset_id: string;
  name: string;
  /**
   * Which of the asset's series reference data is taken from when it holds more than one; null when the asset has no series or the manager has not chosen. It points at a series, not at a contract — the MOEX analytics code itself stays on the series and is not duplicated here.
   */
  reference_series_code?: string | null;
  /**
   * Full composition in display order. Array position is the order. Send `[]` for an empty asset.
   */
  members: InstrumentCatalogAssetMember[];
  /**
   * The collection this asset lives in — an asset belongs to exactly one. Optional in schema; required in backend responses after catalog v6. Position inside the collection is carried by the order of `assets[]`: the assets of one collection come consecutively, and the collections themselves follow the order of `collections[]`.
   */
  collection_id?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCatalogSeriesMap".
 */
export interface InstrumentCatalogSeriesMap {
  [k: string]: InstrumentCatalogSeries;
}
/**
 * An axis of its own, independent of sets: it groups the successive expirations of one futures contract and is unaffected by set membership. Carries no order: `series` is a JSON object (catalogSeriesMap), and the order of an object's members is not semantic. Should the series axis ever need an order, the right move is to turn `series` into an array — not to bring an order field back.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCatalogSeries".
 */
export interface InstrumentCatalogSeries {
  name: string | null;
  /**
   * Canonical ticker of the underlying instrument, when the series has one.
   */
  underlying_ticker?: string | null;
}
/**
 * Order is carried by array position: `collections[]` already arrives in the order the tree is drawn in (the children of one `parent_id` follow one another), so there is no order field on the wire. A commit restates that order wholesale through `commitRequest.collection_order`.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCollection".
 */
export interface InstrumentCollection {
  collection_id: string;
  parent_id?: string | null;
  name: string;
  /**
   * system_pending / _unclassified bucket.
   */
  pending?: boolean;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentAssetSuggestion".
 */
export interface InstrumentAssetSuggestion {
  suggestion_id: string;
  subject_type: 'listing' | 'series';
  subject_ref: string;
  reason: string;
  status: 'pending' | 'accepted' | 'rejected' | 'stale';
  proposed_name?: string;
  proposed_collection_id?: string | null;
  fingerprint?: string;
  created_at?: string;
  last_seen_at?: string;
  resolved_asset_id?: string;
}
/**
 * The caller's personal overlay, served next to the global catalog. `sets[]` are full assetSetView objects — every entry has scope "user" and carries its own membership inline as ordered `asset_ids`; there is no parallel membership array. Personal sets are assembled from the same global assets a manager curates: a user never owns an asset of their own.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentUserState".
 */
export interface InstrumentUserState {
  /**
   * Revision of the PERSONAL aggregate — counted separately from catalog_revision.
   */
  revision: number;
  /**
   * The caller's own sets — every entry has scope: "user" and states its membership inline as ordered `asset_ids`. Set order is the order of this array.
   */
  sets: InstrumentAssetSetView[];
  /**
   * Sets (global or personal) the caller hid from their own view.
   */
  hidden_set_ids: string[];
  /**
   * Personal ordering of set_ids; sets not listed here follow the listed ones in the server's order.
   */
  order: string[];
}
/**
 * Compare-and-set: if the server's current catalog revision differs from `base_revision` the whole commit is rejected with `conflict` and errorResponse.details.catalog_revision carries the current one — the client re-fetches `catalog`, re-applies its edits and retries. Every section is optional; an empty commit is legal (and is a cheap way to read the current revision back). All sections are applied in one transaction, in this order: `asset_sets`, `remove_asset_sets`, `assets`, `remove_assets`, `asset_set_members`, `listings`/`archive_listings`, `series`, `collections`, `remove_collections`, `collection_members`. The server plans the whole delta before applying, so a listing or series upserted in this same request may be referenced from `assets[].members` even though those sections are written later — that is how a pending pool entry and the asset composition that contains it travel atomically. A set created here can be filled by `asset_set_members` in the same request, and an asset created here can be put into that set, because both exist by the time `asset_set_members` runs — `asset_set_members`/other same-commit references use the same client-minted `set_id`/`asset_id` the `assetSetUpsert`/`assetUpsert` entry carries. Order is never a field on an entity: `asset_set_order`, `collection_order`, and the `order` of `asset_set_members`/`collection_members` each state a FULL final order, and every read snapshot carries order as array position. `set_id` and `asset_id` are always client-minted opaque ids (assetSetUpsert/assetUpsert), never generated by the server: a `set_id`/`asset_id` absent from the base snapshot is an INSERT, one already present is an UPDATE, and the server never rewrites an id it is given.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCommitRequest".
 */
export interface InstrumentCommitRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.commit.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * The catalog_revision these edits were built on (CAS guard).
   */
  base_revision: number;
  assets?: InstrumentAssetUpsert[];
  /**
   * asset_ids to delete outright. The deletion takes the asset's set memberships and its composition edges with it, but touches neither the listings nor the series that were its members — they survive uncurated and reappear as unassigned. There is no archive flag for assets.
   */
  remove_assets?: string[];
  /**
   * Upsert of the instrument records themselves, by `ticker`. Copy a pool listing entry's `listing` here unchanged. The element's `group` field is IGNORED — membership is expressed only through `asset_set_members`; clients send `group: null`. instrument.v1 is reused verbatim for its class gating (futures-only expiration/step_price/margin/futoi_code, `isin` for stock only), which is exactly what a listing write has to enforce.
   */
  listings?: InstrumentV1[];
  archive_listings?: InstrumentListingArchival[];
  /**
   * Upsert of futures series. Copy a pending pool series row here (`code` → `series_code`, `underlying` → `underlying_ticker`). The backend materializes that series' active contracts from the MOEX snapshot in the same transaction.
   */
  series?: InstrumentSeriesUpsert[];
  collections?: InstrumentCollectionUpsert[];
  /**
   * collection_ids to delete outright. The assets that were in them are not deleted — they land in the system `_unclassified` bucket.
   */
  remove_collections?: string[];
  /**
   * The FULL final order of collection_ids — not a partial reshuffle. The list is FLAT: a collection carries one global order key in storage, not a position inside its parent, so parents and children are ordered in the same sequence. Collections absent from the list keep their relative position after the listed ones.
   */
  collection_order?: string[];
  /**
   * Which assets belong to which collection, and in what order inside it. An asset belongs to exactly one collection, so an `add` here also moves it out of its previous one.
   */
  collection_members?: InstrumentCollectionMembersEdit[];
  /**
   * Asset sets to create or update — identity and name only; the order of the sets is `asset_set_order`.
   */
  asset_sets?: InstrumentAssetSetUpsert[];
  /**
   * set_ids to delete outright (their membership goes with them). There is no archive flag — a hidden-but-addressable set is a userState.hidden_set_ids concern, not a catalog one.
   */
  remove_asset_sets?: string[];
  /**
   * Membership delta of the asset sets, in asset_ids, with the full resulting order per set.
   */
  asset_set_members?: InstrumentMembersEdit[];
  /**
   * The FULL final order of set_ids — not a partial reshuffle. Sets absent from the list keep their relative position after the listed ones.
   */
  asset_set_order?: string[];
  accept_suggestions?: InstrumentAcceptSuggestion[];
  reject_suggestions?: string[];
  /**
   * Operator's note for this commit — stored verbatim in catalog_audit.reason.
   */
  reason?: string;
}
/**
 * The client mints `asset_id` itself (same generateId style as deal/primitive ids; for a non-empty asset the first block is the code of its first `members[]` entry). Scalars otherwise behave as a patch — an omitted field keeps its stored value — while `members`, when present, is the WHOLE composition in its final order, exactly like membersEdit.order. Composition has no add/remove form on purpose: an asset holds a handful of members that a manager edits as one picture, and a full statement removes any question about what an absent element means. Omit `members` to leave the composition untouched; send `[]` to empty the asset without deleting it.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentAssetUpsert".
 */
export interface InstrumentAssetUpsert {
  /**
   * Client-minted opaque id. Unknown in the current snapshot -> INSERT (create); known -> UPDATE.
   */
  asset_id: string;
  name: string;
  /**
   * Series reference data is taken from; null clears the choice.
   */
  reference_series_code?: string | null;
  /**
   * The FULL composition of the asset, in the order it should end up in — not a partial edit. Each element is `{kind, code}` (same identity as catalogAssetMember / a pool entry). A contract listed here whose series is also listed is rejected.
   */
  members?: InstrumentAssetMemberInput[];
  /**
   * The collection this asset moves into. Position inside that collection is not stated here — send `commitRequest.collection_members` to fix it.
   */
  collection_id?: string;
}
/**
 * Same discriminator and identity as catalogAssetMember (`kind`+`code`). `label` and `market` are snapshot-only and are not written — the server derives them from items/series. A contract listed here whose series is also listed is rejected.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentAssetMemberInput".
 */
export interface InstrumentAssetMemberInput {
  kind: 'listing' | 'series';
  /**
   * Canonical ticker for `listing`, series_code for `series` — case-sensitive, never normalized.
   */
  code: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentListingArchival".
 */
export interface InstrumentListingArchival {
  ticker: string;
  /**
   * Free-form note stored with the audit entry (e.g. "expired", "delisted").
   */
  reason?: string;
}
/**
 * Write form for a pool series row: copy `code` → `series_code`, `name` → `name`, `underlying` → `underlying_ticker`. The series axis carries no order — `series` is a map, not a list.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentSeriesUpsert".
 */
export interface InstrumentSeriesUpsert {
  series_code: string;
  name?: string | null;
  underlying_ticker?: string | null;
}
/**
 * Identity and naming only — position is not stated here; send `commitRequest.collection_order` to fix the order of the tree.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCollectionUpsert".
 */
export interface InstrumentCollectionUpsert {
  collection_id: string;
  parent_id?: string | null;
  name: string;
}
/**
 * An asset lives in exactly ONE collection, so `add` here also states membership: an asset added to a collection leaves the one it was in. Assets that fall out of a collection without being added to another land in the system `_unclassified` bucket. `order`, when present, must list the collection's full membership after add/remove.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCollectionMembersEdit".
 */
export interface InstrumentCollectionMembersEdit {
  collection_id: string;
  /**
   * asset_ids to put into this collection; adding an already-present asset is a no-op, not an error.
   */
  add?: string[];
  /**
   * asset_ids to drop from this collection — an asset that ends up in no collection is not deleted, it lands in the system `_unclassified` bucket.
   */
  remove?: string[];
  /**
   * The FULL asset_id order of this collection after add/remove — not a partial reshuffle.
   */
  order?: string[];
}
/**
 * Server derives scope/owner — client sends only set_id, name and an optional visibility_tier (default on server: user). Position is not stated here; send `commitRequest.asset_set_order` to fix the order of the sets.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentAssetSetUpsert".
 */
export interface InstrumentAssetSetUpsert {
  set_id: string;
  name: string;
  /**
   * Optional; server default is user.
   */
  visibility_tier?: 'manager' | 'user' | 'guest';
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentMembersEdit".
 */
export interface InstrumentMembersEdit {
  set_id: string;
  /**
   * asset_ids to add; adding an already-present asset is a no-op, not an error.
   */
  add?: string[];
  /**
   * asset_ids to drop from this set — an asset that ends up in no set is not deleted, it becomes unassigned.
   */
  remove?: string[];
  /**
   * The FULL asset_id order of this set after add/remove — not a partial reshuffle.
   */
  order?: string[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentAcceptSuggestion".
 */
export interface InstrumentAcceptSuggestion {
  suggestion_id: string;
  asset_id: string;
  collection_id?: string;
}
/**
 * `catalog_revision` is already the new one. A rejected commit is an errorResponse instead — there is no partially-applied outcome.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCommitResponse".
 */
export interface InstrumentCommitResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.commit.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  catalog_revision: number;
  assets: InstrumentCatalogAsset[];
  items: InstrumentV1[];
  series: InstrumentCatalogSeriesMap;
  collections?: InstrumentCollection[];
  asset_sets?: InstrumentAssetSetView[];
  suggestions?: InstrumentAssetSuggestion[];
  applied?: {
    [k: string]: number;
  };
  user?: InstrumentUserState;
}
/**
 * `base_revision` here is the revision of the PERSONAL aggregate (userState.revision), not the global catalog_revision — personal edits never conflict with a manager's commit. Sets created through this operation are implicitly scope: "user" and owned by the caller; a `set_id` naming a global set is rejected. An empty request is legal and just reads the current personal state back.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentUserRequest".
 */
export interface InstrumentUserRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.user.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * userState.revision the edits were built on (CAS guard); a mismatch is `conflict` with details.user_revision.
   */
  base_revision: number;
  /**
   * Personal sets to create or update — scope is implied, never sent. `visibility_tier` is FORBIDDEN in this operation and is rejected with `validation_error`: a personal set has scope `user`, and the tier is meaningful only for global sets.
   */
  sets?: InstrumentAssetSetUpsert[];
  /**
   * Personal set_ids to delete.
   */
  remove_asset_sets?: string[];
  asset_set_members?: InstrumentMembersEdit[];
  /**
   * Replaces the whole hidden list, not a delta.
   */
  hidden_set_ids?: string[];
  /**
   * Replaces the whole personal ordering, not a delta.
   */
  order?: string[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentUserResponse".
 */
export interface InstrumentUserResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.user.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * The new personal revision — same value as user.revision, hoisted for symmetry with catalog_revision.
   */
  user_revision: number;
  user: InstrumentUserState;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentSourcesRequest".
 */
export interface InstrumentSourcesRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.sources.request.v1';
  request_id: AfbwsCommonV1_RequestId;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentSourcesResponse".
 */
export interface InstrumentSourcesResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.sources.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  sources: InstrumentCatalogSource[];
}
/**
 * The registry is assembled, not stored: the MOEX/ISS entry comes from the market-source configuration, broker entries from the connectors currently registered. An unavailable source is still listed — the point of the operation is to show WHY nothing is updating (ISS unreachable, connector offline) rather than to hide the row.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentCatalogSource".
 */
export interface InstrumentCatalogSource {
  /**
   * Handle to pass to refreshRequest — "moex" for the ISS feed, a bf_id for a connector's own catalog. Pool browsing in this revision only accepts source "moex"; refresh may still list broker rows as unavailable/unsupported.
   */
  source_id: string;
  /**
   * What kind of feed this is, so a client can label and group sources without parsing source_id.
   */
  kind: 'moex' | 'broker';
  /**
   * Whether a refresh could run right now — the feed is configured and reachable for `moex`, the connector is online for `broker`.
   */
  available: boolean;
  /**
   * When this source last wrote the catalog, ISO-8601 UTC, taken from the catalog audit; null if it never has. This is also what the "already refreshed today" gate reads.
   */
  last_refresh_at: string | null;
  /**
   * How many catalogued listings currently name this source as the owner of their trading params — the size of what a refresh from here would touch, not the size of the source's own universe.
   */
  listing_count: number;
  inventory_count?: number;
  last_error?: string;
  inventory_revision?: number;
}
/**
 * `dry_run` exists because the planning step is already separate from the write: a preview runs the very same planner and returns the very same report, it just never commits. That is the only difference between the two modes — a manager can always look before archiving a few dozen expired contracts.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentRefreshRequest".
 */
export interface InstrumentRefreshRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.refresh.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * A source_id from sourcesResponse; an unknown or unavailable one is a typed error, not a silent no-op.
   */
  source_id: string;
  /**
   * true — plan and report only, the catalog is not written and its revision does not move.
   */
  dry_run?: boolean;
}
/**
 * A refresh that could not run at all (unknown or offline source, stale catalog under a concurrent commit) is an errorResponse instead — a report always describes a plan that was built successfully.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentRefreshResponse".
 */
export interface InstrumentRefreshResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.refresh.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  source_id: string;
  /**
   * Echo of the request's mode — always present here, unlike in the request where it defaults.
   */
  dry_run: boolean;
  report: InstrumentRefreshReport;
}
/**
 * Lists rather than counts, because the interesting cases are individually reviewable: which contracts got archived, which rows the source offered that the catalog does not carry. Every element is a catalog instrument key in its composite form (`MIC:BOARD:TICKER`) — the wire `ticker` of instrument.v1 collapses to the bare local symbol for MOEX and could not tell two boards apart, and a report is precisely where that ambiguity is unacceptable. `new_series` holds series_codes instead. The three trailing lists are diagnostics, not changes: they say what the refresh deliberately did NOT do.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentRefreshReport".
 */
export interface InstrumentRefreshReport {
  /**
   * Whether the catalog was actually written. false both for a dry run and for a run that found nothing to change — in either case revision_after equals revision_before.
   */
  applied: boolean;
  /**
   * Catalog revision the plan was built on.
   */
  revision_before: number;
  /**
   * Revision after the commit; equal to revision_before when nothing was applied.
   */
  revision_after: number;
  /**
   * Listings created by this refresh — only futures contracts get born this way.
   */
  added: string[];
  /**
   * Existing listings whose source-owned fields changed; lifecycle, membership and provenance are never touched by a refresh.
   */
  updated: string[];
  /**
   * Archived listings the source offered again, so they were un-archived instead of duplicated.
   */
  resurrected: string[];
  archived: InstrumentRefreshArchivedEntry[];
  /**
   * series_codes first seen in this answer. Each one gets a series and an asset of its own, outside every set — the manager decides where it belongs.
   */
  new_series: string[];
  /**
   * Rows the source listed that the catalog does not hold and did NOT add: the catalog is curated, and `commit` is where non-futures rows are born. A curation gap shows up here rather than silently growing the catalog.
   */
  absent_from_catalog: string[];
  /**
   * Futures rows the source gave with no series code — unplaceable, so skipped.
   */
  rows_without_series: string[];
  changes?: {
    [k: string]: number;
  };
  suggestion_ids?: string[];
  inventory_revision_before?: number;
  inventory_revision_after?: number;
}
/**
 * Archival is the part of a refresh that a manager cannot undo by re-running it, so the reason travels with the key instead of being left in the server log.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentRefreshArchivedEntry".
 */
export interface InstrumentRefreshArchivedEntry {
  key: string;
  /**
   * Why it was archived — e.g. expired, or absent from the source's answer.
   */
  reason: string;
}
/**
 * Filterable, paged browse of the complete MOEX (or other source) instrument universe — distinct from the curated `pool` candidate list. `limit` defaults to 50, capped at 200.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentInventoryRequest".
 */
export interface InstrumentInventoryRequest {
  channel: 'instrument';
  schema: 'afbws.instrument.inventory.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  source?: string;
  market?: 'stock' | 'futures' | 'currency' | 'index';
  board?: string;
  instrument_type?: 'stock' | 'currency' | 'index' | 'futures' | 'series';
  query?: string;
  limit?: number;
  cursor?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentInventoryResponse".
 */
export interface InstrumentInventoryResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.inventory.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  total: number;
  next_cursor: string | null;
  inventory_revision: number;
  entries: InstrumentInventoryEntry[];
  source?: string;
  fetched_at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentInventorySeriesEntry".
 */
export interface InstrumentInventorySeriesEntry {
  kind: 'series';
  instrument_type: 'series';
  series_code: string;
  source: string;
  market: 'futures';
  name?: string | null;
  underlying?: string | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentErrorResponse".
 */
export interface InstrumentErrorResponse {
  channel: 'instrument';
  schema: 'afbws.instrument.error.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: InstrumentErrorDetails;
}
/**
 * Populated on `conflict` (stale base_revision: `catalog_revision` for commit, `user_revision` for user — re-fetch, re-apply, retry) and on `validation_error` (`set_ids`/`asset_ids`/`tickers` name the offending rows — one list per level, since a rejected edit can be about a set, an asset or a listing). Absent for errors that carry no such context.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "InstrumentErrorDetails".
 */
export interface InstrumentErrorDetails {
  /**
   * The server's current global catalog revision.
   */
  catalog_revision?: number;
  /**
   * The caller's current personal-aggregate revision.
   */
  user_revision?: number;
  set_ids?: string[];
  asset_ids?: string[];
  tickers?: string[];
  collection_ids?: string[];
  suggestion_ids?: string[];
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
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkGetRequest".
 */
export interface LinkGetRequest {
  channel: 'link';
  schema: 'afbws.link.get.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkGetResponse".
 */
export interface LinkGetResponse {
  channel: 'link';
  schema: 'afbws.link.get.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: LinkEntity;
}
/**
 * scope omitted or "usable": enabled connectors the caller may trade on (allowed_users ACL) plus virtual when permitted — never a manager bypass. scope "admin": full registry as admin views; managers only (backend rejects otherwise). Side-effect status.sync.push after list.response uses the same scope.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkListRequest".
 */
export interface LinkListRequest {
  channel: 'link';
  schema: 'afbws.link.list.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  /**
   * usable (default): working accounts for widgets. admin: ConnectorsModal inventory for managers.
   */
  scope?: 'usable' | 'admin';
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkListResponse".
 */
export interface LinkListResponse {
  channel: 'link';
  schema: 'afbws.link.list.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  items: LinkEntity[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkSetRequest".
 */
export interface LinkSetRequest {
  channel: 'link';
  schema: 'afbws.link.set.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: LinkSetInput;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkSetResponse".
 */
export interface LinkSetResponse {
  channel: 'link';
  schema: 'afbws.link.set.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: LinkEntity;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkDeleteRequest".
 */
export interface LinkDeleteRequest {
  channel: 'link';
  schema: 'afbws.link.delete.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkDeleteResponse".
 */
export interface LinkDeleteResponse {
  channel: 'link';
  schema: 'afbws.link.delete.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkPairRequest".
 */
export interface LinkPairRequest {
  channel: 'link';
  schema: 'afbws.link.pair.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkPairResponse".
 */
export interface LinkPairResponse {
  channel: 'link';
  schema: 'afbws.link.pair.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: LinkEntity;
  pairing_string: string;
  expires_at: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkRestartRequest".
 */
export interface LinkRestartRequest {
  channel: 'link';
  schema: 'afbws.link.restart.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkRestartResponse".
 */
export interface LinkRestartResponse {
  channel: 'link';
  schema: 'afbws.link.restart.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * `code` is an open string, not an enum — at least not_found/forbidden/validation_error/conflict/bf_offline/not_paired/unsupported_action (see AFB/docs/ENTITY_WS_PROTOCOL.md) plus the generic invalid_schema/invalid_channel/internal_error every afbws error response can carry, but nothing here enforces that set at the schema level.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkErrorResponse".
 */
export interface LinkErrorResponse {
  channel: 'link';
  schema: 'afbws.link.error.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: string;
  message: string;
  details?: {};
  item?: LinkEntity;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkSyncPush".
 */
export interface LinkSyncPush {
  channel: 'link';
  schema: 'afbws.link.sync.push.v1';
  items: LinkEntity[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkStatusSyncPush".
 */
export interface LinkStatusSyncPush {
  channel: 'link';
  schema: 'afbws.link.status.sync.push.v1';
  items: LinkStatusV1[];
}
/**
 * Runtime-only BF status — never carries name/broker/ACL/keys/policy/config overrides, see link.user.v1.json/link.admin.v1.json for that. Sourced from BF register/unregister, daemon.capabilities, daemon.status and session.heartbeat handling in AFB — `updated_at` mirrors the triggering envelope's `created_at`. `daemon` is null until the first daemon.status after connect; `session` is null whenever `connected` is false (disconnect resets both). Heartbeat fields are AFB-derived display/runtime metadata, not part of the afb.execution.v1 wire itself.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkStatusV1".
 */
export interface LinkStatusV1 {
  schema: 'afbws.link.status.v1';
  bf_id: string;
  connected: boolean;
  updated_at: string;
  /**
   * ISO timestamp of the last verified session.heartbeat observed by AFB for this BF; null when disconnected or before the first heartbeat.
   */
  last_heartbeat_at?: null | string;
  /**
   * Negotiated at session.hello/hello_ack; used for stale detection (3× interval) and UI display.
   */
  heartbeat_interval_sec?: number;
  /**
   * AFB-derived stale flag for the last heartbeat observation, carried to the frontend for consistent badge/tooltip rendering.
   */
  heartbeat_stale?: boolean;
  daemon: null | DaemonStatusPayload;
  session: null | LinkSession;
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
 * via the `definition` "LinkSession".
 */
export interface LinkSession {
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
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "LinkStatusPush".
 */
export interface LinkStatusPush {
  channel: 'link';
  schema: 'afbws.link.status.push.v1';
  item: LinkStatusV1;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanGetRequest".
 */
export interface TradeplanGetRequest {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.get.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanGetResponse".
 */
export interface TradeplanGetResponse {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.get.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: TradeplanEntity;
}
/**
 * AFB-side single-entry / single-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v1. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `schema` is optional: its absence means afb.tradeplan.v1 (compatibility with frontends older than the tradeplan schema itself).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradePlanV1".
 */
export interface TradePlanV1 {
  id: string;
  ticker: string;
  status?: 'draft' | 'published' | 'completed' | 'archived';
  direction?: 'long' | 'short';
  schema?: 'afb.tradeplan.v1';
  activated_at?: string;
  closed_at?: string;
  archived_at?: string;
  /**
   * Only for outgoing messages: the plan's ticker is not found in the securities catalog. Not persisted — overlaid in plans_for_ws_response on read. Not a lifecycle state.
   */
  instrument_missing?: boolean;
  entry_condition: TradeplanV1_EntryCondition;
  quantity_value?: number | null;
  quantity_mode?: 'lots' | 'margin' | 'balance_pct' | 'risk_currency' | 'risk_factor';
  take_profit?: TradeplanV1_Condition | null;
  stop_loss?: TradeplanV1_Condition | null;
  /**
   * Параметры публикации плана (используется ТОЛЬКО при публикации, не хранит связь с сделкой). bf_id — коннектор по умолчанию для UI; истина при публикации — bf_id из afbws.deal.publish.request.v1. account_id пусто/отсутствует — дефолтный (торговый) счёт коннектора, резолвится на лету (ExecutionService.resolve_plan_account).
   */
  publish?: {
    bf_id?: string;
    account_id?: string;
  };
  /**
   * AFB mail/deals read watermark: notifications with created_at <= delivery_at are treated as read on reconnect.
   */
  delivery_at?: string;
  created_at?: string;
  updated_at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV1_MarketOrPriceCondition".
 */
export interface TradeplanV1_MarketOrPriceCondition {
  condition_type?: 'price';
  price_value?: number | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV1_PrimitiveCondition".
 */
export interface TradeplanV1_PrimitiveCondition {
  condition_type: 'primitive';
  primitive_id: string;
  price_value?: number | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV1_PriceCondition".
 */
export interface TradeplanV1_PriceCondition {
  condition_type?: 'price';
  price_value: number;
}
/**
 * AFB-side multi-entry / multi-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v2. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `direction` (long/short) is the single source of truth for position bias, at plan level — entry legs do not carry a per-leg side (a list of entries with independent buy/sell sides has no defined execution semantics for one deal). Conditions are deal.v2-compatible nodes — price legs carry an explicit `op` (touch/above/below/breakout/breakdown/crossing), `op` omitted on a price leg means touch (accepted for back-compat with old plans); indicator legs may omit `op`, derived from direction/scope at compile time — with two extensions beyond condition.v1.json's plain vocabulary: (1) the `right` side of a condition may be a `primitiveRef` (`{"primitive_id": "..."}`), a reference to a chart line primitive that AFB resolves to a decimal `const` at compile time; (2) an entry leg's `left` may be `condition.v1.json#/$defs/immediateExpr` (`{"source": "immediate"}`) for a market entry — `right`/`op` are structural placeholders in that case, same convention as the compiled deal (see deal.v2.json's conditionNode, immediate branch of condition.v1.json#/$defs/conditionNode): dispatch on `left.source == "immediate"` alone, never read `right`/`op`. Meaningful only on entries — AFB/BF reject it on stop_loss/take_profit. The full left/right pairing matrix (price/quote const-only, indicator/dataset const-or-same-kind) is enforced after compilation by deal.v2.json and by BF, not here — this schema deliberately stays loose to accommodate primitiveRef and immediateExpr. Each leg additionally carries an optional `logic` (`split`/`and`/`or`, see deal.v2.json#/$defs/legJoin for the full grammar) joining it to the preceding leg; AFB carries the field through compilation unchanged onto the corresponding deal.v2 leg.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradePlanV2".
 */
export interface TradePlanV2 {
  id: string;
  ticker: string;
  status?: 'draft' | 'published' | 'completed' | 'archived';
  /**
   * AFB frontend hint only — which of the two editor modes owns this plan. Never crosses the AFB<->BF channel and is dropped at compile time (not copied into the deal). Absence means "advanced": a plan written by a frontend older than this field, or by any non-UI producer, opens in the advanced editor. `simple` additionally asserts the plan is expressible in the simple editor (single leg per role, price/market conditions with above/below, no timeframe/percent/logic) — a `simple` plan that violates this is opened in the advanced editor anyway (see AFB frontend/src/utils/planEditorMode.ts).
   */
  editor?: 'simple' | 'advanced';
  direction: 'long' | 'short';
  schema: 'afb.tradeplan.v2';
  activated_at?: string;
  closed_at?: string;
  archived_at?: string;
  /**
   * Only for outgoing messages: the plan's ticker is not found in the securities catalog. Not persisted — overlaid in plans_for_ws_response on read. Not a lifecycle state.
   */
  instrument_missing?: boolean;
  /**
   * @minItems 1
   */
  entries: [
    {
      leg_id?: TradeplanV2_LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: TradeplanV2_TpConditionNode;
    },
    ...{
      leg_id?: TradeplanV2_LegId;
      percent?: DecimalString;
      logic?: DealV2_LegJoin;
      condition: TradeplanV2_TpConditionNode;
    }[]
  ];
  stop_loss?: TradeplanV2_TpExitList;
  take_profit?: TradeplanV2_TpExitList;
  sizing: DealSizing;
  /**
   * Параметры публикации плана (используется ТОЛЬКО при публикации, не хранит связь с сделкой). bf_id — коннектор по умолчанию для UI; истина при публикации — bf_id из afbws.deal.publish.request.v1. account_id пусто/отсутствует — дефолтный (торговый) счёт коннектора, резолвится на лету (ExecutionService.resolve_plan_account).
   */
  publish?: {
    bf_id?: string;
    account_id?: string;
  };
  /**
   * AFB mail/deals read watermark: notifications with created_at <= delivery_at are treated as read on reconnect.
   */
  delivery_at?: string;
  created_at?: string;
  updated_at?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_TpConditionNode".
 */
export interface TradeplanV2_TpConditionNode {
  id?: string;
  op?: 'touch' | 'above' | 'below' | 'crosses_above' | 'crosses_below' | 'crossing' | 'breakout' | 'breakdown';
  /**
   * Required (enforced after compilation, not here) when op is a price candle operator (breakout/breakdown/crossing).
   */
  timeframe?: '5min' | '10min' | '15min' | '30min' | '1h' | '2h' | '4h' | '1d';
  /**
   * `condition.v1.json#/$defs/immediateExpr` (market entry) is valid only on an entry leg — enforced after compilation by deal.v2.json/BF, not here, same as the rest of this schema's left/right pairing.
   */
  left: ConditionV1_PriceExpr | ConditionV1_IndicatorExpr | ConditionV1_DatasetExpr | ConditionV1_ImmediateExpr;
  right: ConditionV1_RightConst | ConditionV1_IndicatorExpr | ConditionV1_DatasetExpr | TradeplanV2_PrimitiveRef;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_PrimitiveRef".
 */
export interface TradeplanV2_PrimitiveRef {
  primitive_id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanListRequest".
 */
export interface TradeplanListRequest {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.list.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  ticker?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanListResponse".
 */
export interface TradeplanListResponse {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.list.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  items: TradeplanEntity[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanSetRequest".
 */
export interface TradeplanSetRequest {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.set.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: TradeplanEntity;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanSetResponse".
 */
export interface TradeplanSetResponse {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.set.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: TradeplanEntity;
  amend_results: TradeplanAmendResultItem[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanAmendResultItem".
 */
export interface TradeplanAmendResultItem {
  schema: 'afbws.tradeplan.amend_result.v1';
  deal_id: string;
  accepted: boolean;
  revision?: string | number | null;
  status?: string | null;
  message?: string | null;
  code?: string | null;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanDeleteRequest".
 */
export interface TradeplanDeleteRequest {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.delete.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanDeleteResponse".
 */
export interface TradeplanDeleteResponse {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.delete.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsTradeplanChannelV1_ArchiveRequest".
 */
export interface AfbwsTradeplanChannelV1_ArchiveRequest {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.archive.request.v1';
  request_id: AfbwsCommonV1_RequestId;
  id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsTradeplanChannelV1_ArchiveResponse".
 */
export interface AfbwsTradeplanChannelV1_ArchiveResponse {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.archive.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  item: TradeplanEntity;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanErrorResponse".
 */
export interface TradeplanErrorResponse {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.error.response.v1';
  request_id: AfbwsCommonV1_RequestId;
  code: AfbwsCommonV1_ErrorCode;
  message: string;
  details?: {};
  item?: TradeplanEntity;
}
/**
 * items[] is a DELTA, not a snapshot: the client upserts plans in its own list by matching id and leaves everything else untouched. May contain a single element. The authoritative full list comes only from afbws.tradeplan.list.request.v1. Plan deletion is NOT conveyed by this push.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanSyncPush".
 */
export interface TradeplanSyncPush {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.sync.push.v1';
  /**
   * Delta of upserted plans, matched to the client's list by id. Never a full snapshot.
   */
  items: TradeplanEntity[];
}
/**
 * Building blocks reused across deal.v1.json/deal.v2.json/tradeplan.v1.json/tradeplan.v2.json/condition.v1.json/instrument.v1.json and payloads/dataset.*.json. Extracted from deal.v1.json (2026-08-11, tradeplan/deal separation Фаза B1) once it became clear deal.v1.json was serving as the de-facto shared library for the whole protocol, not just the afb.deal.v1 wire shape — deal.v1.json now keeps only what's genuinely v1-specific (conditionNode/entry/exitBlock). On the wire this is invisible: the resolved schema is byte-identical to before the move.
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
 * Single-entry / single-exit deal. All prices, steps, sizing values and thresholds are decimal STRINGS. The deal-level `direction` (long/short, same vocabulary as afb.deal.v2) is the single source of truth for position bias. Shared $defs (decimalString/instrument/target/sizing/executionPolicy/source) live in common.v1.json — this file keeps only what's v1-specific (conditionNode/entry/exitBlock); see common.v1.json's description for why.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV1".
 */
export interface DealV1 {
  schema: 'afb.deal.v1';
  deal_id: string;
  revision: number;
  owner?: {
    user_id?: string;
  };
  target: DealTarget;
  direction: 'long' | 'short';
  entry: DealV1_Entry;
  sizing: DealSizing;
  risk?: {
    take_profit?: DealV1_ExitBlock;
    stop_loss?: DealV1_ExitBlock;
  };
  execution_policy?: DealExecutionPolicy;
  archive_reason?: string;
  source?: DealSource;
}
/**
 * Multi-entry / multi-exit deal. entry, stop_loss, take_profit are root-level lists; each element may carry an optional `percent` (decimal string) and an optional `logic` (`#/$defs/legJoin`) joining it to the PRECEDING element in the same list — see `legJoin` for the full grammar (groups/buckets, `and`/`or` precedence, `percent` placement). Sum of percents per bucket resolves to 100. The deal-level `direction` (long/short) is the single source of truth for position bias — entry legs no longer carry a per-leg `side`, which would let 'buy' and 'sell' legs coexist in the same deal with no defined semantics (a deal is one position, not a basket of unrelated orders). The broker-facing buy/sell of each leg is derived from `direction` and its role: long entry / short exit -> buy; short entry / long exit -> sell. Reuses order/sizing/target defs from deal.v1.json; conditionNode is condition.v1.json's shared vocabulary (see that schema for the full price/indicator/dataset operator semantics) plus the wire-only `node_type` marker. Unlike afb.deal.v1 (fixed above/below/crosses_* /crossing vocabulary), afb.deal.v2 price conditions use condition.v1.json's full operator vocabulary — touch, above/below (inclusive level, no timeframe) and breakout/breakdown/crossing (closed-candle, requires timeframe) — or compare indicator/dataset expressions against a constant or (for indicator/dataset) against another expression of the same kind.
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
 * AFB-side MQTT notification payload published to <topic_base>/alarms/<user_id> when a user alarm triggers. Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time. `display` carries human-readable strings pre-rendered by AFB backend (mirrors frontend alarm cards).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "NotificationAlarmV1".
 */
export interface NotificationAlarmV1 {
  schema: 'afb.notification.alarm.v1';
  alarm_id: string;
  ticker: string;
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
 * DEPRECATED: superseded by broker.accounts (see payloads/broker.accounts.json) — kept for wire compatibility with AFB builds that have not negotiated multi_account. Response to broker.get_account, describing only BF's single trading account. Matches belphegor/reporting/broker_snapshots.py::account_snapshot_payload() exactly, including the account_id/broker_account_id split that broker.accounts deliberately drops (see broker.accounts.json). Correlated via correlation_id.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerAccountPayload".
 */
export interface BrokerAccountPayload {
  /**
   * BF's own trading account id (self._account_id) — NOT necessarily what the broker calls it, see broker_account_id.
   */
  account_id: string;
  /**
   * The account id as returned by the broker's GetAccount response (snapshot.account_id).
   */
  broker_account_id?: string;
  equity?: string | null;
  cash: PayloadsBrokerAccount_CashBalance[];
  positions: PayloadsBrokerAccount_Position[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerAccount_CashBalance".
 */
export interface PayloadsBrokerAccount_CashBalance {
  currency: string;
  value: string;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerAccount_Position".
 */
export interface PayloadsBrokerAccount_Position {
  /**
   * Signed lots (see position_reconcile.signed_broker_qty) — zero-quantity rows are never emitted.
   */
  quantity: number;
  average_price: string;
  current_price?: string | null;
  unrealized_pnl?: string | null;
  /**
   * Venue-resolved identity (exchange/board/ticker/market) — present when the symbol is known to BF's catalog.
   */
  instrument?: {};
  /**
   * Broker-native {broker,symbol} — present when instrument is unresolved, or always when afb.include_broker_ref is set.
   */
  broker_ref?: {};
  [k: string]: unknown;
}
/**
 * Response to broker.get_accounts and unsolicited push after every reconcile pass (see belphegor/reporting/account_directory.py::AccountDirectory, engine.py::_publish_broker_snapshots) — full list of accounts visible to BF's broker token. Only sent to AFB sessions that advertised session.hello_ack.features.multi_account; a BF instance that has negotiated multi_account with this AFB never sends the deprecated broker.account instead (see broker.account.json). Unlike broker.account, `accounts[].account_id` is the ONLY account identifier — no broker_account_id split, by design (the account_id/broker_account_id duplication in broker.account was judged confusing and deliberately not carried forward). Only `default_account_id` (BF's own trading account, self._account_id) is tradable in this phase — see brokers/port.py::account_id docstring; the rest are read-only until a later multi-account execution phase.
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
   * ISO timestamp this snapshot was assembled at. Unlike broker.account, this is always populated (no revision counter — BF does not track one).
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
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerCatalog_Meta".
 */
export interface PayloadsBrokerCatalog_Meta {
  session_date?: string | null;
  revision?: number;
  broker: string;
  exchanges: string[];
  markets: {
    exchange?: string;
    market?: string;
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "PayloadsBrokerCatalog_Slice".
 */
export interface PayloadsBrokerCatalog_Slice {
  session_date?: string | null;
  revision?: number;
  broker: string;
  exchange: string;
  market: string;
  instruments: {
    /**
     * Opaque broker-native locator (e.g. Finam's TICKER@MIC). Not the AFB `ticker`.
     */
    broker_symbol: string;
    exchange?: string;
    board?: string;
    ticker?: string;
    name?: string;
    market?: string;
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
/**
 * NACK for any broker.* command (get_account/get_orders/get_catalog/get_instrument/resolve_instrument). Correlated to the request via correlation_id.
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
   * Machine-readable error code (e.g. broker_disconnected).
   */
  code: string;
  /**
   * The broker.* command that failed (e.g. broker.get_account).
   */
  command_type: string;
  /**
   * Human-readable error detail.
   */
  message?: string;
  [k: string]: unknown;
}
/**
 * DEPRECATED: superseded by broker.get_accounts (see payloads/broker.get_accounts.json) — kept for wire compatibility with AFB builds that have not negotiated multi_account (see daemon.capabilities.json#/properties/features/properties/multi_account, session.hello_ack.json#/properties/features/properties/multi_account). AFB always sends an empty payload; no fields are read by BF (belphegor/plan_engine/engine.py::_get_account).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerGetAccountPayload".
 */
export interface BrokerGetAccountPayload {
  [k: string]: unknown;
}
/**
 * Request the full list of accounts visible to BF's broker token (not just its own trading account) — see belphegor/reporting/account_directory.py::AccountDirectory. Only sent by AFB after the BF instance advertised daemon.capabilities.features.multi_account (see daemon.capabilities.json). AFB always sends an empty payload today; account_ids is reserved for a future partial-refresh use and is not currently read by BF.
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
 * DEPRECATED: superseded by broker.resolve_instrument (see payloads/broker.resolve_instrument.json), which AFB's afbws.instrument.channel.v1 canal uses exclusively for detail lookups. Kept for wire compatibility; belphegor/plan_engine/engine.py::_get_symbol_info still serves it.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerGetInstrumentPayload".
 */
export interface BrokerGetInstrumentPayload {
  symbol: string;
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
 * Response to broker.get_instrument — the enriched instrument (belphegor/domain/instruments.py InstrumentInfo), unlike broker.catalog's brief CatalogEntry rows. Broker-agnostic explicit allow-list, not an asdict()-based dump: broker-native/Finam-specific fields (asset_type, min_step_raw, long_risk_rate, short_risk_rate, future_details, bond_details) never reach this wire — AFB doesn't read them and admitting them would make this canon description implicitly Finam-shaped (belphegor/reporting/broker_snapshots.py::instrument_resolved_payload builds this explicitly, not via InstrumentInfo.to_broker_instrument_dict(), which a different wire field — deal.accepted's broker_instrument — still uses unchanged). `symbol`/`currency` are the canon names on this wire — they map from InstrumentInfo's own internal `symbol`/`quote_currency` attributes, which are unchanged BF-side. additionalProperties stays true so a future broker plugin can add fields without breaking AFB's validation; required kept to `symbol`. This is a PATCH-level description of existing wire behavior, not a new constraint on it.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerInstrumentPayload".
 */
export interface BrokerInstrumentPayload {
  /**
   * Opaque broker-native locator (e.g. Finam's TICKER@MIC).
   */
  symbol: string;
  exchange?: string;
  board?: string;
  ticker?: string;
  mic?: string;
  name?: string;
  market?: string;
  decimals?: number;
  price_step?: string;
  lot_size?: number;
  currency?: string;
  expiration_date?: string | null;
  tradable?: boolean;
  longable?: boolean;
  shortable?: boolean;
  long_initial_margin?: string | null;
  short_initial_margin?: string | null;
  updated_at?: string | null;
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
   * Same trading-params shape as broker.instrument.json (minus symbol/account_id/exchange/board/ticker) — see InstrumentInfo.to_broker_instrument_dict().
   */
  broker_instrument: {
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
 * Deal-instrument pre-flight (AFB's afbws.instrument.channel.v1 `resolve`/`detail`, and the tradeplan publish path) — `deal` is a compiled ExecutionDeal (afb.deal.v1 or afb.deal.v2), the same shape deal.publish carries, sent here purely for its target/instrument fields; BF does not persist it from this command.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BrokerResolveInstrumentPayload".
 */
export interface BrokerResolveInstrumentPayload {
  deal: DealV1 | DealV2;
  [k: string]: unknown;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionTriggeredPayload".
 */
export interface ConditionTriggeredPayload {
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
   * BF's single trading account (brokers/port.py::account_id) — the account this BF instance executes orders on. When features.multi_account is true, the full account list/snapshots are fetched separately via broker.get_accounts, not from this field.
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
     * Deal execution modes this BF instance supports (see deal.v1.json#/$defs/executionPolicy/properties/execution_mode). AFB/UI use this to offer only modes the BF can actually run.
     */
    execution_modes?: ('client' | 'hybrid' | 'server')[];
    reports_api?: boolean;
    catalog?: boolean;
    /**
     * This BF build implements broker.get_accounts/broker.accounts (see payloads/broker.accounts.json) — read-only visibility into every account the broker token can see, not just the trading account named by account_id above. Execution still happens only on account_id in this phase. AFB gates sending broker.get_accounts on this flag being true; absent/false means fall back to the deprecated broker.get_account/broker.account pair.
     */
    multi_account?: boolean;
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
  deal: DealV1 | DealV2;
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
  deal: DealV1 | DealV2;
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
  code: string;
  command_type: string;
  deal_id?: string | number | boolean | {} | unknown[] | null;
  message?: string;
  [k: string]: unknown;
}
/**
 * Report attached to deal.status_changed(closed) with the trade-based fill log for the just-closed deal. `trade_id` is not required — tolerant of older BF versions that predate it. The `summary` block (entry/exit_avg_price, realized_pnl, total_commission) was removed in v2.0.10: it had no consumers (AFB computes realized PnL itself from fills/order events), was never in `required`, and `additionalProperties: true` keeps old and new payloads mutually valid — a PATCH, not a breaking change. `fills[].commission` was removed in the same step for the same reason.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealReportPayload".
 */
export interface DealReportPayload {
  /**
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  close_reason?: string;
  deal_id: string;
  revision: number;
  status: string;
  /**
   * Trade-based fill log: one element per broker trade, not per order — an order filled in several trades (e.g. Finam SubscribeTrades) yields one element per trade, all sharing the same order_id. `order_id` remains the reference to the parent order (for role/leg); commission/summary are not part of this payload (removed in v2.0.10, see below).
   */
  fills?: {
    /**
     * Broker trade identifier. For brokers without a native trade concept, a synthetic id derived from order_id (e.g. `synth-{order_id}`).
     */
    trade_id?: string;
    order_id: string;
    price?: string | number | boolean | {} | unknown[] | null;
    quantity?: number;
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
   * ISO-8601 BF event-occurrence time (same value as the BF journal entry `at`).
   */
  at?: string;
  deal_id: string;
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
 * via the `definition` "OrderFilledPayload".
 */
export interface OrderFilledPayload {
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
   * AFB-side capability flags for this session — read by BF's afb_client (see afb_client/ws_client.py, alongside dry_run/margin_trading above) to decide what it may send this AFB.
   */
  features?: {
    /**
     * This AFB build understands broker.accounts (see payloads/broker.accounts.json) and negotiated_support for it. When true, BF sends broker.accounts (in response to broker.get_accounts, and unsolicited after every reconcile pass) and stops sending the deprecated broker.account to this session. Absent/false means BF must keep sending broker.account only.
     */
    multi_account?: boolean;
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
