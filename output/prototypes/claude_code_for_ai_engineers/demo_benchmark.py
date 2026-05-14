"""
Benchmark Reporting Demo
Demonstrates the benchmark reporting methodology from the AI Engineering Skill Pack.
Generates a structured evaluation report with mock model comparisons.
"""

import json
import random
import math
from datetime import datetime

random.seed(42)


BENCHMARK_SUITES = {
    "text_classification": {
        "name": "Text Classification (SST-2 subset)",
        "num_samples": 200,
        "metric": "accuracy",
    },
    "summarization": {
        "name": "Summarization (CNN/DM subset)",
        "num_samples": 100,
        "metric": "rouge_l",
    },
    "code_generation": {
        "name": "Code Generation (HumanEval subset)",
        "num_samples": 50,
        "metric": "pass@1",
    },
    "qa": {
        "name": "Question Answering (SQuAD subset)",
        "num_samples": 150,
        "metric": "f1",
    },
}

MODELS = {
    "model_a": {"name": "MyModel-7B (fine-tuned)", "params": "7B", "type": "candidate"},
    "model_b": {"name": "Baseline-7B", "params": "7B", "type": "baseline"},
    "model_c": {"name": "GPT-3.5-turbo (ref)", "params": "unknown", "type": "reference"},
}

# Simulated performance profiles
PERFORMANCE_PROFILES = {
    "model_a": {"text_classification": 0.89, "summarization": 0.42, "code_generation": 0.38, "qa": 0.82},
    "model_b": {"text_classification": 0.85, "summarization": 0.38, "code_generation": 0.31, "qa": 0.78},
    "model_c": {"text_classification": 0.92, "summarization": 0.45, "code_generation": 0.67, "qa": 0.88},
}


def simulate_benchmark_run(model_id: str, benchmark_id: str, num_runs: int = 3) -> dict:
    """Simulate running a benchmark with variance across runs."""
    base_score = PERFORMANCE_PROFILES[model_id][benchmark_id]
    suite = BENCHMARK_SUITES[benchmark_id]

    scores = []
    latencies = []
    for _ in range(num_runs):
        noise = random.gauss(0, 0.02)
        score = max(0, min(1, base_score + noise))
        scores.append(round(score, 4))
        latency = random.uniform(0.5, 3.0) * (1 if "7B" in MODELS[model_id]["params"] else 2)
        latencies.append(round(latency, 2))

    mean_score = round(sum(scores) / len(scores), 4)
    std_score = round(math.sqrt(sum((s - mean_score) ** 2 for s in scores) / len(scores)), 4)

    return {
        "model": model_id,
        "benchmark": benchmark_id,
        "metric": suite["metric"],
        "num_samples": suite["num_samples"],
        "num_runs": num_runs,
        "scores": scores,
        "mean": mean_score,
        "std": std_score,
        "mean_latency_ms": round(sum(latencies) / len(latencies) * 1000),
        "p95_latency_ms": round(sorted(latencies)[int(len(latencies) * 0.95)] * 1000),
    }


def run_benchmark_report() -> dict:
    """Run full benchmark evaluation and produce report."""
    print("=" * 70)
    print("  BENCHMARK EVALUATION REPORT")
    print("=" * 70)
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Models:     {len(MODELS)}")
    print(f"  Benchmarks: {len(BENCHMARK_SUITES)}")
    print(f"  Runs/bench: 3 (for variance estimation)")

    all_results = []

    for bench_id, suite in BENCHMARK_SUITES.items():
        print(f"\n{'=' * 70}")
        print(f"  {suite['name']}")
        print(f"  Metric: {suite['metric']} | Samples: {suite['num_samples']}")
        print(f"{'-' * 70}")
        print(f"  {'Model':<30} {'Mean':>8} {'Std':>8} {'Latency(ms)':>12} {'vs Baseline':>12}")
        print(f"  {'-'*28:<30} {'---':>8} {'---':>8} {'---':>12} {'---':>12}")

        bench_results = {}
        for model_id in MODELS:
            result = simulate_benchmark_run(model_id, bench_id)
            bench_results[model_id] = result
            all_results.append(result)

        baseline_mean = bench_results["model_b"]["mean"]
        for model_id, result in bench_results.items():
            delta = result["mean"] - baseline_mean
            delta_str = f"{'+' if delta >= 0 else ''}{delta:.4f}"
            model_name = MODELS[model_id]["name"][:28]
            marker = " *" if MODELS[model_id]["type"] == "candidate" else ""
            print(f"  {model_name + marker:<30} {result['mean']:>8.4f} {result['std']:>8.4f} {result['mean_latency_ms']:>12} {delta_str:>12}")

    # Overall summary
    print(f"\n{'=' * 70}")
    print(f"  OVERALL SUMMARY")
    print(f"{'=' * 70}")

    for model_id, model_info in MODELS.items():
        model_results = [r for r in all_results if r["model"] == model_id]
        avg_score = round(sum(r["mean"] for r in model_results) / len(model_results), 4)
        avg_latency = round(sum(r["mean_latency_ms"] for r in model_results) / len(model_results))
        print(f"  {model_info['name']:<30} avg_score={avg_score:.4f}  avg_latency={avg_latency}ms")

    # Key findings
    print(f"\n  KEY FINDINGS")
    print(f"  " + "-" * 40)

    candidate_results = [r for r in all_results if r["model"] == "model_a"]
    baseline_results = [r for r in all_results if r["model"] == "model_b"]

    wins = sum(1 for c, b in zip(candidate_results, baseline_results) if c["mean"] > b["mean"])
    print(f"  - Candidate beats baseline on {wins}/{len(BENCHMARK_SUITES)} benchmarks")

    weakest = min(candidate_results, key=lambda r: r["mean"])
    print(f"  - Weakest area: {BENCHMARK_SUITES[weakest['benchmark']]['name']} ({weakest['mean']:.4f})")

    ref_results = [r for r in all_results if r["model"] == "model_c"]
    ref_gap = round(sum(r["mean"] for r in ref_results) / len(ref_results) -
                     sum(r["mean"] for r in candidate_results) / len(candidate_results), 4)
    print(f"  - Gap to reference (GPT-3.5): {ref_gap:+.4f} average")
    print(f"  - Largest gap on code generation (expected for 7B model)")
    print()

    report = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "models": {k: v["name"] for k, v in MODELS.items()},
            "benchmarks": list(BENCHMARK_SUITES.keys()),
            "runs_per_benchmark": 3,
        },
        "results": all_results,
        "findings": {
            "candidate_wins": f"{wins}/{len(BENCHMARK_SUITES)}",
            "weakest_benchmark": weakest["benchmark"],
            "reference_gap": ref_gap,
        },
    }
    return report


if __name__ == "__main__":
    report = run_benchmark_report()
    with open("benchmark_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("  Full report saved to benchmark_report.json")
