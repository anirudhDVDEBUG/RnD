#!/usr/bin/env python3
"""
unslop.py — Remove AI-generated slop from text.

Detects and removes overused filler words, cliched phrases, hollow transitions,
and sycophantic openers that make writing sound machine-generated.

Based on patterns from https://github.com/MohamedAbdallah-14/unslop
"""

import re
import sys
import json
from dataclasses import dataclass, field


# ── Slop dictionaries ──────────────────────────────────────────────────────

FILLER_ADVERBS = [
    "seamlessly", "arguably", "notably", "importantly", "crucially",
    "frankly", "undeniably", "essentially", "fundamentally", "ultimately",
    "remarkably", "incredibly", "moreover", "furthermore", "additionally",
    "consequently", "subsequently", "accordingly", "nevertheless",
    "nonetheless", "straightforwardly",
]

HOLLOW_ADJECTIVES = [
    "groundbreaking", "game-changing", "cutting-edge", "revolutionary",
    "transformative", "innovative", "world-class", "best-in-class",
    "state-of-the-art", "next-generation", "holistic", "robust", "scalable",
    "synergistic", "unparalleled", "unprecedented", "pivotal",
    "invaluable", "indispensable", "comprehensive", "meticulous",
]

# Phrases to delete entirely (case-insensitive)
DELETE_PHRASES = [
    r"it'?s worth noting that\s*",
    r"it'?s important to note that\s*",
    r"in today'?s (?:rapidly evolving|fast-paced|digital) landscape[,.]?\s*",
    r"let'?s dive (?:in|deep)\s*",
    r"let'?s unpack\s*",
    r"at the end of the day[,.]?\s*",
    r"this is where \w+ comes in[.]?\s*",
    r"the beauty of [\w\s]+ is (?:that )?",
    r"think of it as\s*",
    r"here'?s the (?:thing|kicker):\s*",
    r"take it to the next level\s*",
    r"by the same token[,.]?\s*",
    r"in a nutshell[,.]?\s*",
    r"at its core[,.]?\s*",
    r"the landscape of \w+\s*",
    r"navigate the landscape\s*",
    r"unlock the (?:power|potential) of\s*",
    r"delve (?:into|deeper)\s*",
    r"in the realm of\s*",
    r"rich tapestry\s*",
    r"embark on a journey\s*",
    r"foster (?:innovation|growth|collaboration)\s*",
    r"it'?s not just about [\w\s]+—\s*it'?s about\s*",
    r"imagine a world where\s*",
    r"in an era where\s*",
    r"peeling back the layers\s*",
    r"the secret sauce\s*",
    # Sycophantic openers
    r"great question!?\s*",
    r"that'?s a really interesting point[.!]?\s*",
    r"absolutely!?\s*",
    r"what a fantastic[\w\s]*[.!]?\s*",
    # Hollow conclusions
    r"in conclusion[,.]?\s*",
    r"to sum up[,.]?\s*",
    r"to summarize[,.]?\s*",
    r"as we'?ve seen[,.]?\s*",
]

# Simple word → replacement mapping
WORD_REPLACEMENTS = {
    "leverage": "use",
    "leveraging": "using",
    "leveraged": "used",
    "utilize": "use",
    "utilizing": "using",
    "utilized": "used",
    "utilization": "use",
    "empower": "help",
    "empowering": "helping",
    "empowered": "helped",
    "revolutionize": "improve",
    "revolutionizing": "improving",
    "revolutionized": "improved",
    "delve": "look",
    "realm": "area",
    "tapestry": "mix",
    "landscape": "field",
}


@dataclass
class SlopMatch:
    """A single detected slop instance."""
    category: str
    original: str
    replacement: str  # empty string means "delete"
    start: int
    end: int


@dataclass
class UnslopResult:
    """Result of running unslop on text."""
    original: str
    cleaned: str
    matches: list[SlopMatch] = field(default_factory=list)

    @property
    def slop_count(self) -> int:
        return len(self.matches)

    @property
    def reduction_pct(self) -> float:
        if not self.original:
            return 0.0
        return (1 - len(self.cleaned) / len(self.original)) * 100


