"""
Claude Code Swarm Toolkit — Demonstration

Simulates the swarm orchestration patterns that the SKILL.md teaches
Claude Code to execute. Shows decomposition, parallel dispatch, and
result merging with mock data (no API keys needed).
"""

import json
import time
import random
import concurrent.futures
from dataclasses import dataclass, field
from typing import List, Dict

# ─── Swarm Patterns ─────────────────────────────────────────────────────────

@dataclass
class SubTask:
    id: int
    name: str
    scope: str  # file/module boundary
    status: str = "pending"
    result: str = ""
    duration: float = 0.0

@dataclass
class SwarmResult:
    pattern: str
    tasks: List[SubTask] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    total_time: float = 0.0
    sequential_time: float = 0.0


def simulate_agent_work(task: SubTask) -> SubTask:
    """Simulate a subagent doing work (mock — no API calls)."""
    work_time = random.uniform(0.3, 0.8)
    time.sleep(work_time)
    task.status = "completed"
    task.duration = work_time
    task.result = f"Successfully processed {task.scope}"
    return task


def decompose_task(user_prompt: str) -> List[SubTask]:
    """Decompose a user request into independent subtasks."""
    # Simulated decomposition logic
    modules = extract_modules(user_prompt)
    return [
        SubTask(id=i, name=f"Process {mod}", scope=mod)
        for i, mod in enumerate(modules)
    ]


def extract_modules(prompt: str) -> List[str]:
    """Extract parallelizable modules from a prompt."""
    # In real usage, Claude Code does this via LLM reasoning
    known_modules = ["auth", "payments", "notifications", "users", "analytics"]
    found = [m for m in known_modules if m in prompt.lower()]
    if not found:
        # Default demo modules
        found = ["auth", "payments", "notifications"]
    return found


def check_conflicts(tasks: List[SubTask]) -> List[str]:
    """Check for conflicts between completed subtasks."""
    conflicts = []
    # Simulate conflict detection
    scopes = [t.scope for t in tasks]
    # In reality, this checks for overlapping file edits
    if len(scopes) != len(set(scopes)):
        conflicts.append("Duplicate scope detected — file boundary violation")
    return conflicts


# ─── Swarm Orchestrators ────────────────────────────────────────────────────

def fan_out_fan_in(prompt: str) -> SwarmResult:
    """Fan-out/Fan-in: parallel independent tasks, merge at end."""
    print("\n[Fan-Out/Fan-In Pattern]")
    print(f"  Prompt: \"{prompt}\"")

    tasks = decompose_task(prompt)
    print(f"  Decomposed into {len(tasks)} subtasks:")
    for t in tasks:
        print(f"    - Agent {t.id}: {t.name} (scope: {t.scope})")

    print("\n  Dispatching agents in parallel...")
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(simulate_agent_work, t): t for t in tasks}
        for future in concurrent.futures.as_completed(futures):
            task = future.result()
            print(f"    Agent {task.id} completed in {task.duration:.2f}s: {task.result}")

    total = time.time() - start
    sequential = sum(t.duration for t in tasks)
    conflicts = check_conflicts(tasks)

    result = SwarmResult(
        pattern="fan-out/fan-in",
        tasks=tasks,
        conflicts=conflicts,
        total_time=total,
        sequential_time=sequential,
    )

    print(f"\n  Parallel time:    {total:.2f}s")
    print(f"  Sequential would: {sequential:.2f}s")
    print(f"  Speedup:          {sequential/total:.1f}x")
    print(f"  Conflicts:        {len(conflicts)}")
    return result


def map_reduce(prompt: str, files: List[str]) -> SwarmResult:
    """Map-Reduce: same operation across many files, aggregate."""
    print("\n[Map-Reduce Pattern]")
    print(f"  Operation: \"{prompt}\"")
    print(f"  Files: {len(files)} targets")

    tasks = [
        SubTask(id=i, name=f"Process {f}", scope=f)
        for i, f in enumerate(files)
    ]

    print("  Mapping across all files in parallel...")
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(simulate_agent_work, t) for t in tasks]
        concurrent.futures.wait(futures)
        tasks = [f.result() for f in futures]

    total = time.time() - start
    sequential = sum(t.duration for t in tasks)

    # Reduce step
    completed = sum(1 for t in tasks if t.status == "completed")
    print(f"  Reduce: {completed}/{len(tasks)} files processed successfully")

    result = SwarmResult(
        pattern="map-reduce",
        tasks=tasks,
        total_time=total,
        sequential_time=sequential,
    )

    print(f"  Parallel time:    {total:.2f}s")
    print(f"  Sequential would: {sequential:.2f}s")
    print(f"  Speedup:          {sequential/total:.1f}x")
    return result


