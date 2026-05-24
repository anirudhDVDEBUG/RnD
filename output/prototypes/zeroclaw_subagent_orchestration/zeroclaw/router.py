"""ZeroClaw Router — dispatches subtasks to specialized subagents."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .agents import AgentSpec, AgentResult


@dataclass
class RouterConfig:
    """Configuration for the ZeroClaw router."""
    agents: dict[str, AgentSpec] = field(default_factory=dict)
    strategy: str = "parallel_then_merge"  # "parallel_then_merge" | "sequential" | "fan_out_fan_in"
    max_workers: int = 4

    def register(self, agent: AgentSpec) -> None:
        self.agents[agent.name] = agent


class Router:
    """Routes subtasks to the correct subagent and collects results."""

    def __init__(self, config: RouterConfig):
        self.config = config

    def route(self, task_name: str) -> AgentSpec | None:
        """Find the best agent for a given task name."""
        # Direct match
        if task_name in self.config.agents:
            return self.config.agents[task_name]
        # Keyword match
        for name, agent in self.config.agents.items():
            if task_name.lower() in agent.role.lower():
                return agent
        return None

    def dispatch_parallel(self, subtasks: list[dict]) -> list[AgentResult]:
        """Run independent subtasks in parallel across agents."""
        results: list[AgentResult] = []
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as pool:
            futures = {}
            for st in subtasks:
                agent = self.route(st["agent"])
                if agent is None:
                    results.append(AgentResult(
                        agent_name=st["agent"],
                        agent_type="unknown",
                        status="error",
                        output={"error": f"No agent registered for '{st['agent']}'"},
                    ))
                    continue
                fut = pool.submit(agent.execute, st["task"], st.get("context"))
                futures[fut] = st

            for fut in as_completed(futures):
                results.append(fut.result())

        return results

    def dispatch_sequential(self, subtasks: list[dict]) -> list[AgentResult]:
        """Run subtasks one after another, passing each output as context to the next."""
        results: list[AgentResult] = []
        carry_context: dict = {}
        for st in subtasks:
            agent = self.route(st["agent"])
            if agent is None:
                results.append(AgentResult(
                    agent_name=st["agent"],
                    agent_type="unknown",
                    status="error",
                    output={"error": f"No agent registered for '{st['agent']}'"},
                ))
                continue
            ctx = {**carry_context, **(st.get("context") or {})}
            result = agent.execute(st["task"], ctx)
            results.append(result)
            carry_context["previous_output"] = result.output
        return results

    def dispatch(self, subtasks: list[dict]) -> list[AgentResult]:
        """Dispatch using the configured strategy."""
        if self.config.strategy == "sequential":
            return self.dispatch_sequential(subtasks)
        return self.dispatch_parallel(subtasks)
