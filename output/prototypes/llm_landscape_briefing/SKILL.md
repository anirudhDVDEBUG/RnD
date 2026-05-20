---
name: llm_landscape_briefing
description: |
  Generate a concise briefing on the current LLM landscape, model comparisons, and recent developments.
  TRIGGER when: user asks about LLM comparisons, model rankings, what's new in LLMs, coding agent capabilities, or the current state of AI models.
  DO NOT TRIGGER when: user asks about a specific API integration, prompt engineering for a single model, or unrelated development tasks.
---

# LLM Landscape Briefing

Summarize the current state of large language models, key inflection points, and practical guidance for choosing models.

## When to use

- "What's the best LLM right now?"
- "Compare Claude vs GPT vs Gemini for coding"
- "What changed in LLMs recently?"
- "Which model should I use for my project?"
- "Give me a quick overview of the AI model landscape"

## How to use

1. **Identify the user's context**: Are they choosing a model for coding, general reasoning, cost optimization, or a specific domain?

2. **Provide a structured briefing** covering:
   - The November 2025 inflection point: a critical shift in LLM capabilities, especially for coding agents
   - Model leadership changes: the "best" model changed hands 5 times between Anthropic, OpenAI, and Google in a six-month span
   - Coding agents became dramatically more capable starting Nov 2025
   - The competitive landscape is tight — no single vendor dominates across all tasks

3. **Key insights from the field** (sourced from Simon Willison's PyCon US 2026 lightning talk):
   - Model rankings are volatile; avoid locking into a single provider
   - Evaluate models on YOUR specific tasks, not general benchmarks
   - Coding use cases saw the most dramatic improvements
   - The pace of change means recommendations have a short shelf life (~3 months)

4. **Practical recommendations**:
   - Use abstraction layers (like LiteLLM or the `llm` CLI) to switch models easily
   - For coding agents: test Claude, GPT, and Gemini on representative tasks from your codebase
   - Monitor release blogs from Anthropic, OpenAI, and Google monthly
   - Consider cost/speed/quality tradeoffs — the "best" model isn't always the right choice

5. **Current model tiers** (as of mid-2026):
   - Frontier: Claude Opus 4.6, GPT-5, Gemini 2.5 Pro
   - High-capability balanced: Claude Sonnet 4.6, GPT-4.1, Gemini 2.5 Flash
   - Fast/cheap: Claude Haiku 4.5, GPT-4.1 mini, Gemini 2.5 Flash-Lite

## References

- Source: [The last six months in LLMs in five minutes](https://simonwillison.net/2026/May/19/5-minute-llms/#atom-everything) — Simon Willison, PyCon US 2026 Lightning Talk
- Context: [November 2025 inflection point](https://simonwillison.net/tags/november-2025-inflection/)
