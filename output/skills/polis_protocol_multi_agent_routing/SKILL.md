---
name: Polis Protocol – Multi-Agent Routing
description: |
  Markdown protocol for orchestrating multi-vendor AI agent teams using capability cards, bandit routing, and compounding lessons.
  Trigger: user mentions multi-agent coordination, agent routing, cross-vendor agents, capability cards, bandit routing, AGENTS.md protocol, or orchestrating Claude/GPT/Gemini teams.
---

# Polis Protocol – Multi-Agent Routing

Set up and manage a markdown-based protocol for coordinating multi-vendor AI agent teams (Claude, GPT, Gemini, Codex, etc.) using capability cards, multi-armed bandit routing, and a compounding lessons ledger.

## When to use

- "Set up multi-agent routing across Claude, GPT, and Gemini"
- "Create capability cards for my AI agent team"
- "Add bandit routing to pick the best agent for each task"
- "Build an AGENTS.md protocol for cross-vendor agent coordination"
- "Track lessons learned across agent runs so they compound"

## How to use

### 1. Initialize the Polis Protocol structure

Create the directory layout for the protocol:

```
.polis/
├── agents/           # Capability cards (one per agent)
│   ├── claude.md
│   ├── gpt.md
│   └── gemini.md
├── routing/
│   └── bandit.md     # Multi-armed bandit routing config
├── lessons/
│   └── ledger.md     # Compounding lessons from agent runs
└── AGENTS.md          # Top-level protocol index
```

### 2. Define capability cards

For each agent vendor, create a capability card in `.polis/agents/`:

```markdown
---
agent: claude
vendor: anthropic
strengths:
  - long-context analysis
  - code generation
  - careful reasoning
weaknesses:
  - no live web access
max_context: 200000
cost_tier: medium
---

# Claude

Best used for tasks requiring deep reasoning, code review, and long-document analysis.
```

### 3. Configure bandit routing

Set up the multi-armed bandit router in `.polis/routing/bandit.md`:

```markdown
---
strategy: thompson_sampling   # or epsilon_greedy, ucb1
exploration_rate: 0.1
reward_metric: task_success_rate
decay: 0.95
---

# Routing Rules

| Task Type       | Primary Agent | Fallback Agent |
|-----------------|---------------|----------------|
| code_generation | claude        | gpt            |
| web_research    | gemini        | gpt            |
| data_analysis   | claude        | gemini         |
| creative_writing| gpt           | claude         |
```

### 4. Record compounding lessons

After each agent run, append results to `.polis/lessons/ledger.md`:

```markdown
## 2026-05-16 – Code refactor task

- **Agent used:** claude
- **Task:** Refactor auth module
- **Outcome:** success
- **Reward:** 0.92
- **Lesson:** Claude excels at large refactors when given full file context. Provide complete files rather than snippets.
```

The bandit router reads these lessons to update arm weights, so future routing decisions improve automatically.

### 5. Route a task

To route a new task through the protocol:

1. Classify the task type (code generation, research, analysis, etc.)
2. Consult the bandit routing table for the recommended agent
3. Check the agent's capability card for constraints (context limits, cost)
4. Execute with the selected agent
5. Record the outcome in the lessons ledger
6. Update bandit arm weights based on the reward signal

### 6. Create the top-level AGENTS.md

The `AGENTS.md` file serves as the protocol index:

```markdown
# Polis Protocol

This project uses the Polis Protocol for multi-vendor agent coordination.

## Registered Agents
- [Claude](agents/claude.md) — Anthropic
- [GPT](agents/gpt.md) — OpenAI  
- [Gemini](agents/gemini.md) — Google

## Routing
See [bandit.md](routing/bandit.md) for task routing configuration.

## Lessons
See [ledger.md](lessons/ledger.md) for accumulated agent performance data.
```

## Key concepts

- **Capability cards**: Markdown files describing each agent's strengths, weaknesses, context limits, and cost tier
- **Bandit routing**: Multi-armed bandit algorithm (Thompson Sampling, UCB1, or epsilon-greedy) that learns which agent performs best for each task type
- **Lessons ledger**: Append-only log of agent run outcomes that feeds back into routing decisions, creating a compounding improvement loop
- **Cross-vendor**: Works across Claude, GPT, Gemini, Codex, and any other LLM agent

## References

- Source: [yehudalevy-collab/polis-protocol](https://github.com/yehudalevy-collab/polis-protocol)
- Topics: multi-agent, agent-routing, cross-vendor, bandit-routing, AGENTS.md
