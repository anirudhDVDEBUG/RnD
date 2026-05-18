"""Coder agent — generates code or content based on plan and research."""

from __future__ import annotations
from typing import TYPE_CHECKING

from .orchestrator import AgentResult

if TYPE_CHECKING:
    from services.llm_provider import LLMProvider

SYSTEM_PROMPT = (
    "You are a code generation agent. Given a task description with a plan and research, "
    "generate clean, well-structured code or content. Include relevant comments."
)


async def run(task: str, llm: LLMProvider) -> AgentResult:
    output = await llm.complete(prompt=task, system=SYSTEM_PROMPT)
    return AgentResult(agent_name="Coder", output=output, metadata={"role": "code_generation"})
