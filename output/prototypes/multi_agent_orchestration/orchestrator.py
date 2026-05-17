"""
Multi-Agent Orchestration Engine
Based on the Harmonist Orchestral framework for building AI agent swarms.
"""

import time
import json
import random
import threading
from dataclasses import dataclass, field
from typing import Callable, Any
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed


class AgentRole(Enum):
    RESEARCHER = "researcher"
    PLANNER = "planner"
    IMPLEMENTER = "implementer"
    REVIEWER = "reviewer"
    COORDINATOR = "coordinator"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentResult:
    agent_name: str
    role: AgentRole
    output: Any
    duration_ms: float
    success: bool
    metadata: dict = field(default_factory=dict)


@dataclass
class Agent:
    name: str
    role: AgentRole
    tools: list[str]
    handler: Callable | None = None

    def execute(self, task_input: dict) -> AgentResult:
        start = time.time()
        try:
            if self.handler:
                output = self.handler(task_input)
            else:
                output = self._default_handler(task_input)
            duration = (time.time() - start) * 1000
            return AgentResult(
                agent_name=self.name,
                role=self.role,
                output=output,
                duration_ms=round(duration, 1),
                success=True,
            )
        except Exception as e:
            duration = (time.time() - start) * 1000
            return AgentResult(
                agent_name=self.name,
                role=self.role,
                output=str(e),
                duration_ms=round(duration, 1),
                success=False,
            )

    def _default_handler(self, task_input: dict) -> dict:
        # Simulate agent work
        time.sleep(random.uniform(0.05, 0.2))
        return {"status": "done", "input_keys": list(task_input.keys())}


