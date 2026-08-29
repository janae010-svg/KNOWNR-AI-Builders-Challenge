"""
Formaxis — Structural Design Layer
=====================================
The Formaxis layer defines the structural schema that the identity signal
must conform to.  The :class:`~knownr.engines.formaxis_engine.FormaxisEngine`
applies structuring rules during Phase 4: Formaxis Structuring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .tracewell import Tracewell


@dataclass
class Formaxis:
    """
    Structural design layer of the KNOWNR system.

    Attributes
    ----------
    tracewell : Tracewell
        The continuity layer this Formaxis structures.
    structure_schema : dict[str, Any]
        Named structural rules applied to the identity signal.
    structure_score : float
        Compliance score in ``[0.0, 1.0]``.
    structured : bool
        True after :meth:`apply_structure` has been called.
    """

    tracewell: Tracewell
    structure_schema: dict[str, Any] = field(default_factory=dict)
    structure_score: float = 0.0
    structured: bool = field(default=False, init=False)

    # ------------------------------------------------------------------
    # Phase 4 — Formaxis Structuring
    # ------------------------------------------------------------------

    def apply_structure(
        self, structure_schema: dict[str, Any], structure_score: float
    ) -> "Formaxis":
        """
        Execute Phase 4: Formaxis Structuring.

        Records the structural schema and compliance score produced by
        the Formaxis Engine and marks the layer as structured.
        Returns *self* to support method chaining.

        Raises
        ------
        RuntimeError
            If the parent Tracewell has not been aligned.
        ValueError
            If ``structure_score`` is outside ``[0.0, 1.0]``.
        """
        if not self.tracewell.aligned:
            raise RuntimeError("Tracewell must be aligned before Formaxis structuring.")
        if not 0.0 <= structure_score <= 1.0:
            raise ValueError(f"structure_score must be in [0.0, 1.0], got {structure_score}.")
        self.structure_schema = structure_schema
        self.structure_score = structure_score
        self.structured = True
        return self

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Formaxis(identity_id="
            f"{self.tracewell.pulseframe.rootline.identity_id!r}, "
            f"structure_score={self.structure_score:.3f}, "
            f"structured={self.structured})"
        )
