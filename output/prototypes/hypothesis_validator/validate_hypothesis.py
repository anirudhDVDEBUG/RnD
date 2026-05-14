#!/usr/bin/env python3
"""
hypothesis_validator demo — runs the 6-step validation framework against a
sample startup hypothesis using mock data (no API keys required).

This mirrors what the Claude Code skill does interactively, but in a
standalone script so you can see the output format and scoring logic.
"""

import json
import textwrap
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Literal

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

ICPRating = Literal["Sharp", "Fuzzy", "Missing"]
EvidenceRating = Literal["Supporting", "Neutral", "Contradicting"]
MoneyRating = Literal["Strong", "Weak", "None"]
GTMRating = Literal["Clear path", "Needs experimentation", "No obvious path"]
Verdict = Literal["Validate further", "Pivot needed", "Kill or rethink"]


@dataclass
class Hypothesis:
    target_customer: str
    problem: str
    desired_action: str
    proposed_solution: str
    key_assumption: str

    def statement(self) -> str:
        return (
            f"{self.target_customer} has {self.problem} and will "
            f"{self.desired_action} for {self.proposed_solution} "
            f"because {self.key_assumption}."
        )


@dataclass
class ICPCheck:
    who_exactly: str
    where_they_gather: str
    segment_size: str
    urgency: str
    rating: ICPRating


@dataclass
class EvidenceScan:
    demand_signals: str
    existing_alternatives: str
    failed_predecessors: str
    market_timing: str
    rating: EvidenceRating


@dataclass
class MoneySignals:
    already_paying: str
    budget_exists: str
    price_anchors: str
    jtbd_value: str
    switching_cost: str
    rating: MoneyRating


@dataclass
class GTMCheck:
    channel_access: str
    first_10_customers: str
    sales_cycle: str
    unfair_advantage: str
    solo_feasibility: str
    rating: GTMRating


@dataclass
class ValidationReport:
    hypothesis: Hypothesis
    icp: ICPCheck
    evidence: EvidenceScan
    money: MoneySignals
    gtm: GTMCheck
    verdict: Verdict = ""
    next_steps: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.verdict:
            self.verdict = self._compute_verdict()

    def _compute_verdict(self) -> Verdict:
        score = 0
        score += {"Sharp": 2, "Fuzzy": 1, "Missing": 0}[self.icp.rating]
        score += {"Supporting": 2, "Neutral": 1, "Contradicting": 0}[self.evidence.rating]
        score += {"Strong": 2, "Weak": 1, "None": 0}[self.money.rating]
        score += {"Clear path": 2, "Needs experimentation": 1, "No obvious path": 0}[self.gtm.rating]
        if score >= 6:
            return "Validate further"
        elif score >= 3:
            return "Pivot needed"
        return "Kill or rethink"

    def _verdict_icon(self) -> str:
        return {
            "Validate further": "[GREEN]",
            "Pivot needed": "[YELLOW]",
            "Kill or rethink": "[RED]",
        }[self.verdict]

    def to_markdown(self) -> str:
        steps = "\n".join(f"  {i+1}. [ ] {s}" for i, s in enumerate(self.next_steps))
        risks = "\n".join(f"  - {r}" for r in self.key_risks)
        return textwrap.dedent(f"""\
        ## Hypothesis Validation Report -- {date.today().isoformat()}

        ### Hypothesis
        {self.hypothesis.statement()}

        ### Scorecard
        | Dimension       | Rating                  | Key Finding |
        |-----------------|-------------------------|-------------|
        | ICP Clarity     | {self.icp.rating:<23} | {self.icp.who_exactly} |
        | Evidence        | {self.evidence.rating:<23} | {self.evidence.demand_signals} |
        | Money Signals   | {self.money.rating:<23} | {self.money.already_paying} |
        | GTM Feasibility | {self.gtm.rating:<23} | {self.gtm.channel_access} |

        ### Overall Verdict
        {self._verdict_icon()} **{self.verdict}**

        ### Recommended Next Steps
        {steps}

        ### Key Risks
        {risks}
        """)

    def to_json(self) -> str:
        d = asdict(self)
        d["verdict"] = self.verdict
        d["date"] = date.today().isoformat()
        return json.dumps(d, indent=2)


