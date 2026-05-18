"""Planner agent — decomposes tasks into ordered subtasks."""

from __future__ import annotations
from typing import TYPE_CHECKING

from .orchestrator import AgentResult

if TYPE_CHECKING:
    from services.llm_provider import LLMProvider

SYSTEM_PROMPT = (
    "You are a project planner agent. Decompose the given task into concrete, "
    "ordered subtasks. Return a numbered list of 3-5 actionable steps."
)


async def run(task: str, llm: LLMProvider) -> AgentResult:
    output = await llm.complete(prompt=task, system=SYSTEM_PROMPT)
    return AgentResult(agent_name="Planner", output=output, metadata={"role": "planning"})
