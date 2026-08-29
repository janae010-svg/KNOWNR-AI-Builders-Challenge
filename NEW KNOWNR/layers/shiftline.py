"""
Shiftline — Correction Layer
==============================
The Shiftline layer applies drift corrections to the identity signal.
When the :class:`~knownr.engines.drift_engine.DriftEngine` detects
deviation from the stable baseline, Shiftline absorbs and compensates
during Phase 6: Shiftline Correction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .bindcore import Bindcore


@dataclass
class Shiftline:
    """
    Correction layer of the KNOWNR system.

    Attributes
    ----------
    bindcore : Bindcore
        The boundary layer that precedes correction.
    drift_delta : float
        Magnitude of detected drift (unsigned, ``>= 0.0``).
    corrections_applied : list[str]
        Human-readable descriptions of each correction applied.
    corrected_signal : dict[str, Any]
        The identity signal after drift compensation.
    corrected : bool
        True after :meth:`correct` has been called.
    """

    bindcore: Bindcore
    drift_delta: float = 0.0
    corrections_applied: list[str] = field(default_factory=list)
    corrected_signal: dict[str, Any] = field(default_factory=dict)
    corrected: bool = field(default=False, init=False)

    # ------------------------------------------------------------------
    # Phase 6 — Shiftline Correction
    # ------------------------------------------------------------------

    def correct(
        self,
        drift_delta: float,
        corrections_applied: list[str],
        corrected_signal: dict[str, Any],
    ) -> "Shiftline":
        """
        Execute Phase 6: Shiftline Correction.

        Records the drift magnitude, the list of corrections, and the
        post-correction signal produced by the Drift Engine.
        Returns *self* to support method chaining.

        Raises
        ------
        RuntimeError
            If the parent Bindcore has not been enforced.
        ValueError
            If ``drift_delta`` is negative.
        """
        if not self.bindcore.enforced:
            raise RuntimeError("Bindcore must be enforced before Shiftline correction.")
        if drift_delta < 0.0:
            raise ValueError(f"drift_delta must be >= 0.0, got {drift_delta}.")
        self.drift_delta = drift_delta
        self.corrections_applied = list(corrections_applied)
        self.corrected_signal = corrected_signal
        self.corrected = True
        return self

    # ------------------------------------------------------------------

    def has_drift(self) -> bool:
        """Return True when meaningful drift was detected (delta > 0)."""
        return self.drift_delta > 0.0

    def __repr__(self) -> str:
        return (
            f"Shiftline(identity_id="
            f"{self.bindcore.formaxis.tracewell.pulseframe.rootline.identity_id!r}, "
            f"drift_delta={self.drift_delta:.4f}, "
            f"corrections={len(self.corrections_applied)}, "
            f"corrected={self.corrected})"
        )
