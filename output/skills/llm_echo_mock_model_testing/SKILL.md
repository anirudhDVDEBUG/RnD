---
name: llm_echo_mock_model_testing
description: |
  Use llm-echo, a fake/mock model plugin for Simon Willison's LLM CLI tool, to write automated tests without calling real LLM APIs.
  TRIGGER: user wants to test LLM pipelines, mock LLM responses, write automated tests for LLM-based code, or use a fake model with the `llm` CLI tool.
---

# llm-echo: Mock Model for LLM Testing

llm-echo is a plugin for [Simon Willison's LLM CLI](https://llm.datasette.io/) that provides a fake model called `echo`. Instead of calling a real LLM, it echoes back the prompt as JSON — making it ideal for automated testing of LLM pipelines and workflows.

## When to use

- "I need a mock model to test my LLM pipeline without making real API calls"
- "How do I write automated tests for code that uses the `llm` CLI?"
- "I want a fake LLM model that echoes back my prompt for testing"
- "How can I test LLM reasoning/thinking block handling without a real model?"
- "Set up a test harness for LLM-based automation"

## How to use

### 1. Install llm-echo

```bash
# Install as an LLM plugin
llm install llm-echo

# Or run ephemerally with uvx
uvx --with llm --with llm-echo llm -m echo "hello world"
```

### 2. Basic usage — echo back a prompt

```bash
# The echo model returns JSON echoing your prompt
llm -m echo "What is the capital of France?"
```

The model does not call any external API. It simply returns a JSON representation of the prompt it received.

### 3. Test reasoning/thinking blocks (v0.5a0+)

As of version 0.5a0, llm-echo supports faking reasoning/thinking blocks, useful for testing against LLM 0.32a0+:

```bash
# Fake a reasoning block (output to stderr) before the echo response
uvx --with llm==0.32a1 --with llm-echo==0.5a0 llm -m echo "hi" -o thinking 1
```

This outputs a simulated reasoning block to standard error before returning the echoed JSON to standard output — useful for testing code that handles extended thinking responses.

### 4. Use in automated test scripts

```bash
#!/bin/bash
# Example: verify your LLM wrapper script handles output correctly
result=$(llm -m echo "test input")
if echo "$result" | grep -q "test input"; then
  echo "PASS: prompt was echoed correctly"
else
  echo "FAIL: unexpected output"
  exit 1
fi
```

### 5. Use in Python tests with the LLM library

```python
import llm

# Get the echo model (llm-echo must be installed)
model = llm.get_model("echo")
response = model.prompt("test prompt")
result = response.text()
# result contains JSON echoing the prompt — assert against it
assert "test prompt" in result
```

## Key details

- **Model name:** `echo`
- **Current version:** 0.5a0 (alpha)
- **Requires:** LLM CLI (`llm` package)
- **Thinking option:** `-o thinking 1` fakes a reasoning block (requires LLM >= 0.32a0)
- **No API keys needed** — runs entirely locally

## References

- [Blog post: llm-echo 0.5a0 — Simon Willison](https://simonwillison.net/2026/May/5/llm-echo/#atom-everything)
- [GitHub: simonw/llm-echo](https://github.com/simonw/llm-echo)
- [LLM CLI documentation](https://llm.datasette.io/)
