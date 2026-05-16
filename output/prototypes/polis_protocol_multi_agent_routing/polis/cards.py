"""Capability cards: parse and query agent markdown cards."""
from __future__ import annotations
import os, re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class AgentCard:
    name: str
    vendor: str
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    max_context: int = 128000
    cost_tier: str = "medium"
    description: str = ""

def parse_card(path: str) -> AgentCard:
    """Parse a markdown capability card with YAML-ish frontmatter."""
    with open(path) as f:
        text = f.read()
    fm = {}
    last_key = None
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if line.startswith("- "):
                # list item belongs to last key
                if last_key:
                    fm.setdefault(last_key, []).append(line[2:].strip())
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                last_key = k
                if v:
                    fm[k] = v
        body_start = m.end()
    else:
        body_start = 0

    desc_lines = [l for l in text[body_start:].strip().splitlines() if not l.startswith("#")]
    return AgentCard(
        name=fm.get("agent", os.path.splitext(os.path.basename(path))[0]),
        vendor=fm.get("vendor", "unknown"),
        strengths=fm.get("strengths", []),
        weaknesses=fm.get("weaknesses", []),
        max_context=int(fm.get("max_context", 128000)),
        cost_tier=fm.get("cost_tier", "medium"),
        description=" ".join(l.strip() for l in desc_lines if l.strip()),
    )

def load_cards(agents_dir: str) -> Dict[str, AgentCard]:
    cards = {}
    for fname in sorted(os.listdir(agents_dir)):
        if fname.endswith(".md"):
            card = parse_card(os.path.join(agents_dir, fname))
            cards[card.name] = card
    return cards
