#!/usr/bin/env python3
"""OncoAgent CLI — run clinical decision support queries from the command line."""

import sys
from oncoagent.graph import run_pipeline

DEMO_CASES = [
    {
        "name": "Tier 1 — Standard NSCLC with EGFR mutation",
        "query": (
            "Patient John Smith (MRN: 12345) diagnosed with stage IV NSCLC, "
            "EGFR exon 19 deletion. No prior treatment. DOB: 03/15/1958. "
            "Requesting first-line therapy recommendation."
        ),
    },
    {
        "name": "Tier 2 — Complex multi-mutation melanoma",
        "query": (
            "Patient Jane Doe (MRN: 67890) with stage IV melanoma, BRAF V600E "
            "and KRAS G12C mutations. Prior treatment with pembrolizumab (progressed). "
            "Email: jane.doe@example.com. Phone: 555-123-4567. "
            "Requesting second-line therapy options."
        ),
    },
    {
        "name": "Tier 1 — HER2-positive breast cancer",
        "query": (
            "Stage IV HER2-positive breast cancer. No prior systemic therapy for "
            "metastatic disease. Requesting first-line treatment recommendation."
        ),
    },
    {
        "name": "Low-confidence — Unmatched rare query",
        "query": (
            "Rare adrenocortical carcinoma with TP53 and CTNNB1 mutations, "
            "post-mitotane failure. Requesting experimental options."
        ),
    },
]

SEPARATOR = "=" * 72


def run_demo():
    print(SEPARATOR)
    print("  OncoAgent — Dual-Tier Multi-Agent Clinical Decision Support")
    print("  Privacy-Preserving Oncology AI with Corrective RAG")
    print(SEPARATOR)
    print()

    for i, case in enumerate(DEMO_CASES, 1):
        print(f"{'─' * 72}")
        print(f"  CASE {i}: {case['name']}")
        print(f"{'─' * 72}")
        print()

        state = run_pipeline(case["query"])

        # Show PHI redaction
        print("INPUT (raw):")
        print(f"  {case['query'][:100]}...")
        print()
        print("INPUT (redacted):")
        print(f"  {state.redacted_query[:100]}...")
        print()

        # Show routing
        print(f"ROUTING: Complexity={state.complexity_score:.2f} → "
              f"Tier {state.selected_tier} | "
              f"RAG Confidence={state.rag_confidence:.3f}")
        print()

        # Show output
        print("OUTPUT:")
        for line in state.final_output.split("\n"):
            print(f"  {line}")
        print()

        # Show audit trail
        print("AUDIT TRAIL:")
        for entry in state.audit_log:
            print(f"  → {entry}")
        print()

    print(SEPARATOR)
    print("  Demo complete. All queries processed with zero PHI leakage.")
    print(SEPARATOR)


def run_single(query: str):
    print(f"Query: {query}")
    print()
    state = run_pipeline(query)
    print(f"Tier: {state.selected_tier} | Complexity: {state.complexity_score:.2f} | "
          f"RAG Confidence: {state.rag_confidence:.3f}")
    print()
    print(state.final_output)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_single(" ".join(sys.argv[1:]))
    else:
        run_demo()