class OrchestrationPattern(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"


class Pipeline:
    """Sequential pipeline: agents execute in order, passing output forward."""

    def __init__(self, name: str):
        self.name = name
        self.stages: list[Agent] = []
        self.results: list[AgentResult] = []

    def add_stage(self, agent: Agent) -> "Pipeline":
        self.stages.append(agent)
        return self

    def run(self, initial_input: dict) -> list[AgentResult]:
        self.results = []
        current_input = initial_input
        print(f"\n{'='*60}")
        print(f"  PIPELINE: {self.name} ({len(self.stages)} stages)")
        print(f"{'='*60}")

        for i, agent in enumerate(self.stages, 1):
            print(f"\n  [{i}/{len(self.stages)}] {agent.name} ({agent.role.value})")
            print(f"      Tools: {', '.join(agent.tools)}")
            result = agent.execute(current_input)
            self.results.append(result)

            status = "OK" if result.success else "FAILED"
            print(f"      Status: {status} ({result.duration_ms}ms)")

            if not result.success:
                print(f"      Error: {result.output}")
                break

            # Pass output as input to next stage
            if isinstance(result.output, dict):
                current_input = {**current_input, **result.output, "_prev_agent": agent.name}
            else:
                current_input = {**current_input, "_prev_output": result.output, "_prev_agent": agent.name}

        return self.results


class FanOut:
    """Parallel fan-out: distribute independent subtasks across agents."""

    def __init__(self, name: str, max_workers: int = 4):
        self.name = name
        self.max_workers = max_workers
        self.agents: list[tuple[Agent, dict]] = []
        self.results: list[AgentResult] = []

    def add_task(self, agent: Agent, task_input: dict) -> "FanOut":
        self.agents.append((agent, task_input))
        return self

    def run(self) -> list[AgentResult]:
        self.results = []
        print(f"\n{'='*60}")
        print(f"  FAN-OUT: {self.name} ({len(self.agents)} parallel tasks)")
        print(f"{'='*60}")

        start = time.time()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for agent, task_input in self.agents:
                future = executor.submit(agent.execute, task_input)
                futures[future] = agent

            for future in as_completed(futures):
                agent = futures[future]
                result = future.result()
                self.results.append(result)
                status = "OK" if result.success else "FAILED"
                print(f"  [{agent.name}] {status} ({result.duration_ms}ms)")

        total_ms = round((time.time() - start) * 1000, 1)
        print(f"\n  Total wall-clock time: {total_ms}ms (parallel)")
        sequential_ms = sum(r.duration_ms for r in self.results)
        print(f"  Sequential equivalent: {round(sequential_ms, 1)}ms")
        print(f"  Speedup: {round(sequential_ms / max(total_ms, 1), 2)}x")

        return self.results


class Coordinator:
    """Hierarchical pattern: coordinator delegates to specialized sub-agents."""

    def __init__(self, name: str, coordinator_agent: Agent):
        self.name = name
        self.coordinator = coordinator_agent
        self.sub_agents: dict[str, Agent] = {}

    def register_agent(self, agent: Agent) -> "Coordinator":
        self.sub_agents[agent.name] = agent
        return self

    def run(self, task: dict) -> dict:
        print(f"\n{'='*60}")
        print(f"  HIERARCHICAL: {self.name}")
        print(f"  Coordinator: {self.coordinator.name}")
        print(f"  Sub-agents: {', '.join(self.sub_agents.keys())}")
        print(f"{'='*60}")

        # Coordinator analyzes and delegates
        print(f"\n  [Coordinator] Analyzing task...")
        coord_result = self.coordinator.execute(task)
        print(f"  [Coordinator] Plan ready ({coord_result.duration_ms}ms)")

        # Execute delegated subtasks
        delegated_results = {}
        for name, agent in self.sub_agents.items():
            print(f"  [Delegate: {name}] Executing...")
            result = agent.execute({**task, "delegation": coord_result.output})
            delegated_results[name] = result
            status = "OK" if result.success else "FAILED"
            print(f"  [Delegate: {name}] {status} ({result.duration_ms}ms)")

        return {
            "coordinator": coord_result,
            "delegated": delegated_results,
        }


# --- Demo handlers that simulate real agent work ---

def research_handler(task_input: dict) -> dict:
    """Simulates research agent gathering information."""
    time.sleep(random.uniform(0.05, 0.15))
    topic = task_input.get("topic", "unknown")
    return {
        "findings": [
            f"Key insight 1 about {topic}: market growing 40% YoY",
            f"Key insight 2 about {topic}: 3 major competitors identified",
            f"Key insight 3 about {topic}: primary user segment is developers",
        ],
        "sources_checked": 12,
        "confidence": 0.87,
    }


def planning_handler(task_input: dict) -> dict:
    """Simulates planning agent creating execution strategy."""
    time.sleep(random.uniform(0.05, 0.15))
    findings = task_input.get("findings", [])
    return {
        "plan": {
            "steps": [
                "Validate market assumptions with data",
                "Design MVP feature set based on findings",
                "Implement core API endpoints",
                "Create integration tests",
            ],
            "estimated_tasks": 4,
            "priority": "high",
        },
        "based_on_findings": len(findings),
    }


def implementation_handler(task_input: dict) -> dict:
    """Simulates implementation agent writing code."""
    time.sleep(random.uniform(0.1, 0.2))
    plan = task_input.get("plan", {})
    steps = plan.get("steps", []) if isinstance(plan, dict) else []
    return {
        "files_created": ["src/api.py", "src/models.py", "src/utils.py"],
        "lines_written": 342,
        "tests_added": 8,
        "steps_completed": len(steps),
    }


def review_handler(task_input: dict) -> dict:
    """Simulates review agent validating output."""
    time.sleep(random.uniform(0.05, 0.1))
    return {
        "review_passed": True,
        "issues_found": 0,
        "suggestions": ["Consider adding rate limiting", "Add input validation on /api/create"],
        "quality_score": 0.92,
    }


def parallel_research_handler(task_input: dict) -> dict:
    """Simulates a parallel research subtask."""
    time.sleep(random.uniform(0.1, 0.3))
    domain = task_input.get("domain", "general")
    return {
        "domain": domain,
        "items_found": random.randint(5, 20),
        "relevance_score": round(random.uniform(0.6, 0.99), 2),
    }


def run_demo():
    """Run the full orchestration demo showing all three patterns."""
    print("\n" + "#" * 60)
    print("#" + " " * 14 + "MULTI-AGENT ORCHESTRATION" + " " * 15 + "#")
    print("#" + " " * 14 + "Engine Demo (Harmonist)" + " " * 17 + "#")
    print("#" * 60)

    # --- Pattern 1: Sequential Pipeline ---
    pipeline = Pipeline("Market Research Pipeline")
    pipeline.add_stage(Agent("Researcher", AgentRole.RESEARCHER, ["WebSearch", "WebFetch"], research_handler))
    pipeline.add_stage(Agent("Planner", AgentRole.PLANNER, ["Read", "TodoWrite"], planning_handler))
    pipeline.add_stage(Agent("Implementer", AgentRole.IMPLEMENTER, ["Edit", "Write", "Bash"], implementation_handler))
    pipeline.add_stage(Agent("Reviewer", AgentRole.REVIEWER, ["Read", "Bash", "Grep"], review_handler))

    results = pipeline.run({"topic": "AI agent frameworks", "scope": "competitive analysis"})

    print(f"\n  Pipeline Summary:")
    print(f"    Stages completed: {sum(1 for r in results if r.success)}/{len(results)}")
    total_time = sum(r.duration_ms for r in results)
    print(f"    Total time: {round(total_time, 1)}ms")
    final = results[-1]
    if final.success and isinstance(final.output, dict):
        print(f"    Quality score: {final.output.get('quality_score', 'N/A')}")

    # --- Pattern 2: Parallel Fan-out ---
    fanout = FanOut("Multi-Domain Research")
    domains = ["competitor_analysis", "pricing_models", "user_feedback", "tech_stack", "market_trends"]
    for domain in domains:
        agent = Agent(f"researcher_{domain}", AgentRole.RESEARCHER, ["WebSearch"], parallel_research_handler)
        fanout.add_task(agent, {"domain": domain, "depth": "deep"})

    par_results = fanout.run()
    print(f"\n  Fan-out Summary:")
    print(f"    Tasks completed: {sum(1 for r in par_results if r.success)}/{len(par_results)}")
    total_items = sum(r.output.get("items_found", 0) for r in par_results if r.success and isinstance(r.output, dict))
    print(f"    Total items found: {total_items}")

    # --- Pattern 3: Hierarchical ---
    coordinator_agent = Agent("TaskCoordinator", AgentRole.COORDINATOR, ["Read", "TodoWrite"], planning_handler)
    hier = Coordinator("Feature Development", coordinator_agent)
    hier.register_agent(Agent("frontend_dev", AgentRole.IMPLEMENTER, ["Edit", "Write"], implementation_handler))
    hier.register_agent(Agent("backend_dev", AgentRole.IMPLEMENTER, ["Edit", "Write", "Bash"], implementation_handler))
    hier.register_agent(Agent("qa_engineer", AgentRole.REVIEWER, ["Bash", "Grep"], review_handler))

    hier_results = hier.run({"feature": "user-auth", "priority": "high"})
    delegated = hier_results["delegated"]
    print(f"\n  Hierarchical Summary:")
    print(f"    Sub-agents executed: {len(delegated)}")
    print(f"    All passed: {all(r.success for r in delegated.values())}")

    # --- Final Summary ---
    print(f"\n{'='*60}")
    print(f"  ORCHESTRATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Patterns demonstrated:")
    print(f"    1. Sequential Pipeline  - 4 agents in series")
    print(f"    2. Parallel Fan-out     - 5 agents in parallel")
    print(f"    3. Hierarchical         - 1 coordinator + 3 delegates")
    print(f"  Total agents invoked: 13")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    run_demo()
