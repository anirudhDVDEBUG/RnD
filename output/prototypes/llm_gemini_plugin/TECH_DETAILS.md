# Technical Details: llm-gemini 0.32a0

## What it does

`llm-gemini` is a plugin for Simon Willison's [`llm`](https://llm.datasette.io/) CLI tool that connects it to Google's Gemini API. It registers Gemini models (2.5 Pro, 2.5 Flash, 2.0 Flash, 1.5 Pro, etc.) so they can be used with the same `llm` interface used for OpenAI, Claude, Ollama, and dozens of other providers.

The **0.32a0 alpha** release adds a significant new capability: **streaming reasoning tokens**. When using a thinking-capable Gemini model (e.g. `gemini-2.0-flash-thinking`), the plugin now surfaces the model's chain-of-thought tokens in real-time before the final answer. This requires the corresponding `llm>=0.32a0` alpha, which added the reasoning-token protocol that plugins can hook into.

## Architecture

```
User shell
  |
  v
llm CLI (Python, pip-installable, >= 0.32a0)
  |  uses pluggy hook system
  v
llm-gemini plugin (0.32a0)
  |  register_models hook -> adds Gemini model classes
  |  each model class wraps google-generativeai SDK
  |  NEW: yields reasoning tokens via llm's ReasoningToken protocol
  v
Google Gemini API (generativelanguage.googleapis.com)
```

**Key components:**

| Component | Role |
|---|---|
| `llm_gemini.py` | Plugin entry point; registers models via LLM's pluggy hooks |
| `google-generativeai` | Google's official Python SDK; handles HTTP, auth, streaming |
| LLM's SQLite log | All prompts/responses stored locally in `~/.llm/logs.db` |
| `~/.llm/keys.json` | API key storage managed by `llm keys` |

**Data flow (reasoning mode):** User prompt -> LLM CLI parses args -> selects Gemini thinking model -> plugin builds `GenerateContentRequest` with `thinking_config` -> sends to Gemini API -> API streams reasoning chunks -> plugin yields `ReasoningToken` objects -> LLM CLI prints reasoning block -> API streams answer chunks -> plugin yields normal tokens -> LLM CLI prints answer block -> logs everything to SQLite.

**Dependencies:**
- Python 3.9+
- `llm>=0.32a0` (the CLI framework, alpha)
- `google-generativeai` (pulled in by the plugin automatically)

## Limitations

- **API key required** for real usage — no local/offline mode. Free tier has rate limits (15 RPM).
- **Alpha software** — both `llm 0.32a0` and `llm-gemini 0.32a0` are pre-release. The reasoning-token protocol may change before stable release.
- **No function calling / tool use** exposed through the LLM CLI interface (the Gemini API supports it, but LLM's plugin abstraction doesn't surface it yet).
- **No fine-tuning** support — inference-only.
- **Context window** handling is implicit — no warning when you exceed a model's context limit; you get an API error.
- **Reasoning tokens** are only available on thinking-capable models. Standard models (e.g. `gemini-2.0-flash`) return answers without a reasoning block.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Agent factories** | Agents can shell out to `llm -m gemini-2.0-flash-thinking` as a second-opinion reasoning model. The streamed chain-of-thought can be captured and compared against Claude's reasoning for multi-model validation pipelines. |
| **Lead-gen & marketing** | Batch-generate copy variants: `cat prompts.jsonl \| llm -m gemini-2.0-flash --batch`. Compare Gemini output against Claude for A/B testing quality. |
| **Ad creatives** | Gemini's multimodal capabilities (image understanding) complement Claude's text strength. Use llm-gemini in a pipeline that analyzes ad images, then feeds descriptions to Claude for copy generation. |
| **Voice AI** | Fast Gemini Flash responses make it viable as a low-latency fallback for voice pipelines when Claude latency is too high for real-time conversation. |
| **Cost optimization** | For high-volume, lower-stakes tasks (summarization, classification), routing to Gemini via `llm` cuts inference costs while keeping Claude for complex reasoning. The reasoning-token streaming lets you inspect *why* Gemini answered the way it did, enabling better routing decisions. |

## References

- [llm-gemini 0.32a0 announcement](https://simonwillison.net/2026/May/19/llm-gemini/#atom-everything)
- [GitHub: simonw/llm-gemini](https://github.com/simonw/llm-gemini)
- [LLM CLI docs](https://llm.datasette.io/)
