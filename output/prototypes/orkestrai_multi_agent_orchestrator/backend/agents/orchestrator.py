"""Central orchestrator agent that decomposes tasks and delegates to specialists."""

from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.llm_provider import LLMProvider


@dataclass
class AgentResult:
    agent_name: str
    output: str
    metadata: dict[str, Any] = field(default_factory=dict)


class Orchestrator:
    """Decomposes a task and routes subtasks to registered specialist agents."""

    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.agents: dict[str, Callable[[str, LLMProvider], Awaitable[AgentResult]]] = {}

    def register(self, name: str, agent_fn: Callable[[str, LLMProvider], Awaitable[AgentResult]]):
        self.agents[name] = agent_fn

    async def run(self, task: str) -> list[AgentResult]:
        results: list[AgentResult] = []

        # Run each registered agent in sequence
        context = task
        for name, agent_fn in self.agents.items():
            result = await agent_fn(context, self.llm)
            results.append(result)
            # Pass accumulated context to next agent
            context = f"{context}\n\nPrevious output from {name}:\n{result.output}"

        return results
