"""``deal_state.v2`` — shared on-disk deal schema for AFB and BF.

Both projects persist per-deal YAML with this exact shape (AFB at
``state/deals/<bf_id>/<deal_id>.yaml``, BF at ``state/deals/<deal_id>.yaml``).

Timestamps: the default ``now_iso`` is UTC. BF/AFB render in market timezone, so
they should pass timestamps explicitly (or set ``DealState.now_iso``) to preserve
their ``+03:00`` market-local rendering.
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
]

# Note: ``waiting_external_signal`` (previously AFB-only) is intentionally
# excluded from the canonical set.
DealStatus = Literal[
    "draft",
    "publishing",
    "published",
    "active",
    "paused",
    "closed",
    "cancelled",
    "orphaned",
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
    # Override to render timestamps in a project-specific timezone.
    now_iso: Callable[[], str] = field(default=_utc_now_iso, repr=False, compare=False)

    deal_id: str = ""
    revision: int = 1
    owner_user_id: str = ""
    status: DealStatus = "published"
    deal: dict[str, Any] = field(default_factory=dict)
    source_refs: dict[str, Any] = field(default_factory=dict)
    status_history: list[dict[str, Any]] = field(default_factory=list)
    orders: list[dict[str, Any]] = field(default_factory=list)
    positions: list[dict[str, Any]] = field(default_factory=list)
    event_journal: list[dict[str, Any]] = field(default_factory=list)
    observed: dict[str, Any] = field(default_factory=dict)
    # Derived; kept on-disk for AFB compatibility (not the source of truth).
    execution_phase: ExecutionPhase = "idle"
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = self.now_iso()
        if not self.updated_at:
            self.updated_at = self.now_iso()

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
        entry: dict[str, Any] = {"status": status, "at": self.now_iso(), "source": source}
        if correlation_id:
            entry["correlation_id"] = correlation_id
        if cancel_reason:
            entry["cancel_reason"] = cancel_reason
        self.status_history.append(entry)

    @classmethod
    def from_dict(cls, raw: Any, *, now_iso: Callable[[], str] = _utc_now_iso) -> "DealState":
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
            now_iso=now_iso,
            deal_id=deal_id,
            revision=revision,
            owner_user_id=str(raw.get("owner_user_id") or ""),
            status=str(raw.get("status") or "published"),  # type: ignore[arg-type]
            deal=deal,
            source_refs=dict(raw.get("source_refs") or {}),
            status_history=list(raw.get("status_history") or []),
            orders=list(raw.get("orders") or []),
            positions=list(raw.get("positions") or []),
            event_journal=list(raw.get("event_journal") or []),
            observed=dict(raw.get("observed") or {}),
            execution_phase=execution_phase,  # type: ignore[arg-type]
            created_at=str(raw.get("created_at") or now_iso()),
            updated_at=str(raw.get("updated_at") or now_iso()),
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("now_iso", None)
        return data
