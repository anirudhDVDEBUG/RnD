#!/usr/bin/env python3
"""
Healthcare Clinical Workflow Optimizer — Interactive Demo

Runs through 6 realistic clinical scenarios showing:
  1. Multi-workflow draft generation (SOAP notes, discharge summaries, etc.)
  2. Role-based access control
  3. Clinician review (approve / edit / reject)
  4. HIPAA-aware audit trail
  5. Impact metrics dashboard

No API keys required — uses mock AI generation with realistic templates.
"""

import sys
import json
from workflow_engine import ClinicalWorkflowOptimizer
from mock_data import ENCOUNTERS, ACCESS_DENIED_SCENARIO

# ANSI colors for terminal readability
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
DIM = "\033[2m"
RESET = "\033[0m"

DIVIDER = f"{DIM}{'=' * 72}{RESET}"
THIN_DIV = f"{DIM}{'-' * 72}{RESET}"


def header(text: str):
    print(f"\n{DIVIDER}")
    print(f"{BOLD}{CYAN}{text}{RESET}")
    print(DIVIDER)


def sub_header(text: str):
    print(f"\n{THIN_DIV}")
    print(f"{BOLD}{text}{RESET}")
    print(THIN_DIV)


def label(key: str, val: str):
    print(f"  {YELLOW}{key}:{RESET} {val}")


def main():
    optimizer = ClinicalWorkflowOptimizer()

    # ── Title ──
    print(f"""
{BOLD}{CYAN}
  Healthcare Clinical Workflow Optimizer
  ======================================{RESET}
  AI-powered documentation assistant that drafts clinical notes,
  patient messages, and care plans — always with human-in-the-loop review.

  Inspired by: AdventHealth + OpenAI partnership for whole-person care
  Demo data: 100% fictional (no real PHI)
""")

    # ── Step 1: Generate drafts for all encounters ──
    header("STEP 1  Generate AI Drafts Across 6 Clinical Workflows")

    for i, encounter in enumerate(ENCOUNTERS, 1):
        wf = encounter["workflow_type"]
        cid = encounter["clinician_id"]
        role = encounter["role"]
        ctx = encounter["context"]

        sub_header(f"Scenario {i}: {wf.replace('_', ' ').title()}")
        label("Clinician", f"{cid} ({role})")
        label("Patient", ctx.get("patient_name", "N/A"))

        result = optimizer.generate_draft(wf, ctx, cid, role)

        label("Status", f"{GREEN}{result['status']}{RESET}")
        label("Word count", str(result["word_count"]))
        print(f"\n{DIM}--- Draft Preview (first 6 lines) ---{RESET}")
        lines = result["draft"].strip().split("\n")
        for line in lines[:6]:
            print(f"  {line}")
        if len(lines) > 6:
            print(f"  {DIM}... ({len(lines) - 6} more lines){RESET}")

    # ── Step 2: Role-based access control demo ──
    header("STEP 2  Role-Based Access Control")

    print(f"  Attempting to generate a discharge summary as an {YELLOW}admin{RESET} user...")
    try:
        optimizer.generate_draft(
            ACCESS_DENIED_SCENARIO["workflow_type"],
            ACCESS_DENIED_SCENARIO["context"],
            ACCESS_DENIED_SCENARIO["clinician_id"],
            ACCESS_DENIED_SCENARIO["role"],
        )
        print(f"  {RED}ERROR: Should have been denied!{RESET}")
    except PermissionError as e:
        print(f"  {GREEN}Access correctly denied:{RESET} {e}")

    print(f"\n  {DIM}Role permissions matrix:{RESET}")
    for role, perms in optimizer.ROLE_PERMISSIONS.items():
        print(f"    {YELLOW}{role:20s}{RESET} {', '.join(perms)}")

    # ── Step 3: Clinician review workflow ──
    header("STEP 3  Clinician Review (Approve / Edit / Reject)")

    # Approve draft 1 as-is
    d1 = optimizer.approve_draft(1, "DR-CHEN-4421")
    sub_header("Draft #1 — Approved as-is")
    label("Workflow", d1["workflow_type"])
    label("Status", f"{GREEN}{d1['status']}{RESET}")
    label("Edited", str(d1["was_edited"]))

    # Approve draft 3 with edits
    d3 = optimizer.approve_draft(3, "RN-GARCIA-1192",
                                  edits="[Clinician edited the patient message to "
                                        "add personalized encouragement and correct "
                                        "the follow-up date to June 2026.]")
    sub_header("Draft #3 — Approved with edits")
    label("Workflow", d3["workflow_type"])
    label("Status", f"{GREEN}{d3['status']}{RESET}")
    label("Edited", f"{YELLOW}{d3['was_edited']}{RESET}")

    # Reject draft 2
    d2 = optimizer.reject_draft(2, "DR-PATEL-7783",
                                 reason="Missing key medication reconciliation details")
    sub_header("Draft #2 — Rejected")
    label("Workflow", d2["workflow_type"])
    label("Status", f"{RED}{d2['status']}{RESET}")
    label("Reason", d2["rejection_reason"])

    # ── Step 4: Audit trail ──
    header("STEP 4  HIPAA-Compliant Audit Trail")

    print(f"  {DIM}(No PHI stored in audit log — only action metadata){RESET}\n")
    for entry in optimizer.audit.entries:
        ts = entry["timestamp"][:19]
        print(f"  {DIM}{ts}{RESET}  {entry['action']:20s}  "
              f"{entry['clinician_id']:20s}  {entry['workflow_type']}")

    summary = optimizer.audit.summary()
    print(f"\n  Total audit events: {BOLD}{summary['total_events']}{RESET}")

    # ── Step 5: Impact metrics ──
    header("STEP 5  Impact Metrics Dashboard")

    metrics = optimizer.get_metrics()
    print()
    label("Total drafts generated", str(metrics["total_drafts"]))
    label("Approved", f"{GREEN}{metrics['approved']}{RESET}")
    label("Rejected", f"{RED}{metrics['rejected']}{RESET}")
    label("Pending review", str(metrics["pending"]))
    label("Edit rate", metrics["edit_rate"])
    label("Avg word count", str(metrics["avg_word_count"]))
    label("Est. minutes saved (this session)", str(metrics["est_minutes_saved"]))
    label("Est. hours saved / month (projected)",
          str(metrics["est_hours_saved_per_month"]))

    print(f"\n  {BOLD}Workflow breakdown:{RESET}")
    for wf, count in metrics["workflow_breakdown"].items():
        bar = GREEN + "#" * (count * 3) + RESET
        print(f"    {wf:25s} {bar} ({count})")

    # ── Summary ──
    header("SUMMARY")
    print(f"""
  This demo showed an end-to-end clinical workflow optimization pipeline:

    1. {BOLD}6 workflow types{RESET} — progress notes, discharge summaries,
       patient messages, referral letters, care plans, after-visit summaries

    2. {BOLD}Role-based access{RESET} — physicians, nurses, admin, care coordinators
       each get appropriate permissions

    3. {BOLD}Human-in-the-loop{RESET} — every AI draft requires clinician review
       (approve, edit, or reject)

    4. {BOLD}Audit trail{RESET} — HIPAA-aware logging without storing PHI

    5. {BOLD}Impact metrics{RESET} — track time saved, edit rates, adoption

  In production, replace MockAIClient with the Claude API (with BAA)
  to generate real clinical documentation drafts.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
