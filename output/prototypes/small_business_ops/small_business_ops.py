#!/usr/bin/env python3
"""
Small Business Ops — Claude Code skill demo with mock data.

Simulates 10 weekly operational workflows a small business owner would run
through Claude with MCP connectors to QuickBooks, Stripe, HubSpot, Gmail, etc.
"""

import json
import sys
from datetime import datetime, timedelta
from textwrap import dedent

# ── Mock data layer (stands in for MCP connector responses) ──────────────

MOCK_INVOICES = [
    {"id": "INV-1041", "customer": "Acme Corp", "amount": 4500.00, "due": "2026-04-15", "status": "overdue", "days_overdue": 37},
    {"id": "INV-1055", "customer": "Bright Ideas LLC", "amount": 1200.00, "due": "2026-04-28", "status": "overdue", "days_overdue": 24},
    {"id": "INV-1062", "customer": "CloudNine SaaS", "amount": 3200.00, "due": "2026-05-10", "status": "overdue", "days_overdue": 12},
    {"id": "INV-1070", "customer": "Delta Design", "amount": 800.00, "due": "2026-05-25", "status": "pending", "days_overdue": 0},
    {"id": "INV-1073", "customer": "Echo Events", "amount": 2100.00, "due": "2026-05-30", "status": "pending", "days_overdue": 0},
]

MOCK_PAYMENTS = [
    {"source": "Stripe", "date": "2026-05-18", "amount": 1450.00, "customer": "FreshFoods Co", "type": "card"},
    {"source": "Stripe", "date": "2026-05-19", "amount": 890.00, "customer": "GreenGrow", "type": "card"},
    {"source": "PayPal", "date": "2026-05-17", "amount": 2200.00, "customer": "Acme Corp", "type": "transfer"},
    {"source": "Square", "date": "2026-05-20", "amount": 340.00, "customer": "Walk-in", "type": "pos"},
    {"source": "Stripe", "date": "2026-05-21", "amount": 1100.00, "customer": "CloudNine SaaS", "type": "card"},
]

MOCK_CRM_CONTACTS = [
    {"name": "Sarah Chen", "company": "Acme Corp", "stage": "negotiation", "last_contact": "2026-05-10", "deal_value": 12000, "priority": "high"},
    {"name": "Mike Torres", "company": "Bright Ideas LLC", "stage": "proposal", "last_contact": "2026-04-22", "deal_value": 8500, "priority": "high"},
    {"name": "Lisa Park", "company": "NovaTech", "stage": "qualified", "last_contact": "2026-05-15", "deal_value": 5000, "priority": "medium"},
    {"name": "James Wilson", "company": "Delta Design", "stage": "discovery", "last_contact": "2026-03-01", "deal_value": 3000, "priority": "low"},
    {"name": "Anna Kowalski", "company": "Echo Events", "stage": "closed-won", "last_contact": "2026-05-20", "deal_value": 2100, "priority": "medium"},
    {"name": "Tom Bradley", "company": "FreshFoods Co", "stage": "discovery", "last_contact": "2026-02-14", "deal_value": 1500, "priority": "low"},
    {"name": "Rachel Nguyen", "company": "GreenGrow", "stage": "qualified", "last_contact": "2026-05-18", "deal_value": 6200, "priority": "medium"},
    {"name": "duplicate_Sarah Chen", "company": "Acme Corp", "stage": "negotiation", "last_contact": "2026-05-10", "deal_value": 12000, "priority": "high"},
]

MOCK_PAYROLL = [
    {"name": "Employee: Dana Rivera", "hours": 80, "rate": 35.00, "total": 2800.00},
    {"name": "Employee: Kevin Patel", "hours": 80, "rate": 28.00, "total": 2240.00},
    {"name": "Contractor: Jess Kim", "hours": 42, "rate": 75.00, "total": 3150.00},
    {"name": "Contractor: Alex Ruiz", "hours": 20, "rate": 60.00, "total": 1200.00},
]

MOCK_COMPLAINT = {
    "customer": "Mike Torres",
    "company": "Bright Ideas LLC",
    "order_id": "ORD-4421",
    "issue": "Received wrong configuration on the software license. Expected Enterprise tier but got Standard.",
    "order_history": [
        {"date": "2026-04-15", "item": "Enterprise License", "amount": 1200.00},
        {"date": "2026-03-10", "item": "Onboarding Package", "amount": 500.00},
    ],
    "prior_emails": 2,
}


