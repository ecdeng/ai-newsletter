"""Point-in-time data layer for the historical case engine.

See ../SPEC.md for the full specification. The short version: every fact the
SEC serves carries the filing date of the document it came from, so "what did
the filings say on date T" is always reconstructible — which is what makes a
leak-free historical case possible without a commercial point-in-time licence.
"""

from . import case, client, comps  # noqa: F401

__all__ = ["client", "comps", "case"]
