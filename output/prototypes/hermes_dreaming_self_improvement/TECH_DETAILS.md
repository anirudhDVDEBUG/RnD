# Technical Details

## What It Does

Hermes Dreaming is a staged self-improvement engine that lets an AI agent propose changes to its own knowledge base -- memory entries, learned skills, and factual knowledge -- through a human-gated review pipeline. The agent analyzes interaction logs, detects patterns (recurring topics, frequently-used tools, explicit corrections), and generates typed proposals. Nothing is applied until a human explicitly approves each proposal.

The core insight is separating *proposing* improvements from *applying* them. This makes agent self-modification auditable and reversible, which matters for production deployments where silent knowledge drift is dangerous.

## Architecture

```
Interaction Log (JSON)
        |
        v
  +-----------+       +----------------+       +-----------+
  |  dream()  | ----> | proposals.json | ----> | review()  |
  +-----------+       +----------------+       +-----------+
                            |                       |
                    approve()/discard()              |
                            |                       v
                            v               Human reads diffs
                      +-----------+
                      |  apply()  |
                      +-----------+
                            |
              +-------------+-------------+
              v             v             v
        memory.json   skills.json    facts.json
```

### Key Files

| File | Purpose |
|---|---|
| `hermes_dreaming/engine.py` | Core logic: `dream()`, `review()`, `approve()`, `discard()`, `apply()` |
| `hermes_dreaming/models.py` | Data classes: `Proposal`, `MemoryEntry`, `SkillEntry`, `FactEntry` |
| `hermes_dreaming/store.py` | JSON-file persistence layer |
| `hermes_dreaming/cli.py` | CLI subcommands wrapping the engine |
| `run.sh` | End-to-end demo script |

### Data Flow

1. **dream()** reads an interaction log (mock data by default), counts topic/tool frequencies, detects corrections, and emits `Proposal` objects with type, action, confidence, and before/after diffs.
2. Proposals are persisted to `proposals.json` with status `staged`.
3. **review()** returns all staged proposals for human inspection.
4. **approve(ids)** / **discard(ids)** flip proposal status.
5. **apply()** walks approved proposals and writes to `memory.json`, `skills.json`, or `facts.json`.

### Proposal Types

| Type | Actions | Example |
|---|---|---|
| `memory_update` | add, merge, prune | "User frequently discusses Python" |
| `skill_update` | add, refine | "Register pytest as a known tool" |
| `fact_update` | add, correct, prune | "Default port is 8080, not 3000" |

### Dependencies

**None.** Pure Python 3.10+ stdlib. No LLM calls, no network, no databases.

In production, the `dream()` function would call an LLM (Claude, etc.) to analyze interactions. This prototype uses deterministic heuristics (frequency counting, correction detection) to demonstrate the pipeline without requiring API keys.

## Limitations

- **No actual LLM analysis.** The dream engine uses simple heuristics, not LLM-powered reflection. A production version would call Claude to generate richer, more nuanced proposals.
- **No MCP server implementation.** The SKILL.md mentions MCP mode (`serve` subcommand) but this prototype focuses on the CLI pipeline. Adding MCP would require `mcp` SDK integration.
- **Flat-file storage.** JSON files work for prototyping but don't support concurrent access or large-scale memory stores.
- **No conflict resolution.** If two proposals touch the same memory key, both get applied sequentially with no merge logic.
- **No interaction log ingestion.** The prototype uses hardcoded mock data. A production version would hook into session logs or conversation history.

## Why This Matters for Claude-Driven Products

**Agent factories / autonomous agents:** Any agent that runs for extended periods needs a way to improve its own knowledge without silently drifting. The review-gate pattern gives operators confidence that the agent isn't accumulating bad facts or losing important context.

**Lead-gen / marketing / ad creatives:** Agents managing campaigns learn user preferences over time (brand voice, audience segments, winning copy patterns). Staged self-improvement lets the agent propose "I've noticed we always use casual tone for Gen-Z segments" as a skill update, which the operator can approve or tweak.

**Voice AI / conversational agents:** Memory consolidation (merging duplicate entries, pruning stale facts) keeps response quality high as conversation history grows. Review gates prevent the agent from "forgetting" something important.

The key architectural takeaway: **make agent self-modification a first-class, auditable workflow** rather than an opaque side-effect of continued operation.
