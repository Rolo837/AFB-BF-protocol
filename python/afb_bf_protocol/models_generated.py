# DO NOT EDIT BY HAND — generated from spec/schemas/ (via
# spec/.generated/bundled-schema.json) by datamodel-codegen, invoked from
# tools/generate.py. Run `afb-bf-protocol-generate` to regenerate.
# source-hash: d66431f2e6808643cd5402f7008ffa463450ec82c046d0c2a1c4f0a3a581ea2f

from __future__ import annotations

from typing import Any, Literal, NotRequired, TypeAlias, TypedDict


class AccountCatalogPush(TypedDict):
    """
    Pure proxy of BF's `broker.catalog` payload (see belphegor/proxy.py). `data` untyped — BF owns the shape, unschematized on the wire.
    """

    type: Literal["catalog"]
    bf_id: str
    data: dict[str, Any]


class AccountEventRecord(TypedDict):
    logged_at: str
    bf_id: str
    deal_id: NotRequired[str | None]
    category: Literal["deal", "order", "position", "condition"]
    event: str
    data: NotRequired[dict[str, Any] | None]


class AccountEventsPush(TypedDict):
    """
    Journal of incoming BF events (JSONL direction=in) for one bf_id/day. See ExecutionService.get_account_events_for_user and event_translator.envelope_to_event_record (AFB/backend/trade/).
    """

    type: Literal["events"]
    bf_id: str
    date: str
    data: list[AccountEventRecord]


class AccountInstrumentPush(TypedDict):
    """
    Pure proxy of BF's `broker.instrument` payload (see belphegor/proxy.py). `data` untyped — BF owns the shape, unschematized on the wire.
    """

    type: Literal["instrument"]
    bf_id: str
    data: dict[str, Any]


class AccountOrdersPush(TypedDict):
    """
    Pure proxy of BF's `broker.orders` payload (see belphegor/proxy.py). `data` untyped for the same reason as account.snapshot.v1.json — BF owns the shape, unschematized on the wire.
    """

    type: Literal["orders"]
    bf_id: str
    data: dict[str, Any]
    revision: NotRequired[int]
    as_of: NotRequired[str]
    source: NotRequired[str]


class AccountSnapshotPush(TypedDict):
    """
    Pure proxy of BF's `broker.account` payload (see belphegor/proxy.py: `dict(envelope.payload)`) plus the AFB envelope wrapper. `data` is intentionally untyped — BF owns that shape and it isn't schematized anywhere (no afb.execution.v1 schema for broker.account); the frontend normalizes it defensively (see belphegor.ts normalizeCashBalances/normalizePositions) rather than trusting a strict shape.
    """

    type: Literal["account"]
    bf_id: str
    data: dict[str, Any]
    revision: NotRequired[int]
    as_of: NotRequired[str]
    source: NotRequired[str]


AfbwsCommonV1ErrorCode: TypeAlias = Literal[
    "not_found",
    "invalid_schema",
    "invalid_channel",
    "validation_error",
    "conflict",
    "internal_error",
]


AfbwsCommonV1RequestId: TypeAlias = str


AfbwsCommonV1Root: TypeAlias = Any


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


class Backstop(TypedDict):
    """
    Per-deal overrides for the hybrid-mode server-side backstop order; unset fields fall back to the executing BF's own config defaults. Meaningful only when execution_mode is `hybrid`.
    """

    offset_steps: NotRequired[int]
    stop_price: NotRequired[DealV1DecimalString]
    max_loss_steps: NotRequired[int]
    take_profit: NotRequired[bool]


class BfRegistryEntry(TypedDict):
    """
    Shared public-view basis for `bfs` (registry push) and `connector` (record CRUD) — see BFRegistryEntry.to_public_dict() in AFB/backend/trade/models.py.
    """

    bf_id: str
    name: str
    enabled: bool
    display_name: str
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


class BrokerPositionLedgerPayload(TypedDict):
    account_id: str
    entries: list[Entry]
    residual_by_symbol: dict[str, int]


class BrokerSizing(TypedDict):
    account_id: NotRequired[str]
    deal_notional: NotRequired[str]
    lots: NotRequired[int]
    required_cash: NotRequired[str]
    required_cash_basis: NotRequired[str]
    sizing_mode: NotRequired[str]
    estimated: NotRequired[bool]


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


