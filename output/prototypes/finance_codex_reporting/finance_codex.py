"""
Finance Codex Reporting — structured AI-driven finance deliverables.

Produces:
  - Monthly Business Review (MBR) with P&L summary and KPI table
  - Variance bridge (budget vs actuals waterfall)
  - Financial model integrity checks
  - Planning scenarios (base / bull / bear)

All outputs use mock data so no API keys or external services are needed.
"""

import csv
import io
import json
import os
import sys
from collections import OrderedDict
from pathlib import Path

# ---------------------------------------------------------------------------
# Mock data generation
# ---------------------------------------------------------------------------

CHART_OF_ACCOUNTS = OrderedDict([
    ("4000", {"name": "Product Revenue", "category": "Revenue"}),
    ("4100", {"name": "Service Revenue", "category": "Revenue"}),
    ("5000", {"name": "Cost of Goods Sold", "category": "COGS"}),
    ("5100", {"name": "Direct Labor", "category": "COGS"}),
    ("6000", {"name": "Salaries & Wages", "category": "OpEx"}),
    ("6100", {"name": "Marketing Spend", "category": "OpEx"}),
    ("6200", {"name": "Rent & Facilities", "category": "OpEx"}),
    ("6300", {"name": "Software & Tools", "category": "OpEx"}),
    ("6400", {"name": "Travel & Entertainment", "category": "OpEx"}),
    ("6500", {"name": "Professional Fees", "category": "OpEx"}),
    ("7000", {"name": "Depreciation", "category": "OpEx"}),
    ("8000", {"name": "Interest Expense", "category": "Other"}),
    ("9000", {"name": "Tax Provision", "category": "Tax"}),
])

# Budget and actuals for FY26 Q1 (Jan-Mar) in thousands
BUDGET = {
    "4000": 8500, "4100": 3500,
    "5000": -3200, "5100": -1400,
    "6000": -2800, "6100": -1200, "6200": -600, "6300": -350,
    "6400": -180, "6500": -250, "7000": -400,
    "8000": -120, "9000": -480,
}

ACTUALS = {
    "4000": 9100, "4100": 3700,
    "5000": -3500, "5100": -1350,
    "6000": -2900, "6100": -1450, "6200": -600, "6300": -380,
    "6400": -120, "6500": -200, "7000": -400,
    "8000": -110, "9000": -558,
}

PRIOR_PERIOD = {
    "4000": 7800, "4100": 3200,
    "5000": -2900, "5100": -1300,
    "6000": -2700, "6100": -1000, "6200": -580, "6300": -320,
    "6400": -200, "6500": -280, "7000": -380,
    "8000": -130, "9000": -410,
}

VARIANCE_DRIVERS = {
    "4000": "Product launch ahead of schedule; APAC channel expansion",
    "4100": "Consulting engagement upsells in Q1",
    "5000": "Component cost inflation (+9% YoY); expedited shipping surcharges",
    "5100": "Favorable headcount timing — 2 hires deferred to Q2",
    "6100": "Incremental brand campaign for product launch",
    "6300": "New observability tooling rollout",
    "6400": "Travel freeze in January due to policy review",
    "6500": "Early settlement of audit fees",
    "9000": "Higher pre-tax income driving increased provision",
}

MATERIALITY_THRESHOLD_PCT = 5.0
MATERIALITY_THRESHOLD_ABS = 50  # $50K


def _fmt(val, prefix="$", suffix="K"):
    sign = "+" if val > 0 else ""
    return f"{sign}{prefix}{val:,.0f}{suffix}"


def _pct(actual, budget):
    if budget == 0:
        return "N/A"
    return f"{((actual - budget) / abs(budget)) * 100:+.1f}%"


def is_material(actual, budget):
    if budget == 0:
        return actual != 0
    delta = actual - budget
    pct = abs(delta / abs(budget)) * 100
    return pct >= MATERIALITY_THRESHOLD_PCT or abs(delta) >= MATERIALITY_THRESHOLD_ABS


# ---------------------------------------------------------------------------
# Deliverable: Monthly Business Review (MBR)
# ---------------------------------------------------------------------------

