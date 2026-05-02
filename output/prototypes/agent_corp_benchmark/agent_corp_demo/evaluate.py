"""
Evaluation and reporting for agent-corp benchmark results.
"""

from tabulate import tabulate


def compute_summary(results):
    """Compute aggregate metrics from a list of result dicts."""
    total = len(results)
    completed = sum(1 for r in results if r["completed"])
    avg_quality = (
        sum(r["code_quality"] for r in results if r["completed"]) / max(completed, 1)
    )
    avg_steps = sum(r["steps"] for r in results) / max(total, 1)
    avg_tokens = sum(r["tokens_used"] for r in results) / max(total, 1)
    avg_tool = sum(r["tool_usage_score"] for r in results) / max(total, 1)

    return {
        "total_tasks": total,
        "completed": completed,
        "completion_rate": round(completed / max(total, 1) * 100, 1),
        "avg_code_quality": round(avg_quality, 2),
        "avg_steps": round(avg_steps, 1),
        "avg_tokens": round(avg_tokens, 0),
        "avg_tool_usage": round(avg_tool, 2),
    }


def summary_by_category(results):
    """Group results by category and compute per-category summaries."""
    categories = {}
    for r in results:
        categories.setdefault(r["category"], []).append(r)
    return {cat: compute_summary(res) for cat, res in sorted(categories.items())}


def print_task_table(results):
    """Print a table of individual task results."""
    rows = []
    for r in results:
        status = "PASS" if r["completed"] else "FAIL"
        rows.append([
            r["task_id"],
            r["category"],
            r["difficulty"],
            status,
            r["steps"],
            r["tokens_used"],
            r["code_quality"],
            r["tool_usage_score"],
        ])
    headers = ["Task", "Category", "Difficulty", "Status", "Steps", "Tokens", "Quality", "Tool Use"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_summary(summary, label="Overall"):
    """Print a summary block."""
    print(f"\n{'='*50}")
    print(f"  {label} Summary")
    print(f"{'='*50}")
    print(f"  Tasks:           {summary['completed']}/{summary['total_tasks']} completed "
          f"({summary['completion_rate']}%)")
    print(f"  Avg Code Quality: {summary['avg_code_quality']}")
    print(f"  Avg Steps:        {summary['avg_steps']}")
    print(f"  Avg Tokens:       {summary['avg_tokens']:.0f}")
    print(f"  Avg Tool Usage:   {summary['avg_tool_usage']}")
    print(f"{'='*50}")


def print_category_table(cat_summaries):
    """Print a comparison table across categories."""
    rows = []
    for cat, s in cat_summaries.items():
        rows.append([
            cat,
            f"{s['completed']}/{s['total_tasks']}",
            f"{s['completion_rate']}%",
            s["avg_code_quality"],
            s["avg_steps"],
            f"{s['avg_tokens']:.0f}",
        ])
    headers = ["Category", "Completed", "Rate", "Quality", "Avg Steps", "Avg Tokens"]
    print("\nPer-Category Breakdown:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_agent_comparison(agent_summaries):
    """Print side-by-side agent comparison."""
    rows = []
    for agent, s in agent_summaries.items():
        rows.append([
            agent,
            f"{s['completed']}/{s['total_tasks']}",
            f"{s['completion_rate']}%",
            s["avg_code_quality"],
            s["avg_steps"],
            f"{s['avg_tokens']:.0f}",
            s["avg_tool_usage"],
        ])
    headers = ["Agent", "Completed", "Rate", "Quality", "Steps", "Tokens", "Tool Use"]
    print("\nAgent Comparison:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
