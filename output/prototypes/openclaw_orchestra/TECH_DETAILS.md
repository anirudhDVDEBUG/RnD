# Technical Details — OpenClaw Orchestra

## What It Does

OpenClaw Orchestra is a multi-agent orchestration framework that decomposes complex development tasks into subtasks and delegates them to isolated specialist agents. Each agent operates in its own workspace directory with dedicated persistent memory (JSON-backed) and a scoped set of tools. A central orchestrator manages the lifecycle: task decomposition, agent provisioning, execution coordination, and optional Linear ticket tracking for oversight.

The core idea is **workspace isolation** — agents cannot interfere with each other's files, memory, or state. This makes multi-agent workflows reproducible and debuggable, unlike shared-context approaches where agents step on each other.

## Architecture

```
orchestrator.py          # Main entry point — task decomp, agent coordination, summary
  |
  +-- orchestra_config.py  # Loads agent topology from YAML/JSON or defaults
  |
  +-- agent.py             # SpecialistAgent class — workspace, memory, tool scope
  |     |
  |     +-- AgentMemory    # Per-agent JSON persistence in workspace/.agent_memory.json
  |
  +-- orchestra.yaml       # Agent topology definition (names, workspaces, tools, prompts)
```

### Data Flow

1. **Orchestrator** receives a task string (e.g., "Implement user auth")
2. **TaskDecomposer** splits it into subtasks based on keyword matching against agent specializations
3. **LinearTracker** creates tickets for each subtask (mock or real)
4. **SpecialistAgents** execute subtasks sequentially — specialist agents first, reviewer last
5. Each agent writes artifacts (Markdown files) to its isolated workspace
6. Agent memory is persisted as JSON in each workspace
7. Orchestrator prints a summary with completion stats and ticket statuses

### Key Files

| File | Role |
|---|---|
| `orchestrator.py` | Entry point, task decomposition, agent coordination |
| `agent.py` | SpecialistAgent + AgentMemory classes |
| `orchestra_config.py` | Config loader (YAML/JSON/defaults) |
| `orchestra.yaml` | Agent topology definition |
| `run.sh` | One-command demo runner |

### Dependencies

- **pyyaml** — YAML config parsing (optional; falls back to JSON or defaults)
- **anthropic** — Claude API client (only needed with `--use-api` flag)
- **Python 3.8+** — no other runtime dependencies

### Model Calls

- In **mock mode** (default): no API calls. Agents return pre-built simulated output.
- In **API mode** (`--use-api`): each agent sends one `messages.create` call to Claude (claude-sonnet-4-20250514) with the agent's system prompt and the subtask description.

## Limitations

- **Task decomposition is keyword-based.** The built-in decomposer uses simple keyword matching, not LLM-powered reasoning. For production use, you'd replace `TaskDecomposer` with a Claude call that analyzes the task semantically.
- **Sequential execution only.** This prototype runs agents one at a time. The real openclaw-orchestra supports parallel agent execution with dependency graphs.
- **No real tool execution.** Agents are told they have tools (code-edit, git, etc.) but this prototype doesn't actually execute them. The full framework integrates with real tool backends.
- **Linear integration is mocked.** Ticket creation/updates are logged but don't hit the Linear API unless you provide real credentials. Even then, the mock tracker is used in this prototype.
- **No inter-agent communication.** Agents cannot message each other mid-task. The reviewer sees only its own mock output, not actual agent artifacts.
- **Memory is per-run.** Workspaces are cleaned on each `run.sh` execution. Persistent cross-run memory requires keeping the workspace directories.

## Why It Matters

For teams building Claude-driven products:

- **Agent factories:** This is the pattern for building "agent of agents" systems. Instead of one monolithic prompt, decompose into specialists. OpenClaw Orchestra provides the scaffolding — isolated workspaces, memory, tool scoping — that makes multi-agent reliable.
- **Lead-gen / marketing automation:** Imagine a "research agent" that finds prospects, a "copywriter agent" that drafts emails, and a "reviewer agent" that checks tone and compliance. Each gets its own workspace and memory. Linear tickets give your team visibility.
- **Ad creative pipelines:** Specialist agents for copy, imagery prompts, A/B variant generation, and compliance review — all coordinated by a single orchestrator with ticket-backed oversight.
- **Voice AI backends:** Multi-agent orchestration can power voice AI systems where different agents handle intent classification, knowledge retrieval, response generation, and safety filtering — each isolated and independently testable.
- **Auditability:** The workspace-per-agent model means every agent's inputs, outputs, and memory are inspectable. Combined with Linear tickets, this gives product teams a complete audit trail of what each agent did and why.
