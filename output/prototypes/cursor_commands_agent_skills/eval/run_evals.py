#!/usr/bin/env python3
"""
Behavioral eval runner for agent slash commands.

Loads command definitions and their rubrics, scores agent outputs
against each criterion, and writes results to a JSON file.

In production this would call an LLM to judge outputs; here we
use deterministic heuristic checks so the demo runs without API keys.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Heuristic scorers (stand-ins for LLM-as-judge in production)
# ---------------------------------------------------------------------------

def _has_section(output: str, heading: str) -> float:
    """Return 1.0 if a markdown heading containing `heading` exists."""
    pattern = rf"^#{{1,3}}\s+.*{re.escape(heading)}"
    return 1.0 if re.search(pattern, output, re.IGNORECASE | re.MULTILINE) else 0.0


def _has_table(output: str) -> float:
    """Return 1.0 if output contains a markdown table."""
    return 1.0 if re.search(r"\|.*\|.*\|", output) else 0.0


def _has_code_block(output: str) -> float:
    """Return 1.0 if output contains a fenced code block."""
    return 1.0 if "```" in output else 0.0


def _no_fabrication_heuristic(output: str) -> float:
    """Very rough: penalise if output references line numbers > 9999."""
    matches = re.findall(r"line\s+(\d+)", output, re.IGNORECASE)
    for m in matches:
        if int(m) > 9999:
            return 0.0
    return 1.0


HEURISTIC_MAP = {
    # /review
    "identifies_real_issues": lambda o: _has_section(o, "Findings"),
    "actionable_suggestions": lambda o: min(1.0, o.lower().count("suggest") * 0.25 + _has_code_block(o) * 0.5),
    "correct_severity": lambda o: 1.0 if any(s in o.lower() for s in ("critical", "warning", "info")) else 0.0,
    "no_false_positives": _no_fabrication_heuristic,
    "format_compliance": lambda o: min(1.0, _has_table(o) * 0.5 + _has_section(o, "Summary") * 0.25 + _has_section(o, "Verdict") * 0.25),
    # /test-plan
    "covers_public_api": lambda o: _has_section(o, "Unit Tests"),
    "edge_cases_identified": lambda o: _has_section(o, "Edge Cases"),
    "correct_categorization": lambda o: 1.0 if all(_has_section(o, h) for h in ("Unit", "Integration")) else 0.5,
    "actionable_steps": lambda o: 1.0 if _has_table(o) else 0.3,
    # /refactor
    "behavioral_equivalence": lambda o: _has_section(o, "Verification"),
    "measurable_improvement": lambda o: _has_section(o, "Rationale"),
    "before_after_clarity": lambda o: 1.0 if o.count("```") >= 4 else (0.5 if "```" in o else 0.0),
    "test_verification": lambda o: 1.0 if re.search(r"test", o, re.IGNORECASE) else 0.0,
}


# ---------------------------------------------------------------------------
# Core evaluation logic
# ---------------------------------------------------------------------------

def load_rubric(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_mock_output(command_name: str, mock_dir: Path) -> str:
    """Load a mock agent output for a command."""
    mock_file = mock_dir / f"{command_name}.md"
    if mock_file.exists():
        return mock_file.read_text()
    return ""


def score_output(output: str, rubric: dict) -> dict:
    """Score a single output against its rubric. Returns per-criterion results."""
    results = []
    weighted_sum = 0.0
    total_weight = 0.0

    for criterion in rubric["rubric"]:
        name = criterion["criterion"]
        weight = criterion["weight"]
        threshold = criterion["pass_threshold"]

        scorer = HEURISTIC_MAP.get(name, lambda _o: 0.5)
        raw_score = scorer(output)
        passed = raw_score >= threshold

        results.append({
            "criterion": name,
            "description": criterion["description"],
            "score": round(raw_score, 3),
            "threshold": threshold,
            "weight": weight,
            "passed": passed,
        })

        weighted_sum += raw_score * weight
        total_weight += weight

    overall = round(weighted_sum / total_weight, 3) if total_weight > 0 else 0.0
    overall_pass = overall >= rubric.get("overall_pass_threshold", 0.8)

    return {
        "command": rubric["command"],
        "criteria": results,
        "overall_score": overall,
        "overall_pass_threshold": rubric.get("overall_pass_threshold", 0.8),
        "passed": overall_pass,
    }


def run_all(rubrics_dir: Path, mock_dir: Path) -> list[dict]:
    """Run evals for every rubric found in rubrics_dir."""
    all_results = []
    for rubric_file in sorted(rubrics_dir.glob("*.yaml")):
        rubric = load_rubric(rubric_file)
        cmd_name = rubric_file.stem
        output = load_mock_output(cmd_name, mock_dir)
        if not output:
            print(f"  [skip] No mock output for {cmd_name}")
            continue
        result = score_output(output, rubric)
        all_results.append(result)
    return all_results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Run behavioral evals for agent commands")
    parser.add_argument("--rubrics-dir", default="eval/rubrics", help="Directory with YAML rubrics")
    parser.add_argument("--mock-dir", default="eval/mock_outputs", help="Directory with mock agent outputs")
    parser.add_argument("--output", default="eval-results.json", help="Output JSON file")
    parser.add_argument("--threshold", type=float, default=0.8, help="Global pass threshold override")
    args = parser.parse_args()

    rubrics_dir = Path(args.rubrics_dir)
    mock_dir = Path(args.mock_dir)

    if not rubrics_dir.exists():
        print(f"ERROR: Rubrics directory not found: {rubrics_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Running evals from {rubrics_dir} with mocks from {mock_dir} ...")
    results = run_all(rubrics_dir, mock_dir)

    out_path = Path(args.output)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults written to {out_path}")
    return results


if __name__ == "__main__":
    main()
