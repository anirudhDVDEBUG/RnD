#!/usr/bin/env python3
"""
YC OpenAI Stake Analysis — standalone demo.

Uses embedded data (no API keys required) to model Y Combinator's stake
in OpenAI and compare it against other notable accelerator returns.
"""

import json
import textwrap
from dataclasses import dataclass

# ── Core data ────────────────────────────────────────────────────────────────

@dataclass
class StakeInfo:
    entity: str
    stake_pct: float          # ownership percentage
    valuation_b: float        # company valuation in $B
    initial_investment_m: float  # estimated initial investment in $M
    source: str

    @property
    def stake_value_b(self) -> float:
        return self.stake_pct / 100 * self.valuation_b

    @property
    def multiple(self) -> float:
        if self.initial_investment_m == 0:
            return float("inf")
        return (self.stake_value_b * 1000) / self.initial_investment_m


OPENAI_VALUATION_B = 852.0  # May 2026

YC_STAKE = StakeInfo(
    entity="Y Combinator",
    stake_pct=0.6,
    valuation_b=OPENAI_VALUATION_B,
    initial_investment_m=0.15,   # YC S05-era deal ~$150K
    source="John Gruber / Daring Fireball, via Simon Willison",
)

# Comparable accelerator mega-returns (public estimates)
COMPARABLES = [
    StakeInfo("YC → Airbnb",        0.7,  75.0,  0.02,  "public filings"),
    StakeInfo("YC → Stripe",        0.5, 220.0,  0.12,  "public estimates"),
    StakeInfo("YC → DoorDash",      0.3,  55.0,  0.12,  "public filings"),
    StakeInfo("Techstars → SendGrid", 6.0, 3.0,  0.018, "public filings"),
]


# ── Analysis functions ───────────────────────────────────────────────────────

def format_dollar(value_b: float) -> str:
    if value_b >= 1.0:
        return f"${value_b:,.1f}B"
    return f"${value_b * 1000:,.0f}M"


def build_summary(stake: StakeInfo) -> str:
    return textwrap.dedent(f"""\
    ╔══════════════════════════════════════════════════════════════╗
    ║  Y COMBINATOR'S STAKE IN OPENAI — KEY NUMBERS              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  OpenAI valuation (May 2026):   {format_dollar(stake.valuation_b):>14}              ║
    ║  YC ownership stake:            {stake.stake_pct:>13.1f}%              ║
    ║  Implied stake value:           {format_dollar(stake.stake_value_b):>14}              ║
    ║  Estimated initial investment:  {format_dollar(stake.initial_investment_m / 1000):>14}              ║
    ║  Estimated return multiple:     {stake.multiple:>12,.0f}x              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  Source: {stake.source:<51} ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


def build_comparables_table(yc: StakeInfo, comps: list[StakeInfo]) -> str:
    lines = [
        "┌──────────────────────┬──────────┬───────────────┬───────────────┐",
        "│ Investment           │ Stake %  │ Stake Value   │ Return Mult.  │",
        "├──────────────────────┼──────────┼───────────────┼───────────────┤",
    ]
    all_stakes = [yc] + comps
    for s in sorted(all_stakes, key=lambda x: x.stake_value_b, reverse=True):
        label = s.entity if s.entity != "Y Combinator" else "YC → OpenAI  ◀"
        lines.append(
            f"│ {label:<20} │ {s.stake_pct:>6.1f}%  │ {format_dollar(s.stake_value_b):>13} │ {s.multiple:>11,.0f}x  │"
        )
    lines.append("└──────────────────────┴──────────┴───────────────┴───────────────┘")
    return "\n".join(lines)


def build_analysis() -> str:
    return textwrap.dedent("""\
    ANALYSIS
    ════════
    1. YC's ~0.6% stake in OpenAI is worth more than $5B at the $852B
       valuation — likely the single largest dollar-value return from
       any startup accelerator investment in history.

    2. The return multiple (~34,000x) dwarfs even YC's other legendary
       bets like Airbnb and Stripe, driven by OpenAI's unprecedented
       valuation trajectory.

    3. This stake was "devilishly difficult information to obtain"
       (Gruber), partly because OpenAI's corporate restructuring from
       nonprofit → capped-profit → for-profit made ownership opaque.

    4. Context for builders: the AI foundation-model layer is generating
       returns that reshape the entire VC/accelerator landscape. For
       teams building Claude-driven products (lead-gen, agent factories,
       voice AI), this signals sustained capital inflows into the
       ecosystem — meaning more potential customers, partners, and
       competitors.

    SOURCES
    ═══════
    • Simon Willison — simonwillison.net/2026/May/5/john-gruber/
    • John Gruber — daringfireball.net/2026/05/y_combinators_stake_in_openai
    • OpenAI — openai.com/index/accelerating-the-next-phase-ai/
    """)


def sensitivity_analysis(stake_pct: float, valuations: list[float]) -> str:
    lines = ["SENSITIVITY: Stake value at different valuations",
             "─" * 50]
    for v in valuations:
        val = stake_pct / 100 * v
        lines.append(f"  At {format_dollar(v):>8} valuation → stake = {format_dollar(val)}")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(build_summary(YC_STAKE))
    print(build_comparables_table(YC_STAKE, COMPARABLES))
    print()
    print(sensitivity_analysis(
        YC_STAKE.stake_pct,
        [300.0, 500.0, 852.0, 1000.0, 1500.0]
    ))
    print()
    print(build_analysis())

    # Also dump structured JSON for downstream tooling
    output = {
        "yc_stake": {
            "stake_pct": YC_STAKE.stake_pct,
            "valuation_b": YC_STAKE.valuation_b,
            "stake_value_b": round(YC_STAKE.stake_value_b, 2),
            "return_multiple": round(YC_STAKE.multiple),
            "source": YC_STAKE.source,
        },
        "comparables": [
            {
                "name": c.entity,
                "stake_value_b": round(c.stake_value_b, 3),
                "multiple": round(c.multiple),
            }
            for c in COMPARABLES
        ],
    }
    with open("output.json", "w") as f:
        json.dump(output, f, indent=2)
    print("Structured output written to output.json")


if __name__ == "__main__":
    main()
