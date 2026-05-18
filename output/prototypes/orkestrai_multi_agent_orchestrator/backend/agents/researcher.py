"""Researcher agent — gathers context and patterns for the task."""

from __future__ import annotations
from typing import TYPE_CHECKING

from .orchestrator import AgentResult

if TYPE_CHECKING:
    from services.llm_provider import LLMProvider

SYSTEM_PROMPT = (
    "You are a research agent. Given a task and plan, gather relevant context, "
    "patterns, and insights that will help with implementation. Be concise and actionable."
)


async def run(task: str, llm: LLMProvider) -> AgentResult:
    output = await llm.complete(prompt=task, system=SYSTEM_PROMPT)
    return AgentResult(agent_name="Researcher", output=output, metadata={"role": "research"})
