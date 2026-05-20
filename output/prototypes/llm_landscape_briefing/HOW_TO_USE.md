# How to Use

## This is a Claude Code Skill

### Install

Copy the `SKILL.md` file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/llm_landscape_briefing
cp SKILL.md ~/.claude/skills/llm_landscape_briefing/SKILL.md
```

That's it. No dependencies, no server, no API keys.

### Trigger phrases

Once installed, Claude Code activates this skill when you say things like:

- "What's the best LLM right now?"
- "Compare Claude vs GPT vs Gemini for coding"
- "What changed in LLMs recently?"
- "Which model should I use for my project?"
- "Give me a quick overview of the AI model landscape"

It will **not** trigger for: specific API integration questions, prompt engineering for a single model, or unrelated dev tasks.

### First 60 seconds

1. Install the skill (copy command above)
2. Open Claude Code in any project
3. Ask: **"What's the current LLM landscape look like?"**
4. Claude responds with a structured briefing covering model tiers, the Nov 2025 inflection point, leadership timeline, and a recommendation tailored to your context (coding, cost, etc.)

Example exchange:

```
You: Which model should I use for my coding agent?

Claude: Based on the current landscape, here's my recommendation...

## Model Leadership Timeline
The "best" coding model changed 5 times since Nov 2025:
- Nov 2025: Claude 3.5 Sonnet — the inflection point for coding agents
- Dec 2025: Gemini 2.0 Flash
- Jan 2026: o3-mini
- Feb 2026: Claude 3.5 Opus
- Mar 2026: GPT-5

## Current Frontier Models for Coding
- Claude Opus 4.6 (Anthropic, May 2026)
- GPT-5 (OpenAI, Mar 2026)
- Gemini 2.5 Pro (Google, Mar 2026)

## My Recommendation
Test all three on representative tasks from YOUR codebase.
Use LiteLLM or the `llm` CLI to abstract the provider layer
so you can switch without rewriting.
```

## Standalone CLI demo

The repo also includes a Python script that generates briefings without Claude:

```bash
# General briefing (text)
python3 llm_briefing.py general

# Coding-focused briefing
python3 llm_briefing.py coding

# JSON output
python3 llm_briefing.py coding json

# All focuses at once
bash run.sh
```

Valid focus areas: `general`, `coding`, `cost_sensitive`, `multi_provider`
