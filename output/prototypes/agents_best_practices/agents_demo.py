"""
Agents Best Practices — Workflow Pattern Simulator

Demonstrates all five agentic workflow patterns with mock agents.
No API keys required — uses simulated agent responses to show
data flow and structural patterns.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    agent_name: str
    input_data: Any
    output_data: Any
    duration_ms: float
    status: str = "success"


def mock_agent(name: str, input_data: Any, transform: callable) -> AgentResult:
    """Simulate an agent processing step with timing."""
    start = time.time()
    output = transform(input_data)
    duration = (time.time() - start) * 1000
    return AgentResult(
        agent_name=name,
        input_data=input_data,
        output_data=output,
        duration_ms=round(duration, 2),
    )


def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_result(result: AgentResult):
    print(f"  [{result.agent_name}] ({result.duration_ms}ms) -> {result.status}")
    if isinstance(result.output_data, dict):
        print(f"    Output: {json.dumps(result.output_data, indent=2)[:200]}")
    else:
        print(f"    Output: {str(result.output_data)[:200]}")


# =============================================================
# Pattern 1: Sequential Pipeline
# =============================================================
def demo_sequential_pipeline():
    print_header("Pattern 1: Sequential Pipeline")
    print("  Goal: Research -> Draft -> Edit -> Publish")
    print()

    results = []

    # Stage 1: Research
    r1 = mock_agent("Researcher", "AI agent best practices", lambda x: {
        "topic": x,
        "sources": ["Anthropic docs", "LangChain patterns", "AutoGPT lessons"],
        "key_points": ["composability", "single responsibility", "observability"],
    })
    results.append(r1)
    print_result(r1)

    # Stage 2: Draft
    r2 = mock_agent("Writer", r1.output_data, lambda x: {
        "title": f"Guide to {x['topic']}",
        "sections": [f"Section on {p}" for p in x["key_points"]],
        "word_count": 1200,
    })
    results.append(r2)
    print_result(r2)

    # Stage 3: Edit
    r3 = mock_agent("Editor", r2.output_data, lambda x: {
        **x,
        "word_count": x["word_count"] - 150,
        "edits_made": 7,
        "quality_score": 0.92,
    })
    results.append(r3)
    print_result(r3)

    # Stage 4: Publish
    r4 = mock_agent("Publisher", r3.output_data, lambda x: {
        "status": "published",
        "url": "/blog/guide-to-ai-agent-best-practices",
        "quality_score": x["quality_score"],
    })
    results.append(r4)
    print_result(r4)

    print(f"\n  Pipeline complete: {len(results)} stages executed sequentially")


# =============================================================
# Pattern 2: Parallel Fan-Out
# =============================================================
def demo_parallel_fanout():
    print_header("Pattern 2: Parallel Fan-Out")
    print("  Goal: Analyze a product from multiple angles simultaneously")
    print()

    task = {"product": "AI Code Assistant", "market": "developer tools"}

    # Simulate parallel execution
    agents = [
        ("Market Analyst", lambda x: {"market_size": "$4.2B", "growth": "32% CAGR"}),
        ("Competitor Scout", lambda x: {"competitors": ["Copilot", "Cursor", "Cody"], "gaps": 2}),
        ("User Researcher", lambda x: {"personas": 3, "top_pain": "context switching"}),
        ("Tech Assessor", lambda x: {"feasibility": "high", "stack": ["Python", "LLM API"]}),
    ]

    results = []
    for name, transform in agents:
        r = mock_agent(name, task, transform)
        results.append(r)
        print_result(r)

    # Aggregation
    agg = mock_agent("Aggregator", [r.output_data for r in results], lambda x: {
        "recommendation": "Proceed",
        "confidence": 0.87,
        "inputs_combined": len(x),
    })
    print_result(agg)
    print(f"\n  Fan-out complete: {len(results)} parallel agents -> 1 aggregator")


# =============================================================
# Pattern 3: Router/Dispatcher
# =============================================================
def demo_router():
    print_header("Pattern 3: Router / Dispatcher")
    print("  Goal: Route different request types to specialist agents")
    print()

    requests = [
        {"type": "code_review", "content": "Review my Python function"},
        {"type": "writing", "content": "Draft an email to the team"},
        {"type": "analysis", "content": "Analyze Q3 sales data"},
    ]

    specialists = {
        "code_review": ("Code Reviewer", lambda x: {"issues": 2, "suggestion": "Add type hints"}),
        "writing": ("Copywriter", lambda x: {"draft": "Hi team...", "tone": "professional"}),
        "analysis": ("Data Analyst", lambda x: {"trend": "up 12%", "insight": "seasonal peak"}),
    }

    for req in requests:
        # Router decides
        route = mock_agent("Router", req, lambda x: {"routed_to": x["type"]})
        print_result(route)

        # Specialist handles
        name, transform = specialists[req["type"]]
        result = mock_agent(name, req["content"], transform)
        print_result(result)
        print()

    print("  Router dispatched 3 requests to 3 specialists")


# =============================================================
# Pattern 4: Iterative Refinement
# =============================================================
def demo_iterative_refinement():
    print_header("Pattern 4: Iterative Refinement")
    print("  Goal: Generate and refine until quality threshold (0.9) is met")
    print()

    quality_threshold = 0.9
    current_draft = {"text": "Initial draft about agents", "quality": 0.6}
    iteration = 0

    while current_draft["quality"] < quality_threshold:
        iteration += 1

        # Review
        review = mock_agent(f"Reviewer (iter {iteration})", current_draft, lambda x: {
            "score": x["quality"],
            "feedback": "Needs more specificity" if x["quality"] < 0.8 else "Minor polish needed",
        })
        print_result(review)

        # Refine
        improvement = min(0.15, quality_threshold - current_draft["quality"] + 0.02)
        refined = mock_agent(f"Refiner (iter {iteration})", current_draft, lambda x: {
            "text": f"Refined draft v{iteration}",
            "quality": round(x["quality"] + improvement, 2),
        })
        current_draft = refined.output_data
        print_result(refined)
        print()

    print(f"  Converged after {iteration} iterations (quality: {current_draft['quality']})")


# =============================================================
# Pattern 5: Human-in-the-Loop
# =============================================================
def demo_human_in_loop():
    print_header("Pattern 5: Human-in-the-Loop")
    print("  Goal: Auto-process with approval checkpoint before critical action")
    print()

    # Stage 1: Automated analysis
    analysis = mock_agent("Analyst", {"transaction": "$50,000 transfer"}, lambda x: {
        "risk_score": 0.73,
        "flags": ["large_amount", "new_recipient"],
        "recommendation": "hold_for_review",
    })
    print_result(analysis)

    # Stage 2: Checkpoint (simulated)
    checkpoint = mock_agent("Approval Gate", analysis.output_data, lambda x: {
        "checkpoint": "HUMAN_REVIEW_REQUIRED",
        "reason": f"Risk score {x['risk_score']} exceeds auto-approve threshold (0.5)",
        "action_blocked": "transfer_execution",
        "simulated_decision": "APPROVED (mock)",
    })
    print_result(checkpoint)

    # Stage 3: Execute after approval
    execution = mock_agent("Executor", checkpoint.output_data, lambda x: {
        "action": "transfer_executed",
        "approval_source": "human_reviewer",
        "audit_id": "AUD-2024-00142",
    })
    print_result(execution)

    print("\n  Human checkpoint prevented unsupervised execution of high-risk action")


# =============================================================
# Summary
# =============================================================
def print_summary():
    print_header("Summary: Agent Workflow Patterns")
    patterns = [
        ("Sequential Pipeline", "Ordered stages, each feeds the next"),
        ("Parallel Fan-Out", "Independent subtasks run simultaneously"),
        ("Router/Dispatcher", "Coordinator routes to specialists"),
        ("Iterative Refinement", "Generate-review loop until threshold"),
        ("Human-in-the-Loop", "Approval gates at critical points"),
    ]
    print()
    for i, (name, desc) in enumerate(patterns, 1):
        print(f"  {i}. {name:24s} — {desc}")

    print(f"\n  Key principles applied in all patterns:")
    print(f"    - Single responsibility per agent")
    print(f"    - Structured I/O (JSON) between agents")
    print(f"    - Observability (logged inputs/outputs/timing)")
    print(f"    - Input validation at boundaries")
    print(f"    - Graceful failure handling")
    print()
    print("  Source: github.com/DenisSergeevitch/agents-best-practices")
    print()


if __name__ == "__main__":
    demo_sequential_pipeline()
    demo_parallel_fanout()
    demo_router()
    demo_iterative_refinement()
    demo_human_in_loop()
    print_summary()
