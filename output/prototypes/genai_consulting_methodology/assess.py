#!/usr/bin/env python3
"""
GenAI Consulting Methodology Toolkit
L1-L5 Maturity Assessment & Eight-Stage Consulting Framework

Diagnoses enterprise GenAI maturity across five dimensions,
generates scorecards, gap analysis, transformation roadmaps,
and use-case prioritization matrices.
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Maturity Levels ──────────────────────────────────────────────────────────

LEVELS = {
    1: ("Initial/Ad-hoc", "No formal AI strategy; scattered experimentation"),
    2: ("Exploring", "Pilot projects underway; basic awareness established"),
    3: ("Defined", "Formal AI strategy exists; governance emerging; repeatable processes"),
    4: ("Managed", "AI integrated into core workflows; metrics-driven optimization"),
    5: ("Optimizing", "AI-native operations; continuous innovation; industry leadership"),
}

DIMENSIONS = [
    "Strategy & Vision",
    "Data & Infrastructure",
    "Talent & Culture",
    "Governance & Ethics",
    "Use Cases & Value",
]

EIGHT_STAGES = [
    "Discovery & Stakeholder Alignment",
    "Maturity Assessment",
    "Opportunity Identification",
    "Architecture & Tool Selection",
    "Pilot Design & Execution",
    "Governance & Policy Framework",
    "Scaling & Operationalization",
    "Continuous Optimization",
]


# ── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class DimensionScore:
    dimension: str
    current_level: int
    target_level: int
    evidence: str
    gaps: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)


@dataclass
class UseCase:
    name: str
    impact: int          # 1-5
    feasibility: int     # 1-5
    strategic_fit: int   # 1-5
    priority_score: float = 0.0

    def compute_priority(self):
        self.priority_score = round(
            self.impact * 0.4 + self.feasibility * 0.35 + self.strategic_fit * 0.25, 2
        )
        return self.priority_score


@dataclass
class RoadmapItem:
    horizon: str      # "90-day", "6-month", "12-month"
    action: str
    dimension: str
    expected_outcome: str


@dataclass
class AssessmentResult:
    company_name: str
    industry: str
    scores: list
    overall_level: float
    overall_label: str
    use_cases: list
    roadmap: list
    current_stage: int
    next_actions: list


# ── Gap Analysis Logic ───────────────────────────────────────────────────────

GAP_RECOMMENDATIONS = {
    "Strategy & Vision": {
        (1, 2): ["Appoint an AI champion or steering committee",
                  "Draft initial AI vision statement aligned to business goals"],
        (2, 3): ["Formalize AI strategy document with executive sponsorship",
                  "Set measurable AI OKRs linked to business outcomes"],
        (3, 4): ["Embed AI KPIs into business unit scorecards",
                  "Establish cross-functional AI council"],
        (4, 5): ["Drive AI-first culture from C-suite",
                  "Launch external AI thought-leadership program"],
    },
    "Data & Infrastructure": {
        (1, 2): ["Inventory existing data assets and assess quality",
                  "Provision basic cloud compute for experimentation"],
        (2, 3): ["Build centralized data lake with governance metadata",
                  "Standardize ML/LLM development environment"],
        (3, 4): ["Implement automated data pipelines with quality gates",
                  "Deploy LLMOps platform (versioning, monitoring, eval)"],
        (4, 5): ["Enable real-time streaming data for AI workloads",
                  "Adopt multi-model orchestration (agents, RAG, fine-tuning)"],
    },
    "Talent & Culture": {
        (1, 2): ["Launch AI literacy program for all employees",
                  "Hire or contract first AI/ML engineers"],
        (2, 3): ["Create AI Center of Excellence with dedicated headcount",
                  "Run cross-functional AI hackathons"],
        (3, 4): ["Embed AI skills into performance reviews and career paths",
                  "Develop internal AI trainer-of-trainers program"],
        (4, 5): ["Recruit AI research talent for differentiated capabilities",
                  "Establish AI fellowship or rotation programs"],
    },
    "Governance & Ethics": {
        (1, 2): ["Define basic acceptable-use policy for AI tools",
                  "Identify regulatory requirements applicable to AI use"],
        (2, 3): ["Create AI ethics review board",
                  "Implement model risk classification framework"],
        (3, 4): ["Deploy automated bias and fairness testing in CI/CD",
                  "Establish incident response process for AI failures"],
        (4, 5): ["Publish external AI transparency report",
                  "Lead industry standards body participation"],
    },
    "Use Cases & Value": {
        (1, 2): ["Identify top-5 quick-win GenAI use cases",
                  "Define ROI measurement framework for pilots"],
        (2, 3): ["Move 2-3 pilots to production with SLAs",
                  "Create reusable prompt/template library"],
        (3, 4): ["Scale to 10+ production AI applications",
                  "Implement A/B testing framework for AI features"],
        (4, 5): ["Productize AI capabilities for customers/partners",
                  "Achieve >30% revenue/cost impact from AI"],
    },
}


def analyze_gaps(dim_score: DimensionScore) -> DimensionScore:
    """Fill gaps and recommendations based on current vs target level."""
    dim = dim_score.dimension
    cur = dim_score.current_level
    tgt = dim_score.target_level

    gaps = []
    recs = []
    for level in range(cur, tgt):
        step = (level, level + 1)
        if dim in GAP_RECOMMENDATIONS and step in GAP_RECOMMENDATIONS[dim]:
            recs.extend(GAP_RECOMMENDATIONS[dim][step])
            gaps.append(f"Gap L{level}→L{level+1}: {LEVELS[level+1][0]} capabilities missing")

    dim_score.gaps = gaps
    dim_score.recommendations = recs
    return dim_score


# ── Roadmap Generator ────────────────────────────────────────────────────────

def generate_roadmap(scores: list) -> list:
    """Create 90-day / 6-month / 12-month roadmap from gap analysis."""
    roadmap = []
    for s in scores:
        if not s.recommendations:
            continue
        # First rec → 90-day, second → 6-month, rest → 12-month
        for i, rec in enumerate(s.recommendations):
            if i == 0:
                horizon = "90-day"
                outcome = f"Close first gap in {s.dimension} (L{s.current_level}→L{s.current_level+1})"
            elif i == 1:
                horizon = "6-month"
                outcome = f"Advance {s.dimension} toward L{min(s.current_level+2, s.target_level)}"
            else:
                horizon = "12-month"
                outcome = f"Reach L{s.target_level} in {s.dimension}"
            roadmap.append(RoadmapItem(
                horizon=horizon, action=rec,
                dimension=s.dimension, expected_outcome=outcome
            ))
    return roadmap


# ── Use-Case Prioritization ─────────────────────────────────────────────────

def prioritize_use_cases(use_cases: list) -> list:
    """Score and sort use cases by weighted priority."""
    for uc in use_cases:
        uc.compute_priority()
    return sorted(use_cases, key=lambda u: u.priority_score, reverse=True)


# ── Determine Consulting Stage ──────────────────────────────────────────────

def determine_stage(overall_level: float) -> tuple:
    """Map maturity level to recommended consulting stage."""
    if overall_level < 1.5:
        return 1, "Discovery & Stakeholder Alignment"
    elif overall_level < 2.0:
        return 2, "Maturity Assessment"
    elif overall_level < 2.5:
        return 3, "Opportunity Identification"
    elif overall_level < 3.0:
        return 4, "Architecture & Tool Selection"
    elif overall_level < 3.5:
        return 5, "Pilot Design & Execution"
    elif overall_level < 4.0:
        return 6, "Governance & Policy Framework"
    elif overall_level < 4.5:
        return 7, "Scaling & Operationalization"
    else:
        return 8, "Continuous Optimization"


# ── Main Assessment ──────────────────────────────────────────────────────────

def run_assessment(company: dict) -> AssessmentResult:
    """Run full maturity assessment from company profile dict."""
    scores = []
    for dim_data in company["dimensions"]:
        ds = DimensionScore(
            dimension=dim_data["dimension"],
            current_level=dim_data["current_level"],
            target_level=dim_data.get("target_level", 5),
            evidence=dim_data.get("evidence", ""),
        )
        analyze_gaps(ds)
        scores.append(ds)

    overall = round(sum(s.current_level for s in scores) / len(scores), 1)
    overall_label = LEVELS[int(round(overall))][0] if 1 <= round(overall) <= 5 else "Unknown"

    use_cases = [UseCase(**uc) for uc in company.get("use_cases", [])]
    use_cases = prioritize_use_cases(use_cases)

    roadmap = generate_roadmap(scores)

    stage_num, stage_name = determine_stage(overall)
    next_actions = [
        f"Current recommended consulting stage: Stage {stage_num} — {stage_name}",
        f"Focus on: {EIGHT_STAGES[stage_num - 1]}",
    ]
    if stage_num < 8:
        next_actions.append(f"Next stage: Stage {stage_num + 1} — {EIGHT_STAGES[stage_num]}")

    return AssessmentResult(
        company_name=company["company_name"],
        industry=company["industry"],
        scores=scores,
        overall_level=overall,
        overall_label=overall_label,
        use_cases=use_cases,
        roadmap=roadmap,
        current_stage=stage_num,
        next_actions=next_actions,
    )


# ── Pretty Printer ───────────────────────────────────────────────────────────

def level_bar(level: int, max_level: int = 5) -> str:
    filled = "█" * level
    empty = "░" * (max_level - level)
    return f"{filled}{empty}"


def print_report(result: AssessmentResult):
    w = 72
    print("=" * w)
    print(f"  GenAI MATURITY ASSESSMENT — {result.company_name.upper()}")
    print(f"  Industry: {result.industry}")
    print("=" * w)

    # Scorecard
    print("\n┌─ MATURITY SCORECARD ─────────────────────────────────────────────┐")
    for s in result.scores:
        bar = level_bar(s.current_level)
        label = LEVELS[s.current_level][0]
        print(f"│  {s.dimension:<24} {bar}  L{s.current_level} ({label})")
    print(f"│{'':─<66}│")
    overall_bar = level_bar(round(result.overall_level))
    print(f"│  {'OVERALL':<24} {overall_bar}  L{result.overall_level} ({result.overall_label})")
    print(f"└{'':─<66}┘")

    # Gap Analysis
    print("\n┌─ GAP ANALYSIS ───────────────────────────────────────────────────┐")
    for s in result.scores:
        if s.gaps:
            print(f"│  {s.dimension}:")
            for g in s.gaps:
                print(f"│    ⚠  {g}")
    print(f"└{'':─<66}┘")

    # Recommendations
    print("\n┌─ KEY RECOMMENDATIONS ────────────────────────────────────────────┐")
    for s in result.scores:
        if s.recommendations:
            print(f"│  {s.dimension}:")
            for r in s.recommendations[:2]:
                print(f"│    → {r}")
    print(f"└{'':─<66}┘")

    # Use-Case Prioritization
    if result.use_cases:
        print("\n┌─ USE CASE PRIORITIZATION MATRIX ─────────────────────────────────┐")
        print(f"│  {'Use Case':<30} {'Impact':>6} {'Feasib':>6} {'Fit':>6} {'Score':>7} │")
        print(f"│  {'':─<57} │")
        for uc in result.use_cases:
            tag = " ★" if uc.priority_score >= 4.0 else ""
            print(f"│  {uc.name:<30} {uc.impact:>6} {uc.feasibility:>6} "
                  f"{uc.strategic_fit:>6} {uc.priority_score:>6.2f}{tag} │")
        print(f"└{'':─<66}┘")

    # Transformation Roadmap
    print("\n┌─ TRANSFORMATION ROADMAP ─────────────────────────────────────────┐")
    for horizon in ["90-day", "6-month", "12-month"]:
        items = [r for r in result.roadmap if r.horizon == horizon]
        if items:
            print(f"│  ── {horizon.upper()} ──")
            for r in items:
                print(f"│    [{r.dimension}] {r.action}")
                print(f"│      Expected: {r.expected_outcome}")
    print(f"└{'':─<66}┘")

    # Consulting Stage
    print("\n┌─ CONSULTING ENGAGEMENT STATUS ───────────────────────────────────┐")
    for i, stage in enumerate(EIGHT_STAGES, 1):
        marker = "►" if i == result.current_stage else " "
        check = "✓" if i < result.current_stage else ("●" if i == result.current_stage else "○")
        print(f"│  {marker} {check} Stage {i}: {stage}")
    print(f"│{'':─<66}│")
    for a in result.next_actions:
        print(f"│  {a}")
    print(f"└{'':─<66}┘")
    print()


# ── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            company = json.load(f)
    else:
        # Read from stdin
        company = json.load(sys.stdin)

    result = run_assessment(company)
    print_report(result)

    # Also dump JSON summary
    summary = {
        "company": result.company_name,
        "industry": result.industry,
        "overall_level": result.overall_level,
        "overall_label": result.overall_label,
        "current_stage": result.current_stage,
        "dimensions": [
            {"dimension": s.dimension, "level": s.current_level, "target": s.target_level}
            for s in result.scores
        ],
        "top_use_cases": [
            {"name": uc.name, "score": uc.priority_score}
            for uc in result.use_cases[:3]
        ],
    }
    with open("assessment_output.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("→ JSON summary written to assessment_output.json")


if __name__ == "__main__":
    main()
