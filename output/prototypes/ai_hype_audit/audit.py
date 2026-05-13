"""
AI Hype Audit — Analyze AI proposals/memos for substance vs. hype.

Scores text across 5 dimensions and produces a structured verdict.
"""

import re
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Tuple

# Buzzword patterns: phrases that sound impressive but say nothing concrete
BUZZWORDS = [
    r"paradigm.?shift", r"game.?chang", r"revolutioniz", r"transform(?:ative|ing)",
    r"next.?gen(?:eration)?", r"bleeding.?edge", r"cutting.?edge", r"best.?in.?class",
    r"world.?class", r"synerg", r"leverage\s+(?:ai|ml|llm)", r"ai.?first",
    r"ai.?native", r"ai.?powered", r"intelligent\s+automation", r"cognitive",
    r"hyper.?automat", r"autonomous\s+(?:agent|system)", r"agentic",
    r"end.?to.?end\s+ai", r"full.?stack\s+ai", r"self.?healing",
    r"zero.?touch", r"turnkey\s+ai", r"democratiz", r"unlock(?:ing)?\s+value",
    r"10x", r"100x", r"exponential", r"moonshot", r"north\s+star",
    r"force\s+multiplier", r"supercharg", r"turbo.?charg",
    r"could\s+change\s+(?:literally\s+)?everything", r"disrupt",
    r"magic(?:al)?", r"silver\s+bullet", r"no.?brainer",
]

# Specificity indicators: signs the text has concrete details
SPECIFICITY_MARKERS = [
    r"\d+%", r"\$[\d,]+", r"\d+\s*(?:hours?|days?|weeks?|months?)",
    r"(?:reduce|increase|improve)\s+\w+\s+by\s+\d+",
    r"pilot\s+(?:with|phase|scope)", r"success\s+(?:metric|criteria|kpi)",
    r"fallback", r"rollback", r"error\s+rate", r"accuracy\s+of\s+\d+",
    r"api\s+cost", r"latency", r"p\d{2}", r"baseline",
    r"a/b\s+test", r"control\s+group", r"measured\s+by",
]

# Red flags for human impact issues
HUMAN_IMPACT_FLAGS = [
    r"replac(?:e|ing)\s+(?:\w+\s+)?(?:team|staff|role|position|employee)",
    r"automat(?:e|ing)\s+(?:\w+\s+)?(?:away|out)",
    r"(?:no|don.?t)\s+need\s+(?:\w+\s+)?(?:humans?|people|staff)",
    r"headcount\s+reduction", r"rif\b", r"redundan",
    r"ralph\s+loop",  # from the source material
]


@dataclass
class AuditFlag:
    phrase: str
    category: str  # buzzword, vague_claim, human_impact, no_roi
    explanation: str
    suggested_rewrite: str = ""


@dataclass
class AuditResult:
    substance_score: int  # 1-10
    buzzword_density: float  # 0-1
    specificity_score: float  # 0-1
    feasibility_score: float  # 0-1
    roi_grounding: float  # 0-1
    human_impact_honesty: float  # 0-1
    flags: List[AuditFlag] = field(default_factory=list)
    verdict: str = ""  # Ship It, Needs Work, Career Theater


def find_matches(text: str, patterns: list) -> List[Tuple[str, str]]:
    """Find all pattern matches with their surrounding context."""
    matches = []
    for pattern in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            start = max(0, m.start() - 20)
            end = min(len(text), m.end() + 20)
            context = text[start:end].strip()
            matches.append((m.group(), context))
    return matches


def score_buzzword_density(text: str) -> Tuple[float, List[AuditFlag]]:
    """Score buzzword density (0=none, 1=all buzzwords)."""
    words = text.split()
    if not words:
        return 0.0, []

    matches = find_matches(text, BUZZWORDS)
    density = min(1.0, len(matches) / max(1, len(words) / 20))

    flags = []
    for match_text, context in matches[:10]:  # cap at 10 flags
        flags.append(AuditFlag(
            phrase=context,
            category="buzzword",
            explanation=f'"{match_text}" is a buzzword that adds no technical specificity.',
            suggested_rewrite=f"Replace with a concrete metric or specific technical description."
        ))
    return density, flags


def score_specificity(text: str) -> float:
    """Score how specific the text is (0=vague, 1=highly specific)."""
    words = text.split()
    if not words:
        return 0.0
    matches = find_matches(text, SPECIFICITY_MARKERS)
    return min(1.0, len(matches) / max(1, len(words) / 50))


def score_feasibility(text: str) -> Tuple[float, List[AuditFlag]]:
    """Check if automation claims are feasible with current AI."""
    flags = []
    infeasible_patterns = [
        (r"fully\s+automat(?:e|ed|ing)\s+(?:all|every|entire)", "Full automation of complex workflows is rarely achievable — specify which subtasks are automated."),
        (r"(?:100|near.?100)%\s+(?:accuracy|automat)", "100% accuracy/automation claims are unrealistic — specify expected error rates."),
        (r"replace\s+(?:all|entire)\s+(?:team|department|workflow)", "Wholesale replacement claims ignore integration complexity and edge cases."),
        (r"no\s+human\s+(?:intervention|oversight|review)\s+(?:needed|required)", "Removing all human oversight is a red flag — specify the review cadence."),
    ]

    score = 0.8  # start optimistic
    for pattern, explanation in infeasible_patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            score -= 0.2
            start = max(0, m.start() - 15)
            end = min(len(text), m.end() + 15)
            flags.append(AuditFlag(
                phrase=text[start:end].strip(),
                category="vague_claim",
                explanation=explanation,
                suggested_rewrite="Add scope limits, error rates, and human review checkpoints."
            ))
    return max(0.0, score), flags


