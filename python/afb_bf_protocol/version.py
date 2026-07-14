"""Protocol and package versions.

``PROTOCOL_VERSION`` is the value carried in the envelope ``protocol`` field and
is the wire-compatibility contract. ``__version__`` is the semver of this package
(and the git tag), tracked separately — see ``VERSIONING.md`` at the repo root.
"""
from __future__ import annotations

# Wire protocol version (envelope.protocol). Bump the trailing vN only on a
# breaking wire change (MAJOR).
PROTOCOL_VERSION = "afb.execution.v1"

# Package/spec semver. Keep in sync with python/pyproject.toml [project].version
# and the git tag.
__version__ = "1.12.0"
