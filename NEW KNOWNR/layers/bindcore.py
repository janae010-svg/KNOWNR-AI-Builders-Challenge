"""
Bindcore — Boundary Layer
===========================
The Bindcore layer enforces identity boundaries, preventing structural
overflow or signal contamination.  The
:class:`~knownr.engines.bind_engine.BindEngine` applies boundary rules
during Phase 5: Bindcore Enforcement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .formaxis import Formaxis


@dataclass
class Bindcore:
    """
    Boundary layer of the KNOWNR system.

    Attributes
    ----------
    formaxis : Formaxis
        The structural layer this Bindcore constrains.
    boundary_rules : dict[str, Any]
        Named rules that define the permissible identity boundary.
    boundary_score : float
        Boundary compliance score in ``[0.0, 1.0]``.
    violations : list[str]
        Descriptions of any boundary violations detected.
    enforced : bool
        True after :meth:`enforce` has been called.
    """

    formaxis: Formaxis
    boundary_rules: dict[str, Any] = field(default_factory=dict)
    boundary_score: float = 0.0
    violations: list[str] = field(default_factory=list)
    enforced: bool = field(default=False, init=False)

    # ------------------------------------------------------------------
    # Phase 5 — Bindcore Enforcement
    # ------------------------------------------------------------------

    def enforce(
        self,
        boundary_rules: dict[str, Any],
        boundary_score: float,
        violations: list[str] | None = None,
    ) -> "Bindcore":
        """
        Execute Phase 5: Bindcore Enforcement.

        Applies boundary rules produced by the Bind Engine, records any
        violations, and marks the layer as enforced.
        Returns *self* to support method chaining.

        Raises
        ------
        RuntimeError
            If the parent Formaxis has not been structured.
        ValueError
            If ``boundary_score`` is outside ``[0.0, 1.0]``.
        """
        if not self.formaxis.structured:
            raise RuntimeError("Formaxis must be structured before Bindcore enforcement.")
        if not 0.0 <= boundary_score <= 1.0:
            raise ValueError(f"boundary_score must be in [0.0, 1.0], got {boundary_score}.")
        self.boundary_rules = boundary_rules
        self.boundary_score = boundary_score
        self.violations = list(violations) if violations else []
        self.enforced = True
        return self

    # ------------------------------------------------------------------

    def is_clean(self) -> bool:
        """Return True when no boundary violations were recorded."""
        return len(self.violations) == 0

    def __repr__(self) -> str:
        return (
            f"Bindcore(identity_id="
            f"{self.formaxis.tracewell.pulseframe.rootline.identity_id!r}, "
            f"boundary_score={self.boundary_score:.3f}, "
            f"violations={len(self.violations)}, "
            f"enforced={self.enforced})"
        )
