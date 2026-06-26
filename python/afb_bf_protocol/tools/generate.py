"""Spec-driven codegen: derive the message taxonomy from spec/asyncapi.yaml.

The AsyncAPI document is the source of truth for the message set. Each
``components.messages.*`` entry carries its type as ``name`` (``category.event``)
and tags ``class:<system|user|trading>``, ``dir:<afb2bf|bf2afb>`` and optionally
``persisted``. This module reads those and renders ``afb_bf_protocol/taxonomy.py``.

Run:  ``python -m afb_bf_protocol.tools.generate``  (or ``afb-bf-protocol-generate``)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..taxonomy import MessageMeta, split_category_type


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _spec_path() -> Path:
    return _repo_root() / "spec" / "asyncapi.yaml"


def parse_spec_registry(spec_path: Path | None = None) -> dict[str, MessageMeta]:
    """Build {message_type: MessageMeta} from the AsyncAPI document."""
    import yaml

    spec = yaml.safe_load((spec_path or _spec_path()).read_text())
    messages: dict[str, Any] = spec.get("components", {}).get("messages", {})
    registry: dict[str, MessageMeta] = {}
    for _key, msg in messages.items():
        msg_type = str(msg["name"])
        tags = {str(t["name"]) for t in (msg.get("tags") or [])}
        message_class = next((t.split(":", 1)[1] for t in tags if t.startswith("class:")), None)
        direction = next((t.split(":", 1)[1] for t in tags if t.startswith("dir:")), None)
        if message_class is None or direction is None:
            raise ValueError(f"message {msg_type!r} missing class:/dir: tags")
        category, event = split_category_type(msg_type)
        registry[msg_type] = MessageMeta(
            message_class=message_class,  # type: ignore[arg-type]
            direction=direction,  # type: ignore[arg-type]
            category=category,
            event=event,
            persists_on_bf="persisted" in tags,
        )
    return registry


def render_taxonomy(registry: dict[str, MessageMeta]) -> str:
    lines: list[str] = []
    w = lines.append
    w('"""Message taxonomy for afb.execution.v1.')
    w("")
    w("DO NOT EDIT BY HAND — regenerated from ``spec/asyncapi.yaml`` by")
    w("``tools/generate.py`` (the message tags ``class:*`` / ``dir:*`` / ``persisted``).")
    w("Edit the spec, then run ``afb-bf-protocol-generate``.")
    w('"""')
    w("from __future__ import annotations")
    w("")
    w("from dataclasses import dataclass")
    w("from typing import Literal")
    w("")
    w("__all__ = [")
    for name in (
        "SupportedMarket", "SUPPORTED_MARKETS", "MessageClass", "MessageDirection",
        "MessageMeta", "MESSAGE_REGISTRY", "ALL_MESSAGE_TYPES", "COMMAND_TYPES",
        "BF_EVENT_TYPES", "PERSISTED_BF_EVENT_TYPES", "split_category_type",
    ):
        w(f'    "{name}",')
    w("]")
    w("")
    w('SupportedMarket = Literal["stock", "futures", "currency"]')
    w('SUPPORTED_MARKETS: frozenset[str] = frozenset({"stock", "futures", "currency"})')
    w("")
    w('MessageClass = Literal["system", "user", "trading"]')
    w('MessageDirection = Literal["afb2bf", "bf2afb"]')
    w("")
    w("")
    w("@dataclass(frozen=True, slots=True)")
    w("class MessageMeta:")
    w("    message_class: MessageClass")
    w("    direction: MessageDirection")
    w("    category: str")
    w("    event: str")
    w("    persists_on_bf: bool = False")
    w("")
    w("")
    w("def split_category_type(message_type: str) -> tuple[str, str]:")
    w('    category, dot, event = str(message_type).partition(".")')
    w("    if not dot or not category or not event:")
    w("        raise ValueError(f\"Invalid message type {message_type!r}, expected 'category.type'\")")
    w("    return category, event")
    w("")
    w("")
    w("MESSAGE_REGISTRY: dict[str, MessageMeta] = {")
    for t, m in registry.items():
        persists = ", persists_on_bf=True" if m.persists_on_bf else ""
        w(
            f'    "{t}": MessageMeta("{m.message_class}", "{m.direction}", '
            f'"{m.category}", "{m.event}"{persists}),'
        )
    w("}")
    w("")
    w("ALL_MESSAGE_TYPES: frozenset[str] = frozenset(MESSAGE_REGISTRY.keys())")
    w("COMMAND_TYPES: frozenset[str] = frozenset(")
    w('    t for t, m in MESSAGE_REGISTRY.items() if m.direction == "afb2bf"')
    w(")")
    w("BF_EVENT_TYPES: frozenset[str] = frozenset(")
    w('    t for t, m in MESSAGE_REGISTRY.items() if m.direction == "bf2afb"')
    w(")")
    w("PERSISTED_BF_EVENT_TYPES: frozenset[str] = frozenset(")
    w("    t for t, m in MESSAGE_REGISTRY.items() if m.persists_on_bf")
    w(")")
    return "\n".join(lines) + "\n"


def render_messages_doc(registry: dict[str, MessageMeta]) -> str:
    """Render docs/MESSAGES.md from the spec-derived registry."""
    root = _repo_root()
    have_payload = {p.stem for p in (root / "spec" / "schemas" / "payloads").glob("*.json")}
    have_example = {p.stem for p in (root / "examples").glob("*.json")}

    lines: list[str] = []
    w = lines.append
    w("<!-- DO NOT EDIT — generated from spec/asyncapi.yaml by tools/generate.py -->")
    w("# Message catalog — afb.execution.v1")
    w("")
    w("Every message is a signed envelope (see `spec/schemas/envelope.json`).")
    w("`persisted` = written to BF's `trading_events` journal.")
    w("")
    for direction, title in (("afb2bf", "AFB → BF (commands)"), ("bf2afb", "BF → AFB (events & replies)")):
        w(f"## {title}")
        w("")
        w("| type | class | persisted | payload schema | example |")
        w("|------|-------|-----------|----------------|---------|")
        for t, m in registry.items():
            if m.direction != direction:
                continue
            schema = f"`spec/schemas/payloads/{t}.json`" if t in have_payload else "—"
            example = f"`examples/{t}.json`" if t in have_example else "—"
            persisted = "yes" if m.persists_on_bf else ""
            w(f"| `{t}` | {m.message_class} | {persisted} | {schema} | {example} |")
        w("")
    return "\n".join(lines) + "\n"


def main() -> int:
    registry = parse_spec_registry()
    root = _repo_root()
    target = root / "python" / "afb_bf_protocol" / "taxonomy.py"
    target.write_text(render_taxonomy(registry))
    docs = root / "docs" / "MESSAGES.md"
    docs.parent.mkdir(parents=True, exist_ok=True)
    docs.write_text(render_messages_doc(registry))
    print(f"wrote {target} and {docs} ({len(registry)} message types from spec)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
