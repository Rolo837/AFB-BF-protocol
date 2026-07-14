"""Reference implementation of the condition-node operator semantics defined by
``spec/schemas/condition.v1.json``. This is the single point of truth for how
every consumer (BF's ``plan_engine.conditions``, AFB's alarm checker, trade-plan
processor and dataset signal runner) must evaluate a condition — see that
schema's ``$defs.conditionNode`` description for the operator vocabulary and
``docs/PROTOCOL.md`` for the worked examples.

Price conditions support six fully-supported operators — none of them legacy
or deprecated: ``touch`` (op omitted or ``"touch"``), ``above``/``below``
(``PRICE_LEVEL_OPS``, inclusive level check, no timeframe) and
``breakout``/``breakdown``/``crossing`` (``PRICE_CANDLE_OPS``, last CLOSED
candle of the given timeframe). They also differ in how BF executes a fired
condition: ``touch`` places a LIMIT order (bounded slippage via
``limit_offset_steps``); the other five place a MARKET order (must fill
regardless of slippage) — see ``belphegor.plan_engine.order_policy`` on the
BF side. This module only evaluates *whether* a condition fired; the
execution-type decision lives entirely in BF.

Pure stdlib, no I/O: callers own sourcing ``cur``/``prev`` (and, for indicators
and datasets, the same for the right-hand side) and the last CLOSED candle for
price candle operators. A ``None`` input at any point means "no data available"
and always evaluates to ``False`` — never an exception — matching BF's existing
invariant that a condition with missing data does not fire.

Fixes the confirmed crossing boundary bug (case 3.248 in alarm
alarm-5a01-4480-ba65's logs): a same-sample ``prev == ref`` used to be treated
as strictly inside the "not yet crossed" side (via ``prev < ref``), silently
swallowing a cross that starts exactly on the reference value. The correct
boundary (this module's and hence the wire's semantics) is non-strict on the
`prev` side: ``crosses_above`` fires when ``prev <= ref_prev and cur > ref_cur``.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Optional, Union

__all__ = [
    "TIMEFRAMES",
    "SCALAR_OPS",
    "PRICE_TOUCH_OPS",
    "PRICE_LEVEL_OPS",
    "PRICE_CANDLE_OPS",
    "DEPRECATED_PRICE_TICK_OPS",
    "DEPRECATED_PRICE_OPS",
    "DEPRECATED_QUOTE_OPS",
    "OPS_BY_SOURCE",
    "evaluate_touch",
    "evaluate_price_level_op",
    "evaluate_scalar_op",
    "evaluate_candle_op",
]

Number = Union[str, int, float, Decimal]

# condition.v1.json#/$defs/timeframe — single source of truth for the wire
# timeframe enum, mirrored here (rather than parsed from the schema at import
# time) so callers that only need envelope/signing (no jsonschema dependency,
# e.g. BF's deep payload validation) can still validate timeframe values.
TIMEFRAMES: tuple[str, ...] = (
    "5min", "10min", "15min", "30min", "1h", "2h", "4h", "1d",
)

# indicator/dataset conditions, and the deprecated tick-based price/quote ops.
SCALAR_OPS: frozenset[str] = frozenset(
    {"above", "below", "crosses_above", "crosses_below", "crossing"}
)

# Explicit spelling of the price touch operator. `op` omitted entirely is the
# same operator, kept for wire back-compat with pre-touch-op deals/plans —
# see evaluate_touch. Both forms dispatch identically on every consumer.
PRICE_TOUCH_OPS: frozenset[str] = frozenset({"touch"})

# Inclusive price level checks (no timeframe).
PRICE_LEVEL_OPS: frozenset[str] = frozenset({"above", "below"})

# price conditions with a `timeframe`, evaluated on the last CLOSED candle only.
PRICE_CANDLE_OPS: frozenset[str] = frozenset({"breakout", "breakdown", "crossing"})

# Deprecated tick crosses_* / crossing on price without timeframe.
DEPRECATED_PRICE_TICK_OPS: frozenset[str] = frozenset(
    {"crosses_above", "crosses_below", "crossing"}
)

# Back-compat alias: all non-candle tick ops on price (level + deprecated).
DEPRECATED_PRICE_OPS: frozenset[str] = PRICE_LEVEL_OPS | DEPRECATED_PRICE_TICK_OPS

# quote conditions — full scalar vocabulary, deprecated in v1.4.0.
DEPRECATED_QUOTE_OPS: frozenset[str] = SCALAR_OPS

# Valid explicit `op` values per left.source. `price` additionally allows
# omitting `op` entirely — equivalent to `op="touch"`, see evaluate_touch.
OPS_BY_SOURCE: dict[str, frozenset[str]] = {
    "price": PRICE_TOUCH_OPS | PRICE_CANDLE_OPS | PRICE_LEVEL_OPS | DEPRECATED_PRICE_TICK_OPS,
    "quote": DEPRECATED_QUOTE_OPS,
    "indicator": SCALAR_OPS,
    "dataset": SCALAR_OPS,
}


def _dec(value: Optional[Number]) -> Optional[Decimal]:
    if value is None:
        return None
    return value if isinstance(value, Decimal) else Decimal(str(value))


def evaluate_touch(
    cur: Optional[Number], prev: Optional[Number], level: Optional[Number]
) -> bool:
    """Price touch (`op="touch"`, or `op` omitted for wire back-compat): the
    level lies between the previous and current sample, i.e.
    ``min(prev, cur) <= level <= max(prev, cur)``. Callers dispatch both
    `op is None` and `op == "touch"` to this function — they are the same
    operator. BF executes a fired touch as a LIMIT order (price ~= level,
    bounded slippage); see order_policy on the BF side for the execution-type
    decision, which this module does not make."""
    cur_d, prev_d, level_d = _dec(cur), _dec(prev), _dec(level)
    if cur_d is None or prev_d is None or level_d is None:
        return False
    lo, hi = (prev_d, cur_d) if prev_d <= cur_d else (cur_d, prev_d)
    return lo <= level_d <= hi


def evaluate_price_level_op(
    op: str,
    cur: Optional[Number],
    level: Optional[Number],
) -> bool:
    """Inclusive price level check: ``above`` = ``cur >= level``;
    ``below`` = ``cur <= level``. Does not use ``prev``. BF executes a fired
    above/below as a MARKET order — it must fill regardless of how far price
    has moved past ``level``."""
    cur_d, level_d = _dec(cur), _dec(level)
    if cur_d is None or level_d is None:
        return False
    if op == "above":
        return cur_d >= level_d
    if op == "below":
        return cur_d <= level_d
    raise ValueError(f"unknown price level op: {op!r}")


def evaluate_scalar_op(
    op: str,
    cur: Optional[Number],
    prev: Optional[Number],
    ref_cur: Optional[Number],
    ref_prev: Optional[Number] = None,
) -> bool:
    """The 5-operator scalar vocabulary shared by indicator/dataset conditions
    and the deprecated tick-based price/quote conditions.

    ``ref_prev`` defaults to ``ref_cur`` — a constant right-hand side has no
    history of its own, which is exactly what makes the boundary semantics
    below reduce correctly to "prev sample was on the const's other side".

    Boundary (fixes the prev==ref bug, see module docstring):
    ``crosses_above`` = ``prev <= ref_prev and cur > ref_cur``;
    ``crosses_below`` = ``prev >= ref_prev and cur < ref_cur``;
    ``crossing`` = either of the above. A touch without departure
    (``cur == ref_cur``) is never a cross.
    """
    cur_d, ref_cur_d = _dec(cur), _dec(ref_cur)
    if cur_d is None or ref_cur_d is None:
        return False
    if op == "above":
        return cur_d > ref_cur_d
    if op == "below":
        return cur_d < ref_cur_d
    if op not in ("crosses_above", "crosses_below", "crossing"):
        raise ValueError(f"unknown scalar op: {op!r}")
    prev_d = _dec(prev)
    if prev_d is None:
        return False
    ref_prev_d = ref_cur_d if ref_prev is None else _dec(ref_prev)
    crosses_above = prev_d <= ref_prev_d and cur_d > ref_cur_d
    crosses_below = prev_d >= ref_prev_d and cur_d < ref_cur_d
    if op == "crosses_above":
        return crosses_above
    if op == "crosses_below":
        return crosses_below
    return crosses_above or crosses_below


def evaluate_candle_op(
    op: str,
    open_: Optional[Number],
    close: Optional[Number],
    level: Optional[Number],
) -> bool:
    """Price candle operators, evaluated against a single CLOSED candle's
    open/close relative to `level`. Callers are responsible for only ever
    passing the last closed candle of the condition's `timeframe` — this
    function has no notion of "closed" itself.

    ``breakout`` = ``open < level and close > level``;
    ``breakdown`` = ``open > level and close < level``;
    ``crossing`` = either of the above. Like above/below, BF executes a fired
    candle op as a MARKET order: by the time a full candle has closed past
    ``level``, price has typically moved well beyond it.
    """
    open_d, close_d, level_d = _dec(open_), _dec(close), _dec(level)
    if open_d is None or close_d is None or level_d is None:
        return False
    if op not in ("breakout", "breakdown", "crossing"):
        raise ValueError(f"unknown candle op: {op!r}")
    breakout = open_d < level_d and close_d > level_d
    breakdown = open_d > level_d and close_d < level_d
    if op == "breakout":
        return breakout
    if op == "breakdown":
        return breakdown
    return breakout or breakdown
