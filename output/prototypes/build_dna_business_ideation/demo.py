#!/usr/bin/env python3
"""
Build DNA — Business Ideation Demo

Demonstrates the full skill workflow using a mock founder profile:
  Phase 1: Adaptive Intake (Founder DNA Extraction)
  Phase 2: Personalized Idea Generation
  Phase 3: Deep Dive on selected idea (Market, GTM, MVP, 72-hour plan)
"""

import json
import textwrap
from dataclasses import dataclass, field, asdict
from typing import List

# ── Mock Founder Profile ────────────────────────────────────────────────────

MOCK_FOUNDER = {
    "skills": [
        "Full-stack web development (Python/React)",
        "Data analysis & SQL",
        "Technical writing",
        "API integration",
    ],
    "experience": [
        "5 years at a B2B SaaS company (developer tools)",
        "Built internal dashboards used by 200+ engineers",
        "Led migration from monolith to microservices",
    ],
    "unfair_advantages": [
        "Deep network in DevOps/platform-engineering community",
        "Access to 10k-subscriber developer newsletter",
        "Fluent in English and Spanish (LATAM market access)",
    ],
    "resources": {
        "hours_per_week": 15,
        "starting_budget_usd": 500,
        "co_founders": False,
    },
    "preferences": {
        "business_types": ["SaaS", "creator", "services"],
        "revenue_goal_6mo_usd": 3000,
    },
}


# ── Data Models ─────────────────────────────────────────────────────────────

@dataclass
class BusinessIdea:
    name: str
    one_liner: str
    why_you: str
    business_model: str
    target_customer: str
    differentiation: str
    difficulty: dict  # technical, marketing, operational (1-5)


@dataclass
class DeepDive:
    idea_name: str
    market_analysis: dict
    gtm_plan: dict
    mvp_roadmap: dict
    action_plan_72h: list


# ── Phase 1: Intake ─────────────────────────────────────────────────────────

def phase1_intake(profile: dict) -> None:
    print("=" * 70)
    print("PHASE 1 — FOUNDER DNA EXTRACTION")
    print("=" * 70)
    print()
    for section, data in profile.items():
        label = section.replace("_", " ").title()
        print(f"  {label}:")
        if isinstance(data, list):
            for item in data:
                print(f"    - {item}")
        elif isinstance(data, dict):
            for k, v in data.items():
                print(f"    {k.replace('_', ' ').title()}: {v}")
        print()

    print("  Follow-up insights:")
    print("    * Strong signal: developer-tools domain + owned audience (newsletter)")
    print("    * LATAM fluency opens cross-border arbitrage channels")
    print("    * Budget is lean — ideas must be bootstrappable under $500")
    print()


# ── Phase 2: Idea Generation ────────────────────────────────────────────────

def phase2_ideation(profile: dict) -> List[BusinessIdea]:
    ideas = [
        BusinessIdea(
            name="DevDash Templates",
            one_liner="Pre-built, customizable internal-tool dashboards sold to engineering teams.",
            why_you="You built dashboards used by 200+ engineers — you know exactly what teams need and skip.",
            business_model="One-time purchase ($49-149) + premium templates subscription ($19/mo)",
            target_customer="Engineering managers at mid-size SaaS companies tired of building admin UIs from scratch.",
            differentiation="Battle-tested layouts from real production use, not generic UI kits.",
            difficulty={"technical": 2, "marketing": 3, "operational": 1},
        ),
        BusinessIdea(
            name="MicroMove Advisor",
            one_liner="A paid newsletter + async consulting package helping teams migrate monoliths to microservices.",
            why_you="You led a full migration — your playbook is the product.",
            business_model="Newsletter sponsorship ($500-2k/issue) + paid consulting calls ($250/hr)",
            target_customer="CTOs and staff engineers at companies with 50-500 devs hitting scaling walls.",
            differentiation="First-hand migration war stories, not theory. Spanish-language edition opens LATAM.",
            difficulty={"technical": 1, "marketing": 2, "operational": 2},
        ),
        BusinessIdea(
            name="APIBridge LATAM",
            one_liner="Done-for-you API integrations connecting US SaaS tools with LATAM payment & logistics providers.",
            why_you="Bilingual + deep API skills + LATAM access = a unique cross-border bridge.",
            business_model="Project fees ($2-5k) + retainer for maintenance ($500/mo)",
            target_customer="US e-commerce brands expanding into Mexico, Colombia, Brazil.",
            differentiation="Cultural fluency + technical depth — most integration shops have one, not both.",
            difficulty={"technical": 3, "marketing": 4, "operational": 3},
        ),
        BusinessIdea(
            name="SkillStack.dev",
            one_liner="A SaaS that helps developer-relations teams track which content actually drives signups.",
            why_you="You understand developer tooling from the inside and have a newsletter to seed initial users.",
            business_model="SaaS subscription ($49-199/mo per team)",
            target_customer="DevRel leads at developer-tool companies (Vercel, Supabase-tier).",
            differentiation="Purpose-built for DevRel attribution — not a repurposed marketing analytics tool.",
            difficulty={"technical": 4, "marketing": 3, "operational": 2},
        ),
    ]
    return ideas


