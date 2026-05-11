"""
Multi-agent pipeline for CNC manufacturability analysis.

Agent 1: Operations Classifier  — determines required CNC operations from geometry
Agent 2: Tool Matcher            — deterministic inventory lookup (tool_database.py)
Agent 3: Feasibility Decision    — GO / NO-GO / CONDITIONAL verdict
Agent 4: Report Generator        — human-readable manufacturability report

In production, Agents 1/3/4 use an LLM (e.g., Qwen 2.5 7B via vLLM).
This demo uses rule-based logic so it runs without any model server.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from tool_database import match_tools

# ---------------------------------------------------------------------------
# Material knowledge base
# ---------------------------------------------------------------------------
MATERIAL_DB = {
    "Steel 304": {
        "machinability": "medium",
        "preferred_tooling": "carbide",
        "sfm_range": [200, 400],
        "notes": "Work hardens — use constant feed, avoid dwelling",
    },
    "Aluminum 6061": {
        "machinability": "excellent",
        "preferred_tooling": "HSS or carbide",
        "sfm_range": [800, 1500],
        "notes": "Use high RPM, watch for chip welding",
    },
    "Titanium Grade 5": {
        "machinability": "difficult",
        "preferred_tooling": "carbide",
        "sfm_range": [100, 200],
        "notes": "Low speed, high feed, flood coolant required",
    },
}


@dataclass
class PartSpec:
    features: dict
    material: str = "Steel 304"
    tolerance_mm: float = 0.05
    threads: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Agent 1: Operations Classifier (rule-based stand-in for LLM)
# ---------------------------------------------------------------------------
def classify_operations(spec: PartSpec) -> list[dict]:
    """Determine required CNC operations from part features."""
    ops = []
    mat_info = MATERIAL_DB.get(spec.material, MATERIAL_DB["Steel 304"])

    # Face milling for flat surfaces
    bb = spec.features.get("bounding_box_mm", [100, 100, 25])
    max_dim = max(bb[0], bb[1])
    face_mill_dia = 16.0 if max_dim <= 100 else 10.0  # pick suitable size
    ops.append({
        "operation": "Face milling (top/bottom)",
        "tool_type": "flat_end_mill",
        "diameter_mm": face_mill_dia,
        "reason": f"Flatten stock to {bb[2]}mm height",
    })

    # Drilling for each hole group
    for hole in spec.features.get("holes", []):
        ops.append({
            "operation": f"Drill {hole['count']}x Ø{hole['diameter_mm']}mm {hole.get('type', '')} holes",
            "tool_type": "twist_drill",
            "diameter_mm": hole["diameter_mm"],
            "reason": f"Depth {hole.get('depth_mm', 'through')}mm",
        })

    # Tapping for threads
    for thread in spec.features.get("threads", []):
        ops.append({
            "operation": f"Tap {thread['count']}x {thread['spec']} threads",
            "tool_type": "spiral_tap",
            "thread": thread["spec"],
            "diameter_mm": None,
            "reason": f"Depth {thread['depth_mm']}mm",
        })

    # Chamfering
    for chamfer in spec.features.get("chamfers", []):
        ops.append({
            "operation": f"Chamfer {chamfer['count']}x edges ({chamfer['size_mm']}mm)",
            "tool_type": "chamfer_mill",
            "diameter_mm": 12.0,
            "reason": "Edge break / deburr",
        })

    # Pocket milling
    for pocket in spec.features.get("pockets", []):
        em_dia = min(pocket["corner_radius_mm"] * 2, 10.0)
        ops.append({
            "operation": f"Mill pocket {pocket['length_mm']}x{pocket['width_mm']}mm, depth {pocket['depth_mm']}mm",
            "tool_type": "flat_end_mill",
            "diameter_mm": em_dia,
            "reason": f"Corner radius {pocket['corner_radius_mm']}mm",
        })

    # Reaming for tight-tolerance holes
    if spec.tolerance_mm <= 0.025:
        for hole in spec.features.get("holes", []):
            if hole["diameter_mm"] >= 8.0:
                ops.append({
                    "operation": f"Ream {hole['count']}x Ø{hole['diameter_mm']}mm holes to ±{spec.tolerance_mm}mm",
                    "tool_type": "machine_reamer",
                    "diameter_mm": hole["diameter_mm"],
                    "reason": "Tight tolerance finish",
                })

    return ops


# ---------------------------------------------------------------------------
# Agent 3: Feasibility Decision (rule-based stand-in for LLM)
# ---------------------------------------------------------------------------
def decide_feasibility(spec: PartSpec, tool_results: dict) -> dict:
    """Produce a GO / NO-GO / CONDITIONAL decision with rationale."""
    match_rate = tool_results["match_rate"]
    missing = tool_results["missing"]
    mat_info = MATERIAL_DB.get(spec.material, MATERIAL_DB["Steel 304"])

    # Risk flags
    risk_flags = []
    if mat_info["machinability"] == "difficult":
        risk_flags.append(f"Difficult material ({spec.material}) — verify spindle torque and coolant")
    if spec.tolerance_mm <= 0.01:
        risk_flags.append(f"Very tight tolerance (±{spec.tolerance_mm}mm) — may need grinding")
    bb = spec.features.get("bounding_box_mm", [0, 0, 0])
    if any(d > 300 for d in bb):
        risk_flags.append("Large part — verify work envelope of available machines")
    if mat_info["machinability"] == "medium":
        risk_flags.append(f"Verify spindle speed range for {spec.material} ({mat_info['sfm_range']} SFM)")

    # Decision logic
    total_missing_cost = sum(m["estimated_cost_usd"] for m in missing)
    action_items = [
        f"Purchase {m['tool_type']} ({m['detail']}) — est. ${m['estimated_cost_usd']}"
        for m in missing
    ]

    if match_rate == 100 and not risk_flags:
        decision = "YES"
        confidence = "HIGH"
        reason = "All required tools available, no risk flags identified."
    elif match_rate >= 70:
        decision = "CONDITIONAL"
        confidence = "HIGH" if match_rate >= 90 else "MEDIUM"
        reason = (
            f"{len(missing)} tool(s) missing (est. ${total_missing_cost} to procure). "
            f"Match rate: {match_rate:.0f}%."
        )
    else:
        decision = "NO"
        confidence = "HIGH"
        reason = f"Too many missing tools ({len(missing)}). Match rate: {match_rate:.0f}%."

    # Setup time estimate (rough heuristic)
    num_ops = tool_results["total_required"]
    setup_hours = round(0.5 + num_ops * 0.3, 1)

    return {
        "decision": decision,
        "confidence": confidence,
        "reason": reason,
        "action_items": action_items,
        "risk_flags": risk_flags,
        "estimated_setup_hours": setup_hours,
        "total_procurement_cost_usd": total_missing_cost,
    }


# ---------------------------------------------------------------------------
# Agent 4: Report Generator (rule-based stand-in for LLM)
# ---------------------------------------------------------------------------
def generate_report(
    spec: PartSpec,
    operations: list[dict],
    tool_results: dict,
    feasibility: dict,
) -> str:
    """Generate a human-readable manufacturability report."""
    bb = spec.features["bounding_box_mm"]
    lines = []
    lines.append("=" * 70)
    lines.append("  CNC MANUFACTURABILITY REPORT")
    lines.append("=" * 70)
    lines.append("")

    # Executive summary
    decision_icon = {"YES": "[PASS]", "NO": "[FAIL]", "CONDITIONAL": "[COND]"}
    lines.append(f"  VERDICT: {decision_icon.get(feasibility['decision'], '?')} {feasibility['decision']}")
    lines.append(f"  Confidence: {feasibility['confidence']}")
    lines.append(f"  {feasibility['reason']}")
    lines.append("")

    # Part overview
    lines.append("-" * 70)
    lines.append("  PART ANALYSIS")
    lines.append("-" * 70)
    lines.append(f"  File:       {spec.features.get('part_name', 'N/A')}")
    lines.append(f"  Material:   {spec.material}")
    lines.append(f"  Tolerance:  +/-{spec.tolerance_mm} mm")
    lines.append(f"  Envelope:   {bb[0]} x {bb[1]} x {bb[2]} mm")
    lines.append(f"  Volume:     {spec.features.get('volume_mm3', 0):.0f} mm3")
    lines.append(f"  Surfaces:   {spec.features.get('flat_surfaces', 0)} flat")
    hole_count = sum(h["count"] for h in spec.features.get("holes", []))
    lines.append(f"  Holes:      {hole_count} total")
    thread_count = sum(t["count"] for t in spec.features.get("threads", []))
    lines.append(f"  Threads:    {thread_count} total")
    lines.append("")

    # Operations
    lines.append("-" * 70)
    lines.append("  REQUIRED OPERATIONS")
    lines.append("-" * 70)
    for i, op in enumerate(operations, 1):
        lines.append(f"  {i:2d}. {op['operation']}")
        lines.append(f"      Tool: {op['tool_type']}  |  {op.get('reason', '')}")
    lines.append("")

    # Tool matching
    lines.append("-" * 70)
    lines.append(f"  TOOL AVAILABILITY  ({tool_results['match_rate']:.0f}% match)")
    lines.append("-" * 70)
    if tool_results["matched"]:
        lines.append("  Available:")
        for m in tool_results["matched"]:
            lines.append(f"    [OK]  {m['tool_id']:8s}  {m['tool_type']:18s}  {m['detail']}")
    if tool_results["missing"]:
        lines.append("  Missing:")
        for m in tool_results["missing"]:
            lines.append(f"    [!!]  {m['tool_type']:18s}  {m['detail']:12s}  est. ${m['estimated_cost_usd']}")
    lines.append("")

    # Risk flags
    if feasibility["risk_flags"]:
        lines.append("-" * 70)
        lines.append("  RISK FLAGS")
        lines.append("-" * 70)
        for flag in feasibility["risk_flags"]:
            lines.append(f"  * {flag}")
        lines.append("")

    # Action items
    if feasibility["action_items"]:
        lines.append("-" * 70)
        lines.append("  ACTION ITEMS")
        lines.append("-" * 70)
        for item in feasibility["action_items"]:
            lines.append(f"  -> {item}")
        lines.append("")

    # Summary
    lines.append("-" * 70)
    lines.append("  SUMMARY")
    lines.append("-" * 70)
    lines.append(f"  Est. setup time:       {feasibility['estimated_setup_hours']} hours")
    lines.append(f"  Procurement cost:      ${feasibility['total_procurement_cost_usd']}")
    lines.append(f"  Operations count:      {len(operations)}")
    mat_info = MATERIAL_DB.get(spec.material, {})
    lines.append(f"  Material machinability: {mat_info.get('machinability', 'unknown')}")
    lines.append(f"  Tooling preference:    {mat_info.get('preferred_tooling', 'N/A')}")
    lines.append("")
    lines.append("=" * 70)
    lines.append(f"  Generated by CNC Manufacturability Multi-Agent System")
    lines.append("=" * 70)

    return "\n".join(lines)