# ---------------------------------------------------------------------------
# Mock data: two sample hypotheses (one strong, one weak)
# ---------------------------------------------------------------------------

def build_strong_example() -> ValidationReport:
    """AI meeting-notes tool — strong signals across the board."""
    return ValidationReport(
        hypothesis=Hypothesis(
            target_customer="Remote-first startup founders (seed to Series A, 5-30 employees)",
            problem="losing 5+ hours/week to meeting notes, action-item tracking, and follow-ups",
            desired_action="pay $29/mo per seat",
            proposed_solution="an AI meeting assistant that auto-generates notes, extracts action items, and pushes them to project-management tools",
            key_assumption="founders value saved time over privacy concerns about recording meetings",
        ),
        icp=ICPCheck(
            who_exactly="Can name 5+: YC W24 batch founders, Indie Hackers top posters, micro-SaaS founders on Twitter/X",
            where_they_gather="Indie Hackers, r/startups, Twitter/X #buildinpublic, YC Slack, Lenny's Newsletter community",
            segment_size="~120K remote-first startups globally (Carta data); niche enough to dominate, big enough to matter",
            urgency="Painkiller — founders mention meeting overhead as top-3 time sink in surveys",
            rating="Sharp",
        ),
        evidence=EvidenceScan(
            demand_signals="'AI meeting notes' Google Trends up 340% YoY; r/productivity threads weekly; 2.1K upvotes on a Show HN post for a similar concept",
            existing_alternatives="Otter.ai ($16.99/mo), Fireflies.ai ($18/mo), Fathom (free tier) — all general-purpose, none deeply integrated with PM tools",
            failed_predecessors="Noted.ai shut down 2022 (ran out of funding, not demand); Hugo pivoted to enterprise",
            market_timing="GPT-4o-class models make real-time transcription + summarisation cheap; Zoom/Meet APIs now mature",
            rating="Supporting",
        ),
        money=MoneySignals(
            already_paying="Yes — Otter.ai has 1M+ users, Fireflies raised $14M; customers paying $10-$30/mo today",
            budget_exists="SaaS tool budget is standard at seed+ startups; meeting tools are a recognised line item",
            price_anchors="$10-$30/mo per seat for AI transcription; $5-$15/mo for basic note tools",
            jtbd_value="Saving 5 hrs/week at a $75/hr founder-equivalent rate = $1,500/mo value per person",
            switching_cost="Low — meetings happen regardless; switching just means swapping the bot in the call",
            rating="Strong",
        ),
        gtm=GTMCheck(
            channel_access="Organic: Twitter/X build-in-public, Indie Hackers, Product Hunt launch, YC founder Slack channels",
            first_10_customers="DM 50 founders from personal network + IH/Twitter who tweeted about meeting pain; offer free pilot",
            sales_cycle="Self-serve with 14-day trial; no enterprise sales needed at this stage",
            unfair_advantage="Founder has 8 years in remote work tooling; 4K Twitter followers in target niche",
            solo_feasibility="Yes — one developer can build MVP with Whisper API + GPT-4o + Zapier integrations in 4-6 weeks",
            rating="Clear path",
        ),
        next_steps=[
            "Run 10 customer-discovery calls using Mom Test framework this week",
            "Build landing page with waitlist; target 200 sign-ups in 2 weeks via Twitter/IH",
            "Ship concierge MVP (manually send notes) for first 5 users to validate retention",
            "Set pricing experiment: $19 vs $29/mo A/B test on landing page",
        ],
        key_risks=[
            "Zoom/Google may bundle AI notes natively (platform risk)",
            "Privacy objections from recorded meeting participants",
            "Low switching cost means low moat — must win on integrations and speed",
        ],
    )


