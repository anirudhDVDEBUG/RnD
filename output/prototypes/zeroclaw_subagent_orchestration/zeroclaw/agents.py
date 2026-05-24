"""Specialized subagent definitions for the ZeroClaw pattern."""

from __future__ import annotations

import time
import random
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    """Output from a single subagent execution."""
    agent_name: str
    agent_type: str
    status: str  # "success" | "error"
    output: Any = None
    elapsed_ms: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class AgentSpec:
    """Specification for a subagent."""
    name: str
    role: str
    agent_type: str  # "explore", "code", "review"
    tools: list[str] = field(default_factory=list)

    def execute(self, task: str, context: dict | None = None) -> AgentResult:
        """Execute this agent on a task. Uses mock logic for demo."""
        start = time.monotonic()
        # Simulate work with type-specific behavior
        output = _simulate_agent_work(self.agent_type, self.name, task, context or {})
        elapsed = (time.monotonic() - start) * 1000
        return AgentResult(
            agent_name=self.name,
            agent_type=self.agent_type,
            status="success",
            output=output,
            elapsed_ms=round(elapsed, 1),
            metadata={"tools_available": self.tools},
        )


def _simulate_agent_work(agent_type: str, name: str, task: str, context: dict) -> dict:
    """Simulate agent work based on type. Replace with real Claude API calls."""
    time.sleep(random.uniform(0.05, 0.15))  # simulate latency

    if agent_type == "explore":
        return {
            "findings": [
                f"Analyzed codebase for: {task}",
                "Found 3 relevant modules and 12 functions",
                "Key dependency: requests>=2.28",
                "Architecture follows hexagonal pattern",
            ],
            "files_examined": random.randint(8, 25),
            "recommendations": [
                "Consider caching API responses",
                "Extract shared utilities into common module",
            ],
        }
    elif agent_type == "code":
        return {
            "files_modified": [
                {"path": "src/handler.py", "action": "created", "lines_added": 45},
                {"path": "src/utils.py", "action": "modified", "lines_added": 12, "lines_removed": 3},
            ],
            "summary": f"Implemented solution for: {task}",
            "tests_added": 2,
        }
    elif agent_type == "review":
        score = random.uniform(7.5, 9.8)
        return {
            "quality_score": round(score, 1),
            "issues_found": max(0, random.randint(0, 3)),
            "checks": {
                "type_safety": "pass",
                "test_coverage": f"{random.randint(78, 95)}%",
                "security_scan": "pass",
                "lint": "pass" if score > 8.0 else "1 warning",
            },
            "verdict": "approved" if score > 8.0 else "changes_requested",
        }
    else:
        return {"note": f"Agent '{name}' completed task: {task}"}


# Pre-built agent specs for common roles
RESEARCH_AGENT = AgentSpec(
    name="research",
    role="Gather information, search codebases, read documentation",
    agent_type="explore",
    tools=["Grep", "Glob", "Read", "WebFetch"],
)

CODE_AGENT = AgentSpec(
    name="code",
    role="Write, edit, and refactor code",
    agent_type="code",
    tools=["Edit", "Write", "Bash"],
)

REVIEW_AGENT = AgentSpec(
    name="review",
    role="Validate output, run tests, check quality",
    agent_type="review",
    tools=["Bash", "Read", "Grep"],
)
