"""Sign/verify roundtrip and example signature validity against the test keys."""
from __future__ import annotations

import json

import pytest

from afb_bf_protocol import (
    Envelope,
    MESSAGE_REGISTRY,
    generate_keypair,
    load_public_key,
    make_envelope,
    sign_envelope,
    verify_envelope,
)
from conftest import EXAMPLES

EXAMPLE_FILES = sorted(EXAMPLES.glob("*.json"))


def test_sign_verify_roundtrip():
    priv, pub = generate_keypair()
    env = make_envelope(
        sender="afb", recipient="bf-1", msg_type="deal.operation",
        payload={"operations": [{"deal_id": "d1", "revision": 1, "op": "activate"}]},
        key_id="k1",
    )
    sign_envelope(env, priv)
    verify_envelope(env, pub)  # no raise


def test_tampered_payload_fails():
    priv, pub = generate_keypair()
    env = make_envelope(
        sender="afb", recipient="bf-1", msg_type="session.hello_ack",
        payload={"a": 1}, key_id="k1",
    )
    sign_envelope(env, priv)
    env.payload["a"] = 2  # mutate after signing
    with pytest.raises(ValueError):
        verify_envelope(env, pub)


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.stem)
def test_example_signature_valid(path):
    afb_pub = load_public_key(EXAMPLES / "_keys" / "afb-public.pem")
    bf_pub = load_public_key(EXAMPLES / "_keys" / "bf-public.pem")
    env = Envelope.from_dict(json.loads(path.read_text()))
    meta = MESSAGE_REGISTRY[env.type]
    pub = afb_pub if meta.direction == "afb2bf" else bf_pub
    verify_envelope(env, pub)
