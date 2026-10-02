"""afbws/config.channel.v1.json + config.v1.json — schema-first config channel
(AFB backend<->AFB frontend only). Replaces legacy `settings`/`help`/`setup`.
Validated as dict literals against the channel schema's $defs."""
from __future__ import annotations

import pytest

CONFIG_CHANNEL_ID = "https://github.com/Rolo837/AFB-BF-protocol/spec/schemas/afbws/config.channel.v1.json"


def _validator(def_name: str, registry):
    from jsonschema import Draft202012Validator

    return Draft202012Validator({"$ref": f"{CONFIG_CHANNEL_ID}#/$defs/{def_name}"}, registry=registry)


def _msg(op: str, **extra):
    return {"channel": "config", "schema": f"afbws.config.{op}.v1", **extra}


def test_capability_id_declared():
    from afb_bf_protocol import CONFIG_CHANNEL_V1

    assert CONFIG_CHANNEL_V1 == "afbws.config.channel.v1"


_SETTINGS = {
    "profile": {"email": "a@b.c", "notify_telegram": True, "notify_system": False, "sound": "game/coin"},
    "interface": {
        "layout": {"offset_right": 10, "offset_top": 0, "debug_mode": False},
        "snow_mode": False,
        "futures_days_to_expiration": 2,
        "chart_toolbar": {"favorite_timeframes": ["1min"]},
    },
    "dataset": {"positions": {"longColor": "#00ff00", "longPanel": 1}},
    "dashboard": {"cols": 12, "layouts": {"lg": [{"widget": "deals", "x": 0, "y": 0, "w": 4, "h": 3}]}},
    "trade": {"default_risk_pct": 0.5, "notify": {"link": True}, "plan_editor_placement": "modal"},
}


def test_settings_read_request(registry):
    _validator("settings", registry).validate(_msg("settings", request_id="r1"))


def test_settings_write_and_response(registry):
    v = _validator("settings", registry)
    v.validate(_msg("settings", request_id="r1", settings={"interface": {"snow_mode": True}}))
    v.validate(_msg("settings", request_id="r1", settings=_SETTINGS))


def test_settings_push_requires_settings(registry):
    v = _validator("settings", registry)
    v.validate(_msg("settings", settings=_SETTINGS))
    with pytest.raises(Exception):
        v.validate(_msg("settings"))


def test_settings_rejects_legacy_keys(registry):
    v = _validator("settings", registry)
    for legacy in ("me", "service", "limits", "name", "favorites", "indicators"):
        with pytest.raises(Exception):
            v.validate(_msg("settings", request_id="r1", settings={legacy: {}}))


def test_settings_boolean_strict(registry):
    v = _validator("settings", registry)
    with pytest.raises(Exception):
        v.validate(_msg("settings", request_id="r1", settings={"interface": {"snow_mode": "true"}}))


def test_defaults_read_write_push(registry):
    v = _validator("defaults", registry)
    v.validate(_msg("defaults", request_id="r1"))
    v.validate(_msg("defaults", request_id="r1", defaults={"dataset": {"hhi": {}}, "interface": {}}))
    v.validate(_msg("defaults", defaults={"dataset": {}}))
    with pytest.raises(Exception):
        v.validate(_msg("defaults"))  # push without defaults
    with pytest.raises(Exception):
        v.validate(_msg("defaults", request_id="r1", defaults={"trade": {}}))  # not a platform default block


def test_help(registry):
    v = _validator("help", registry)
    v.validate(_msg("help", request_id="r1", section="Alarms"))
    v.validate(_msg("help", request_id="r1", section="Alarms", content="<p>x</p>"))
    for bad in (
        _msg("help", section="Alarms"),  # no request_id
        _msg("help", request_id="r1"),  # no section
        _msg("help", request_id="r1", section="../etc"),
    ):
        with pytest.raises(Exception):
            v.validate(bad)


def test_roles(registry):
    v = _validator("roles", registry)
    v.validate(_msg("roles", request_id="r1"))
    v.validate(_msg("roles", request_id="r1", tiers={"user": {"title": "U", "limits": {"max_sets": 3}}}, capabilities={"trade": ["user"]}))
    v.validate(
        _msg(
            "roles",
            request_id="r1",
            tiers={},
            capabilities={},
            default_tier="user",
            groups_yaml={},
            getcourse_groups=[],
            getcourse_groups_error=None,
            limits_template={"keys": ["max_sets"], "defaults": {"max_sets": 1}},
        )
    )
    with pytest.raises(Exception):
        v.validate(_msg("roles", request_id="r1", tiers={}))  # tiers without capabilities


def test_token_request_and_response_never_carries_token(registry):
    v = _validator("token", registry)
    v.validate(_msg("token", request_id="r1", kind="moex", token="abc"))
    v.validate(_msg("token", request_id="r1", kind="getcourse", ok=True))
    for bad in (
        _msg("token", request_id="r1", kind="finam", token="abc"),
        _msg("token", request_id="r1", kind="moex"),
        _msg("token", request_id="r1", kind="moex", token="abc", ok=True),
        _msg("token", request_id="r1", kind="moex", ok=False),
    ):
        with pytest.raises(Exception):
            v.validate(bad)


def test_error(registry):
    v = _validator("error", registry)
    v.validate(_msg("error", request_id="r1", code="forbidden", message="Только для администратора"))
    v.validate(_msg("error", code="validation_error", message="x", item={"interface": {}}))
    with pytest.raises(Exception):
        v.validate(_msg("error", code="nope", message="x"))
    with pytest.raises(Exception):
        v.validate(_msg("error", code="forbidden", message=""))


def test_channel_root_oneof_routes_by_schema(registry):
    from jsonschema import Draft202012Validator

    root = Draft202012Validator({"$ref": CONFIG_CHANNEL_ID}, registry=registry)
    root.validate(_msg("settings", request_id="r1"))
    root.validate(_msg("token", request_id="r1", kind="moex", ok=True))
    with pytest.raises(Exception):
        root.validate({"channel": "config", "schema": "afbws.config.nope.v1"})
