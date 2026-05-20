# Technical Details: datasette-llm

## What it does

`datasette-llm` is a Datasette plugin that brings LLM prompting capabilities into Datasette via Simon Willison's `llm` library. It lets Datasette instances answer natural-language questions about their data by assembling context (schema, sample rows, metadata) and sending it to a configured LLM model.

The key extensibility mechanism is the `llm_prompt_context()` plugin hook. Any Datasette plugin can implement this hook to inject additional context into LLM prompts -- table schemas, sample data, documentation, business rules, etc. Version 0.1a8 fixed issue #7, where this hook did not fully consume generator/iterable responses, causing context from generator-based plugins to be silently truncated.

## Architecture

```
User question
    |
    v
datasette-llm
    |
    +-- Calls llm_prompt_context() on all registered plugins
    |       Plugin A: returns "schema: ..."        (string)
    |       Plugin B: yields row1, row2, row3      (generator)
    |       Plugin C: returns "hint: ..."          (string)
    |
    +-- Assembles full context from all responses
    |     (v0.1a8 fix: generators are now fully exhausted)
    |
    +-- Sends context + user question to LLM via `llm` library
    |
    v
LLM response (SQL, summary, etc.)
```

**Key files in datasette-llm:**
- Plugin hook registration via Datasette's `pluggy` system
- Uses `llm` library for model abstraction (supports Claude, GPT-4, local models, etc.)
- Context assembly collects string and iterable returns from all `llm_prompt_context()` implementors

**Dependencies:**
- `datasette` (>=0.64)
- `llm` (Simon Willison's LLM CLI/library)
- A model plugin (e.g., `llm-claude-3`, `llm-gpt-4`)
- Python 3.9+

## Limitations

- **Alpha software** (v0.1a8): Hook API may change.
- **Requires API keys**: Real usage needs a configured LLM provider. No built-in free/local model.
- **No built-in UI**: The plugin provides the hook infrastructure; UI is up to consuming plugins or Datasette's own interface.
- **No streaming**: Responses are collected in full before returning.
- **No cost tracking**: Token usage is not logged by datasette-llm itself.

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | datasette-llm's hook system is a pattern for building pluggable LLM context assembly. Agents that query structured data can use the same architecture to let plugins contribute domain knowledge. |
| **Lead-gen / marketing** | Natural-language access to customer databases via Datasette. Non-technical marketers can query lead data without writing SQL. |
| **Ad creatives** | Query performance data in Datasette with natural language, then pipe results to creative generation. The plugin hook lets you inject brand guidelines as context. |
| **Voice AI** | Voice-to-text -> datasette-llm -> SQL results -> text-to-speech. The context hook lets you inject conversation history. |

## References

- [datasette-llm 0.1a8 release](https://simonwillison.net/2026/May/19/datasette-llm/#atom-everything)
- [GitHub: datasette-llm](https://github.com/datasette/datasette-llm)
- [Bug fix: llm_prompt_context() chain collection -- Issue #7](https://github.com/datasette/datasette-llm/issues/7)
- [Simon Willison's llm library](https://github.com/simonw/llm)
