# Technical Details — Prompt Cache Skills

## What It Does

Prompt Cache Skills is a static analyzer for LLM agent prompt structures. It inspects how an agent harness (Claude Code, Aider, Cline, etc.) constructs its API requests and identifies patterns that prevent Anthropic's prompt caching from activating. It then applies automated patches — removing dynamic elements from cached prefixes, reordering messages, and inserting `cache_control` breakpoints — to unlock 50-80% input token cost savings.

This is **not** a runtime proxy or middleware. It's an audit-and-patch tool that modifies the agent's prompt construction code or configuration so that subsequent API calls benefit from caching automatically.

## Architecture

### Key Files

| File | Purpose |
|------|---------|
| `prompt_cache_analyzer.py` | Core library: pattern detectors, harness-specific analyzers, optimizer, report formatter |
| `demo.py` | Standalone demo with 3 mock agent configs (Claude Code, Aider, Generic) |
| `run.sh` | One-command entry point |
| `SKILL.md` | Claude Code skill definition (drop into `~/.claude/skills/`) |

### Data Flow

```
Agent config (dict)
  ├── system_prompt (string)
  ├── tools (list of tool defs)
  ├── messages (conversation history)
  └── harness-specific fields (repo_map, etc.)
        │
        ▼
  ┌─────────────┐
  │  analyze()   │  ← detects issues: dynamic content, bad ordering,
  │              │     missing breakpoints, undersized prefix
  └──────┬──────┘
         │
         ▼
  ┌──────────────────┐
  │ optimize_config() │  ← patches: removes dynamic elements, reorders
  │                    │     messages, adds cache_control breakpoints
  └──────┬────────────┘
         │
         ▼
  Patched config (dict) + AnalysisResult
```

### Detection Patterns

1. **Dynamic content in prefix** — regex scan for `{timestamp}`, `{uuid}`, `{session_id}`, `datetime.now`, `Date.now`, etc.
2. **Message ordering** — system messages must precede user messages for prefix caching
3. **Missing cache breakpoints** — checks for `cache_control: {type: ephemeral}` blocks
4. **Undersized prefix** — warns if cacheable prefix is below the 1,024-token minimum
5. **CLAUDE.md interpolation** — detects dynamic values mixed into CLAUDE.md content

### Dependencies

**None.** Pure Python 3.9+ stdlib (`json`, `re`, `dataclasses`, `copy`). No pip packages required.

### Model Calls

**None.** This is a static analysis tool. It does not call any LLM APIs. It analyzes and patches the *configuration* that gets sent to APIs.

## Limitations

- **Token estimation is approximate** — uses a ~4 chars/token heuristic, not a real tokenizer. For precise counts, use `anthropic`'s token counting API.
- **Does not modify source code** — the optimizer works on config dicts, not on the agent's Python/JS source files. For Aider/Cline, you'd need to apply the suggested patches to their codebase manually.
- **No runtime verification** — cannot confirm cache hits without actual API calls. The tool tells you *what* to fix, but you verify via `cache_read_input_tokens` in API responses.
- **Anthropic-specific** — cache_control breakpoints are an Anthropic API feature. OpenAI-compatible providers may use automatic prefix caching (no breakpoints needed) or not support caching at all.
- **Regex-based detection** — may miss obfuscated dynamic patterns or catch false positives on string literals that look like template variables.

## Why This Matters

For teams building Claude-driven products:

- **Agent factories / automation platforms** — agents with large system prompts (tool definitions, workflow instructions) make dozens of API calls per task. Caching cuts the per-call cost by 90% on the repeated prefix, often saving $50-200/day at scale.
- **Lead-gen and marketing agents** — high-volume pipelines that process hundreds of prospects/day benefit from caching the static persona + instructions prefix.
- **Voice AI** — real-time voice agents need sub-second latency. Cached prefixes reduce time-to-first-token because the model skips re-processing the cached portion.
- **Ad creative generation** — batch workflows generating many variations share the same brand guidelines prefix, making caching especially effective.

The ROI is immediate and compounding: fix the prompt structure once, save on every subsequent API call.
