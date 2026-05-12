"""
Enterprise AI Scaling Playbook — core engine.

Takes an organization's maturity assessment answers and produces
a phased scaling plan with prioritized recommendations.
"""

from dataclasses import dataclass
from enum import IntEnum


class Phase(IntEnum):
    TRUST = 1
    GOVERNANCE = 2
    WORKFLOWS = 3
    QUALITY = 4
    COMPOUND = 5

    @property
    def label(self):
        return {
            1: "Build Trust with Early Wins",
            2: "Establish Governance",
            3: "Design Scalable Workflows",
            4: "Maintain Quality at Scale",
            5: "Compound Impact",
        }[self.value]


@dataclass
class AssessmentAnswer:
    question_id: str
    score: int  # 1-5
    notes: str = ""


@dataclass
class Recommendation:
    phase: Phase
    priority: str  # HIGH / MEDIUM / LOW
    title: str
    action: str
    rationale: str


@dataclass
class PlaybookReport:
    org_name: str
    current_phase: Phase
    maturity_score: float
    dimension_scores: dict[str, float]
    recommendations: list[Recommendation]
    next_milestones: list[str]

    def render_text(self) -> str:
        lines: list[str] = []
        w = 60
        lines.append("=" * w)
        lines.append("ENTERPRISE AI SCALING PLAYBOOK")
        lines.append(f"Organization: {self.org_name}")
        lines.append("=" * w)
        lines.append("")

        # Maturity summary
        bar_len = 30
        filled = round(self.maturity_score / 5 * bar_len)
        bar = "#" * filled + "-" * (bar_len - filled)
        lines.append(f"Overall AI Maturity Score: {self.maturity_score:.1f} / 5.0")
        lines.append(f"  [{bar}]")
        lines.append(f"Current Phase: Phase {self.current_phase.value} — {self.current_phase.label}")
        lines.append("")

        # Dimension breakdown
        lines.append("-" * w)
        lines.append("DIMENSION SCORES")
        lines.append("-" * w)
        for dim, score in sorted(self.dimension_scores.items()):
            filled = round(score / 5 * 20)
            bar = "#" * filled + "-" * (20 - filled)
            lines.append(f"  {dim:<28s} {score:.1f}  [{bar}]")
        lines.append("")

        # Recommendations grouped by priority
        lines.append("-" * w)
        lines.append("RECOMMENDATIONS")
        lines.append("-" * w)
        for pri in ("HIGH", "MEDIUM", "LOW"):
            recs = [r for r in self.recommendations if r.priority == pri]
            if not recs:
                continue
            lines.append(f"\n  [{pri} PRIORITY]")
            for i, r in enumerate(recs, 1):
                lines.append(f"  {i}. (Phase {r.phase.value}) {r.title}")
                lines.append(f"     Action:    {r.action}")
                lines.append(f"     Rationale: {r.rationale}")
        lines.append("")

        # Next milestones
        lines.append("-" * w)
        lines.append("NEXT 90-DAY MILESTONES")
        lines.append("-" * w)
        for i, m in enumerate(self.next_milestones, 1):
            lines.append(f"  {i}. {m}")
        lines.append("")
        lines.append("=" * w)
        return "\n".join(lines)


# ── Assessment dimensions & questions ────────────────────────

DIMENSIONS = {
    "Leadership & Strategy": [
        ("ls1", "Does executive leadership actively sponsor AI initiatives?"),
        ("ls2", "Is there a documented AI strategy aligned with business goals?"),
    ],
    "Governance & Risk": [
        ("gr1", "Do you have a formal AI governance framework?"),
        ("gr2", "Are data-privacy and security policies defined for AI use?"),
    ],
    "Talent & Culture": [
        ("tc1", "Do teams have access to AI training and upskilling programs?"),
        ("tc2", "Are there designated AI champions in each business unit?"),
    ],
    "Workflow Integration": [
        ("wi1", "Are AI tools embedded in day-to-day workflows?"),
        ("wi2", "Do you have standardized human-in-the-loop patterns?"),
    ],
    "Quality & Evaluation": [
        ("qe1", "Is there automated quality monitoring for AI outputs?"),
        ("qe2", "Do you track adoption and satisfaction metrics?"),
    ],
    "Scale & Impact": [
        ("si1", "Do AI workflows feed into each other (compound value)?"),
        ("si2", "Are learnings shared across teams via CoEs or communities?"),
    ],
}


def _all_questions() -> list[tuple[str, str, str]]:
    """Return (dimension, qid, question_text) triples."""
    out = []
    for dim, qs in DIMENSIONS.items():
        for qid, text in qs:
            out.append((dim, qid, text))
    return out


def compute_dimension_scores(answers: list[AssessmentAnswer]) -> dict[str, float]:
    score_map: dict[str, int] = {a.question_id: a.score for a in answers}
    dim_scores: dict[str, float] = {}
    for dim, qs in DIMENSIONS.items():
        vals = [score_map.get(qid, 3) for qid, _ in qs]
        dim_scores[dim] = sum(vals) / len(vals)
    return dim_scores


def determine_phase(maturity: float) -> Phase:
    if maturity < 1.8:
        return Phase.TRUST
    if maturity < 2.6:
        return Phase.GOVERNANCE
    if maturity < 3.4:
        return Phase.WORKFLOWS
    if maturity < 4.2:
        return Phase.QUALITY
    return Phase.COMPOUND


# ── Recommendation engine ────────────────────────────────────

