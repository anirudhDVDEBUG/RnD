# Technical Details: DeepSeek Loop Agent

## What it does

DeepSeek Loop Agent is a CLI that runs a **tool-using agent loop** over the DeepSeek chat API. It sends a prompt to DeepSeek, parses any tool-call requests from the response, executes those tools locally, feeds the results back, and repeats until the model produces a final text answer or hits a turn limit. The loop pattern is identical to how Claude Code operates — but with DeepSeek as the LLM backend instead of Anthropic's API.

The original implementation is in Rust (single binary, fast startup). This prototype reimplements the same architecture in Python for rapid evaluation.

## Architecture

```
User prompt
    │
    ▼
┌─────────────┐     ┌──────────────┐
│  AgentLoop   │────▶│ DeepSeek API │  (or MockClient for offline)
│              │◀────│  /v1/chat    │
│  - messages  │     └──────────────┘
│  - turns     │
│  - events    │
└──────┬──────┘
       │ tool_calls[]
       ▼
┌─────────────┐
│ ToolRegistry │
│  file_read   │
│  file_write  │
│  bash        │
│  grep        │
│  glob        │
└──────┬──────┘
       │ results
       ▼
  (back to AgentLoop → next DeepSeek call)
```

### Key files

| File | Purpose |
|------|---------|
| `deepseek_loop.py` | Core agent loop, SdkMessage events, permission checks |
| `tools.py` | Built-in tool implementations and registry |
| `mock_deepseek.py` | Mock client (scripted responses) + real DeepSeek API client |
| `cron_scheduler.py` | Cron expression parser and interval-based scheduler |
| `cli.py` | CLI entry point with argparse (mirrors Rust binary's flags) |

### Data flow

1. **CLI** parses args → constructs `AgentLoop` with permission mode + model
2. **AgentLoop.run()** sends `[system, user]` messages to DeepSeek
3. DeepSeek responds with `content` + optional `tool_calls[]`
4. If tool calls present: **ToolRegistry.execute()** runs each tool, appends results as `tool` messages
5. Loop back to step 2 until no tool calls (pure text response) or max turns
6. Each step emits **SdkMessage** events (text, tool_use, tool_result, done, error)

### Dependencies

- **Python 3.10+** (stdlib only — no pip packages)
- Real API calls use `urllib.request` (no `requests` needed)
- Original Rust version: `tokio`, `reqwest`, `serde`, `clap`

## Limitations

- **No streaming tokens**: The Python prototype uses non-streaming API calls. The Rust original supports SSE token streaming.
- **No interactive permission prompts**: In mock/demo mode, all tools are auto-allowed. The Rust version has a real terminal prompt.
- **Limited cron parser**: Supports basic cron fields (`*`, `*/N`, `N`, `N-M`, `N,M`) but not all edge cases (e.g., `L`, `W`, `#`).
- **No persistent state**: The agent loop doesn't persist conversation history across runs. Each invocation starts fresh.
- **DeepSeek tool-use quality**: DeepSeek's function-calling accuracy varies by model version. The `deepseek-chat` model supports tools but may hallucinate tool schemas compared to Claude or GPT-4.
- **No sandboxing**: Bash tool executes commands directly — no Docker isolation or chroot.

## Why it matters

For teams building Claude-driven products (agent factories, lead-gen, marketing automation):

- **Cost arbitrage**: DeepSeek models are significantly cheaper per token than Claude or GPT-4. For high-volume agent tasks (cron-scheduled scans, bulk content analysis), this can reduce costs 5-10x.
- **Architecture portability**: The agent loop pattern (prompt → tool calls → results → repeat) is model-agnostic. This project proves you can swap the LLM backend while keeping the same tool interface and permission model.
- **Hybrid deployments**: Use Claude for high-stakes decisions and DeepSeek for routine automated loops (log monitoring, status checks, data gathering) — same tool set, different cost tiers.
- **Self-hosted option**: DeepSeek models can run on local GPUs. Combined with this agent loop, you get a fully offline Claude-Code-like agent with no API dependency.
