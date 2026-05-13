#!/usr/bin/env python3
"""
TDM Messaging Audit — Evaluate product copy through the lens of
Technical Decision Makers who follow analyst trends.

Scores messaging on 5 dimensions and rewrites weak sections.
"""

import sys
import textwrap
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Analyst vocabulary & trend signals
# ---------------------------------------------------------------------------

ANALYST_TERMS = {
    "ai strategy", "cloud-native", "zero trust", "context engine",
    "generative ai", "agentic", "rag", "retrieval-augmented",
    "mlops", "data mesh", "platform engineering", "composable architecture",
    "observability", "ai governance", "responsible ai", "llmops",
    "enterprise-grade", "digital transformation", "multimodal",
    "ai-native", "copilot", "foundation model", "fine-tuning",
}

CAREER_SAFETY_SIGNALS = {
    "trusted by", "fortune 500", "enterprise", "soc 2", "hipaa",
    "gdpr", "iso 27001", "gartner", "forrester", "mckinsey",
    "case study", "customer stories", "logo", "compliance",
    "industry leader", "recognized by", "award", "certified",
}

TREND_ANCHORS = {
    "ai", "artificial intelligence", "machine learning", "cloud",
    "security", "zero trust", "automation", "data-driven",
    "context", "llm", "large language model", "generative",
    "agentic", "agent", "copilot", "platform",
}

JARGON_RED_FLAGS = {
    "blazingly fast", "10x developer", "footgun", "bikeshed",
    "yak shaving", "dogfooding", "neckbeard", "grok",
    "repl-driven", "monad", "functor", "nix flake",
    "lobste.rs", "hacker news", "hn", "sicp",
}


@dataclass
class DimensionScore:
    name: str
    score: int  # 1-5
    evidence: list[str] = field(default_factory=list)
    rewrite: str = ""


@dataclass
class AuditResult:
    product_name: str
    dimensions: list[DimensionScore] = field(default_factory=list)

    @property
    def overall_score(self) -> float:
        if not self.dimensions:
            return 0.0
        return sum(d.score for d in self.dimensions) / len(self.dimensions)


def _count_matches(text: str, terms: set[str]) -> list[str]:
    lower = text.lower()
    return [t for t in terms if t in lower]


def _score_analyst_alignment(text: str) -> DimensionScore:
    matches = _count_matches(text, ANALYST_TERMS)
    if len(matches) >= 5:
        score = 5
    elif len(matches) >= 3:
        score = 4
    elif len(matches) >= 1:
        score = 3
    else:
        score = 1
    return DimensionScore(
        name="Analyst Alignment",
        score=score,
        evidence=matches if matches else ["No analyst-recognized terminology found"],
        rewrite="" if score >= 3 else (
            "Lead with an analyst-recognized category: "
            "\"The [Gartner-recognized category] platform for [outcome].\" "
            "Use terms like 'AI governance', 'platform engineering', or "
            "'composable architecture' that map to published analyst frameworks."
        ),
    )


def _score_career_safety(text: str) -> DimensionScore:
    matches = _count_matches(text, CAREER_SAFETY_SIGNALS)
    if len(matches) >= 5:
        score = 5
    elif len(matches) >= 3:
        score = 4
    elif len(matches) >= 1:
        score = 3
    else:
        score = 1
    return DimensionScore(
        name="Career-Safety Signaling",
        score=score,
        evidence=matches if matches else ["No social proof or compliance signals found"],
        rewrite="" if score >= 3 else (
            "Add trust signals: \"Trusted by [N]+ enterprises\" | "
            "\"SOC 2 Type II certified\" | \"Recognized in [Analyst] report\". "
            "Place enterprise logos above the fold."
        ),
    )


def _score_trend_anchoring(text: str) -> DimensionScore:
    matches = _count_matches(text, TREND_ANCHORS)
    if len(matches) >= 4:
        score = 5
    elif len(matches) >= 2:
        score = 4
    elif len(matches) >= 1:
        score = 3
    else:
        score = 1
    return DimensionScore(
        name="Trend Anchoring",
        score=score,
        evidence=matches if matches else ["No recognized secular trends referenced"],
        rewrite="" if score >= 3 else (
            "Anchor to a secular trend: \"Built for the AI-native enterprise\" "
            "or \"Part of your zero-trust strategy.\" TDMs need a trend label "
            "they can cite in internal memos."
        ),
    )