def pipeline(stages: List[str]) -> SwarmResult:
    """Pipeline: sequential stages, each builds on prior output."""
    print("\n[Pipeline Pattern]")
    print(f"  Stages: {' -> '.join(stages)}")

    tasks = []
    start = time.time()

    for i, stage in enumerate(stages):
        task = SubTask(id=i, name=stage, scope=f"stage_{i}")
        print(f"  Stage {i}: {stage}...", end=" ", flush=True)
        task = simulate_agent_work(task)
        tasks.append(task)
        print(f"done ({task.duration:.2f}s)")

    total = time.time() - start

    result = SwarmResult(
        pattern="pipeline",
        tasks=tasks,
        total_time=total,
        sequential_time=total,  # Pipeline is inherently sequential
    )

    print(f"  Total pipeline time: {total:.2f}s")
    return result


def explore_then_act(research_topics: List[str], action: str) -> SwarmResult:
    """Explore-then-Act: research agents gather info, action agent executes."""
    print("\n[Explore-then-Act Pattern]")
    print(f"  Research phase: {len(research_topics)} topics in parallel")
    print(f"  Action phase: \"{action}\"")

    # Phase 1: Parallel exploration
    explore_tasks = [
        SubTask(id=i, name=f"Research {topic}", scope=topic)
        for i, topic in enumerate(research_topics)
    ]

    print("\n  Phase 1 — Exploring in parallel...")
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(simulate_agent_work, t) for t in explore_tasks]
        concurrent.futures.wait(futures)
        explore_tasks = [f.result() for f in futures]

    for t in explore_tasks:
        print(f"    Explorer {t.id}: {t.result} ({t.duration:.2f}s)")

    # Phase 2: Action based on research
    print("\n  Phase 2 — Acting on findings...")
    action_task = SubTask(id=99, name=action, scope="combined_output")
    action_task = simulate_agent_work(action_task)
    print(f"    Action agent: {action_task.result} ({action_task.duration:.2f}s)")

    total = time.time() - start
    all_tasks = explore_tasks + [action_task]
    sequential = sum(t.duration for t in all_tasks)

    result = SwarmResult(
        pattern="explore-then-act",
        tasks=all_tasks,
        total_time=total,
        sequential_time=sequential,
    )

    print(f"\n  Total time:       {total:.2f}s")
    print(f"  Sequential would: {sequential:.2f}s")
    print(f"  Speedup:          {sequential/total:.1f}x")
    return result


# ─── Main Demo ──────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Claude Code Swarm Toolkit — Pattern Demonstration")
    print("=" * 60)
    print("\nThis demo simulates the 4 swarm patterns the skill teaches")
    print("Claude Code to execute. No API keys needed — uses mock agents.\n")

    results = []

    # 1. Fan-out/Fan-in
    r1 = fan_out_fan_in("Refactor auth, payments, and notifications modules")
    results.append(r1)

    # 2. Map-Reduce
    files = [
        "services/user_service.py",
        "services/order_service.py",
        "services/email_service.py",
        "services/cache_service.py",
        "services/queue_service.py",
    ]
    r2 = map_reduce("Add type hints to all service files", files)
    results.append(r2)

    # 3. Pipeline
    r3 = pipeline(["Analyze codebase", "Design solution", "Implement changes", "Write tests"])
    results.append(r3)

    # 4. Explore-then-Act
    r4 = explore_then_act(
        research_topics=["competitor pricing", "market trends", "user feedback"],
        action="Generate pricing recommendation report"
    )
    results.append(r4)

    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"\n{'Pattern':<20} {'Agents':<8} {'Time':<8} {'Speedup':<8}")
    print("-" * 44)
    for r in results:
        speedup = f"{r.sequential_time/r.total_time:.1f}x" if r.total_time > 0 else "1.0x"
        print(f"{r.pattern:<20} {len(r.tasks):<8} {r.total_time:<8.2f} {speedup:<8}")

    total_parallel = sum(r.total_time for r in results)
    total_sequential = sum(r.sequential_time for r in results)
    print("-" * 44)
    print(f"{'TOTAL':<20} {'':<8} {total_parallel:<8.2f} {total_sequential/total_parallel:.1f}x")
    print(f"\nSwarm orchestration saved ~{total_sequential - total_parallel:.1f}s in this demo.")
    print("In real usage with LLM calls, savings scale to minutes.\n")


if __name__ == "__main__":
    main()
