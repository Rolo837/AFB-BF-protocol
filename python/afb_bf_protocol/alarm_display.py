"""Human-readable alarm condition labels for MQTT notifications.

Mirrors AFB frontend ``alarmConditionDescription.ts`` and
``chartIndicatorDisplayLabel.ts`` so backend can pre-render ``display`` fields
before publishing to MQTT.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

OP_LABELS: dict[str, str] = {
    "crossing": "Пересечение",
    "breakdown": "Пробой вниз",
    "breakout": "Пробой вверх",
    "crosses_above": "Пересечение вверх",
    "crosses_below": "Пересечение вниз",
    "above": "Выше",
    "below": "Ниже",
}

DATASET_LABELS: dict[str, str] = {
    "positions": "Позиции",
    "trades": "Сделки",
    "hhi": "Концентрация",
    "orders": "Ордера",
}


def _indicator_settings(ind: Mapping[str, Any]) -> dict[str, Any]:
    settings = ind.get("settings")
    if isinstance(settings, dict):
        return settings
    return {}


def chart_indicator_display_label(ind: Mapping[str, Any]) -> str:
    """Short indicator label as on chart cards (e.g. ``WMA (5)``)."""
    ind_type = str(ind.get("type") or "")
    settings = _indicator_settings(ind)
    if ind_type == "wma":
        period = settings.get("period")
        return f"WMA ({period if period is not None else '—'})"
    if ind_type == "kama":
        er = settings.get("erPeriod")
        return f"KAMA ({er if er is not None else '—'})"
    if ind_type == "psar":
        start = settings.get("start")
        return f"PSAR ({start if start is not None else '—'})"
    if ind_type == "cot":
        period = settings.get("period")
        return f"WillCo ({period if period is not None else '—'})"
    return ind_type.upper() if ind_type else "—"


def _find_indicator(indicators: Sequence[Mapping[str, Any]], indicator_id: str | None) -> Mapping[str, Any] | None:
    if not indicator_id:
        return None
    for ind in indicators:
        if str(ind.get("id") or "") == indicator_id:
            return ind
    return None


def condition_op_label(op: str | None) -> str:
    """Operator label; missing ``op`` means price touch."""
    if not op:
        return "Касание"
    return OP_LABELS.get(op, op)


def condition_description(
    condition: Mapping[str, Any] | None,
    indicators: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """Condition body: ``Цена 250.5`` / ``WMA (5) / KAMA (10)`` / ``Позиции/long 100``."""
    c = condition or {}
    left = c.get("left") or {}
    right = c.get("right") or {}
    source = left.get("source") or "price"
    val_str = right.get("const") if right.get("const") is not None else "—"
    inds = indicators or []

    if source == "dataset":
        dataset_id = str(left.get("dataset_id") or "")
        if dataset_id == "volume":
            return "Объём (временно не поддерживается)"
        label = DATASET_LABELS.get(dataset_id, dataset_id)
        field = str(left.get("field") or "")
        return f"{label}/{field or '—'} {val_str}"

    if source == "indicator":
        ind = _find_indicator(inds, str(left.get("id") or "") or None)
        label = chart_indicator_display_label(ind) if ind else str(left.get("id") or "—")
        if right.get("source") == "indicator":
            ref_ind = _find_indicator(inds, str(right.get("id") or "") or None)
            ref_label = chart_indicator_display_label(ref_ind) if ref_ind else str(right.get("id") or "—")
            return f"{label} / {ref_label}"
        return f"{label} {val_str}"

    return f"Цена {val_str}"


def condition_text(
    condition: Mapping[str, Any] | None,
    indicators: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """``Оператор, описание`` — as on frontend alarm cards."""
    c = condition or {}
    op = c.get("op")
    return f"{condition_op_label(op if isinstance(op, str) else None)}, {condition_description(c, indicators)}"


def instrument_label(shortname: str | None, ticker: str) -> str:
    """``Сбербанк (SBER)`` or ticker alone when shortname is missing."""
    secid = (ticker or "").strip() or "?"
    name = (shortname or "").strip()
    if name:
        return f"{name} ({secid})"
    return secid


def build_display(
    *,
    condition: Mapping[str, Any] | None,
    ticker: str,
    shortname: str | None = None,
    indicators: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, str]:
    """Build the ``display`` block for afb.notification.alarm_triggered.v1."""
    c = condition or {}
    op = c.get("op")
    op_label = condition_op_label(op if isinstance(op, str) else None)
    desc = condition_description(c, indicators)
    return {
        "instrument_label": instrument_label(shortname, ticker),
        "condition_op": op_label,
        "condition_description": desc,
        "condition_text": f"{op_label}, {desc}",
    }
