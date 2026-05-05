# Technical Details

## What It Does

Photo-agents implements a three-tier memory architecture (working, episodic, semantic) where each memory entry is anchored to a visual screenshot capture. This gives LLM agents a "photographic memory" — they can recall not just what they did, but what the screen looked like when they did it. On top of this, a skill-extraction system watches for repeated successful action sequences and automatically codifies them as reusable, callable skill modules.

The core insight: grounding agent memory in actual visual state (screenshots) reduces hallucination about UI state and enables more reliable computer-use automation. Agents don't just remember "I clicked a button" — they remember what the button looked like and where it was.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                    Agent                          │
│  ┌───────────┐  ┌──────────┐  ┌──────────────┐ │
│  │   Think   │→ │   Act    │→ │  Record      │ │
│  └─────┬─────┘  └────┬─────┘  └──────┬───────┘ │
│        │              │               │          │
│  ┌─────▼──────────────▼───────────────▼───────┐ │
│  │           Vision Grounding                  │ │
│  │  (capture screenshot → CLIP embedding)      │ │
│  └─────────────────┬──────────────────────────┘ │
│                    │                             │
│  ┌─────────────────▼──────────────────────────┐ │
│  │           Layered Memory                    │ │
│  │  ┌─────────┐ ┌──────────┐ ┌────────────┐  │ │
│  │  │ Working │ │ Episodic │ │  Semantic   │  │ │
│  │  │(buffer) │ │(episodes)│ │  (facts)    │  │ │
│  │  └─────────┘ └──────────┘ └────────────┘  │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │           Skill Registry                    │ │
│  │  (auto-extract repeated patterns → skills) │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `photo_agents/agent.py` | Core agent loop: think → act → record |
| `photo_agents/memory.py` | Three-tier memory (working/episodic/semantic) |
| `photo_agents/vision.py` | Screenshot capture + visual embedding |
| `photo_agents/skills.py` | Skill registry + auto-extraction from patterns |
| `demo.py` | End-to-end demonstration |

### Data Flow

1. **Observation** → Agent receives task/context
2. **Vision Capture** → Screenshot taken, embedded via CLIP
3. **Working Memory** → Recent context stored in sliding window
4. **Think** → Agent reasons about observation + memory
5. **Act** → Agent executes action, records in episodic memory
6. **Skill Check** → If action sequence repeats 2+ times → auto-extract skill
7. **Semantic Store** → Key facts persisted for cross-session recall

### Dependencies

- **Core demo**: Python 3.10+ (stdlib only, no external deps)
- **Production**: anthropic/openai SDK, pyautogui, Pillow, CLIP/sentence-transformers
- **Storage**: JSON files on disk (episodes, facts, skills)

### Model Calls

In production, the agent's `think()` step calls an LLM (Claude or GPT-4) to:
- Interpret the current screenshot
- Decide next action based on memory context
- Generate skill descriptions when extracting patterns

This demo simulates the LLM reasoning to run without API keys.

## Limitations

- **No actual screenshot capture** in this demo — uses text placeholders. Production requires `pyautogui` + display server.
- **No real CLIP embeddings** — vision similarity is simulated via hash comparison. Real system needs `sentence-transformers` with CLIP.
- **Skill extraction is naive** — only matches exact action sequences. Production would use semantic similarity to detect similar-but-not-identical patterns.
- **No safety sandbox** — computer-use actions execute directly. Production needs confirmation UI for destructive operations.
- **Memory is file-based** — works for single-agent scenarios but doesn't scale to multi-agent or concurrent access.
- **No LLM integration** in demo — the think/act loop is deterministic. Real value comes from LLM reasoning over visual context.

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent Factories** | Pattern for building agents that improve themselves over time — skills compound across sessions |
| **Lead-gen / Marketing** | Agents that learn to navigate CRMs, fill forms, extract data — and get faster as they learn skills |
| **Ad Creatives** | Visual grounding means agents can verify their own output matches design specs |
| **Voice AI** | Layered memory architecture transfers directly to conversation context management |
| **Computer-use automation** | Vision-grounded memory reduces the #1 failure mode: agents forgetting what state the UI is in |

The key architectural takeaway: **separating memory into tiers + grounding in visual state** produces more reliable autonomous agents than flat context windows alone.
