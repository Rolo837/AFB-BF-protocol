"""afbws/market.channel.v1.json — schema-first market channel (AFB backend<->AFB
frontend only). Negotiated via auth.support/auth_ok.support; not part of the
afb.execution.v1 AFB<->BF wire. Replaces legacy `candles`, `stream/favorites`,
`stream/positions`, `securities/marketdata|futures|positions`. Validated as
dict literals directly against the channel schema's $defs (no fixture files)."""
from __future__ import annotations

import json

import pytest

MARKET_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/market.channel.v1.json"


def _validator(def_name: str, registry):
    """Validate against a named $def of the channel file via a full-URI $ref,
    so its own internal `#/$defs/...` cross-refs (e.g. table's per-kind
    if/then, error's shared errorCode) resolve against the whole document
    rather than the extracted fragment alone."""
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{MARKET_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


def _candles_series_msg(**overrides):
    msg = {
        "channel": "market",
        "schema": "afbws.market.series.v1",
        "request_id": "req-1",
        "instrument_key": "MISX:TQBR:SBER",
        "period": "1min",
        "tz": "Europe/Moscow",
        "received_at": "2026-09-23T10:00:00+03:00",
        "mode": "replace",
        "from": "2026-09-20",
        "to": "2026-09-23",
        "tables": [
            {
                "kind": "candles",
                "columns": ["time", "open", "high", "low", "close", "volume"],
                "rows": [[1758610800, 251.0, 253.5, 250.0, 252.0, 10000]],
            }
        ],
    }
    msg.update(overrides)
    return msg


def _quote_snapshot_msg(**overrides):
    msg = {
        "channel": "market",
        "schema": "afbws.market.snapshot.v1",
        "request_id": "req-2",
        "scope": "get",
        "tz": "Europe/Moscow",
        "received_at": "2026-09-23T10:00:00+03:00",
        "mode": "full",
        "tables": [
            {
                "kind": "quote",
                "columns": ["instrument_key", "last", "close", "bid", "offer"],
                "rows": [["MISX:TQBR:SBER", 252.0, 251.0, 251.9, 252.1]],
            }
        ],
    }
    msg.update(overrides)
    return msg


# --- x-afbws-support-id --------------------------------------------------

def test_x_afbws_support_id():
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "market.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    assert doc["x-afbws-support-id"] == "afbws.market.channel.v1"


def test_no_message_def_declares_a_type_property():
    """New channels forbid `type`: routing is channel+schema only. Enforced
    structurally by additionalProperties:false + the declared properties list
    on every message $def, checked here so a future edit can't reintroduce it."""
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[2] / "spec" / "schemas" / "afbws" / "market.channel.v1.json"
    )
    doc = json.loads(schema_path.read_text())
    for def_name, def_schema in doc["$defs"].items():
        props = def_schema.get("properties", {})
        assert "type" not in props, f"{def_name} must not declare a 'type' property"


# --- table (per-kind columns) ---------------------------------------------

@pytest.mark.parametrize(
    "kind,columns,row_tail",
    [
        ("candles", ["time", "open", "high", "low", "close", "volume"], [1.0, 2.0, 0.5, 1.5, 100]),
        ("positions", ["time", "long", "short", "position", "openinterest"], [10, 5, 5, 15]),
        (
            "positions",
            ["time", "long", "short", "position", "openinterest", "fiz_long", "yur_position"],
            [10, 5, 5, 15, 3, 12],
        ),
        (
            "trades",
            ["time", "trades", "trades_b", "trades_s", "vol", "vol_b", "vol_s", "pr_vwap_b", "pr_vwap_s"],
            [100, 60, 40, 1000, 600, 400, 251.5, 251.2],
        ),
        (
            "hhi",
            [
                "time", "hhi_volume", "hhi_buy", "hhi_sell",
                "hhi_agressive", "hhi_agressive_buy", "hhi_agressive_sell",
                "hhi_passive", "hhi_passive_buy", "hhi_passive_sell",
                "hhi_netflow_buy", "hhi_netflow_sell",
            ],
            [1.0] * 11,
        ),
        ("orders", ["time", "bid", "offer", "delta"], [100, 101, 1]),
        (
            "quote",
            ["instrument_key", "last", "close", "percent", "open", "high", "low", "bid", "offer",
             "lots", "volume", "numtrades", "updated_at"],
            [252.0, 251.0, 0.4, 251.5, 253.0, 250.5, 251.9, 252.1, 1000, 500000, 320, 1758610800],
        ),
        (
            "oi",
            ["instrument_key", "time", "long", "short", "position", "openinterest"],
            [1758610800, 10, 5, 5, 15],
        ),
        (
            "oi_daily",
            [
                "instrument_key", "time", "long", "short", "position", "openinterest",
                "fiz_long", "fiz_short", "yur_long", "yur_short", "fiz_position", "yur_position",
            ],
            [1758585600, 10, 5, 5, 15, 3, 2, 7, 3, 12, 3],
        ),
    ],
)
def test_table_valid_columns_per_kind(registry, kind, columns, row_tail):
    key = "MISX:TQBR:SBER" if kind in ("quote", "oi", "oi_daily") else 1758610800
    row = [key] + row_tail if kind in ("quote", "oi", "oi_daily") else [1758610800] + row_tail
    table = {"kind": kind, "columns": columns, "rows": [row]}
    _validator("table", registry).validate(table)  # does not raise


