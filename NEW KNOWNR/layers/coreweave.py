"""
Coreweave — Integration and Expression Layer
=============================================
The Coreweave layer is the topmost layer of the KNOWNR system.  It
integrates all preceding layer outputs and, through the
:class:`~knownr.engines.echo_engine.EchoEngine` and
:class:`~knownr.engines.coreline_engine.CorelineEngine`, produces the
final identity expression during Phase 7: Coreweave Output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .shiftline import Shiftline


@dataclass
class Coreweave:
    """
    Integration and expression layer of the KNOWNR system.

    Attributes
    ----------
    shiftline : Shiftline
        The correction layer that feeds into final integration.
    integrated_signal : dict[str, Any]
        The fully integrated identity signal ready for expression.
    expression_output : str
        The formatted final expression string produced by the Echo Engine.
    woven : bool
        True after :meth:`weave` has been called.
    """

    shiftline: Shiftline
    integrated_signal: dict[str, Any] = field(default_factory=dict)
    expression_output: str = ""
    woven: bool = field(default=False, init=False)

    # ------------------------------------------------------------------
    # Phase 7 — Coreweave Output
    # ------------------------------------------------------------------

    def weave(
        self,
        integrated_signal: dict[str, Any],
        expression_output: str,
    ) -> "Coreweave":
        """
        Execute Phase 7: Coreweave Output.

        Receives the integrated signal and expression string from the
        Coreline Engine and marks the layer as woven.
        Returns *self* to support method chaining.

        Raises
        ------
        RuntimeError
            If the parent Shiftline has not been corrected.
        """
        if not self.shiftline.corrected:
            raise RuntimeError("Shiftline must be corrected before Coreweave output.")
        self.integrated_signal = integrated_signal
        self.expression_output = expression_output
        self.woven = True
        return self

    # ------------------------------------------------------------------

    def _root(self) -> Any:
        return self.shiftline.bindcore.formaxis.tracewell.pulseframe.rootline

    def __repr__(self) -> str:
        return (
            f"Coreweave(identity_id={self._root().identity_id!r}, "
            f"woven={self.woven}, "
            f"expression_output={self.expression_output!r})"
        )
