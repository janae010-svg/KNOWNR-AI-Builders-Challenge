"""
Echo Engine — Expression Formatting
======================================
The Echo Engine takes a corrected Shiftline signal and formats it into
a human-readable expression string.  This string becomes the
``expression_output`` field of the
:class:`~knownr.layers.coreweave.Coreweave` layer.
"""

from __future__ import annotations

from knownr.layers.shiftline import Shiftline


class EchoEngine:
    """
    Formats the corrected identity signal into a final expression string.

    Parameters
    ----------
    template:
        A Python format string that receives the corrected signal
        dictionary as keyword arguments.  Defaults to a built-in
        human-readable format.
    """

    DEFAULT_TEMPLATE = (
        "[KNOWNR EXPRESSION] identity_id={identity_id} | "
        "pulse={pulse_strength:.3f} | "
        "continuity={continuity_score:.3f} | "
        "structure={structure_score:.3f} | "
        "boundary={boundary_score:.3f} | "
        "drift={drift_delta:.4f} | "
        "drift_compensated={drift_compensated}"
    )

    def __init__(self, template: str | None = None) -> None:
        self.template = template or self.DEFAULT_TEMPLATE

    # ------------------------------------------------------------------

    def format_expression(self, shiftline: Shiftline) -> str:
        """
        Produce the final expression string from the Shiftline signal.

        Parameters
        ----------
        shiftline:
            A corrected :class:`~knownr.layers.shiftline.Shiftline`.

        Returns
        -------
        str
            The formatted expression string.

        Raises
        ------
        RuntimeError
            If the Shiftline has not been corrected.
        """
        if not shiftline.corrected:
            raise RuntimeError("EchoEngine requires a corrected Shiftline.")
        return self.template.format(**shiftline.corrected_signal)

    def __repr__(self) -> str:
        return "EchoEngine()"
