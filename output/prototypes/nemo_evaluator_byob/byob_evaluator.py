"""
NeMo Evaluator BYOB — Bring Your Own Benchmark

End-to-end pipeline:
  1. Generate evaluation dataset (JSONL)
  2. Build judge prompt template (YAML)
  3. Create NeMo Evaluator config (YAML)
  4. Run mock evaluation (simulated LLM + judge scoring)
  5. Produce results summary with per-metric stats
"""

import json
import random
import statistics
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Sample evaluation dataset
# ---------------------------------------------------------------------------

SAMPLE_DATASET = [
    {
        "input": "Explain the difference between TCP and UDP protocols.",
        "reference": "TCP is connection-oriented, reliable, and ordered. UDP is connectionless, faster, but unreliable.",
        "context": "Networking fundamentals",
    },
    {
        "input": "What is a Python decorator and when would you use one?",
        "reference": "A decorator is a function that wraps another function to extend its behavior without modifying it. Common uses include logging, authentication, and caching.",
        "context": "Python programming",
    },
    {
        "input": "Summarize the CAP theorem in distributed systems.",
        "reference": "The CAP theorem states that a distributed system can provide at most two of three guarantees: Consistency, Availability, and Partition tolerance.",
        "context": "Distributed systems theory",
    },
    {
        "input": "How does gradient descent work in machine learning?",
        "reference": "Gradient descent iteratively adjusts model parameters in the direction that minimizes the loss function by computing gradients.",
        "context": "Machine learning optimization",
    },
    {
        "input": "What are the SOLID principles in software design?",
        "reference": "SOLID stands for Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles.",
        "context": "Software engineering",
    },
    {
        "input": "Explain how DNS resolution works step by step.",
        "reference": "DNS resolution involves querying recursive resolvers, root nameservers, TLD nameservers, and authoritative nameservers to translate a domain name to an IP address.",
        "context": "Internet infrastructure",
    },
    {
        "input": "What is the difference between supervised and unsupervised learning?",
        "reference": "Supervised learning uses labeled data to train models for prediction. Unsupervised learning finds patterns in unlabeled data through clustering or dimensionality reduction.",
        "context": "Machine learning basics",
    },
    {
        "input": "Describe how a B-tree index improves database query performance.",
        "reference": "B-tree indexes maintain sorted data in a balanced tree structure, allowing O(log n) search, insert, and delete operations, dramatically reducing full table scans.",
        "context": "Database internals",
    },
]

# Simulated model responses (varying quality for realistic demo)
MOCK_RESPONSES = [
    "TCP is a connection-oriented protocol that ensures reliable, ordered delivery of data. UDP is connectionless, providing faster but unreliable transmission without guarantees on delivery order.",
    "A decorator in Python is a design pattern that lets you add new functionality to an existing object without modifying its structure. You'd use one for cross-cutting concerns like logging or access control.",
    "CAP theorem says you can only pick two out of consistency, availability, and partition tolerance in a distributed database.",
    "Gradient descent is an optimization algorithm. It works by computing the gradient of the loss function and updating weights in the negative gradient direction to minimize error. The learning rate controls step size.",
    "SOLID is an acronym for five design principles: Single Responsibility (one reason to change), Open-Closed (open for extension, closed for modification), Liskov Substitution (subtypes must be substitutable), Interface Segregation (prefer small interfaces), and Dependency Inversion (depend on abstractions).",
    "When you type a URL, your browser asks a DNS resolver, which checks its cache. If not cached, it queries root servers, then TLD servers, then the authoritative server for the domain, returning the IP.",
    "Supervised learning needs labels — you give it examples with answers. Unsupervised doesn't need labels and instead groups similar data together.",
    "A B-tree keeps data sorted in a tree where each node can have multiple children. This allows the database to find rows quickly using binary-search-like traversal instead of scanning every row.",
]

# ---------------------------------------------------------------------------
# 2. Judge prompt template
# ---------------------------------------------------------------------------

JUDGE_PROMPT_TEMPLATE = """\
judge_prompt: |
  You are an expert evaluator assessing the quality of an LLM response.

  ## Input Question
  {{input}}

  ## Model Response
  {{response}}

  ## Reference Answer
  {{reference}}

  ## Context
  {{context}}

  ## Evaluation Criteria
  Rate the response on a scale of 1-5 for each criterion:

  - **Accuracy**: Does the response correctly answer the question?
    1 = Completely wrong, 5 = Perfectly correct
  - **Completeness**: Does it cover all important aspects?
    1 = Major gaps, 5 = Comprehensive
  - **Clarity**: Is it well-structured and easy to understand?
    1 = Confusing, 5 = Crystal clear

  Return your evaluation as JSON:
  {"accuracy": <1-5>, "completeness": <1-5>, "clarity": <1-5>, "reasoning": "<brief explanation>"}
"""

