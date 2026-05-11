#!/usr/bin/env python3
"""
CNC Manufacturability Multi-Agent Pipeline
===========================================
5-stage pipeline that analyzes a part for CNC manufacturability:

  1. STEP Parser        → extract geometry features
  2. Operations Agent   → classify required CNC operations
  3. Tool Matcher       → check shop inventory
  4. Feasibility Agent  → GO / NO-GO / CONDITIONAL
  5. Report Agent       → human-readable report

Run:  python pipeline.py [--part sample_bracket|simple_plate]
                         [--material "Steel 304"|"Aluminum 6061"|"Titanium Grade 5"]
                         [--tolerance 0.05]
"""

import argparse
import json
import sys
import time

from step_parser import extract_features_mock
from agents import PartSpec, classify_operations, decide_feasibility, generate_report
from tool_database import match_tools


def run_pipeline(part_name: str, material: str, tolerance: float) -> str:
    t0 = time.time()

    # Stage 1: Feature extraction
    print("[Stage 1/5] Extracting features from STEP file...")
    features = extract_features_mock(part_name)
    t1 = time.time()
    print(f"  -> {len(features.get('holes', []))} hole groups, "
          f"{len(features.get('threads', []))} thread specs, "
          f"{len(features.get('pockets', []))} pockets  ({t1 - t0:.2f}s)")

    # Build part spec
    spec = PartSpec(
        features=features,
        material=material,
        tolerance_mm=tolerance,
        threads=features.get("threads", []),
    )

    # Stage 2: Operations classification
    print("[Stage 2/5] Classifying required CNC operations...")
    operations = classify_operations(spec)
    t2 = time.time()
    print(f"  -> {len(operations)} operations identified  ({t2 - t1:.2f}s)")

    # Stage 3: Tool matching
    print("[Stage 3/5] Matching against shop tool inventory...")
    tool_results = match_tools(operations)
    t3 = time.time()
    print(f"  -> {len(tool_results['matched'])} matched, "
          f"{len(tool_results['missing'])} missing  "
          f"({tool_results['match_rate']:.0f}% match)  ({t3 - t2:.2f}s)")

    # Stage 4: Feasibility decision
    print("[Stage 4/5] Making feasibility decision...")
    feasibility = decide_feasibility(spec, tool_results)
    t4 = time.time()
    print(f"  -> {feasibility['decision']} (confidence: {feasibility['confidence']})  ({t4 - t3:.2f}s)")

    # Stage 5: Report generation
    print("[Stage 5/5] Generating manufacturability report...")
    report = generate_report(spec, operations, tool_results, feasibility)
    t5 = time.time()
    print(f"  -> Report ready  ({t5 - t4:.2f}s)")

    total = t5 - t0
    print(f"\nPipeline completed in {total:.2f}s\n")

    # Also dump structured JSON
    structured = {
        "part": features.get("part_name"),
        "material": material,
        "tolerance_mm": tolerance,
        "operations_count": len(operations),
        "tool_match_rate": tool_results["match_rate"],
        "decision": feasibility["decision"],
        "confidence": feasibility["confidence"],
        "missing_tools": len(tool_results["missing"]),
        "procurement_cost_usd": feasibility["total_procurement_cost_usd"],
        "setup_hours": feasibility["estimated_setup_hours"],
        "risk_flags": feasibility["risk_flags"],
        "pipeline_time_seconds": round(total, 3),
    }
    print("--- Structured JSON Output ---")
    print(json.dumps(structured, indent=2))
    print()

    return report


def main():
    parser = argparse.ArgumentParser(description="CNC Manufacturability Multi-Agent Pipeline")
    parser.add_argument("--part", default="sample_bracket",
                        choices=["sample_bracket", "simple_plate"],
                        help="Mock part to analyze")
    parser.add_argument("--material", default="Steel 304",
                        help="Material type (e.g., 'Steel 304', 'Aluminum 6061', 'Titanium Grade 5')")
    parser.add_argument("--tolerance", type=float, default=0.05,
                        help="Required tolerance in mm")
    args = parser.parse_args()

    report = run_pipeline(args.part, args.material, args.tolerance)
    print(report)


if __name__ == "__main__":
    main()
