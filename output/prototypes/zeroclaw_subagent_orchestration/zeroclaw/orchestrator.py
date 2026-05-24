"""Top-level orchestrator — decomposes, routes, and merges."""

from __future__ import annotations

from .agents import AgentSpec, RESEARCH_AGENT, CODE_AGENT, REVIEW_AGENT
from .router import Router, RouterConfig
from .merger import merge_results, MergedResult


class Orchestrator:
    """ZeroClaw orchestrator that manages the full agent pipeline."""

    def __init__(self, strategy: str = "parallel_then_merge", agents: list[AgentSpec] | None = None):
        config = RouterConfig(strategy=strategy)
        for agent in (agents or [RESEARCH_AGENT, CODE_AGENT, REVIEW_AGENT]):
            config.register(agent)
        self.router = Router(config)
        self.config = config

    def decompose(self, task: str) -> list[dict]:
        """Break a high-level task into subtasks mapped to agents.

        In production this would call Claude to do intelligent decomposition.
        Here we use a deterministic rule-based approach for the demo.
        """
        subtasks = [
            {
                "agent": "research",
                "task": f"Research and gather context for: {task}",
                "context": {"original_task": task},
            },
            {
                "agent": "code",
                "task": f"Implement solution for: {task}",
                "context": {"original_task": task},
            },
            {
                "agent": "review",
                "task": f"Review implementation for: {task}",
                "context": {"original_task": task},
            },
        ]
        return subtasks

    def run(self, task: str) -> MergedResult:
        """Execute the full orchestration pipeline."""
        subtasks = self.decompose(task)
        results = self.router.dispatch(subtasks)
        return merge_results(results, task)
