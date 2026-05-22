"""Data models for agent profiles, routing rules, and workflows."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentProfile:
    agent: str
    strengths: list[str] = field(default_factory=list)
    context_window: str = "medium"
    preferred_tasks: list[str] = field(default_factory=list)

    def match_score(self, task_description: str) -> float:
        """Score how well this agent matches a task based on strengths and preferred tasks."""
        task_lower = task_description.lower()
        score = 0.0
        for strength in self.strengths:
            if strength.lower() in task_lower:
                score += 2.0
        for pref in self.preferred_tasks:
            if pref.lower() in task_lower:
                score += 1.5
        return score


@dataclass
class RoutingRule:
    pattern: str
    route_to: str
    priority: str = "medium"

    @property
    def priority_weight(self) -> int:
        return {"high": 3, "medium": 2, "low": 1}.get(self.priority, 2)


@dataclass
class HookConfig:
    pre_task: list[dict[str, str]] = field(default_factory=list)
    post_task: list[dict[str, str]] = field(default_factory=list)
    handoff: list[dict[str, str]] = field(default_factory=list)


@dataclass
class WorkflowStep:
    agent: str
    task: str
    input_path: Optional[str] = None
    output_path: Optional[str] = None


@dataclass
class Workflow:
    name: str
    steps: list[WorkflowStep] = field(default_factory=list)
