"""
Pulseframe — Identity Signal Layer
====================================
The Pulseframe captures the live identity signal emitted by a Rootline
foundation.  It holds the current pulse reading produced by the
:class:`~knownr.engines.pulse_engine.PulseEngine` during
Phase 2: Pulseframe Reading.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .rootline import Rootline


@dataclass
class Pulseframe:
    """
    Identity signal layer of the KNOWNR system.

    Attributes
    ----------
    rootline : Rootline
        The foundation layer this Pulseframe reads from.
    pulse_reading : dict[str, Any]
        Raw signal values produced during the Pulseframe Reading phase.
    pulse_strength : float
        Normalised signal strength in the range ``[0.0, 1.0]``.
    read : bool
        True after :meth:`capture_pulse` has been called.
    """

    rootline: Rootline
    pulse_reading: dict[str, Any] = field(default_factory=dict)
    pulse_strength: float = 0.0
    read: bool = field(default=False, init=False)

    # ------------------------------------------------------------------
    # Phase 2 — Pulseframe Reading
    # ------------------------------------------------------------------

    def capture_pulse(self, pulse_reading: dict[str, Any], pulse_strength: float) -> "Pulseframe":
        """
        Execute Phase 2: Pulseframe Reading.

        Stores the signal values emitted by the Pulse Engine and marks
        the layer as read.  Returns *self* to support method chaining.

        Parameters
        ----------
        pulse_reading:
            Key/value signal data produced by the Pulse Engine.
        pulse_strength:
            Normalised strength value ``[0.0, 1.0]``.

        Raises
        ------
        RuntimeError
            If the parent Rootline has not been initialized.
        ValueError
            If ``pulse_strength`` is outside ``[0.0, 1.0]``.
        """
        if not self.rootline.initialized:
            raise RuntimeError("Rootline must be initialized before capturing a Pulseframe.")
        if not 0.0 <= pulse_strength <= 1.0:
            raise ValueError(f"pulse_strength must be in [0.0, 1.0], got {pulse_strength}.")
        self.pulse_reading = pulse_reading
        self.pulse_strength = pulse_strength
        self.read = True
        return self

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Pulseframe(identity_id={self.rootline.identity_id!r}, "
            f"pulse_strength={self.pulse_strength:.3f}, "
            f"read={self.read})"
        )