# ---------------------------------------------------------------------------
# 3. Evaluation config
# ---------------------------------------------------------------------------

EVAL_CONFIG_TEMPLATE = """\
# NeMo Evaluator BYOB Configuration
# Generated by nemo_evaluator_byob prototype

type: custom
name: {name}

dataset:
  path: {dataset_path}
  format: jsonl

evaluation:
  method: llm-as-judge
  judge:
    prompt_template: {judge_prompt_path}
    model: {judge_model}
    response_format: json
  metrics:
{metrics_yaml}
  aggregation: mean

target:
  model: {target_model}
  endpoint: {endpoint}
"""


# ---------------------------------------------------------------------------
# 4. Mock judge (simulates LLM-as-judge scoring)
# ---------------------------------------------------------------------------

def mock_judge_score(response: str, reference: str) -> dict:
    """Simulate a judge model scoring a response against reference.

    Uses simple heuristics (word overlap, length ratio) to produce
    deterministic-ish scores that vary realistically across examples.
    """
    random.seed(hash(response + reference) % 2**32)

    # Word overlap heuristic for accuracy
    resp_words = set(response.lower().split())
    ref_words = set(reference.lower().split())
    overlap = len(resp_words & ref_words) / max(len(ref_words), 1)
    accuracy = min(5, max(1, round(overlap * 5 + random.uniform(-0.5, 0.5))))

    # Length ratio for completeness
    length_ratio = len(response) / max(len(reference), 1)
    completeness = min(5, max(1, round(min(length_ratio, 1.5) * 3.5 + random.uniform(-0.5, 0.5))))

    # Sentence structure for clarity
    sentences = response.count('.') + response.count('!') + response.count('?')
    clarity = min(5, max(1, round(min(sentences, 4) * 1.2 + random.uniform(0, 1))))

    reasons = []
    if accuracy >= 4:
        reasons.append("Response aligns well with reference answer")
    elif accuracy <= 2:
        reasons.append("Response diverges significantly from reference")
    else:
        reasons.append("Partially correct but missing key details")

    if completeness >= 4:
        reasons.append("covers the topic comprehensively")
    else:
        reasons.append("could be more thorough")

    return {
        "accuracy": accuracy,
        "completeness": completeness,
        "clarity": clarity,
        "reasoning": "; ".join(reasons),
    }


# ---------------------------------------------------------------------------
# 5. Pipeline orchestration
# ---------------------------------------------------------------------------

def create_output_dir(base: str = "output") -> Path:
    out = Path(base)
    out.mkdir(parents=True, exist_ok=True)
    (out / "results").mkdir(exist_ok=True)
    return out


def write_dataset(out: Path) -> Path:
    path = out / "eval_dataset.jsonl"
    with open(path, "w") as f:
        for item in SAMPLE_DATASET:
            f.write(json.dumps(item) + "\n")
    return path


def write_judge_prompt(out: Path) -> Path:
    path = out / "judge_prompt.yaml"
    path.write_text(JUDGE_PROMPT_TEMPLATE)
    return path


def write_eval_config(out: Path, dataset_path: Path, judge_path: Path,
                       benchmark_name: str = "tech-knowledge-benchmark",
                       judge_model: str = "nim/meta-llama/llama-3.1-70b-instruct",
                       target_model: str = "my-finetuned-model",
                       endpoint: str = "http://localhost:8000/v1") -> Path:
    metrics = [
        {"name": "accuracy", "type": "numeric", "range": [1, 5]},
        {"name": "completeness", "type": "numeric", "range": [1, 5]},
        {"name": "clarity", "type": "numeric", "range": [1, 5]},
    ]
    metrics_yaml = ""
    for m in metrics:
        metrics_yaml += f"    - name: {m['name']}\n"
        metrics_yaml += f"      type: {m['type']}\n"
        metrics_yaml += f"      range: {m['range']}\n"

    config_text = EVAL_CONFIG_TEMPLATE.format(
        name=benchmark_name,
        dataset_path=str(dataset_path),
        judge_prompt_path=str(judge_path),
        judge_model=judge_model,
        target_model=target_model,
        endpoint=endpoint,
        metrics_yaml=metrics_yaml,
    )
    path = out / "eval_config.yaml"
    path.write_text(config_text)
    return path


