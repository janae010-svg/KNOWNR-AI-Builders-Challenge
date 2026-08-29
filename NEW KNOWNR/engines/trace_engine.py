"""
Trace Engine — Continuity Tracking
=====================================
The Trace Engine evaluates how consistently the current Pulseframe
signal aligns with prior traces recorded in a Tracewell.  It produces
a continuity score used in Phase 3: Tracewell Alignment.
"""

from __future__ import annotations

from knownr.layers.pulseframe import Pulseframe
from knownr.layers.tracewell import Tracewell


class TraceEngine:
    """
    Computes a continuity score by comparing the current
    :class:`~knownr.layers.pulseframe.Pulseframe` against the
    :class:`~knownr.layers.tracewell.Tracewell` history.
    """

    #: Continuity score assigned when there is no prior history to compare.
    BASELINE_SCORE: float = 1.0

    def align_tracewell(self, pulseframe: Pulseframe, tracewell: Tracewell) -> Tracewell:
        """
        Align the ``tracewell`` against the current ``pulseframe``.

        Parameters
        ----------
        pulseframe:
            A read :class:`~knownr.layers.pulseframe.Pulseframe`.
        tracewell:
            The :class:`~knownr.layers.tracewell.Tracewell` accumulating
            this identity's history.

        Returns
        -------
        Tracewell
            The aligned tracewell with ``aligned=True``.

        Raises
        ------
        RuntimeError
            If the Pulseframe has not been read.
        """
        if not pulseframe.read:
            raise RuntimeError("TraceEngine requires a read Pulseframe.")

        continuity_score = self._compute_continuity(pulseframe, tracewell)
        tracewell.align(continuity_score)
        return tracewell

    # ------------------------------------------------------------------

    def _compute_continuity(
        self, pulseframe: Pulseframe, tracewell: Tracewell
    ) -> float:
        """
        Compare the current pulse strength against the mean strength of
        past readings to derive a continuity score.
        """
        history = tracewell.trace_history
        if not history:
            return self.BASELINE_SCORE

        # Use attribute_count as a lightweight proxy for signal identity.
        current_count: int = pulseframe.pulse_reading.get("attribute_count", 0)
        past_counts = [entry.get("attribute_count", 0) for entry in history]
        mean_past = sum(past_counts) / len(past_counts)

        if mean_past == 0:
            return self.BASELINE_SCORE

        ratio = current_count / mean_past
        # Clamp to [0.0, 1.0]; ratio > 1 also indicates divergence.
        return min(ratio, 1.0) if ratio <= 1.0 else max(0.0, 2.0 - ratio)

    def __repr__(self) -> str:
        return "TraceEngine()"