# ── Workflow implementations ─────────────────────────────────────────────

def monday_brief():
    """Pull open invoices, payments, CRM opps into a prioritized action list."""
    today = datetime.now().strftime("%A, %B %d, %Y")
    overdue = [i for i in MOCK_INVOICES if i["status"] == "overdue"]
    total_overdue = sum(i["amount"] for i in overdue)
    total_pending = sum(i["amount"] for i in MOCK_INVOICES if i["status"] == "pending")
    week_revenue = sum(p["amount"] for p in MOCK_PAYMENTS)
    top_deals = sorted(
        [c for c in MOCK_CRM_CONTACTS if c["stage"] not in ("closed-won",)],
        key=lambda x: x["deal_value"], reverse=True
    )[:3]

    print(f"""
================================================================================
  MONDAY BRIEF — {today}
================================================================================

  CASH POSITION SNAPSHOT
  ──────────────────────
  Last 7 days revenue:       ${week_revenue:>10,.2f}
  Outstanding (overdue):     ${total_overdue:>10,.2f}  ({len(overdue)} invoices)
  Outstanding (not yet due): ${total_pending:>10,.2f}

  OVERDUE INVOICES — ACTION REQUIRED
  ───────────────────────────────────""")
    for inv in overdue:
        print(f"  {inv['id']:>10}  {inv['customer']:<22} ${inv['amount']:>9,.2f}  ({inv['days_overdue']}d overdue)")

    print(f"""
  TOP CRM OPPORTUNITIES
  ─────────────────────""")
    for d in top_deals:
        print(f"  {d['name']:<20} {d['company']:<20} ${d['deal_value']:>8,}  [{d['stage']}]")

    print(f"""
  THIS WEEK'S PRIORITIES
  ──────────────────────
  1. Chase {len(overdue)} overdue invoices (${total_overdue:,.2f} at risk)
  2. Follow up with {top_deals[0]['name']} — {top_deals[0]['stage']} stage
  3. Review contractor hours for payroll (Friday deadline)
  4. Update CRM — {len([c for c in MOCK_CRM_CONTACTS if 'duplicate' in c['name']])} duplicate(s) detected

================================================================================
""")


def invoice_chase():
    """Identify overdue invoices and draft follow-up emails."""
    overdue = [i for i in MOCK_INVOICES if i["status"] == "overdue"]
    print("""
================================================================================
  INVOICE CHASE — Overdue Follow-ups
================================================================================
""")
    for inv in overdue:
        print(f"""  ┌─ {inv['id']} — {inv['customer']} — ${inv['amount']:,.2f} ({inv['days_overdue']}d overdue)
  │
  │  DRAFT EMAIL (via Gmail):
  │  Subject: Friendly reminder — Invoice {inv['id']} past due
  │  Body: Hi, I hope you're well. I wanted to follow up on invoice
  │        {inv['id']} for ${inv['amount']:,.2f}, which was due on {inv['due']}.
  │        Could you let me know when we can expect payment?
  │
  │  CRM LOG: Contact attempt recorded for {inv['customer']}
  └──────────────────────────────────────────────────────
""")
    print(f"  Summary: {len(overdue)} emails drafted, {len(overdue)} CRM entries logged.")
    print(f"  Total outstanding: ${sum(i['amount'] for i in overdue):,.2f}")
    print("================================================================================\n")


