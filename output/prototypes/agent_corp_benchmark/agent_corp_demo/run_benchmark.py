#!/usr/bin/env python3
"""
agent-corp benchmark demo — simulates multiple agents running through
realistic SWE tasks and compares their performance.
"""

import json
import os
import sys

from agent_corp_demo.tasks import TASKS, get_tasks, simulate_agent_run
from agent_corp_demo.evaluate import (
    compute_summary,
    summary_by_category,
    print_task_table,
    print_summary,
    print_category_table,
    print_agent_comparison,
)

AGENTS = ["claude-agent", "gpt-agent", "gemini-agent"]


def run_full_benchmark():
    print("=" * 60)
    print("  AGENT-CORP BENCHMARK — Simulated Company Environment")
    print("=" * 60)
    print(f"\n  Tasks: {len(TASKS)}  |  Agents: {len(AGENTS)}  |  "
          f"Categories: {len(set(t['category'] for t in TASKS))}\n")

    # --- Run each agent through all tasks ---
    all_results = {}
    for agent in AGENTS:
        results = [simulate_agent_run(task, agent) for task in TASKS]
        all_results[agent] = results

    # --- Per-agent detail (show first agent only to keep output readable) ---
    first_agent = AGENTS[0]
    print(f"\n--- Detailed Results: {first_agent} ---\n")
    print_task_table(all_results[first_agent])

    # --- Per-category breakdown for first agent ---
    cat_summaries = summary_by_category(all_results[first_agent])
    print_category_table(cat_summaries)
    overall = compute_summary(all_results[first_agent])
    print_summary(overall, label=f"{first_agent} Overall")

    # --- Cross-agent comparison ---
    agent_summaries = {
        agent: compute_summary(results) for agent, results in all_results.items()
    }
    print_agent_comparison(agent_summaries)

    # --- Save JSON results ---
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    results_path = os.path.join(results_dir, "benchmark_results.json")

    output = {
        agent: {
            "results": results,
            "summary": compute_summary(results),
            "by_category": summary_by_category(results),
        }
        for agent, results in all_results.items()
    }
    with open(results_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {results_path}")
    print("\nDone. Use the JSON output to build dashboards or feed into CI.\n")


if __name__ == "__main__":
    run_full_benchmark()