def unslop(text: str, *, verbose: bool = False) -> UnslopResult:
    """Remove AI slop from text. Returns UnslopResult with cleaned text and match details."""
    matches: list[SlopMatch] = []
    cleaned = text

    # Pass 1: Delete cliched phrases
    for pattern in DELETE_PHRASES:
        for m in re.finditer(pattern, cleaned, re.IGNORECASE):
            matches.append(SlopMatch(
                category="cliched_phrase",
                original=m.group(),
                replacement="",
                start=m.start(),
                end=m.end(),
            ))
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Pass 2: Remove filler adverbs (standalone, with optional comma)
    for word in FILLER_ADVERBS:
        # Match word at sentence start with comma, or mid-sentence
        pat_start = re.compile(rf"\b{word},?\s+", re.IGNORECASE)
        for m in pat_start.finditer(cleaned):
            matches.append(SlopMatch(
                category="filler_adverb",
                original=m.group().strip(),
                replacement="",
                start=m.start(),
                end=m.end(),
            ))
        cleaned = pat_start.sub("", cleaned)

    # Pass 3: Flag hollow adjectives (remove standalone, keep if part of compound)
    for word in HOLLOW_ADJECTIVES:
        pat = re.compile(rf"\b{word}\b\s*", re.IGNORECASE)
        for m in pat.finditer(cleaned):
            matches.append(SlopMatch(
                category="hollow_adjective",
                original=m.group().strip(),
                replacement="",
                start=m.start(),
                end=m.end(),
            ))
        cleaned = pat.sub("", cleaned)

    # Pass 4: Word replacements
    for old, new in WORD_REPLACEMENTS.items():
        pat = re.compile(rf"\b{old}\b", re.IGNORECASE)
        for m in pat.finditer(cleaned):
            # Preserve original casing for first letter
            repl = new
            if m.group()[0].isupper():
                repl = new[0].upper() + new[1:]
            matches.append(SlopMatch(
                category="word_replacement",
                original=m.group(),
                replacement=repl,
                start=m.start(),
                end=m.end(),
            ))
        def _replace(m, new=new):
            repl = new
            if m.group()[0].isupper():
                repl = new[0].upper() + new[1:]
            return repl
        cleaned = pat.sub(_replace, cleaned)

    # Cleanup: collapse multiple spaces, fix orphan punctuation
    cleaned = re.sub(r"  +", " ", cleaned)
    cleaned = re.sub(r" ,", ",", cleaned)
    cleaned = re.sub(r"\n ", "\n", cleaned)
    cleaned = re.sub(r"^\s+", "", cleaned, flags=re.MULTILINE)

    return UnslopResult(original=text, cleaned=cleaned, matches=matches)


def format_report(result: UnslopResult) -> str:
    """Format a human-readable report of slop removal."""
    lines = []
    lines.append(f"Slop instances found: {result.slop_count}")
    lines.append(f"Text reduced by: {result.reduction_pct:.1f}%")
    lines.append("")

    if result.matches:
        by_cat: dict[str, list[SlopMatch]] = {}
        for m in result.matches:
            by_cat.setdefault(m.category, []).append(m)

        for cat, items in by_cat.items():
            label = cat.replace("_", " ").title()
            lines.append(f"  [{label}] ({len(items)} found)")
            for item in items[:10]:  # cap display
                orig = item.original.strip()
                if item.replacement:
                    lines.append(f"    - \"{orig}\" -> \"{item.replacement}\"")
                else:
                    lines.append(f"    - \"{orig}\" (removed)")
            if len(items) > 10:
                lines.append(f"    ... and {len(items) - 10} more")
            lines.append("")

    lines.append("--- CLEANED TEXT ---")
    lines.append(result.cleaned)
    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Remove AI slop from text")
    parser.add_argument("input", nargs="?", help="Input file (default: stdin)")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only output cleaned text")
    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    result = unslop(text)

    if args.json:
        out = json.dumps({
            "slop_count": result.slop_count,
            "reduction_pct": round(result.reduction_pct, 1),
            "matches": [
                {"category": m.category, "original": m.original.strip(), "replacement": m.replacement}
                for m in result.matches
            ],
            "cleaned": result.cleaned,
        }, indent=2)
    elif args.quiet:
        out = result.cleaned
    else:
        out = format_report(result)

    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"Written to {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