def print_ideas(ideas: List[BusinessIdea]) -> None:
    print("=" * 70)
    print("PHASE 2 — PERSONALIZED BUSINESS IDEAS")
    print("=" * 70)
    print()
    for i, idea in enumerate(ideas, 1):
        diff = idea.difficulty
        print(f"  [{i}] {idea.name}")
        print(f"      \"{idea.one_liner}\"")
        print(f"      Why YOU:       {idea.why_you}")
        print(f"      Model:         {idea.business_model}")
        print(f"      Customer:      {idea.target_customer}")
        print(f"      Moat:          {idea.differentiation}")
        print(f"      Difficulty:    Tech {diff['technical']}/5 | Mktg {diff['marketing']}/5 | Ops {diff['operational']}/5")
        print()


# ── Phase 3: Deep Dive ──────────────────────────────────────────────────────

def phase3_deep_dive(idea: BusinessIdea, profile: dict) -> DeepDive:
    return DeepDive(
        idea_name=idea.name,
        market_analysis={
            "tam": "$2.4B (internal tooling / low-code dashboard market)",
            "competitors": [
                "Retool — powerful but expensive ($10+/user/mo), overkill for simple dashboards",
                "Appsmith — open-source but requires hosting & config overhead",
                "Generic UI kits (Tailwind UI, Tremor) — not dashboard-specific",
            ],
            "timing": "Post-AI boom: teams want to ship internal tools faster, not build from scratch.",
            "channels_ranked": [
                "1. Your 10k dev newsletter (warm audience, free)",
                "2. Dev Twitter / X threads showing before/after screenshots",
                "3. Product Hunt launch",
                "4. r/webdev, r/reactjs, Hacker News Show HN",
            ],
        },
        gtm_plan={
            "pre_launch": [
                "Week -2: Tease 3 dashboard screenshots in newsletter",
                "Week -1: Collect 200 waitlist emails via simple landing page",
            ],
            "launch_day": [
                "Product Hunt submission (Tuesday 12:01 AM PT)",
                "Newsletter blast to full 10k list",
                "X/Twitter thread: '5 dashboards I built at [company] — now yours for $49'",
            ],
            "post_launch": [
                "Week +1: Collect feedback, ship 2 quick-win templates",
                "Week +2: Publish a 'How I built this' blog post for SEO",
                "Month +2: Launch subscription tier with new templates monthly",
            ],
            "pricing": "$49 starter (3 templates) / $99 pro (10 templates) / $19/mo subscription",
            "first_10_customers": "DM 30 engineering managers from your network, offer 50% early-bird discount.",
        },
        mvp_roadmap={
            "core_features": [
                "5 polished React dashboard templates (metrics, CRUD, logs, charts, settings)",
                "One-command install (npx create-devdash)",
                "Docs site with live preview",
            ],
            "tech_stack": "React + Tailwind + Recharts (matches your existing skills)",
            "week_by_week": {
                "Week 1": "Extract & clean 3 best dashboards from your past work",
                "Week 2": "Build template scaffolding CLI (npx create-devdash)",
                "Week 3": "Add 2 more templates, write docs, deploy preview site",
                "Week 4": "Payment integration (Lemon Squeezy — $0 upfront), landing page",
            },
            "do_not_build": [
                "Authentication / user accounts (just sell static templates)",
                "Hosting or deployment features",
                "A visual drag-and-drop editor (scope creep)",
            ],
        },
        action_plan_72h=[
            {
                "period": "Hours 0-4 (Day 1 morning)",
                "tasks": [
                    "Pick your best internal dashboard and strip proprietary data",
                    "Set up a GitHub repo: devdash-templates",
                    "Deploy a bare-bones landing page on Vercel (headline + email capture)",
                ],
            },
            {
                "period": "Hours 4-8 (Day 1 afternoon)",
                "tasks": [
                    "Write a newsletter issue: 'I'm packaging my best dashboards — want early access?'",
                    "Send to your 10k list; goal: 100 signups",
                    "Post a screenshot thread on X/Twitter",
                ],
            },
            {
                "period": "Hours 8-16 (Day 2)",
                "tasks": [
                    "Polish the first template into a standalone package",
                    "Add a README with install instructions",
                    "DM 10 eng-manager contacts: 'Building this — would you pay $49?'",
                ],
            },
            {
                "period": "Hours 16-24 (Day 3)",
                "tasks": [
                    "Set up Lemon Squeezy checkout link ($49 early-bird price)",
                    "Add payment link to landing page",
                    "Reply to every email/DM — close your first sale",
                    "MILESTONE: First dollar earned",
                ],
            },
        ],
    )