def _score_jargon_calibration(text: str) -> DimensionScore:
    red_flags = _count_matches(text, JARGON_RED_FLAGS)
    if not red_flags:
        score = 5
    elif len(red_flags) <= 1:
        score = 3
    else:
        score = 1
    return DimensionScore(
        name="Jargon Calibration",
        score=score,
        evidence=[f"Developer jargon detected: {', '.join(red_flags)}"] if red_flags else ["Clean — no insider jargon"],
        rewrite="" if score >= 3 else (
            "Remove developer-culture jargon. Replace 'blazingly fast' with "
            "'high performance'; replace community references with outcome "
            "language a VP of Engineering would use in a board deck."
        ),
    )


def _score_defensibility(text: str) -> DimensionScore:
    """Can a TDM point to this page and say 'this is the right choice'?"""
    safety = _count_matches(text, CAREER_SAFETY_SIGNALS)
    trends = _count_matches(text, TREND_ANCHORS)
    analyst = _count_matches(text, ANALYST_TERMS)
    combined = len(safety) + len(trends) + len(analyst)
    if combined >= 10:
        score = 5
    elif combined >= 6:
        score = 4
    elif combined >= 3:
        score = 3
    elif combined >= 1:
        score = 2
    else:
        score = 1
    return DimensionScore(
        name="Defensibility Framing",
        score=score,
        evidence=[f"Combined defensibility signals: {combined}"],
        rewrite="" if score >= 3 else (
            "Frame purchasing as risk reduction: \"Reduce integration risk with "
            "a proven platform\" or \"Join 500+ teams already in production.\" "
            "Make it easy to copy-paste into a procurement justification."
        ),
    )


def audit_copy(product_name: str, copy_text: str) -> AuditResult:
    result = AuditResult(product_name=product_name)
    result.dimensions = [
        _score_analyst_alignment(copy_text),
        _score_career_safety(copy_text),
        _score_trend_anchoring(copy_text),
        _score_jargon_calibration(copy_text),
        _score_defensibility(copy_text),
    ]
    return result


# ---------------------------------------------------------------------------
# Pretty-print
# ---------------------------------------------------------------------------

def _bar(score: int) -> str:
    filled = "█" * score
    empty = "░" * (5 - score)
    return f"{filled}{empty}"


def print_report(result: AuditResult) -> None:
    print("=" * 68)
    print(f"  TDM MESSAGING AUDIT — {result.product_name}")
    print("=" * 68)
    print()
    print(f"  Overall TDM Resonance Score: {result.overall_score:.1f} / 5.0")
    print()

    # Summary table
    print("  ┌─────────────────────────┬───────┬───────────┐")
    print("  │ Dimension               │ Score │ Visual    │")
    print("  ├─────────────────────────┼───────┼───────────┤")
    for d in result.dimensions:
        name = d.name.ljust(23)
        score_str = str(d.score).center(5)
        bar = _bar(d.score)
        print(f"  │ {name} │ {score_str} │ {bar}     │")
    print("  └─────────────────────────┴───────┴───────────┘")
    print()

    # Detailed breakdown
    for d in result.dimensions:
        icon = "✓" if d.score >= 3 else "✗"
        print(f"  {icon} {d.name} ({d.score}/5)")
        for e in d.evidence:
            print(f"    → {e}")
        if d.rewrite:
            print(f"    ⚡ REWRITE: {d.rewrite}")
        print()

    # Key insight
    print("─" * 68)
    print(textwrap.fill(
        '"The thing about 90% of TDMs is that they\'re motivated primarily '
        'by NOT GETTING FIRED. They follow secular trends supported by '
        'analysts and broad public sentiment." — Mitchell Hashimoto',
        width=66, initial_indent="  ", subsequent_indent="  ",
    ))
    print("─" * 68)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) > 1:
        copy_file = sys.argv[1]
        with open(copy_file) as f:
            copy_text = f.read()
        product_name = sys.argv[2] if len(sys.argv) > 2 else "Product"
    else:
        # Use built-in sample
        from sample_copies import SAMPLES
        for name, text in SAMPLES.items():
            result = audit_copy(name, text)
            print_report(result)
            print("\n")
        return

    result = audit_copy(product_name, copy_text)
    print_report(result)


if __name__ == "__main__":
    main()
