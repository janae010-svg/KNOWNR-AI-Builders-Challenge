"""
Drift Engine — Correction Logic
================================
The Drift Engine measures the deviation (drift) between the post-boundary
signal and the established continuity baseline, then produces a corrected
signal that is fed into the Shiftline layer.
Operates during Phase 6: Shiftline Correction.
"""

from __future__ import annotations

from typing import Any

from knownr.layers.bindcore import Bindcore
from knownr.layers.shiftline import Shiftline


class DriftEngine:
    """
    Detects identity drift by comparing the Bindcore boundary score
    against the Tracewell continuity score, applies corrections, and
    returns a :class:`~knownr.layers.shiftline.Shiftline`.

    Parameters
    ----------
    drift_threshold:
        Minimum absolute score difference considered meaningful drift.
        Defaults to ``0.1``.
    """

    def __init__(self, drift_threshold: float = 0.1) -> None:
        self.drift_threshold = drift_threshold

    # ------------------------------------------------------------------

    def correct_shiftline(self, bindcore: Bindcore) -> Shiftline:
        """
        Compute drift and produce a corrected
        :class:`~knownr.layers.shiftline.Shiftline`.

        Parameters
        ----------
        bindcore:
            An enforced :class:`~knownr.layers.bindcore.Bindcore`.

        Returns
        -------
        Shiftline
            A corrected Shiftline with ``corrected=True``.
        """
        continuity_score = bindcore.formaxis.tracewell.continuity_score
        boundary_score = bindcore.boundary_score
        drift_delta = abs(boundary_score - continuity_score)

        corrections: list[str] = []
        corrected_signal = self._build_corrected_signal(bindcore)

        if drift_delta >= self.drift_threshold:
            corrections.append(
                f"Drift of {drift_delta:.4f} detected "
                f"(boundary={boundary_score:.3f}, "
                f"continuity={continuity_score:.3f}); signal re-anchored."
            )
            corrected_signal["drift_compensated"] = True
            corrected_signal["drift_delta"] = drift_delta
        else:
            corrected_signal["drift_compensated"] = False
            corrected_signal["drift_delta"] = drift_delta

        shiftline = Shiftline(bindcore=bindcore)
        shiftline.correct(drift_delta, corrections, corrected_signal)
        return shiftline

    # ------------------------------------------------------------------

    def _build_corrected_signal(self, bindcore: Bindcore) -> dict[str, Any]:
        """Assemble the corrected signal from all prior layer scores."""
        rootline = bindcore.formaxis.tracewell.pulseframe.rootline
        return {
            "identity_id": rootline.identity_id,
            "base_attributes": dict(rootline.base_attributes),
            "pulse_strength": bindcore.formaxis.tracewell.pulseframe.pulse_strength,
            "continuity_score": bindcore.formaxis.tracewell.continuity_score,
            "structure_score": bindcore.formaxis.structure_score,
            "boundary_score": bindcore.boundary_score,
            "violations": list(bindcore.violations),
        }

    def __repr__(self) -> str:
        return f"DriftEngine(drift_threshold={self.drift_threshold})"