def test_table_wrong_column_for_kind_rejected(registry):
    from jsonschema import ValidationError

    table = {
        "kind": "candles",
        "columns": ["time", "open", "high", "low", "close", "volume", "bid"],
        "rows": [[1758610800, 1.0, 2.0, 0.5, 1.5, 100, 1]],
    }
    with pytest.raises(ValidationError):
        _validator("table", registry).validate(table)


def test_table_wrong_first_column_series_kind_rejected(registry):
    from jsonschema import ValidationError

    table = {
        "kind": "candles",
        "columns": ["open", "high", "low", "close", "volume", "time"],
        "rows": [[1.0, 2.0, 0.5, 1.5, 100, 1758610800]],
    }
    with pytest.raises(ValidationError):
        _validator("table", registry).validate(table)


def test_table_wrong_first_column_snapshot_kind_rejected(registry):
    from jsonschema import ValidationError

    table = {
        "kind": "quote",
        "columns": ["last", "instrument_key"],
        "rows": [[252.0, "MISX:TQBR:SBER"]],
    }
    with pytest.raises(ValidationError):
        _validator("table", registry).validate(table)


def test_table_unknown_kind_rejected(registry):
    from jsonschema import ValidationError

    table = {"kind": "bogus", "columns": ["time", "open"], "rows": [[1, 2]]}
    with pytest.raises(ValidationError):
        _validator("table", registry).validate(table)


def test_table_snapshot_column_in_series_table_rejected(registry):
    """oi's own allowed columns (e.g. `openinterest`) must not leak into a
    series-only kind like candles, and vice versa: series tables in a
    `series` message are restricted to series kinds by the message def, not
    by `table` alone -- covered by test_series_snapshot_kind_rejected."""
    from jsonschema import ValidationError

    table = {
        "kind": "candles",
        "columns": ["time", "updated_at"],
        "rows": [[1758610800, 1758610800]],
    }
    with pytest.raises(ValidationError):
        _validator("table", registry).validate(table)


# --- series ----------------------------------------------------------------

def test_series_valid_reply(registry):
    _validator("series", registry).validate(_candles_series_msg())  # does not raise


def test_series_valid_push_no_request_id(registry):
    msg = _candles_series_msg(mode="merge")
    del msg["request_id"]
    _validator("series", registry).validate(msg)  # does not raise


def test_series_missing_received_at_rejected(registry):
    from jsonschema import ValidationError

    msg = _candles_series_msg()
    del msg["received_at"]
    with pytest.raises(ValidationError):
        _validator("series", registry).validate(msg)


def test_series_extra_property_rejected(registry):
    from jsonschema import ValidationError

    msg = _candles_series_msg(unexpected="nope")
    with pytest.raises(ValidationError):
        _validator("series", registry).validate(msg)


def test_series_bad_period_enum_rejected(registry):
    from jsonschema import ValidationError

    msg = _candles_series_msg(period="3min")
    with pytest.raises(ValidationError):
        _validator("series", registry).validate(msg)


def test_series_bad_mode_rejected(registry):
    from jsonschema import ValidationError

    msg = _candles_series_msg(mode="update")  # "update" is a snapshot mode, not series
    with pytest.raises(ValidationError):
        _validator("series", registry).validate(msg)


