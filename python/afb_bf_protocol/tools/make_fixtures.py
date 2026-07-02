"""Generate signed example envelopes from payload sources.

Reads ``examples/_payloads/<type>.json`` (authentic payload bodies sourced from
real BF wire data and the protocol spec), wraps each in an envelope with the
correct sender/recipient for its taxonomy direction, signs it with the committed
**test** keypair, and writes ``examples/<stem>.json``.

A source file name may carry a ``__variant`` suffix (e.g.
``deal.publish__v2.json``) when a message type needs more than one example —
the part before ``__`` is looked up in ``MESSAGE_REGISTRY`` and used to
validate against ``spec/schemas/payloads/<type>.json``, while the full stem
becomes the output file name so variants don't collide.

The keypair under ``examples/_keys/`` is derived from a fixed seed — it is for
fixtures/tests only and must never be used on a real connection.

Run from the repo root:  ``python -m afb_bf_protocol.tools.make_fixtures``
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from afb_bf_protocol import (
    MESSAGE_REGISTRY,
    export_private_key_pem,
    export_public_key_pem,
    make_envelope,
    sign_envelope,
)

BF_ID = "finam-arena-316"

# Fixed seeds -> deterministic, reproducible test keys (NOT for real use).
_SEEDS = {
    "afb": b"afb-bf-protocol::test-key::afb-side\x00\x00",
    "bf": b"afb-bf-protocol::test-key::bf-side\x00\x00\x00",
}
_KEY_IDS = {"afb": "afb-test-1", "bf": "belphegor-test-1"}


def _repo_root() -> Path:
    # python/afb_bf_protocol/tools/make_fixtures.py -> repo root is 4 levels up.
    return Path(__file__).resolve().parents[3]


def _ensure_keys(keys_dir: Path) -> dict[str, Ed25519PrivateKey]:
    keys_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, Ed25519PrivateKey] = {}
    for side, seed in _SEEDS.items():
        priv = Ed25519PrivateKey.from_private_bytes(seed[:32])
        (keys_dir / f"{side}-private.pem").write_bytes(export_private_key_pem(priv))
        (keys_dir / f"{side}-public.pem").write_bytes(export_public_key_pem(priv.public_key()))
        out[side] = priv
    return out


def main() -> int:
    root = _repo_root()
    examples = root / "examples"
    payloads_dir = examples / "_payloads"
    keys = _ensure_keys(examples / "_keys")

    written = 0
    for pf in sorted(payloads_dir.glob("*.json")):
        stem = pf.stem
        msg_type = stem.split("__", 1)[0]
        meta = MESSAGE_REGISTRY.get(msg_type)
        if meta is None:
            print(f"  skip {stem}: {msg_type!r} not in MESSAGE_REGISTRY")
            continue
        payload = json.loads(pf.read_text())
        if meta.direction == "afb2bf":
            side, sender, recipient = "afb", "afb", BF_ID
        else:
            side, sender, recipient = "bf", BF_ID, "afb"
        idem = f"{sender}:{stem}:fixture-0001"
        digest = hashlib.sha256(stem.encode()).hexdigest()
        env = make_envelope(
            sender=sender,
            recipient=recipient,
            msg_type=msg_type,
            payload=payload,
            key_id=_KEY_IDS[side],
            idempotency_key=idem,
            message_id=f"{digest[:8]}-{digest[8:12]}-4{digest[13:16]}-8{digest[17:20]}-{digest[20:32]}",
            created_at="2026-06-26T12:00:00+03:00",
        )
        sign_envelope(env, keys[side])
        (examples / f"{stem}.json").write_text(
            json.dumps(env.to_dict(), ensure_ascii=False, indent=2) + "\n"
        )
        written += 1
    print(f"wrote {written} signed example envelopes to {examples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
