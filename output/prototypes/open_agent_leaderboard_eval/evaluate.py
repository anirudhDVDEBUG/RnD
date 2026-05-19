#!/usr/bin/env python3
"""
Open Agent Leaderboard Evaluator — Demo Mode

Simulates running an agent through the Exgentic evaluation protocol across all
six benchmarks. Uses mock task execution to demonstrate the evaluation flow,
metric collection, and leaderboard comparison without requiring API keys.

Usage:
    python evaluate.py                    # Full demo evaluation
    python evaluate.py --benchmark swe    # Single benchmark
    python evaluate.py --compare          # Compare all leaderboard agents
"""

import argparse
import json
import random
import sys
import time
from pathlib import Path

from leaderboard_data import BENCHMARKS, get_leaderboard

# Seed for reproducible mock results
random.seed(42)


# ── Mock task definitions per benchmark ──────────────────────────────────────

MOCK_TASKS = {
    "SWE-Bench Verified": [
        {"id": "django__django-16379", "desc": "Fix URLValidator to accept IPv6 URLs"},
        {"id": "sympy__sympy-24213", "desc": "Collect mishandles Derivative expressions"},
        {"id": "scikit-learn__scikit-learn-25638", "desc": "ColumnTransformer output order bug"},
    ],
    "BrowseComp+": [
        {"id": "bc-047", "desc": "Find the founding date of a specific obscure company"},
        {"id": "bc-112", "desc": "Identify the author of a niche academic paper from 2019"},
        {"id": "bc-203", "desc": "Cross-reference patent holders across two jurisdictions"},
    ],
    "AppWorld": [
        {"id": "aw-daily-15", "desc": "Schedule meeting across 3 calendars, send invites"},
        {"id": "aw-shop-08", "desc": "Find cheapest flight + hotel combo under budget"},
        {"id": "aw-social-22", "desc": "Post photo to social media with location tag"},
    ],
    "tau2-Airline": [
        {"id": "tau-air-001", "desc": "Rebook passenger after cancellation per policy"},
        {"id": "tau-air-017", "desc": "Process upgrade request with loyalty points"},
        {"id": "tau-air-033", "desc": "Handle baggage claim for international transfer"},
    ],
    "tau2-Retail": [
        {"id": "tau-ret-005", "desc": "Process return outside window with manager override"},
        {"id": "tau-ret-019", "desc": "Apply stacking discount coupons correctly"},
        {"id": "tau-ret-041", "desc": "Resolve inventory discrepancy for online order"},
    ],
    "tau2-Telecom": [
        {"id": "tau-tel-002", "desc": "Diagnose intermittent connectivity, escalate if needed"},
        {"id": "tau-tel-014", "desc": "Migrate customer to new plan preserving promotions"},
        {"id": "tau-tel-028", "desc": "Troubleshoot VoIP quality degradation"},
    ],
}


# ── Exgentic Protocol Simulation ─────────────────────────────────────────────

