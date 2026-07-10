<!-- DO NOT EDIT — generated from spec/asyncapi.yaml by tools/generate.py -->
# Message catalog — afb.execution.v1

Every message is a signed envelope (see `spec/schemas/envelope.json`).
`persisted` = written to BF's `trading_events` journal.

## AFB → BF (commands)

| type | class | persisted | payload schema | example |
|------|-------|-----------|----------------|---------|
| `session.hello_ack` | system |  | `spec/schemas/payloads/session.hello_ack.json` | `examples/session.hello_ack.json` |
| `session.resync_response` | system |  | `spec/schemas/payloads/session.resync_response.json` | `examples/session.resync_response.json` |
| `daemon.capabilities_query` | system |  | `spec/schemas/payloads/daemon.capabilities_query.json` | `examples/daemon.capabilities_query.json` |
| `daemon.restart` | system |  | — | — |
| `broker.get_account` | user |  | — | — |
| `broker.get_orders` | user |  | — | — |
| `broker.get_catalog` | user |  | — | — |
| `broker.get_instrument` | user |  | — | — |
| `broker.resolve_instrument` | user |  | — | — |
| `deal.publish` | user |  | `spec/schemas/payloads/deal.publish.json` | `examples/deal.publish.json` |
| `deal.operation` | user |  | `spec/schemas/payloads/deal.operation.json` | `examples/deal.operation.json` |
| `deal.amend` | user |  | `spec/schemas/payloads/deal.amend.json` | — |
| `deal.resync` | system |  | — | — |
| `deal.signal` | system |  | — | — |

## BF → AFB (events & replies)

| type | class | persisted | payload schema | example |
|------|-------|-----------|----------------|---------|
| `session.hello` | system |  | `spec/schemas/payloads/session.hello.json` | `examples/session.hello.json` |
| `session.heartbeat` | system |  | `spec/schemas/payloads/session.heartbeat.json` | `examples/session.heartbeat.json` |
| `session.resync_request` | system |  | `spec/schemas/payloads/session.resync_request.json` | `examples/session.resync_request.json` |
| `daemon.status` | system | yes | `spec/schemas/payloads/daemon.status.json` | `examples/daemon.status.json` |
| `daemon.capabilities` | system |  | `spec/schemas/payloads/daemon.capabilities.json` | `examples/daemon.capabilities.json` |
| `daemon.error` | system | yes | — | — |
| `broker.account` | user |  | — | — |
| `broker.orders` | user |  | — | — |
| `broker.catalog` | user |  | — | — |
| `broker.instrument` | user |  | — | — |
| `broker.instrument_resolved` | user |  | — | — |
| `broker.position_ledger` | trading | yes | `spec/schemas/payloads/broker.position_ledger.json` | — |
| `deal.accepted` | trading | yes | `spec/schemas/payloads/deal.accepted.json` | `examples/deal.accepted.json` |
| `deal.rejected` | trading | yes | `spec/schemas/payloads/deal.rejected.json` | `examples/deal.rejected.json` |
| `deal.status_changed` | trading | yes | `spec/schemas/payloads/deal.status_changed.json` | `examples/deal.status_changed.json` |
| `deal.archived` | trading | yes | `spec/schemas/payloads/deal.archived.json` | `examples/deal.archived.json` |
| `deal.orders_synced` | trading | yes | — | — |
| `deal.positions_synced` | trading | yes | `spec/schemas/payloads/deal.positions_synced.json` | `examples/deal.positions_synced.json` |
| `deal.report` | trading | yes | `spec/schemas/payloads/deal.report.json` | `examples/deal.report.json` |
| `deal.snapshot` | trading |  | — | — |
| `condition.triggered` | trading | yes | `spec/schemas/payloads/condition.triggered.json` | `examples/condition.triggered.json` |
| `order.created` | trading | yes | `spec/schemas/payloads/order.created.json` | `examples/order.created.json` |
| `order.partially_filled` | trading | yes | — | — |
| `order.filled` | trading | yes | `spec/schemas/payloads/order.filled.json` | `examples/order.filled.json` |
| `order.cancelled` | trading | yes | — | — |
| `order.rejected` | trading | yes | — | — |
| `position.opened` | trading | yes | `spec/schemas/payloads/position.opened.json` | `examples/position.opened.json` |
| `position.changed` | trading | yes | — | — |
| `position.closed` | trading | yes | — | — |

