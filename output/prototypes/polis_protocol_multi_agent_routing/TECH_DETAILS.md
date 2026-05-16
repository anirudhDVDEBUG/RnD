# Technical Details — Polis Protocol

## What It Does

Polis Protocol is a **markdown-first coordination layer** for multi-vendor AI agent teams. Instead of hardcoding which LLM handles which task, you define each agent's capabilities in a markdown "card," then let a multi-armed bandit algorithm learn the optimal routing from actual outcomes. A lessons ledger feeds results back into the router, creating a compounding improvement loop where routing gets better over time without manual tuning.

The protocol is deliberately file-based (markdown + JSON) so it works inside any repo, with any orchestration framework, and is human-readable by default. There is no server, no database, no vendor lock-in.

## Architecture

### Key Files

| File | Purpose |
|------|---------|
| `polis/cards.py` | Parses markdown capability cards with YAML-ish frontmatter into `AgentCard` dataclasses |
| `polis/bandit.py` | Multi-armed bandit router — Thompson Sampling, UCB1, or epsilon-greedy |
| `polis/ledger.py` | Append-only JSON ledger of agent run outcomes; can replay into router for warm-start |
| `demo.py` | End-to-end simulation: loads cards, routes 60 tasks, records lessons, prints stats |
| `.polis/agents/*.md` | Capability cards (one per agent vendor) |
| `.polis/routing/bandit.md` | Human-readable routing config and fallback table |
| `.polis/lessons/ledger.json` | Machine-readable outcome log |

### Data Flow

```
Task arrives
    │
    ▼
BanditRouter.select(task_type)
    │  ← reads arm stats (alpha/beta per agent per task type)
    ▼
Agent selected via Thompson Sampling
    │
    ▼
Agent executes task (simulated in demo; real API call in production)
    │
    ▼
Reward observed (0.0 – 1.0)
    │
    ├──▶ BanditRouter.update() — updates Beta distribution params
    └──▶ Ledger.append() — persists outcome to JSON
                │
                ▼
         Next run: Ledger.replay_into(router) warm-starts from history
```

### Bandit Strategies

- **Thompson Sampling** (default): Samples from Beta(alpha, beta) per arm. Balances exploration and exploitation naturally. Best for most use cases.
- **UCB1**: Upper Confidence Bound. Deterministic; good for reproducible routing.
- **Epsilon-greedy**: Exploits best-known agent (1-epsilon) of the time, explores randomly epsilon of the time.

All strategies apply exponential **decay** (default 0.95) to non-selected arms so the router adapts when agent quality changes over time.

### Dependencies

**None.** Pure Python 3.8+ standard library (`dataclasses`, `json`, `math`, `random`, `re`, `os`). No pip install needed.

## Limitations

- **No actual API calls.** The demo simulates rewards from a ground-truth matrix. In production you'd wire `router.select()` to real agent SDKs (Anthropic, OpenAI, Google) and feed back real success metrics.
- **No concurrency.** The router is single-threaded. For high-throughput production use, you'd want to lock arm stats or use an async-safe variant.
- **Frontmatter parsing is minimal.** It handles the simple YAML subset used in the cards but not full YAML (no nested objects, no anchors). Works fine for the protocol's needs.
- **No cost optimization.** The bandit optimizes for task success only. A production version could add a cost-aware objective (e.g., reward minus normalized cost).
- **Reward must be provided externally.** The protocol doesn't define how to measure task success — that's left to the integrating system (e.g., test pass rate, human rating, downstream metric).

## Why It Might Matter

If you're building Claude-driven products — lead-gen pipelines, marketing automation, ad creative engines, agent factories, voice AI — you likely already use multiple LLM vendors for different sub-tasks. Polis Protocol gives you:

1. **Auditable routing decisions** — everything in markdown, version-controlled, diffable.
2. **Self-improving routing** — the bandit learns from outcomes instead of relying on static rules.
3. **Vendor portability** — add a new agent by dropping a `.md` card; the bandit starts exploring it automatically.
4. **Team alignment** — non-engineers can read the capability cards and routing table to understand which agent does what and why.

For agent factory builders specifically: Polis provides the "meta-routing" layer that sits above individual agent frameworks (LangChain, CrewAI, Claude Agent SDK) and decides which framework/vendor to invoke for each sub-task.

## Source

[yehudalevy-collab/polis-protocol](https://github.com/yehudalevy-collab/polis-protocol)