ConditionNode: TypeAlias = (
    ConditionNode1 | ConditionNode2 | ConditionNode3 | ConditionNode4 | ConditionNode5
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
    const: DealV1DecimalString


ConditionV1ScalarOp: TypeAlias = Literal[
    "above", "below", "crosses_above", "crosses_below", "crossing"
]


ConditionV1Timeframe: TypeAlias = Literal[
    "5min", "10min", "15min", "30min", "1h", "2h", "4h", "1d"
]


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
    allowed_roles: NotRequired[list[str]]
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


class DealAmendPayload(TypedDict):
    """
    Re-define an existing deal in place. `deal` is the full new definition (its `revision` must be `base_revision` + 1, same `deal_id`). BF gates the change against the allowed-edit matrix (amend_rules) using the deal's live execution phase, then lets reconcile bring broker orders to the new desired state. Unlike deal.publish, the deal's status and observed execution state (orders/positions/phase) are preserved.
    """

    deal_id: str
    base_revision: int
    deal: DealV1 | DealV2


class DealArchivedPayload(TypedDict):
    archived_at: NotRequired[str]
    at: NotRequired[str]
    deal_id: str
    reason: str
    revision: int


class DealEventPush(TypedDict):
    """
    See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--event. `data` shape depends on category/event (status_changed, created, archived-as-status_changed, or a raw BF envelope payload) — deliberately untyped here.
    """

    type: Literal["event"]
    deal_id: str
    bf_id: str
    category: Literal["deal", "order", "position", "condition"]
    event: str
    logged_at: str
    data: dict[str, Any]


class DealOperationPayload(TypedDict):
    operations: NotRequired[list[Operation]]


class DealPnlPush(TypedDict):
    """
    See AFB/docs/WS_EXECUTION_CHANNELS.md#deal--pnl. Periodic unrealized-P&L push, not persisted.
    """

    type: Literal["pnl"]
    deal_id: str
    bf_id: str
    data: Data1


class DealPositionsSyncedPayload(TypedDict):
    at: NotRequired[str]
    changed: NotRequired[list[ChangedItem]]
    deal_id: str


class DealPublishPayload(TypedDict):
    deal: DealV1 | DealV2


class DealRecordPush(TypedDict):
    """
    Full authoritative deal snapshot, pushed so the frontend replaces its cached copy instead of merging partial fields from thin `event` pushes. `data` is the same shape as DealState.to_dict() (deal_state.v2.json).
    """

    type: Literal["deal_record"]
    deal_id: str
    bf_id: str
    data: DealStateV2


class DealRejectedPayload(TypedDict):
    at: NotRequired[str]
    code: str
    command_type: str
    deal_id: NotRequired[str | float | int | bool | dict[str, Any] | list[Any] | None]
    message: NotRequired[str]


class DealReportPayload(TypedDict):
    at: NotRequired[str]
    close_reason: NotRequired[str]
    deal_id: str
    revision: int
    status: str
    fills: NotRequired[list[Fill]]
    summary: NotRequired[Summary]


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
    revision: int
    status: str


class DealV1(TypedDict):
    """
    Single-entry / single-exit deal. All prices, steps, sizing values and thresholds are decimal STRINGS. The deal-level `direction` (long/short, same vocabulary as afb.deal.v2) is the single source of truth for position bias.
    """

    schema: Literal["afb.deal.v1"]
    deal_id: str
    revision: int
    owner: NotRequired[Owner]
    target: DealV1Target
    direction: Literal["long", "short"]
    entry: DealV1Entry
    sizing: DealV1Sizing
    risk: NotRequired[Risk]
    execution_policy: NotRequired[DealV1ExecutionPolicy]
    archive_reason: NotRequired[str]


class DealV1ConditionNode(TypedDict):
    node_type: Literal["event"]
    id: NotRequired[str]
    op: Literal["above", "below", "crosses_above", "crosses_below", "crossing"]
    left: Left
    right: Right


DealV1DecimalString: TypeAlias = str


class DealV1Entry(TypedDict):
    condition: DealV1ConditionNode


class DealV1ExecutionPolicy(TypedDict):
    on_afb_disconnect: NotRequired[str]
    max_spread_steps: NotRequired[int]
    margin_trading: NotRequired[bool]
    execution_mode: NotRequired[Literal["client", "hybrid", "server"]]
    backstop: NotRequired[Backstop]


class DealV1ExitBlock(TypedDict):
    condition: NotRequired[DealV1ConditionNode]


class DealV1Instrument(TypedDict):
    exchange: str
    board: str
    ticker: str
    market: NotRequired[Literal["stock", "futures", "currency"]]
    price_step: NotRequired[DealV1DecimalString]
    step_price: NotRequired[DealV1DecimalString]


class DealV1Sizing(TypedDict):
    mode: Literal["lots", "margin", "risk_currency", "risk_factor", "balance_pct"]
    value: DealV1DecimalString


class DealV1Target(TypedDict):
    bf_id: str
    broker: str
    instrument: DealV1Instrument
    binding: NotRequired[dict[str, Any]]


class DealV2(TypedDict):
    """
    Multi-entry / multi-exit deal. entry, stop_loss, take_profit are root-level lists; each element may carry an optional `percent` (decimal string). Sum of percents per role resolves to 100. The deal-level `direction` (long/short) is the single source of truth for position bias — entry legs no longer carry a per-leg `side`, which would let 'buy' and 'sell' legs coexist in the same deal with no defined semantics (a deal is one position, not a basket of unrelated orders). The broker-facing buy/sell of each leg is derived from `direction` and its role: long entry / short exit -> buy; short entry / long exit -> sell. Reuses order/sizing/target defs from deal.v1.json; conditionNode is condition.v1.json's shared vocabulary (see that schema for the full price/indicator/dataset operator semantics) plus the wire-only `node_type` marker. Unlike afb.deal.v1 (fixed above/below/crosses_*/crossing vocabulary), afb.deal.v2 price conditions use condition.v1.json's full operator vocabulary — touch, above/below (inclusive level, no timeframe) and breakout/breakdown/crossing (closed-candle, requires timeframe) — or compare indicator/dataset expressions against a constant or (for indicator/dataset) against another expression of the same kind.
    """

    schema: Literal["afb.deal.v2"]
    deal_id: str
    revision: int
    owner: NotRequired[dict[str, Any]]
    target: DealV1Target
    direction: Literal["long", "short"]
    entry: list[EntryItem]
    stop_loss: NotRequired[DealV2ExitList]
    take_profit: NotRequired[DealV2ExitList]
    sizing: DealV1Sizing
    execution_policy: NotRequired[DealV1ExecutionPolicy]
    archive_reason: NotRequired[str]


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
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """

    node_type: Literal["event"]


class DealV2ConditionNode10(DealV2ConditionNode4, DealV2ConditionNode6):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode11(DealV2ConditionNode5, DealV2ConditionNode6):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode7(DealV2ConditionNode1, DealV2ConditionNode6):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode8(DealV2ConditionNode2, DealV2ConditionNode6):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


class DealV2ConditionNode9(DealV2ConditionNode3, DealV2ConditionNode6):
    """
    Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
    """


DealV2ConditionNode: TypeAlias = (
    DealV2ConditionNode7
    | DealV2ConditionNode8
    | DealV2ConditionNode9
    | DealV2ConditionNode10
    | DealV2ConditionNode11
)
"""
Wire-level condition node: same vocabulary as condition.v1.json#/$defs/conditionNode, plus the mandatory `node_type` envelope marker used on the AFB<->BF wire (trade-plan conditions, which never cross the wire, don't carry it).
"""


class DealV2ExitListItem(TypedDict):
    percent: NotRequired[DealV1DecimalString]
    condition: DealV2ConditionNode


DealV2ExitList: TypeAlias = list[DealV2ExitListItem]


class Deals(TypedDict):
    revision: int
    status: str
    execution_phase: NotRequired[str]
    archived: bool


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
    percent: NotRequired[DealV1DecimalString]
    condition: TradeplanV2TpConditionNode


class EntryItem(TypedDict):
    percent: NotRequired[DealV1DecimalString]
    condition: DealV2ConditionNode


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


class Fill(TypedDict):
    commission: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
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
    | GpErrorResponse
)


class GpV1(TypedDict):
    """
    AFB-side chart primitive (line/line_enter/line_sl/line_tp/note/zone/ruler) — like afb.alarm.v1, this is NOT an AsyncAPI wire message, it never crosses the AFB<->BF channel. Promotes the parked settings.primitives[secid][] draft (draft/primitive.v1.json) into a strict canonical entity: `ticker` becomes an explicit required field instead of an implicit dict key, so get(id)/list(ticker) work on a flat collection. Never carries `used_in_tradeplans` (rejected by additionalProperties: false) — whether a primitive is referenced by a tradeplan is derived fresh from the tradeplans themselves on every read, never persisted or transmitted as part of this entity (see AFB/docs/ENTITY_WS_PROTOCOL.md). `stop` is a second anchor point required only for zone/ruler (forbidden for every other kind, enforced by the `allOf` below, not just by convention); `text` is accepted only for `note` (optional even there).
    """

    schema: Literal["afb.gp.v1"]
    id: str
    ticker: str
    kind: Literal["line", "line_enter", "line_sl", "line_tp", "note", "zone", "ruler"]
    start: GpV1Point
    stop: NotRequired[GpV1Point]
    text: NotRequired[str]


class GpV1Point(TypedDict):
    time: int
    price: float


class Health(TypedDict):
    overall: NotRequired[Literal["ok", "warning", "critical"]]
    points: NotRequired[dict[str, Any]]


class Instrument(TypedDict):
    shortname: NotRequired[str]
    secname: NotRequired[str]


class Left(TypedDict):
    """
    afb.deal.v1 conditions only compare against the last traded price. quote/indicator/dataset sources are afb.deal.v2-only.
    """

    source: Literal["price"]
    field: NotRequired[Literal["last"]]


class LinkAdminSetInput(TypedDict):
    """
    Manager upsert: `bf_id` omitted means create (backend assigns/validates id and requires broker + defaults); `bf_id` present and already registered means update. Backend enforces which combination is valid, not this schema.
    """

    bf_id: NotRequired[str]
    name: NotRequired[str]
    enabled: NotRequired[bool]
    display_name: NotRequired[str]
    broker: NotRequired[str]
    protocol: NotRequired[str]
    dry_run: NotRequired[bool | None]
    margin_trading: NotRequired[bool | None]
    execution_policy: NotRequired[ConnectorExecutionPolicy]
    allowed_roles: NotRequired[list[str]]
    allowed_users: NotRequired[list[str]]


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
    channel: Literal["link"]
    schema: Literal["afbws.link.list.request.v1"]
    request_id: AfbwsCommonV1RequestId


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
    allowed_roles: list[str]
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


class LinkUserSetInput(TypedDict):
    """
    A non-manager caller may only adjust dry_run/execution_policy on their own already-existing connector — never name/enabled/display_name/broker/protocol/allowed_*, and never create a new entry (bf_id must already exist and be owned by the caller; enforced by the backend, not this schema).
    """

    bf_id: str
    dry_run: NotRequired[bool | None]
    execution_policy: NotRequired[ConnectorExecutionPolicy]


LinkSetInput: TypeAlias = LinkUserSetInput | LinkAdminSetInput


class LinkUserV1(BfRegistryEntry, LinkSharedFields):
    """
    Caller-scoped BF connector config record for a non-manager viewer (owner: capability trade + user_id in allowed_users, or role-only access — role-only is read-only, enforced by the backend, not this schema). Never carries `connected`/`daemon`/session runtime — see link.status.v1.json for that, delivered on a separate push. The synthetic `virtual` pseudo-connector also uses this exact shape (kind:"virtual") — see link.channel.v1.json. `$defs/sharedFields` is the single source of the fields link.admin.v1.json reuses (via $ref) so the two views can't drift apart independently.
    """

    schema: Literal["afbws.link.user.v1"]


LinkEntity: TypeAlias = LinkUserV1 | LinkAdminV1


class MarketData(TypedDict):
    """
    What market data this BF instance can serve, and on which wire timeframes (see condition.v1.json#/$defs/timeframe) — used by AFB to validate indicator/price-candle condition timeframes before publish.
    """

    quotes: NotRequired[bool]
    candles: NotRequired[bool]
    orderbook: NotRequired[bool]
    timeframes: NotRequired[list[ConditionV1Timeframe]]


class Meta(TypedDict):
    brokers: list[str]


Model: TypeAlias = Any


class NotificationAlarmV1(TypedDict):
    """
    AFB-side MQTT notification payload published to <topic_base>/alarms/<user_id> when a user alarm triggers. Consumed by the AFB informer daemon (Telegram/email). NOT an AsyncAPI wire message — never crosses the AFB<->BF channel, not signed. `timestamp` is added by MQTTPublisher at publish time. `display` carries human-readable strings pre-rendered by AFB backend (mirrors frontend alarm cards).
    """

    schema: Literal["afb.notification.alarm.v1"]
    alarm_id: str
    ticker: str
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


class Operation(TypedDict):
    deal_id: str
    revision: int
    op: NotRequired[str]


class OrderCreatedPayload(TypedDict):
    at: NotRequired[str]
    deal_id: str
    order_id: str
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


class PositionOpenedPayload(TypedDict):
    at: NotRequired[str]
    average_price: NotRequired[str]
    deal_id: str
    quantity: NotRequired[int]
    realized_pnl: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    symbol: NotRequired[str]


class Right(TypedDict):
    const: DealV1DecimalString


class Risk(TypedDict):
    take_profit: NotRequired[DealV1ExitBlock]
    stop_loss: NotRequired[DealV1ExitBlock]


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


class SessionHelloPayload(TypedDict):
    bf_id: str
    dry_run: NotRequired[bool]
    margin_trading: NotRequired[bool]
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


class Summary(TypedDict):
    entry_avg_price: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    exit_avg_price: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    realized_pnl: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]
    total_commission: NotRequired[
        str | float | int | bool | dict[str, Any] | list[Any] | None
    ]


class TradePlanV1(TypedDict):
    """
    AFB-side single-entry / single-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v1. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `schema` is optional: its absence means afb.tradeplan.v1 (compatibility with frontends older than the tradeplan schema itself).
    """

    id: str
    ticker: str
    status: NotRequired[Literal["new", "active", "published", "closed", "expired"]]
    direction: NotRequired[Literal["long", "short"]]
    schema: NotRequired[Literal["afb.tradeplan.v1"]]
    activated_at: NotRequired[str]
    closed_at: NotRequired[str]
    entry_condition: TradeplanV1EntryCondition
    quantity_value: NotRequired[float | None]
    quantity_mode: NotRequired[
        Literal["lots", "margin", "balance_pct", "risk_currency", "risk_factor"]
    ]
    take_profit: NotRequired[TradeplanV1Condition | None]
    stop_loss: NotRequired[TradeplanV1Condition | None]
    deal_id: NotRequired[str]
    connector: NotRequired[str]
    delivery_at: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


class TradePlanV2(TypedDict):
    """
    AFB-side multi-entry / multi-exit trade plan template, persisted per-user and compiled by AFB into an afb.deal.v2. This is NOT an AsyncAPI wire message — it never crosses the AFB<->BF channel. `direction` (long/short) is the single source of truth for position bias, at plan level — entry legs do not carry a per-leg side (a list of entries with independent buy/sell sides has no defined execution semantics for one deal). Conditions are deal.v2-compatible nodes — price legs carry an explicit `op` (touch/above/below/breakout/breakdown/crossing), `op` omitted on a price leg means touch (accepted for back-compat with old plans); indicator legs may omit `op`, derived from direction/scope at compile time — with one extension: the `right` side of a condition may be a `primitiveRef` (`{"primitive_id": "..."}`), a reference to a chart line primitive that AFB resolves to a decimal `const` at compile time. The full left/right pairing matrix (price/quote const-only, indicator/dataset const-or-same-kind) is enforced after compilation by deal.v2.json and by BF, not here — this schema deliberately stays loose to accommodate primitiveRef.
    """

    id: str
    ticker: str
    status: NotRequired[Literal["new", "active", "published", "closed", "expired"]]
    direction: Literal["long", "short"]
    schema: Literal["afb.tradeplan.v2"]
    activated_at: NotRequired[str]
    closed_at: NotRequired[str]
    entries: list[Entry1]
    stop_loss: NotRequired[TradeplanV2TpExitList]
    take_profit: NotRequired[TradeplanV2TpExitList]
    sizing: DealV1Sizing
    deal_id: NotRequired[str]
    connector: NotRequired[str]
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
    left: ConditionV1PriceExpr | ConditionV1IndicatorExpr | ConditionV1DatasetExpr
    right: (
        ConditionV1RightConst
        | ConditionV1IndicatorExpr
        | ConditionV1DatasetExpr
        | TradeplanV2PrimitiveRef
    )


class TradeplanV2TpExitListItem(TypedDict):
    percent: NotRequired[DealV1DecimalString]
    condition: TradeplanV2TpConditionNode


TradeplanV2TpExitList: TypeAlias = list[TradeplanV2TpExitListItem]


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
