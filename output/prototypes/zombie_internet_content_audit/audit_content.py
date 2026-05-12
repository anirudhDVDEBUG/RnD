#!/usr/bin/env python3
"""
Zombie Internet Content Audit

Scans text for hallmarks of AI-generated writing ("slop") and zombie internet
patterns. Based on the framework described by Jason Koebler (404 Media) and
highlighted by Simon Willison.

Usage:
    python audit_content.py <file_or_text>
    python audit_content.py --dir <directory>
    echo "some text" | python audit_content.py --stdin
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Signal definitions
# ---------------------------------------------------------------------------

LEXICAL_TELLS = {
    # word/phrase -> weight (higher = stronger signal)
    "delve": 3,
    "delves": 3,
    "delving": 3,
    "landscape": 2,
    "arguably": 2,
    "it's important to note": 3,
    "it is important to note": 3,
    "game-changer": 3,
    "game changer": 3,
    "in today's fast-paced world": 4,
    "in today's rapidly evolving": 4,
    "comprehensive": 2,
    "cutting-edge": 2,
    "cutting edge": 2,
    "straightforward": 1,
    "i'd be happy to": 3,
    "great question": 3,
    "let's dive in": 3,
    "dive into": 2,
    "elevate": 2,
    "leverage": 2,
    "harness the power": 3,
    "unlock the potential": 3,
    "navigate the complexities": 3,
    "ever-evolving": 3,
    "in conclusion": 1,
    "in summary": 1,
    "furthermore": 1,
    "moreover": 1,
    "realm": 2,
    "tapestry": 3,
    "multifaceted": 3,
    "nuanced": 2,
    "robust": 2,
    "seamless": 2,
    "seamlessly": 2,
    "pivotal": 2,
    "embark": 3,
    "embark on a journey": 4,
    "foster": 2,
    "underscores": 2,
    "underscoring": 2,
    "not only...but also": 2,
    "stands as a testament": 4,
    "serves as a reminder": 3,
    "whether you're a seasoned": 4,
    "in the ever-changing": 3,
    "it's worth noting": 2,
    "at the end of the day": 2,
    "transformative": 2,
    "revolutionize": 2,
    "paradigm": 2,
    "synergy": 2,
    "ecosystem": 1,
    "holistic": 2,
    "streamline": 2,
}

STRUCTURAL_PATTERNS = [
    {
        "name": "Listicle padding",
        "pattern": r"(?:^|\n)\s*\d+\.\s+\*\*[^*]+\*\*",
        "weight": 2,
        "description": "Numbered list with bold headings (listicle-style padding)",
    },
    {
        "name": "Uniform paragraph length",
        "check": "paragraph_uniformity",
        "weight": 2,
        "description": "Paragraphs suspiciously similar in length",
    },
    {
        "name": "Formulaic intro-body-conclusion",
        "pattern": r"(?i)^.{0,200}(in this article|in this post|in this guide|let'?s explore|we'?ll explore|we will explore)",
        "weight": 2,
        "description": "Formulaic introduction promising to explore a topic",
    },
    {
        "name": "Excessive hedging",
        "pattern": r"(?i)\b(may|might|could|potentially|arguably|perhaps)\b",
        "weight": 0.3,  # low per-hit, but accumulates
        "threshold": 8,
        "description": "Excessive hedging language",
    },
    {
        "name": "Hollow superlatives",
        "pattern": r"(?i)\b(incredible|amazing|remarkable|extraordinary|unparalleled|unprecedented)\b",
        "weight": 1,
        "description": "Hollow superlatives without substantiation",
    },
    {
        "name": "Emoji bullet lists",
        "pattern": r"(?:^|\n)\s*[^\w\s]\s+\w",
        "weight": 1,
        "description": "Emoji-prefixed bullet points",
    },
]

ZOMBIE_PATTERNS = [
    {
        "name": "Engagement bait",
        "pattern": r"(?i)(what do you think\?|share your thoughts|let me know in the comments|drop a comment|agree\?|thoughts\?$)",
        "weight": 2,
        "description": "Engagement-bait phrasing",
    },
    {
        "name": "Generic authority appeal",
        "pattern": r"(?i)(experts? (say|agree|suggest|recommend|believe)|according to (studies|research|experts|scientists))",
        "weight": 2,
        "description": "Vague appeals to unnamed experts or studies",
    },
    {
        "name": "SEO keyword stuffing",
        "check": "keyword_density",
        "weight": 2,
        "description": "Suspiciously high repetition of key phrases (SEO stuffing)",
    },
    {
        "name": "Hustlebro framing",
        "pattern": r"(?i)(passive income|side hustle|financial freedom|6[- ]figure|7[- ]figure|scale your|grow your business|monetize)",
        "weight": 2,
        "description": "Hustlebro/influencer framing language",
    },
]


# ---------------------------------------------------------------------------
# Analysis engine
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    category: str  # lexical | structural | zombie
    signal_name: str
    description: str
    weight: float
    matches: list = field(default_factory=list)
    line_refs: list = field(default_factory=list)


@dataclass
class AuditResult:
    source: str
    total_words: int
    total_score: float
    confidence: str  # low / medium / high
    classification: str
    findings: list = field(default_factory=list)
    summary: str = ""


def _lines_for_match(text: str, span_start: int) -> int:
    """Return 1-based line number for a character offset."""
    return text[:span_start].count("\n") + 1


def _check_paragraph_uniformity(text: str) -> Optional[Finding]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) < 4:
        return None
    lengths = [len(p) for p in paragraphs]
    avg = sum(lengths) / len(lengths)
    if avg == 0:
        return None
    deviations = [abs(l - avg) / avg for l in lengths]
    mean_dev = sum(deviations) / len(deviations)
    if mean_dev < 0.15:  # very uniform
        return Finding(
            category="structural",
            signal_name="Uniform paragraph length",
            description=f"Paragraphs are suspiciously uniform in length (mean deviation {mean_dev:.0%} from average {avg:.0f} chars)",
            weight=2,
            matches=[f"avg={avg:.0f} chars, deviation={mean_dev:.0%}"],
        )
    return None


def _check_keyword_density(text: str) -> Optional[Finding]:
    words = text.lower().split()
    if len(words) < 50:
        return None
    # Find 2-grams and 3-grams
    ngrams = {}
    for n in (2, 3):
        for i in range(len(words) - n + 1):
            gram = " ".join(words[i : i + n])
            if len(gram) > 6:
                ngrams[gram] = ngrams.get(gram, 0) + 1
    # Flag any ngram appearing > 1% of word count and at least 4 times
    threshold = max(4, len(words) * 0.01)
    stuffed = {k: v for k, v in ngrams.items() if v >= threshold}
    if stuffed:
        top = sorted(stuffed.items(), key=lambda x: -x[1])[:5]
        return Finding(
            category="zombie",
            signal_name="SEO keyword stuffing",
            description="Suspiciously high repetition of key phrases",
            weight=2,
            matches=[f'"{k}" x{v}' for k, v in top],
        )
    return None


def audit(text: str, source: str = "<stdin>") -> AuditResult:
    """Run the full audit pipeline on a piece of text."""
    findings: list[Finding] = []
    word_count = len(text.split())

    # --- Lexical tells ---
    for phrase, weight in LEXICAL_TELLS.items():
        pattern = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
        hits = list(pattern.finditer(text))
        if hits:
            lines = [_lines_for_match(text, m.start()) for m in hits]
            findings.append(Finding(
                category="lexical",
                signal_name=f'"{phrase}"',
                description=f"AI-associated phrase found {len(hits)} time(s)",
                weight=weight * len(hits),
                matches=[m.group() for m in hits],
                line_refs=lines,
            ))

    # --- Structural tells ---
    for sp in STRUCTURAL_PATTERNS:
        if "check" in sp:
            if sp["check"] == "paragraph_uniformity":
                f = _check_paragraph_uniformity(text)
                if f:
                    findings.append(f)
            continue
        pattern = re.compile(sp["pattern"], re.MULTILINE)
        hits = list(pattern.finditer(text))
        threshold = sp.get("threshold", 1)
        if len(hits) >= threshold:
            lines = [_lines_for_match(text, m.start()) for m in hits]
            effective_weight = sp["weight"] * min(len(hits), 10)
            findings.append(Finding(
                category="structural",
                signal_name=sp["name"],
                description=sp["description"],
                weight=effective_weight,
                matches=[m.group().strip()[:80] for m in hits[:5]],
                line_refs=lines[:5],
            ))

    # --- Zombie internet patterns ---
    for zp in ZOMBIE_PATTERNS:
        if "check" in zp:
            if zp["check"] == "keyword_density":
                f = _check_keyword_density(text)
                if f:
                    findings.append(f)
            continue
        pattern = re.compile(zp["pattern"], re.MULTILINE)
        hits = list(pattern.finditer(text))
        if hits:
            lines = [_lines_for_match(text, m.start()) for m in hits]
            findings.append(Finding(
                category="zombie",
                signal_name=zp["name"],
                description=zp["description"],
                weight=zp["weight"] * len(hits),
                matches=[m.group().strip()[:80] for m in hits[:5]],
                line_refs=lines[:5],
            ))

    # --- Score and classify ---
    total_score = sum(f.weight for f in findings)

    # Normalize by text length (short texts get less penalized)
    length_factor = min(1.0, word_count / 300)
    adjusted_score = total_score * length_factor

    if adjusted_score < 5:
        confidence = "low"
    elif adjusted_score < 15:
        confidence = "medium"
    else:
        confidence = "high"

    # Classification
    lexical_score = sum(f.weight for f in findings if f.category == "lexical")
    structural_score = sum(f.weight for f in findings if f.category == "structural")
    zombie_score = sum(f.weight for f in findings if f.category == "zombie")

    if confidence == "low":
        classification = "Likely authentic human writing"
    elif zombie_score > lexical_score and zombie_score > structural_score:
        classification = "AI-augmented human writing with zombie internet patterns"
    elif structural_score > lexical_score:
        classification = "Human-edited AI draft"
    else:
        classification = "Pure bot output / unedited AI generation"

    # Summary
    top_findings = sorted(findings, key=lambda f: -f.weight)[:5]
    summary_parts = []
    for f in top_findings:
        refs = f", lines {f.line_refs[:3]}" if f.line_refs else ""
        summary_parts.append(f"  - [{f.category.upper()}] {f.signal_name}: {f.description} (weight={f.weight:.1f}{refs})")

    summary = "\n".join(summary_parts) if summary_parts else "  No significant AI-generation signals detected."

    return AuditResult(
        source=source,
        total_words=word_count,
        total_score=round(total_score, 1),
        confidence=confidence,
        classification=classification,
        findings=findings,
        summary=summary,
    )


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_report(result: AuditResult, fmt: str = "text") -> str:
    if fmt == "json":
        d = asdict(result)
        return json.dumps(d, indent=2)

    lines = []
    lines.append("=" * 70)
    lines.append(f"ZOMBIE INTERNET CONTENT AUDIT")
    lines.append(f"Source: {result.source}")
    lines.append(f"Words: {result.total_words}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  Confidence:     {result.confidence.upper()}")
    lines.append(f"  Score:          {result.total_score}")
    lines.append(f"  Classification: {result.classification}")
    lines.append("")
    lines.append("-" * 70)
    lines.append("TOP SIGNALS:")
    lines.append(result.summary)
    lines.append("-" * 70)

    if result.findings:
        # Breakdown by category
        for cat in ("lexical", "structural", "zombie"):
            cat_findings = [f for f in result.findings if f.category == cat]
            if cat_findings:
                lines.append(f"\n{cat.upper()} SIGNALS ({len(cat_findings)}):")
                for f in sorted(cat_findings, key=lambda x: -x.weight):
                    refs = ""
                    if f.line_refs:
                        refs = f" [lines: {', '.join(str(l) for l in f.line_refs[:5])}]"
                    lines.append(f"  {f.signal_name}: {f.description}{refs}")
                    if f.matches:
                        for m in f.matches[:3]:
                            lines.append(f"    -> {m}")

    lines.append("")
    lines.append("=" * 70)
    lines.append("NOTE: No detector is 100% accurate. This identifies patterns")
    lines.append("consistent with AI generation, not proof. Always pair with")
    lines.append("human judgment.")
    lines.append("=" * 70)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Audit content for AI-generated slop and zombie internet patterns"
    )
    parser.add_argument("input", nargs="?", help="File path or text to audit")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--dir", help="Audit all .txt/.md files in a directory")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    results = []

    if args.stdin or (not args.input and not args.dir and not sys.stdin.isatty()):
        text = sys.stdin.read()
        results.append(audit(text, source="<stdin>"))
    elif args.dir:
        p = Path(args.dir)
        for f in sorted(p.glob("**/*")):
            if f.suffix in (".txt", ".md") and f.is_file():
                text = f.read_text(errors="replace")
                results.append(audit(text, source=str(f)))
    elif args.input:
        p = Path(args.input)
        if p.is_file():
            text = p.read_text(errors="replace")
            results.append(audit(text, source=str(p)))
        else:
            # Treat as inline text
            results.append(audit(args.input, source="<inline>"))
    else:
        parser.print_help()
        sys.exit(1)

    for r in results:
        print(format_report(r, fmt=args.format))
        print()


if __name__ == "__main__":
    main()
