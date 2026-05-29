#!/usr/bin/env python3
"""
hermes_bridge.py — Local simulator of hermes-code-bridge control plane.

Demonstrates the core pattern: a central orchestrator (Hermes Agent) that
receives a coding task, decomposes it, selects the best-fit CLI agent for
each subtask, dispatches work, and merges results.

This is a *mock* implementation — no real agents or API keys required.
It faithfully mirrors the architecture described in
https://github.com/xuyang-liu16/hermes-code-bridge
"""

from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Optional


# ---------------------------------------------------------------------------
# Agent registry
# ---------------------------------------------------------------------------

class AgentID(str, Enum):
    CLAUDE_CODE = "claude-code"
    CODEX = "codex"
    KIMI_CODE = "kimi-code"
    OPENCODE = "opencode"
    GEMINI_CLI = "gemini-cli"


@dataclass
class AgentProfile:
    agent_id: AgentID
    display_name: str
    strengths: List[str]
    cli_command: str
    available: bool = True

    def match_score(self, task_tags: List[str]) -> float:
        overlap = set(self.strengths) & set(task_tags)
        return len(overlap) / max(len(self.strengths), 1)


AGENT_REGISTRY: List[AgentProfile] = [
    AgentProfile(
        AgentID.CLAUDE_CODE, "Claude Code",
        ["refactor", "architecture", "testing", "documentation", "debugging"],
        "claude --print",
    ),
    AgentProfile(
        AgentID.CODEX, "Codex CLI",
        ["prototyping", "boilerplate", "scripting", "code-generation"],
        "codex --quiet",
    ),
    AgentProfile(
        AgentID.KIMI_CODE, "Kimi Code",
        ["translation", "multilingual", "frontend", "css"],
        "kimi-code run",
    ),
    AgentProfile(
        AgentID.OPENCODE, "OpenCode",
        ["open-source", "rust", "go", "systems"],
        "opencode exec",
    ),
    AgentProfile(
        AgentID.GEMINI_CLI, "Gemini CLI",
        ["data-analysis", "notebooks", "google-cloud", "multimodal"],
        "gemini run",
    ),
]


# ---------------------------------------------------------------------------
# Task decomposition
# ---------------------------------------------------------------------------

@dataclass
class SubTask:
    title: str
    description: str
    tags: List[str]
    assigned_agent: Optional[str] = None
    status: str = "pending"
    result: Optional[str] = None


@dataclass
class TaskPlan:
    original_prompt: str
    subtasks: List[SubTask] = field(default_factory=list)
    strategy: str = "parallel"  # parallel | sequential


def decompose_task(prompt: str) -> TaskPlan:
    """Simulate Hermes decomposing a high-level coding task."""
    plan = TaskPlan(original_prompt=prompt)

    # Simple keyword-based decomposition (real Hermes uses LLM planning)
    if "full-stack" in prompt.lower() or "web app" in prompt.lower():
        plan.subtasks = [
            SubTask("Design API schema", "Create REST endpoint definitions", ["architecture", "documentation"]),
            SubTask("Scaffold frontend", "Generate React/Vue boilerplate", ["frontend", "boilerplate"]),
            SubTask("Implement backend", "Write server logic and DB models", ["code-generation", "systems"]),
            SubTask("Write tests", "Unit + integration tests", ["testing", "debugging"]),
            SubTask("Analyze data layer", "Profile queries, add indexes", ["data-analysis"]),
        ]
        plan.strategy = "parallel"
    elif "refactor" in prompt.lower():
        plan.subtasks = [
            SubTask("Analyze codebase", "Identify code smells and duplication", ["architecture", "debugging"]),
            SubTask("Extract modules", "Break monolith into modules", ["refactor", "systems"]),
            SubTask("Update tests", "Fix broken tests after refactor", ["testing"]),
        ]
        plan.strategy = "sequential"
    elif "bug" in prompt.lower() or "fix" in prompt.lower():
        plan.subtasks = [
            SubTask("Reproduce bug", "Create minimal reproduction", ["debugging", "testing"]),
            SubTask("Root-cause analysis", "Trace through code to find cause", ["debugging", "architecture"]),
            SubTask("Implement fix", "Write the patch", ["code-generation", "refactor"]),
            SubTask("Regression tests", "Add tests to prevent recurrence", ["testing"]),
        ]
        plan.strategy = "sequential"
    else:
        plan.subtasks = [
            SubTask("Analyze request", "Understand what needs to be built", ["architecture"]),
            SubTask("Generate code", "Produce implementation", ["code-generation", "prototyping"]),
            SubTask("Quality check", "Review and test output", ["testing", "debugging"]),
        ]
        plan.strategy = "parallel"

    return plan


