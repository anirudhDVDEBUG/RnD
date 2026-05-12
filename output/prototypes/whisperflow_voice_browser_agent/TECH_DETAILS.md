# Technical Details

## What it does

WhisperFlow chains three AI capabilities into a single loop: (1) Whisper STT converts spoken commands to text, (2) GPT-4o Vision analyzes a live browser screenshot plus DOM context to plan a sequence of actions, and (3) Playwright executes those actions in a real Chromium instance. An adaptive memory layer records which CSS selectors succeed or fail on each domain, enabling self-healing — when a selector breaks (e.g., after a site redesign), the agent recalls past alternatives and retries automatically.

A lightweight expert-routing layer classifies each command into a persona (Navigator, Searcher, Reader, Interactor, Analyst) so the system prompt sent to GPT-4o is tailored to the task type.

## Architecture

```
Voice Command (mic)
       |
  voice_input.py  --- Whisper STT ---> text command
       |
  expert_personas.py --- keyword routing ---> chosen persona
       |
  browser_agent.py --- Playwright ---> screenshot + page context
       |
  vision_analyzer.py --- GPT-4o Vision ---> action plan [click, type, navigate, ...]
       |
  browser_agent.py --- execute actions ---> DOM mutations
       |
  memory_store.py --- record success/failure ---> memory.json
       |
  (loop back to voice input)
```

### Key files

| File | Purpose |
|---|---|
| `main.py` | Orchestrator: runs the voice-plan-execute loop |
| `voice_input.py` | Captures mic audio, sends to Whisper, returns text |
| `browser_agent.py` | Playwright wrapper: navigate, click, type, screenshot |
| `vision_analyzer.py` | Sends screenshot + context to GPT-4o, parses action JSON |
| `memory_store.py` | JSON-backed store tracking selector success/failure rates |
| `expert_personas.py` | Routes commands to specialist personas by keyword match |

### Dependencies

- **OpenAI API** (Whisper + GPT-4o Vision) — the core intelligence
- **Playwright** — headless Chromium browser automation
- **sounddevice / numpy** — mic capture for voice input
- **No database** — memory is a flat JSON file

### Model calls per command

| Step | Model | Tokens (approx) |
|---|---|---|
| Transcription | `whisper-1` | audio-length dependent |
| Action planning | `gpt-4o` (vision) | ~500-1500 output |

## Limitations

- **English only** — Whisper supports many languages, but the expert persona keywords and mock data are English.
- **No multi-tab support** — operates on a single browser tab.
- **No authentication flows** — cannot handle CAPTCHAs, 2FA, or OAuth pop-ups.
- **Selector fragility** — the self-healing memory helps, but heavily JS-rendered SPAs with random class names can still break.
- **Cost** — each command round-trip costs ~$0.01-0.05 in API calls (screenshot image + text).
- **Latency** — Whisper + Vision + Playwright round-trip is 3-8 seconds per command.
- **Expert routing is naive** — keyword matching, not LLM-based classification. Works for common commands but misroutes edge cases.

## Why it matters for Claude-driven products

1. **Voice AI pipelines**: Shows how to chain STT -> reasoning -> action in a tight loop. Directly applicable to voice-first agent factories.
2. **Self-healing agents**: The memory-based selector retry pattern applies to any web scraping or automation agent, not just voice-driven ones. Useful for lead-gen bots, marketing automation, and ad-creative scrapers that break when target sites change.
3. **Multi-persona routing**: The expert-routing pattern (classify intent -> select specialized prompt) is a lightweight alternative to full multi-agent orchestration. Applicable to customer service bots, content generation pipelines, and any system that needs to handle diverse user intents.
4. **Browser-as-tool for LLMs**: Demonstrates the pattern of screenshot -> vision model -> action plan that is becoming standard in agentic browsing (similar to Claude's computer use). Understanding this architecture helps when building or evaluating competing approaches.
