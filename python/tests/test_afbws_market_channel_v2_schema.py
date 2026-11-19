"""afbws/market.channel.v2.json — registry fields (`<source>.<field>[@median(N)]`),
chart slots, fixed quote columns. One schema id per message; validated against
the channel's root (oneOf), its $defs and the shipped examples."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/market.channel.v2.json"
EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "market_channel_v2"
CANDLES = {
    "source": "candles",
    "columns": ["time", "open", "high", "low", "close", "volume"],
    "rows": [[1795000800, 1.0, 2.0, 0.5, 1.5, 10]],
}


def _validator(registry, def_name: str | None = None):
    from jsonschema import Draft202012Validator

    ref = ID if def_name is None else f"{ID}#/$defs/{def_name}"
    return Draft202012Validator({"$ref": ref}, registry=registry)


def _msg(op: str, **extra):
    return {"channel": "market", "schema": f"afbws.market.{op}.v2", **extra}


def _get(**extra):
    base = {"request_id": "r", "target": "series", "slot": 0, "instrument_key": "MISX:TQBR:SBER",
            "period": "5min", "start_date": "2026-11-01"}
    base.update(extra)
    return _msg("get", **base)


def _series(**extra):
    base = {"slot": 0, "instrument_key": "MISX:TQBR:SBER", "period": "5min", "mode": "replace",
            "tables": [copy.deepcopy(CANDLES)]}
    base.update(extra)
    return _msg("series", **base)


def _bad(v, doc):
    with pytest.raises(Exception):
        v.validate(doc)


def test_capability_id_declared():
    from afb_bf_protocol import MARKET_CHANNEL_V2

    assert MARKET_CHANNEL_V2 == "afbws.market.channel.v2"


def test_examples_validate(registry):
    root = _validator(registry)
    files = sorted(EXAMPLES.glob("*.json"))
    assert len(files) >= 15
    for path in files:
        root.validate(json.loads(path.read_text(encoding="utf-8")))


@pytest.mark.parametrize("field", [
    "trades.val_b", "positions.openinterest", "trades.val_b@median(1)", "trades.val_b@median(31)",
    "trades.val_b@median(999)", "obstats.imbalance_vol@median(7)",
])
def test_get_series_valid_fields(registry, field):
    _validator(registry, "get").validate(_get(fields=[field]))


@pytest.mark.parametrize("field", [
    "trades.val_b@median(0)", "trades.val_b@median(1000)", "trades.val_b@median(x)", "trades.val_b@median()",
    "trades.val_b@median(05)", "trades.val_b@mean(3)", "val_b", "Trades.val_b", "trades.val_b@median(3)@median(3)",
    "trades.", ".val_b", "trades.val-b",
])
def test_get_series_bad_fields(registry, field):
    _bad(_validator(registry, "get"), _get(fields=[field]))


def test_get_series_fields_shape(registry):
    v = _validator(registry, "get")
    v.validate(_get())  # candles only
    _bad(v, _get(fields=[]))
    _bad(v, _get(fields=["trades.val_b", "trades.val_b"]))


def test_get_series_requires_slot_and_core(registry):
    v = _validator(registry, "get")
    v.validate(_get(slot=1, end_date="2026-11-10"))
    for key in ("slot", "instrument_key", "period", "start_date"):
        doc = _get()
        del doc[key]
        _bad(v, doc)
    _bad(v, _get(slot=2))
    _bad(v, _get(slot="0"))
    _bad(v, _get(period="1week"))
    _bad(v, _get(instrument_keys=["MISX:TQBR:SBER"]))


def test_get_quotes_and_fields_targets(registry):
    v = _validator(registry, "get")
    v.validate(_msg("get", request_id="r", target="quotes"))
    v.validate(_msg("get", request_id="r", target="quotes", instrument_keys=["MISX:TQBR:SBER"]))
    _bad(v, _msg("get", request_id="r", target="quotes", slot=0))
    _bad(v, _msg("get", request_id="r", target="quotes", fields=["trades.val_b"]))
    _bad(v, _msg("get", request_id="r", target="quotes", period="1d"))
    _bad(v, _msg("get", request_id="r", target="quotes", instrument_keys=["a"] * 2 + ["b"]))  # duplicates
    v.validate(_msg("get", request_id="r", target="fields", instrument_key="MISX:TQBR:SBER"))
    v.validate(_msg("get", request_id="r", target="fields"))  # no instrument_key: full catalog
    _bad(v, _msg("get", request_id="r", target="fields", instrument_key="MISX:TQBR:SBER", slot=0))
    _bad(v, _msg("get", request_id="r", target="fields", instrument_key="MISX:TQBR:SBER", fields=["trades.val_b"]))


def test_get_unknown_target_and_extras(registry):
    v = _validator(registry, "get")
    _bad(v, _msg("get", request_id="r", target="snapshot"))
    _bad(v, _msg("get", request_id="r", target="series", slot=0, instrument_key="MISX:TQBR:SBER",
                 period="5min", start_date="2026-11-01", kinds=["candles"]))  # v1 leftover
    _bad(_validator(registry, "get"), _msg("get", target="quotes"))  # request_id required


def test_series_candles_first(registry):
    v = _validator(registry, "series")
    v.validate(_series())
    data = {"source": "trades", "columns": ["time", "val_b@median(5)"], "rows": [[1795000800, None]]}
    v.validate(_series(tables=[copy.deepcopy(CANDLES), data]))
    v.validate(_series(request_id="r", mode="merge", slot=1))
    _bad(v, _series(tables=[]))
    _bad(v, _series(tables=[data]))  # tables[0] must be candles
    _bad(v, _series(tables=[data, copy.deepcopy(CANDLES)]))
    _bad(v, _series(tables=[copy.deepcopy(CANDLES), copy.deepcopy(CANDLES)]))  # candles only at [0]
    short = copy.deepcopy(CANDLES)
    short["columns"] = ["time", "close"]
    short["rows"] = [[1795000800, 1.5]]
    _bad(v, _series(tables=[short]))


def test_series_requires_slot_and_mode(registry):
    v = _validator(registry, "series")
    for key in ("slot", "instrument_key", "period", "mode", "tables"):
        doc = _series()
        del doc[key]
        _bad(v, doc)
    _bad(v, _series(slot=5))
    _bad(v, _series(mode="full"))
    _bad(v, _series(message="partial"))  # no free-text message in v2
    _bad(v, _series(tz="Europe/Moscow"))  # v1 leftovers are gone
    _bad(v, _series(received_at="2026-11-19T10:00:00+03:00"))


def test_series_table_rules(registry):
    v = _validator(registry, "series")

    def with_data(**over):
        t = {"source": "trades", "columns": ["time", "val_b"], "rows": [[1795000800, 1.0]]}
        t.update(over)
        return _series(tables=[copy.deepcopy(CANDLES), t])

    v.validate(with_data(resolved_key="MISX:SBRF"))
    _bad(v, with_data(columns=["val_b", "time"]))  # time first
    _bad(v, with_data(columns=["time", "val_b", "val_b"]))
    _bad(v, with_data(columns=["time", "Val_B"]))
    _bad(v, with_data(columns=["time", "val_b@median(0)"]))
    _bad(v, with_data(source="Trades"))
    _bad(v, with_data(rows=[[1795000800, "x"]]))  # numbers and null only
    _bad(v, with_data(kind="trades"))
    _bad(v, with_data(resolved_key=""))


@pytest.mark.parametrize("reason", ["unknown", "not_applicable", "no_access", "not_supported"])
def test_series_unavailable_reasons(registry, reason):
    _validator(registry, "series").validate(_series(unavailable=[{"field": "trades.x", "reason": reason}]))


def test_series_unavailable_bad(registry):
    v = _validator(registry, "series")
    _bad(v, _series(unavailable=[{"field": "trades.x", "reason": "forbidden"}]))
    _bad(v, _series(unavailable=[{"field": "trades.x"}]))
    _bad(v, _series(unavailable=[{"reason": "unknown"}]))


def test_series_future_times_and_data_status(registry):
    v = _validator(registry, "series")
    v.validate(_series(future_times=[1, 2], data_status={"state": "partial", "source": "x", "reason": "r",
                                                         "since": "2026-11-19T10:00:00+03:00"}))
    _bad(v, _series(data_status={"state": "fresh", "source": "x", "reason": "r", "since": "2026-11-19T10:00:00+03:00"}))
    _bad(v, _series(future_times=["a"]))


def test_quotes_fixed_columns(registry):
    v = _validator(registry, "quotes")
    cols = ["instrument_key", "last", "close", "percent", "volume"]
    v.validate(_msg("quotes", mode="full", columns=cols, rows=[["MISX:TQBR:SBER", 1, None, 0.1, 5]]))
    v.validate(_msg("quotes", mode="update", columns=cols, rows=[]))
    v.validate(_msg("quotes", request_id="r", mode="full", columns=cols, rows=[]))
    _bad(v, _msg("quotes", mode="full", columns=["instrument_key", "last"], rows=[]))
    _bad(v, _msg("quotes", mode="full", columns=cols + ["bid"], rows=[]))
    _bad(v, _msg("quotes", mode="full", columns=["last", "instrument_key", "close", "percent", "volume"], rows=[]))
    _bad(v, _msg("quotes", mode="snapshot", columns=cols, rows=[]))
    _bad(v, _msg("quotes", mode="full", columns=cols, rows=[["MISX:TQBR:SBER", 1, None]]))  # short row
    _bad(v, _msg("quotes", mode="full", columns=cols, rows=[["MISX:TQBR:SBER", "x", None, 0, 0]]))


def test_fields_message(registry):
    v = _validator(registry, "fields")
    ok = _msg("fields", request_id="r", instrument_key="MISX:TQBR:SBER", median_max_days=31,
              sources=[{"source": "trades", "step_sec": 300, "fields": [{"name": "val_b", "median": True, "unit": "rub"}]},
                       {"source": "hhi", "resolved_key": "MISX:RFUD:X", "step_sec": 86400, "fields": []}])
    v.validate(ok)
    for key in ("request_id", "sources", "median_max_days"):
        doc = copy.deepcopy(ok)
        del doc[key]
        _bad(v, doc)
    catalog = copy.deepcopy(ok)
    del catalog["instrument_key"]
    catalog["sources"] = [catalog["sources"][0]]
    v.validate(catalog)  # full catalog reply: no instrument_key
    for patch in ({"median_max_days": 0}, {"sources": [{"source": "trades", "step_sec": 0, "fields": []}]},
                  {"sources": [{"source": "trades", "step_sec": 300, "fields": [{"name": "val_b", "median": True}]}]},
                  {"sources": [{"source": "trades", "step_sec": 300, "fields": [{"name": "val_b", "median": True, "unit": "kg"}]}]},
                  {"sources": [{"source": "trades", "step_sec": 300, "fields": [{"name": "val_b", "median": "yes"}]}]},
                  {"sources": [{"source": "Trades", "step_sec": 300, "fields": []}]}):
        _bad(v, {**ok, **patch})


def test_subscribe_and_subscription(registry):
    s = _validator(registry, "subscribe")
    s.validate(_msg("subscribe", request_id="r", instrument_keys=[]))
    s.validate(_msg("subscribe", request_id="r", instrument_keys=["MISX:TQBR:SBER"]))
    _bad(s, _msg("subscribe", request_id="r"))
    _bad(s, _msg("subscribe", request_id="r", instrument_keys=["a", "a"]))
    _bad(s, _msg("subscribe", request_id="r", instrument_keys=["a"], futures=True))
    r = _validator(registry, "subscription")
    r.validate(_msg("subscription", request_id="r", instrument_keys=["a"],
                    rejected=[{"instrument_key": "b", "code": "not_found"}]))
    _bad(r, _msg("subscription", request_id="r", instrument_keys=["a"], rejected=[{"instrument_key": "b", "code": "busy"}]))
    _bad(r, _msg("subscription", request_id="r", instrument_keys=["a"]))


@pytest.mark.parametrize("code", ["superseded", "busy", "not_supported", "provider_error", "timeout", "internal_error"])
def test_error_codes(registry, code):
    _validator(registry, "error").validate(_msg("error", code=code, message="m"))


def test_error_bad(registry):
    v = _validator(registry, "error")
    _bad(v, _msg("error", code="oops", message="m"))
    _bad(v, _msg("error", code="timeout"))
    _bad(v, _msg("error", code="busy", message="m", retry_after_sec=-1))


def test_v1_error_codes_do_not_widen():
    """provider_error/timeout live only in v2: common errorCode (used by v1) is unchanged."""
    from pathlib import Path as P

    common = json.loads((P(__file__).resolve().parents[2] / "spec/schemas/afbws/common.v1.json").read_text())
    codes = common["$defs"]["errorCode"]["enum"]
    assert "provider_error" not in codes and "timeout" not in codes


def test_source_status(registry):
    v = _validator(registry, "sourceStatus")
    v.validate(_msg("source_status", sources=[{"source": "x", "state": "down", "since": "2026-11-19T10:00:00+03:00", "reason": "r"}]))
    _bad(v, _msg("source_status", sources=[{"source": "x", "state": "weird", "since": "2026-11-19T10:00:00+03:00"}]))


def test_root_oneof_rejects_wrong_schema_id(registry):
    root = _validator(registry)
    _bad(root, _msg("snapshot", mode="full"))
    _bad(root, {"channel": "market", "schema": "afbws.market.get.v1", "request_id": "r", "target": "series"})


@pytest.mark.parametrize("unit", ["price", "lots", "rub", "count", "contracts", "persons", "ratio", "hhi"])
def test_field_entry_units(registry, unit):
    _validator(registry, "fieldEntry").validate({"name": "val_b", "median": False, "unit": unit})


def test_field_entry_unit_required_and_closed(registry):
    v = _validator(registry, "fieldEntry")
    _bad(v, {"name": "val_b", "median": False})
    _bad(v, {"name": "val_b", "median": False, "unit": "percent"})
