"""Core orchestrator: route tasks, run hooks, execute workflows."""

import json
import time
from datetime import datetime
from pathlib import Path

from .models import AgentProfile, HookConfig, Workflow, WorkflowStep
from .router import Router


class MockAgentExecutor:
    """Simulates agent execution for demo purposes (no real API calls)."""

    MOCK_RESPONSES = {
        "claude": "Analyzed the task thoroughly. Proposed a modular architecture with clear separation of concerns. "
                  "Identified 3 refactoring opportunities and 2 potential edge cases.",
        "codex": "Generated scaffolding with 4 files: model, controller, service, and test. "
                 "All boilerplate follows project conventions.",
        "cursor": "Applied UI refinements: updated 2 components, fixed responsive layout, "
                  "added hover states and smooth transitions.",
        "gemini": "Research complete. Found 5 relevant references, summarized key findings, "
                  "and identified 2 alternative approaches worth exploring.",
        "windsurf": "Completed rapid iteration: prototyped 3 variants, benchmarked performance, "
                    "selected optimal approach with 40% fewer LOC.",
    }

    def execute(self, agent: str, task: str, context: dict | None = None) -> dict:
        time.sleep(0.1)  # simulate latency
        return {
            "agent": agent,
            "task": task,
            "status": "completed",
            "output": self.MOCK_RESPONSES.get(agent, f"[{agent}] Task completed successfully."),
            "timestamp": datetime.now().isoformat(),
            "tokens_used": {"input": 450, "output": 280},
        }


class Orchestrator:
    def __init__(self, router: Router, hooks: HookConfig, executor=None):
        self.router = router
        self.hooks = hooks
        self.executor = executor or MockAgentExecutor()
        self.history: list[dict] = []

    def _run_hooks(self, hook_list: list[dict], context: dict) -> list[str]:
        """Simulate running hooks. Returns list of hook names executed."""
        executed = []
        for hook in hook_list:
            for name, _cmd in hook.items():
                executed.append(name)
        return executed

    def route_and_execute(self, task: str) -> dict:
        """Route a task to the best agent and execute it."""
        agent, reason, confidence = self.router.route(task)

        # Run pre-task hooks
        pre_hooks = self._run_hooks(self.hooks.pre_task, {"task": task, "agent": agent})

        # Execute
        result = self.executor.execute(agent, task)
        result["routing"] = {"reason": reason, "confidence": round(confidence, 2)}
        result["hooks"] = {"pre": pre_hooks}

        # Run post-task hooks
        post_hooks = self._run_hooks(self.hooks.post_task, {"task": task, "result": result})
        result["hooks"]["post"] = post_hooks

        self.history.append(result)
        return result

    def run_workflow(self, workflow: Workflow) -> list[dict]:
        """Execute a multi-step workflow, chaining agents together."""
        results = []
        previous_output = None

        for i, step in enumerate(workflow.steps):
            context = {}
            if step.input_path and previous_output:
                context["input"] = previous_output
            if i > 0:
                # Run handoff hooks between agents
                self._run_hooks(self.hooks.handoff, {
                    "source": workflow.steps[i - 1].agent,
                    "target": step.agent,
                })

            result = self.executor.execute(step.agent, step.task, context)
            result["workflow_step"] = i + 1
            result["output_path"] = step.output_path
            results.append(result)
            previous_output = result["output"]
            self.history.append(result)

        return results
