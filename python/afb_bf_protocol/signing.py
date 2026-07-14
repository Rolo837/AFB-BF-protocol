"""Ed25519 key IO and envelope sign/verify.

Ported from BF (the fuller implementation): supports PEM (PKCS#8/SPKI) and raw
32-byte keys, signs the canonical ``signing_string`` and verifies both the
signature and ``payload_hash``.
"""
from __future__ import annotations

import base64
import hashlib
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

from .envelope import payload_hash, signing_string
from .models import Envelope, Signature

__all__ = [
    "b64url_encode",
    "b64url_decode",
    "load_private_key",
    "load_public_key",
    "sign_envelope",
    "verify_envelope",
    "generate_keypair",
    "export_private_key_pem",
    "export_public_key_pem",
    "ensure_dev_keypair",
    "key_fingerprint",
]


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def load_private_key(path: Path) -> Ed25519PrivateKey:
    raw = Path(path).read_bytes()
    if raw.startswith(b"-----"):
        from cryptography.hazmat.primitives.serialization import load_pem_private_key

        key = load_pem_private_key(raw, password=None)
        if not isinstance(key, Ed25519PrivateKey):
            raise ValueError("Expected Ed25519 private key")
        return key
    if len(raw) == 32:
        return Ed25519PrivateKey.from_private_bytes(raw)
    raise ValueError(f"Unsupported private key format: {path}")


def load_public_key(path: Path) -> Ed25519PublicKey:
    raw = Path(path).read_bytes()
    if raw.startswith(b"-----"):
        if b"BEGIN PRIVATE KEY" in raw or b"BEGIN ENCRYPTED PRIVATE KEY" in raw:
            raise ValueError(
                f"{path}: file contains a private key, not a public key."
            )
        from cryptography.hazmat.primitives.serialization import load_pem_public_key

        key = load_pem_public_key(raw)
        if not isinstance(key, Ed25519PublicKey):
            raise ValueError("Expected Ed25519 public key")
        return key
    if len(raw) == 32:
        return Ed25519PublicKey.from_public_bytes(raw)
    raise ValueError(f"Unsupported public key format: {path}")


def sign_envelope(envelope: Envelope, private_key: Ed25519PrivateKey) -> Envelope:
    """Recompute ``payload_hash``, sign the signing string, set the signature value."""
    envelope.payload_hash = payload_hash(envelope.payload)
    sig_bytes = private_key.sign(signing_string(envelope).encode("utf-8"))
    envelope.signature = Signature(
        alg="Ed25519",
        key_id=envelope.signature.key_id,
        value=b64url_encode(sig_bytes),
    )
    return envelope


def verify_envelope(envelope: Envelope, public_key: Ed25519PublicKey) -> None:
    """Raise on ``payload_hash`` mismatch or invalid signature."""
    if envelope.payload_hash != payload_hash(envelope.payload):
        raise ValueError("payload_hash mismatch")
    public_key.verify(
        b64url_decode(envelope.signature.value),
        signing_string(envelope).encode("utf-8"),
    )


def generate_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    private_key = Ed25519PrivateKey.generate()
    return private_key, private_key.public_key()


def export_private_key_pem(private_key: Ed25519PrivateKey) -> bytes:
    return private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )


def export_public_key_pem(public_key: Ed25519PublicKey) -> bytes:
    return public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )


def key_fingerprint(public_key: Ed25519PublicKey) -> str:
    """First 12 hex chars of sha256(SPKI DER) — a diagnostic key_id, not a trust check."""
    der = public_key.public_bytes(
        encoding=Encoding.DER,
        format=PublicFormat.SubjectPublicKeyInfo,
    )
    return hashlib.sha256(der).hexdigest()[:12]


def ensure_dev_keypair(
    *,
    private_key_file: Path,
    public_key_file: Path | None,
    auto_generate: bool,
) -> None:
    """Create a PEM keypair for dev when the private key is missing."""
    private_key_file = Path(private_key_file)
    if private_key_file.exists():
        return
    if not auto_generate:
        raise FileNotFoundError(
            f"Private key not found: {private_key_file}. "
            "Create PEM keys or set auto_generate=True."
        )
    private_key_file.parent.mkdir(parents=True, exist_ok=True)
    private_key, public_key = generate_keypair()
    private_key_file.write_bytes(export_private_key_pem(private_key))
    pub_path = Path(public_key_file) if public_key_file else private_key_file.with_name(
        "public.pem"
    )
    pub_path.parent.mkdir(parents=True, exist_ok=True)
    pub_path.write_bytes(export_public_key_pem(public_key))
