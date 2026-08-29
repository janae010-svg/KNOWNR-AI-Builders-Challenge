"""
Bind Engine — Boundary Enforcement
=====================================
The Bind Engine evaluates the structured Formaxis layer against a set of
boundary rules, detecting violations and computing a boundary compliance
score.  Operates during Phase 5: Bindcore Enforcement.
"""

from __future__ import annotations

from typing import Any

from knownr.layers.formaxis import Formaxis
from knownr.layers.bindcore import Bindcore


class BindEngine:
    """
    Enforces identity boundaries defined in a rule set and produces a
    :class:`~knownr.layers.bindcore.Bindcore` layer.

    Parameters
    ----------
    default_rules:
        Boundary rules applied when none are passed to
        :meth:`enforce_bindcore`.
    """

    DEFAULT_RULES: dict[str, Any] = {
        "min_structure_score": 0.5,
        "max_violations_allowed": 0,
    }

    def __init__(self, default_rules: dict[str, Any] | None = None) -> None:
        self.default_rules = default_rules or dict(self.DEFAULT_RULES)

    # ------------------------------------------------------------------

    def enforce_bindcore(
        self,
        formaxis: Formaxis,
        rules: dict[str, Any] | None = None,
    ) -> Bindcore:
        """
        Apply boundary rules to ``formaxis`` and return an enforced
        :class:`~knownr.layers.bindcore.Bindcore`.

        Parameters
        ----------
        formaxis:
            A structured :class:`~knownr.layers.formaxis.Formaxis`.
        rules:
            Optional override rule set.

        Returns
        -------
        Bindcore
            An enforced Bindcore with ``enforced=True``.
        """
        active_rules = rules if rules is not None else self.default_rules
        violations = self._detect_violations(formaxis, active_rules)
        boundary_score = self._compute_boundary_score(formaxis, violations, active_rules)

        bindcore = Bindcore(formaxis=formaxis)
        bindcore.enforce(active_rules, boundary_score, violations)
        return bindcore

    # ------------------------------------------------------------------

    def _detect_violations(
        self, formaxis: Formaxis, rules: dict[str, Any]
    ) -> list[str]:
        violations: list[str] = []
        min_score: float = rules.get("min_structure_score", 0.0)
        if formaxis.structure_score < min_score:
            violations.append(
                f"structure_score {formaxis.structure_score:.3f} "
                f"below minimum {min_score:.3f}"
            )
        return violations

    def _compute_boundary_score(
        self,
        formaxis: Formaxis,
        violations: list[str],
        rules: dict[str, Any],
    ) -> float:
        max_allowed: int = rules.get("max_violations_allowed", 0)
        if violations:
            excess = max(0, len(violations) - max_allowed)
            penalty = excess * 0.25
            return max(0.0, formaxis.structure_score - penalty)
        return formaxis.structure_score

    def __repr__(self) -> str:
        return f"BindEngine(default_rules={list(self.default_rules.keys())})"
