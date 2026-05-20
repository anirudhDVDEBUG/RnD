---
name: llm-gemini Plugin
description: |
  Install and use the llm-gemini plugin to access Google Gemini models via Simon Willison's LLM CLI tool, including streaming reasoning tokens.
  TRIGGER when: user wants to use Gemini models with the LLM CLI, install llm-gemini, stream reasoning tokens from Gemini, or configure Gemini API access through the llm tool.
  DO NOT TRIGGER when: user is using the Gemini API directly, using Google's official SDK, or working with non-LLM CLI tools.
---

# llm-gemini Plugin

Use the `llm-gemini` plugin to access Google Gemini models through the [LLM](https://llm.datasette.io/) command-line tool by Simon Willison.

## When to use

- "How do I use Gemini with the llm CLI tool?"
- "Install the llm-gemini plugin for reasoning token streaming"
- "Set up Gemini models in llm"
- "Stream reasoning tokens from Gemini via llm"
- "Configure llm to use Google Gemini API"

## How to use

### 1. Install LLM and the Gemini plugin

```bash
pip install llm
llm install llm-gemini
```

For the alpha version with reasoning token streaming support:

```bash
pip install llm>=0.32a0
llm install llm-gemini==0.32a0
```

### 2. Configure your Gemini API key

```bash
llm keys set gemini
# Paste your Google AI Studio API key when prompted
```

### 3. Use Gemini models

```bash
# Basic prompt
llm -m gemini-2.0-flash "Explain quantum computing"

# With reasoning/thinking tokens (requires llm>=0.32a0 and llm-gemini>=0.32a0)
llm -m gemini-2.0-flash-thinking "Solve this step by step: what is 247 * 893?"
```

### 4. Stream reasoning tokens

With `llm>=0.32a0` and `llm-gemini>=0.32a0`, reasoning tokens are streamed in real-time, allowing you to see the model's chain-of-thought as it generates.

```bash
llm -m gemini-2.0-flash-thinking "Write a proof that there are infinitely many primes" --no-stream false
```

### Key features of llm-gemini 0.32a0

- Compatible with `llm>=0.32a0` alpha
- Adds ability to stream reasoning tokens from supported Gemini models
- Supports all Gemini model variants available through Google AI Studio

## References

- [llm-gemini 0.32a0 release](https://github.com/simonw/llm-gemini/releases/tag/0.32a0)
- [Source: Simon Willison's Weblog](https://simonwillison.net/2026/May/19/llm-gemini/#atom-everything)
- [LLM CLI documentation](https://llm.datasette.io/)
