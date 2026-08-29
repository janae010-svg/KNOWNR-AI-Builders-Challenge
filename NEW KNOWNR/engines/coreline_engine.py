"""
Coreline Engine — Integration and Output
==========================================
The Coreline Engine is the final engine in the KNOWNR pipeline.  It
integrates all layer outputs, calls the
:class:`~knownr.engines.echo_engine.EchoEngine` to format the expression,
and returns a completed :class:`~knownr.layers.coreweave.Coreweave` layer.
"""

from __future__ import annotations

from typing import Any

from knownr.layers.shiftline import Shiftline
from knownr.layers.coreweave import Coreweave
from knownr.engines.echo_engine import EchoEngine


class CorelineEngine:
    """
    Integrates all prior layer outputs and weaves them into a final
    :class:`~knownr.layers.coreweave.Coreweave` expression.

    Parameters
    ----------
    echo_engine:
        The :class:`~knownr.engines.echo_engine.EchoEngine` used to
        format the expression.  A default instance is created when
        *None* is passed.
    """

    def __init__(self, echo_engine: EchoEngine | None = None) -> None:
        self.echo_engine = echo_engine or EchoEngine()

    # ------------------------------------------------------------------

    def weave_coreweave(self, shiftline: Shiftline) -> Coreweave:
        """
        Produce a woven :class:`~knownr.layers.coreweave.Coreweave` layer
        from a corrected ``shiftline``.

        Parameters
        ----------
        shiftline:
            A corrected :class:`~knownr.layers.shiftline.Shiftline`.

        Returns
        -------
        Coreweave
            A fully woven Coreweave with ``woven=True``.
        """
        integrated_signal = self._integrate(shiftline)
        expression_output = self.echo_engine.format_expression(shiftline)

        coreweave = Coreweave(shiftline=shiftline)
        coreweave.weave(integrated_signal, expression_output)
        return coreweave

    # ------------------------------------------------------------------

    def _integrate(self, shiftline: Shiftline) -> dict[str, Any]:
        """Merge all layer-level scores into a single integrated record."""
        bindcore = shiftline.bindcore
        formaxis = bindcore.formaxis
        tracewell = formaxis.tracewell
        pulseframe = tracewell.pulseframe
        rootline = pulseframe.rootline

        return {
            "identity_id": rootline.identity_id,
            "base_attributes": dict(rootline.base_attributes),
            "pulse_strength": pulseframe.pulse_strength,
            "continuity_score": tracewell.continuity_score,
            "trace_depth": tracewell.get_trace_depth(),
            "structure_score": formaxis.structure_score,
            "boundary_score": bindcore.boundary_score,
            "violations": list(bindcore.violations),
            "drift_delta": shiftline.drift_delta,
            "corrections_applied": list(shiftline.corrections_applied),
            "corrected_signal": dict(shiftline.corrected_signal),
        }

    def __repr__(self) -> str:
        return f"CorelineEngine(echo_engine={self.echo_engine!r})"
