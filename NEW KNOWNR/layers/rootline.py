"""
Rootline — Foundation Layer
============================
The Rootline is the lowest layer of the KNOWNR identity stability system.
It establishes the immutable base identity record from which all higher layers
derive their signal. A Rootline must be initialized before any evaluation
cycle can begin (Phase 1: Rootline Initialization).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Rootline:
    """
    Foundation layer of the KNOWNR system.

    Attributes
    ----------
    identity_id : str
        A unique identifier anchoring this identity record.
    base_attributes : dict[str, Any]
        Immutable key/value pairs that define the raw identity foundation.
    initialized : bool
        Set to True after :meth:`initialize` completes successfully.
    """

    identity_id: str
    base_attributes: dict[str, Any] = field(default_factory=dict)
    initialized: bool = field(default=False, init=False)

    # ------------------------------------------------------------------
    # Phase 1 — Rootline Initialization
    # ------------------------------------------------------------------

    def initialize(self) -> "Rootline":
        """
        Execute Phase 1: Rootline Initialization.

        Validates that ``identity_id`` is non-empty and marks the layer
        as initialized.  Returns *self* to support method chaining.

        Raises
        ------
        ValueError
            If ``identity_id`` is empty or blank.
        """
        if not self.identity_id or not self.identity_id.strip():
            raise ValueError("Rootline.identity_id must be a non-empty string.")
        self.initialized = True
        return self

    # ------------------------------------------------------------------

    def set_base_attribute(self, key: str, value: Any) -> None:
        """Add or update a single base attribute on the foundation layer."""
        self.base_attributes[key] = value

    def get_base_attribute(self, key: str, default: Any = None) -> Any:
        """Retrieve a base attribute by key."""
        return self.base_attributes.get(key, default)

    def __repr__(self) -> str:
        return (
            f"Rootline(identity_id={self.identity_id!r}, "
            f"initialized={self.initialized}, "
            f"base_attributes={list(self.base_attributes.keys())})"
        )
