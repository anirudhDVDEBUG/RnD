#!/usr/bin/env python3
"""
Authentic Founder Voice — AI red-flag scanner and rewrite demo.

Scans founder emails for AI-generated patterns and shows before/after rewrites.
No API keys needed — uses regex pattern matching and curated rewrites.
"""

import re
import sys
import textwrap
from samples import SAMPLES

# ---------------------------------------------------------------------------
# Red-flag patterns: (regex, label, category)
# ---------------------------------------------------------------------------
RED_FLAGS = [
    # Corporate filler
    (r"(?i)I hope this (message |email )?finds you well", "corporate filler opener", "filler"),
    (r"(?i)thank you (so much )?for your time( and consideration)?", "gratitude filler", "filler"),
    (r"(?i)I wanted to reach out", "soft opener", "filler"),
    (r"(?i)at your earliest convenience", "formal hedge", "filler"),
    (r"(?i)I would (love|be happy|be delighted|be absolutely delighted) (the opportunity )?to", "over-eager hedge", "filler"),
    (r"(?i)please let me know if you have availability", "scheduling filler", "filler"),
    (r"(?i)looking forward to connecting", "closing filler", "filler"),
    (r"(?i)warm(est)? regards", "formal sign-off", "filler"),
    (r"(?i)with gratitude", "formal sign-off", "filler"),
    (r"(?i)dear (valued |esteemed )?investors?", "formal address", "filler"),
    (r"(?i)I truly appreciate", "over-earnest filler", "filler"),
    (r"(?i)I'm (incredibly |extremely )?grateful", "over-earnest filler", "filler"),

    # Superlatives
    (r"(?i)\brevolutionary\b", "superlative", "superlative"),
    (r"(?i)\bgroundbreaking\b", "superlative", "superlative"),
    (r"(?i)\bgame[- ]changing\b", "superlative", "superlative"),
    (r"(?i)\bunprecedented\b", "superlative", "superlative"),
    (r"(?i)\btransformative\b", "superlative", "superlative"),
    (r"(?i)\binnovative\b", "superlative", "superlative"),
    (r"(?i)\bcutting[- ]edge\b", "superlative", "superlative"),
    (r"(?i)\bworld[- ]class\b", "superlative", "superlative"),
    (r"(?i)\bbest[- ]in[- ]class\b", "superlative", "superlative"),
    (r"(?i)\bstate[- ]of[- ]the[- ]art\b", "superlative", "superlative"),
    (r"(?i)\bbreakthrough\b", "superlative", "superlative"),
    (r"(?i)\bimpressive\b", "superlative", "superlative"),
    (r"(?i)\btremendous\b", "superlative", "superlative"),
    (r"(?i)\bincredible\b", "superlative", "superlative"),
    (r"(?i)\bremarkable\b", "superlative", "superlative"),

    # AI cliches
    (r"(?i)at the intersection of", "AI cliche", "cliche"),
    (r"(?i)\bleverag(e|es|ing)\b", "AI cliche", "cliche"),
    (r"(?i)\bsynerg(y|ies)\b", "AI cliche", "cliche"),
    (r"(?i)\bempower(s|ing|ed)?\b", "AI cliche", "cliche"),
    (r"(?i)poised to disrupt", "AI cliche", "cliche"),
    (r"(?i)reimagining the future", "AI cliche", "cliche"),
    (r"(?i)unlock(ing)? .{0,20}value", "AI cliche", "cliche"),
    (r"(?i)on a mission to", "AI cliche", "cliche"),
    (r"(?i)democratize access", "AI cliche", "cliche"),
    (r"(?i)laser[- ]focused", "AI cliche", "cliche"),
    (r"(?i)what (truly |really )?sets us apart", "AI cliche", "cliche"),
    (r"(?i)the definitive leader", "AI cliche", "cliche"),
    (r"(?i)unparalleled", "AI cliche", "cliche"),
    (r"(?i)next generation of", "AI cliche", "cliche"),
    (r"(?i)deep[- ]dive", "AI cliche", "cliche"),

    # Empty rhetoric
    (r"(?i)the results speak for themselves", "empty rhetoric", "rhetoric"),
    (r"(?i)working tirelessly", "empty rhetoric", "rhetoric"),
    (r"(?i)ambitious roadmap", "empty rhetoric", "rhetoric"),
    (r"(?i)overwhelmingly positive", "empty rhetoric", "rhetoric"),
    (r"(?i)significant interest", "vague claim", "rhetoric"),
    (r"(?i)across multiple verticals", "vague scope", "rhetoric"),
    (r"(?i)what truly matters", "empty rhetoric", "rhetoric"),
    (r"(?i)lasting value", "empty rhetoric", "rhetoric"),
    (r"(?i)on the horizon", "empty rhetoric", "rhetoric"),
    (r"(?i)garnered", "over-formal verb", "rhetoric"),
    (r"(?i)humbled by", "false modesty", "rhetoric"),
    (r"(?i)comprehensive (strategic )?plan", "vague scope", "rhetoric"),
]


