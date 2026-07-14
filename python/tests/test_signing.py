"""afb_bf_protocol.signing — key IO, envelope sign/verify, key_fingerprint."""
from __future__ import annotations

from afb_bf_protocol.signing import key_fingerprint, load_public_key
from conftest import EXAMPLES

# Hardcoded so an accidental change to the fingerprint formula (DER vs PEM,
# hash, truncation length) breaks this test instead of silently drifting.
AFB_PUBLIC_KEY_FINGERPRINT = "f998f76a4644"


def test_key_fingerprint_hardcoded_vector():
    pub = load_public_key(EXAMPLES / "_keys" / "afb-public.pem")
    assert key_fingerprint(pub) == AFB_PUBLIC_KEY_FINGERPRINT


def test_key_fingerprint_length():
    pub = load_public_key(EXAMPLES / "_keys" / "afb-public.pem")
    assert len(key_fingerprint(pub)) == 12


def test_key_fingerprint_differs_between_keys():
    afb_pub = load_public_key(EXAMPLES / "_keys" / "afb-public.pem")
    bf_pub = load_public_key(EXAMPLES / "_keys" / "bf-public.pem")
    assert key_fingerprint(afb_pub) != key_fingerprint(bf_pub)


def test_key_fingerprint_deterministic():
    pub = load_public_key(EXAMPLES / "_keys" / "afb-public.pem")
    assert key_fingerprint(pub) == key_fingerprint(pub)