def test_series_snapshot_kind_table_rejected(registry):
    """A snapshot-only kind (quote/oi/oi_daily) must not validate inside a
    `series` message's `tables`."""
    from jsonschema import ValidationError

    msg = _candles_series_msg()
    msg["tables"] = [
        {
            "kind": "quote",
            "columns": ["instrument_key", "last"],
            "rows": [["MISX:TQBR:SBER", 252.0]],
        }
    ]
    with pytest.raises(ValidationError):
        _validator("series", registry).validate(msg)


def test_series_nan_string_is_structurally_a_valid_string_column_value(registry):
    """The wire convention is `null` instead of NaN (see table's description),
    but JSON Schema can't distinguish the string "NaN" from any other string
    at the type level -- this test documents that the ban is a protocol
    convention (server-side), not something this schema enforces itself."""
    msg = _candles_series_msg()
    msg["tables"][0]["rows"][0][-1] = "NaN"
    _validator("series", registry).validate(msg)  # does not raise: string is a valid row value


def test_series_null_instead_of_nan_valid(registry):
    msg = _candles_series_msg()
    msg["tables"][0]["rows"][0][-1] = None
    _validator("series", registry).validate(msg)  # does not raise


# --- snapshot ----------------------------------------------------------------

def test_snapshot_valid_reply(registry):
    _validator("snapshot", registry).validate(_quote_snapshot_msg())  # does not raise


def test_snapshot_valid_push_no_request_id(registry):
    msg = _quote_snapshot_msg(mode="update", scope="quotes")
    del msg["request_id"]
    _validator("snapshot", registry).validate(msg)  # does not raise


def test_snapshot_missing_tz_rejected(registry):
    from jsonschema import ValidationError

    msg = _quote_snapshot_msg()
    del msg["tz"]
    with pytest.raises(ValidationError):
        _validator("snapshot", registry).validate(msg)


def test_snapshot_missing_scope_rejected(registry):
    from jsonschema import ValidationError

    msg = _quote_snapshot_msg()
    del msg["scope"]
    with pytest.raises(ValidationError):
        _validator("snapshot", registry).validate(msg)


def test_snapshot_unknown_scope_rejected(registry):
    from jsonschema import ValidationError

    msg = _quote_snapshot_msg(scope="favorites")
    with pytest.raises(ValidationError):
        _validator("snapshot", registry).validate(msg)


def test_snapshot_scope_quotes_full_valid(registry):
    msg = _quote_snapshot_msg(scope="quotes", mode="full")
    del msg["request_id"]
    _validator("snapshot", registry).validate(msg)  # does not raise


def test_snapshot_scope_quotes_update_valid(registry):
    msg = _quote_snapshot_msg(scope="quotes", mode="update")
    del msg["request_id"]
    _validator("snapshot", registry).validate(msg)  # does not raise


def test_snapshot_scope_futures_full_valid(registry):
    msg = _quote_snapshot_msg(scope="futures", mode="full")
    del msg["request_id"]
    msg["tables"] = [
        {
            "kind": "quote",
            "columns": ["instrument_key", "last"],
            "rows": [["MISX:RFUD:IMOEXF", 3500.0]],
        },
        {
            "kind": "oi",
            "columns": ["instrument_key", "time", "long", "short"],
            "rows": [["MISX:RFUD:IMOEXF", 1758610800, 100, 90]],
        },
        {
            "kind": "oi_daily",
            "columns": ["instrument_key", "time", "long", "short"],
            "rows": [["MISX:RFUD:IMOEXF", 1758585600, 100, 90]],
        },
    ]
    _validator("snapshot", registry).validate(msg)  # does not raise


def test_snapshot_scope_get_requires_no_particular_mode(registry):
    """scope="get" is the one-shot get(target=snapshot) reply; unlike quotes/
    futures it carries request_id by default (see _quote_snapshot_msg) but
    the schema does not itself tie scope to mode or request_id presence."""
    _validator("snapshot", registry).validate(_quote_snapshot_msg(scope="get"))  # does not raise


def test_snapshot_series_kind_table_rejected(registry):
    from jsonschema import ValidationError

    msg = _quote_snapshot_msg()
    msg["tables"] = [
        {
            "kind": "candles",
            "columns": ["time", "open"],
            "rows": [[1758610800, 1.0]],
        }
    ]
    with pytest.raises(ValidationError):
        _validator("snapshot", registry).validate(msg)


def test_snapshot_extra_property_rejected(registry):
    from jsonschema import ValidationError

    msg = _quote_snapshot_msg(unexpected=True)
    with pytest.raises(ValidationError):
        _validator("snapshot", registry).validate(msg)


