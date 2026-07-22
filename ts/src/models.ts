/**
 * DO NOT EDIT BY HAND — generated from spec/schemas/ (all *.json files) by
 * ts/tools/generate-models.mjs (invoked via `afb-bf-protocol-generate`).
 * source-hash: 8a6d10a0be4fb20d891ff68066d43ffb8ba4fe24a8c92500bf07f9ca54fab226
 */

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
 * Client-generated correlation id (e.g. uuid4), echoed verbatim in the matching response.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AfbwsCommonV1_RequestId".
 */
export type AfbwsCommonV1_RequestId = string;
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
 * via the `definition` "DealV1_DecimalString".
 */
export type DealV1_DecimalString = string;
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
 * via the `definition` "AfbwsCommonV1_ErrorCode".
 */
export type AfbwsCommonV1_ErrorCode =
  'not_found' | 'invalid_schema' | 'invalid_channel' | 'validation_error' | 'conflict' | 'internal_error';
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "BfsRegistryEntry".
 */
export type BfsRegistryEntry = BfRegistryEntry & {
  connected: boolean;
  dry_run: boolean;
  dry_run_afb?: boolean;
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
  | GpErrorResponse;
/**
 * AFB-side chart primitive (line/line_enter/line_sl/line_tp/note/zone/ruler) — like afb.alarm.v1, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel. Promotes the parked settings.primitives[secid][] draft (draft/primitive.v1.json) into a strict canonical entity: `ticker` becomes an explicit required field instead of an implicit dict key, so get(id)/list(ticker) work on a flat collection. Never carries `used_in_tradeplans` (rejected by additionalProperties: false) — whether a primitive is referenced by a tradeplan is derived fresh from the tradeplans themselves on every read, never persisted or transmitted as part of this entity (see AFB/docs/ENTITY_WS_PROTOCOL.md). `stop` is a second anchor point required only for zone/ruler (forbidden for every other kind, enforced by the `allOf` below, not just by convention); `text` is accepted only for `note` (optional even there).
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
  percent?: DealV1_DecimalString;
  condition: TradeplanV2_TpConditionNode;
}[];
/**
 * Optional protective time in seconds: the condition must remain continuously true for this many real seconds (BF monotonic clock) before firing. False, evaluate gaps, amend/pause/cancel and BF restart reset progress; progress is not persisted. AFB draft emulation and alarms ignore it. Only meaningful with price above/below (producer converts touch to above/below before wire); multi-leg plans may carry duration independently per leg.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_Duration".
 */
export type ConditionV1_Duration = number;
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
 * via the `definition` "DealV2_ExitList".
 */
export type DealV2_ExitList = {
  percent?: DealV1_DecimalString;
  condition: DealV2_ConditionNode;
}[];

/**
 * Pure proxy of BF's `broker.catalog` payload (see belphegor/proxy.py). `data` untyped — BF owns the shape, unschematized on the wire.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountCatalogPush".
 */
export interface AccountCatalogPush {
  type: 'catalog';
  bf_id: string;
  data: {
    [k: string]: unknown;
  };
}
/**
 * Journal of incoming BF events (JSONL direction=in) for one bf_id/day. See ExecutionService.get_account_events_for_user and event_translator.envelope_to_event_record (AFB/backend/trade/).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountEventsPush".
 */
export interface AccountEventsPush {
  type: 'events';
  bf_id: string;
  date: string;
  data: AccountEventRecord[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountEventRecord".
 */
export interface AccountEventRecord {
  logged_at: string;
  bf_id: string;
  deal_id?: string | null;
  category: 'deal' | 'order' | 'position' | 'condition';
  event: string;
  data?: {} | null;
}
/**
 * Pure proxy of BF's `broker.instrument` payload (see belphegor/proxy.py). `data` untyped — BF owns the shape, unschematized on the wire.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountInstrumentPush".
 */
export interface AccountInstrumentPush {
  type: 'instrument';
  bf_id: string;
  data: {
    [k: string]: unknown;
  };
}
/**
 * Pure proxy of BF's `broker.orders` payload (see belphegor/proxy.py). `data` untyped for the same reason as account.snapshot.v1.json — BF owns the shape, unschematized on the wire.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountOrdersPush".
 */
export interface AccountOrdersPush {
  type: 'orders';
  bf_id: string;
  data: {
    [k: string]: unknown;
  };
  /**
   * Merged in by event_translator._merge_snapshot_meta when present on the BF payload.
   */
  revision?: number;
  as_of?: string;
  source?: string;
}
/**
 * Pure proxy of BF's `broker.account` payload (see belphegor/proxy.py: `dict(envelope.payload)`) plus the AFB envelope wrapper. `data` is intentionally untyped — BF owns that shape and it isn't schematized anywhere (no afb.execution.v1 schema for broker.account); the frontend normalizes it defensively (see belphegor.ts normalizeCashBalances/normalizePositions) rather than trusting a strict shape.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "AccountSnapshotPush".
 */
export interface AccountSnapshotPush {
  type: 'account';
  bf_id: string;
  data: {
    [k: string]: unknown;
  };
  /**
   * Merged in by event_translator._merge_snapshot_meta when present on the BF payload.
   */
  revision?: number;
  as_of?: string;
  source?: string;
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
  const: DealV1_DecimalString;
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
 * See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--event. `data` shape depends on category/event (status_changed, created, archived-as-status_changed, or a raw BF envelope payload) — deliberately untyped here.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealEventPush".
 */
export interface DealEventPush {
  type: 'event';
  deal_id: string;
  bf_id: string;
  category: 'deal' | 'order' | 'position' | 'condition';
  event: string;
  logged_at: string;
  data: {
    [k: string]: unknown;
  };
}
/**
 * See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--pnl. Periodic unrealized-P&L push, not persisted.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealPnlPush".
 */
export interface DealPnlPush {
  type: 'pnl';
  deal_id: string;
  bf_id: string;
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
 * Full authoritative deal snapshot, pushed so the frontend replaces its cached copy instead of merging partial fields from thin `event` pushes. `data` is the same shape as DealState.to_dict() (deal_state.v2.json).
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealRecordPush".
 */
export interface DealRecordPush {
  type: 'deal_record';
  deal_id: string;
  bf_id: string;
  data: DealStateV2;
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
   * Negotiated heartbeat interval for stale detection/display in AFB frontend.
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
  status?: 'new' | 'active' | 'published' | 'closed' | 'expired';
  direction?: 'long' | 'short';
  schema?: 'afb.tradeplan.v1';
  activated_at?: string;
  closed_at?: string;
  entry_condition: TradeplanV1_EntryCondition;
  quantity_value?: number | null;
  quantity_mode?: 'lots' | 'margin' | 'balance_pct' | 'risk_currency' | 'risk_factor';
  take_profit?: TradeplanV1_Condition | null;
  stop_loss?: TradeplanV1_Condition | null;
  deal_id?: string;
  /**
   * AFB bf_id (real connector or virtual) used when publishing this plan. Omitted when user has neither trade nor virtual capability.
   */
  connector?: string;
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
 * AFB-side multi-entry / multi-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v2. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `direction` (long/short) is the single source of truth for position bias, at plan level — entry legs do not carry a per-leg side (a list of entries with independent buy/sell sides has no defined execution semantics for one deal). Conditions are deal.v2-compatible nodes — price legs carry an explicit `op` (touch/above/below/breakout/breakdown/crossing), `op` omitted on a price leg means touch (accepted for back-compat with old plans); indicator legs may omit `op`, derived from direction/scope at compile time — with one extension: the `right` side of a condition may be a `primitiveRef` (`{"primitive_id": "..."}`), a reference to a chart line primitive that AFB resolves to a decimal `const` at compile time. The full left/right pairing matrix (price/quote const-only, indicator/dataset const-or-same-kind) is enforced after compilation by deal.v2.json and by BF, not here — this schema deliberately stays loose to accommodate primitiveRef.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradePlanV2".
 */
export interface TradePlanV2 {
  id: string;
  ticker: string;
  status?: 'new' | 'active' | 'published' | 'closed' | 'expired';
  direction: 'long' | 'short';
  schema: 'afb.tradeplan.v2';
  activated_at?: string;
  closed_at?: string;
  /**
   * @minItems 1
   */
  entries: [
    {
      percent?: DealV1_DecimalString;
      condition: TradeplanV2_TpConditionNode;
    },
    ...{
      percent?: DealV1_DecimalString;
      condition: TradeplanV2_TpConditionNode;
    }[]
  ];
  stop_loss?: TradeplanV2_TpExitList;
  take_profit?: TradeplanV2_TpExitList;
  sizing: DealV1_Sizing;
  deal_id?: string;
  /**
   * AFB bf_id (real connector or virtual) used when publishing this plan. Omitted when user has neither trade nor virtual capability.
   */
  connector?: string;
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
  left: ConditionV1_PriceExpr | ConditionV1_IndicatorExpr | ConditionV1_DatasetExpr;
  right: ConditionV1_RightConst | ConditionV1_IndicatorExpr | ConditionV1_DatasetExpr | TradeplanV2_PrimitiveRef;
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
 * via the `definition` "TradeplanV2_PrimitiveRef".
 */
export interface TradeplanV2_PrimitiveRef {
  primitive_id: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV1_Sizing".
 */
export interface DealV1_Sizing {
  mode: 'lots' | 'margin' | 'risk_currency' | 'risk_factor' | 'balance_pct';
  value: DealV1_DecimalString;
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
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanSyncPush".
 */
export interface TradeplanSyncPush {
  channel: 'tradeplan';
  schema: 'afbws.tradeplan.sync.push.v1';
  items: TradeplanEntity[];
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "ConditionV1_ImmediateExpr".
 */
export interface ConditionV1_ImmediateExpr {
  source: 'immediate';
}
/**
 * Single-entry / single-exit deal. All prices, steps, sizing values and thresholds are decimal STRINGS. The deal-level `direction` (long/short, same vocabulary as afb.deal.v2) is the single source of truth for position bias.
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
  target: DealV1_Target;
  direction: 'long' | 'short';
  entry: DealV1_Entry;
  sizing: DealV1_Sizing;
  risk?: {
    take_profit?: DealV1_ExitBlock;
    stop_loss?: DealV1_ExitBlock;
  };
  execution_policy?: DealV1_ExecutionPolicy;
  archive_reason?: string;
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV1_Target".
 */
export interface DealV1_Target {
  bf_id: string;
  broker: string;
  instrument: DealV1_Instrument;
  /**
   * broker-native locator added by BF after publish
   */
  binding?: {};
}
/**
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV1_Instrument".
 */
export interface DealV1_Instrument {
  exchange: string;
  board: string;
  ticker: string;
  market?: 'stock' | 'futures' | 'currency';
  price_step?: DealV1_DecimalString;
  step_price?: DealV1_DecimalString;
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
    const: DealV1_DecimalString;
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
 * via the `definition` "DealV1_ExecutionPolicy".
 */
export interface DealV1_ExecutionPolicy {
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
    stop_price?: DealV1_DecimalString;
    max_loss_steps?: number;
    /**
     * Reserved for a future server-side take-profit leg (OCO). Always rejected as true for now — the backstop is protection-only in this phase.
     */
    take_profit?: boolean;
  };
}
/**
 * Multi-entry / multi-exit deal. entry, stop_loss, take_profit are root-level lists; each element may carry an optional `percent` (decimal string). Sum of percents per role resolves to 100. The deal-level `direction` (long/short) is the single source of truth for position bias — entry legs no longer carry a per-leg `side`, which would let 'buy' and 'sell' legs coexist in the same deal with no defined semantics (a deal is one position, not a basket of unrelated orders). The broker-facing buy/sell of each leg is derived from `direction` and its role: long entry / short exit -> buy; short entry / long exit -> sell. Reuses order/sizing/target defs from deal.v1.json; conditionNode is condition.v1.json's shared vocabulary (see that schema for the full price/indicator/dataset operator semantics) plus the wire-only `node_type` marker. Unlike afb.deal.v1 (fixed above/below/crosses_* /crossing vocabulary), afb.deal.v2 price conditions use condition.v1.json's full operator vocabulary — touch, above/below (inclusive level, no timeframe) and breakout/breakdown/crossing (closed-candle, requires timeframe) — or compare indicator/dataset expressions against a constant or (for indicator/dataset) against another expression of the same kind.
 *
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "DealV2".
 */
export interface DealV2 {
  schema: 'afb.deal.v2';
  deal_id: string;
  revision: number;
  owner?: {};
  target: DealV1_Target;
  direction: 'long' | 'short';
  /**
   * @minItems 1
   */
  entry: [
    {
      percent?: DealV1_DecimalString;
      condition: DealV2_ConditionNode;
    },
    ...{
      percent?: DealV1_DecimalString;
      condition: DealV2_ConditionNode;
    }[]
  ];
  stop_loss?: DealV2_ExitList;
  take_profit?: DealV2_ExitList;
  sizing: DealV1_Sizing;
  execution_policy?: DealV1_ExecutionPolicy;
  archive_reason?: string;
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
  fills?: {
    commission?: string | number | boolean | {} | unknown[] | null;
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
  summary?: {
    entry_avg_price?: string | number | boolean | {} | unknown[] | null;
    exit_avg_price?: string | number | boolean | {} | unknown[] | null;
    realized_pnl?: string | number | boolean | {} | unknown[] | null;
    total_commission?: string | number | boolean | {} | unknown[] | null;
    [k: string]: unknown;
  };
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
  heartbeat_interval_sec?: number;
  protocol: string;
  accepted_protocol?: string;
  dry_run?: boolean;
  dry_run_afb?: boolean;
  dry_run_bf?: boolean;
  margin_trading?: boolean;
  margin_trading_afb?: boolean;
  margin_trading_bf?: boolean;
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