class ExgenticProtocol:
    """Simulates the Exgentic unified evaluation protocol."""

    def __init__(self, agent_name: str, model: str):
        self.agent_name = agent_name
        self.model = model
        self.results = {}

    def create_task_envelope(self, benchmark: str, task: dict) -> dict:
        """Create a Task/Context/Actions envelope per the Exgentic protocol."""
        return {
            "task": {
                "id": task["id"],
                "benchmark": benchmark,
                "description": task["desc"],
            },
            "context": {
                "benchmark_rules": f"Standard {benchmark} evaluation rules",
                "tools_available": self._get_tools(benchmark),
                "max_steps": 30,
            },
            "actions": self._get_actions(benchmark),
        }

    def _get_tools(self, benchmark: str) -> list:
        tool_map = {
            "SWE-Bench Verified": ["bash", "file_editor", "git", "python"],
            "BrowseComp+": ["web_search", "page_reader", "note_taker"],
            "AppWorld": ["api_caller", "calendar", "email", "browser"],
            "tau2-Airline": ["crm_lookup", "booking_system", "policy_db"],
            "tau2-Retail": ["order_system", "inventory_db", "coupon_engine"],
            "tau2-Telecom": ["network_diag", "account_mgr", "ticket_system"],
        }
        return tool_map.get(benchmark, [])

    def _get_actions(self, benchmark: str) -> list:
        return ["observe", "think", "act", "submit_answer"]

    def run_task(self, envelope: dict) -> dict:
        """Simulate running a single task. Returns mock trajectory + result."""
        task_id = envelope["task"]["id"]
        benchmark = envelope["task"]["benchmark"]

        # Simulate execution steps
        n_steps = random.randint(5, 25)
        success = random.random() < 0.55  # ~55% success rate
        cost = round(random.uniform(0.15, 2.80), 2)

        # Failed tasks cost more (matching the paper's finding)
        if not success:
            cost = round(cost * random.uniform(1.2, 1.54), 2)

        return {
            "task_id": task_id,
            "benchmark": benchmark,
            "success": success,
            "steps": n_steps,
            "cost_usd": cost,
            "trajectory_length": n_steps,
        }

    def evaluate_benchmark(self, benchmark: str) -> dict:
        """Run all tasks in a benchmark and aggregate results."""
        tasks = MOCK_TASKS.get(benchmark, [])
        task_results = []

        for task in tasks:
            envelope = self.create_task_envelope(benchmark, task)
            result = self.run_task(envelope)
            task_results.append(result)

        successes = sum(1 for r in task_results if r["success"])
        total_cost = sum(r["cost_usd"] for r in task_results)
        success_rate = (successes / len(task_results) * 100) if task_results else 0

        return {
            "benchmark": benchmark,
            "tasks_run": len(task_results),
            "successes": successes,
            "success_rate": round(success_rate, 1),
            "total_cost": round(total_cost, 2),
            "avg_cost_per_task": round(total_cost / len(task_results), 2) if task_results else 0,
            "task_results": task_results,
        }


# ── Display helpers ──────────────────────────────────────────────────────────

def print_header(text: str):
    width = 72
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def print_benchmark_result(result: dict):
    bm = result["benchmark"]
    sr = result["success_rate"]
    bar = "█" * int(sr / 5) + "░" * (20 - int(sr / 5))
    cost_str = f"${result['avg_cost_per_task']:.2f}/task"

    print(f"\n  {bm:<24} {bar} {sr:5.1f}%   {cost_str}")
    for tr in result["task_results"]:
        status = "✓" if tr["success"] else "✗"
        print(f"    {status} {tr['task_id']:<30} steps={tr['steps']:>2}  cost=${tr['cost_usd']:.2f}")


def print_leaderboard_comparison(my_avg: float, my_cost: float):
    print_header("LEADERBOARD COMPARISON")
    leaderboard = get_leaderboard()

    print(f"\n  {'Rank':<5} {'Agent':<20} {'Model':<22} {'Avg Score':>10} {'$/Task':>8}")
    print(f"  {'─'*5} {'─'*20} {'─'*22} {'─'*10} {'─'*8}")

    inserted = False
    rank = 1
    for entry in leaderboard:
        if not inserted and my_avg >= entry["avg_score"]:
            print(f"  {rank:<5} {'>>> YOUR AGENT <<<':<20} {'(demo)':<22} {my_avg:>9.1f}% {my_cost:>7.2f}")
            rank += 1
            inserted = True
        print(f"  {rank:<5} {entry['agent']:<20} {entry['model']:<22} {entry['avg_score']:>9.1f}% {entry['avg_cost']:>7.2f}")
        rank += 1

    if not inserted:
        print(f"  {rank:<5} {'>>> YOUR AGENT <<<':<20} {'(demo)':<22} {my_avg:>9.1f}% {my_cost:>7.2f}")

    print()


def print_cost_analysis(all_results: list):
    print_header("COST ANALYSIS: FAILED vs SUCCESSFUL TASKS")

    success_costs = []
    fail_costs = []
    for bm_result in all_results:
        for tr in bm_result["task_results"]:
            if tr["success"]:
                success_costs.append(tr["cost_usd"])
            else:
                fail_costs.append(tr["cost_usd"])

    avg_s = sum(success_costs) / len(success_costs) if success_costs else 0
    avg_f = sum(fail_costs) / len(fail_costs) if fail_costs else 0
    ratio = (avg_f / avg_s * 100 - 100) if avg_s > 0 else 0

    print(f"\n  Successful tasks: {len(success_costs):>3} runs, avg cost ${avg_s:.2f}")
    print(f"  Failed tasks:     {len(fail_costs):>3} runs, avg cost ${avg_f:.2f}")
    print(f"  Failure premium:  +{ratio:.0f}% (paper reports 20-54%)")
    print()