def close_month():
    """Reconcile transactions and generate P&L snapshot."""
    stripe_total = sum(p["amount"] for p in MOCK_PAYMENTS if p["source"] == "Stripe")
    paypal_total = sum(p["amount"] for p in MOCK_PAYMENTS if p["source"] == "PayPal")
    square_total = sum(p["amount"] for p in MOCK_PAYMENTS if p["source"] == "Square")
    gross = stripe_total + paypal_total + square_total
    payroll_total = sum(p["total"] for p in MOCK_PAYROLL)
    ops_expenses = 1850.00  # rent, tools, subscriptions
    net = gross - payroll_total - ops_expenses

    print(f"""
================================================================================
  MONTH-END CLOSE — May 2026
================================================================================

  REVENUE RECONCILIATION
  ──────────────────────
  Stripe:      ${stripe_total:>10,.2f}  ({len([p for p in MOCK_PAYMENTS if p['source'] == 'Stripe'])} txns)
  PayPal:      ${paypal_total:>10,.2f}  ({len([p for p in MOCK_PAYMENTS if p['source'] == 'PayPal'])} txns)
  Square:      ${square_total:>10,.2f}  ({len([p for p in MOCK_PAYMENTS if p['source'] == 'Square'])} txns)
                ──────────
  Gross:       ${gross:>10,.2f}

  DISCREPANCIES
  ─────────────
  [!] PayPal txn $2,200.00 (Acme Corp) — no matching invoice found. Verify.

  P&L SNAPSHOT
  ────────────
  Revenue:          ${gross:>10,.2f}
  Payroll:         -${payroll_total:>10,.2f}
  Operating costs: -${ops_expenses:>10,.2f}
                    ──────────
  Net income:      ${net:>10,.2f}

  Status: {"PROFITABLE" if net > 0 else "LOSS"} — review flagged discrepancies before finalizing.
================================================================================
""")


def plan_payroll():
    """Calculate payroll totals and prepare payment run."""
    total = sum(p["total"] for p in MOCK_PAYROLL)
    employees = [p for p in MOCK_PAYROLL if "Employee" in p["name"]]
    contractors = [p for p in MOCK_PAYROLL if "Contractor" in p["name"]]

    print(f"""
================================================================================
  PAYROLL PLANNING — Pay Period: May 11-24, 2026
================================================================================

  EMPLOYEES (W-2)
  ───────────────""")
    for p in employees:
        print(f"  {p['name']:<30} {p['hours']:>3}h x ${p['rate']:<6.2f} = ${p['total']:>9,.2f}")
    print(f"  {'Subtotal':<30} {'':>15}   ${sum(e['total'] for e in employees):>9,.2f}")

    print(f"""
  CONTRACTORS (1099)
  ──────────────────""")
    for p in contractors:
        print(f"  {p['name']:<30} {p['hours']:>3}h x ${p['rate']:<6.2f} = ${p['total']:>9,.2f}")
    print(f"  {'Subtotal':<30} {'':>15}   ${sum(c['total'] for c in contractors):>9,.2f}")

    print(f"""
                                                      ──────────
  TOTAL PAYROLL:                                      ${total:>9,.2f}

  Payment run ready for approval.
================================================================================
""")


def call_list():
    """Generate prioritized call sheet from CRM."""
    contacts = sorted(
        [c for c in MOCK_CRM_CONTACTS if "duplicate" not in c["name"] and c["stage"] != "closed-won"],
        key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]]
    )
    print("""
================================================================================
  CALL LIST — Prioritized Follow-ups
================================================================================

  #   Priority  Contact              Company              Deal Value  Last Contact
  ─── ──────── ──────────────────── ──────────────────── ────────── ────────────""")
    for i, c in enumerate(contacts, 1):
        days_ago = (datetime.now() - datetime.strptime(c["last_contact"], "%Y-%m-%d")).days
        flag = " **STALE**" if days_ago > 30 else ""
        print(f"  {i:<3} {c['priority']:<8} {c['name']:<20} {c['company']:<20} ${c['deal_value']:>8,}  {c['last_contact']}{flag}")
    print(f"""
  Total pipeline value: ${sum(c['deal_value'] for c in contacts):>,}
  Stale leads (>30d): {len([c for c in contacts if (datetime.now() - datetime.strptime(c['last_contact'], '%Y-%m-%d')).days > 30])}
================================================================================
""")


def handle_complaint():
    """Draft response to customer complaint using order history."""
    c = MOCK_COMPLAINT
    print(f"""
================================================================================
  COMPLAINT HANDLER — {c['customer']} ({c['company']})
================================================================================

  ORDER HISTORY
  ─────────────""")
    for o in c["order_history"]:
        print(f"  {o['date']}  {o['item']:<25} ${o['amount']:>9,.2f}")

    print(f"""
  ISSUE: {c['issue']}
  Prior communications: {c['prior_emails']} emails

  DRAFT RESPONSE (via Gmail):
  ───────────────────────────
  Subject: Re: Order {c['order_id']} — License tier correction

  Hi {c['customer'].split()[0]},

  Thank you for reaching out, and I sincerely apologize for the mix-up with
  your license tier. I can see from our records that you purchased the
  Enterprise License on {c['order_history'][0]['date']}.

  I've escalated this to our provisioning team and your account should be
  upgraded to Enterprise within 24 hours. As a gesture of goodwill, I'd like
  to extend your subscription by one month at no charge.

  Please let me know if there's anything else I can help with.

  Best regards

  CRM UPDATE: Complaint logged, deal stage flagged for review.
================================================================================
""")


