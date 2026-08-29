"""
Evaluation Loop — Seven-Phase Identity Processing
===================================================
The EvaluationLoop orchestrates all seven KNOWNR phases in sequence:

  Phase 1  — Rootline Initialization
  Phase 2  — Pulseframe Reading
  Phase 3  — Tracewell Alignment
  Phase 4  — Formaxis Structuring
  Phase 5  — Bindcore Enforcement
  Phase 6  — Shiftline Correction
  Phase 7  — Coreweave Output

After completing Phase 7 the loop emits a
:class:`~knownr.evaluation.coreweave_packet.CoreweavePacket`.
"""

from __future__ import annotations

import logging
from typing import Any

from knownr.layers.rootline import Rootline
from knownr.layers.tracewell import Tracewell

from knownr.engines.pulse_engine import PulseEngine
from knownr.engines.trace_engine import TraceEngine
from knownr.engines.formaxis_engine import FormaxisEngine
from knownr.engines.bind_engine import BindEngine
from knownr.engines.drift_engine import DriftEngine
from knownr.engines.coreline_engine import CorelineEngine

from knownr.evaluation.coreweave_packet import CoreweavePacket

logger = logging.getLogger(__name__)


class EvaluationLoop:
    """
    Stateful driver that runs the seven-phase KNOWNR evaluation cycle.

    One ``EvaluationLoop`` instance is bound to a single identity
    (``identity_id``).  Calling :meth:`run_cycle` advances the cycle
    counter and returns a fresh :class:`~knownr.evaluation.coreweave_packet.CoreweavePacket`.

    Parameters
    ----------
    identity_id : str
        Unique identifier for the identity under evaluation.
    base_attributes : dict[str, Any]
        Initial attribute map seeded into the Rootline.
    pulse_engine : PulseEngine | None
        Custom Pulse Engine.  A default instance is created if *None*.
    trace_engine : TraceEngine | None
        Custom Trace Engine.
    formaxis_engine : FormaxisEngine | None
        Custom Formaxis Engine.
    bind_engine : BindEngine | None
        Custom Bind Engine.
    drift_engine : DriftEngine | None
        Custom Drift Engine.
    coreline_engine : CorelineEngine | None
        Custom Coreline Engine.
    """

    def __init__(
        self,
        identity_id: str,
        base_attributes: dict[str, Any] | None = None,
        pulse_engine: PulseEngine | None = None,
        trace_engine: TraceEngine | None = None,
        formaxis_engine: FormaxisEngine | None = None,
        bind_engine: BindEngine | None = None,
        drift_engine: DriftEngine | None = None,
        coreline_engine: CorelineEngine | None = None,
    ) -> None:
        self.identity_id = identity_id
        self.base_attributes: dict[str, Any] = base_attributes or {}

        # Engines — use defaults when not provided
        self.pulse_engine = pulse_engine or PulseEngine()
        self.trace_engine = trace_engine or TraceEngine()
        self.formaxis_engine = formaxis_engine or FormaxisEngine()
        self.bind_engine = bind_engine or BindEngine()
        self.drift_engine = drift_engine or DriftEngine()
        self.coreline_engine = coreline_engine or CorelineEngine()

        # Persistent Tracewell accumulates history across cycles
        self._rootline: Rootline | None = None
        self._tracewell: Tracewell | None = None
        self._cycle: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_cycle(
        self,
        attribute_updates: dict[str, Any] | None = None,
    ) -> CoreweavePacket:
        """
        Execute one full seven-phase evaluation cycle and return the
        resulting :class:`~knownr.evaluation.coreweave_packet.CoreweavePacket`.

        Parameters
        ----------
        attribute_updates:
            Optional dictionary of attribute changes to apply to the
            Rootline before this cycle's Pulseframe reading.

        Returns
        -------
        CoreweavePacket
        """
        self._cycle += 1
        logger.debug("EvaluationLoop: starting cycle %d for %r", self._cycle, self.identity_id)

        # ----------------------------------------------------------
        # Phase 1 — Rootline Initialization
        # ----------------------------------------------------------
        logger.debug("  Phase 1: Rootline Initialization")
        rootline = Rootline(
            identity_id=self.identity_id,
            base_attributes=dict(self.base_attributes),
        )
        if attribute_updates:
            for key, value in attribute_updates.items():
                rootline.set_base_attribute(key, value)
                self.base_attributes[key] = value  # persist for next cycle
        rootline.initialize()
        self._rootline = rootline

        # ----------------------------------------------------------
        # Phase 2 — Pulseframe Reading
        # ----------------------------------------------------------
        logger.debug("  Phase 2: Pulseframe Reading")
        pulseframe = self.pulse_engine.read_pulseframe(rootline)

        # ----------------------------------------------------------
        # Phase 3 — Tracewell Alignment
        # ----------------------------------------------------------
        logger.debug("  Phase 3: Tracewell Alignment")
        if self._tracewell is None:
            # First cycle — create the persistent Tracewell
            self._tracewell = Tracewell(pulseframe=pulseframe)
        else:
            # Subsequent cycles — swap in the new Pulseframe and realign
            self._tracewell.pulseframe = pulseframe
            self._tracewell.aligned = False  # reset for realignment
        self.trace_engine.align_tracewell(pulseframe, self._tracewell)

        # ----------------------------------------------------------
        # Phase 4 — Formaxis Structuring
        # ----------------------------------------------------------
        logger.debug("  Phase 4: Formaxis Structuring")
        formaxis = self.formaxis_engine.structure_formaxis(self._tracewell)

        # ----------------------------------------------------------
        # Phase 5 — Bindcore Enforcement
        # ----------------------------------------------------------
        logger.debug("  Phase 5: Bindcore Enforcement")
        bindcore = self.bind_engine.enforce_bindcore(formaxis)

        # ----------------------------------------------------------
        # Phase 6 — Shiftline Correction
        # ----------------------------------------------------------
        logger.debug("  Phase 6: Shiftline Correction")
        shiftline = self.drift_engine.correct_shiftline(bindcore)

        # ----------------------------------------------------------
        # Phase 7 — Coreweave Output
        # ----------------------------------------------------------
        logger.debug("  Phase 7: Coreweave Output")
        coreweave = self.coreline_engine.weave_coreweave(shiftline)

        # ----------------------------------------------------------
        # Emit Coreweave Packet
        # ----------------------------------------------------------
        packet = self._build_packet(coreweave)
        logger.debug("  Cycle %d complete: %s", self._cycle, packet.summary_line())
        return packet

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_packet(self, coreweave) -> CoreweavePacket:  # type: ignore[no-untyped-def]
        """Assemble a CoreweavePacket from the completed Coreweave layer."""
        sig = coreweave.integrated_signal
        rootline = coreweave.shiftline.bindcore.formaxis.tracewell.pulseframe.rootline

        stability_score = self._compute_stability(coreweave)

        identity_summary: dict[str, Any] = {
            "identity_id": sig["identity_id"],
            "base_attributes": sig["base_attributes"],
            "pulse_strength": sig["pulse_strength"],
        }

        drift_analysis: dict[str, Any] = {
            "drift_delta": sig["drift_delta"],
            "drift_compensated": sig["corrected_signal"].get("drift_compensated", False),
            "corrections_applied": sig["corrections_applied"],
        }

        continuity_trace: dict[str, Any] = {
            "continuity_score": sig["continuity_score"],
            "trace_depth": sig["trace_depth"],
        }

        return CoreweavePacket(
            identity_id=rootline.identity_id,
            identity_summary=identity_summary,
            stability_score=stability_score,
            drift_analysis=drift_analysis,
            continuity_trace=continuity_trace,
            expression_output=coreweave.expression_output,
            cycle=self._cycle,
        )

    @staticmethod
    def _compute_stability(coreweave) -> float:  # type: ignore[no-untyped-def]
        """
        Derive a composite stability score as the mean of the four
        primary layer scores.
        """
        sig = coreweave.integrated_signal
        scores = [
            sig["pulse_strength"],
            sig["continuity_score"],
            sig["structure_score"],
            sig["boundary_score"],
        ]
        return sum(scores) / len(scores)

    # ------------------------------------------------------------------

    @property
    def cycle(self) -> int:
        """Current (last completed) cycle number."""
        return self._cycle

    def __repr__(self) -> str:
        return (
            f"EvaluationLoop(identity_id={self.identity_id!r}, "
            f"cycle={self._cycle})"
        )
