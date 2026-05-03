"""
Founder Fundraising Outreach Generator

Generates investor outreach emails (cold, follow-up, warm intro) and
due diligence prep documents using structured templates and founder/company context.
"""

import json
import textwrap
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class CompanyProfile:
    name: str
    one_liner: str
    stage: str  # pre-seed, seed, series-a
    raising: str  # e.g. "$2M"
    traction: list[str] = field(default_factory=list)
    website: str = ""
    founder_name: str = ""
    founder_title: str = "CEO & Co-Founder"
    founder_linkedin: str = ""


@dataclass
class InvestorProfile:
    name: str
    firm: str
    thesis: str = ""
    portfolio_companies: list[str] = field(default_factory=list)
    shared_connection: Optional[str] = None


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def _wrap(text: str, width: int = 72) -> str:
    return "\n".join(textwrap.fill(line, width=width) for line in text.splitlines())


def generate_cold_email(company: CompanyProfile, investor: InvestorProfile) -> str:
    portfolio_ref = ""
    if investor.portfolio_companies:
        portfolio_ref = (
            f"I noticed {investor.firm}'s investment in {investor.portfolio_companies[0]} "
            f"— our approach to {company.one_liner.split(',')[0].lower().strip()} is adjacent."
        )
    else:
        portfolio_ref = (
            f"Your thesis around {investor.thesis} aligns closely with what we're building."
        )

    traction_lines = "\n".join(f"  - {t}" for t in company.traction[:3])

    body = f"""\
Subject: {company.name} — {company.traction[0] if company.traction else company.one_liner}

Hi {investor.name},

{portfolio_ref}

{company.name} {company.one_liner}. We're raising a {company.raising} {company.stage} round.

Here's where we are:
{traction_lines}

Would you have 15 minutes this week or next for a quick intro call?

Best,
{company.founder_name}
{company.founder_title}, {company.name}
{company.website}
{company.founder_linkedin}
"""
    return _wrap(body)


def generate_followup(company: CompanyProfile, investor: InvestorProfile,
                      prior_context: str, new_traction: str) -> str:
    body = f"""\
Subject: Re: {company.name} — quick update

Hi {investor.name},

Great speaking with you {prior_context}. Wanted to share a quick update:

{new_traction}

We're still in the process of closing our {company.raising} {company.stage} round and would love to continue the conversation. Do you have 15 minutes this week?

Best,
{company.founder_name}
{company.founder_title}, {company.name}
"""
    return _wrap(body)


def generate_warm_intro(company: CompanyProfile, investor: InvestorProfile,
                        connector_name: str) -> str:
    blurb = (
        f"{company.founder_name} is the {company.founder_title} of {company.name}, "
        f"which {company.one_liner}. They're raising a {company.raising} {company.stage} "
        f"round."
    )
    if company.traction:
        blurb += f" Key traction: {company.traction[0]}."

    fit_reason = ""
    if investor.portfolio_companies:
        fit_reason = (
            f"{investor.name} would be a great fit given {investor.firm}'s investment "
            f"in {investor.portfolio_companies[0]} and their thesis around {investor.thesis}."
        )
    else:
        fit_reason = (
            f"{investor.name} would be a great fit given {investor.firm}'s focus on "
            f"{investor.thesis}."
        )

    body = f"""\
Subject: Intro request — {company.name} <> {investor.name} ({investor.firm})

Hi {connector_name},

Would you be open to making an intro to {investor.name} at {investor.firm}?

{fit_reason}

Here's a forwardable blurb:

---

{blurb}

They'd love to set up a 15-minute call with {investor.name} to share more.
{company.founder_name} can be reached at {company.founder_linkedin or company.website}.

---

Thanks so much for considering this!

Best,
{company.founder_name}
"""
    return _wrap(body)


def generate_dd_prep(company: CompanyProfile) -> str:
    body = f"""\
# Due Diligence Prep — {company.name}

## Company Overview
{company.name} {company.one_liner}.
- Stage: {company.stage}
- Raising: {company.raising}
- Website: {company.website}

## Traction & Metrics
{"".join(f"- {t}" + chr(10) for t in company.traction)}
## Team
- {company.founder_name}, {company.founder_title}
  LinkedIn: {company.founder_linkedin}

## Market Size & Competitive Landscape
[To be completed — include TAM/SAM/SOM analysis and key competitors]

## Financial Model Summary
[To be completed — include revenue projections, burn rate, runway]

## Cap Table Overview
[To be completed — current ownership breakdown]

## Key Risks & Mitigations
[To be completed — top 3-5 risks with mitigation strategies]
"""
    return body


# ---------------------------------------------------------------------------
# Demo runner
# ---------------------------------------------------------------------------

DEMO_COMPANY = CompanyProfile(
    name="Lattice AI",
    one_liner="builds real-time compliance monitoring for fintech companies, cutting audit prep from weeks to hours",
    stage="seed",
    raising="$3M",
    traction=[
        "42% MoM revenue growth over the last 6 months",
        "18 paying enterprise customers including 2 Fortune 500 pilots",
        "$380K ARR, up from $45K ARR 9 months ago",
    ],
    website="https://lattice-ai.example.com",
    founder_name="Sarah Chen",
    founder_title="CEO & Co-Founder",
    founder_linkedin="https://linkedin.com/in/sarahchen",
)

DEMO_INVESTORS = [
    InvestorProfile(
        name="Maria Rodriguez",
        firm="Gradient Ventures",
        thesis="applied AI in regulated industries",
        portfolio_companies=["ComplianceBot", "RegTech Labs"],
    ),
    InvestorProfile(
        name="James Park",
        firm="Fintech Capital",
        thesis="infrastructure for financial services",
        portfolio_companies=["PayStack", "LedgerX"],
        shared_connection="David Kim (YC W24 batch)",
    ),
]


def run_demo():
    sep = "=" * 72

    print(sep)
    print("FOUNDER FUNDRAISING OUTREACH — DEMO OUTPUT")
    print(sep)

    # 1. Cold email
    print(f"\n{'─' * 72}")
    print("1. COLD EMAIL")
    print(f"{'─' * 72}\n")
    print(generate_cold_email(DEMO_COMPANY, DEMO_INVESTORS[0]))

    # 2. Follow-up
    print(f"\n{'─' * 72}")
    print("2. FOLLOW-UP EMAIL")
    print(f"{'─' * 72}\n")
    print(generate_followup(
        DEMO_COMPANY,
        DEMO_INVESTORS[0],
        prior_context="at the Fintech Summit last Tuesday",
        new_traction="We just closed our 18th enterprise customer and crossed $380K ARR — a 8.4x increase in 9 months.",
    ))

    # 3. Warm intro request
    print(f"\n{'─' * 72}")
    print("3. WARM INTRO REQUEST")
    print(f"{'─' * 72}\n")
    print(generate_warm_intro(
        DEMO_COMPANY,
        DEMO_INVESTORS[1],
        connector_name="David",
    ))

    # 4. Due diligence prep
    print(f"\n{'─' * 72}")
    print("4. DUE DILIGENCE PREP DOC (template)")
    print(f"{'─' * 72}\n")
    print(generate_dd_prep(DEMO_COMPANY))

    # 5. JSON export of company profile
    print(f"\n{'─' * 72}")
    print("5. STRUCTURED COMPANY PROFILE (JSON)")
    print(f"{'─' * 72}\n")
    print(json.dumps(asdict(DEMO_COMPANY), indent=2))

    print(f"\n{sep}")
    print("All 4 outreach types generated successfully.")
    print(f"{sep}")


if __name__ == "__main__":
    run_demo()