def run_campaign():
    """Plan a marketing campaign using CRM segments."""
    qualified = [c for c in MOCK_CRM_CONTACTS if c["stage"] in ("qualified", "discovery") and "duplicate" not in c["name"]]
    print(f"""
================================================================================
  CAMPAIGN PLANNER — Q2 Upsell Campaign
================================================================================

  TARGET SEGMENT: Qualified + Discovery leads ({len(qualified)} contacts)
  ──────────────""")
    for c in qualified:
        print(f"  {c['name']:<20} {c['company']:<20} [{c['stage']}]  ${c['deal_value']:>,}")

    print(f"""
  CAMPAIGN DETAILS
  ────────────────
  Name:     "Unlock Enterprise Features — Limited Time"
  Channel:  Email (Gmail) + CRM tracking
  Duration: 2 weeks (May 25 - Jun 8, 2026)

  EMAIL TEMPLATE DRAFT:
  Subject: Exclusive offer for {qualified[0]['company'] if qualified else 'you'} — upgrade & save 20%

  Hi {{first_name}},

  I noticed you've been exploring our platform and wanted to share an
  exclusive opportunity. For the next two weeks, you can upgrade to our
  Enterprise tier at 20% off.

  This includes [feature A], [feature B], and priority support.

  Want to hop on a quick call this week? I'd love to walk you through it.

  Estimated pipeline impact: ${sum(c['deal_value'] for c in qualified):>,}
================================================================================
""")


def friday_brief():
    """Summarize the week's performance and set up next week."""
    week_revenue = sum(p["amount"] for p in MOCK_PAYMENTS)
    new_customers = 2
    resolved_issues = 3
    won_deals = [c for c in MOCK_CRM_CONTACTS if c["stage"] == "closed-won"]

    print(f"""
================================================================================
  FRIDAY BRIEF — Week of May 18, 2026
================================================================================

  WEEK IN NUMBERS
  ───────────────
  Revenue collected:    ${week_revenue:>10,.2f}
  New customers:        {new_customers:>10}
  Deals closed:         {len(won_deals):>10}  (${sum(d['deal_value'] for d in won_deals):>,})
  Issues resolved:      {resolved_issues:>10}

  HIGHLIGHTS
  ──────────
  + Closed Echo Events deal ($2,100)
  + Received Acme Corp payment via PayPal ($2,200)
  + Resolved licensing complaint for Bright Ideas LLC

  CARRIED OVER
  ────────────
  - INV-1041 (Acme Corp, $4,500) still overdue — 37 days
  - James Wilson (Delta Design) — stale lead, needs decision: pursue or archive

  NEXT WEEK PRIORITIES
  ────────────────────
  1. Final push on Acme Corp invoice
  2. Follow up with Mike Torres — proposal stage
  3. Launch Q2 upsell campaign
  4. Prepare monthly close (May 31)
================================================================================
""")


def quarterly_review():
    """Aggregate 3 months of data into board-ready summary."""
    print("""
================================================================================
  QUARTERLY REVIEW — Q1 2026 (Jan-Mar)
================================================================================

  FINANCIAL SUMMARY
  ─────────────────
  Revenue:          $87,450.00   (+12% vs Q4 2025)
  COGS:            -$31,200.00
  Gross margin:     $56,250.00   (64.3%)
  Operating costs: -$22,800.00
  Net income:       $33,450.00   (38.3% margin)

  REVENUE BY CHANNEL
  ──────────────────
  Stripe:    $52,470  (60%)
  PayPal:    $21,863  (25%)
  Square:    $13,117  (15%)

  CRM GROWTH
  ──────────
  New leads:           47
  Converted to deals:  18  (38% conversion)
  Deals closed-won:    12  ($68,400 total)
  Avg deal size:       $5,700

  CAMPAIGN PERFORMANCE
  ────────────────────
  Emails sent:    1,240
  Open rate:      34.2%
  Click rate:     8.7%
  Deals sourced:  4 ($22,800)

  KEY METRICS vs TARGETS
  ──────────────────────
  Revenue:     $87,450 / $80,000 target  [EXCEEDED +9.3%]
  New clients:      12 / 10 target       [EXCEEDED +20%]
  Churn:           2.1% / <5% target     [ON TRACK]
  NPS:              72 / 60 target       [EXCEEDED]

  RECOMMENDATIONS
  ───────────────
  1. Increase ad spend — CAC ($420) well below LTV ($4,200)
  2. Hire part-time support — ticket volume up 28%
  3. Renegotiate Stripe rates at current volume
================================================================================
""")