# --- subscribe / subscription ------------------------------------------------

def test_subscribe_valid(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-3",
        "quotes": {"instrument_keys": ["MISX:TQBR:SBER", "MISX:TQBR:GAZP"]},
        "futures": True,
    }
    _validator("subscribe", registry).validate(msg)  # does not raise


def test_subscribe_quotes_only_valid(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-3b",
        "quotes": {"instrument_keys": ["MISX:TQBR:SBER"]},
    }
    _validator("subscribe", registry).validate(msg)  # does not raise: futures omitted


def test_subscribe_futures_only_valid(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-3c",
        "futures": True,
    }
    _validator("subscribe", registry).validate(msg)  # does not raise: quotes omitted


def test_subscribe_futures_false_valid(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-3d",
        "futures": False,
    }
    _validator("subscribe", registry).validate(msg)  # does not raise


def test_subscribe_empty_body_valid_unsubscribe_all(registry):
    msg = {"channel": "market", "schema": "afbws.market.subscribe.v1", "request_id": "req-4"}
    _validator("subscribe", registry).validate(msg)  # does not raise


def test_subscribe_quotes_instrument_keys_maxitems_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-5",
        "quotes": {"instrument_keys": [f"MISX:TQBR:T{i}" for i in range(2001)]},
    }
    with pytest.raises(ValidationError):
        _validator("subscribe", registry).validate(msg)


def test_subscribe_quotes_missing_instrument_keys_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-6",
        "quotes": {},
    }
    with pytest.raises(ValidationError):
        _validator("subscribe", registry).validate(msg)


def test_subscribe_futures_non_boolean_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-7",
        "futures": "true",
    }
    with pytest.raises(ValidationError):
        _validator("subscribe", registry).validate(msg)


def test_subscribe_removed_series_field_rejected(registry):
    """`series` was removed from subscribe.v1 in revision 2 -- the series
    (candles/dataset) subscription is now driven entirely by `get`
    (target=series), see get.v1's description."""
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-8",
        "series": [{"instrument_key": "MISX:TQBR:SBER", "period": "1min", "kinds": ["candles"]}],
    }
    with pytest.raises(ValidationError):
        _validator("subscribe", registry).validate(msg)


def test_subscribe_removed_snapshot_kinds_field_rejected(registry):
    """The old `snapshot{kinds,instrument_keys}` shape was replaced by
    `quotes{instrument_keys}` (no `kinds`: quotes is always quote rows)."""
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.subscribe.v1",
        "request_id": "req-9",
        "snapshot": {"kinds": ["quote"], "instrument_keys": ["MISX:TQBR:SBER"]},
    }
    with pytest.raises(ValidationError):
        _validator("subscribe", registry).validate(msg)


def test_subscription_valid_with_rejected(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.subscription.v1",
        "request_id": "req-3",
        "quotes": {"instrument_keys": ["MISX:TQBR:SBER"]},
        "futures": True,
        "rejected": [{"instrument_key": "MISX:BOGUS:XXX", "code": "not_found", "message": "unknown instrument"}],
    }
    _validator("subscription", registry).validate(msg)  # does not raise


def test_subscription_futures_false_and_no_quotes_valid(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.subscription.v1",
        "request_id": "req-3e",
        "futures": False,
        "rejected": [],
    }
    _validator("subscription", registry).validate(msg)  # does not raise: quotes omitted means empty scope


def test_subscription_missing_rejected_field_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.subscription.v1",
        "request_id": "req-3",
        "futures": False,
    }
    with pytest.raises(ValidationError):
        _validator("subscription", registry).validate(msg)


def test_subscription_missing_futures_rejected(registry):
    """`futures` is required in subscription.v1 -- it always reflects the
    accepted state, even when the subscribe request omitted it."""
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.subscription.v1",
        "request_id": "req-3",
        "rejected": [],
    }
    with pytest.raises(ValidationError):
        _validator("subscription", registry).validate(msg)


# --- get ---------------------------------------------------------------------

def test_get_series_valid(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.get.v1",
        "request_id": "req-7",
        "target": "series",
        "instrument_key": "MISX:TQBR:SBER",
        "period": "1min",
        "kinds": ["candles"],
        "start_date": "2026-09-01",
    }
    _validator("get", registry).validate(msg)  # does not raise


