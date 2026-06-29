"""``deal_state.v2`` — shared on-disk deal schema for AFB and BF.

Both projects persist per-deal YAML with this shape (AFB at
``state/deals/<bf_id>/<deal_id>.yaml``, BF at ``state/deals/<deal_id>.yaml``).

Timestamps default to UTC. AFB and BF render in market-local time, so each calls
``set_now_iso(market_now_iso)`` once at import to install its timestamp provider;
the field order and ``to_dict()`` output then match each side's existing files.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Literal

__all__ = [
    "DealStatus",
    "ExecutionPhase",
    "OrderRole",
    "CancelReason",
    "DealStatusSource",
    "DealState",
    "safe_deal_filename",
    "archived_deal_filename",
    "set_now_iso",
    "current_now_iso",
]

# Note: ``waiting_external_signal`` (previously AFB-only) is intentionally excluded.
DealStatus = Literal[
    "draft", "publishing", "published", "active", "paused", "closed", "cancelled", "orphaned"
]
ExecutionPhase = Literal[
    "idle", "awaiting_entry", "entry_working", "holding", "exit_working"
]
OrderRole = Literal["entry", "stop_loss", "take_profit", "cancel_close"]
CancelReason = Literal[
    "user_cancel",
    "publish_rejected",
    "execution_error",
    "tradable_disabled",
    "trading_halted",
    "position_mismatch",
    "legacy_failed",
    "legacy_degraded",
]
DealStatusSource = Literal["afb", "bf"]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


_now_iso: Callable[[], str] = _utc_now_iso


def set_now_iso(fn: Callable[[], str]) -> None:
    """Install the timestamp provider used for created_at/updated_at/status history."""
    global _now_iso
    _now_iso = fn


def current_now_iso() -> str:
    return _now_iso()


def safe_deal_filename(deal_id: str) -> str:
    if ":" in deal_id:
        return deal_id.split(":")[0]
    if "/" in deal_id:
        return deal_id.split("/")[0]
    return deal_id


def archived_deal_filename(deal_id: str) -> str:
    base = safe_deal_filename(deal_id)
    if base.startswith("deal-"):
        return f"deleted-{base[5:]}"
    return f"deleted-{base}"


@dataclass
class DealState:
    deal_id: str
    revision: int
    owner_user_id: str
    status: DealStatus
    deal: dict[str, Any]
    source_refs: dict[str, Any] = field(default_factory=dict)
    status_history: list[dict[str, Any]] = field(default_factory=list)
    orders: list[dict[str, Any]] = field(default_factory=list)
    positions: list[dict[str, Any]] = field(default_factory=list)
    event_journal: list[dict[str, Any]] = field(default_factory=list)
    # Compact observed-state snapshot (controller model). orders[]/positions[]
    # remain the authoritative observed facts; this is a derived summary.
    observed: dict[str, Any] = field(default_factory=dict)
    # Derived; kept on-disk for compatibility (not the source of truth).
    execution_phase: ExecutionPhase = "idle"
    created_at: str = field(default_factory=current_now_iso)
    updated_at: str = field(default_factory=current_now_iso)

    def bf_id(self) -> str:
        target = self.deal.get("target") if isinstance(self.deal.get("target"), dict) else {}
        return str(target.get("bf_id") or "").strip()

    def append_status_history(
        self,
        status: str,
        *,
        source: DealStatusSource = "bf",
        correlation_id: str | None = None,
        cancel_reason: str | None = None,
    ) -> None:
        entry: dict[str, Any] = {"status": status, "at": current_now_iso(), "source": source}
        if correlation_id:
            entry["correlation_id"] = correlation_id
        if cancel_reason:
            entry["cancel_reason"] = cancel_reason
        self.status_history.append(entry)

    @classmethod
    def from_dict(cls, raw: Any) -> "DealState":
        if not isinstance(raw, dict):
            raise ValueError("deal_state must be an object")
        deal = raw.get("deal")
        if not isinstance(deal, dict):
            raise ValueError("deal must be an object")
        deal_id = str(raw.get("deal_id") or deal.get("deal_id") or "").strip()
        if not deal_id:
            raise ValueError("deal_id is required")
        revision = int(raw.get("revision", deal.get("revision", 1)))
        execution_phase = str(raw.get("execution_phase") or "idle").strip() or "idle"
        return cls(
            deal_id=deal_id,
            revision=revision,
            owner_user_id=str(raw.get("owner_user_id") or deal.get("owner", {}).get("user_id") or ""),
            status=str(raw.get("status") or "published"),  # type: ignore[arg-type]
            deal=deal,
            source_refs=dict(raw.get("source_refs") or {}),
            status_history=list(raw.get("status_history") or []),
            orders=list(raw.get("orders") or []),
            positions=list(raw.get("positions") or []),
            event_journal=list(raw.get("event_journal") or []),
            observed=dict(raw.get("observed") or {}),
            execution_phase=execution_phase,  # type: ignore[arg-type]
            created_at=str(raw.get("created_at") or current_now_iso()),
            updated_at=str(raw.get("updated_at") or current_now_iso()),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_resync_payload(self) -> dict[str, Any]:
        """Snapshot for deal.resync (status authoritative from AFB)."""
        return {
            "deal_id": self.deal_id,
            "revision": self.revision,
            "status": self.status,
            "deal": self.deal,
            "status_history": list(self.status_history),
            "source_refs": dict(self.source_refs),
        }
