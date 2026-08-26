"""spec/schemas/iss/ — MOEX ISS market/series descriptors AFB's
backend/integrations/iss_registry.py reads from the installed package.

ISS never crosses the AFB<->BF wire and is not part of spec/asyncapi.yaml
(same standing as notification.*.vN.json) — canon lives here purely so it
ships inside the installed afb_bf_protocol package (see iss_registry.py's own
docstring for why). These tests only check the canon is internally
consistent; AFB's own test suite covers what its registry does with it."""
from __future__ import annotations

import json

import pytest

from conftest import SPEC_SCHEMAS

ISS_DIR = SPEC_SCHEMAS / "iss"
MARKETS_DIR = ISS_DIR / "markets"


def _load(path):
    return json.loads(path.read_text())


def _market_files():
    return sorted(MARKETS_DIR.glob("*.json"))


@pytest.mark.parametrize("path", _market_files(), ids=lambda p: p.name)
def test_descriptor_matches_meta_schema(path, registry):
    from jsonschema import Draft202012Validator

    meta = _load(ISS_DIR / "meta" / "iss.market.v1.json")
    Draft202012Validator(meta, registry=registry).validate(_load(path))


@pytest.mark.parametrize("path", _market_files(), ids=lambda p: p.name)
def test_descriptor_id_matches_its_own_path(path):
    doc = _load(path)
    expected = (
        "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/iss/markets/"
        f"{path.name}"
    )
    assert doc["$id"] == expected


@pytest.mark.parametrize("path", _market_files(), ids=lambda p: p.name)
def test_every_named_column_is_in_the_dictionary(path):
    doc = _load(path)
    dictionary = _load(ISS_DIR / "iss.columns.v1.json")["columns"]
    for column in doc.get("x-iss-columns", {}):
        assert column in dictionary, f"{path.name}: {column!r} missing from iss.columns.v1.json"


def test_columns_dictionary_is_well_formed():
    dictionary = _load(ISS_DIR / "iss.columns.v1.json")["columns"]
    for name, spec in dictionary.items():
        assert "iss_type" in spec, name


def test_futures_series_key_is_required_and_maps_to_series_name():
    dictionary = _load(ISS_DIR / "iss.columns.v1.json")["columns"]
    descriptor = _load(MARKETS_DIR / "futures_series.json")
    assert descriptor["x-iss-columns"]["asset_code"]["required"] is True
    assert descriptor["x-iss-columns"]["name"]["required"] is True
    assert dictionary["name"]["target"] == "series_name"


def test_options_markets_are_architecture_only_in_the_canon():
    """The descriptors exist and validate; nothing in AFB's own
    market_source.yaml enables them (see AFB's test_iss_registry.py)."""
    for name, key in (("options.json", "ASSETCODE"), ("options_series.json", "asset_code")):
        doc = _load(MARKETS_DIR / name)
        assert doc["x-iss-columns"][key]["required"] is True
