#!/usr/bin/env python3
"""
humanize_chinese — rewrite AI-generated Chinese text so it reads naturally.

Pure-Python, rule-based transformer.  No external API keys required.
Works by applying ~20 substitution / restructuring heuristics that target
the most common "AI voice" patterns in Chinese text.
"""

import re
import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Replacement tables
# ---------------------------------------------------------------------------

# Overly formal connectors → colloquial equivalents
FORMAL_TO_COLLOQUIAL: list[tuple[str, list[str]]] = [
    ("此外", ["另外", "还有"]),
    ("因此", ["所以", "这样一来"]),
    ("然而", ["不过", "但是"]),
    ("综上所述", ["总的来说", "说到底"]),
    ("与此同时", ["同时", "另一方面"]),
    ("尽管如此", ["话虽如此", "虽说这样"]),
    ("值得注意的是", ["值得一提", "有意思的是"]),
    ("需要注意的是", ["不过话说回来", "有一点是"]),
    ("从某种程度上讲", ["某种程度上", "说白了"]),
    ("在很大程度上", ["很大程度上", "基本上"]),
    ("由此可见", ["可以看出", "这就说明"]),
    ("不可否认", ["确实", "没错"]),
    ("毋庸置疑", ["毫无疑问", "肯定的是"]),
    ("如前所述", ["前面说了", "刚才提到"]),
    ("众所周知", ["大家都知道", "其实大家清楚"]),
    ("在当今社会", ["现在", "如今"]),
    ("随着…的发展", ["这些年", "最近"]),
    ("具有重要意义", ["很重要", "挺关键的"]),
    ("发挥着重要作用", ["很关键", "起了大作用"]),
    ("取得了显著的进展", ["发展得特别快", "进步了不少"]),
]

# Hedging / filler to remove or shorten
HEDGING_PHRASES: list[str] = [
    "总的来说，",
    "从总体上来看，",
    "一般来说，",
    "客观地说，",
    "事实上，",
    "毫无疑问，",
    "不可否认的是，",
]

# Stiff verb phrases → natural alternatives
VERB_SWAPS: list[tuple[str, str]] = [
    ("进行了深入的探讨", "好好聊了聊"),
    ("进行了详细的分析", "仔细分析了一下"),
    ("给予了高度评价", "评价很高"),
    ("产生了深远的影响", "影响挺大"),
    ("实现了全面的覆盖", "基本都覆盖了"),
    ("非常好", "挺好的"),
    ("非常重要", "很重要"),
]

# Discourse markers to sprinkle (low frequency)
DISCOURSE_MARKERS: list[str] = [
    "其实",
    "说实话",
    "话说回来",
    "对了",
    "说到这",
]


# ---------------------------------------------------------------------------
# Humanizer
# ---------------------------------------------------------------------------

@dataclass
class HumanizeResult:
    original: str
    humanized: str
    changes: list[str] = field(default_factory=list)


def humanize(text: str, *, register: str = "casual", seed: int | None = None) -> HumanizeResult:
    """Apply humanization rules to *text* and return a HumanizeResult."""
    rng = random.Random(seed)
    changes: list[str] = []
    out = text

    # 1. Formal → colloquial connector swaps
    for formal, options in FORMAL_TO_COLLOQUIAL:
        if formal in out:
            replacement = rng.choice(options)
            out = out.replace(formal, replacement, 1)
            changes.append(f"'{formal}' → '{replacement}'")

    # 2. Remove hedging openers
    for hedge in HEDGING_PHRASES:
        if hedge in out:
            out = out.replace(hedge, "", 1)
            changes.append(f"removed hedging: '{hedge.rstrip('，')}'")

    # 3. Verb phrase naturalisation
    for stiff, natural in VERB_SWAPS:
        if stiff in out:
            out = out.replace(stiff, natural, 1)
            changes.append(f"'{stiff}' → '{natural}'")

    # 4. Sentence-length variation: split very long sentences at 、 lists
    #    and recombine with shorter punctuation.
    sentences = re.split(r'(?<=[。！？])', out)
    rebuilt: list[str] = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        # If sentence > 60 chars and contains enumeration, break it up
        if len(s) > 60 and '、' in s:
            parts = s.split('，')
            if len(parts) >= 3:
                mid = len(parts) // 2
                first_half = '，'.join(parts[:mid]) + '。'
                second_half = '，'.join(parts[mid:])
                rebuilt.append(first_half)
                rebuilt.append(second_half)
                changes.append("split long sentence for rhythm")
                continue
        rebuilt.append(s)
    out = ''.join(rebuilt)

    # 5. Optionally insert a discourse marker before the second sentence
    if register == "casual":
        parts = re.split(r'(?<=[。])', out)
        parts = [p for p in parts if p.strip()]
        if len(parts) >= 2:
            marker = rng.choice(DISCOURSE_MARKERS)
            # Insert marker at start of second sentence
            second = parts[1].lstrip()
            if second and not any(second.startswith(m) for m in DISCOURSE_MARKERS):
                parts[1] = marker + '，' + second.lstrip()
                changes.append(f"added discourse marker: '{marker}'")
        out = ''.join(parts)

    # 6. Light punctuation cleanup
    out = out.replace('。。', '。').replace('，，', '，')

    return HumanizeResult(original=text, humanized=out.strip(), changes=changes)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Humanize AI-generated Chinese text",
    )
    parser.add_argument("text", nargs="?", help="Chinese text to humanize (or use --file / stdin)")
    parser.add_argument("-f", "--file", help="Read text from file")
    parser.add_argument("-r", "--register", choices=["casual", "professional", "creative"],
                        default="casual", help="Target register (default: casual)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.error("Provide text as argument, via --file, or pipe to stdin")

    result = humanize(text, register=args.register, seed=args.seed)

    print("=" * 60)
    print("ORIGINAL:")
    print(result.original)
    print()
    print("HUMANIZED:")
    print(result.humanized)
    print()
    print(f"CHANGES ({len(result.changes)}):")
    for c in result.changes:
        print(f"  • {c}")
    print("=" * 60)


if __name__ == "__main__":
    main()
