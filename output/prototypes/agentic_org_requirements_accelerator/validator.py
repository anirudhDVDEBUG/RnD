"""Cross-validate agent outputs and produce the final consolidated report."""

from typing import Dict, List
from datetime import datetime


def cross_validate(stories: List[Dict], dep_result: Dict, estimates: List[Dict], specs: List[Dict]) -> Dict:
    """Check for inconsistencies across agent outputs."""
    warnings = []

    story_req_ids = {s["requirement_id"] for s in stories}
    estimate_req_ids = {e["requirement_id"] for e in estimates}
    spec_req_ids = {s["requirement_id"] for s in specs}

    # Check for requirements missing from any agent
    all_ids = story_req_ids | estimate_req_ids | spec_req_ids
    for rid in all_ids:
        if rid not in story_req_ids:
            warnings.append(f"{rid}: has estimate/spec but no user story decomposition")
        if rid not in estimate_req_ids:
            warnings.append(f"{rid}: has story but no feasibility estimate")

    # Check for high-risk items that are also critical priority
    high_risk_critical = [
        e for e in estimates
        if e["risk_level"] == "high" and any(
            s["priority"] == "critical" for s in stories if s["requirement_id"] == e["requirement_id"]
        )
    ]
    for item in high_risk_critical:
        warnings.append(
            f"{item['requirement_id']}: CRITICAL priority but HIGH risk — needs spike before committing to timeline"
        )

    return {
        "warnings": warnings,
        "gaps": dep_result.get("gaps", []),
        "conflicts": dep_result.get("conflicts", []),
        "total_story_points": sum(e["story_points"] for e in estimates),
        "phase_breakdown": _phase_summary(estimates),
    }


def _phase_summary(estimates: List[Dict]) -> Dict:
    phases = {}
    for e in estimates:
        phase = e.get("suggested_phase", 3)
        phases.setdefault(phase, {"count": 0, "points": 0})
        phases[phase]["count"] += 1
        phases[phase]["points"] += e["story_points"]
    return phases


def generate_report(
    project_name: str,
    description: str,
    stories: List[Dict],
    dep_result: Dict,
    estimates: List[Dict],
    specs: List[Dict],
    validation: Dict,
) -> str:
    """Generate the final markdown report."""
    lines = [
        f"# Requirements Analysis Report: {project_name}",
        f"",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"*Method: Agentic parallel analysis (4 agents)*",
        f"",
        f"> {description}",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| User Stories | {len(stories)} |",
        f"| Dependencies | {len(dep_result.get('dependencies', []))} |",
        f"| Conflicts | {len(dep_result.get('conflicts', []))} |",
        f"| Gaps Found | {len(dep_result.get('gaps', []))} |",
        f"| Total Story Points | {validation['total_story_points']} |",
        f"| Validation Warnings | {len(validation['warnings'])} |",
        f"",
    ]

    # Phase breakdown
    lines.append("## Delivery Phases\n")
    for phase_num in sorted(validation["phase_breakdown"].keys()):
        info = validation["phase_breakdown"][phase_num]
        lines.append(f"### Phase {phase_num}")
        lines.append(f"- **Items:** {info['count']}")
        lines.append(f"- **Story Points:** {info['points']}")
        phase_items = [e for e in estimates if e.get("suggested_phase") == phase_num]
        for item in phase_items:
            lines.append(f"  - [{item['complexity']}] {item['requirement_id']}: {item['text'][:60]}...")
        lines.append("")

    # Prioritized backlog
    lines.append("## Prioritized Backlog\n")
    sorted_stories = sorted(stories, key=lambda s: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(s["priority"], 4))
    for story in sorted_stories:
        lines.append(f"### {story['story_id']}: {story['title'][:80]}")
        lines.append(f"- **Priority:** {story['priority']} | **Domain:** {story['domain']} | **Source:** {story['source']}")
        lines.append(f"- **Acceptance Criteria:**")
        for ac in story["acceptance_criteria"]:
            lines.append(f"  - {ac}")
        lines.append("")

    # Technical specs
    lines.append("## Technical Specifications\n")
    for spec in specs:
        lines.append(f"### {spec['requirement_id']}: {spec['title'][:70]}")
        lines.append(f"- **Service:** {spec['service']}")
        lines.append(f"- **Tech:** {spec['suggested_tech']}")
        lines.append(f"- **API:** `{spec['api_endpoint']}`")
        lines.append(f"- **Data:** {spec['data_model_notes']}")
        lines.append(f"- **Testing:** {spec['testing_strategy']}")
        lines.append("")

    # Dependencies
    lines.append("## Dependency Graph\n")
    lines.append("```")
    seen = set()
    for dep in dep_result.get("dependencies", []):
        key = (dep["from"], dep["to"])
        if key not in seen:
            arrow = "--blocks-->" if dep["type"] == "blocks" else "---related---"
            lines.append(f"  {dep['from']} {arrow} {dep['to']}  ({dep['group']})")
            seen.add(key)
    lines.append("```\n")

    # Risk assessment
    lines.append("## Risk Assessment\n")
    lines.append("| Requirement | Complexity | Risk | Notes |")
    lines.append("|-------------|-----------|------|-------|")
    for e in sorted(estimates, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["risk_level"], 3)):
        lines.append(f"| {e['requirement_id']} | {e['complexity']} | {e['risk_level']} | {e['risk_notes'][:60]}... |")
    lines.append("")

    # Gaps and warnings
    if validation["gaps"] or validation["warnings"]:
        lines.append("## Warnings and Gaps\n")
        for gap in validation["gaps"]:
            lines.append(f"- **GAP:** {gap['message']}")
        for w in validation["warnings"]:
            lines.append(f"- **WARNING:** {w}")
        lines.append("")

    # Traceability
    lines.append("## Traceability Matrix\n")
    lines.append("| Requirement | Stories | Estimate | Spec | Phase |")
    lines.append("|-------------|---------|----------|------|-------|")
    req_ids = sorted(set(s["requirement_id"] for s in stories))
    for rid in req_ids:
        s_count = sum(1 for s in stories if s["requirement_id"] == rid)
        has_est = "Y" if any(e["requirement_id"] == rid for e in estimates) else "N"
        has_spec = "Y" if any(s["requirement_id"] == rid for s in specs) else "N"
        phase = next((e["suggested_phase"] for e in estimates if e["requirement_id"] == rid), "?")
        lines.append(f"| {rid} | {s_count} stories | {has_est} | {has_spec} | {phase} |")
    lines.append("")

    return "\n".join(lines)