def print_deep_dive(dd: DeepDive) -> None:
    print("=" * 70)
    print(f"PHASE 3 — DEEP DIVE: {dd.idea_name.upper()}")
    print("=" * 70)

    # Market Analysis
    print("\n  MARKET ANALYSIS")
    print(f"    TAM: {dd.market_analysis['tam']}")
    print("    Competitors:")
    for c in dd.market_analysis["competitors"]:
        print(f"      - {c}")
    print(f"    Timing: {dd.market_analysis['timing']}")
    print("    Acquisition Channels (ranked):")
    for ch in dd.market_analysis["channels_ranked"]:
        print(f"      {ch}")

    # GTM
    print("\n  GO-TO-MARKET PLAN")
    print("    Pre-launch:")
    for step in dd.gtm_plan["pre_launch"]:
        print(f"      - {step}")
    print("    Launch Day:")
    for step in dd.gtm_plan["launch_day"]:
        print(f"      - {step}")
    print("    Post-launch:")
    for step in dd.gtm_plan["post_launch"]:
        print(f"      - {step}")
    print(f"    Pricing: {dd.gtm_plan['pricing']}")
    print(f"    First 10 Customers: {dd.gtm_plan['first_10_customers']}")

    # MVP Roadmap
    print("\n  MVP ROADMAP")
    print("    Core Features:")
    for f in dd.mvp_roadmap["core_features"]:
        print(f"      - {f}")
    print(f"    Tech Stack: {dd.mvp_roadmap['tech_stack']}")
    print("    Build Plan:")
    for week, task in dd.mvp_roadmap["week_by_week"].items():
        print(f"      {week}: {task}")
    print("    DO NOT Build:")
    for x in dd.mvp_roadmap["do_not_build"]:
        print(f"      - {x}")

    # 72-hour plan
    print("\n  72-HOUR ACTION PLAN")
    for block in dd.action_plan_72h:
        print(f"    {block['period']}:")
        for t in block["tasks"]:
            print(f"      [ ] {t}")
    print()


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print()
    print("  Build DNA — Business Ideation from Your Unique Strengths")
    print("  =========================================================")
    print("  Demo with mock founder profile (no API keys required)")
    print()

    # Phase 1
    phase1_intake(MOCK_FOUNDER)

    # Phase 2
    ideas = phase2_ideation(MOCK_FOUNDER)
    print_ideas(ideas)

    # Phase 3 — auto-select idea #1 for demo
    selected = ideas[0]
    print(f"  >> Auto-selecting idea [{1}] \"{selected.name}\" for deep dive...\n")
    dd = phase3_deep_dive(selected, MOCK_FOUNDER)
    print_deep_dive(dd)

    # Summary
    print("=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print()
    print("  In a live Claude session the skill would:")
    print("    1. Ask YOU the intake questions interactively")
    print("    2. Generate ideas tailored to YOUR unique DNA")
    print("    3. Let you pick an idea, then produce the full deep-dive")
    print()
    print("  Install: copy SKILL.md to ~/.claude/skills/build_dna_business_ideation/")
    print("  Trigger: 'build a business around my skills'")
    print()

    # Also dump structured JSON for programmatic consumers
    output = {
        "founder_profile": MOCK_FOUNDER,
        "ideas": [asdict(i) for i in ideas],
        "deep_dive": asdict(dd),
    }
    with open("output.json", "w") as f:
        json.dump(output, f, indent=2)
    print("  Structured output written to output.json")
    print()


if __name__ == "__main__":
    main()