def run_evaluation(out: Path) -> list[dict]:
    """Run mock evaluation: pair each dataset item with a simulated
    model response, then score it with the mock judge."""
    results = []
    for i, (item, response) in enumerate(zip(SAMPLE_DATASET, MOCK_RESPONSES)):
        scores = mock_judge_score(response, item["reference"])
        result = {
            "id": i + 1,
            "input": item["input"],
            "response": response,
            "reference": item["reference"],
            "scores": scores,
        }
        results.append(result)

    # Write detailed results
    results_path = out / "results" / "eval_results.jsonl"
    with open(results_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    return results


def print_summary(results: list[dict]) -> None:
    """Print a formatted summary table of evaluation results."""
    metrics = ["accuracy", "completeness", "clarity"]

    print("\n" + "=" * 72)
    print("  NeMo Evaluator BYOB — Evaluation Results")
    print("=" * 72)
    print(f"  Benchmark: tech-knowledge-benchmark")
    print(f"  Examples evaluated: {len(results)}")
    print(f"  Judge: mock-llm-judge (simulated)")
    print("-" * 72)

    # Per-example table
    print(f"\n  {'#':<4} {'Accuracy':<10} {'Complete':<10} {'Clarity':<10} {'Question (truncated)'}")
    print(f"  {'—'*4} {'—'*9} {'—'*9} {'—'*9} {'—'*30}")
    for r in results:
        s = r["scores"]
        q = r["input"][:40] + ("..." if len(r["input"]) > 40 else "")
        print(f"  {r['id']:<4} {s['accuracy']:<10} {s['completeness']:<10} {s['clarity']:<10} {q}")

    # Aggregate stats
    print(f"\n{'—' * 72}")
    print(f"  {'Metric':<16} {'Mean':>8} {'Median':>8} {'Std Dev':>8} {'Min':>6} {'Max':>6}")
    print(f"  {'—'*15} {'—'*8} {'—'*8} {'—'*8} {'—'*6} {'—'*6}")
    overall_scores = []
    for m in metrics:
        vals = [r["scores"][m] for r in results]
        overall_scores.extend(vals)
        mean = statistics.mean(vals)
        median = statistics.median(vals)
        stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
        print(f"  {m:<16} {mean:>8.2f} {median:>8.1f} {stdev:>8.2f} {min(vals):>6} {max(vals):>6}")

    overall_mean = statistics.mean(overall_scores)
    print(f"\n  Overall score (mean of all metrics): {overall_mean:.2f} / 5.00")

    # Flag low-scoring examples
    low = [r for r in results if any(r["scores"][m] <= 2 for m in metrics)]
    if low:
        print(f"\n  ⚠ Low-scoring examples ({len(low)} flagged):")
        for r in low:
            worst = min(metrics, key=lambda m: r["scores"][m])
            print(f"    #{r['id']}: {worst}={r['scores'][worst]} — {r['input'][:50]}...")
    else:
        print(f"\n  ✓ No low-scoring examples (all metrics ≥ 3)")

    print("=" * 72)


def main():
    print("NeMo Evaluator BYOB — Bring Your Own Benchmark Demo")
    print("=" * 50)

    out = create_output_dir()

    # Step 1: Generate dataset
    print("\n[1/5] Generating evaluation dataset...")
    ds_path = write_dataset(out)
    print(f"      → {ds_path}  ({len(SAMPLE_DATASET)} examples)")

    # Step 2: Write judge prompt
    print("[2/5] Creating judge prompt template...")
    jp_path = write_judge_prompt(out)
    print(f"      → {jp_path}")

    # Step 3: Build eval config
    print("[3/5] Building evaluation config...")
    cfg_path = write_eval_config(out, ds_path, jp_path)
    print(f"      → {cfg_path}")

    # Step 4: Run mock evaluation
    print("[4/5] Running evaluation (mock judge)...")
    results = run_evaluation(out)
    print(f"      → {out / 'results' / 'eval_results.jsonl'}")

    # Step 5: Print summary
    print("[5/5] Generating results summary...")
    print_summary(results)

    # Write summary JSON
    metrics = ["accuracy", "completeness", "clarity"]
    summary = {}
    for m in metrics:
        vals = [r["scores"][m] for r in results]
        summary[m] = {"mean": round(statistics.mean(vals), 2),
                       "median": statistics.median(vals),
                       "min": min(vals), "max": max(vals)}
    summary_path = out / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\n  Results saved to {out / 'results/'}")
    print("  Done.\n")


if __name__ == "__main__":
    main()
