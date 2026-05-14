"""
Agent Debugging Trace Demo
Demonstrates the agent debugging methodology from the AI Engineering Skill Pack.
Simulates an agent execution trace and performs root cause analysis.
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class TraceStep:
    step: int
    action: str
    type: str  # llm_call, tool_call, observation, decision
    input_preview: str
    output_preview: str
    tokens_used: int
    duration_ms: int
    status: str  # success, error, warning
    error_detail: Optional[str] = None


def simulate_agent_trace() -> list[TraceStep]:
    """Simulate a realistic agent execution with a failure scenario."""
    return [
        TraceStep(
            step=1, action="Initial Planning", type="llm_call",
            input_preview="Task: Find the top 3 Python packages for web scraping and compare their features",
            output_preview="Plan: 1) Search for packages 2) Get details 3) Compare features 4) Write report",
            tokens_used=1250, duration_ms=820, status="success"
        ),
        TraceStep(
            step=2, action="web_search('python web scraping packages 2025')", type="tool_call",
            input_preview='{"query": "python web scraping packages 2025", "num_results": 10}',
            output_preview="Results: beautifulsoup4, scrapy, playwright, selenium, httpx...",
            tokens_used=0, duration_ms=1200, status="success"
        ),
        TraceStep(
            step=3, action="Process search results", type="llm_call",
            input_preview="Search results with 10 packages...",
            output_preview="Selected top 3: beautifulsoup4, scrapy, playwright. Need details on each.",
            tokens_used=2100, duration_ms=950, status="success"
        ),
        TraceStep(
            step=4, action="get_package_info('beautifulsoup4')", type="tool_call",
            input_preview='{"package": "beautifulsoup4"}',
            output_preview="beautifulsoup4 4.12.3 - Screen-scraping library. Downloads: 85M/month",
            tokens_used=0, duration_ms=450, status="success"
        ),
        TraceStep(
            step=5, action="get_package_info('scrapy')", type="tool_call",
            input_preview='{"package": "scrapy"}',
            output_preview="scrapy 2.11.0 - Web crawling framework. Downloads: 4M/month",
            tokens_used=0, duration_ms=380, status="success"
        ),
        TraceStep(
            step=6, action="get_package_info('playwright')", type="tool_call",
            input_preview='{"package": "playwright"}',
            output_preview="",
            tokens_used=0, duration_ms=5000, status="error",
            error_detail="TimeoutError: Request timed out after 5000ms"
        ),
        TraceStep(
            step=7, action="Retry decision", type="llm_call",
            input_preview="Tool call failed with timeout. Should retry or proceed with partial data?",
            output_preview="Retrying get_package_info for playwright...",
            tokens_used=890, duration_ms=620, status="warning"
        ),
        TraceStep(
            step=8, action="get_package_info('playwright')", type="tool_call",
            input_preview='{"package": "playwright"}',
            output_preview="",
            tokens_used=0, duration_ms=5000, status="error",
            error_detail="TimeoutError: Request timed out after 5000ms"
        ),
        TraceStep(
            step=9, action="Retry decision", type="llm_call",
            input_preview="Second timeout on playwright. Retry again?",
            output_preview="Retrying get_package_info for playwright one more time...",
            tokens_used=920, duration_ms=580, status="warning"
        ),
        TraceStep(
            step=10, action="get_package_info('playwright')", type="tool_call",
            input_preview='{"package": "playwright"}',
            output_preview="",
            tokens_used=0, duration_ms=5000, status="error",
            error_detail="TimeoutError: Request timed out after 5000ms"
        ),
        TraceStep(
            step=11, action="Stuck in retry loop", type="llm_call",
            input_preview="Third timeout. Context window filling with repeated errors.",
            output_preview="Let me try get_package_info for playwright again with...",
            tokens_used=3200, duration_ms=1100, status="error",
            error_detail="Agent entered retry loop without fallback strategy"
        ),
    ]


def analyze_trace(trace: list[TraceStep]) -> dict:
    """Perform root cause analysis on the agent trace."""
    analysis = {
        "total_steps": len(trace),
        "successful_steps": sum(1 for s in trace if s.status == "success"),
        "failed_steps": sum(1 for s in trace if s.status == "error"),
        "warning_steps": sum(1 for s in trace if s.status == "warning"),
        "total_tokens": sum(s.tokens_used for s in trace),
        "total_duration_ms": sum(s.duration_ms for s in trace),
        "failure_points": [],
        "patterns_detected": [],
        "root_cause": "",
        "classification": "",
        "recommendations": [],
    }

    # Detect failure points
    for step in trace:
        if step.status == "error":
            analysis["failure_points"].append({
                "step": step.step,
                "action": step.action,
                "error": step.error_detail,
            })

    # Detect retry loop
    error_actions = [s.action for s in trace if s.status == "error"]
    from collections import Counter
    action_counts = Counter(error_actions)
    repeated = {a: c for a, c in action_counts.items() if c > 1}
    if repeated:
        analysis["patterns_detected"].append({
            "pattern": "Retry Loop",
            "details": f"Same action failed {max(repeated.values())} times: {list(repeated.keys())[0]}",
            "severity": "HIGH",
        })

    # Detect context waste
    error_tokens = sum(s.tokens_used for s in trace if s.status in ("error", "warning"))
    total_tokens = analysis["total_tokens"]
    if total_tokens > 0 and error_tokens / total_tokens > 0.3:
        analysis["patterns_detected"].append({
            "pattern": "Context Waste",
            "details": f"{error_tokens}/{total_tokens} tokens ({round(error_tokens/total_tokens*100)}%) spent on error handling",
            "severity": "MEDIUM",
        })

    # Root cause
    analysis["root_cause"] = (
        "Agent lacks a fallback strategy for tool failures. When get_package_info "
        "times out, the agent retries indefinitely instead of: (a) using cached/alternative "
        "data, (b) proceeding with partial results, or (c) substituting a different package."
    )
    analysis["classification"] = "Planning Issue - Missing error recovery strategy"

    analysis["recommendations"] = [
        "Add max_retries=2 parameter to tool calls with exponential backoff",
        "Implement fallback: after 2 retries, proceed with partial data and note the gap",
        "Add a 'substitute' strategy: if one package fails, try the next candidate",
        "Set a total token budget and abort gracefully when approaching the limit",
        "Log tool latency and set adaptive timeouts based on historical p95",
    ]

    return analysis


def print_trace_report(trace: list[TraceStep], analysis: dict):
    """Print formatted debugging report."""
    print("=" * 70)
    print("  AGENT EXECUTION TRACE & DEBUG REPORT")
    print("=" * 70)

    # Execution trace
    print(f"\n  EXECUTION TRACE ({len(trace)} steps)")
    print("-" * 70)
    for step in trace:
        status_icon = {"success": "[OK]", "error": "[ERR]", "warning": "[WARN]"}[step.status]
        print(f"  {step.step:>2}. {status_icon:>6}  {step.type:<12}  {step.action[:45]}")
        if step.error_detail:
            print(f"              -> {step.error_detail}")

    # Summary stats
    print(f"\n" + "=" * 70)
    print(f"  EXECUTION SUMMARY")
    print(f"=" * 70)
    print(f"  Steps:     {analysis['total_steps']} total, {analysis['successful_steps']} OK, {analysis['failed_steps']} errors, {analysis['warning_steps']} warnings")
    print(f"  Tokens:    {analysis['total_tokens']:,} used")
    print(f"  Duration:  {analysis['total_duration_ms']:,} ms ({analysis['total_duration_ms']/1000:.1f}s)")

    # Failure analysis
    print(f"\n" + "=" * 70)
    print(f"  FAILURE ANALYSIS")
    print(f"=" * 70)
    print(f"\n  Failure Points:")
    for fp in analysis["failure_points"]:
        print(f"    Step {fp['step']}: {fp['action']}")
        print(f"           {fp['error']}")

    print(f"\n  Patterns Detected:")
    for p in analysis["patterns_detected"]:
        print(f"    [{p['severity']}] {p['pattern']}: {p['details']}")

    print(f"\n  Root Cause:")
    # Wrap long text
    rc = analysis["root_cause"]
    words = rc.split()
    line = "    "
    for w in words:
        if len(line) + len(w) > 68:
            print(line)
            line = "    " + w + " "
        else:
            line += w + " "
    if line.strip():
        print(line)

    print(f"\n  Classification: {analysis['classification']}")

    # Recommendations
    print(f"\n" + "=" * 70)
    print(f"  RECOMMENDATIONS")
    print(f"=" * 70)
    for i, rec in enumerate(analysis["recommendations"], 1):
        print(f"  {i}. {rec}")
    print()


def run_agent_debug():
    """Run the agent debugging demo."""
    trace = simulate_agent_trace()
    analysis = analyze_trace(trace)
    print_trace_report(trace, analysis)

    report = {
        "trace": [asdict(s) for s in trace],
        "analysis": analysis,
    }
    with open("agent_debug_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("  Full report saved to agent_debug_report.json")
    return report


if __name__ == "__main__":
    run_agent_debug()
