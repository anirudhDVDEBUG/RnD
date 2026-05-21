#!/usr/bin/env python3
"""
Skill Router — routes user requests to the best-matching installed Claude Code skill.

Scans a skills directory, parses SKILL.md frontmatter, scores each skill against
the user's request, and either suggests top matches or auto-routes silently.
"""

import os
import re
import sys
import json
import argparse
from dataclasses import dataclass, field
from pathlib import Path
from difflib import SequenceMatcher


@dataclass
class Skill:
    name: str
    description: str
    triggers: list[str] = field(default_factory=list)
    path: str = ""


def parse_skill_md(filepath: str) -> Skill | None:
    """Parse a SKILL.md file and extract name, description, and trigger phrases."""
    try:
        text = Path(filepath).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    # Extract YAML-ish frontmatter between --- delimiters
    fm_match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return None

    frontmatter = fm_match.group(1)
    name = ""
    description = ""
    triggers: list[str] = []

    for line in frontmatter.splitlines():
        line = line.strip()
        if line.lower().startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.lower().startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("- ") and not name == "":
            # Could be a trigger line in a triggers list
            triggers.append(line[2:].strip().strip('"').strip("'"))

    # Also scan for TRIGGER: lines in the body
    trigger_match = re.search(r"TRIGGER[:\s]+(.*?)(?:\n|$)", text, re.IGNORECASE)
    if trigger_match:
        trigger_text = trigger_match.group(1)
        # Split on commas or "or"
        for phrase in re.split(r",\s*|\s+or\s+", trigger_text):
            phrase = phrase.strip().strip('"').strip("'")
            if phrase and len(phrase) > 3:
                triggers.append(phrase)

    if not name:
        name = Path(filepath).parent.name

    return Skill(name=name, description=description, triggers=triggers, path=filepath)


def scan_skills_dir(skills_dir: str) -> list[Skill]:
    """Recursively scan a directory for SKILL.md files and parse each."""
    skills = []
    root = Path(skills_dir)
    if not root.is_dir():
        return skills

    for skill_file in root.rglob("SKILL.md"):
        skill = parse_skill_md(str(skill_file))
        if skill:
            skills.append(skill)
    return skills


def score_skill(skill: Skill, query: str) -> float:
    """Score a skill against a user query (0.0 to 1.0)."""
    query_lower = query.lower()
    best = 0.0

    # 1. Exact trigger match — highest priority
    for trigger in skill.triggers:
        trigger_lower = trigger.lower()
        if trigger_lower in query_lower:
            # Boost by how much of the query it covers
            coverage = len(trigger_lower) / max(len(query_lower), 1)
            best = max(best, 0.70 + 0.30 * coverage)

    # 2. Name match
    name_lower = skill.name.lower().replace("-", " ").replace("_", " ")
    if name_lower in query_lower:
        best = max(best, 0.80)

    # 3. Description keyword overlap
    desc_words = set(re.findall(r"\w{3,}", skill.description.lower()))
    query_words = set(re.findall(r"\w{3,}", query_lower))
    if desc_words and query_words:
        overlap = len(desc_words & query_words)
        union = len(desc_words | query_words)
        jaccard = overlap / union if union else 0
        best = max(best, jaccard * 0.85)

    # 4. Fuzzy similarity on name
    ratio = SequenceMatcher(None, name_lower, query_lower).ratio()
    best = max(best, ratio * 0.50)

    return round(best, 3)


def route(skills: list[Skill], query: str, auto: bool = False, top_n: int = 3) -> dict:
    """Route a query to the best skill(s). Returns a result dict."""
    scored = [(skill, score_skill(skill, query)) for skill in skills]
    scored.sort(key=lambda x: x[1], reverse=True)
    scored = [(s, sc) for s, sc in scored if sc > 0.0]

    if not scored:
        return {"mode": "no_match", "matches": [], "message": "No matching skill found."}

    top = scored[:top_n]

    if auto:
        best_skill, best_score = scored[0]
        if best_score >= 0.70:
            return {
                "mode": "auto_routed",
                "skill": best_skill.name,
                "score": best_score,
                "message": f"Auto-routed to **{best_skill.name}** (confidence {best_score:.0%})",
            }
        else:
            # Fall back to suggest mode
            return {
                "mode": "suggest_fallback",
                "matches": [
                    {"skill": s.name, "score": sc, "description": s.description}
                    for s, sc in top
                ],
                "message": f"Confidence too low for auto-routing ({best_score:.0%}). Suggestions below.",
            }

    return {
        "mode": "suggest",
        "matches": [
            {"skill": s.name, "score": sc, "description": s.description}
            for s, sc in top
        ],
    }


