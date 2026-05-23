# Tech Details: Build Ship Grow Content Strategy

## What It Actually Does

This is a Claude Code skill (a structured markdown prompt) that instructs Claude to generate multi-format content strategies following a three-phase methodology: **Build** (pre-launch content foundation), **Ship** (launch-day execution plan), and **Grow** (sustained post-launch growth). When triggered, Claude reads the skill file and uses its instructions to produce content pillars, calendars, launch checklists, growth plans, social media copy, and SEO blog outlines -- all tailored to the user's product description.

The companion Python script (`content_strategy.py`) demonstrates the same output structure using deterministic templates, no LLM calls required. This lets you evaluate the skill's output format and coverage before adopting it.

## Architecture

```
~/.claude/skills/build-ship-grow/
  SKILL.md            <- The actual skill (markdown prompt with structured sections)

content_strategy.py   <- Standalone demo: generates strategy from Product dataclass
run.sh                <- Runs the demo end-to-end
```

### Key components in `content_strategy.py`:

| Component | Purpose |
|-----------|---------|
| `Product` dataclass | Holds product name, tagline, audience, pain points, stage, differentiators |
| `build_content_pillars()` | Generates 3-5 content pillars from audience and pain points |
| `generate_content_calendar()` | Produces a week-by-week calendar with themes, channels, deliverables |
| `generate_launch_checklist()` | 11-item launch checklist with owners, timing, and status |
| `generate_growth_plan()` | 3-phase 90-day plan with actions and KPI targets |
| `generate_social_copy()` | Twitter thread, LinkedIn post, Product Hunt tagline |
| `generate_blog_outline()` | SEO-optimized blog structure with meta description |
| `render_strategy()` | Formats everything into readable ASCII output |

### Data flow:

1. User provides product context (name, audience, pain points, stage)
2. Each generator function produces a structured dict
3. `render_strategy()` formats all outputs into a single report
4. CLI supports both human-readable and JSON output modes

### Dependencies:

- **Python 3.10+** (uses `list[str]` type hints)
- **No external packages** -- stdlib only (`json`, `textwrap`, `datetime`, `argparse`)
- **No API keys** -- the demo is fully offline; the skill itself runs through Claude Code's built-in LLM

## Limitations

- **The skill is a prompt, not code.** Output quality depends entirely on Claude's interpretation. There is no validation, no API integration, no analytics hookup.
- **No real metrics tracking.** The growth plan suggests what to measure but doesn't connect to any analytics platform.
- **Generic templates.** The launch checklist and growth phases are broadly applicable but not industry-specific. A B2B SaaS launch differs significantly from a consumer app launch.
- **No scheduling or automation.** The content calendar is a plan document, not a scheduler. You still need to manually post or integrate with tools like Buffer/Typefully.
- **Single-pass output.** The skill generates a strategy in one shot. It doesn't iteratively refine based on performance data (though you can re-run it with updated context).

## Why This Matters for Claude-Driven Products

If you're building products in any of these spaces, this skill pattern is directly relevant:

- **Lead-gen / Marketing:** The skill produces ready-to-use marketing copy (social posts, blog outlines, email sequences). Adapt this pattern to generate lead-gen content for your specific vertical.
- **Ad Creatives:** The social copy generator demonstrates how to template persuasive copy with product-specific hooks. Extend it for ad variations and A/B test copy.
- **Agent Factories:** This is a concrete example of a "strategy agent" -- a skill that takes structured input and produces a multi-artifact output plan. The Build->Ship->Grow framework could be wrapped as an autonomous agent workflow.
- **Voice AI:** The content calendar and social copy patterns could feed a voice AI content pipeline (e.g., generating podcast scripts or voice-over copy from the blog outlines).

The broader takeaway: Claude Code skills that encode domain-specific methodologies (like Build->Ship->Grow) turn Claude from a general assistant into a specialized strategist. This is the pattern worth studying.
