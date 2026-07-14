"""afb_bf_protocol.enrollment — pairing token / MAC / pairing-string helpers.

The MAC test vectors are hardcoded to freeze the wire format: any accidental
change to the hashed strings (context, separator, field order) breaks these
tests instead of silently drifting between AFB and BF.
"""
from __future__ import annotations

import hmac

import pytest

from afb_bf_protocol.enrollment import (
    ENROLL_CONTEXT,
    PAIRING_STRING_PREFIX,
    PAIRING_TOKEN_PREFIX,
    PairingInfo,
    PairingStringError,
    build_pairing_string,
    derive_mac_key,
    enroll_request_mac,
    enroll_response_mac,
    generate_nonce,
    generate_pairing_token,
    macs_equal,
    pairing_token_hash,
    parse_pairing_string,
    public_key_pem_hash,
)

TOKEN = "bf1_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
MAC_KEY_HEX = "6811ba83d417ec1eba52c3c57dcdead5397ae025bf0e0e7741fc309d11956c1f"
REQUEST_MAC = "d47ddf73fa4ea1ad0014aa04c78be31d542e87aa0af267b6629d1c8f53ca7420"
RESPONSE_MAC = "69ce72d65f6eb57414dac1f228894b8453b180c951bb043d2704d47318e05753"


def test_generate_pairing_token_format():
    token = generate_pairing_token()
    assert token.startswith(PAIRING_TOKEN_PREFIX)
    body = token[len(PAIRING_TOKEN_PREFIX):]
    assert len(token) == 36
    assert len(body) == 32
    assert body == body.lower()
    assert all(c in "abcdefghijklmnopqrstuvwxyz234567" for c in body)


def test_generate_pairing_token_unique():
    assert generate_pairing_token() != generate_pairing_token()


def test_derive_mac_key_hardcoded_vector():
    assert derive_mac_key(TOKEN).hex() == MAC_KEY_HEX


def test_enroll_request_mac_hardcoded_vector():
    mac_key = bytes.fromhex(MAC_KEY_HEX)
    mac = enroll_request_mac(
        mac_key,
        bf_id="bf-test",
        client_nonce="client-nonce-1",
        bf_public_key_pem="PEM-BF-PUBLIC",
    )
    assert mac == REQUEST_MAC


def test_enroll_response_mac_hardcoded_vector():
    mac_key = bytes.fromhex(MAC_KEY_HEX)
    mac = enroll_response_mac(
        mac_key,
        bf_id="bf-test",
        client_nonce="client-nonce-1",
        server_nonce="server-nonce-1",
        afb_public_key_pem="PEM-AFB-PUBLIC",
    )
    assert mac == RESPONSE_MAC


def test_request_mac_differs_from_response_mac():
    assert REQUEST_MAC != RESPONSE_MAC


@pytest.mark.parametrize(
    "mutate",
    [
        lambda kw: {**kw, "bf_id": "bf-other"},
        lambda kw: {**kw, "client_nonce": "client-nonce-2"},
        lambda kw: {**kw, "bf_public_key_pem": "PEM-BF-PUBLIC-2"},
    ],
)
def test_enroll_request_mac_sensitive_to_inputs(mutate):
    mac_key = bytes.fromhex(MAC_KEY_HEX)
    base = {
        "bf_id": "bf-test",
        "client_nonce": "client-nonce-1",
        "bf_public_key_pem": "PEM-BF-PUBLIC",
    }
    assert enroll_request_mac(mac_key, **mutate(base)) != REQUEST_MAC


def test_enroll_request_mac_sensitive_to_key():
    other_key = derive_mac_key("bf1_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    mac = enroll_request_mac(
        other_key,
        bf_id="bf-test",
        client_nonce="client-nonce-1",
        bf_public_key_pem="PEM-BF-PUBLIC",
    )
    assert mac != REQUEST_MAC


def test_macs_equal_uses_compare_digest(monkeypatch):
    calls = []
    original = hmac.compare_digest

    def spy(a, b):
        calls.append((a, b))
        return original(a, b)

    monkeypatch.setattr(hmac, "compare_digest", spy)
    assert macs_equal("abc", "abc") is True
    assert macs_equal("abc", "abd") is False
    assert calls == [("abc", "abc"), ("abc", "abd")]


def test_generate_nonce_is_random_and_urlsafe():
    a, b = generate_nonce(), generate_nonce()
    assert a != b
    assert all(c not in a for c in "+/=")


def test_pairing_token_hash_is_sha256_hex():
    h = pairing_token_hash(TOKEN)
    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)


def test_public_key_pem_hash_sensitive_to_exact_string():
    assert public_key_pem_hash("PEM-A") != public_key_pem_hash("PEM-B")
    assert public_key_pem_hash("PEM-A") == public_key_pem_hash("PEM-A")


def test_pairing_string_roundtrip():
    s = build_pairing_string("ws://127.0.0.1:8013/bf/v1", "bf-test-pair", TOKEN)
    assert s.startswith(PAIRING_STRING_PREFIX)
    info = parse_pairing_string(s)
    assert info == PairingInfo(
        afb_ws_url="ws://127.0.0.1:8013/bf/v1", bf_id="bf-test-pair", token=TOKEN
    )


def test_parse_pairing_string_rejects_wrong_prefix():
    with pytest.raises(PairingStringError):
        parse_pairing_string("notaprefix_abc")


def test_parse_pairing_string_rejects_garbage_body():
    with pytest.raises(PairingStringError):
        parse_pairing_string(PAIRING_STRING_PREFIX + "!!!not-base64!!!")


def test_parse_pairing_string_rejects_wrong_version():
    from afb_bf_protocol.envelope import canonical_json

    import base64

    payload = {"v": 2, "afb": "ws://x", "bf": "bf-1", "tok": TOKEN}
    body = base64.urlsafe_b64encode(canonical_json(payload).encode()).rstrip(b"=").decode()
    with pytest.raises(PairingStringError):
        parse_pairing_string(PAIRING_STRING_PREFIX + body)


def test_parse_pairing_string_rejects_bad_bf_id():
    s = build_pairing_string("ws://127.0.0.1:8013/bf/v1", "bf id with spaces", TOKEN)
    with pytest.raises(PairingStringError):
        parse_pairing_string(s)


def test_parse_pairing_string_rejects_bad_token():
    s = build_pairing_string("ws://127.0.0.1:8013/bf/v1", "bf-test", "not-a-token")
    with pytest.raises(PairingStringError):
        parse_pairing_string(s)


def test_enroll_context_matches_documented_value():
    assert ENROLL_CONTEXT == "afb-bf-enroll.v1"