def build_weak_example() -> ValidationReport:
    """Blockchain pet-food tracker — weak signals, used to show a 'kill' verdict."""
    return ValidationReport(
        hypothesis=Hypothesis(
            target_customer="Health-conscious pet owners in the US",
            problem="not knowing where their pet food ingredients come from",
            desired_action="pay $9.99/mo",
            proposed_solution="a blockchain-powered pet-food supply-chain tracker app",
            key_assumption="pet owners care enough about ingredient provenance to pay a monthly fee for transparency",
        ),
        icp=ICPCheck(
            who_exactly="Cannot name 5 specific prospects — 'health-conscious pet owners' is too broad",
            where_they_gather="General pet forums, but no single concentrated community focused on supply-chain transparency",
            segment_size="~67M US pet-owning households — mass market, impossible to dominate as a solo founder",
            urgency="Vitamin — pet owners care about quality but rarely research supply chains themselves",
            rating="Fuzzy",
        ),
        evidence=EvidenceScan(
            demand_signals="'Pet food supply chain' has flat Google Trends; no Reddit threads requesting this; no Show HN traction",
            existing_alternatives="Pet-food brands self-certify (Blue Buffalo, Orijen); USDA has inspection data — customers trust labels",
            failed_predecessors="FoodLogiQ tried B2C food traceability and pivoted to B2B; blockchain food-tracking startups in human food struggled",
            market_timing="No clear catalyst — blockchain UX is still poor for consumers; no regulatory push",
            rating="Contradicting",
        ),
        money=MoneySignals(
            already_paying="No — pet owners pay for premium food brands, not for traceability tools on top",
            budget_exists="No recognised consumer budget line for 'food traceability subscriptions'",
            price_anchors="Pet food apps are mostly free (BarkHappy, Pet First Aid); premium pet-tech is hardware (GPS collars $5-$10/mo)",
            jtbd_value="Job is 'feel confident about pet health' — but existing brand trust already does this for most owners",
            switching_cost="N/A — no current tool to switch from; this is a new behavior to create",
            rating="None",
        ),
        gtm=GTMCheck(
            channel_access="No organic channel with concentrated demand; would need paid ads from day one",
            first_10_customers="No clear path — cold outreach to pet owners about blockchain is a hard sell",
            sales_cycle="Would need to be self-serve, but requires both consumer adoption AND pet-food brand partnerships",
            unfair_advantage="None stated — no pet industry experience, no existing audience, no brand partnerships",
            solo_feasibility="No — requires blockchain infra, brand partnerships, and consumer app simultaneously",
            rating="No obvious path",
        ),
        next_steps=[
            "Interview 10 premium pet-food buyers — do they actually worry about supply chains?",
            "Explore B2B pivot: sell traceability to pet-food brands instead of consumers",
            "Consider dropping blockchain — a simple 'ingredient sourcing report' might address the core need with 10x less complexity",
        ],
        key_risks=[
            "Solving a problem customers don't feel — no pull from market",
            "Blockchain adds complexity without clear consumer value",
            "Two-sided marketplace problem: need brands AND consumers simultaneously",
        ],
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("  HYPOTHESIS VALIDATOR — Demo Run")
    print("=" * 70)

    # --- Example 1: Strong hypothesis ---
    print("\n>>> EXAMPLE 1: Strong hypothesis (AI meeting-notes tool)\n")
    strong = build_strong_example()
    print(strong.to_markdown())

    print("\n" + "-" * 70)

    # --- Example 2: Weak hypothesis ---
    print("\n>>> EXAMPLE 2: Weak hypothesis (Blockchain pet-food tracker)\n")
    weak = build_weak_example()
    print(weak.to_markdown())

    # --- JSON output ---
    print("-" * 70)
    print("\n>>> JSON output (strong example) for programmatic use:\n")
    print(strong.to_json())

    print("\n" + "=" * 70)
    print("  Done. Install the SKILL.md in Claude Code for interactive use.")
    print("  See HOW_TO_USE.md for setup instructions.")
    print("=" * 70)


if __name__ == "__main__":
    main()
