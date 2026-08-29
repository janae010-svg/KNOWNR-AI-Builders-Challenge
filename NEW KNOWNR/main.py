"""
KNOWNR -- Main Entry Point
===========================
Demonstrates a full multi-cycle identity evaluation using the
KNOWNR seven-layer, seven-engine pipeline.

Run:
    python -m knownr.main
or:
    python knownr/main.py
"""

from __future__ import annotations

import logging
import json

from knownr.evaluation.evaluation_loop import EvaluationLoop

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-8s %(name)s -- %(message)s",
)
logger = logging.getLogger("knownr.main")


def run_demo() -> None:
    """Run three evaluation cycles against a sample identity."""

    print("\n" + "=" * 72)
    print("  KNOWNR -- Identity Stability Evaluation System")
    print("=" * 72 + "\n")

    # ------------------------------------------------------------------
    # Bootstrap: create the evaluation loop for identity "SUBJECT-001"
    # ------------------------------------------------------------------
    loop = EvaluationLoop(
        identity_id="SUBJECT-001",
        base_attributes={
            "name": "Orin Vaelus",
            "origin": "Coreweave Sector 7",
            "class": "Pulsebound",
            "stability_tier": "A",
        },
    )

    # ------------------------------------------------------------------
    # Cycle 1 -- Baseline evaluation
    # ------------------------------------------------------------------
    print("-- Cycle 1: Baseline evaluation ------------------------------------------")
    packet_1 = loop.run_cycle()
    _print_packet(packet_1)

    # ------------------------------------------------------------------
    # Cycle 2 -- Attribute update (simulated identity shift)
    # ------------------------------------------------------------------
    print("\n-- Cycle 2: Identity attribute shift -------------------------------------")
    packet_2 = loop.run_cycle(
        attribute_updates={
            "stability_tier": "B",
            "active_phase": "transition",
        }
    )
    _print_packet(packet_2)

    # ------------------------------------------------------------------
    # Cycle 3 -- Recovery / stabilisation
    # ------------------------------------------------------------------
    print("\n-- Cycle 3: Recovery / re-stabilisation ----------------------------------")
    packet_3 = loop.run_cycle(
        attribute_updates={
            "stability_tier": "A",
            "active_phase": "stable",
        }
    )
    _print_packet(packet_3)

    print("\n" + "=" * 72)
    print("  Evaluation complete.  Packets serialised below.")
    print("=" * 72 + "\n")

    packets = [packet_1.to_dict(), packet_2.to_dict(), packet_3.to_dict()]
    print(json.dumps(packets, indent=2))


def _print_packet(packet) -> None:  # type: ignore[no-untyped-def]
    """Pretty-print a CoreweavePacket to stdout."""
    print(f"  Summary  : {packet.summary_line()}")
    print(f"  Stable?  : {packet.is_stable()}")
    print(f"  Has Drift: {packet.has_drift()}")
    print("  Expression:")
    print(f"    {packet.expression_output}")


if __name__ == "__main__":
    run_demo()
