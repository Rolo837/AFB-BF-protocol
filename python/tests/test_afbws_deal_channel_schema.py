"""afbws/deal.channel.v1.json — schema-first deal channel (AFB backend<->AFB
frontend only). Negotiated via auth.support/auth_ok.support; not part of the
afb.execution.v1 AFB<->BF wire. See plans/deal-channel-migration_97a53aa5.plan.md."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

DEAL_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/deal.channel.v1.json"

_TARGET = {
    "bf_id": "bf-main",
    "broker": "finam",
    "instrument": {"exchange": "MOEX", "board": "TQBR", "ticker": "SBER"},
}
_PUBLIC_DEAL_V1 = {
    "schema": "afb.deal.v1",
    "deal_id": "deal-1",
    "revision": 1,
    "target": _TARGET,
    "direction": "long",
    "entry": {"condition": {"node_type": "event", "op": "above", "left": {"source": "price", "field": "last"}, "right": {"const": "100"}}},
    "sizing": {"mode": "lots", "value": "1"},
    "source": {"tradeplan_id": "tp-1"},
}
_SUMMARY = {
    "deal_id": "deal-1",
    "revision": 1,
    "status": "active",
    "execution_phase": "holding",
    "bf_id": "bf-main",
    "tradeplan_id": "tp-1",
    "ticker": "SBER",
    "direction": "long",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}
_DETAIL = {
    **_SUMMARY,
    "deal": _PUBLIC_DEAL_V1,
    "editable_fields": ["sizing"],
}


def _validator(def_name: str, registry):
    """Full-URI $ref so internal cross-refs (dealDetail->publicExecutionDeal,
    errorResponse->errorCode, dealResult->dealSummary/dealDetail) resolve
    against the whole document, same pattern as the alarm/tradeplan channels."""
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{DEAL_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


# --- get ---------------------------------------------------------------

def test_get_request_valid(registry):
    msg = {"channel": "deal", "schema": "afbws.deal.get.request.v1", "request_id": "req-1", "deal_id": "deal-1"}
    _validator("getRequest", registry).validate(msg)  # does not raise


def test_get_response_valid(registry):
    msg = {"channel": "deal", "schema": "afbws.deal.get.response.v1", "request_id": "req-1", "item": _DETAIL}
    _validator("getResponse", registry).validate(msg)  # does not raise


def test_get_request_wrong_channel_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "tradeplan", "schema": "afbws.deal.get.request.v1", "request_id": "req-1", "deal_id": "deal-1"}
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_type_field_rejected(registry):
    """No `type` field anywhere on the negotiated channel — see §3 of the plan."""
    from jsonschema import ValidationError

    msg = {"channel": "deal", "schema": "afbws.deal.get.request.v1", "request_id": "req-1", "deal_id": "deal-1", "type": "get"}
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_get_request_missing_request_id_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "deal", "schema": "afbws.deal.get.request.v1", "deal_id": "deal-1"}
    with pytest.raises(ValidationError):
        _validator("getRequest", registry).validate(msg)


def test_deal_detail_rejects_internal_deal_state_fields(registry):
    """dealDetail must never carry persisted-DealState-only data."""
    from jsonschema import ValidationError

    for leak_key, leak_value in (
        ("source_refs", {"draft_tradeplan_id": "tp-1"}),
        ("status_history", []),
        ("event_journal", []),
        ("orders", []),
        ("positions", []),
        ("observed", {}),
    ):
        bad = {**_DETAIL, leak_key: leak_value}
        with pytest.raises(ValidationError):
            _validator("getResponse", registry).validate(
                {"channel": "deal", "schema": "afbws.deal.get.response.v1", "request_id": "req-1", "item": bad}
            )


# --- list ----------------------------------------------------------------

def test_list_request_no_filters_needed(registry):
    msg = {"channel": "deal", "schema": "afbws.deal.list.request.v1", "request_id": "req-1"}
    _validator("listRequest", registry).validate(msg)  # does not raise


def test_list_response_valid(registry):
    msg = {"channel": "deal", "schema": "afbws.deal.list.response.v1", "request_id": "req-1", "items": [_SUMMARY]}
    _validator("listResponse", registry).validate(msg)  # does not raise


def test_list_response_item_is_summary_not_detail_shaped(registry):
    """A dealSummary must not need (nor tolerate) the editor payload fields."""
    from jsonschema import ValidationError

    bad_item = {**_SUMMARY, "deal": _PUBLIC_DEAL_V1}
    msg = {"channel": "deal", "schema": "afbws.deal.list.response.v1", "request_id": "req-1", "items": [bad_item]}
    with pytest.raises(ValidationError):
        _validator("listResponse", registry).validate(msg)


# --- publish ---------------------------------------------------------------

def test_publish_request_valid(registry):
    msg = {
        "channel": "deal",
        "schema": "afbws.deal.publish.request.v1",
        "request_id": "req-1",
        "tradeplan_id": "tp-1",
        "bf_id": "bf-main",
    }
    _validator("publishRequest", registry).validate(msg)  # does not raise


def test_publish_request_inline_data_rejected(registry):
    """No inline plan-like draft on the schema-first channel — only a stored
    tradeplan_id reference (see §2.3 of the migration plan)."""
    from jsonschema import ValidationError

    msg = {
        "channel": "deal",
        "schema": "afbws.deal.publish.request.v1",
        "request_id": "req-1",
        "tradeplan_id": "tp-1",
        "bf_id": "bf-main",
        "data": {"id": "tp-1"},
    }
    with pytest.raises(ValidationError):
        _validator("publishRequest", registry).validate(msg)


def test_publish_request_plural_bf_ids_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "deal",
        "schema": "afbws.deal.publish.request.v1",
        "request_id": "req-1",
        "tradeplan_id": "tp-1",
        "bf_ids": ["bf-main"],
    }
    with pytest.raises(ValidationError):
        _validator("publishRequest", registry).validate(msg)


def test_publish_response_valid(registry):
    msg = {
        "channel": "deal",
        "schema": "afbws.deal.publish.response.v1",
        "request_id": "req-1",
        "results": [{"deal_id": "deal-1", "bf_id": "bf-main", "status": "publishing", "accepted": True, "item": _DETAIL}],
        "accepted": True,
    }
    _validator("publishResponse", registry).validate(msg)  # does not raise


# --- rebind ------------------------------------------------------------

def test_rebind_request_addresses_deal_not_plan(registry):
    msg = {
        "channel": "deal",
        "schema": "afbws.deal.rebind.request.v1",
        "request_id": "req-1",
        "deal_id": "deal-1",
        "bf_id": "bf-backup",
    }
    _validator("rebindRequest", registry).validate(msg)  # does not raise


def test_rebind_request_tradeplan_id_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "deal",
        "schema": "afbws.deal.rebind.request.v1",
        "request_id": "req-1",
        "tradeplan_id": "tp-1",
        "bf_id": "bf-backup",
    }
    with pytest.raises(ValidationError):
        _validator("rebindRequest", registry).validate(msg)


# --- operation ---------------------------------------------------------

@pytest.mark.parametrize("action", ["activate", "pause", "resume", "cancel", "reconcile", "delete"])
def test_operation_item_accepts_every_enum_action(registry, action):
    item = {"deal_id": "deal-1", "action": action}
    _validator("operationItem", registry).validate(item)  # does not raise


@pytest.mark.parametrize("action", ["close", "archive"])
def test_operation_item_unknown_action_rejected(registry, action):
    """'archive' was removed as a schema-valid action (was runtime-reserved,
    never actually wired to any handler) — see tradeplan/deal separation Фаза B1."""
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("operationItem", registry).validate({"deal_id": "deal-1", "action": action})


def test_operation_item_cancel_open_orders_only_for_cancel(registry):
    from jsonschema import ValidationError

    ok = {"deal_id": "deal-1", "action": "cancel", "cancel_open_orders": True}
    _validator("operationItem", registry).validate(ok)  # does not raise

    bad = {"deal_id": "deal-1", "action": "pause", "cancel_open_orders": True}
    with pytest.raises(ValidationError):
        _validator("operationItem", registry).validate(bad)


def test_operation_request_response_valid(registry):
    req = {
        "channel": "deal",
        "schema": "afbws.deal.operation.request.v1",
        "request_id": "req-1",
        "items": [{"deal_id": "deal-1", "action": "pause"}, {"deal_id": "deal-2", "action": "resume"}],
    }
    _validator("operationRequest", registry).validate(req)  # does not raise

    resp = {
        "channel": "deal",
        "schema": "afbws.deal.operation.response.v1",
        "request_id": "req-1",
        "results": [
            {"deal_id": "deal-1", "bf_id": "bf-main", "status": "paused", "accepted": True},
            {"deal_id": "deal-2", "bf_id": "bf-main", "status": "active", "accepted": False, "code": "unsupported_action"},
        ],
        "accepted": True,
    }
    _validator("operationResponse", registry).validate(resp)  # does not raise


# --- amend (phase B) ----------------------------------------------------

def test_amend_request_response_valid(registry):
    req = {
        "channel": "deal",
        "schema": "afbws.deal.amend.request.v1",
        "request_id": "req-1",
        "deal_id": "deal-1",
        "deal_edit": {"sizing": {"mode": "lots", "value": "2"}},
        "base_revision": 3,
    }
    _validator("amendRequest", registry).validate(req)  # does not raise

    resp = {
        "channel": "deal",
        "schema": "afbws.deal.amend.response.v1",
        "request_id": "req-1",
        "item": _DETAIL,
        "revision": 4,
        "status": "active",
        "accepted": True,
    }
    _validator("amendResponse", registry).validate(resp)  # does not raise


def test_amend_request_rejects_legacy_drop_overrides_key(registry):
    """drop_overrides was removed (was an explicit no-op on both sides) —
    see tradeplan/deal separation Фаза B1."""
    from jsonschema import ValidationError

    req = {
        "channel": "deal",
        "schema": "afbws.deal.amend.request.v1",
        "request_id": "req-1",
        "deal_id": "deal-1",
        "drop_overrides": ["stop_loss"],
    }
    with pytest.raises(ValidationError):
        _validator("amendRequest", registry).validate(req)


# --- error ---------------------------------------------------------------

@pytest.mark.parametrize(
    "code",
    ["not_found", "invalid_schema", "validation_error", "forbidden", "conflict", "bf_offline", "unsupported_action", "internal_error"],
)
def test_error_response_known_codes(registry, code):
    msg = {"channel": "deal", "schema": "afbws.deal.error.response.v1", "request_id": "req-1", "code": code, "message": "x"}
    _validator("errorResponse", registry).validate(msg)  # does not raise


def test_error_response_conflict_carries_authoritative_item(registry):
    msg = {
        "channel": "deal",
        "schema": "afbws.deal.error.response.v1",
        "request_id": "req-1",
        "code": "conflict",
        "message": "stale revision",
        "item": _DETAIL,
    }
    _validator("errorResponse", registry).validate(msg)  # does not raise


# --- deal.record / deal.pnl / deal.event pushes (updated, referenced by this channel) ---

def test_record_push_valid_and_is_public_projection(registry):
    from jsonschema import Draft202012Validator

    msg = {"channel": "deal", "schema": "afbws.deal.record.push.v1", "deal_id": "deal-1", "bf_id": "bf-main", "item": _DETAIL}
    Draft202012Validator(
        {"$ref": "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/deal.record.v1.json"}, registry=registry
    ).validate(msg)  # does not raise


def test_record_push_has_no_request_id_property(registry):
    resolved = registry["https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/deal.record.v1.json"]
    assert "request_id" not in resolved.contents["properties"]


def test_pnl_push_has_no_trend_field(registry):
    resolved = registry["https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/deal.pnl.v1.json"]
    assert "trend" not in resolved.contents["properties"]["data"]["properties"]


def test_event_push_category_enum(registry):
    from jsonschema import Draft202012Validator, ValidationError

    v = Draft202012Validator(
        {"$ref": "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/deal.event.v1.json"}, registry=registry
    )
    msg = {
        "channel": "deal",
        "schema": "afbws.deal.event.push.v1",
        "deal_id": "deal-1",
        "bf_id": "bf-main",
        "category": "deal",
        "event": "amended",
        "logged_at": "2026-01-01T00:00:00Z",
        "data": {"anything": "goes"},
    }
    v.validate(msg)  # does not raise
    with pytest.raises(ValidationError):
        v.validate({**msg, "category": "not_a_real_category"})


# --- triggered push / ack ------------------------------------------------

def test_triggered_push_valid(registry):
    msg = {
        "channel": "deal",
        "schema": "afbws.deal.triggered.push.v1",
        "events": [
            {
                "schema": "afb.deal.trigger.v1",
                "notification_id": "deal-1:status_changed:t1",
                "deal_id": "deal-1",
                "bf_id": "bf-main",
                "event": "status_changed",
                "created_at": "2026-01-01T00:00:00Z",
                "data": {"status": "active"},
            }
        ],
    }
    _validator("triggeredPush", registry).validate(msg)  # does not raise


def test_triggered_push_has_no_request_id_property():
    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "deal.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    assert "request_id" not in doc["$defs"]["triggeredPush"]["properties"]


def test_ack_request_and_response_valid(registry):
    req = {
        "channel": "deal",
        "schema": "afbws.deal.ack.request.v1",
        "request_id": "req-1",
        "events": [{"schema": "afb.deal.trigger_ack.v1", "notification_id": "deal-1:status_changed:t1"}],
    }
    _validator("ackRequest", registry).validate(req)  # does not raise

    resp = {
        "channel": "deal",
        "schema": "afbws.deal.ack.response.v1",
        "request_id": "req-1",
        "results": [{"schema": "afbws.deal.ack_result.v1", "notification_id": "deal-1:status_changed:t1", "status": "ok"}],
    }
    _validator("ackResponse", registry).validate(resp)  # does not raise


# --- dealSummary/dealDetail: realized_pnl, sizing/execution_policy/market ---

def test_summary_and_detail_optional_realized_pnl(registry):
    with_pnl = {**_SUMMARY, "realized_pnl": {"value": "123.45", "degraded": None}}
    _validator("dealSummary", registry).validate(with_pnl)  # does not raise
    _validator("dealSummary", registry).validate(_SUMMARY)  # absent is also valid


def test_realized_pnl_degraded_value_must_be_null(registry):
    from jsonschema import ValidationError

    bad = {"value": "1", "degraded": "missing_price"}
    with pytest.raises(ValidationError):
        _validator("dealRealizedPnl", registry).validate(bad)
    ok = {"value": None, "degraded": "missing_price"}
    _validator("dealRealizedPnl", registry).validate(ok)  # does not raise


def test_realized_pnl_unknown_degraded_code_rejected(registry):
    from jsonschema import ValidationError

    with pytest.raises(ValidationError):
        _validator("dealRealizedPnl", registry).validate({"value": None, "degraded": "totally_unknown"})


def test_summary_accepts_sizing_execution_policy_market_and_broker_sizing(registry):
    """dealSummary now carries the user-set sizing {mode,value} and
    execution_policy (whole $ref, same as the compiled deal) alongside the
    pre-existing broker_sizing projection — see tradeplan/deal separation
    Фаза B1. All four are optional."""
    full = {
        **_SUMMARY,
        "market": "futures",
        "sizing": {"mode": "risk_factor", "value": "2"},
        "execution_policy": {"execution_mode": "hybrid", "max_spread_steps": 3},
        "broker_sizing": {"lots": 1, "required_cash": "1000", "resolved_lots": 1},
    }
    _validator("dealSummary", registry).validate(full)  # does not raise


def test_summary_sizing_rejects_broker_shaped_object(registry):
    """sizing is the canonical {mode,value} $ref — a broker_sizing-shaped
    object under the `sizing` key (the old, pre-rename meaning) must be
    rejected, not silently accepted as something else."""
    from jsonschema import ValidationError

    bad = {**_SUMMARY, "sizing": {"lots": 1, "required_cash": "1000"}}
    with pytest.raises(ValidationError):
        _validator("dealSummary", registry).validate(bad)


def test_detail_does_not_require_overrides_key(registry):
    """overrides was removed entirely (dead Phase-B-cancelled design, always
    `{}` in practice) — dealDetail must validate without it."""
    _validator("dealDetail", registry).validate(_DETAIL)  # does not raise


def test_detail_rejects_overrides_key(registry):
    """overrides is no longer a declared property — additionalProperties:
    false must reject it outright, not silently accept and ignore."""
    from jsonschema import ValidationError

    bad = {**_DETAIL, "overrides": {}}
    with pytest.raises(ValidationError):
        _validator("dealDetail", registry).validate(bad)


# --- no `type` field anywhere ------------------------------------------

def test_no_message_def_declares_a_type_property():
    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "deal.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"
