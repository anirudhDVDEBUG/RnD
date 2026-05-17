#!/usr/bin/env python3
"""Multi-Agent Market Lab Demo — runs a full experiment pipeline with mock data."""
import json
import random

random.seed(42)  # Reproducible demo output

from market_lab import Orchestrator, ExperimentTracker

# --- Configuration ---
CONFIG = {
    "agents": [
        {"name": "voice_ai_scout", "segment": "voice_ai", "budget": 0.30,
         "capabilities": ["web_search", "news_scan", "patent_monitor"]},
        {"name": "ad_creative_analyst", "segment": "ad_creatives", "budget": 0.25,
         "capabilities": ["web_search", "social_listen", "competitor_track"]},
        {"name": "agent_factory_watcher", "segment": "agent_factories", "budget": 0.25,
         "capabilities": ["github_scan", "news_scan", "arxiv_monitor"]},
        {"name": "leadgen_researcher", "segment": "lead_generation", "budget": 0.20,
         "capabilities": ["web_search", "pricing_monitor", "review_scan"]},
    ],
    "allocation_cap": 0.50,
    "allocation_floor": 0.08,
}


def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    print_header("MULTI-AGENT MARKET LAB — Demo Run")
    print(f"\nInitializing orchestrator with {len(CONFIG['agents'])} agents...")

    orch = Orchestrator(CONFIG)

    # Show initial status
    status = orch.status()
    print("\n--- Agent Fleet ---")
    for name, info in status["agents"].items():
        print(f"  [{info['budget']:.0%}] {name:25s} | segment: {info['segment']}")

    # Create and run experiment
    print_header("EXPERIMENT: Market Signal Discovery")
    exp = orch.tracker.create(
        name="signal_discovery_v1",
        hypothesis="Multi-agent parallel research discovers 20+ signals in 5 iterations",
        parameters={"iterations": 5, "agents": len(CONFIG["agents"])},
        success_metrics={"min_signals": 20, "min_confidence": 0.5},
        iteration_limit=5,
    )

    print(f"  Hypothesis: {exp.hypothesis}")
    print(f"  Success metrics: {exp.success_metrics}")
    print(f"\nRunning experiment ({exp.iteration_limit} iterations)...\n")

    orch.run_experiment(exp)

    # Print iteration results
    print("--- Iteration Results ---")
    for r in exp.results[:-1]:  # skip final outcome entry
        print(f"  Iter {r['iteration']:2d}: {r['signals_found']:3d} signals | "
              f"avg confidence: {r['avg_confidence']:.3f} | "
              f"top agent: {max(r['agent_performance'], key=r['agent_performance'].get)}")

    # Evaluate
    print_header("EVALUATION")
    evaluation = exp.evaluate()
    for metric, result in evaluation.items():
        status_icon = "PASS" if result["passed"] else "FAIL"
        print(f"  [{status_icon}] {metric}: target={result['target']}, actual={result['actual']}")

    # Rebalance
    print_header("DYNAMIC REBALANCING")
    print("  Rebalancing allocations based on agent performance...\n")
    changes = orch.rebalance()
    for c in changes:
        arrow = "+" if c.new_budget > c.old_budget else "-" if c.new_budget < c.old_budget else "="
        print(f"  {arrow} {c.agent_name:25s}: {c.old_budget:.0%} -> {c.new_budget:.0%} ({c.reason})")

    # Final status
    print_header("FINAL STATUS")
    final = orch.status()
    print(f"  Total signals collected: {final['total_signals']}")
    print(f"  Experiments run: {final['experiments']['total']}")
    print(f"  Experiments completed: {final['experiments']['completed']}")
    print("\n  Agent Performance Ranking:")
    ranked = sorted(final["agents"].items(), key=lambda x: x[1]["performance"], reverse=True)
    for i, (name, info) in enumerate(ranked, 1):
        print(f"    {i}. {name:25s} | score: {info['performance']:.3f} | signals: {info['signals']}")

    # Export summary
    summary = {
        "experiment": exp.name,
        "hypothesis_validated": all(r["passed"] for r in evaluation.values()),
        "total_signals": final["total_signals"],
        "agent_scores": {n: info["performance"] for n, info in final["agents"].items()},
        "allocation_after_rebalance": {n: info["budget"] for n, info in final["agents"].items()},
    }
    print(f"\n--- Exportable Summary (JSON) ---")
    print(json.dumps(summary, indent=2))
    print(f"\n{'='*60}")
    print("  Demo complete. No external API keys required.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