_REC_TEMPLATES: dict[str, list[tuple[Phase, str, str, str]]] = {
    "Leadership & Strategy": [
        (Phase.TRUST, "Secure executive AI sponsorship",
         "Schedule an AI value briefing with C-suite stakeholders",
         "Executive sponsorship is the #1 predictor of successful AI scaling"),
        (Phase.GOVERNANCE, "Document organization-wide AI strategy",
         "Draft a 1-page AI strategy doc linking AI goals to business KPIs",
         "Without clear strategy, teams duplicate effort and pick low-value use cases"),
    ],
    "Governance & Risk": [
        (Phase.GOVERNANCE, "Establish AI governance framework",
         "Form a cross-functional governance committee (legal, security, engineering, business)",
         "Clear guardrails let teams move faster — governance enables speed"),
        (Phase.GOVERNANCE, "Define AI risk tiers",
         "Classify use cases into Tier 1 (full autonomy), Tier 2 (review), Tier 3 (AI-assisted)",
         "Risk tiering sets appropriate oversight without blanket restrictions"),
    ],
    "Talent & Culture": [
        (Phase.TRUST, "Launch AI upskilling program",
         "Offer hands-on workshops covering prompt engineering and AI-assisted workflows",
         "People drive adoption — technology alone doesn't scale"),
        (Phase.QUALITY, "Designate AI champions per business unit",
         "Identify and empower 1-2 AI champions in each department",
         "Champions accelerate adoption and create feedback loops"),
    ],
    "Workflow Integration": [
        (Phase.WORKFLOWS, "Map and prioritize AI-ready workflows",
         "Audit top-20 repetitive tasks and rank by AI leverage potential",
         "Start narrow, scale wide — depth before breadth"),
        (Phase.WORKFLOWS, "Build shared prompt library",
         "Create a versioned, team-accessible repository of tested prompts and templates",
         "Standardization prevents wheel-reinvention and ensures consistency"),
    ],
    "Quality & Evaluation": [
        (Phase.QUALITY, "Implement automated output monitoring",
         "Set up regression tests and quality dashboards for AI-powered workflows",
         "Quality over quantity — ten good workflows beat a hundred bad ones"),
        (Phase.QUALITY, "Track adoption and satisfaction metrics",
         "Deploy quarterly surveys and usage analytics across AI-enabled tools",
         "Metrics expose what's working and where to invest next"),
    ],
    "Scale & Impact": [
        (Phase.COMPOUND, "Connect AI workflows for compound value",
         "Identify 2-3 workflow chains where one AI output feeds the next",
         "Compound workflows create exponential rather than linear returns"),
        (Phase.COMPOUND, "Establish internal AI community of practice",
         "Launch monthly cross-team showcases and a shared case-study library",
         "Shared learnings prevent repeated mistakes and surface best practices"),
    ],
}


def generate_recommendations(dim_scores: dict[str, float], current_phase: Phase) -> list[Recommendation]:
    recs: list[Recommendation] = []
    for dim, score in dim_scores.items():
        templates = _REC_TEMPLATES.get(dim, [])
        for phase, title, action, rationale in templates:
            # Include if this dimension is weak or the recommendation phase is at/near current phase
            if score < 3.0 or phase.value <= current_phase.value + 1:
                priority = "HIGH" if score < 2.5 else ("MEDIUM" if score < 3.5 else "LOW")
                recs.append(Recommendation(phase=phase, priority=priority,
                                           title=title, action=action, rationale=rationale))
    # Deduplicate and sort
    seen = set()
    unique = []
    for r in recs:
        if r.title not in seen:
            seen.add(r.title)
            unique.append(r)
    pri_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    unique.sort(key=lambda r: (pri_order[r.priority], r.phase.value))
    return unique


def generate_milestones(current_phase: Phase, dim_scores: dict[str, float]) -> list[str]:
    milestones = []
    weakest = sorted(dim_scores.items(), key=lambda x: x[1])
    if current_phase <= Phase.TRUST:
        milestones.append("Complete 2 pilot AI use cases with measurable ROI")
        milestones.append("Present pilot results to leadership for buy-in")
    if current_phase <= Phase.GOVERNANCE:
        milestones.append("Publish v1 AI governance policy document")
        milestones.append("Convene first governance committee meeting")
    if current_phase <= Phase.WORKFLOWS:
        milestones.append("Deploy AI in 3+ production workflows with human-in-the-loop")
        milestones.append("Release shared prompt library to all teams")
    if current_phase <= Phase.QUALITY:
        milestones.append("Achieve 90%+ user satisfaction on AI-assisted workflows")
        milestones.append("Activate AI champions in every business unit")
    if current_phase >= Phase.COMPOUND:
        milestones.append("Launch first compound AI workflow chain")
        milestones.append("Publish internal AI maturity scorecard")
    # Add dimension-specific milestone for weakest area
    if weakest:
        dim_name = weakest[0][0]
        milestones.append(f"Improve '{dim_name}' score from {weakest[0][1]:.1f} to {min(weakest[0][1]+1, 5.0):.1f}")
    return milestones[:6]


def generate_playbook(org_name: str, answers: list[AssessmentAnswer]) -> PlaybookReport:
    dim_scores = compute_dimension_scores(answers)
    maturity = sum(dim_scores.values()) / len(dim_scores)
    current_phase = determine_phase(maturity)
    recs = generate_recommendations(dim_scores, current_phase)
    milestones = generate_milestones(current_phase, dim_scores)
    return PlaybookReport(
        org_name=org_name,
        current_phase=current_phase,
        maturity_score=maturity,
        dimension_scores=dim_scores,
        recommendations=recs,
        next_milestones=milestones,
    )