def scan(text: str) -> list[dict]:
    """Scan text for AI red flags. Returns list of {pattern, label, category, match}."""
    findings = []
    seen = set()
    for pattern, label, category in RED_FLAGS:
        for m in re.finditer(pattern, text):
            key = (label, m.group())
            if key not in seen:
                seen.add(key)
                findings.append({
                    "pattern": pattern,
                    "label": label,
                    "category": category,
                    "match": m.group(),
                })
    return findings


def score(findings: list[dict]) -> str:
    """Return a letter grade based on number of flags."""
    n = len(findings)
    if n == 0:
        return "A"
    elif n <= 2:
        return "B"
    elif n <= 5:
        return "C"
    elif n <= 10:
        return "D"
    else:
        return "F"


def format_findings(findings: list[dict]) -> str:
    """Pretty-print red flag findings."""
    if not findings:
        return "  (none found)"
    lines = []
    by_cat = {}
    for f in findings:
        by_cat.setdefault(f["category"], []).append(f)
    cat_labels = {"filler": "Corporate Filler", "superlative": "Superlatives",
                  "cliche": "AI Cliches", "rhetoric": "Empty Rhetoric"}
    for cat in ["filler", "superlative", "cliche", "rhetoric"]:
        items = by_cat.get(cat, [])
        if items:
            lines.append(f"  [{cat_labels[cat]}]")
            for f in items:
                lines.append(f'    - "{f["match"]}" ({f["label"]})')
    return "\n".join(lines)


def wrap(text: str, width: int = 72, indent: str = "  ") -> str:
    """Wrap and indent text for display."""
    paragraphs = text.split("\n\n")
    wrapped = []
    for p in paragraphs:
        lines = p.split("\n")
        for line in lines:
            if line.strip().startswith("- "):
                wrapped.append(indent + line.strip())
            else:
                wrapped.append(textwrap.fill(line.strip(), width=width,
                                             initial_indent=indent,
                                             subsequent_indent=indent))
    return "\n".join(wrapped)


def main():
    print("=" * 72)
    print("  AUTHENTIC FOUNDER VOICE — AI Red Flag Scanner")
    print("  Inspired by Paul Graham: 'AI-written emails are immediately obvious'")
    print("=" * 72)

    total_flags = 0

    for i, sample in enumerate(SAMPLES, 1):
        print(f"\n{'─' * 72}")
        print(f"  SAMPLE {i}: {sample['label']}")
        print(f"{'─' * 72}")

        # Show original
        print("\n  ORIGINAL (AI-polished):")
        print(wrap(sample["text"]))

        # Scan
        findings = scan(sample["text"])
        total_flags += len(findings)
        grade = score(findings)

        print(f"\n  RED FLAGS ({len(findings)} found, grade: {grade}):")
        print(format_findings(findings))

        # Show rewrite
        print("\n  REWRITTEN (authentic founder voice):")
        print(wrap(sample["rewrite"]))

    # Summary
    print(f"\n{'=' * 72}")
    print(f"  SUMMARY")
    print(f"{'=' * 72}")
    print(f"  Emails scanned:    {len(SAMPLES)}")
    print(f"  Total red flags:   {total_flags}")
    print(f"  Avg flags/email:   {total_flags / len(SAMPLES):.1f}")
    print(f"  Pattern database:  {len(RED_FLAGS)} detection rules")
    print()
    print("  The Paul Graham test: 'Would the reader suspect AI wrote this?'")
    print("  If yes — rewrite until the answer is no.")
    print()
    print("  Install the skill:  cp SKILL.md ~/.claude/skills/authentic_founder_voice/")
    print("  Then ask Claude:    'Review my pitch email — does it sound AI-generated?'")
    print(f"{'=' * 72}")


if __name__ == "__main__":
    main()
