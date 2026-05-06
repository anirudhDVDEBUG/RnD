# Technical Details: llm-echo

## What It Does

`llm-echo` is a minimal plugin for Simon Willison's [`llm`](https://llm.datasette.io/) CLI framework. It registers a model called `echo` that, instead of making HTTP calls to an LLM provider, simply serializes the incoming prompt into JSON and returns it. This makes it a deterministic, zero-latency, zero-cost stand-in for any real LLM model — ideal for automated testing of pipelines, wrappers, and integrations built on top of `llm`.

As of version 0.5a0, it also supports faking "reasoning/thinking" blocks (the `thinking` option), which lets you test code that handles extended thinking responses from models like Claude — without spending tokens.

## Architecture

```
llm CLI framework
  └── plugin registry (entry_points)
        └── llm-echo plugin
              ├── EchoModel class (implements llm.Model)
              │     ├── execute() → yields JSON of prompt
              │     └── supports thinking option (-o thinking 1)
              └── registered as model name "echo"
```

**Key files (in the llm-echo repo):**

- `llm_echo.py` — single-file plugin; defines `EchoModel`, hooks into `llm`'s plugin system via `hookimpl`
- `pyproject.toml` — declares the `llm` entry point so `llm install llm-echo` discovers the model

**Data flow:**

1. User runs `llm -m echo "prompt text"`
2. `llm` framework resolves `echo` → `EchoModel`
3. `EchoModel.execute()` serializes the prompt to JSON
4. If `-o thinking 1` is set, a fake reasoning block is emitted to stderr first
5. JSON output is returned to stdout

**Dependencies:**

- `llm` (the only runtime dependency) — itself depends on `click`, `sqlite-utils`, `openai`, etc.
- No additional API keys, network access, or external services required

## Limitations

- **Not a real model** — it doesn't generate meaningful text; it's purely for structural/integration testing
- **No streaming simulation** — output is returned all at once, not token-by-token
- **JSON format may vary** — the exact JSON structure echoed back is an implementation detail and may change between versions
- **Alpha status** — v0.5a0 is pre-release; API/output format is not yet stable
- **Thinking blocks are fake** — the reasoning output is a fixed placeholder, not dynamic content

## Why It Matters for Claude-Driven Products

If you're building products on top of LLM tooling — agent factories, marketing automation, lead-gen pipelines, ad-creative generators, or voice AI systems — you need reliable tests that don't burn API credits or break when rate-limited.

**Concrete use cases:**

- **Agent factories:** Test multi-step agent orchestration logic (routing, retries, output parsing) using `echo` as a stand-in for real models. Validate that your agent framework handles responses correctly before swapping in Claude.
- **Marketing / ad creatives:** Test your prompt templates and output parsers against deterministic responses. Verify that your pipeline correctly extracts structured data from LLM output without paying per-test-run.
- **CI/CD integration:** Add `llm -m echo` tests to your CI pipeline. They run in milliseconds, need no secrets, and catch regressions in your LLM wrapper code.
- **Thinking/reasoning handling:** Test that your code correctly processes extended thinking blocks (stderr) separately from main output (stdout) — critical for Claude-based applications using chain-of-thought.

The pattern is simple: use `echo` in dev/test, swap to `claude-3.5-sonnet` (or whichever model) in production. Your integration tests stay fast, free, and deterministic.
