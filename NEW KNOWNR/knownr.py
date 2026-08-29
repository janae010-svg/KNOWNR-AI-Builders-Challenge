"""
KNOWNR Prototype – IBM Bob Powered
Modular AI reasoning engine with typed stage contracts, role-based sovereignty,
real continuity validation, and structured extensibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Stage contracts — typed boundaries between every engine
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class IdentityResult:
    role: str
    intent: str
    context: dict = field(default_factory=dict)


@dataclass(frozen=True)
class SovereigntyResult:
    boundaries: list[str]
    constraints: list[str]
    validated_intent: str
    role: str


@dataclass(frozen=True)
class ArchitectResult:
    plan: str
    steps: list[str]
    constraints: list[str]
    role: str
    intent: str


@dataclass(frozen=True)
class ContinuityResult:
    continuity: bool
    notes: str
    validated_steps: list[str]
    warnings: list[str]


@dataclass(frozen=True)
class ExpressionResult:
    result: str
    role: str
    intent: str
    steps: list[str]
    warnings: list[str]
    constraints: list[str]


# ---------------------------------------------------------------------------
# Role policy registry — drives SovereigntyEngine
# ---------------------------------------------------------------------------

# Each role maps to (boundaries, constraints).  Add new roles here without
# touching any engine logic.
_ROLE_POLICIES: dict[str, tuple[list[str], list[str]]] = {
    "founder": (
        ["stay aligned with vision", "avoid premature scaling", "maintain clarity of purpose"],
        ["no context collapse", "no strategy fragmentation", "no unchecked pivot"],
    ),
    "operator": (
        ["stay within execution mandate", "preserve process integrity"],
        ["no scope creep", "no unauthorised priority change"],
    ),
    "advisor": (
        ["remain objective", "avoid direct execution bias"],
        ["no conflict of interest", "no undisclosed assumption"],
    ),
    "architect": (
        ["maintain system coherence", "document all dependencies"],
        ["no unreviewed structural change", "no hidden coupling"],
    ),
}

_DEFAULT_POLICY: tuple[list[str], list[str]] = (
    ["stay aligned", "avoid collapse", "maintain clarity"],
    ["no drift", "no fragmentation"],
)

# Required pipeline steps — ContinuityEngine validates these are present.
_REQUIRED_STEPS = [
    "Establish identity clarity",
    "Apply sovereignty boundaries",
    "Generate aligned decision pathway",
    "Produce structured output",
]


# ---------------------------------------------------------------------------
# Engine protocols — allow drop-in strategy substitution
# ---------------------------------------------------------------------------

@runtime_checkable
class IdentityEngineProtocol(Protocol):
    def interpret(self, scenario: dict) -> IdentityResult: ...


@runtime_checkable
class SovereigntyEngineProtocol(Protocol):
    def apply_rules(self, identity: IdentityResult) -> SovereigntyResult: ...


@runtime_checkable
class ArchitectEngineProtocol(Protocol):
    def orchestrate(self, identity: IdentityResult, sovereignty: SovereigntyResult) -> ArchitectResult: ...


@runtime_checkable
class ContinuityEngineProtocol(Protocol):
    def maintain(self, architect: ArchitectResult) -> ContinuityResult: ...


@runtime_checkable
class ExpressionModuleProtocol(Protocol):
    def express(self, continuity: ContinuityResult, architect: ArchitectResult) -> ExpressionResult: ...


# ---------------------------------------------------------------------------
# Default engine implementations
# ---------------------------------------------------------------------------

class IdentityEngine:
    """Parses and validates a scenario dict into a typed IdentityResult."""

    def interpret(self, scenario: dict) -> IdentityResult:
        role = str(scenario.get("role", "unknown")).strip() or "unknown"
        intent = str(scenario.get("intent", "unspecified")).strip() or "unspecified"
        context = scenario.get("context", {})
        if not isinstance(context, dict):
            context = {}
        return IdentityResult(role=role, intent=intent, context=context)


class SovereigntyEngine:
    """Applies role-aware policy boundaries and constraints."""

    def apply_rules(self, identity: IdentityResult) -> SovereigntyResult:
        key = identity.role.lower()
        boundaries, constraints = _ROLE_POLICIES.get(key, _DEFAULT_POLICY)

        # Context-driven constraint injection
        extra_constraints: list[str] = []
        priority = identity.context.get("priority", "").lower()
        if priority == "high":
            extra_constraints.append("escalate blockers immediately")
        if identity.context.get("confidential"):
            extra_constraints.append("restrict output to authorised recipients")

        return SovereigntyResult(
            boundaries=list(boundaries),
            constraints=list(constraints) + extra_constraints,
            validated_intent=identity.intent,
            role=identity.role,
        )


class ArchitectModeEngine:
    """Builds a structured, role-specific plan from identity and sovereignty data."""

    # Role-specific step libraries; fallback to defaults when role is unknown.
    _STEP_LIBRARY: dict[str, list[str]] = {
        "founder": [
            "Establish identity clarity",
            "Apply sovereignty boundaries",
            "Map strategic intent to near-term milestones",
            "Identify critical dependencies and risks",
            "Generate aligned decision pathway",
            "Produce structured output",
        ],
        "operator": [
            "Establish identity clarity",
            "Apply sovereignty boundaries",
            "Decompose intent into executable tasks",
            "Assign ownership and deadlines",
            "Generate aligned decision pathway",
            "Produce structured output",
        ],
        "architect": [
            "Establish identity clarity",
            "Apply sovereignty boundaries",
            "Audit current system state",
            "Model proposed structural changes",
            "Validate against sovereignty constraints",
            "Generate aligned decision pathway",
            "Produce structured output",
        ],
    }

    _DEFAULT_STEPS: list[str] = [
        "Establish identity clarity",
        "Apply sovereignty boundaries",
        "Generate aligned decision pathway",
        "Produce structured output",
    ]

    def orchestrate(
        self, identity: IdentityResult, sovereignty: SovereigntyResult
    ) -> ArchitectResult:
        key = identity.role.lower()
        steps = list(self._STEP_LIBRARY.get(key, self._DEFAULT_STEPS))

        plan = (
            f"Structured plan for {identity.role} "
            f"with intent '{identity.intent}' "
            f"under {len(sovereignty.constraints)} active constraint(s)."
        )

        return ArchitectResult(
            plan=plan,
            steps=steps,
            constraints=sovereignty.constraints,
            role=identity.role,
            intent=identity.intent,
        )


class ContinuityEngine:
    """Validates that the architect plan satisfies required pipeline integrity."""

    def maintain(self, architect: ArchitectResult) -> ContinuityResult:
        missing = [s for s in _REQUIRED_STEPS if s not in architect.steps]
        warnings: list[str] = []

        if missing:
            warnings.append(f"Missing required steps: {missing}")

        if not architect.constraints:
            warnings.append("No sovereignty constraints active — reasoning may be unconstrained.")

        if architect.intent.lower() in ("", "unspecified"):
            warnings.append("Intent is unspecified — plan may lack direction.")

        continuity = len(missing) == 0
        notes = (
            "No collapse detected. Reasoning remains aligned."
            if continuity
            else f"Continuity breach: {len(missing)} required step(s) absent."
        )

        return ContinuityResult(
            continuity=continuity,
            notes=notes,
            validated_steps=architect.steps,
            warnings=warnings,
        )


class ExpressionModule:
    """Produces a structured, content-derived output from the full pipeline."""

    def express(
        self, continuity: ContinuityResult, architect: ArchitectResult
    ) -> ExpressionResult:
        status = "aligned and sovereign" if continuity.continuity else "misaligned — review required"
        result = (
            f"[{architect.role.upper()}] Reasoning pipeline {status}. "
            f"Intent: '{architect.intent}'. "
            f"{len(architect.steps)} step(s) planned, "
            f"{len(architect.constraints)} constraint(s) active."
        )

        return ExpressionResult(
            result=result,
            role=architect.role,
            intent=architect.intent,
            steps=continuity.validated_steps,
            warnings=continuity.warnings,
            constraints=architect.constraints,
        )


# ---------------------------------------------------------------------------
# KnownrSystem — pipeline orchestrator with stage-level error handling
# ---------------------------------------------------------------------------

class KnownrSystem:
    """
    Orchestrates the full KNOWNR reasoning pipeline.

    Each engine is injected at construction time, making the system fully
    testable and extensible — swap any engine by passing a conforming
    implementation to __init__.
    """

    def __init__(
        self,
        identity_engine: IdentityEngineProtocol | None = None,
        sovereignty_engine: SovereigntyEngineProtocol | None = None,
        architect_engine: ArchitectEngineProtocol | None = None,
        continuity_engine: ContinuityEngineProtocol | None = None,
        expression_module: ExpressionModuleProtocol | None = None,
    ) -> None:
        self.identity = identity_engine or IdentityEngine()
        self.sovereignty = sovereignty_engine or SovereigntyEngine()
        self.architect = architect_engine or ArchitectModeEngine()
        self.continuity = continuity_engine or ContinuityEngine()
        self.expression = expression_module or ExpressionModule()

    def run(self, scenario: dict) -> ExpressionResult:
        stages = [
            ("IdentityEngine",       lambda: self.identity.interpret(scenario)),
            ("SovereigntyEngine",    lambda identity: self.sovereignty.apply_rules(identity)),
            ("ArchitectModeEngine",  lambda identity, sov: self.architect.orchestrate(identity, sov)),
            ("ContinuityEngine",     lambda arch: self.continuity.maintain(arch)),
            ("ExpressionModule",     lambda cont, arch: self.expression.express(cont, arch)),
        ]

        try:
            identity_result: IdentityResult = stages[0][1]()
            sovereignty_result: SovereigntyResult = stages[1][1](identity_result)
            architect_result: ArchitectResult = stages[2][1](identity_result, sovereignty_result)
            continuity_result: ContinuityResult = stages[3][1](architect_result)
            expression_result: ExpressionResult = stages[4][1](continuity_result, architect_result)
        except Exception as exc:
            raise RuntimeError(
                f"KNOWNR pipeline failed at stage '{exc.__class__.__name__}': {exc}"
            ) from exc

        return expression_result


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    scenarios = [
        {
            "role": "Founder",
            "intent": "Design next workflow",
            "context": {"priority": "high"},
        },
        {
            "role": "Architect",
            "intent": "Refactor data layer",
            "context": {"confidential": True},
        },
        {
            "role": "Operator",
            "intent": "Deploy release candidate",
            "context": {"priority": "high", "confidential": False},
        },
    ]

    system = KnownrSystem()

    for scenario in scenarios:
        print(f"\n{'-' * 60}")
        output = system.run(scenario)
        print(f"Result   : {output.result}")
        print(f"Steps    : {output.steps}")
        print(f"Constraints: {output.constraints}")
        if output.warnings:
            print(f"Warnings : {output.warnings}")
