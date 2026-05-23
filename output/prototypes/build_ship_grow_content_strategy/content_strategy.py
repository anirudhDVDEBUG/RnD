#!/usr/bin/env python3
"""
Build Ship Grow Content Strategy — Demo Engine

Generates structured content strategies following the Build -> Ship -> Grow
methodology. Runs fully offline with mock data to demonstrate the skill's
output formats: content calendars, launch checklists, growth plans, and
social media copy.
"""

import json
import textwrap
from datetime import datetime, timedelta
from typing import Optional

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

class Product:
    """Minimal product descriptor."""
    def __init__(self, name: str, tagline: str, audience: str,
                 pain_points: list[str], stage: str, differentiators: list[str]):
        self.name = name
        self.tagline = tagline
        self.audience = audience
        self.pain_points = pain_points
        self.stage = stage  # build | ship | grow
        self.differentiators = differentiators


# ---------------------------------------------------------------------------
# Strategy generators
# ---------------------------------------------------------------------------

def build_content_pillars(product: Product) -> list[dict]:
    """Return 3-5 content pillars aligned with the audience."""
    base = [
        {"pillar": f"How {product.name} solves {product.pain_points[0]}",
         "format": "Tutorial / walkthrough", "frequency": "Weekly"},
        {"pillar": "Building in public updates",
         "format": "Dev log / thread", "frequency": "2x per week"},
        {"pillar": f"Industry trends for {product.audience}",
         "format": "Curated roundup", "frequency": "Weekly"},
    ]
    if len(product.pain_points) > 1:
        base.append({
            "pillar": f"Deep dive: {product.pain_points[1]}",
            "format": "Long-form blog post", "frequency": "Bi-weekly",
        })
    if len(product.differentiators) > 0:
        base.append({
            "pillar": f"Why {product.differentiators[0]} matters",
            "format": "Comparison / case study", "frequency": "Monthly",
        })
    return base


def generate_content_calendar(product: Product, weeks: int = 4) -> list[dict]:
    """Generate a week-by-week content calendar."""
    today = datetime.now()
    channels = ["Blog", "Twitter/X", "LinkedIn", "Newsletter"]
    topics_by_week = [
        f"Introduce {product.name} — what problem it solves",
        f"Behind the scenes: building {product.name}",
        f"User pain point deep-dive: {product.pain_points[0]}",
        f"Differentiation story: {product.differentiators[0] if product.differentiators else 'our approach'}",
    ]
    calendar = []
    for w in range(weeks):
        start = today + timedelta(weeks=w)
        calendar.append({
            "week": w + 1,
            "start_date": start.strftime("%Y-%m-%d"),
            "theme": topics_by_week[w % len(topics_by_week)],
            "channels": channels[:2 + (w % 3)],
            "deliverables": [
                f"1 blog post on '{topics_by_week[w % len(topics_by_week)]}'",
                "3 social posts repurposed from blog",
                "1 newsletter issue" if w % 2 == 0 else "1 Twitter/X thread",
            ],
        })
    return calendar


def generate_launch_checklist(product: Product) -> list[dict]:
    """Produce a launch-day checklist."""
    return [
        {"task": "Finalize landing page copy and CTA", "owner": "Marketing", "due": "T-7 days", "done": False},
        {"task": "Write launch announcement blog post", "owner": "Content", "due": "T-5 days", "done": False},
        {"task": "Draft Twitter/X launch thread (8-10 tweets)", "owner": "Content", "due": "T-3 days", "done": False},
        {"task": "Prepare Product Hunt listing (tagline, images, maker comment)", "owner": "Growth", "due": "T-3 days", "done": False},
        {"task": "Schedule launch-day email to waitlist", "owner": "Marketing", "due": "T-2 days", "done": False},
        {"task": "Brief 5 supporters to upvote/comment at launch", "owner": "Growth", "due": "T-1 day", "done": False},
        {"task": "Ship final build to production", "owner": "Engineering", "due": "T-0", "done": False},
        {"task": "Publish blog post and social threads", "owner": "Content", "due": "T-0 09:00", "done": False},
        {"task": "Go live on Product Hunt", "owner": "Growth", "due": "T-0 00:01 PST", "done": False},
        {"task": "Monitor and respond to comments for 12 hours", "owner": "All", "due": "T-0 all day", "done": False},
        {"task": "Send launch recap + metrics email to team", "owner": "Marketing", "due": "T+1 day", "done": False},
    ]


