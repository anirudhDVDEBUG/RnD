"""Hierarchical goal management for autonomous agent."""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import json
import os


class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    DEFERRED = "deferred"


class GoalTier(str, Enum):
    ASPIRATION = "aspiration"  # Long-term (identity-level)
    OBJECTIVE = "objective"    # Medium-term (weeks)
    TASK = "task"              # Immediate (next action)


@dataclass
class Goal:
    description: str
    tier: GoalTier
    status: GoalStatus = GoalStatus.ACTIVE
    progress: float = 0.0
    sub_goals: List[str] = field(default_factory=list)
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "tier": self.tier.value,
            "status": self.status.value,
            "progress": self.progress,
            "sub_goals": self.sub_goals,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Goal":
        return cls(
            id=data.get("id"),
            description=data["description"],
            tier=GoalTier(data["tier"]),
            status=GoalStatus(data.get("status", "active")),
            progress=data.get("progress", 0.0),
            sub_goals=data.get("sub_goals", []),
        )


class GoalManager:
    """Manages a hierarchy of goals the agent autonomously pursues."""

    def __init__(self, storage_path: str = "logs/goals.json"):
        self.storage_path = storage_path
        self.goals: List[Goal] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                self.goals = [Goal.from_dict(g) for g in data.get("goals", [])]

    def save(self):
        os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({"goals": [g.to_dict() for g in self.goals]}, f, indent=2)

    def add_goal(self, description: str, tier: GoalTier = GoalTier.TASK) -> Goal:
        goal = Goal(
            id=f"goal_{len(self.goals)+1}",
            description=description,
            tier=tier,
        )
        self.goals.append(goal)
        self.save()
        return goal

    def get_active_goals(self, tier: Optional[GoalTier] = None) -> List[Goal]:
        return [
            g for g in self.goals
            if g.status == GoalStatus.ACTIVE
            and (tier is None or g.tier == tier)
        ]

    def complete_goal(self, goal_id: str):
        for g in self.goals:
            if g.id == goal_id:
                g.status = GoalStatus.COMPLETED
                g.progress = 1.0
                self.save()
                return g
        return None

    def next_task(self) -> Optional[Goal]:
        """Get the highest-priority immediate task."""
        tasks = self.get_active_goals(GoalTier.TASK)
        return tasks[0] if tasks else None

    def status_report(self) -> str:
        active = self.get_active_goals()
        completed = [g for g in self.goals if g.status == GoalStatus.COMPLETED]
        lines = [f"Goals: {len(active)} active, {len(completed)} completed"]
        for g in active:
            lines.append(f"  [{g.tier.value}] {g.description} ({g.progress*100:.0f}%)")
        return "\n".join(lines)