def crm_maintenance():
    """Deduplicate contacts, update stages, archive dead leads."""
    dupes = [c for c in MOCK_CRM_CONTACTS if "duplicate" in c["name"]]
    stale = [c for c in MOCK_CRM_CONTACTS
             if "duplicate" not in c["name"]
             and (datetime.now() - datetime.strptime(c["last_contact"], "%Y-%m-%d")).days > 60]
    active = [c for c in MOCK_CRM_CONTACTS
              if "duplicate" not in c["name"]
              and c not in stale]

    print(f"""
================================================================================
  CRM MAINTENANCE REPORT
================================================================================

  DUPLICATES FOUND: {len(dupes)}
  ─────────────────""")
    for d in dupes:
        original = d["name"].replace("duplicate_", "")
        print(f"  MERGE: '{d['name']}' → '{original}' (same company: {d['company']})")

    print(f"""
  STALE LEADS (>60 days no contact): {len(stale)}
  ──────────────────────────────────""")
    for s in stale:
        days = (datetime.now() - datetime.strptime(s["last_contact"], "%Y-%m-%d")).days
        print(f"  ARCHIVE: {s['name']:<20} {s['company']:<20} Last contact: {days}d ago  (${s['deal_value']:>,})")

    print(f"""
  ACTIVE PIPELINE: {len(active)} contacts
  ─────────────────""")
    for a in active:
        print(f"  {a['name']:<20} {a['company']:<20} [{a['stage']}]  ${a['deal_value']:>,}")

    print(f"""
  ACTIONS TAKEN
  ─────────────
  - Merged {len(dupes)} duplicate(s)
  - Archived {len(stale)} stale lead(s)
  - Active pipeline: {len(active)} contacts, ${sum(a['deal_value'] for a in active):>,} total value
================================================================================
""")


# ── CLI ──────────────────────────────────────────────────────────────────

WORKFLOWS = {
    "monday":     ("Monday Brief",      monday_brief),
    "chase":      ("Invoice Chase",     invoice_chase),
    "close":      ("Close Month",       close_month),
    "payroll":    ("Plan Payroll",      plan_payroll),
    "calls":      ("Call List",         call_list),
    "complaint":  ("Handle Complaint",  handle_complaint),
    "campaign":   ("Run Campaign",      run_campaign),
    "friday":     ("Friday Brief",      friday_brief),
    "quarterly":  ("Quarterly Review",  quarterly_review),
    "crm":        ("CRM Maintenance",   crm_maintenance),
}


def main():
    if len(sys.argv) > 1:
        key = sys.argv[1].lower()
        if key == "all":
            for name, (label, fn) in WORKFLOWS.items():
                fn()
            return
        if key in WORKFLOWS:
            WORKFLOWS[key][1]()
            return
        print(f"Unknown workflow: {key}")
        print(f"Available: {', '.join(WORKFLOWS.keys())}, all")
        sys.exit(1)

    # Default: show menu and run a few key workflows
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              SMALL BUSINESS OPS — Claude Code Skill Demo                   ║
║                                                                            ║
║  10 pre-built workflows for weekly business operations                     ║
║  Powered by Claude MCP connectors: QuickBooks, Stripe, HubSpot, Gmail     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Available workflows:
""")
    for key, (label, _) in WORKFLOWS.items():
        print(f"  {key:<12} — {label}")

    print(f"\nUsage: python3 {sys.argv[0]} <workflow>   (or 'all' to run everything)")
    print("\n── Running demo: Monday Brief + Invoice Chase + CRM Maintenance ──")

    monday_brief()
    invoice_chase()
    crm_maintenance()


if __name__ == "__main__":
    main()
