"""afb-bf-protocol — shared wire protocol for AFB (OMS) and BF (executor).

Single source of truth for the ``afb.execution.v1`` envelope: models, canonical
JSON / hashing, Ed25519 signing, envelope-level validation, message taxonomy and
the shared ``deal_state.v2`` schema. The AsyncAPI spec in ``spec/`` is the canon
for message shapes; the JSON Schemas there validate payloads.
"""
from __future__ import annotations

from .version import PROTOCOL_VERSION, __version__
from .models import Envelope, Signature, ExecutionDeal
from .envelope import (
    canonical_json,
    payload_hash,
    signing_string,
    signing_string_parts,
    parse_iso_datetime,
    make_envelope,
)
from .signing import (
    sign_envelope,
    verify_envelope,
    load_private_key,
    load_public_key,
    generate_keypair,
    export_private_key_pem,
    export_public_key_pem,
    ensure_dev_keypair,
    b64url_encode,
    b64url_decode,
)
from .validation import (
    ProtocolValidationError,
    validate_envelope_fields,
    validate_envelope_shape,
    ReplayCache,
)
from .taxonomy import (
    MessageMeta,
    MESSAGE_REGISTRY,
    ALL_MESSAGE_TYPES,
    COMMAND_TYPES,
    BF_EVENT_TYPES,
    PERSISTED_BF_EVENT_TYPES,
    split_category_type,
    SUPPORTED_MARKETS,
)
from .deal_state import (
    DealState,
    DealStatus,
    safe_deal_filename,
    archived_deal_filename,
    set_now_iso,
    current_now_iso,
)

__all__ = [
    "PROTOCOL_VERSION",
    "__version__",
    "Envelope",
    "Signature",
    "ExecutionDeal",
    "canonical_json",
    "payload_hash",
    "signing_string",
    "signing_string_parts",
    "parse_iso_datetime",
    "make_envelope",
    "sign_envelope",
    "verify_envelope",
    "load_private_key",
    "load_public_key",
    "generate_keypair",
    "export_private_key_pem",
    "export_public_key_pem",
    "ensure_dev_keypair",
    "b64url_encode",
    "b64url_decode",
    "ProtocolValidationError",
    "validate_envelope_fields",
    "validate_envelope_shape",
    "ReplayCache",
    "MessageMeta",
    "MESSAGE_REGISTRY",
    "ALL_MESSAGE_TYPES",
    "COMMAND_TYPES",
    "BF_EVENT_TYPES",
    "PERSISTED_BF_EVENT_TYPES",
    "split_category_type",
    "SUPPORTED_MARKETS",
    "DealState",
    "DealStatus",
    "safe_deal_filename",
    "archived_deal_filename",
    "set_now_iso",
    "current_now_iso",
]
