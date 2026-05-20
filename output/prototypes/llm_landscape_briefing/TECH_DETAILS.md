# Technical Details

## What it does

This is a Claude Code **skill** — a markdown file that injects domain knowledge into Claude's context when triggered by relevant user queries. The skill encodes a curated snapshot of the LLM competitive landscape as of mid-2026, sourced from Simon Willison's PyCon US 2026 lightning talk "The last six months in LLMs in five minutes." It provides Claude with structured facts about model tiers, the Nov 2025 coding-agent inflection point, leadership changes across vendors, and practical model-selection guidance.

The companion Python script (`llm_briefing.py`) demonstrates the same knowledge as a standalone CLI tool, producing text or JSON briefings without requiring any API calls.

## Architecture

```
~/.claude/skills/llm_landscape_briefing/
  SKILL.md          <- Claude Code reads this at trigger time

llm_briefing.py     <- Standalone demo (Python 3.6+, stdlib only)
run.sh              <- Runs all demo modes
```

- **SKILL.md**: Trigger conditions in YAML frontmatter, structured guidance in markdown body. Claude Code's skill loader matches user intent against the `description` field and injects the full file into the conversation context.
- **llm_briefing.py**: Embedded dicts for model tiers, leadership timeline, insights, and per-focus recommendations. Outputs formatted text or JSON. Zero dependencies beyond Python stdlib.
- **Data flow**: User query -> Claude Code skill matcher -> SKILL.md injected into context -> Claude generates briefing using the embedded facts + its own knowledge.

## Limitations

- **Static data**: The skill and demo embed a fixed snapshot. The LLM landscape moves fast (~3 month shelf life per the source). You'll need to update the model tiers and timeline manually.
- **No live benchmarks**: Does not query any benchmark API or run evals. Recommendations are editorial, not empirical.
- **Single source**: Based primarily on one (excellent) lightning talk. Does not aggregate multiple analyst reports or pricing data.
- **Skill, not agent**: The SKILL.md gives Claude knowledge but doesn't give it tools to look up current pricing, run benchmarks, or compare outputs. It's a knowledge injection, not an autonomous workflow.

## Why it matters for Claude-driven products

- **Agent factories**: If you're building agents that use LLMs under the hood, knowing which model to slot in (and planning for model rotation) is a first-order architectural decision. This skill surfaces that decision framework.
- **Lead-gen / marketing**: "Which AI model is best for X?" is a high-intent search query. Content based on this skill's structured data can drive organic traffic and position you as an informed advisor.
- **Ad creatives**: Understanding model capabilities lets you make accurate claims in ad copy (e.g., "powered by frontier-tier Claude Opus 4.6") rather than generic "AI-powered" messaging.
- **Voice AI**: Model selection for real-time voice (latency-sensitive) vs. batch processing (cost-sensitive) is a key tradeoff this briefing helps navigate.
- **Cost planning**: The three-tier framework (Frontier / Balanced / Fast-Cheap) maps directly to product pricing tiers and margin calculations.

## Source

Simon Willison, "The last six months in LLMs in five minutes," PyCon US 2026 Lightning Talk.
https://simonwillison.net/2026/May/19/5-minute-llms/#atom-everything
