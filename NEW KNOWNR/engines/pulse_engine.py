"""
Pulse Engine — Identity Evaluation
=====================================
The Pulse Engine reads a Rootline foundation and produces a pulse reading
(a dictionary of signal values) together with a normalised pulse strength.
It is the first engine invoked in the KNOWNR evaluation cycle.
"""

from __future__ import annotations

from typing import Any

from knownr.layers.rootline import Rootline
from knownr.layers.pulseframe import Pulseframe


class PulseEngine:
    """
    Evaluates the identity signal from a :class:`~knownr.layers.rootline.Rootline`.

    The Pulse Engine is responsible for translating raw base attributes
    into a structured pulse reading and assigning a pulse strength score.
    """

    # ------------------------------------------------------------------
    # Engine parameters
    # ------------------------------------------------------------------

    #: Default pulse strength assigned when all base attributes are present.
    DEFAULT_STRENGTH: float = 0.85

    def __init__(self, strength_override: float | None = None) -> None:
        """
        Parameters
        ----------
        strength_override:
            When provided, the engine uses this fixed strength value
            instead of computing one dynamically.
        """
        self.strength_override = strength_override

    # ------------------------------------------------------------------
    # Primary operation
    # ------------------------------------------------------------------

    def read_pulseframe(self, rootline: Rootline) -> Pulseframe:
        """
        Produce a :class:`~knownr.layers.pulseframe.Pulseframe` from the
        given ``rootline``.

        Parameters
        ----------
        rootline:
            An initialized :class:`~knownr.layers.rootline.Rootline`.

        Returns
        -------
        Pulseframe
            A Pulseframe with the pulse reading captured and ``read=True``.

        Raises
        ------
        RuntimeError
            If the Rootline has not been initialized.
        """
        if not rootline.initialized:
            raise RuntimeError("PulseEngine requires an initialized Rootline.")

        pulse_reading = self._build_pulse_reading(rootline)
        pulse_strength = self._compute_strength(rootline)

        pulseframe = Pulseframe(rootline=rootline)
        pulseframe.capture_pulse(pulse_reading, pulse_strength)
        return pulseframe

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_pulse_reading(self, rootline: Rootline) -> dict[str, Any]:
        """Derive a pulse reading dictionary from the Rootline attributes."""
        return {
            "identity_id": rootline.identity_id,
            "attribute_count": len(rootline.base_attributes),
            "attributes_snapshot": dict(rootline.base_attributes),
        }

    def _compute_strength(self, rootline: Rootline) -> float:
        """Return the pulse strength for this Rootline."""
        if self.strength_override is not None:
            return self.strength_override
        # Attenuate slightly when no base attributes are provided.
        if not rootline.base_attributes:
            return 0.5
        return self.DEFAULT_STRENGTH

    def __repr__(self) -> str:
        return f"PulseEngine(strength_override={self.strength_override})"