def test_get_series_missing_start_date_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.get.v1",
        "request_id": "req-7",
        "target": "series",
        "instrument_key": "MISX:TQBR:SBER",
        "period": "1min",
        "kinds": ["candles"],
    }
    with pytest.raises(ValidationError):
        _validator("get", registry).validate(msg)


def test_get_series_with_snapshot_only_field_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.get.v1",
        "request_id": "req-7",
        "target": "series",
        "instrument_key": "MISX:TQBR:SBER",
        "period": "1min",
        "kinds": ["candles"],
        "start_date": "2026-09-01",
        "instrument_keys": ["MISX:TQBR:SBER"],
    }
    with pytest.raises(ValidationError):
        _validator("get", registry).validate(msg)


def test_get_series_wrong_kinds_for_target_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.get.v1",
        "request_id": "req-7",
        "target": "series",
        "instrument_key": "MISX:TQBR:SBER",
        "period": "1min",
        "kinds": ["quote"],
        "start_date": "2026-09-01",
    }
    with pytest.raises(ValidationError):
        _validator("get", registry).validate(msg)


def test_get_snapshot_valid_all_instruments(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.get.v1",
        "request_id": "req-8",
        "target": "snapshot",
        "kinds": ["quote", "oi"],
    }
    _validator("get", registry).validate(msg)  # does not raise: instrument_keys omitted means "all"


def test_get_snapshot_valid_with_instrument_keys(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.get.v1",
        "request_id": "req-8",
        "target": "snapshot",
        "kinds": ["quote"],
        "instrument_keys": ["MISX:TQBR:SBER"],
    }
    _validator("get", registry).validate(msg)  # does not raise


def test_get_snapshot_with_series_only_field_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.get.v1",
        "request_id": "req-8",
        "target": "snapshot",
        "kinds": ["quote"],
        "instrument_key": "MISX:TQBR:SBER",
    }
    with pytest.raises(ValidationError):
        _validator("get", registry).validate(msg)


def test_get_missing_target_rejected(registry):
    from jsonschema import ValidationError

    msg = {"channel": "market", "schema": "afbws.market.get.v1", "request_id": "req-9"}
    with pytest.raises(ValidationError):
        _validator("get", registry).validate(msg)


# --- error -----------------------------------------------------------------

def test_error_valid(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.error.v1",
        "request_id": "req-10",
        "code": "not_found",
        "message": "Instrument not found",
    }
    _validator("error", registry).validate(msg)  # does not raise


def test_error_unknown_code_rejected(registry):
    from jsonschema import ValidationError

    msg = {
        "channel": "market",
        "schema": "afbws.market.error.v1",
        "code": "totally_unknown",
        "message": "x",
    }
    with pytest.raises(ValidationError):
        _validator("error", registry).validate(msg)


def test_error_request_id_optional(registry):
    msg = {
        "channel": "market",
        "schema": "afbws.market.error.v1",
        "code": "bf_offline",
        "message": "no broker connection",
    }
    _validator("error", registry).validate(msg)  # does not raise


# --- instrument_key regression (common.v1.json#/$defs/instrumentKey) ---------

def test_instrument_key_empty_string_rejected(registry):
    from jsonschema import ValidationError

    msg = _candles_series_msg(instrument_key="")
    with pytest.raises(ValidationError):
        _validator("series", registry).validate(msg)


def test_root_oneof_dispatches_each_message_kind(registry):
    """Sanity check that the whole-file root oneOf (channel+schema routing,
    no `type` field) accepts one example of each top-level message kind."""
    from jsonschema import Draft202012Validator

    root = Draft202012Validator({"$ref": MARKET_CHANNEL_ID}, registry=registry)
    root.validate(_candles_series_msg())
    root.validate(_quote_snapshot_msg())
    root.validate({"channel": "market", "schema": "afbws.market.subscribe.v1", "request_id": "r"})
    root.validate(
        {
            "channel": "market",
            "schema": "afbws.market.subscription.v1",
            "request_id": "r",
            "futures": False,
            "rejected": [],
        }
    )
    root.validate(
        {
            "channel": "market",
            "schema": "afbws.market.get.v1",
            "request_id": "r",
            "target": "snapshot",
            "kinds": ["quote"],
        }
    )
    root.validate(
        {
            "channel": "market",
            "schema": "afbws.market.error.v1",
            "code": "internal_error",
            "message": "boom",
        }
    )