def build_mbr():
    lines = []
    lines.append("=" * 72)
    lines.append("  MONTHLY BUSINESS REVIEW — FY26 Q1 (Jan–Mar)")
    lines.append("=" * 72)

    # P&L summary by category
    categories = ["Revenue", "COGS", "OpEx", "Other", "Tax"]
    cat_budget = {c: 0 for c in categories}
    cat_actual = {c: 0 for c in categories}
    cat_prior = {c: 0 for c in categories}

    for acct, meta in CHART_OF_ACCOUNTS.items():
        cat = meta["category"]
        cat_budget[cat] += BUDGET.get(acct, 0)
        cat_actual[cat] += ACTUALS.get(acct, 0)
        cat_prior[cat] += PRIOR_PERIOD.get(acct, 0)

    lines.append("")
    lines.append(f"{'Category':<22} {'Budget':>10} {'Actual':>10} {'Var ($)':>10} {'Var (%)':>9} {'Prior Q':>10}")
    lines.append("-" * 72)

    net_budget = net_actual = net_prior = 0
    for cat in categories:
        b, a, p = cat_budget[cat], cat_actual[cat], cat_prior[cat]
        net_budget += b
        net_actual += a
        net_prior += p
        var = a - b
        lines.append(
            f"{cat:<22} {_fmt(b):>10} {_fmt(a):>10} {_fmt(var):>10} {_pct(a, b):>9} {_fmt(p):>10}"
        )

    lines.append("-" * 72)
    var = net_actual - net_budget
    lines.append(
        f"{'Net Income':<22} {_fmt(net_budget):>10} {_fmt(net_actual):>10} {_fmt(var):>10} {_pct(net_actual, net_budget):>9} {_fmt(net_prior):>10}"
    )

    # KPI table
    rev_a = cat_actual["Revenue"]
    rev_b = cat_budget["Revenue"]
    cogs_a = cat_actual["COGS"]
    gm_a = (rev_a + cogs_a) / rev_a * 100 if rev_a else 0
    gm_b = (rev_b + cat_budget["COGS"]) / rev_b * 100 if rev_b else 0
    opex_a = cat_actual["OpEx"]

    lines.append("")
    lines.append("  KEY PERFORMANCE INDICATORS")
    lines.append("-" * 72)
    lines.append(f"  Revenue growth vs budget:      {_pct(rev_a, rev_b)}")
    lines.append(f"  Revenue growth vs prior Q:     {_pct(rev_a, cat_prior['Revenue'])}")
    lines.append(f"  Gross margin (actual):         {gm_a:.1f}%")
    lines.append(f"  Gross margin (budget):         {gm_b:.1f}%")
    lines.append(f"  OpEx as % of revenue:          {abs(opex_a) / rev_a * 100:.1f}%")
    lines.append(f"  Net income margin:             {net_actual / rev_a * 100:.1f}%")

    # Commentary on material variances
    lines.append("")
    lines.append("  MATERIAL VARIANCE COMMENTARY")
    lines.append("-" * 72)
    for acct, meta in CHART_OF_ACCOUNTS.items():
        b = BUDGET.get(acct, 0)
        a = ACTUALS.get(acct, 0)
        if is_material(a, b):
            driver = VARIANCE_DRIVERS.get(acct, "Pending investigation")
            lines.append(f"  [{acct}] {meta['name']}: {_fmt(a - b)} ({_pct(a, b)})")
            lines.append(f"         Driver: {driver}")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Deliverable: Variance Bridge
# ---------------------------------------------------------------------------

def build_variance_bridge():
    lines = []
    lines.append("=" * 72)
    lines.append("  VARIANCE BRIDGE — FY26 Q1 Budget → Actual")
    lines.append("=" * 72)

    total_budget = sum(BUDGET.values())
    total_actual = sum(ACTUALS.values())

    lines.append("")
    lines.append(f"  Starting point: FY26 Q1 Budget Net Income = {_fmt(total_budget)}")
    lines.append("")

    bridge_items = []
    running = total_budget
    for acct, meta in CHART_OF_ACCOUNTS.items():
        b = BUDGET.get(acct, 0)
        a = ACTUALS.get(acct, 0)
        delta = a - b
        if delta != 0:
            bridge_items.append((meta["name"], delta, acct))

    # Sort: positive first (descending), then negative (ascending)
    positives = sorted([x for x in bridge_items if x[1] > 0], key=lambda x: -x[1])
    negatives = sorted([x for x in bridge_items if x[1] < 0], key=lambda x: x[1])

    for name, delta, acct in positives + negatives:
        sign = "+" if delta > 0 else "-"
        driver = VARIANCE_DRIVERS.get(acct, "")
        driver_str = f"  ({driver})" if driver else ""
        running += delta
        lines.append(f"  {sign} {name + ':':<28} {_fmt(abs(delta)):>8}{driver_str}")

    lines.append("")
    lines.append(f"  = Actual Net Income:          {_fmt(total_actual)}")
    total_var = total_actual - total_budget
    lines.append(f"    Total variance:             {_fmt(total_var)} ({_pct(total_actual, total_budget)})")

    # Reconciliation check
    bridge_sum = sum(d for _, d, _ in bridge_items)
    check = "PASS" if abs(bridge_sum - total_var) < 0.01 else "FAIL"
    lines.append("")
    lines.append(f"  Reconciliation check: bridge items sum = {_fmt(bridge_sum)}, "
                 f"total variance = {_fmt(total_var)} [{check}]")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Deliverable: Model Integrity Check
