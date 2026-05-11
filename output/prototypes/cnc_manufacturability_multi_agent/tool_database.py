"""
Shop tool inventory database and matching logic.
Agent 2 in the pipeline — pure deterministic, no LLM.
"""

# Simulated machine shop tool inventory
SHOP_INVENTORY = {
    "end_mills": [
        {"id": "EM-001", "type": "flat_end_mill", "diameter_mm": 6.0, "material": "carbide", "max_rpm": 12000},
        {"id": "EM-002", "type": "flat_end_mill", "diameter_mm": 10.0, "material": "carbide", "max_rpm": 10000},
        {"id": "EM-003", "type": "flat_end_mill", "diameter_mm": 16.0, "material": "carbide", "max_rpm": 8000},
        {"id": "EM-004", "type": "ball_end_mill", "diameter_mm": 8.0, "material": "carbide", "max_rpm": 11000},
        {"id": "EM-005", "type": "flat_end_mill", "diameter_mm": 3.0, "material": "HSS", "max_rpm": 15000},
    ],
    "drills": [
        {"id": "DR-001", "type": "twist_drill", "diameter_mm": 5.0, "material": "carbide", "max_rpm": 14000},
        {"id": "DR-002", "type": "twist_drill", "diameter_mm": 8.0, "material": "carbide", "max_rpm": 12000},
        {"id": "DR-003", "type": "twist_drill", "diameter_mm": 10.0, "material": "HSS", "max_rpm": 10000},
        {"id": "DR-004", "type": "center_drill", "diameter_mm": 3.0, "material": "carbide", "max_rpm": 16000},
        {"id": "DR-005", "type": "twist_drill", "diameter_mm": 6.8, "material": "carbide", "max_rpm": 13000},
        {"id": "DR-006", "type": "twist_drill", "diameter_mm": 6.0, "material": "carbide", "max_rpm": 13500},
    ],
    "taps": [
        {"id": "TP-001", "type": "spiral_tap", "thread": "M6x1.0", "material": "HSS-E"},
        {"id": "TP-002", "type": "spiral_tap", "thread": "M8x1.25", "material": "HSS-E"},
        {"id": "TP-003", "type": "spiral_tap", "thread": "M12x1.75", "material": "HSS-E"},
    ],
    "reamers": [
        {"id": "RM-001", "type": "machine_reamer", "diameter_mm": 8.0, "material": "carbide"},
        {"id": "RM-002", "type": "machine_reamer", "diameter_mm": 10.0, "material": "carbide"},
    ],
    "chamfer_tools": [
        {"id": "CH-001", "type": "chamfer_mill", "angle_deg": 45, "diameter_mm": 12.0, "material": "carbide"},
        {"id": "CH-002", "type": "chamfer_mill", "angle_deg": 60, "diameter_mm": 8.0, "material": "carbide"},
    ],
}

# Estimated procurement costs for missing tools
PROCUREMENT_COSTS = {
    "twist_drill": 25,
    "center_drill": 20,
    "flat_end_mill": 45,
    "ball_end_mill": 55,
    "spiral_tap": 15,
    "machine_reamer": 60,
    "chamfer_mill": 40,
    "thread_mill": 80,
}


def match_tools(required_operations: list[dict]) -> dict:
    """
    Match required operations against shop inventory.
    Returns availability status for each operation.
    """
    results = {
        "matched": [],
        "missing": [],
        "total_required": len(required_operations),
    }

    for op in required_operations:
        tool_type = op.get("tool_type", "")
        diameter = op.get("diameter_mm")
        thread = op.get("thread")
        matched = False

        # Search across inventory categories
        for category, tools in SHOP_INVENTORY.items():
            for tool in tools:
                if tool["type"] == tool_type:
                    if thread and tool.get("thread") == thread:
                        matched = True
                        results["matched"].append({
                            "operation": op["operation"],
                            "tool_id": tool["id"],
                            "tool_type": tool_type,
                            "detail": thread or f"{diameter}mm",
                        })
                        break
                    elif diameter and abs(tool.get("diameter_mm", 0) - diameter) < 0.1:
                        matched = True
                        results["matched"].append({
                            "operation": op["operation"],
                            "tool_id": tool["id"],
                            "tool_type": tool_type,
                            "detail": f"{diameter}mm",
                        })
                        break
            if matched:
                break

        if not matched:
            cost = PROCUREMENT_COSTS.get(tool_type, 50)
            results["missing"].append({
                "operation": op["operation"],
                "tool_type": tool_type,
                "detail": thread or f"{diameter}mm" if diameter else "N/A",
                "estimated_cost_usd": cost,
            })

    results["match_rate"] = (
        len(results["matched"]) / results["total_required"] * 100
        if results["total_required"] > 0
        else 0
    )
    return results
