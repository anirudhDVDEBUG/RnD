# Technical Details — OpenSquilla Token-Efficient Agent

## What It Does

OpenSquilla is a Python-based AI agent framework designed around one core idea: **maximize the intelligence you get per token spent**. Instead of sending verbose, filler-laden prompts to an LLM, OpenSquilla compresses prompts before they hit the model, routes tasks to specialized skill handlers when possible (bypassing the LLM entirely for known tasks), and persists agent memory across sessions to avoid re-explaining context.

The framework also supports MCP (Model Context Protocol) server declarations, allowing agents to use external tools (filesystem, GitHub, databases) through a standardized interface compatible with Claude and other MCP-aware clients.

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `opensquilla_agent.py` | Core framework: `Agent`, `PromptCompressor`, `Skill` decorator, `AgentMemory`, `MCPConfig` |
| `demo.py` | End-to-end demo exercising all features |
| `run.sh` | One-command execution |

### Data Flow

```
User prompt
    |
    v
PromptCompressor.compress(prompt, budget)
    |-- Strip filler phrases ("please", "could you", "kindly")
    |-- Collapse whitespace
    |-- Truncate to token budget
    |
    v
Skill matching (keyword-based)
    |-- Match found -> execute skill function directly (no LLM call)
    |-- No match -> proceed to LLM
    |
    v
Memory injection (append stored context)
    |
    v
LLM call (mock in demo; real API in production)
    |
    v
Response + stats (original tokens, compressed tokens, savings %, density)
```

### Dependencies

- **Runtime:** Python 3.8+ stdlib only (json, hashlib, pathlib, dataclasses)
- **Production OpenSquilla:** adds `httpx`, `pydantic`, and an LLM provider SDK (e.g., `anthropic`, `openai`)
- **MCP integration:** requires `npx` and MCP server packages (e.g., `@modelcontextprotocol/server-filesystem`)

### Intelligence Density Metric

```
intelligence_density = compressed_tokens / original_tokens
```

Lower values mean more compression — the agent delivers the same task with fewer tokens. A density of 0.36 means the agent uses only 36% of the original token budget.

## Limitations

- **Compression is naive:** The current compressor strips known filler phrases and truncates. It does not use semantic analysis, embedding-based deduplication, or chain-of-thought distillation. Production OpenSquilla may implement more sophisticated strategies.
- **Skill matching is keyword-based:** A skill named "summarize" matches any prompt containing "summarize." No intent classification or NLU is used in this demo.
- **No real LLM backend in demo:** The mock response simulates the pipeline but does not call any model. Real OpenSquilla requires an API key for actual inference.
- **Memory is flat JSON:** No vector search, no relevance ranking — all memory entries are injected into context. This will hit token budget limits as memory grows.
- **MCP is config-only:** The framework generates MCP server JSON but does not start or communicate with MCP servers at runtime in this demo.

## Why It Might Matter

### For Claude-driven products

| Use Case | Relevance |
|---|---|
| **Lead-gen / Sales agents** | Token budgets directly affect cost-per-lead. Compressing prompts by 40-60% at the same quality level cuts API costs proportionally. Skills let you hard-code known operations (scoring, enrichment) without burning tokens. |
| **Marketing / Ad creatives** | Batch generation of ad copy across channels multiplies token usage. Budget-aware agents prevent runaway costs while maintaining output quality across hundreds of variants. |
| **Agent factories** | When spawning many agents (one per customer, one per campaign), token efficiency is the difference between $0.02/agent-run and $0.05/agent-run at scale. Memory persistence avoids re-prompting. |
| **Voice AI** | Real-time voice agents have strict latency requirements. Fewer tokens = faster time-to-first-token. Prompt compression reduces both cost and latency. |
| **MCP tool orchestration** | Declarative MCP config means agents can be shipped with their tool dependencies as JSON, making deployment reproducible across environments. |

### Cost math

At Anthropic's Sonnet pricing (~$3/M input tokens), compressing a 1000-token prompt to 400 tokens saves $1.80 per 1000 calls. At 100K calls/month, that is $180/month saved from prompt compression alone.
