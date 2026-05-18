"""Action registry — extensible plugin system for agent capabilities."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class ActionResult:
    success: bool
    output: str
    side_effects: List[str] = None

    def __post_init__(self):
        if self.side_effects is None:
            self.side_effects = []


class ActionRegistry:
    """Plugin-based action system. Register callables the agent can invoke."""

    def __init__(self):
        self._actions: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, fn: Callable, description: str = "", requires_confirmation: bool = False):
        self._actions[name] = {
            "fn": fn,
            "description": description,
            "requires_confirmation": requires_confirmation,
        }

    def execute(self, name: str, **kwargs) -> ActionResult:
        if name not in self._actions:
            return ActionResult(success=False, output=f"Unknown action: {name}")
        try:
            result = self._actions[name]["fn"](**kwargs)
            return ActionResult(success=True, output=str(result))
        except Exception as e:
            return ActionResult(success=False, output=f"Error: {e}")

    def list_actions(self) -> List[Dict[str, str]]:
        return [
            {"name": name, "description": info["description"]}
            for name, info in self._actions.items()
        ]

    def describe(self) -> str:
        lines = ["Available actions:"]
        for name, info in self._actions.items():
            lines.append(f"  - {name}: {info['description']}")
        return "\n".join(lines)


# Built-in actions for the demo
def action_log_thought(thought: str) -> str:
    """Log an internal thought."""
    return f"[Thought logged] {thought}"


def action_search_memory(query: str, memory=None) -> str:
    """Search agent memory."""
    if memory is None:
        return "No memory system available."
    results = memory.recall(query)
    if not results:
        return "No relevant memories found."
    return json.dumps(results, indent=2)


def action_set_goal(description: str, goal_manager=None) -> str:
    """Create a new goal."""
    if goal_manager is None:
        return "No goal manager available."
    goal = goal_manager.add_goal(description)
    return f"Created goal: {goal.id} - {goal.description}"


def action_reflect(observation: str) -> str:
    """Reflect on an observation and derive insight."""
    return f"[Reflection] Observed: {observation}. Integrating into world model."


def register_default_actions(registry: ActionRegistry):
    """Register the built-in action set."""
    registry.register("log_thought", action_log_thought, "Log an internal thought")
    registry.register("reflect", action_reflect, "Reflect on an observation")
    registry.register("search_memory", action_search_memory, "Search past memories")
    registry.register("set_goal", action_set_goal, "Set a new goal")