# ---------------------------------------------------------------------------
# Agent selection & dispatch
# ---------------------------------------------------------------------------

def select_agent(subtask: SubTask) -> AgentProfile:
    """Pick the best-fit agent for a subtask based on tag overlap."""
    available = [a for a in AGENT_REGISTRY if a.available]
    scored = sorted(available, key=lambda a: a.match_score(subtask.tags), reverse=True)
    return scored[0]


def dispatch_subtask(subtask: SubTask, agent: AgentProfile) -> str:
    """Simulate dispatching a subtask to a CLI agent and getting a result."""
    subtask.assigned_agent = agent.display_name
    subtask.status = "running"

    # Simulate execution latency (50-200 ms)
    latency = random.uniform(0.05, 0.20)
    time.sleep(latency)

    subtask.status = "completed"
    subtask.result = (
        f"[{agent.display_name}] Completed '{subtask.title}' "
        f"({subtask.description}) in {latency*1000:.0f}ms via `{agent.cli_command}`"
    )
    return subtask.result


# ---------------------------------------------------------------------------
# Orchestrator (control plane)
# ---------------------------------------------------------------------------

@dataclass
class OrchestrationResult:
    prompt: str
    strategy: str
    steps: List[dict]
    total_time_ms: float
    agents_used: List[str]


def orchestrate(prompt: str) -> OrchestrationResult:
    """Full Hermes control-plane loop: decompose -> select -> dispatch -> merge."""
    t0 = time.time()

    # 1. Decompose
    plan = decompose_task(prompt)

    steps = []
    agents_used = set()

    # 2. Select & dispatch
    for st in plan.subtasks:
        agent = select_agent(st)
        result_text = dispatch_subtask(st, agent)
        agents_used.add(agent.display_name)
        steps.append({
            "subtask": st.title,
            "agent": agent.display_name,
            "tags": st.tags,
            "result": result_text,
        })

    elapsed = (time.time() - t0) * 1000

    return OrchestrationResult(
        prompt=prompt,
        strategy=plan.strategy,
        steps=steps,
        total_time_ms=round(elapsed, 1),
        agents_used=sorted(agents_used),
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    prompts = [
        "Build a full-stack web app with user auth and dashboards",
        "Refactor the payment module to reduce coupling",
        "Fix the race condition bug in the async task queue",
    ]

    print("=" * 72)
    print("  Hermes Code Bridge — Multi-Agent Orchestration Demo")
    print("=" * 72)
    print()

    for prompt in prompts:
        result = orchestrate(prompt)
        print(f"TASK: {result.prompt}")
        print(f"  Strategy : {result.strategy}")
        print(f"  Agents   : {', '.join(result.agents_used)}")
        print(f"  Time     : {result.total_time_ms:.0f} ms")
        print()
        for i, step in enumerate(result.steps, 1):
            print(f"  [{i}] {step['subtask']}")
            print(f"      Agent: {step['agent']}  Tags: {step['tags']}")
            print(f"      -> {step['result']}")
            print()
        print("-" * 72)
        print()

    # JSON summary for machine consumption
    summary = {
        "demo": "hermes-code-bridge",
        "agents_available": [a.display_name for a in AGENT_REGISTRY],
        "prompts_run": len(prompts),
    }
    print("JSON summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
