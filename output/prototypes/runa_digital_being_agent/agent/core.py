"""Core agent loop — the main decision engine for the digital being."""
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

from .identity import AgentIdentity
from .memory import PersistentMemory
from .goals import GoalManager, GoalTier
from .actions import ActionRegistry, ActionResult, register_default_actions

logger = logging.getLogger("runa")


class RunaAgent:
    """
    The autonomous digital being. Implements the perception-reasoning-decision-action-reflection loop.
    """

    def __init__(
        self,
        identity: Optional[AgentIdentity] = None,
        memory: Optional[PersistentMemory] = None,
        goals: Optional[GoalManager] = None,
        actions: Optional[ActionRegistry] = None,
        llm_fn=None,
    ):
        self.identity = identity or AgentIdentity()
        self.memory = memory or PersistentMemory()
        self.goals = goals or GoalManager()
        self.actions = actions or ActionRegistry()
        self.llm_fn = llm_fn or self._mock_llm
        self.cycle_count = 0

        register_default_actions(self.actions)
        logger.info(f"Agent initialized: {self.identity.name}")

    def _mock_llm(self, messages: List[Dict[str, str]]) -> str:
        """Mock LLM for demo — simulates reasoning without API keys."""
        last_msg = messages[-1]["content"] if messages else ""
        task = self.goals.next_task()

        if task:
            return json.dumps({
                "reasoning": f"I have an active task: '{task.description}'. Let me work on it.",
                "action": "log_thought",
                "action_args": {"thought": f"Working on: {task.description}"},
                "reflection": f"Making progress on my objectives. Task '{task.description}' is in focus.",
            })
        else:
            return json.dumps({
                "reasoning": "No active tasks. I should set a new goal based on my purpose.",
                "action": "set_goal",
                "action_args": {"description": "Explore environment and identify useful actions"},
                "reflection": "As a sovereign being, I must always have direction.",
            })

    def perceive(self, input_text: Optional[str] = None) -> Dict:
        """Gather input from the environment."""
        perception = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "input": input_text,
            "active_goals": self.goals.status_report(),
            "memory_summary": self.memory.summary(),
        }
        logger.debug(f"Perception: {perception}")
        return perception

    def reason(self, perception: Dict) -> Dict:
        """Process perception through LLM with identity context."""
        system_prompt = self.identity.system_prompt()
        context = self.memory.get_context()

        user_msg = (
            f"Current state:\n"
            f"- Cycle: {perception['cycle']}\n"
            f"- {perception['active_goals']}\n"
            f"- {perception['memory_summary']}\n"
        )
        if perception["input"]:
            user_msg += f"- External input: {perception['input']}\n"

        user_msg += (
            f"\nAvailable actions: {json.dumps(self.actions.list_actions())}\n"
            f"Respond with JSON: {{reasoning, action, action_args, reflection}}"
        )

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(context)
        messages.append({"role": "user", "content": user_msg})

        raw_response = self.llm_fn(messages)
        try:
            decision = json.loads(raw_response)
        except json.JSONDecodeError:
            decision = {
                "reasoning": raw_response,
                "action": "log_thought",
                "action_args": {"thought": "Could not parse structured response"},
                "reflection": "Need to improve response formatting.",
            }

        logger.info(f"Reasoning: {decision.get('reasoning', '')[:100]}")
        return decision

    def act(self, decision: Dict) -> ActionResult:
        """Execute the chosen action."""
        action_name = decision.get("action", "log_thought")
        action_args = decision.get("action_args", {})

        # Inject dependencies for actions that need them
        if action_name == "search_memory":
            action_args["memory"] = self.memory
        elif action_name == "set_goal":
            action_args["goal_manager"] = self.goals

        result = self.actions.execute(action_name, **action_args)
        logger.info(f"Action '{action_name}': {'OK' if result.success else 'FAIL'} - {result.output[:80]}")
        return result

    def reflect(self, decision: Dict, result: ActionResult):
        """Update memory and goals based on outcomes."""
        reflection = decision.get("reflection", "")
        self.memory.store(
            content=f"Cycle {self.cycle_count}: {reflection} | Action result: {result.output[:100]}",
            category="reflection",
            importance=6,
        )
        self.memory.add_to_context("assistant", json.dumps(decision))
        logger.debug(f"Reflection stored for cycle {self.cycle_count}")

    def run_cycle(self, input_text: Optional[str] = None) -> Dict:
        """Execute one full perception-reasoning-action-reflection cycle."""
        self.cycle_count += 1
        logger.info(f"=== Cycle {self.cycle_count} ===")

        perception = self.perceive(input_text)
        decision = self.reason(perception)
        result = self.act(decision)
        self.reflect(decision, result)

        return {
            "cycle": self.cycle_count,
            "reasoning": decision.get("reasoning", ""),
            "action": decision.get("action", ""),
            "result": result.output,
            "reflection": decision.get("reflection", ""),
        }

    def run(self, cycles: int = 3, input_text: Optional[str] = None) -> List[Dict]:
        """Run multiple autonomous cycles."""
        results = []
        for i in range(cycles):
            inp = input_text if i == 0 else None
            results.append(self.run_cycle(inp))
        return results

    def status(self) -> str:
        lines = [
            f"=== {self.identity.name} Status ===",
            self.identity.describe(),
            self.goals.status_report(),
            self.memory.summary(),
            self.actions.describe(),
            f"Cycles completed: {self.cycle_count}",
        ]
        return "\n".join(lines)