def generate_growth_plan(product: Product) -> dict:
    """Build a post-launch growth plan."""
    return {
        "objective": f"Acquire first 1,000 users for {product.name}",
        "timeline": "90 days post-launch",
        "phases": [
            {
                "phase": "Week 1-2: Foundation",
                "actions": [
                    "Publish 2 SEO-targeted articles per week",
                    "Launch a weekly newsletter for early adopters",
                    "Engage in 3 relevant communities daily (Reddit, Discord, Slack)",
                ],
                "kpi": "200 signups, 50 newsletter subscribers",
            },
            {
                "phase": "Week 3-6: Amplify",
                "actions": [
                    "Start a referral program (give 1 month free for each referral)",
                    "Publish 1 case study featuring an early user",
                    "Guest post on 2 industry blogs",
                    "Run a Twitter/X giveaway or challenge",
                ],
                "kpi": "500 signups, 150 newsletter subscribers, 3% referral rate",
            },
            {
                "phase": "Week 7-12: Scale",
                "actions": [
                    "Double down on top 2 performing channels",
                    "Launch a content repurposing engine (blog -> thread -> newsletter -> short video)",
                    "A/B test landing page headline and CTA",
                    "Explore paid acquisition on best-performing channel ($500 test budget)",
                ],
                "kpi": "1,000 signups, 400 newsletter subscribers, <$5 CAC",
            },
        ],
        "metrics_to_track": [
            "Weekly signups by channel",
            "Newsletter open rate & click-through rate",
            "Referral conversion rate",
            "Content engagement (shares, saves, comments)",
            "CAC (Customer Acquisition Cost)",
        ],
    }


def generate_social_copy(product: Product) -> dict:
    """Generate ready-to-post social media copy."""
    return {
        "twitter_thread": [
            f"I just shipped {product.name} -- {product.tagline}",
            f"The problem: {product.pain_points[0]}.",
            f"Most solutions out there {'miss the mark' if len(product.differentiators) == 0 else 'lack ' + product.differentiators[0]}.",
            f"{product.name} fixes this by focusing on what actually matters to {product.audience}.",
            f"Here's what you get:\n- {product.differentiators[0] if product.differentiators else 'A better workflow'}\n- Built for {product.audience}\n- Free to start",
            f"Try it today and tell me what you think. Link in bio.",
            f"If this resonates, RT the first tweet so others can find it. I'm building this in public and would love your feedback.",
        ],
        "linkedin_post": textwrap.dedent(f"""\
            After months of building, I'm excited to announce {product.name}.

            {product.tagline}

            The {product.audience} space has a real problem:
            {product.pain_points[0]}.

            {product.name} takes a different approach -- {product.differentiators[0] if product.differentiators else 'simplicity first'}.

            Early users are already seeing results.

            If you're in {product.audience}, I'd love your feedback.
            Drop a comment or DM me to get early access.

            #buildinpublic #launch #startup
        """),
        "product_hunt_tagline": f"{product.tagline} | Built for {product.audience}",
    }


