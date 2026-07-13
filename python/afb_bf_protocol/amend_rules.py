"""Allowed-edit matrix for amending an already-published deal.

Single source of truth for *what* may change *when* in a live deal. Both AFB
(for UX gating / pre-validation) and BF (the authoritative gate) call
``evaluate_amend`` so the rules never drift between the two sides — same pattern
as the spec-driven ``taxonomy``.

The rules are a function of the deal's **execution phase** (derived in BF by
``infer_execution_stage``) plus its **status**. ``idle`` phase is reached both by
``published`` (not yet activated → everything editable) and by terminal statuses
(``closed`` / ``cancelled`` / ``orphaned`` → nothing editable), so ``status`` is
needed to tell them apart.

Matrix (``✓`` allow · ``~`` allow-with-warning · ``✗`` deny):

    field \\ phase        published  awaiting_entry  entry_working  holding  exit_working  terminal
    instrument           ✓          ✗               ✗              ✗        ✗             ✗
    side                 ✓          ✓               ~              ✗        ✗             ✗
    entry (condition)    ✓          ✓               ~              ✗        ✗             ✗
    sizing               ✓          ✓               ✓              ✗        ✗             ✗
    stop_loss            ✓          ✓               ✓              ✓        ~             ✗
    take_profit          ✓          ✓               ✓              ✓        ~             ✗
    execution_policy     ✓          ✓               ✓              ✓        ~             ✗

Invariants encoded here:
- Entry-defining fields (instrument / side / entry condition) freeze the
  moment a position exists. ``entry_working`` means a live entry order with **no**
  fill yet (``infer_execution_stage`` returns ``holding`` as soon as there is any
  position), so it is still safe to cancel+replace the entry there.
  ``entry``'s deprecated ``order`` sub-block (order type/time_in_force/offset —
  now decided solely by BF, not part of the deal) is ignored here even if still
  present on old stored deals, so it never causes a spurious "entry changed".
  "side" reads ``entry.side`` (legacy buy/sell) or the deal-level ``direction``
  (long/short) on afb.deal.v1 — at least one is present, entry.side wins when
  both are — and only the deal-level ``direction`` on afb.deal.v2, which has
  no per-leg side at all (see amend_rules._sides).
- Sizing is editable only before a position is taken; once holding (or exiting) it
  is frozen. Changing a held position's size is a *reduce/add* flow, not an amend.
- Protective levels (stop_loss / take_profit) stay editable for almost the whole
  life of the deal; in ``exit_working`` they are allowed but flagged (race with
  the closing order in flight).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .deal_state import DealStatus, ExecutionPhase

__all__ = [
    "AmendContext",
    "FieldVerdict",
    "AmendDecision",
    "AMEND_FIELDS",
    "evaluate_amend",
    "is_amend_allowed",
]

# Terminal statuses: the deal is finished, nothing may change.
_TERMINAL_STATUSES: frozenset[str] = frozenset({"closed", "cancelled", "orphaned"})

# Semantic fields the matrix governs, in display order.
AMEND_FIELDS: tuple[str, ...] = (
    "instrument",
    "side",
    "entry",
    "sizing",
    "stop_loss",
    "take_profit",
    "execution_policy",
)


@dataclass(frozen=True)
class AmendContext:
    """Authoritative facts the gate needs, supplied by the caller.

    ``status`` / ``phase`` come from the stored deal (BF derives ``phase`` via
    ``infer_execution_stage``; AFB uses the last ``execution_phase`` it was told,
    defaulting an active/paused deal with unknown phase to ``holding``).
    """

    status: DealStatus
    phase: ExecutionPhase


@dataclass(frozen=True)
class FieldVerdict:
    field: str
    changed: bool
    allowed: bool
    reason: str = ""
    warning: bool = False


@dataclass(frozen=True)
class AmendDecision:
    """Result of evaluating an amend. ``allowed`` is True iff every *changed*
    field is permitted (an amend that changes nothing governed by the matrix is
    trivially allowed)."""

    allowed: bool
    fields: tuple[FieldVerdict, ...] = field(default_factory=tuple)

    def changed(self) -> list[FieldVerdict]:
        return [v for v in self.fields if v.changed]

    def rejected(self) -> list[FieldVerdict]:
        return [v for v in self.fields if v.changed and not v.allowed]

    def warnings(self) -> list[FieldVerdict]:
        return [v for v in self.fields if v.changed and v.allowed and v.warning]

    def reasons(self) -> list[str]:
        return [v.reason for v in self.rejected() if v.reason]

    def per_field(self) -> dict[str, dict[str, Any]]:
        """Compact map for wire/UI: {field: {changed, allowed, reason, warning}}."""
        return {
            v.field: {
                "changed": v.changed,
                "allowed": v.allowed,
                "reason": v.reason,
                "warning": v.warning,
            }
            for v in self.fields
        }


# --- deal field extraction (schema v1 + v2) ---------------------------------

def _is_v2(deal: dict[str, Any]) -> bool:
    if str(deal.get("schema") or "") == "afb.deal.v2":
        return True
    return isinstance(deal.get("entry"), list)


def _instrument_identity(deal: dict[str, Any]) -> tuple[str, str, str, str]:
    target = deal.get("target") if isinstance(deal.get("target"), dict) else {}
    instr = target.get("instrument") if isinstance(target.get("instrument"), dict) else {}
    return (
        str(instr.get("exchange") or ""),
        str(instr.get("board") or ""),
        str(instr.get("ticker") or ""),
        str(instr.get("market") or ""),
    )


def _sides(deal: dict[str, Any]) -> tuple[str, ...]:
    if _is_v2(deal):
        return (str(deal.get("direction") or ""),)
    # afb.deal.v1: position bias is entry.side (legacy) or the root `direction`
    # (target vocabulary) — at least one is present per the deal.v1 schema;
    # producers are moving to setting both, so prefer entry.side when present.
    entry = deal.get("entry")
    if isinstance(entry, dict) and entry.get("side"):
        return (str(entry.get("side") or ""),)
    if deal.get("direction"):
        return (str(deal.get("direction") or ""),)
    return ()


def _entry_triggers(deal: dict[str, Any]) -> Any:
    """Entry condition(s), excluding ``side`` (governed separately) and the
    deprecated per-leg ``order`` block (BF-only concern, not part of the deal)."""
    entry = deal.get("entry")
    if _is_v2(deal) and isinstance(entry, list):
        return [
            {
                "percent": (e or {}).get("percent"),
                "condition": (e or {}).get("condition"),
            }
            for e in entry
        ]
    if isinstance(entry, dict):
        return [{"condition": entry.get("condition")}]
    return []


def _sizing(deal: dict[str, Any]) -> Any:
    return deal.get("sizing")


def _stops(deal: dict[str, Any]) -> Any:
    if _is_v2(deal):
        return deal.get("stop_loss") or []
    risk = deal.get("risk") if isinstance(deal.get("risk"), dict) else {}
    sl = risk.get("stop_loss")
    return [sl] if sl else []


def _takes(deal: dict[str, Any]) -> Any:
    if _is_v2(deal):
        return deal.get("take_profit") or []
    risk = deal.get("risk") if isinstance(deal.get("risk"), dict) else {}
    tp = risk.get("take_profit")
    return [tp] if tp else []


def _policy(deal: dict[str, Any]) -> Any:
    return deal.get("execution_policy")


_EXTRACTORS = {
    "instrument": _instrument_identity,
    "side": _sides,
    "entry": _entry_triggers,
    "sizing": _sizing,
    "stop_loss": _stops,
    "take_profit": _takes,
    "execution_policy": _policy,
}


# --- per-field phase rules ---------------------------------------------------

def _field_allowed(field_name: str, ctx: AmendContext) -> tuple[bool, str, bool]:
    """Return (allowed, reason_code, warning) for changing ``field_name`` now."""
    status, phase = ctx.status, ctx.phase

    if status in _TERMINAL_STATUSES:
        return False, "terminal_immutable", False

    # ``idle`` phase with a non-terminal status == published but not activated:
    # nothing is executing yet, so everything is editable (re-binds on activate).
    if phase == "idle":
        return True, "", False

    # Active / paused, position-bearing lifecycle.
    if field_name == "instrument":
        return False, "instrument_immutable_on_active", False

    if field_name in ("side", "entry"):
        if phase == "awaiting_entry":
            return True, "", False
        if phase == "entry_working":
            # live entry order, no fill yet — safe to cancel+replace
            return True, "entry_cancel_replace", True
        return False, "entry_locked_after_fill", False  # holding / exit_working

    if field_name == "sizing":
        # Editable only before any position is taken; once holding (or exiting),
        # the size is frozen — changing a held position is a reduce/add flow, not
        # an amend.
        if phase in ("awaiting_entry", "entry_working"):
            return True, "", False
        return False, "size_immutable_after_entry", False  # holding / exit_working

    if field_name in ("stop_loss", "take_profit"):
        if phase == "exit_working":
            return True, "exit_in_flight", True
        return True, "", False

    if field_name == "execution_policy":
        return True, "", phase == "exit_working"

    # Unknown / non-governed field (owner, binding, archive_reason): permissive.
    return True, "", False


def evaluate_amend(
    old_deal: dict[str, Any],
    new_deal: dict[str, Any],
    ctx: AmendContext,
) -> AmendDecision:
    """Decide whether ``new_deal`` may replace ``old_deal`` given ``ctx``.

    Compares the matrix-governed fields, and for each field that actually changed
    applies the phase rule. The amend is allowed iff no changed field is denied.
    """
    verdicts: list[FieldVerdict] = []
    for name in AMEND_FIELDS:
        extract = _EXTRACTORS[name]
        changed = extract(old_deal) != extract(new_deal)
        if not changed:
            verdicts.append(FieldVerdict(name, changed=False, allowed=True))
            continue
        allowed, reason, warning = _field_allowed(name, ctx)
        verdicts.append(
            FieldVerdict(name, changed=True, allowed=allowed, reason=reason, warning=warning)
        )

    overall = all(v.allowed for v in verdicts if v.changed)
    return AmendDecision(allowed=overall, fields=tuple(verdicts))


def is_amend_allowed(
    old_deal: dict[str, Any],
    new_deal: dict[str, Any],
    ctx: AmendContext,
) -> bool:
    return evaluate_amend(old_deal, new_deal, ctx).allowed