def score_roi_grounding(text: str) -> float:
    """Check if costs and ROI are addressed."""
    roi_patterns = [
        r"cost\s+(?:of|per|estimate)", r"budget", r"roi\b", r"break.?even",
        r"api\s+(?:cost|credit|spend)", r"engineering\s+(?:time|hours|effort)",
        r"integration\s+(?:cost|effort|time)", r"total\s+cost",
        r"savings\s+of\s+\$?\d+",
    ]
    matches = find_matches(text, roi_patterns)
    return min(1.0, len(matches) / 3)


def score_human_impact(text: str) -> Tuple[float, List[AuditFlag]]:
    """Check if human/workforce impact is handled responsibly."""
    flags = []
    matches = find_matches(text, HUMAN_IMPACT_FLAGS)

    # Good patterns (responsible handling)
    good_patterns = [
        r"upskill", r"retrain", r"transition\s+plan", r"augment(?:ing|ation)?",
        r"human.?in.?the.?loop", r"assist(?:ing|ance)", r"support(?:ing)?\s+(?:team|staff)",
    ]
    good_matches = find_matches(text, good_patterns)

    if matches and not good_matches:
        for match_text, context in matches[:5]:
            flags.append(AuditFlag(
                phrase=context,
                category="human_impact",
                explanation="Mentions workforce displacement without addressing transition, retraining, or augmentation.",
                suggested_rewrite="Add a transition plan: who is affected, what retraining is offered, what new roles are created."
            ))
        return 0.2, flags
    elif matches and good_matches:
        return 0.7, flags
    elif not matches:
        return 0.8, flags  # neutral — doesn't discuss it
    return 0.5, flags


def audit(text: str) -> AuditResult:
    """Run the full AI hype audit on the provided text."""
    buzzword_density, buzz_flags = score_buzzword_density(text)
    specificity = score_specificity(text)
    feasibility, feas_flags = score_feasibility(text)
    roi = score_roi_grounding(text)
    human_impact, human_flags = score_human_impact(text)

    all_flags = buzz_flags + feas_flags + human_flags

    # Compute substance score (1-10)
    raw = (
        (1 - buzzword_density) * 0.25 +
        specificity * 0.25 +
        feasibility * 0.20 +
        roi * 0.15 +
        human_impact * 0.15
    )
    substance_score = max(1, min(10, round(raw * 10)))

    # Determine verdict
    if substance_score >= 7:
        verdict = "Ship It"
    elif substance_score >= 4:
        verdict = "Needs Work"
    else:
        verdict = "Career Theater"

    return AuditResult(
        substance_score=substance_score,
        buzzword_density=round(buzzword_density, 2),
        specificity_score=round(specificity, 2),
        feasibility_score=round(feasibility, 2),
        roi_grounding=round(roi, 2),
        human_impact_honesty=round(human_impact, 2),
        flags=all_flags,
        verdict=verdict,
    )


def format_report(result: AuditResult) -> str:
    """Format the audit result as a readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  AI HYPE AUDIT REPORT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  SUBSTANCE SCORE: {result.substance_score}/10")
    lines.append(f"  VERDICT: {result.verdict}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  DIMENSION SCORES")
    lines.append("-" * 60)
    lines.append(f"  Buzzword Density:      {result.buzzword_density:.0%} (lower is better)")
    lines.append(f"  Specificity:           {result.specificity_score:.0%}")
    lines.append(f"  Feasibility:           {result.feasibility_score:.0%}")
    lines.append(f"  ROI Grounding:         {result.roi_grounding:.0%}")
    lines.append(f"  Human Impact Honesty:  {result.human_impact_honesty:.0%}")
    lines.append("")

    if result.flags:
        lines.append("-" * 60)
        lines.append("  FLAGGED PHRASES")
        lines.append("-" * 60)
        for i, flag in enumerate(result.flags, 1):
            lines.append(f"")
            lines.append(f"  [{i}] ({flag.category.upper()})")
            lines.append(f"      \"{flag.phrase}\"")
            lines.append(f"      -> {flag.explanation}")
            if flag.suggested_rewrite:
                lines.append(f"      FIX: {flag.suggested_rewrite}")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    """Run audit on stdin or provided file."""
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    result = audit(text)
    print(format_report(result))
    print()
    print("JSON output:")
    print(json.dumps({
        "substance_score": result.substance_score,
        "verdict": result.verdict,
        "buzzword_density": result.buzzword_density,
        "specificity_score": result.specificity_score,
        "feasibility_score": result.feasibility_score,
        "roi_grounding": result.roi_grounding,
        "human_impact_honesty": result.human_impact_honesty,
        "flags_count": len(result.flags),
    }, indent=2))


if __name__ == "__main__":
    main()
