# Technical Details

## What this is

A **Claude Code skill** — a structured markdown file (`SKILL.md`) that injects domain knowledge about OpenAI's GPT-5.5 Instant release into Claude's context when triggered by relevant user queries. The companion Python script (`gpt55_overview.py`) demonstrates the same knowledge base in standalone form for evaluation.

This is not a code library or an MCP server. It's a knowledge artifact that makes Claude conversationally competent about a specific competitor release without requiring web search or API calls.

## Architecture

```
SKILL.md                 ← Claude skill file (drop into ~/.claude/skills/)
gpt55_overview.py        ← Standalone demo: same knowledge, runnable without Claude
run.sh                   ← Entry point: runs the demo
requirements.txt         ← No external deps (Python stdlib only)
```

**Data flow (as a skill):**
1. User asks Claude Code a question matching a trigger phrase
2. Claude Code loads `SKILL.md` into context
3. Claude uses the structured facts to answer accurately

**Data flow (standalone demo):**
1. `run.sh` calls `python3 gpt55_overview.py`
2. Script iterates five canned queries, prints formatted answers
3. Dumps the full knowledge base as JSON for downstream tooling

## Key facts encoded

- **Model identity:** GPT-5.5 Instant, OpenAI, May 2026, new ChatGPT default
- **Improvements:** accuracy, clarity, hallucination reduction, personalization, latency
- **Hallucination approach:** architectural + training pipeline changes targeting confabulation
- **Personalization:** tone, detail level, interaction style — stored in user profile, applied at inference
- **Lineup position:** default/fast tier; o-series handles heavy reasoning
- **Competitive comparison:** side-by-side table vs Claude Opus 4.6, Sonnet 4.6, Haiku 4.5

## Dependencies

- Python 3.6+ (stdlib only: `json`, `textwrap`, `datetime`)
- No API keys, no network access, no external packages

## Limitations

- **Static knowledge:** The skill reflects the blog post at time of writing. It does not auto-update if OpenAI revises pricing, benchmarks, or capabilities.
- **No benchmark numbers:** OpenAI's announcement emphasizes qualitative improvements. The skill does not contain specific benchmark scores because none were published in the source material.
- **No API integration:** This skill tells Claude *about* GPT-5.5 Instant; it does not call the OpenAI API or proxy requests to it.
- **Single source:** Based on the official OpenAI blog post. Does not incorporate third-party benchmarks or user reports.

## Why this matters for Claude-based product builders

| Domain | Relevance |
|---|---|
| **Lead-gen / marketing** | Competitor positioning intelligence — know what claims OpenAI is making so your copy can counter effectively |
| **Ad creatives** | GPT-5.5 Instant's personalization controls could enable self-serve brand-voice tuning in ChatGPT; Claude skills should match this |
| **Agent factories** | "Instant" latency positioning means speed comparisons will intensify; architect around Haiku/Sonnet for speed-sensitive agents |
| **Voice AI** | Low-latency default model raises expectations; Claude voice pipelines should benchmark against this baseline |
| **Competitive analysis** | Structured knowledge lets your Claude agents answer "how do we compare?" questions accurately instead of hallucinating |

## Source

- [GPT-5.5 Instant: smarter, clearer, and more personalized — OpenAI Blog](https://openai.com/index/gpt-5-5-instant)
