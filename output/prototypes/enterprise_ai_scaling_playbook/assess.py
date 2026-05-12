#!/usr/bin/env python3
"""
Enterprise AI Scaling Playbook — CLI assessment tool.

Usage:
    python assess.py                  # interactive assessment
    python assess.py --demo           # run with mock data (no input required)
    python assess.py --json out.json  # save report as JSON
"""

import argparse
import json
from playbook import (
    DIMENSIONS,
    AssessmentAnswer,
    generate_playbook,
    _all_questions,
)


# ── Mock profiles for demo mode ──────────────────────────────

MOCK_PROFILES = {
    "early_stage": {
        "name": "Acme Widgets Inc. (Early-stage AI adoption)",
        "scores": {
            "ls1": 2, "ls2": 1,
            "gr1": 1, "gr2": 2,
            "tc1": 2, "tc2": 1,
            "wi1": 1, "wi2": 1,
            "qe1": 1, "qe2": 2,
            "si1": 1, "si2": 1,
        },
    },
    "mid_journey": {
        "name": "GlobalTech Solutions (Mid-journey scaling)",
        "scores": {
            "ls1": 4, "ls2": 3,
            "gr1": 3, "gr2": 3,
            "tc1": 3, "tc2": 2,
            "wi1": 3, "wi2": 2,
            "qe1": 2, "qe2": 3,
            "si1": 2, "si2": 2,
        },
    },
    "advanced": {
        "name": "NovaCorp AI-First (Advanced maturity)",
        "scores": {
            "ls1": 5, "ls2": 5,
            "gr1": 4, "gr2": 5,
            "tc1": 4, "tc2": 4,
            "wi1": 5, "wi2": 4,
            "qe1": 4, "qe2": 4,
            "si1": 3, "si2": 4,
        },
    },
}


def run_interactive() -> tuple[str, list[AssessmentAnswer]]:
    """Prompt user through the assessment interactively."""
    print("\n" + "=" * 60)
    print("  ENTERPRISE AI SCALING — MATURITY ASSESSMENT")
    print("=" * 60)
    print("\nRate each statement from 1 (strongly disagree) to 5 (strongly agree).\n")

    org_name = input("Organization name: ").strip() or "My Organization"
    answers: list[AssessmentAnswer] = []

    for dim, qid, text in _all_questions():
        while True:
            try:
                raw = input(f"  [{dim}] {text}\n  Score (1-5): ").strip()
                score = int(raw)
                if 1 <= score <= 5:
                    answers.append(AssessmentAnswer(question_id=qid, score=score))
                    break
                print("  Please enter a number between 1 and 5.")
            except (ValueError, EOFError):
                print("  Please enter a number between 1 and 5.")
    return org_name, answers


def run_demo():
    """Run all three mock profiles and print reports."""
    print("\n" + "#" * 60)
    print("  ENTERPRISE AI SCALING PLAYBOOK — DEMO MODE")
    print("  Analyzing 3 sample organizations...")
    print("#" * 60)

    for key, profile in MOCK_PROFILES.items():
        answers = [
            AssessmentAnswer(question_id=qid, score=score)
            for qid, score in profile["scores"].items()
        ]
        report = generate_playbook(profile["name"], answers)
        print("\n")
        print(report.render_text())


def main():
    parser = argparse.ArgumentParser(
        description="Enterprise AI Scaling Playbook — assess your AI maturity and get a scaling plan"
    )
    parser.add_argument("--demo", action="store_true",
                        help="Run with mock data (no input needed)")
    parser.add_argument("--json", metavar="FILE",
                        help="Also save the report as JSON")
    parser.add_argument("--profile", choices=list(MOCK_PROFILES.keys()),
                        help="Run a specific mock profile")
    args = parser.parse_args()

    if args.demo or args.profile:
        if args.profile:
            profiles = {args.profile: MOCK_PROFILES[args.profile]}
        else:
            profiles = MOCK_PROFILES

        reports = []
        print("\n" + "#" * 60)
        print("  ENTERPRISE AI SCALING PLAYBOOK — DEMO MODE")
        if len(profiles) > 1:
            print(f"  Analyzing {len(profiles)} sample organizations...")
        print("#" * 60)

        for key, profile in profiles.items():
            answers = [
                AssessmentAnswer(question_id=qid, score=score)
                for qid, score in profile["scores"].items()
            ]
            report = generate_playbook(profile["name"], answers)
            print("\n")
            print(report.render_text())
            reports.append(report)

        if args.json:
            data = []
            for r in reports:
                data.append({
                    "org_name": r.org_name,
                    "maturity_score": r.maturity_score,
                    "current_phase": r.current_phase.value,
                    "current_phase_label": r.current_phase.label,
                    "dimension_scores": r.dimension_scores,
                    "recommendations": [
                        {"phase": rec.phase.value, "priority": rec.priority,
                         "title": rec.title, "action": rec.action,
                         "rationale": rec.rationale}
                        for rec in r.recommendations
                    ],
                    "next_milestones": r.next_milestones,
                })
            with open(args.json, "w") as f:
                json.dump(data, f, indent=2)
            print(f"\nJSON report saved to: {args.json}")
    else:
        org_name, answers = run_interactive()
        report = generate_playbook(org_name, answers)
        print("\n")
        print(report.render_text())

        if args.json:
            data = {
                "org_name": report.org_name,
                "maturity_score": report.maturity_score,
                "current_phase": report.current_phase.value,
                "dimension_scores": report.dimension_scores,
                "recommendations": [
                    {"phase": r.phase.value, "priority": r.priority,
                     "title": r.title, "action": r.action, "rationale": r.rationale}
                    for r in report.recommendations
                ],
                "next_milestones": report.next_milestones,
            }
            with open(args.json, "w") as f:
                json.dump(data, f, indent=2)
            print(f"\nJSON report saved to: {args.json}")


if __name__ == "__main__":
    main()
