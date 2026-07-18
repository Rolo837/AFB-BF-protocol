/**
 * DO NOT EDIT BY HAND — generated from spec/schemas/ (all *.json files) by
 * ts/tools/generate-models.mjs (invoked via `afb-bf-protocol-generate`).
 * source-hash: 124f84592503c48e5c18d26cf60d1c1a2e884f99e7199a68857d9d1494ab34ad
 */

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
   * afb.deal.v1 conditions only compare against the last traded price. quote/indicator/dataset sources are afb.deal.v2-only.
   */
  left: {
    source: 'price';
    field?: 'last';
  };
  right: {
    const: DealV1_DecimalString;
  };
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
 * This interface was referenced by `_GeneratedRoot`'s JSON-Schema
 * via the `definition` "TradeplanV2_PrimitiveRef".
 */
export interface TradeplanV2_PrimitiveRef {
  primitive_id: string;
}