def print_key_findings():
    print_header("KEY FINDINGS FROM THE OPEN AGENT LEADERBOARD")
    findings = [
        "Model choice is the primary performance driver (~70% of variance)",
        "Tool shortlisting improves performance across ALL configurations",
        "General-purpose agents CAN match specialized ones on diverse tasks",
        "Same model + different architecture = 2x+ cost difference",
        "Open-weight models trail frontier by 18-29 points on average",
        "Failed runs cost 20-54% more than successful ones",
    ]
    for i, f in enumerate(findings, 1):
        print(f"  {i}. {f}")
    print()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Open Agent Leaderboard Evaluator (Demo Mode)"
    )
    parser.add_argument(
        "--benchmark", "-b",
        choices=["swe", "browse", "appworld", "airline", "retail", "telecom"],
        help="Run a single benchmark (default: all)",
    )
    parser.add_argument(
        "--compare", "-c",
        action="store_true",
        help="Show leaderboard comparison only",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Write results to JSON file",
    )
    args = parser.parse_args()

    benchmark_map = {
        "swe": "SWE-Bench Verified",
        "browse": "BrowseComp+",
        "appworld": "AppWorld",
        "airline": "tau2-Airline",
        "retail": "tau2-Retail",
        "telecom": "tau2-Telecom",
    }

    if args.compare:
        print_leaderboard_comparison(51.9, 0.87)
        print_key_findings()
        return

    # Set up the evaluator
    agent = ExgenticProtocol(agent_name="MyAgent-Demo", model="mock-model")

    if args.benchmark:
        benchmarks_to_run = [benchmark_map[args.benchmark]]
    else:
        benchmarks_to_run = BENCHMARKS

    print_header("OPEN AGENT LEADERBOARD — EVALUATION RUN")
    print(f"\n  Agent:       {agent.agent_name}")
    print(f"  Model:       {agent.model}")
    print(f"  Benchmarks:  {len(benchmarks_to_run)}")
    print(f"  Protocol:    Exgentic Unified (Task / Context / Actions)")

    all_results = []
    for bm in benchmarks_to_run:
        sys.stdout.write(f"\n  Running {bm}...")
        sys.stdout.flush()
        result = agent.evaluate_benchmark(bm)
        all_results.append(result)
        sys.stdout.write(" done\n")

    # Display results
    print_header("BENCHMARK RESULTS")
    for r in all_results:
        print_benchmark_result(r)

    # Aggregate
    total_tasks = sum(r["tasks_run"] for r in all_results)
    total_success = sum(r["successes"] for r in all_results)
    total_cost = sum(r["total_cost"] for r in all_results)
    avg_score = total_success / total_tasks * 100 if total_tasks else 0
    avg_cost = total_cost / total_tasks if total_tasks else 0

    print_header("AGGREGATE METRICS")
    print(f"\n  Total tasks:       {total_tasks}")
    print(f"  Total successes:   {total_success}")
    print(f"  Average score:     {avg_score:.1f}%")
    print(f"  Total cost:        ${total_cost:.2f}")
    print(f"  Avg cost/task:     ${avg_cost:.2f}")

    # Cost analysis
    print_cost_analysis(all_results)

    # Leaderboard comparison
    print_leaderboard_comparison(round(avg_score, 1), round(avg_cost, 2))

    # Key findings
    print_key_findings()

    # Optional JSON output
    if args.output:
        output_data = {
            "agent": agent.agent_name,
            "model": agent.model,
            "benchmarks": all_results,
            "aggregate": {
                "total_tasks": total_tasks,
                "avg_score": round(avg_score, 1),
                "avg_cost_per_task": round(avg_cost, 2),
                "total_cost": round(total_cost, 2),
            },
        }
        # Remove non-serializable bits
        Path(args.output).write_text(json.dumps(output_data, indent=2, default=str))
        print(f"  Results written to {args.output}")

    print("  Done. See HOW_TO_USE.md for next steps.\n")


if __name__ == "__main__":
    main()
