#!/usr/bin/env python3
"""
Maestro Agent Orchestrator - Demo
Routes tasks to the best AI coding agent and runs multi-agent workflows.
"""

import json
import os
import sys

from maestro.loader import load_hooks, load_profiles, load_routing, load_workflow
from maestro.orchestrator import Orchestrator
from maestro.router import Router

SEPARATOR = "=" * 70


def print_header(title: str):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def print_result(result: dict):
    routing = result.get("routing", {})
    hooks = result.get("hooks", {})
    print(f"  Agent:      {result['agent']}")
    print(f"  Task:       {result['task']}")
    print(f"  Status:     {result['status']}")
    if routing:
        print(f"  Routed by:  {routing['reason']}")
        print(f"  Confidence: {routing['confidence']:.0%}")
    if hooks.get("pre"):
        print(f"  Pre-hooks:  {', '.join(hooks['pre'])}")
    if hooks.get("post"):
        print(f"  Post-hooks: {', '.join(hooks['post'])}")
    print(f"  Output:     {result['output']}")
    print(f"  Tokens:     {result['tokens_used']['input']}in / {result['tokens_used']['output']}out")


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    maestro_dir = os.path.join(base, ".maestro")

    # Load configuration
    print_header("MAESTRO AGENT ORCHESTRATOR")
    print("  Loading configuration...")

    profiles = load_profiles(os.path.join(maestro_dir, "profiles"))
    print(f"  Loaded {len(profiles)} agent profiles: {', '.join(profiles.keys())}")

    rules, fallback = load_routing(os.path.join(maestro_dir, "routing.yaml"))
    print(f"  Loaded {len(rules)} routing rules (fallback: {fallback})")

    hooks = load_hooks(os.path.join(maestro_dir, "hooks.yaml"))
    print(f"  Loaded hooks: {len(hooks.pre_task)} pre, {len(hooks.post_task)} post, {len(hooks.handoff)} handoff")

    # Create orchestrator
    router = Router(rules, profiles, fallback)
    orchestrator = Orchestrator(router, hooks)

    # ── Demo 1: Single-task routing ──
    print_header("DEMO 1: SINGLE-TASK ROUTING")
    print("  Routing 6 different tasks to the best-suited agent...\n")

    tasks = [
        "Refactor the auth module for better testability",
        "Generate CRUD boilerplate for the user management API",
        "Fix the responsive layout on the dashboard component",
        "Research best practices for rate limiting in microservices",
        "Optimize the database query performance in the reporting module",
        "Design a plugin architecture for the notification system",
    ]

    for i, task in enumerate(tasks, 1):
        print(f"  --- Task {i} ---")
        result = orchestrator.route_and_execute(task)
        print_result(result)
        print()

    # ── Demo 2: Routing table overview ──
    print_header("DEMO 2: ROUTING TABLE")
    print(f"  {'Pattern':<45} {'Agent':<10} {'Priority':<10}")
    print(f"  {'-'*45} {'-'*10} {'-'*10}")
    for rule in rules:
        print(f"  {rule.pattern:<45} {rule.route_to:<10} {rule.priority:<10}")
    print(f"\n  Fallback agent: {fallback}")

    # ── Demo 3: Multi-agent workflow ──
    print_header("DEMO 3: MULTI-AGENT WORKFLOW")
    workflow_file = os.path.join(maestro_dir, "workflows", "feature_implementation.yaml")
    workflow = load_workflow(workflow_file)
    print(f"  Workflow: '{workflow.name}' ({len(workflow.steps)} steps)\n")

    results = orchestrator.run_workflow(workflow)
    for result in results:
        step_num = result["workflow_step"]
        print(f"  --- Step {step_num}: {result['agent']} ---")
        print(f"  Task:   {result['task']}")
        print(f"  Output: {result['output']}")
        if result.get("output_path"):
            print(f"  Saved:  {result['output_path']}")
        print()

    # ── Demo 4: Agent profiles summary ──
    print_header("DEMO 4: AGENT PROFILES")
    for name, profile in profiles.items():
        print(f"  [{name}] context={profile.context_window}")
        print(f"    Strengths: {', '.join(profile.strengths)}")
        print(f"    Preferred: {', '.join(profile.preferred_tasks)}")
        print()

    # ── Summary ──
    print_header("SESSION SUMMARY")
    print(f"  Total tasks executed: {len(orchestrator.history)}")
    agent_counts = {}
    for r in orchestrator.history:
        agent_counts[r["agent"]] = agent_counts.get(r["agent"], 0) + 1
    for agent, count in sorted(agent_counts.items(), key=lambda x: -x[1]):
        bar = "#" * (count * 4)
        print(f"    {agent:<10} {bar} ({count})")
    print(f"\n  All tasks completed successfully.")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
