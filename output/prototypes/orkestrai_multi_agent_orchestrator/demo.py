#!/usr/bin/env python3
"""Standalone demo of the Orkestrai multi-agent orchestrator (no API keys needed)."""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from services.llm_provider import LLMProvider
from agents.orchestrator import Orchestrator
from agents.planner import run as planner_run
from agents.researcher import run as researcher_run
from agents.coder import run as coder_run
from agents.reviewer import run as reviewer_run


async def main():
    task = "Build a landing page for an AI writing assistant SaaS product"

    print("=" * 60)
    print("  Orkestrai Multi-Agent Orchestrator Demo")
    print("=" * 60)
    print()
    print(f'Task: "{task}"')
    print()

    # Initialize with mock mode (no API keys needed)
    llm = LLMProvider(mock_mode=True)
    orch = Orchestrator(llm)
    orch.register("Planner", planner_run)
    orch.register("Researcher", researcher_run)
    orch.register("Coder", coder_run)
    orch.register("Reviewer", reviewer_run)

    print("[Orchestrator] Decomposing task and delegating to agents...")
    print()

    results = await orch.run(task)

    for result in results:
        print(f"{'─' * 60}")
        print(f"[{result.agent_name}] (role: {result.metadata.get('role', 'unknown')})")
        print(f"{'─' * 60}")
        # Indent output for readability
        for line in result.output.split("\n"):
            print(f"  {line}")
        print()

    print("=" * 60)
    print("  ORCHESTRATION COMPLETE")
    print(f"  Agents used: {len(results)}")
    print(f"  Pipeline: {' -> '.join(r.agent_name for r in results)}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