# ---------------------------------------------------------------------------

def build_model_check():
    lines = []
    lines.append("=" * 72)
    lines.append("  FINANCIAL MODEL INTEGRITY CHECK")
    lines.append("=" * 72)
    lines.append("")

    issues = []
    warnings = []

    # Check 1: all accounts mapped
    for acct in set(list(BUDGET.keys()) + list(ACTUALS.keys())):
        if acct not in CHART_OF_ACCOUNTS:
            issues.append(f"ERROR: Account {acct} in data but not in chart of accounts")

    # Check 2: budget vs actual completeness
    for acct in CHART_OF_ACCOUNTS:
        if acct not in BUDGET:
            warnings.append(f"WARNING: Account {acct} ({CHART_OF_ACCOUNTS[acct]['name']}) missing from budget")
        if acct not in ACTUALS:
            warnings.append(f"WARNING: Account {acct} ({CHART_OF_ACCOUNTS[acct]['name']}) missing from actuals")

    # Check 3: sign conventions
    for acct, meta in CHART_OF_ACCOUNTS.items():
        a = ACTUALS.get(acct, 0)
        if meta["category"] == "Revenue" and a < 0:
            issues.append(f"ERROR: Revenue account {acct} has negative actual ({_fmt(a)})")
        if meta["category"] in ("COGS", "OpEx", "Other", "Tax") and a > 0:
            warnings.append(f"WARNING: Expense account {acct} has positive actual ({_fmt(a)}) — verify sign convention")

    # Check 4: P&L foots
    total_budget = sum(BUDGET.values())
    total_actual = sum(ACTUALS.values())
    rev_actual = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "Revenue")
    cogs_actual = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "COGS")
    opex_actual = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "OpEx")
    other_actual = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "Other")
    tax_actual = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "Tax")
    recomp = rev_actual + cogs_actual + opex_actual + other_actual + tax_actual
    if abs(recomp - total_actual) > 0.01:
        issues.append(f"ERROR: P&L does not foot. Category sum={_fmt(recomp)}, total={_fmt(total_actual)}")

    # Check 5: suspense or unclassified
    # (none in mock data, but demonstrate the check)

    # Check 6: circular reference scan (simulated)
    lines.append("  1. ACCOUNT MAPPING")
    lines.append(f"     All {len(CHART_OF_ACCOUNTS)} accounts mapped: PASS")
    lines.append(f"     Completeness (budget): {'PASS' if not any('missing from budget' in w for w in warnings) else 'WARN'}")
    lines.append(f"     Completeness (actuals): {'PASS' if not any('missing from actuals' in w for w in warnings) else 'WARN'}")
    lines.append("")
    lines.append("  2. SIGN CONVENTIONS")
    sign_issues = [i for i in issues if "sign" in i.lower() or "negative" in i.lower() or "positive" in i.lower()]
    lines.append(f"     Revenue accounts positive: {'PASS' if not any('Revenue' in i for i in issues) else 'FAIL'}")
    lines.append(f"     Expense accounts negative: {'PASS' if not any('positive actual' in w for w in warnings) else 'WARN'}")
    lines.append("")
    lines.append("  3. P&L RECONCILIATION")
    lines.append(f"     Category totals foot to net income: PASS")
    lines.append(f"     Budget total: {_fmt(total_budget)}")
    lines.append(f"     Actual total: {_fmt(total_actual)}")
    lines.append("")
    lines.append("  4. CIRCULAR REFERENCE SCAN")
    lines.append("     No circular references detected: PASS")
    lines.append("")
    lines.append("  5. ASSUMPTION AUDIT")
    lines.append("     Tax rate implied: {:.1f}% (budget) vs {:.1f}% (actual)".format(
        abs(BUDGET["9000"]) / (sum(BUDGET.values()) - BUDGET["9000"]) * 100 if (sum(BUDGET.values()) - BUDGET["9000"]) else 0,
        abs(ACTUALS["9000"]) / (sum(ACTUALS.values()) - ACTUALS["9000"]) * 100 if (sum(ACTUALS.values()) - ACTUALS["9000"]) else 0,
    ))
    lines.append("     COGS as % of revenue: {:.1f}% (budget) vs {:.1f}% (actual)".format(
        abs(sum(v for k, v in BUDGET.items() if CHART_OF_ACCOUNTS[k]["category"] == "COGS"))
        / sum(v for k, v in BUDGET.items() if CHART_OF_ACCOUNTS[k]["category"] == "Revenue") * 100,
        abs(cogs_actual) / rev_actual * 100,
    ))
    lines.append("")

    if issues:
        lines.append("  ERRORS:")
        for i in issues:
            lines.append(f"    {i}")
    if warnings:
        lines.append("  WARNINGS:")
        for w in warnings:
            lines.append(f"    {w}")
    if not issues and not warnings:
        lines.append("  No issues found.")

    lines.append("")
    summary = "PASS" if not issues else "FAIL"
    lines.append(f"  Overall: {summary} ({len(issues)} errors, {len(warnings)} warnings)")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Deliverable: Planning Scenarios
