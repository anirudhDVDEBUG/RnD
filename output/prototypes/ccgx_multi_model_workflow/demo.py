#!/usr/bin/env python3
"""
CCGX Multi-Model Workflow — Demo
Runs a set of sample tasks through the router and orchestrator,
printing a clear summary of routing decisions and model outputs.
"""

import json
from ccgx.router import route_task, QUALITY_CONFIGS
from ccgx.orchestrator import run_workflow

SAMPLE_TASKS = [
    "Build a responsive React dashboard with Tailwind CSS cards and charts",
    "Create a REST API endpoint for user authentication with JWT tokens",
    "Design a Vue.js modal component with animation transitions",
    "Set up PostgreSQL database migrations and seed data for the users table",
    "Write integration tests for the full signup-to-login flow",
    "Add a dark mode toggle to the settings page UI",
    "Deploy the Docker containers to Kubernetes with health checks",
    "Implement a drag-and-drop kanban board component in React",
]

SEPARATOR = "=" * 72
THIN_SEP = "-" * 72

MODEL_LABELS = {
    "gemini": "Gemini  (frontend)",
    "codex":  "Codex   (backend)",
    "claude": "Claude  (general)",
}


def print_header(title: str) -> None:
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def demo_routing() -> None:
    """Show how each task gets classified and routed."""
    print_header("STEP 1: Task Routing Decisions")
    print()
    for i, task in enumerate(SAMPLE_TASKS, 1):
        result = route_task(task)
        label = MODEL_LABELS.get(result.model, result.model)
        bar_len = int(result.confidence * 20)
        bar = "#" * bar_len + "." * (20 - bar_len)
        print(f"  [{i}] {task[:65]}")
        print(f"      -> {label}  confidence=[{bar}] {result.confidence:.0%}")
        print(f"         FE signals={result.frontend_score}  BE signals={result.backend_score}")
        print()


def demo_quality_tiers() -> None:
    """Show the three quality tier configurations."""
    print_header("STEP 2: Quality Tier Configurations")
    print()
    for tier, config in QUALITY_CONFIGS.items():
        print(f"  {tier.upper():12s}  iterations={config['max_iterations']}  "
              f"tests={'yes' if config['run_tests'] else 'no ':3s}  "
              f"review={'yes' if config['review'] else 'no ':3s}  "
              f"-- {config['description']}")
    print()


def demo_workflow() -> None:
    """Run full orchestrated workflow and show results."""
    for tier in ("draft", "standard", "production"):
        print_header(f"STEP 3: Workflow Run  [quality={tier}]")
        print()
        run = run_workflow(SAMPLE_TASKS, quality_tier=tier, autonomous=True)

        for i, result in enumerate(run.results, 1):
            r = result.routing
            m = result.response
            label = MODEL_LABELS.get(r.model, r.model)
            print(f"  [{i}] {r.task[:60]}")
            print(f"      model={label}  tokens={m.tokens_used}  latency={m.latency_ms}ms")
            print(f"      output: {m.output}")
            print()

        print(f"  {THIN_SEP}")
        print(f"  SUMMARY: {len(run.results)} tasks | "
              f"{run.total_tokens} total tokens | "
              f"{run.total_latency_ms}ms total latency")
        breakdown = run.model_breakdown
        parts = [f"{MODEL_LABELS.get(k,k)}: {v}" for k, v in sorted(breakdown.items())]
        print(f"  ROUTING:  {' | '.join(parts)}")
        print()


def demo_single_task_json() -> None:
    """Show JSON output for a single task routing — useful for integrations."""
    print_header("STEP 4: JSON Output (single task)")
    print()
    task = "Build a GraphQL API with Prisma ORM and Redis caching"
    result = route_task(task, quality_tier="production")
    payload = {
        "task": result.task,
        "routed_to": result.model,
        "confidence": result.confidence,
        "frontend_score": result.frontend_score,
        "backend_score": result.backend_score,
        "quality_tier": result.quality_tier,
    }
    print(json.dumps(payload, indent=2))
    print()


if __name__ == "__main__":
    print()
    print("  CCGX Multi-Model Workflow — Demo")
    print("  Auto-routes frontend -> Gemini, backend -> Codex")
    print()
    demo_routing()
    demo_quality_tiers()
    demo_workflow()
    demo_single_task_json()
    print(SEPARATOR)
    print("  Demo complete. See HOW_TO_USE.md for integration details.")
    print(SEPARATOR)
