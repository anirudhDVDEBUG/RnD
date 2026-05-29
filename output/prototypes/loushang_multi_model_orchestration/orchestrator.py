"""
Loushang-style multi-model coding orchestration demo.
Demonstrates: stateful sessions, tool governance, traceable delivery, multi-agent workflows.
"""

import json
import time
import uuid
import os
from dataclasses import dataclass, field, asdict
from typing import Any
from enum import Enum


class StepType(str, Enum):
    PLAN = "plan"
    IMPLEMENT = "implement"
    REVIEW = "review"


class ToolPolicy(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class ToolCall:
    tool_name: str
    agent: str
    args: dict
    result: str
    allowed: bool
    timestamp: float = field(default_factory=time.time)


@dataclass
class SessionTrace:
    session_id: str
    steps: list[dict] = field(default_factory=list)
    tool_calls: list[dict] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    status: str = "running"


@dataclass
class GovernancePolicy:
    """Defines which tools an agent can access."""
    agent_name: str
    allowed_tools: list[str]
    denied_tools: list[str]

    def check(self, tool_name: str) -> bool:
        if tool_name in self.denied_tools:
            return False
        if self.allowed_tools and tool_name not in self.allowed_tools:
            return False
        return True


# --- Mock Model Agents ---

class MockAgent:
    """Base mock agent simulating an LLM provider."""

    def __init__(self, name: str, model_id: str):
        self.name = name
        self.model_id = model_id

    def plan(self, task: str) -> dict:
        raise NotImplementedError

    def implement(self, subtasks: list[str]) -> dict:
        raise NotImplementedError

    def review(self, code: str) -> dict:
        raise NotImplementedError


class DeepSeekAgent(MockAgent):
    def __init__(self):
        super().__init__("deepseek-r1", "deepseek-r1-250528")

    def plan(self, task: str) -> dict:
        # Simulate planning with reasoning
        subtasks = []
        if "validation" in task.lower() or "registration" in task.lower():
            subtasks = [
                "Validate email format using regex pattern",
                "Check password strength (min 8 chars, mixed case, digits)",
                "Sanitize username (strip whitespace, check forbidden chars)",
            ]
        elif "error" in task.lower():
            subtasks = [
                "Add try/except blocks around external calls",
                "Define custom exception hierarchy",
                "Add structured error logging",
            ]
        else:
            subtasks = [
                f"Analyze requirements for: {task}",
                "Identify key components and interfaces",
                "Define test cases for acceptance criteria",
            ]
        return {
            "model": self.model_id,
            "subtasks": subtasks,
            "reasoning": f"Decomposed '{task}' into {len(subtasks)} atomic subtasks",
        }


class ClaudeAgent(MockAgent):
    def __init__(self):
        super().__init__("claude-opus", "claude-opus-4-6")

    def implement(self, subtasks: list[str]) -> dict:
        # Simulate code generation
        code_lines = [
            '"""Auto-generated validators module."""',
            "import re",
            "",
            "",
            "def validate_email(email: str) -> bool:",
            '    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"',
            "    return bool(re.match(pattern, email))",
            "",
            "",
            "def check_password_strength(password: str) -> dict:",
            '    issues = []',
            "    if len(password) < 8:",
            '        issues.append("Password must be at least 8 characters")',
            "    if not re.search(r'[A-Z]', password):",
            '        issues.append("Must contain uppercase letter")',
            "    if not re.search(r'[0-9]', password):",
            '        issues.append("Must contain a digit")',
            '    return {"valid": len(issues) == 0, "issues": issues}',
            "",
            "",
            "def sanitize_username(username: str) -> str:",
            '    forbidden = set(\'<>"/;\\\\\')',
            "    cleaned = username.strip()",
            "    cleaned = ''.join(c for c in cleaned if c not in forbidden)",
            "    return cleaned[:64]  # max length",
            "",
            "",
            "# --- Tool calls made during implementation ---",
            "TOOL_CALLS = [",
            '    {"tool": "read_file", "args": {"path": "models/user.py"}},',
            '    {"tool": "write_file", "args": {"path": "validators.py"}},',
            '    {"tool": "run_tests", "args": {"suite": "test_validators"}},',
            "]",
        ]
        return {
            "model": self.model_id,
            "files": {"validators.py": "\n".join(code_lines)},
            "lines_written": len(code_lines),
            "tool_calls_made": ["read_file", "write_file", "run_tests"],
        }


class QwenAgent(MockAgent):
    def __init__(self):
        super().__init__("qwen-max", "qwen-max-2025")

    def review(self, code: str) -> dict:
        # Simulate code review
        return {
            "model": self.model_id,
            "verdict": "APPROVED",
            "blocking_issues": 0,
            "suggestions": [
                "Consider adding type hints to return values",
                "Email regex could be replaced with email-validator library for edge cases",
            ],
            "score": 8.5,
        }


# --- Orchestrator ---

class Orchestrator:
    """Multi-model workflow orchestrator with session management and governance."""

    def __init__(self):
        self.agents = {
            "deepseek-r1": DeepSeekAgent(),
            "claude-opus": ClaudeAgent(),
            "qwen-max": QwenAgent(),
        }
        self.policies = {
            "claude-opus": GovernancePolicy(
                agent_name="claude-opus",
                allowed_tools=["read_file", "write_file", "run_tests"],
                denied_tools=["delete_file", "exec_shell"],
            ),
            "deepseek-r1": GovernancePolicy(
                agent_name="deepseek-r1",
                allowed_tools=["read_file", "search"],
                denied_tools=["write_file", "exec_shell", "delete_file"],
            ),
            "qwen-max": GovernancePolicy(
                agent_name="qwen-max",
                allowed_tools=["read_file", "search", "lint"],
                denied_tools=["write_file", "exec_shell", "delete_file"],
            ),
        }
        self.sessions: dict[str, SessionTrace] = {}

    def create_session(self) -> str:
        session_id = uuid.uuid4().hex[:8]
        self.sessions[session_id] = SessionTrace(session_id=session_id)
        return session_id

    def check_governance(self, agent_name: str, tool_name: str) -> bool:
        policy = self.policies.get(agent_name)
        if not policy:
            return True
        return policy.check(tool_name)

    def run_workflow(self, task: str, workflow: list[tuple[StepType, str]]) -> dict:
        """Run a multi-step workflow. Each step is (StepType, agent_name)."""
        session_id = self.create_session()
        trace = self.sessions[session_id]
        results = {}

        print(f"\n[Session {session_id}] Starting workflow: {'-'.join(s[0].value for s in workflow)}")
        print(f"  Provider: mock (demo mode)\n")

        for i, (step_type, agent_name) in enumerate(workflow, 1):
            agent = self.agents[agent_name]
            print(f"[Step {i}/{len(workflow)}] {step_type.value.upper()} (model: {agent.model_id})")

            if step_type == StepType.PLAN:
                print(f'  Task: "{task}"')
                result = agent.plan(task)
                print(f"  Result: {len(result['subtasks'])} subtasks identified")
                for j, st in enumerate(result["subtasks"], 1):
                    print(f"    {j}. {st}")
                results["plan"] = result

            elif step_type == StepType.IMPLEMENT:
                subtasks = results.get("plan", {}).get("subtasks", [task])
                print(f"  Generating code for {len(subtasks)} subtasks...")

                result = agent.implement(subtasks)

                # Governance check on tool calls
                violations = 0
                for tool_name in result.get("tool_calls_made", []):
                    allowed = self.check_governance(agent_name, tool_name)
                    trace.tool_calls.append(asdict(ToolCall(
                        tool_name=tool_name,
                        agent=agent_name,
                        args={},
                        result="ok" if allowed else "BLOCKED",
                        allowed=allowed,
                    )))
                    if not allowed:
                        violations += 1

                for fname, content in result.get("files", {}).items():
                    print(f"  Files written: {fname} ({result['lines_written']} lines)")
                results["implement"] = result

            elif step_type == StepType.REVIEW:
                code = ""
                for f in results.get("implement", {}).get("files", {}).values():
                    code += f
                print(f"  Reviewing {list(results.get('implement', {}).get('files', {}).keys())}...")
                result = agent.review(code)
                print(f"  Result: {result['verdict']} ({len(result['suggestions'])} suggestions, {result['blocking_issues']} blocking issues)")
                results["review"] = result

            trace.steps.append({
                "step": step_type.value,
                "agent": agent_name,
                "model": agent.model_id,
            })
            print()

        # Finalize
        trace.end_time = time.time()
        trace.status = "delivered"
        duration = trace.end_time - trace.start_time
        policy_violations = sum(1 for tc in trace.tool_calls if not tc.get("allowed", True))

        print(f"[Session {session_id}] DELIVERED")
        print(f"  Duration: {duration:.1f}s | Tool calls: {len(trace.tool_calls)} | Policy violations: {policy_violations}")

        # Save trace
        trace_dir = os.path.join(os.path.dirname(__file__), "traces")
        os.makedirs(trace_dir, exist_ok=True)
        trace_path = os.path.join(trace_dir, f"session_{session_id}.json")
        with open(trace_path, "w") as f:
            json.dump({
                "session_id": session_id,
                "status": trace.status,
                "duration_s": round(duration, 2),
                "steps": trace.steps,
                "tool_calls": trace.tool_calls,
                "results": {
                    "plan": results.get("plan"),
                    "implement": {k: v for k, v in results.get("implement", {}).items() if k != "files"},
                    "review": results.get("review"),
                },
            }, f, indent=2, default=str)
        print(f"  Trace saved: {trace_path}")

        return {
            "session_id": session_id,
            "status": "delivered",
            "results": results,
            "trace_path": trace_path,
        }


def demo_governance():
    """Show governance policy enforcement."""
    print("\n--- Tool Governance Demo ---\n")
    orch = Orchestrator()

    checks = [
        ("claude-opus", "write_file", True),
        ("claude-opus", "exec_shell", False),
        ("deepseek-r1", "read_file", True),
        ("deepseek-r1", "write_file", False),
        ("qwen-max", "delete_file", False),
        ("qwen-max", "lint", True),
    ]

    print(f"  {'Agent':<15} {'Tool':<15} {'Allowed':<10}")
    print(f"  {'-'*15} {'-'*15} {'-'*10}")
    for agent, tool, expected in checks:
        result = orch.check_governance(agent, tool)
        status = "ALLOW" if result else "DENY"
        print(f"  {agent:<15} {tool:<15} {status:<10}")


def main():
    print("=" * 55)
    print("  Loushang Multi-Model Orchestration Demo")
    print("=" * 55)

    orch = Orchestrator()

    # Run the standard plan-implement-review workflow
    workflow = [
        (StepType.PLAN, "deepseek-r1"),
        (StepType.IMPLEMENT, "claude-opus"),
        (StepType.REVIEW, "qwen-max"),
    ]

    result = orch.run_workflow(
        task="Add input validation to user registration endpoint",
        workflow=workflow,
    )

    # Show governance
    demo_governance()

    # Show session info
    print("\n--- Session Management ---\n")
    print(f"  Active sessions: {len(orch.sessions)}")
    for sid, trace in orch.sessions.items():
        print(f"  - {sid}: {trace.status} ({len(trace.steps)} steps, {len(trace.tool_calls)} tool calls)")

    print("\n" + "=" * 55)
    print("  Demo complete. See traces/ directory for full session log.")
    print("=" * 55)


if __name__ == "__main__":
    main()
