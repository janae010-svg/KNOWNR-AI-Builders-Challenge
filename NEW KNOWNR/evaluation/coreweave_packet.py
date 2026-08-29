"""
Coreweave Packet — Final Evaluation Output
============================================
The CoreweavePacket is the structured output produced at the end of each
KNOWNR evaluation cycle.  It bundles the identity summary, stability
score, drift analysis, continuity trace, and the final expression output
into a single, portable record.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class CoreweavePacket:
    """
    Immutable output bundle produced by the
    :class:`~knownr.evaluation.evaluation_loop.EvaluationLoop` at the
    end of each evaluation cycle.

    Attributes
    ----------
    identity_id : str
        The unique identifier of the evaluated identity.
    identity_summary : dict[str, Any]
        Snapshot of base attributes and derived identity metadata.
    stability_score : float
        Composite score in ``[0.0, 1.0]`` reflecting overall identity
        stability across all seven layers.
    drift_analysis : dict[str, Any]
        Delta, compensation flag, and any drift corrections applied.
    continuity_trace : dict[str, Any]
        Continuity score and historical trace depth.
    expression_output : str
        The formatted final expression string from the Echo Engine.
    timestamp : str
        ISO-8601 UTC timestamp when the packet was created.
    cycle : int
        Evaluation cycle counter (1-based).
    """

    identity_id: str
    identity_summary: dict[str, Any]
    stability_score: float
    drift_analysis: dict[str, Any]
    continuity_trace: dict[str, Any]
    expression_output: str
    cycle: int = 1
    timestamp: str = field(
        default_factory=lambda: datetime.now(tz=timezone.utc).isoformat()
    )

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def is_stable(self, threshold: float = 0.7) -> bool:
        """
        Return True when ``stability_score`` meets or exceeds
        ``threshold``.

        Parameters
        ----------
        threshold:
            Minimum acceptable stability.  Defaults to ``0.7``.
        """
        return self.stability_score >= threshold

    def has_drift(self) -> bool:
        """Return True when meaningful drift was detected this cycle."""
        return self.drift_analysis.get("drift_compensated", False)

    def summary_line(self) -> str:
        """Return a compact one-line text summary of the packet."""
        stable_tag = "STABLE" if self.is_stable() else "UNSTABLE"
        drift_tag = "DRIFT" if self.has_drift() else "CLEAN"
        return (
            f"[Cycle {self.cycle}] {self.identity_id} | "
            f"stability={self.stability_score:.3f} {stable_tag} | "
            f"{drift_tag} | {self.timestamp}"
        )

    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialise the packet to a plain dictionary."""
        return {
            "identity_id": self.identity_id,
            "cycle": self.cycle,
            "timestamp": self.timestamp,
            "stability_score": self.stability_score,
            "identity_summary": self.identity_summary,
            "drift_analysis": self.drift_analysis,
            "continuity_trace": self.continuity_trace,
            "expression_output": self.expression_output,
        }

    def __repr__(self) -> str:
        return (
            f"CoreweavePacket(identity_id={self.identity_id!r}, "
            f"cycle={self.cycle}, "
            f"stability_score={self.stability_score:.3f})"
        )