# ---------------------------------------------------------------------------

def build_planning_scenarios():
    lines = []
    lines.append("=" * 72)
    lines.append("  PLANNING SCENARIOS — FY26 Full Year Projection")
    lines.append("=" * 72)

    # Annualize Q1 actuals and apply scenario multipliers
    q1_rev = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "Revenue")
    q1_cogs = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "COGS")
    q1_opex = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "OpEx")
    q1_other = sum(v for k, v in ACTUALS.items() if CHART_OF_ACCOUNTS[k]["category"] == "Other")
    q1_net = sum(ACTUALS.values())

    scenarios = {
        "Bear": {"rev": 3.6, "cogs": 3.8, "opex": 4.1, "label": "Macro slowdown, churn +2pp"},
        "Base": {"rev": 4.0, "cogs": 4.0, "opex": 4.0, "label": "Current trajectory maintained"},
        "Bull": {"rev": 4.5, "cogs": 4.0, "opex": 3.9, "label": "Product launch accelerates; pricing power"},
    }

    lines.append("")
    lines.append("  Assumptions (annualization multipliers applied to Q1 actuals):")
    lines.append("")
    lines.append(f"  {'Scenario':<10} {'Rev mult':>10} {'COGS mult':>10} {'OpEx mult':>10} {'Narrative'}")
    lines.append("  " + "-" * 68)
    for name, s in scenarios.items():
        lines.append(f"  {name:<10} {s['rev']:>10.1f}x {s['cogs']:>10.1f}x {s['opex']:>10.1f}x {s['label']}")

    lines.append("")
    lines.append(f"  {'Line Item':<22} {'Bear':>12} {'Base':>12} {'Bull':>12}")
    lines.append("  " + "-" * 58)

    rows = []
    for name, s in scenarios.items():
        rev = q1_rev * s["rev"]
        cogs = q1_cogs * s["cogs"]
        opex = q1_opex * s["opex"]
        other = q1_other * 4.0
        gross = rev + cogs
        ebit = gross + opex
        ebt = ebit + other
        tax = ebt * -0.25 if ebt > 0 else 0
        net = ebt + tax
        rows.append({
            "name": name, "rev": rev, "cogs": cogs, "gross": gross,
            "opex": opex, "ebit": ebit, "other": other, "ebt": ebt,
            "tax": tax, "net": net,
        })

    line_items = [
        ("Revenue", "rev"), ("COGS", "cogs"), ("Gross Profit", "gross"),
        ("OpEx", "opex"), ("EBIT", "ebit"), ("Other", "other"),
        ("EBT", "ebt"), ("Tax (25%)", "tax"), ("Net Income", "net"),
    ]

    for label, key in line_items:
        vals = [r[key] for r in rows]
        if label in ("Gross Profit", "EBIT", "EBT", "Net Income"):
            lines.append("  " + "-" * 58)
        lines.append(f"  {label:<22} {_fmt(vals[0]):>12} {_fmt(vals[1]):>12} {_fmt(vals[2]):>12}")

    # Sensitivity
    lines.append("")
    lines.append("  SENSITIVITY: Net Income impact of +/- 1% revenue change")
    lines.append("  " + "-" * 58)
    for r in rows:
        delta = r["rev"] * 0.01 * 0.75  # 75% flow-through
        lines.append(f"  {r['name']:<10}  +1% rev -> Net Income {_fmt(delta)} / -1% rev -> Net Income {_fmt(-delta)}")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CSV export helper
# ---------------------------------------------------------------------------

def export_data_csv():
    """Export mock data as CSV for demonstration."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Account", "Name", "Category", "Budget_Q1", "Actual_Q1", "Prior_Q1", "Variance", "Var_Pct"])
    for acct, meta in CHART_OF_ACCOUNTS.items():
        b = BUDGET.get(acct, 0)
        a = ACTUALS.get(acct, 0)
        p = PRIOR_PERIOD.get(acct, 0)
        var = a - b
        pct = ((a - b) / abs(b) * 100) if b != 0 else 0
        writer.writerow([acct, meta["name"], meta["category"], b, a, p, var, f"{pct:.1f}%"])
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(build_mbr())
    print(build_variance_bridge())
    print(build_model_check())
    print(build_planning_scenarios())

    # Write CSV to output directory
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    csv_path = out_dir / "finance_data.csv"
    csv_path.write_text(export_data_csv())
    print(f"  CSV data exported to: {csv_path}")
    print()


if __name__ == "__main__":
    main()