def format_result(result: dict) -> str:
    """Pretty-print a routing result for terminal output."""
    lines = []
    mode = result["mode"]

    if mode == "auto_routed":
        lines.append(f"  >>> {result['message']}")
    elif mode == "no_match":
        lines.append(f"  (!) {result['message']}")
    else:
        if mode == "suggest_fallback":
            lines.append(f"  (!) {result['message']}")
        lines.append("  Suggested skills:")
        for i, m in enumerate(result["matches"], 1):
            pct = f"{m['score']:.0%}"
            lines.append(f"    {i}. {m['skill']} — {m['description'][:60]} ({pct} match)")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Skill Router CLI")
    parser.add_argument("query", nargs="?", help="The user request to route")
    parser.add_argument("--skills-dir", default=".claude/skills", help="Path to skills directory")
    parser.add_argument("--auto", action="store_true", help="Enable silent auto-routing")
    parser.add_argument("--json", action="store_true", dest="json_out", help="Output JSON")
    parser.add_argument("--demo", action="store_true", help="Run built-in demo with mock skills")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    skills = scan_skills_dir(args.skills_dir)
    if not skills:
        print(f"No skills found in {args.skills_dir}")
        sys.exit(1)

    result = route(skills, args.query, auto=args.auto)
    if args.json_out:
        print(json.dumps(result, indent=2))
    else:
        print(format_result(result))


def run_demo():
    """Run an end-to-end demo with mock skills."""
    print("=" * 64)
    print("  SKILL ROUTER — Demo")
    print("=" * 64)

    # Build mock skills in-memory
    mock_skills = [
        Skill(
            name="landing-page-builder",
            description="Creates marketing landing pages with HTML/CSS. Generates responsive hero sections, CTAs, and testimonial blocks.",
            triggers=["build a landing page", "create a marketing page", "generate landing page"],
        ),
        Skill(
            name="test-writer",
            description="Generates unit and integration tests for Python and TypeScript codebases using pytest and vitest.",
            triggers=["write tests", "generate tests", "add test coverage", "create unit tests"],
        ),
        Skill(
            name="deploy-to-cloudflare",
            description="Deploys static sites and Workers to Cloudflare Pages. Handles wrangler config and DNS setup.",
            triggers=["deploy to cloudflare", "publish to pages", "set up cloudflare worker"],
        ),
        Skill(
            name="seo-audit",
            description="Audits a webpage for SEO issues: meta tags, heading hierarchy, structured data, page speed signals.",
            triggers=["run seo audit", "check seo", "analyze page seo", "seo review"],
        ),
        Skill(
            name="ad-creative-gen",
            description="Generates ad creatives for Facebook, Google, and LinkedIn campaigns. Produces copy variants and image prompts.",
            triggers=["create ad creative", "generate ad copy", "build ad campaign assets"],
        ),
        Skill(
            name="voice-agent-scaffold",
            description="Scaffolds a voice AI agent using Vapi or Bland.ai. Sets up prompts, tools, and webhook handlers.",
            triggers=["build voice agent", "create voice ai", "scaffold vapi agent"],
        ),
    ]

    test_queries = [
        ("I need to build a landing page for my SaaS product", False),
        ("Write tests for my Python API", False),
        ("Route this: deploy my site to Cloudflare", True),
        ("Which skill handles SEO analysis?", False),
        ("Generate Facebook ad copy for summer sale", True),
        ("Help me refactor my database schema", False),  # No strong match
    ]

    for query, auto in test_queries:
        mode_label = "[auto-route]" if auto else "[suggest]  "
        print(f"\n{'─' * 64}")
        print(f"  Query: \"{query}\"  {mode_label}")
        print(f"{'─' * 64}")
        result = route(mock_skills, query, auto=auto)
        print(format_result(result))

    print(f"\n{'=' * 64}")
    print("  Demo complete. Routed 6 queries across 6 mock skills.")
    print(f"{'=' * 64}")

    # Also output JSON for the last query
    print("\nJSON output for last query:")
    result = route(mock_skills, test_queries[-1][0], auto=False)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
