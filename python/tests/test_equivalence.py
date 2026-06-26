"""Byte-for-byte equivalence with the legacy BF and AFB implementations.

Guards against regressions while the two sides migrate onto this package: the
canonical JSON, payload_hash and signing string must be identical. Skipped if the
sibling AFB/BF checkouts are not present next to this repo.
"""
from __future__ import annotations

import glob
import importlib.util
import json
import os

import pytest

from afb_bf_protocol import Envelope, canonical_json, payload_hash, signing_string
from conftest import EXAMPLES, REPO_ROOT

APACK = REPO_ROOT.parent  # .../aPack
BF_ENV = APACK / "BF" / "belphegor" / "protocol" / "envelope.py"
AFB_PROTO = APACK / "AFB" / "backend" / "trade" / "protocol.py"

pytestmark = pytest.mark.skipif(
    not (BF_ENV.exists() and AFB_PROTO.exists()),
    reason="sibling AFB/BF checkouts not found",
)

PAYLOADS = sorted(glob.glob(str(EXAMPLES / "_payloads" / "*.json")))


def _load_bf():
    spec = importlib.util.spec_from_file_location("bf_envelope", BF_ENV)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_afb():
    src = AFB_PROTO.read_text().replace(
        "from .models import PROTOCOL_VERSION, ExecutionEnvelope",
        "PROTOCOL_VERSION='afb.execution.v1'",
    )
    ns: dict = {}
    exec(compile(src, "afb_protocol", "exec"), ns)
    return ns


@pytest.mark.parametrize("pf", PAYLOADS, ids=lambda p: os.path.basename(p)[:-5])
def test_canonical_and_hash_match_legacy(pf):
    bf = _load_bf()
    afb = _load_afb()
    payload = json.loads(open(pf).read())

    assert canonical_json(payload) == bf.canonical_json(payload)
    assert payload_hash(payload) == bf.payload_hash(payload)
    assert canonical_json(payload).encode("utf-8") == afb["canonical_json"](payload)
    assert payload_hash(payload) == afb["payload_hash"](payload)


@pytest.mark.parametrize("path", sorted(EXAMPLES.glob("*.json")), ids=lambda p: p.stem)
def test_signing_string_matches_afb(path):
    afb = _load_afb()
    env = Envelope.from_dict(json.loads(path.read_text()))
    afb_sig = afb["signing_string"](
        env.protocol, env.type, env.message_id, env.created_at, env.payload_hash
    ).decode()
    assert signing_string(env) == afb_sig
