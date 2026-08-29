"""
Formaxis Engine — Structural Shaping
=======================================
The Formaxis Engine applies a structural schema to the aligned Tracewell,
evaluating how well the identity signal conforms to the expected form.
Operates during Phase 4: Formaxis Structuring.
"""

from __future__ import annotations

from typing import Any

from knownr.layers.tracewell import Tracewell
from knownr.layers.formaxis import Formaxis


class FormaxisEngine:
    """
    Shapes the identity signal by applying structural rules from a
    schema and computing a structure compliance score.

    Parameters
    ----------
    default_schema:
        The structural schema applied when none is passed to
        :meth:`structure_formaxis`.  Defaults to a minimal schema.
    """

    DEFAULT_SCHEMA: dict[str, Any] = {
        "requires_identity_id": True,
        "requires_attributes": False,
        "min_continuity_score": 0.0,
    }

    def __init__(self, default_schema: dict[str, Any] | None = None) -> None:
        self.default_schema = default_schema or dict(self.DEFAULT_SCHEMA)

    # ------------------------------------------------------------------

    def structure_formaxis(
        self,
        tracewell: Tracewell,
        schema: dict[str, Any] | None = None,
    ) -> Formaxis:
        """
        Apply structural rules to the ``tracewell`` and return a
        populated :class:`~knownr.layers.formaxis.Formaxis`.

        Parameters
        ----------
        tracewell:
            An aligned :class:`~knownr.layers.tracewell.Tracewell`.
        schema:
            Optional override schema.  Falls back to ``default_schema``.

        Returns
        -------
        Formaxis
            A structured Formaxis with ``structured=True``.
        """
        active_schema = schema if schema is not None else self.default_schema
        structure_score = self._evaluate_schema(tracewell, active_schema)
        formaxis = Formaxis(tracewell=tracewell)
        formaxis.apply_structure(active_schema, structure_score)
        return formaxis

    # ------------------------------------------------------------------

    def _evaluate_schema(
        self, tracewell: Tracewell, schema: dict[str, Any]
    ) -> float:
        """Score the tracewell against each schema rule."""
        checks_passed = 0
        total_checks = 0

        if schema.get("requires_identity_id"):
            total_checks += 1
            if tracewell.pulseframe.rootline.identity_id:
                checks_passed += 1

        if schema.get("requires_attributes"):
            total_checks += 1
            if tracewell.pulseframe.rootline.base_attributes:
                checks_passed += 1

        min_cont: float = schema.get("min_continuity_score", 0.0)
        total_checks += 1
        if tracewell.continuity_score >= min_cont:
            checks_passed += 1

        return checks_passed / total_checks if total_checks > 0 else 1.0

    def __repr__(self) -> str:
        return f"FormaxisEngine(default_schema={list(self.default_schema.keys())})"
