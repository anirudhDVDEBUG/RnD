# Technical Details: LangGraph Agent Graphs

## What It Does

LangGraph models agent logic as a **directed graph** where nodes are Python functions and edges define transitions between them. Unlike linear chain-based approaches, LangGraph supports **cycles** (agent re-enters the LLM after tool execution), **conditional branching** (route based on LLM output), and **persistent state** (checkpointing across turns). This makes it the go-to library for building production-grade agent systems that need reliability, observability, and human oversight.

This demo implements a complete agent graph from scratch — state definition, tool registry, conditional routing, tool execution, and checkpointed memory — using mock LLM responses so the full execution loop is visible without API keys.

## Architecture

### Data Flow

```
User Message
    |
    v
[START] --> [agent node] ---> should_call_tools? ---> [END]
                ^                    |
                |                    v (has tool_calls)
                +------------ [tool node]
```

1. **User message** enters the graph via `AgentState.messages`
2. **Agent node** invokes the LLM (or mock), appends assistant message to state
3. **Conditional edge** (`should_call_tools`) inspects the last message:
   - If it contains `tool_calls` → route to `tool node`
   - Otherwise → route to `END`
4. **Tool node** executes each tool call, appends tool results to state
5. **Edge back to agent** — the cycle continues until the LLM responds without tool calls

### Key Files

| File | Lines | Role |
|------|-------|------|
| `agent_graph.py` | ~280 | Everything: state, tools, mock LLM, graph builder, demos |

### Dependencies

- **`langgraph`** (>=0.2.0) — Graph runtime, `StateGraph`, `MemorySaver`, streaming
- **`langchain-core`** (>=0.3.0) — Base message types, tool abstractions

For real LLM calls, add `langchain-anthropic` or `langchain-openai`.

### State Schema

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # append-only message list
    tool_calls_count: int                     # tracks total tool invocations
```

The `add_messages` annotation tells LangGraph to **append** new messages rather than overwrite — critical for maintaining conversation history across cycles.

### Mock LLM Design

The `MockLLM` class replays scripted scenarios (defined in `SCENARIOS` dict) to simulate tool-calling behaviour. Each scenario is a sequence of assistant turns with optional `tool_calls`. This lets the demo show the full agent loop — including multi-tool parallel execution and conditional routing — without network calls.

## Limitations

- **Mock only by default**: No real LLM reasoning — responses are scripted. Swap `MockLLM` for `ChatAnthropic`/`ChatOpenAI` to get real inference.
- **In-memory checkpointing**: `MemorySaver` doesn't persist across process restarts. For production, use `SqliteSaver` or `PostgresSaver`.
- **No human-in-the-loop demo**: The code shows the `interrupt_before` API in SKILL.md but the demo doesn't exercise it (would require interactive input).
- **No subgraph/multi-agent**: Single-agent graph only. LangGraph supports nested subgraphs and `create_react_agent` for multi-agent orchestration.
- **No streaming tokens**: Demo uses `stream_mode="updates"` (node-level). Token-level streaming requires a real LLM.

## Why This Matters for Claude-Driven Products

| Use Case | How LangGraph Helps |
|----------|-------------------|
| **Agent factories** | Define agent topologies as data (graph configs), compile them dynamically. Each customer gets a different graph shape. |
| **Lead-gen / marketing agents** | Tool nodes call CRMs, email APIs, analytics. Conditional edges handle qualification logic. Checkpointing recovers from failures mid-funnel. |
| **Ad creative pipelines** | Multi-step generation (research → brief → copy → image prompt → review) maps naturally to a graph with human-in-the-loop approval gates. |
| **Voice AI** | LangGraph's streaming + interrupt model works well for real-time voice agents that need to pause for user input or escalate to humans. |
| **Compliance / audit** | Every graph execution is fully traceable. Checkpoints provide time-travel debugging. `interrupt_before` enforces human approval on sensitive actions. |

LangGraph is the graph runtime — Claude (via `langchain-anthropic`) is the reasoning engine. Together they let you build agents that are **stateful**, **observable**, and **interruptible** — the three properties most production agent systems need.
