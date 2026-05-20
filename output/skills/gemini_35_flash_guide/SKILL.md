---
name: gemini_35_flash_guide
description: |
  Guide for working with Google's Gemini 3.5 Flash model — pricing, capabilities, API usage, and migration from earlier Flash models.
  TRIGGER: user mentions Gemini 3.5 Flash, gemini-3.5-flash model ID, Google I/O 2026 model updates, Gemini Flash pricing, or migrating from Gemini 3 Flash Preview.
---

# Gemini 3.5 Flash Guide

Reference skill for Google's Gemini 3.5 Flash model released at Google I/O 2026. Covers model specs, pricing changes, API usage, and the new Interactions API.

## When to use

- "How do I call Gemini 3.5 Flash via the API?"
- "What's the model ID for the latest Gemini Flash?"
- "How does Gemini 3.5 Flash pricing compare to previous Flash models?"
- "What are the token limits for Gemini 3.5 Flash?"
- "How do I migrate from Gemini 3 Flash Preview to 3.5 Flash?"

## Model specifications

| Property | Value |
|---|---|
| Model ID | `gemini-3.5-flash` |
| Knowledge cut-off | January 2025 |
| Max input tokens | 1,048,576 (1M context) |
| Max output tokens | 65,536 |
| Computer use | Not supported |
| Release | GA (no preview modifier) |

## How to use

### 1. Identify the correct model ID

Use `gemini-3.5-flash` as the model identifier. This model skipped the `-preview` stage and went straight to general availability.

### 2. Call via the Gemini API

Using the Google AI Python SDK:

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-3.5-flash")
response = model.generate_content("Your prompt here")
print(response.text)
```

Using curl:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Your prompt here"}]}]}'
```

### 3. Account for pricing changes

Gemini 3.5 Flash has a **notable price increase** compared to earlier Flash-family models (Gemini 3 Flash Preview, Gemini 2.5 Flash). Review current pricing at the Google AI pricing page before budgeting workloads. The Flash line historically offered the lowest per-token cost in Google's lineup; 3.5 Flash remains cost-effective but is more expensive than its predecessors.

### 4. Consider the new Interactions API (beta)

Google introduced the [Interactions API](https://ai.google.dev/gemini-api/docs/interactions), currently in beta. It provides server-side conversation history management, similar to OpenAI's Responses API pattern. If you need multi-turn state managed server-side, evaluate this API alongside the standard `generateContent` endpoint.

### 5. Migration from earlier models

- Replace model ID `gemini-3-flash-preview` or `gemini-2.5-flash` with `gemini-3.5-flash`.
- Feature parity is mostly the same as the Gemini 3.x series, **except** computer use is not available.
- Test output quality — 3.5 Flash may produce different results on the same prompts.
- Update cost projections given the price increase.

## Availability

Gemini 3.5 Flash is available across:
- **Consumer**: Gemini app, AI Mode in Google Search
- **Developer**: Google Antigravity platform, Gemini API via Google AI Studio, Android Studio
- **Enterprise**: Gemini Enterprise Agent Platform, Gemini Enterprise

## References

- [Simon Willison's analysis: Gemini 3.5 Flash](https://simonwillison.net/2026/May/19/gemini-35-flash/#atom-everything)
- [Google blog: Gemini 3.5 announcement](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/)
- [What's new in Gemini 3.5 Flash (dev docs)](https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5)
- [Interactions API docs (beta)](https://ai.google.dev/gemini-api/docs/interactions)
