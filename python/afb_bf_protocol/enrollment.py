"""Pairing/enrollment helpers for the AFB <-> BF key exchange over ws:// (no TLS).

A high-entropy one-time pairing token authenticates an HMAC-confirmed exchange
of freshly generated Ed25519 public keys: an active MITM without the token
cannot substitute either side's key. See ``docs/PROTOCOL.md`` (Enrollment
section) for the full scheme and the exact strings hashed below — this module
is the single implementation both AFB and BF call into, so the two sides can
never drift on the wire format.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import secrets
from dataclasses import dataclass

from .envelope import canonical_json

__all__ = [
    "PAIRING_TOKEN_PREFIX",
    "PAIRING_STRING_PREFIX",
    "ENROLL_CONTEXT",
    "PairingInfo",
    "PairingStringError",
    "generate_pairing_token",
    "pairing_token_hash",
    "derive_mac_key",
    "generate_nonce",
    "public_key_pem_hash",
    "enroll_request_mac",
    "enroll_response_mac",
    "macs_equal",
    "build_pairing_string",
    "parse_pairing_string",
]

PAIRING_TOKEN_PREFIX = "bf1_"
PAIRING_STRING_PREFIX = "afbpair1_"
ENROLL_CONTEXT = "afb-bf-enroll.v1"

_BF_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_TOKEN_RE = re.compile(rf"^{re.escape(PAIRING_TOKEN_PREFIX)}[a-z2-7]{{32}}$")


class PairingStringError(ValueError):
    """Raised on a malformed/unsupported pairing string ("not the right code")."""


@dataclass(frozen=True, slots=True)
class PairingInfo:
    afb_ws_url: str
    bf_id: str
    token: str


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def generate_pairing_token() -> str:
    """``bf1_`` + lowercase unpadded base32 of 20 random bytes (160 bits)."""
    raw = secrets.token_bytes(20)
    body = base64.b32encode(raw).decode("ascii").rstrip("=").lower()
    return PAIRING_TOKEN_PREFIX + body


def pairing_token_hash(token: str) -> str:
    """sha256 hex of the token — stored for diagnostics; never used for verification."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def derive_mac_key(token: str) -> bytes:
    """``K = HMAC-SHA256(key=token, msg="afb-bf-enroll.v1|kdf")`` — the shared MAC key."""
    return hmac.new(
        token.encode("utf-8"), f"{ENROLL_CONTEXT}|kdf".encode("utf-8"), hashlib.sha256
    ).digest()


def generate_nonce() -> str:
    """base64url (16 random bytes) — used for ``client_nonce``/``server_nonce``."""
    return _b64url_encode(secrets.token_bytes(16))


def public_key_pem_hash(public_key_pem: str) -> str:
    """sha256 hex of the PEM string exactly as carried on the wire (not re-serialized)."""
    return hashlib.sha256(public_key_pem.encode("utf-8")).hexdigest()


def enroll_request_mac(mac_key: bytes, *, bf_id: str, client_nonce: str, bf_public_key_pem: str) -> str:
    msg = (
        f"{ENROLL_CONTEXT}|bf2afb|{bf_id}|{client_nonce}|"
        f"{public_key_pem_hash(bf_public_key_pem)}"
    )
    return hmac.new(mac_key, msg.encode("utf-8"), hashlib.sha256).hexdigest()


def enroll_response_mac(
    mac_key: bytes,
    *,
    bf_id: str,
    client_nonce: str,
    server_nonce: str,
    afb_public_key_pem: str,
) -> str:
    msg = (
        f"{ENROLL_CONTEXT}|afb2bf|{bf_id}|{client_nonce}|{server_nonce}|"
        f"{public_key_pem_hash(afb_public_key_pem)}"
    )
    return hmac.new(mac_key, msg.encode("utf-8"), hashlib.sha256).hexdigest()


def macs_equal(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)


def build_pairing_string(afb_ws_url: str, bf_id: str, token: str) -> str:
    payload = {"v": 1, "afb": afb_ws_url, "bf": bf_id, "tok": token}
    return PAIRING_STRING_PREFIX + _b64url_encode(canonical_json(payload).encode("utf-8"))


def parse_pairing_string(pairing_string: str) -> PairingInfo:
    s = str(pairing_string or "").strip()
    if not s.startswith(PAIRING_STRING_PREFIX):
        raise PairingStringError(f"pairing string must start with {PAIRING_STRING_PREFIX!r}")
    body = s[len(PAIRING_STRING_PREFIX):]
    try:
        data = json.loads(_b64url_decode(body).decode("utf-8"))
    except Exception as exc:
        raise PairingStringError("malformed pairing string") from exc
    if not isinstance(data, dict):
        raise PairingStringError("malformed pairing string")
    if data.get("v") != 1:
        raise PairingStringError(f"unsupported pairing string version: {data.get('v')!r}")
    afb_ws_url = data.get("afb")
    bf_id = data.get("bf")
    token = data.get("tok")
    if not isinstance(afb_ws_url, str) or not afb_ws_url:
        raise PairingStringError("missing afb ws_url")
    if not isinstance(bf_id, str) or not _BF_ID_RE.match(bf_id):
        raise PairingStringError("invalid bf_id")
    if not isinstance(token, str) or not _TOKEN_RE.match(token):
        raise PairingStringError("invalid pairing token")
    return PairingInfo(afb_ws_url=afb_ws_url, bf_id=bf_id, token=token)
