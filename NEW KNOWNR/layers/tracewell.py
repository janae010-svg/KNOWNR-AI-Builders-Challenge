"""
Tracewell — Continuity Layer
==============================
The Tracewell accumulates a historical trace of identity signals, enabling
the :class:`~knownr.engines.trace_engine.TraceEngine` to evaluate continuity
across evaluation cycles.  Activated during Phase 3: Tracewell Alignment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .pulseframe import Pulseframe


@dataclass
class Tracewell:
    """
    Continuity layer of the KNOWNR system.

    Attributes
    ----------
    pulseframe : Pulseframe
        The current identity signal layer being traced.
    trace_history : list[dict[str, Any]]
        Ordered log of past pulse readings, oldest first.
    continuity_score : float
        Continuity metric in ``[0.0, 1.0]``.  Higher is more stable.
    aligned : bool
        True after :meth:`align` has been called.
    """

    pulseframe: Pulseframe
    trace_history: list[dict[str, Any]] = field(default_factory=list)
    continuity_score: float = 0.0
    aligned: bool = field(default=False, init=False)

    # ------------------------------------------------------------------
    # Phase 3 — Tracewell Alignment
    # ------------------------------------------------------------------

    def align(self, continuity_score: float) -> "Tracewell":
        """
        Execute Phase 3: Tracewell Alignment.

        Appends the current pulse reading to ``trace_history``, records
        the given ``continuity_score``, and marks the layer aligned.
        Returns *self* to support method chaining.

        Raises
        ------
        RuntimeError
            If the parent Pulseframe has not been read.
        ValueError
            If ``continuity_score`` is outside ``[0.0, 1.0]``.
        """
        if not self.pulseframe.read:
            raise RuntimeError("Pulseframe must be read before Tracewell alignment.")
        if not 0.0 <= continuity_score <= 1.0:
            raise ValueError(f"continuity_score must be in [0.0, 1.0], got {continuity_score}.")
        self.trace_history.append(dict(self.pulseframe.pulse_reading))
        self.continuity_score = continuity_score
        self.aligned = True
        return self

    # ------------------------------------------------------------------

    def get_trace_depth(self) -> int:
        """Return the number of recorded trace entries."""
        return len(self.trace_history)

    def __repr__(self) -> str:
        return (
            f"Tracewell(identity_id={self.pulseframe.rootline.identity_id!r}, "
            f"continuity_score={self.continuity_score:.3f}, "
            f"trace_depth={self.get_trace_depth()}, "
            f"aligned={self.aligned})"
        )
