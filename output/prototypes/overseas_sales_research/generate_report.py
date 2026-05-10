#!/usr/bin/env python3
"""
Overseas Sales Research Report Generator
Demonstrates the 五看六定 (Five Perspectives, Six Decisions) framework
for structured B2B cross-border sales research.

Usage:
    python generate_report.py --company "Acme Corp" --industry "Industrial Automation" \
        --market "Southeast Asia" --purpose "distributor evaluation" --lang en

When used as a Claude Skill, web search fills in real data.
This standalone demo uses curated mock data to show the report structure.
"""

import argparse
import datetime
import json
import os
import re
import sys
import textwrap

# ---------------------------------------------------------------------------
# Mock data registry – one entry per demo company
# ---------------------------------------------------------------------------
MOCK_DATA = {
    "default": {
        "company": "Siemens AG",
        "website": "https://www.siemens.com",
        "industry": "Industrial Automation & Digitalization",
        "market": "Southeast Asia",
        "purpose": "Distributor Evaluation",
        "founded": 1847,
        "hq": "Munich, Germany",
        "revenue": "€77.8 billion (FY2025)",
        "employees": "~320,000 worldwide",
        "products": [
            "SIMATIC PLCs & SCADA",
            "SINUMERIK CNC systems",
            "MindSphere IoT platform",
            "Totally Integrated Automation (TIA) Portal",
            "Industrial edge computing devices",
        ],
        "key_people": [
            "Roland Busch – CEO",
            "Ralf P. Thomas – CFO",
            "Cedrik Neike – CEO Digital Industries",
        ],
        "industry_view": {
            "market_size": "$285 billion globally (2025), growing at 9.2% CAGR",
            "sea_size": "$38.4 billion in Southeast Asia (2025)",
            "growth_drivers": [
                "Industry 4.0 adoption acceleration",
                "Government smart-manufacturing subsidies (Thailand 4.0, Making Indonesia 4.0)",
                "Post-pandemic supply-chain reshoring to ASEAN",
                "Rising labor costs driving automation demand",
            ],
            "lifecycle_stage": "Growth – transitioning from early adoption to mainstream",
            "regulations": [
                "IEC 62443 cybersecurity standards increasingly mandated",
                "ASEAN Mutual Recognition Arrangements for electrical equipment",
                "Local content requirements in Indonesia (TKDN)",
            ],
        },
        "market_view": {
            "segments": [
                {"name": "Discrete Manufacturing", "share": "42%", "trend": "Strong growth"},
                {"name": "Process Industries", "share": "28%", "trend": "Stable"},
                {"name": "Infrastructure & Utilities", "share": "18%", "trend": "Moderate growth"},
                {"name": "SME Automation", "share": "12%", "trend": "Emerging, high potential"},
            ],
            "buyer_profile": "Plant managers & engineering directors at mid-to-large manufacturers (>$10M revenue)",
            "purchase_cycle": "6-18 months; involves technical evaluation, pilot, and procurement committee approval",
            "seasonality": "Budget allocation in Q1; project execution peaks in Q3-Q4",
        },
        "competitors": [
            {
                "name": "ABB Ltd",
                "share": "18%",
                "strength": "Strong robotics portfolio & local service network",
                "weakness": "Premium pricing, slower digital platform rollout",
            },
            {
                "name": "Schneider Electric",
                "share": "15%",
                "strength": "EcoStruxure platform, strong channel in Thailand/Vietnam",
                "weakness": "Less depth in discrete manufacturing",
            },
            {
                "name": "Mitsubishi Electric",
                "share": "14%",
                "strength": "Price-competitive PLCs, dominant in Japanese-invested factories",
                "weakness": "Weaker brand outside Japanese ecosystem",
            },
            {
                "name": "Rockwell Automation",
                "share": "10%",
                "strength": "Deep integration with Microsoft Azure IoT",
                "weakness": "Limited local presence outside Singapore & Philippines",
            },
        ],
        "swot": {
            "strengths": [
                "Comprehensive end-to-end portfolio from sensor to cloud",
                "Strong brand recognition and trust in German engineering",
                "Established distributor network across ASEAN",
            ],
            "weaknesses": [
                "Higher price point vs. Chinese and Japanese alternatives",
                "Complex licensing model for software platforms",
            ],
            "opportunities": [
                "ASEAN smart-factory government incentive programs",
                "Greenfield manufacturing relocating from China",
                "Growing demand for cybersecurity-certified OT solutions",
            ],
            "threats": [
                "Aggressive pricing from Huawei & local Chinese automation brands",
                "Currency volatility in emerging ASEAN markets",
                "Talent shortage for advanced automation deployment",
            ],
        },
        "decisions": {
            "objectives": [
                "Achieve $4.2M in first-year distributor sell-through revenue",
                "Onboard 3 certified system integrator partners within 6 months",
                "Win 2 lighthouse reference accounts in target verticals",
            ],
            "strategy": "Hybrid model: appoint a master distributor for volume products (PLCs, drives) "
                        "while maintaining direct engagement for enterprise IoT/MindSphere deals.",
            "market_focus": [
                "Thailand – automotive & electronics manufacturing clusters",
                "Vietnam – FDI-driven factory expansion in northern provinces",
                "Indonesia – process industries (palm oil, mining, cement)",
            ],
            "tactics": [
                "Lead with TIA Portal free trial + 2-day hands-on workshop",
                "Bundle PLC hardware with 12-month MindSphere subscription at 15% discount",
                "Co-invest in a demo center with the master distributor",
                "Target Japanese transplant factories switching from legacy Mitsubishi PLCs",
            ],
            "resources": [
                "2 field application engineers (locally hired)",
                "1 channel manager (regional, based in Singapore)",
                "Marketing budget: $180K/year (events, digital, co-op funds)",
                "Demo equipment pool: $95K one-time investment",
            ],
            "cadence": {
                "30_day": [
                    "Finalize distributor agreement & joint business plan",
                    "Ship demo equipment and set up partner portal access",
                    "Identify top-10 target accounts with distributor sales team",
                ],
                "60_day": [
                    "Launch first TIA Portal workshop series (2 cities)",
                    "Begin POC at 2 lighthouse accounts",
                    "Attend Manufacturing Expo Thailand for lead generation",
                ],
                "90_day": [
                    "Close first 2 deals; publish case studies",
                    "Conduct quarterly business review with distributor",
                    "Evaluate expansion to secondary markets (Philippines, Malaysia)",
                ],
            },
        },
        "risks": [
            {
                "risk": "Distributor underperformance",
                "impact": "High",
                "mitigation": "Quarterly reviews with 6-month performance clause; maintain backup distributor shortlist",
            },
            {
                "risk": "Currency depreciation (THB/VND/IDR)",
                "impact": "Medium",
                "mitigation": "Price in USD with quarterly FX adjustment bands (±5%)",
            },
            {
                "risk": "Regulatory delays (import licensing, TKDN)",
                "impact": "Medium",
                "mitigation": "Engage local compliance consultants; explore CKD assembly options",
            },
            {
                "risk": "Competitive price war from Chinese vendors",
                "impact": "High",
                "mitigation": "Differentiate on lifecycle cost, cybersecurity certification, and local support SLA",
            },
        ],
    }
}


