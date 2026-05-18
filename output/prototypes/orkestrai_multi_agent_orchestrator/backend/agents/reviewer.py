"""Reviewer agent — scores output quality and suggests improvements."""

from __future__ import annotations
from typing import TYPE_CHECKING

from .orchestrator import AgentResult

if TYPE_CHECKING:
    from services.llm_provider import LLMProvider

SYSTEM_PROMPT = (
    "You are a quality review agent. Evaluate the generated output for quality, "
    "completeness, and correctness. Provide a score out of 10 and specific suggestions."
)


async def run(task: str, llm: LLMProvider) -> AgentResult:
    output = await llm.complete(prompt=task, system=SYSTEM_PROMPT)
    return AgentResult(agent_name="Reviewer", output=output, metadata={"role": "review"})
