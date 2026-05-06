# How to Use

## This is a Claude Skill

A Claude Code **skill** is a markdown file that Claude loads when a matching trigger phrase is detected. No server, no API keys, no build step.

## Install (30 seconds)

```bash
# 1. Create the skill directory
mkdir -p ~/.claude/skills/gpt55_instant_model_overview

# 2. Copy the skill file
cp SKILL.md ~/.claude/skills/gpt55_instant_model_overview/SKILL.md
```

That's it. Next time Claude Code starts a conversation, the skill is available.

## Trigger phrases

Say any of these (or similar) to Claude Code and the skill activates:

| Phrase | What you get |
|---|---|
| "What is GPT-5.5 Instant?" | Full overview: release info, key improvements, lineup position |
| "What's new in ChatGPT's default model?" | Same overview, framed around the product change |
| "How does GPT-5.5 Instant reduce hallucinations?" | Technical detail on their approach |
| "What personalization features does GPT-5.5 Instant have?" | Feature breakdown + mechanism |
| "Compare GPT-5.5 Instant to previous GPT models" | Competitive comparison table |

## Will NOT trigger for

- Questions about GPT-4, GPT-5, or other OpenAI models in general
- General AI topics unrelated to this specific release
- Questions about Claude or Anthropic models

## First 60 seconds

```
You:    What is GPT-5.5 Instant and why should I care?

Claude: GPT-5.5 Instant is OpenAI's new default model for ChatGPT,
        announced May 2026. Key improvements:
        - Smarter, more accurate responses
        - Reduced hallucinations (architectural + training changes)
        - Built-in personalization controls (tone, detail, style)
        - Optimized latency ("Instant" designation)

        It replaces the previous ChatGPT default. Complex reasoning
        still routes to o-series models.

        For Claude-based builders, this raises the bar on
        hallucination metrics and makes personalization table stakes.
        Counter with citations, tool-use transparency, and Claude
        skills for brand-voice tuning.
```

## Run the standalone demo

```bash
bash run.sh
```

This runs a Python script that simulates all five skill queries and prints structured output — no API keys needed.