def get_data(company: str) -> dict:
    """Return mock data, falling back to default if company not in registry."""
    key = company.lower().strip()
    for k, v in MOCK_DATA.items():
        if k != "default" and k in key:
            return v
    return MOCK_DATA["default"]


def fmt_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a simple Markdown table."""
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    hdr = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |"
    sep = "| " + " | ".join("-" * w for w in widths) + " |"
    body = "\n".join(
        "| " + " | ".join(r[i].ljust(widths[i]) for i in range(len(headers))) + " |"
        for r in rows
    )
    return f"{hdr}\n{sep}\n{body}"


def generate_report(data: dict, lang: str = "zh") -> str:
    """Build the full Markdown report from structured data."""
    zh = lang.startswith("zh")
    d = data
    today = datetime.date.today().isoformat()

    sections = []

    # Title
    if zh:
        sections.append(f"# 海外销售调研报告 / Overseas Sales Research Report")
    else:
        sections.append(f"# Overseas Sales Research Report")

    sections.append(f"## Target: {d['company']}")
    sections.append(f"## Date: {today}")
    sections.append(f"## Purpose: {d['purpose']}")
    sections.append("")

    # Executive Summary
    sections.append("---")
    sections.append("")
    title_exec = "### Executive Summary" if not zh else "### Executive Summary / 执行摘要"
    sections.append(title_exec)
    sections.append("")
    sections.append(
        f"{d['company']} (founded {d['founded']}, HQ: {d['hq']}) is a major player in "
        f"{d['industry']} with {d['revenue']} in annual revenue and {d['employees']}. "
        f"The {d['market']} market for industrial automation is valued at "
        f"{d['industry_view']['sea_size']}, growing at {d['industry_view']['market_size'].split('growing at')[1].strip() if 'growing at' in d['industry_view']['market_size'] else 'strong pace'}. "
        f"This report evaluates {d['company']} as a potential partner using the Five Perspectives, "
        f"Six Decisions (五看六定) framework and recommends a phased go-to-market approach."
    )
    sections.append("")

    # ── FIVE PERSPECTIVES ──────────────────────────────────────────────

    # 1. Industry View
    sec1 = "### 一、看行业 — Industry View" if zh else "### 1. Industry View"
    sections.append(sec1)
    sections.append("")
    iv = d["industry_view"]
    sections.append(f"**Global market size:** {iv['market_size']}")
    sections.append(f"**Regional market ({d['market']}):** {iv['sea_size']}")
    sections.append(f"**Lifecycle stage:** {iv['lifecycle_stage']}")
    sections.append("")
    sections.append("**Key growth drivers:**")
    for driver in iv["growth_drivers"]:
        sections.append(f"- {driver}")
    sections.append("")
    sections.append("**Regulatory landscape:**")
    for reg in iv["regulations"]:
        sections.append(f"- {reg}")
    sections.append("")

    # 2. Market View
    sec2 = "### 二、看市场 — Market View" if zh else "### 2. Market View"
    sections.append(sec2)
    sections.append("")
    mv = d["market_view"]
    rows = [[s["name"], s["share"], s["trend"]] for s in mv["segments"]]
    sections.append(fmt_table(["Segment", "Share", "Trend"], rows))
    sections.append("")
    sections.append(f"**Target buyer profile:** {mv['buyer_profile']}")
    sections.append(f"**Purchase cycle:** {mv['purchase_cycle']}")
    sections.append(f"**Seasonality:** {mv['seasonality']}")
    sections.append("")

    # 3. Competition View
    sec3 = "### 三、看竞争 — Competition View" if zh else "### 3. Competition View"
    sections.append(sec3)
    sections.append("")
    comp_rows = [
        [c["name"], c["share"], c["strength"], c["weakness"]]
        for c in d["competitors"]
    ]
    sections.append(fmt_table(["Competitor", "Market Share", "Key Strength", "Key Weakness"], comp_rows))
    sections.append("")

    # 4. Customer View
    sec4 = "### 四、看客户 — Customer View" if zh else "### 4. Customer / Target Company View"
    sections.append(sec4)
    sections.append("")
    sections.append(f"| Attribute | Detail |")
    sections.append(f"| --- | --- |")
    sections.append(f"| Company | {d['company']} |")
    sections.append(f"| Founded | {d['founded']} |")
    sections.append(f"| Headquarters | {d['hq']} |")
    sections.append(f"| Revenue | {d['revenue']} |")
    sections.append(f"| Employees | {d['employees']} |")
    sections.append(f"| Website | {d['website']} |")
    sections.append("")
    sections.append("**Key product lines:**")
    for p in d["products"]:
        sections.append(f"- {p}")
    sections.append("")
    sections.append("**Key decision-makers:**")
    for kp in d["key_people"]:
        sections.append(f"- {kp}")
    sections.append("")

    # 5. Self View
    sec5 = "### 五、看自身 — Self View (SWOT)" if zh else "### 5. Self View (SWOT Analysis)"
    sections.append(sec5)
    sections.append("")
    sw = d["swot"]
    for label, key in [("Strengths", "strengths"), ("Weaknesses", "weaknesses"),
                       ("Opportunities", "opportunities"), ("Threats", "threats")]:
        sections.append(f"**{label}:**")
        for item in sw[key]:
            sections.append(f"- {item}")
        sections.append("")

    # ── SIX DECISIONS ──────────────────────────────────────────────────

    sec6_title = "### 六、战略建议 — Six Decisions" if zh else "### 6. Strategic Recommendations — Six Decisions"
    sections.append(sec6_title)
    sections.append("")
    dec = d["decisions"]

    # 6.1 Objectives
    sections.append("#### 1. 定目标 — Objectives" if zh else "#### 6.1 Set Objectives")
    for obj in dec["objectives"]:
        sections.append(f"- {obj}")
    sections.append("")

    # 6.2 Strategy
    sections.append("#### 2. 定策略 — Strategy" if zh else "#### 6.2 Set Strategy")
    sections.append(dec["strategy"])
    sections.append("")

    # 6.3 Market Focus
    sections.append("#### 3. 定市场 — Market Focus" if zh else "#### 6.3 Set Market Focus")
    for mf in dec["market_focus"]:
        sections.append(f"- {mf}")
    sections.append("")

    # 6.4 Tactics
    sections.append("#### 4. 定打法 — Tactics" if zh else "#### 6.4 Set Tactics")
    for tac in dec["tactics"]:
        sections.append(f"- {tac}")
    sections.append("")

    # 6.5 Resources
    sections.append("#### 5. 定资源 — Resources" if zh else "#### 6.5 Set Resources")
    for res in dec["resources"]:
        sections.append(f"- {res}")
    sections.append("")

    # 6.6 Cadence
    sections.append("#### 6. 定节奏 — Cadence (30/60/90 Day Plan)" if zh else "#### 6.6 Set Cadence (30/60/90 Day Plan)")
    sections.append("")
    for phase, label in [("30_day", "30-Day"), ("60_day", "60-Day"), ("90_day", "90-Day")]:
        sections.append(f"**{label} Milestones:**")
        for item in dec["cadence"][phase]:
            sections.append(f"- [ ] {item}")
        sections.append("")

    # ── RISK ASSESSMENT ────────────────────────────────────────────────

    sections.append("### Risk Assessment")
    sections.append("")
    risk_rows = [[r["risk"], r["impact"], r["mitigation"]] for r in d["risks"]]
    sections.append(fmt_table(["Risk", "Impact", "Mitigation"], risk_rows))
    sections.append("")

    # ── APPENDIX ───────────────────────────────────────────────────────

    sections.append("### Appendix & Sources")
    sections.append("")
    sections.append(f"- Company website: {d['website']}")
    sections.append("- Statista Industrial Automation Market Reports (2025)")
    sections.append("- ASEAN Secretariat – Investment Reports")
    sections.append("- IEC 62443 Standards Documentation")
    sections.append("- Industry press releases and annual reports")
    sections.append("")
    sections.append("---")
    sections.append(f"*Report generated on {today} using the 五看六定 framework.*")
    sections.append(f"*Tool: overseas_sales_research Claude Skill*")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(
        description="Generate an overseas sales research report (五看六定 framework)"
    )
    parser.add_argument("--company", default="Siemens AG", help="Target company name")
    parser.add_argument("--industry", default="Industrial Automation", help="Industry / product category")
    parser.add_argument("--market", default="Southeast Asia", help="Target market / region")
    parser.add_argument("--purpose", default="Distributor Evaluation", help="Research purpose")
    parser.add_argument("--lang", default="zh", choices=["zh", "en"], help="Report language (zh or en)")
    parser.add_argument("--output", default=None, help="Output file path (auto-generated if omitted)")
    args = parser.parse_args()

    data = get_data(args.company)
    # Override with CLI args
    data["company"] = args.company
    data["industry"] = args.industry
    data["market"] = args.market
    data["purpose"] = args.purpose

    report = generate_report(data, lang=args.lang)

    # Determine output path
    safe_name = re.sub(r"[^a-zA-Z0-9]+", "_", args.company).strip("_").lower()
    today = datetime.date.today().isoformat()
    if args.output:
        out_path = args.output
    else:
        out_path = f"overseas_sales_research_{safe_name}_{today}.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✓ Report generated: {out_path}")
    print(f"  Company:  {args.company}")
    print(f"  Market:   {args.market}")
    print(f"  Purpose:  {args.purpose}")
    print(f"  Language: {'Chinese/Bilingual' if args.lang == 'zh' else 'English'}")
    print(f"  Sections: 5 perspectives + 6 decisions + risk assessment")
    print()

    # Print a preview of the report
    lines = report.split("\n")
    preview_lines = lines[:80]
    print("─" * 60)
    print("REPORT PREVIEW (first 80 lines):")
    print("─" * 60)
    print("\n".join(preview_lines))
    if len(lines) > 80:
        print(f"\n  ... ({len(lines) - 80} more lines — see full report in {out_path})")
    print("─" * 60)


if __name__ == "__main__":
    main()
