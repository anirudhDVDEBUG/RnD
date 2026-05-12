"""
Goalkeeper: Contract-driven goal execution with a judge that gates
completion against an explicit Definition of Done (DoD).

This module demonstrates the pattern locally without requiring any API keys.
It uses a rule-based judge that inspects artifacts to verify DoD criteria.
"""

import json
import os
import re
import textwrap
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class CriterionStatus(Enum):
    PENDING = "pending"
    PASS = "pass"
    FAIL = "fail"


@dataclass
class Criterion:
    description: str
    status: CriterionStatus = CriterionStatus.PENDING
    feedback: str = ""
    verifier: Callable | None = None  # optional programmatic check


@dataclass
class Goal:
    title: str
    description: str
    criteria: list[Criterion] = field(default_factory=list)
    artifacts: dict = field(default_factory=dict)  # produced work products
    iteration: int = 0
    max_iterations: int = 5

    @property
    def is_complete(self) -> bool:
        return all(c.status == CriterionStatus.PASS for c in self.criteria)

    def summary(self) -> str:
        lines = [f"Goal: {self.title}", f"  {self.description}", ""]
        lines.append("Definition of Done:")
        for i, c in enumerate(self.criteria, 1):
            icon = {"pass": "[PASS]", "fail": "[FAIL]", "pending": "[    ]"}[c.status.value]
            lines.append(f"  {icon} {i}. {c.description}")
            if c.feedback:
                lines.append(f"         -> {c.feedback}")
        return "\n".join(lines)


class Judge:
    """Independent judge that evaluates each DoD criterion against artifacts."""

    def evaluate(self, goal: Goal) -> Goal:
        """Run every criterion's verifier against the goal's artifacts."""
        goal.iteration += 1
        print(f"\n--- Judge Evaluation (iteration {goal.iteration}) ---")
        for criterion in goal.criteria:
            if criterion.verifier:
                try:
                    passed, feedback = criterion.verifier(goal.artifacts)
                    criterion.status = CriterionStatus.PASS if passed else CriterionStatus.FAIL
                    criterion.feedback = feedback
                except Exception as e:
                    criterion.status = CriterionStatus.FAIL
                    criterion.feedback = f"Verifier error: {e}"
            else:
                criterion.status = CriterionStatus.FAIL
                criterion.feedback = "No verifier attached"
        print(goal.summary())
        return goal


class GoalkeeperEngine:
    """Orchestrates plan -> execute -> judge loop until DoD is met."""

    def __init__(self):
        self.judge = Judge()

    def run(self, goal: Goal, executor: Callable) -> Goal:
        """
        Run the goal to completion:
          1. Execute work (produces/updates artifacts)
          2. Judge evaluates artifacts against DoD
          3. If any criterion fails and iterations remain, loop back to 1
        """
        print("=" * 60)
        print(f"GOALKEEPER: Starting goal '{goal.title}'")
        print("=" * 60)
        print(goal.summary())

        while not goal.is_complete and goal.iteration < goal.max_iterations:
            # Identify what still needs work
            failed = [
                c for c in goal.criteria
                if c.status != CriterionStatus.PASS
            ]
            print(f"\n>>> Executor: working on {len(failed)} pending/failed criteria...")

            # Execute work
            goal = executor(goal)

            # Judge
            goal = self.judge.evaluate(goal)

            if goal.is_complete:
                print("\n*** ALL CRITERIA PASSED -- Goal complete! ***")
                return goal

        if not goal.is_complete:
            print(f"\n!!! Max iterations ({goal.max_iterations}) reached. Goal incomplete. !!!")

        return goal