def generate_blog_outline(product: Product) -> dict:
    """Generate an SEO-optimized blog outline."""
    keyword = product.pain_points[0].lower().replace(" ", "-")
    return {
        "title": f"How to Solve {product.pain_points[0]} — A Complete Guide",
        "target_keyword": keyword,
        "estimated_word_count": "1,500-2,000",
        "sections": [
            {"heading": "Introduction", "notes": f"Hook with the pain point. Mention {product.name} as the solution."},
            {"heading": f"What Is {product.pain_points[0]}?", "notes": "Define the problem. Use stats if available."},
            {"heading": "Why Existing Solutions Fall Short", "notes": "Discuss common approaches and their limitations."},
            {"heading": f"How {product.name} Approaches This Differently",
             "notes": f"Introduce {product.differentiators[0] if product.differentiators else 'your unique angle'}."},
            {"heading": "Step-by-Step: Getting Started", "notes": "Walkthrough with screenshots or code snippets."},
            {"heading": "Results and What to Expect", "notes": "Social proof, early metrics, or testimonials."},
            {"heading": "Conclusion + CTA", "notes": "Summarize value. Link to signup or trial."},
        ],
        "internal_links": [f"/{keyword}-guide", "/getting-started", "/pricing"],
        "meta_description": f"Learn how to solve {product.pain_points[0]} with {product.name}. A step-by-step guide for {product.audience}.",
    }


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def hr():
    return "=" * 72


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a simple Markdown-style ASCII table."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * widths[i] for i in range(len(headers)))
    lines = [header_line, sep_line]
    for row in rows:
        lines.append(" | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))
    return "\n".join(lines)


def render_strategy(product: Product) -> str:
    """Render the full strategy report to stdout-friendly text."""
    parts = []

    parts.append(hr())
    parts.append(f"  BUILD SHIP GROW -- Content Strategy for {product.name}")
    parts.append(f"  Stage: {product.stage.upper()}")
    parts.append(hr())

    # --- Content pillars ---
    parts.append("\n## Content Pillars\n")
    pillars = build_content_pillars(product)
    rows = [[p["pillar"], p["format"], p["frequency"]] for p in pillars]
    parts.append(render_table(["Pillar", "Format", "Frequency"], rows))

    # --- Content calendar ---
    parts.append(f"\n\n## 4-Week Content Calendar\n")
    calendar = generate_content_calendar(product)
    for week in calendar:
        parts.append(f"### Week {week['week']} (starts {week['start_date']})")
        parts.append(f"  Theme: {week['theme']}")
        parts.append(f"  Channels: {', '.join(week['channels'])}")
        for d in week["deliverables"]:
            parts.append(f"    - {d}")
        parts.append("")

    # --- Launch checklist ---
    parts.append(f"\n## Launch Checklist\n")
    checklist = generate_launch_checklist(product)
    for item in checklist:
        box = "[x]" if item["done"] else "[ ]"
        parts.append(f"  {box} {item['task']}  ({item['owner']}, {item['due']})")

    # --- Growth plan ---
    parts.append(f"\n\n## 90-Day Growth Plan\n")
    plan = generate_growth_plan(product)
    parts.append(f"Objective: {plan['objective']}")
    parts.append(f"Timeline:  {plan['timeline']}\n")
    for phase in plan["phases"]:
        parts.append(f"### {phase['phase']}")
        for a in phase["actions"]:
            parts.append(f"  - {a}")
        parts.append(f"  KPI target: {phase['kpi']}\n")
    parts.append("Metrics to track:")
    for m in plan["metrics_to_track"]:
        parts.append(f"  - {m}")

    # --- Social copy ---
    parts.append(f"\n\n## Ready-to-Post Social Copy\n")
    social = generate_social_copy(product)
    parts.append("### Twitter/X Launch Thread")
    for i, tweet in enumerate(social["twitter_thread"], 1):
        parts.append(f"  {i}/ {tweet}")
    parts.append(f"\n### LinkedIn Post\n{social['linkedin_post']}")
    parts.append(f"### Product Hunt Tagline\n  {social['product_hunt_tagline']}")

    # --- Blog outline ---
    parts.append(f"\n\n## SEO Blog Outline\n")
    blog = generate_blog_outline(product)
    parts.append(f"Title: {blog['title']}")
    parts.append(f"Target keyword: {blog['target_keyword']}")
    parts.append(f"Word count: {blog['estimated_word_count']}")
    parts.append(f"Meta description: {blog['meta_description']}\n")
    for section in blog["sections"]:
        parts.append(f"  H2: {section['heading']}")
        parts.append(f"      {section['notes']}")

    parts.append(f"\n{hr()}")
    parts.append("  Strategy generated by Build Ship Grow Content Strategy Skill")
    parts.append(hr())

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

DEMO_PRODUCT = Product(
    name="SkillForge",
    tagline="Ship Claude Code skills in minutes, not days",
    audience="indie hackers and AI-tool builders",
    pain_points=[
        "creating polished Claude Code skills takes too long",
        "no structured workflow for skill distribution",
    ],
    stage="ship",
    differentiators=[
        "one-command scaffolding with best-practice templates",
        "built-in testing and validation",
    ],
)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Build Ship Grow Content Strategy — generate a full content + growth plan."
    )
    parser.add_argument("--name", default=None, help="Product name")
    parser.add_argument("--tagline", default=None, help="One-line product tagline")
    parser.add_argument("--audience", default=None, help="Target audience")
    parser.add_argument("--stage", choices=["build", "ship", "grow"], default=None,
                        help="Current stage: build, ship, or grow")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    args = parser.parse_args()

    product = DEMO_PRODUCT
    if args.name:
        product = Product(
            name=args.name,
            tagline=args.tagline or f"{args.name} — a great product",
            audience=args.audience or "developers and creators",
            pain_points=["inefficient workflows", "lack of automation"],
            stage=args.stage or "ship",
            differentiators=["simple and effective approach"],
        )

    if args.json:
        data = {
            "product": {"name": product.name, "tagline": product.tagline,
                        "audience": product.audience, "stage": product.stage},
            "content_pillars": build_content_pillars(product),
            "content_calendar": generate_content_calendar(product),
            "launch_checklist": generate_launch_checklist(product),
            "growth_plan": generate_growth_plan(product),
            "social_copy": generate_social_copy(product),
            "blog_outline": generate_blog_outline(product),
        }
        print(json.dumps(data, indent=2))
    else:
        print(render_strategy(product))


if __name__ == "__main__":
    main()
