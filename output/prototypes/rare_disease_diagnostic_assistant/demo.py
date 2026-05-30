#!/usr/bin/env python3
"""
Rare Disease Diagnostic Assistant — Demo

Runs three mock patient cases through the diagnostic engine and prints
structured differential diagnosis reports. No API keys required.
"""

import json
import sys
from diagnostic_engine import PatientProfile, rank_diagnoses, generate_report, format_report_text

DEMO_CASES = [
    PatientProfile(
        patient_id="CASE-001",
        hpo_terms=[
            "HP:0001250",  # Seizures
            "HP:0001263",  # Global developmental delay
            "HP:0000256",  # Macrocephaly
        ],
        negative_findings=["HP:0001249"],  # No intellectual disability
        age_onset="2 years",
        sex="F",
        genetic_tests_done=["WES", "CMA"],
    ),
    PatientProfile(
        patient_id="CASE-002",
        hpo_terms=[
            "HP:0003202",  # Skeletal muscle atrophy
            "HP:0001252",  # Hypotonia
            "HP:0001371",  # Flexion contracture
            "HP:0002650",  # Scoliosis
            "HP:0001644",  # Dilated cardiomyopathy
        ],
        negative_findings=[],
        age_onset="4 years",
        sex="M",
        genetic_tests_done=[],
    ),
    PatientProfile(
        patient_id="CASE-003",
        hpo_terms=[
            "HP:0002240",  # Hepatomegaly
            "HP:0001903",  # Anemia
            "HP:0001250",  # Seizures
            "HP:0001252",  # Hypotonia
            "HP:0001508",  # Failure to thrive
            "HP:0011968",  # Feeding difficulties
        ],
        negative_findings=["HP:0000256"],  # No macrocephaly
        age_onset="6 months",
        sex="M",
        genetic_tests_done=["CMA"],
    ),
]


def run_demo():
    print()
    print("  Rare Disease Diagnostic Assistant")
    print("  Inspired by Boston Children's Hospital + AI approach")
    print("  (Demo with mock data — no API keys needed)")
    print()

    all_reports = []

    for case in DEMO_CASES:
        print(case.describe())
        print()

        candidates = rank_diagnoses(case, top_n=3)
        report = generate_report(case, candidates)
        all_reports.append(report)

        print(format_report_text(report))
        print()

    # Also dump JSON for the first case to show structured output
    print("-" * 72)
    print("  STRUCTURED JSON OUTPUT (Case 001)")
    print("-" * 72)
    print(json.dumps(all_reports[0], indent=2))
    print()

    print(f"Processed {len(DEMO_CASES)} cases. Done.")
    return 0


if __name__ == "__main__":
    sys.exit(run_demo())
