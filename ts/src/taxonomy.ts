// DO NOT EDIT BY HAND — regenerated from `spec/asyncapi.yaml` by
// `tools/generate.py` (the message tags `class:*` / `dir:*` / `persisted`).
// Edit the spec, then run `afb-bf-protocol-generate`.

export type SupportedMarket = "stock" | "futures" | "currency";
export const SUPPORTED_MARKETS: ReadonlySet<string> = new Set([
  "stock",
  "futures",
  "currency",
]);

export type MessageClass = "system" | "user" | "trading";
export type MessageDirection = "afb2bf" | "bf2afb";

export interface MessageMeta {
  readonly message_class: MessageClass;
  readonly direction: MessageDirection;
  readonly category: string;
  readonly event: string;
  readonly persists_on_bf: boolean;
}

export function splitCategoryType(messageType: string): [string, string] {
  const dot = messageType.indexOf(".");
  if (dot <= 0 || dot === messageType.length - 1) {
    throw new Error(`Invalid message type ${JSON.stringify(messageType)}, expected 'category.type'`);
  }
  return [messageType.slice(0, dot), messageType.slice(dot + 1)];
}

export const MESSAGE_REGISTRY = {
  "session.hello": {
    message_class: "system",
    direction: "bf2afb",
    category: "session",
    event: "hello",
    persists_on_bf: false,
  },
  "session.enroll_request": {
    message_class: "system",
    direction: "bf2afb",
    category: "session",
    event: "enroll_request",
    persists_on_bf: false,
  },
  "session.enroll_response": {
    message_class: "system",
    direction: "afb2bf",
    category: "session",
    event: "enroll_response",
    persists_on_bf: false,
  },
  "session.reenroll_request": {
    message_class: "system",
    direction: "afb2bf",
    category: "session",
    event: "reenroll_request",
    persists_on_bf: false,
  },
  "session.heartbeat": {
    message_class: "system",
    direction: "bf2afb",
    category: "session",
    event: "heartbeat",
    persists_on_bf: false,
  },
  "session.resync_request": {
    message_class: "system",
    direction: "bf2afb",
    category: "session",
    event: "resync_request",
    persists_on_bf: false,
  },
  "session.hello_ack": {
    message_class: "system",
    direction: "afb2bf",
    category: "session",
    event: "hello_ack",
    persists_on_bf: false,
  },
  "session.resync_response": {
    message_class: "system",
    direction: "afb2bf",
    category: "session",
    event: "resync_response",
    persists_on_bf: false,
  },
  "daemon.status": {
    message_class: "system",
    direction: "bf2afb",
    category: "daemon",
    event: "status",
    persists_on_bf: true,
  },
  "daemon.capabilities": {
    message_class: "system",
    direction: "bf2afb",
    category: "daemon",
    event: "capabilities",
    persists_on_bf: false,
  },
  "daemon.error": {
    message_class: "system",
    direction: "bf2afb",
    category: "daemon",
    event: "error",
    persists_on_bf: true,
  },
  "daemon.capabilities_query": {
    message_class: "system",
    direction: "afb2bf",
    category: "daemon",
    event: "capabilities_query",
    persists_on_bf: false,
  },
  "daemon.restart": {
    message_class: "system",
    direction: "afb2bf",
    category: "daemon",
    event: "restart",
    persists_on_bf: false,
  },
  "broker.get_account": {
    message_class: "user",
    direction: "afb2bf",
    category: "broker",
    event: "get_account",
    persists_on_bf: false,
  },
  "broker.get_orders": {
    message_class: "user",
    direction: "afb2bf",
    category: "broker",
    event: "get_orders",
    persists_on_bf: false,
  },
  "broker.get_catalog": {
    message_class: "user",
    direction: "afb2bf",
    category: "broker",
    event: "get_catalog",
    persists_on_bf: false,
  },
  "broker.get_instrument": {
    message_class: "user",
    direction: "afb2bf",
    category: "broker",
    event: "get_instrument",
    persists_on_bf: false,
  },
  "broker.resolve_instrument": {
    message_class: "user",
    direction: "afb2bf",
    category: "broker",
    event: "resolve_instrument",
    persists_on_bf: false,
  },
  "broker.account": {
    message_class: "user",
    direction: "bf2afb",
    category: "broker",
    event: "account",
    persists_on_bf: false,
  },
  "broker.orders": {
    message_class: "user",
    direction: "bf2afb",
    category: "broker",
    event: "orders",
    persists_on_bf: false,
  },
  "broker.catalog": {
    message_class: "user",
    direction: "bf2afb",
    category: "broker",
    event: "catalog",
    persists_on_bf: false,
  },
  "broker.instrument": {
    message_class: "user",
    direction: "bf2afb",
    category: "broker",
    event: "instrument",
    persists_on_bf: false,
  },
  "broker.instrument_resolved": {
    message_class: "user",
    direction: "bf2afb",
    category: "broker",
    event: "instrument_resolved",
    persists_on_bf: false,
  },
  "broker.position_ledger": {
    message_class: "trading",
    direction: "bf2afb",
    category: "broker",
    event: "position_ledger",
    persists_on_bf: true,
  },
  "deal.publish": {
    message_class: "user",
    direction: "afb2bf",
    category: "deal",
    event: "publish",
    persists_on_bf: false,
  },
  "deal.operation": {
    message_class: "user",
    direction: "afb2bf",
    category: "deal",
    event: "operation",
    persists_on_bf: false,
  },
  "deal.amend": {
    message_class: "user",
    direction: "afb2bf",
    category: "deal",
    event: "amend",
    persists_on_bf: false,
  },
  "deal.resync": {
    message_class: "system",
    direction: "afb2bf",
    category: "deal",
    event: "resync",
    persists_on_bf: false,
  },
  "deal.signal": {
    message_class: "system",
    direction: "afb2bf",
    category: "deal",
    event: "signal",
    persists_on_bf: false,
  },
  "deal.accepted": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "accepted",
    persists_on_bf: true,
  },
  "deal.rejected": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "rejected",
    persists_on_bf: true,
  },
  "deal.status_changed": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "status_changed",
    persists_on_bf: true,
  },
  "deal.archived": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "archived",
    persists_on_bf: true,
  },
  "deal.orders_synced": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "orders_synced",
    persists_on_bf: true,
  },
  "deal.positions_synced": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "positions_synced",
    persists_on_bf: true,
  },
  "deal.report": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "report",
    persists_on_bf: true,
  },
  "deal.snapshot": {
    message_class: "trading",
    direction: "bf2afb",
    category: "deal",
    event: "snapshot",
    persists_on_bf: false,
  },
  "condition.triggered": {
    message_class: "trading",
    direction: "bf2afb",
    category: "condition",
    event: "triggered",
    persists_on_bf: true,
  },
  "order.created": {
    message_class: "trading",
    direction: "bf2afb",
    category: "order",
    event: "created",
    persists_on_bf: true,
  },
  "order.partially_filled": {
    message_class: "trading",
    direction: "bf2afb",
    category: "order",
    event: "partially_filled",
    persists_on_bf: true,
  },
  "order.filled": {
    message_class: "trading",
    direction: "bf2afb",
    category: "order",
    event: "filled",
    persists_on_bf: true,
  },
  "order.cancelled": {
    message_class: "trading",
    direction: "bf2afb",
    category: "order",
    event: "cancelled",
    persists_on_bf: true,
  },
  "order.rejected": {
    message_class: "trading",
    direction: "bf2afb",
    category: "order",
    event: "rejected",
    persists_on_bf: true,
  },
  "position.opened": {
    message_class: "trading",
    direction: "bf2afb",
    category: "position",
    event: "opened",
    persists_on_bf: true,
  },
  "position.changed": {
    message_class: "trading",
    direction: "bf2afb",
    category: "position",
    event: "changed",
    persists_on_bf: true,
  },
  "position.closed": {
    message_class: "trading",
    direction: "bf2afb",
    category: "position",
    event: "closed",
    persists_on_bf: true,
  },
} as const satisfies Record<string, MessageMeta>;

export type MessageType = keyof typeof MESSAGE_REGISTRY;

export function isMessageType(value: string): value is MessageType {
  return Object.prototype.hasOwnProperty.call(MESSAGE_REGISTRY, value);
}

export const ALL_MESSAGE_TYPES: readonly MessageType[] = Object.keys(
  MESSAGE_REGISTRY,
) as MessageType[];

export const COMMAND_TYPES: ReadonlySet<MessageType> = new Set(
  ALL_MESSAGE_TYPES.filter((t) => MESSAGE_REGISTRY[t].direction === "afb2bf"),
);

export const BF_EVENT_TYPES: ReadonlySet<MessageType> = new Set(
  ALL_MESSAGE_TYPES.filter((t) => MESSAGE_REGISTRY[t].direction === "bf2afb"),
);

export const PERSISTED_BF_EVENT_TYPES: ReadonlySet<MessageType> = new Set(
  ALL_MESSAGE_TYPES.filter((t) => MESSAGE_REGISTRY[t].persists_on_bf),
);
