# llm-echo: Mock Model for Testing LLM Pipelines

**TL;DR:** `llm-echo` is a plugin for Simon Willison's `llm` CLI that provides a fake "echo" model — it returns your prompt as JSON instead of calling a real API. This lets you write automated tests for LLM pipelines with zero API keys and zero cost.

## Headline Result

```
$ llm -m echo "What is the capital of France?"
{"prompt": "What is the capital of France?"}
```

No API call. No latency. No cost. Just your prompt echoed back as structured data — ready for assertions in your test suite.

## Quick Start

```bash
bash run.sh
```

This installs dependencies into a local venv and runs a 4-test demo suite covering basic echo, JSON parsing, pipeline mocking, and the Python API.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install steps, skill setup, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, limitations, relevance to Claude-driven products

## Source

- Blog post: [llm-echo 0.5a0 — Simon Willison](https://simonwillison.net/2026/May/5/llm-echo/#atom-everything)
- Repo: [simonw/llm-echo](https://github.com/simonw/llm-echo)
