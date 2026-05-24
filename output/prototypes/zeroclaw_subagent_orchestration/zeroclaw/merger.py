"""Result merger — combines subagent outputs into a unified report."""

from __future__ import annotations

from dataclasses import dataclass
from .agents import AgentResult


@dataclass
class MergedResult:
    """Final merged output from all subagents."""
    overall_status: str
    agent_count: int
    total_elapsed_ms: float
    summary: str
    details: list[dict]
    conflicts: list[str]


def merge_results(results: list[AgentResult], original_task: str) -> MergedResult:
    """Merge outputs from multiple subagents into a single report."""
    details = []
    conflicts = []
    all_success = True

    for r in results:
        details.append({
            "agent": r.agent_name,
            "type": r.agent_type,
            "status": r.status,
            "elapsed_ms": r.elapsed_ms,
            "output": r.output,
        })
        if r.status != "success":
            all_success = False

    # Detect conflicts between parallel outputs
    review_results = [r for r in results if r.agent_type == "review"]
    for rev in review_results:
        if rev.output and rev.output.get("verdict") == "changes_requested":
            conflicts.append(
                f"Review agent '{rev.agent_name}' requested changes "
                f"(score: {rev.output.get('quality_score', 'N/A')})"
            )

    total_ms = sum(r.elapsed_ms for r in results)
    summary_parts = [f"Task: {original_task}"]
    summary_parts.append(f"Dispatched to {len(results)} subagent(s)")
    summary_parts.append(f"Total processing: {total_ms:.0f}ms")
    if conflicts:
        summary_parts.append(f"Conflicts detected: {len(conflicts)}")
    else:
        summary_parts.append("No conflicts detected")

    return MergedResult(
        overall_status="success" if all_success and not conflicts else "needs_review",
        agent_count=len(results),
        total_elapsed_ms=round(total_ms, 1),
        summary=" | ".join(summary_parts),
        details=details,
        conflicts=conflicts,
    )
