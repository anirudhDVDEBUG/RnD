"""
ERPAVal Workflow Engine — orchestrates the six-phase autonomous development
cycle: Explore -> Research -> Plan -> Act -> Validate -> Compound.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Any

from classifier import classify_task, Classification
from lessons_store import (
    load_lessons, add_lesson, search_lessons, format_lessons, Lesson,
)


PHASES = ["explore", "research", "plan", "act", "validate", "compound"]


@dataclass
class PhaseResult:
    phase: str
    summary: str
    artifacts: Dict[str, Any] = field(default_factory=dict)
    skipped: bool = False


@dataclass
class WorkflowRun:
    task: str
    classification: Classification
    results: List[PhaseResult] = field(default_factory=list)
    lessons_added: List[Lesson] = field(default_factory=list)

    @property
    def succeeded(self) -> bool:
        return all(not r.skipped or r.phase == "research" for r in self.results)


class ERPAValWorkflow:
    """
    Runs the six-phase ERPAVal cycle. Each phase is a pluggable callback;
    defaults use mock implementations suitable for demonstration.
    """

    def __init__(self, lessons_path: Optional[str] = None,
                 phase_handlers: Optional[Dict[str, Callable]] = None):
        self.lessons_path = lessons_path
        self.handlers: Dict[str, Callable] = phase_handlers or {}

    # ---------- default phase implementations (mock) ----------

    def _default_explore(self, task: str, classification: Classification,
                         prior: List[PhaseResult]) -> PhaseResult:
        return PhaseResult(
            phase="explore",
            summary=f"Scanned codebase for areas related to: {task}",
            artifacts={
                "files_examined": ["src/auth.py", "src/config.py", "tests/test_auth.py"],
                "observations": [
                    "Auth module uses session-based tokens with 30s default TTL",
                    "Config loaded from environment variables at startup",
                ],
            },
        )

    def _default_research(self, task: str, classification: Classification,
                          prior: List[PhaseResult]) -> PhaseResult:
        existing = search_lessons(task, self.lessons_path)
        return PhaseResult(
            phase="research",
            summary="Searched lessons store and codebase patterns",
            artifacts={
                "prior_lessons": format_lessons(existing),
                "patterns_found": [
                    "Retry decorator used in src/api_client.py",
                    "Timeout constants centralised in src/config.py",
                ],
            },
        )

    def _default_plan(self, task: str, classification: Classification,
                      prior: List[PhaseResult]) -> PhaseResult:
        return PhaseResult(
            phase="plan",
            summary="Created implementation plan",
            artifacts={
                "steps": [
                    "1. Update DEFAULT_TIMEOUT in src/config.py from 30 to 60",
                    "2. Add retry wrapper to auth.login() in src/auth.py:45",
                    "3. Add unit test for timeout + retry in tests/test_auth.py",
                ],
                "validation_criteria": [
                    "All existing tests pass",
                    "New test covers retry on timeout",
                ],
                "rollback": "Revert config constant and remove retry decorator",
            },
        )

    def _default_act(self, task: str, classification: Classification,
                     prior: List[PhaseResult]) -> PhaseResult:
        plan = next((r for r in prior if r.phase == "plan"), None)
        steps_done = []
        if plan:
            for step in plan.artifacts.get("steps", []):
                steps_done.append(f"[done] {step}")
        return PhaseResult(
            phase="act",
            summary="Executed planned changes",
            artifacts={"changes_applied": steps_done},
        )

    def _default_validate(self, task: str, classification: Classification,
                          prior: List[PhaseResult]) -> PhaseResult:
        return PhaseResult(
            phase="validate",
            summary="All checks passed",
            artifacts={
                "tests_run": 42,
                "tests_passed": 42,
                "tests_failed": 0,
                "regression_check": "PASS",
                "diff_review": "No unintended changes detected",
            },
        )

    def _default_compound(self, task: str, classification: Classification,
                          prior: List[PhaseResult]) -> PhaseResult:
        lesson = add_lesson(
            task=task,
            category="pattern",
            insight=f"Completed '{task}' via ERPAVal cycle; "
                    f"classifier routed as {classification.task_type.value}.",
            tags=[classification.task_type.value, "erpaval"],
            path=self.lessons_path,
        )
        return PhaseResult(
            phase="compound",
            summary="Lesson captured in store",
            artifacts={"lesson": lesson.insight},
        )

    # ---------- orchestration ----------

    _DEFAULTS = {
        "explore": "_default_explore",
        "research": "_default_research",
        "plan": "_default_plan",
        "act": "_default_act",
        "validate": "_default_validate",
        "compound": "_default_compound",
    }

    def run(self, task: str, verbose: bool = True) -> WorkflowRun:
        classification = classify_task(task)
        workflow = WorkflowRun(task=task, classification=classification)

        if verbose:
            _print_header(task, classification)

        for phase in PHASES:
            handler = self.handlers.get(phase)
            if handler is None:
                handler = getattr(self, self._DEFAULTS[phase])

            result = handler(task, classification, workflow.results)
            workflow.results.append(result)

            if verbose:
                _print_phase(result, phase in classification.emphasized_phases)

        if verbose:
            _print_footer(workflow)

        return workflow


# ---------- display helpers ----------

def _print_header(task: str, c: Classification):
    print("=" * 64)
    print("  ERPAVal Workflow")
    print("=" * 64)
    print(f"  Task        : {task}")
    print(f"  Classified  : {c.task_type.value} (confidence {c.confidence:.0%})")
    print(f"  Entry phase : {c.entry_phase}")
    print(f"  Emphasis    : {', '.join(c.emphasized_phases)}")
    print(f"  Reasoning   : {c.reasoning}")
    print("-" * 64)


def _print_phase(result: PhaseResult, emphasized: bool):
    marker = " ** " if emphasized else "    "
    tag = "[EMPHASIS]" if emphasized else ""
    print(f"\n{marker}Phase: {result.phase.upper()} {tag}")
    print(f"    Summary: {result.summary}")
    if result.artifacts:
        for key, val in result.artifacts.items():
            if isinstance(val, list):
                print(f"    {key}:")
                for item in val:
                    print(f"      - {item}")
            else:
                print(f"    {key}: {val}")


def _print_footer(workflow: WorkflowRun):
    print("\n" + "=" * 64)
    status = "SUCCESS" if workflow.succeeded else "NEEDS ATTENTION"
    print(f"  Workflow complete — {status}")
    print(f"  Phases executed: {len(workflow.results)}")
    print("=" * 64)
