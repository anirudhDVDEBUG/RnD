# How to Use llm-gemini 0.32a0

## Install

```bash
# 1. Install the LLM CLI tool (alpha for reasoning-token support)
pip install 'llm>=0.32a0'

# 2. Install the Gemini plugin alpha
llm install llm-gemini==0.32a0

# 3. Set your Gemini API key (free at https://aistudio.google.com/)
llm keys set gemini
# Paste your key when prompted
```

No other dependencies. Works on Linux, macOS, Windows (WSL).

## This is an LLM CLI Plugin

This is **not** a Claude Skill or MCP server by default. It's a plugin for the standalone [`llm`](https://llm.datasette.io/) CLI tool by Simon Willison. You invoke it directly from your terminal:

```bash
llm -m gemini-2.0-flash-thinking "Your prompt here"
```

### Using as a Claude Skill (optional)

If you want Claude Code to know how to invoke llm-gemini on your behalf, drop the skill file:

```bash
mkdir -p ~/.claude/skills/llm_gemini_plugin
cp SKILL.md ~/.claude/skills/llm_gemini_plugin/SKILL.md
```

Trigger phrases that activate the skill:
- "Use Gemini with the llm CLI tool"
- "Install the llm-gemini plugin for reasoning token streaming"
- "Stream reasoning tokens from Gemini via llm"
- "Set up Gemini models in llm"
- "Configure llm to use Google Gemini API"

## First 60 Seconds

After install, here's input-to-output in under a minute:

### 1. Verify the plugin is installed

```
$ llm plugins
[{"name": "llm-gemini", "version": "0.32a0", ...}]
```

### 2. List Gemini models

```
$ llm models list | grep gemini
gemini-2.5-pro            gemini   1M ctx, thinking
gemini-2.5-flash          gemini   1M ctx, thinking
gemini-2.0-flash          gemini   1M ctx
gemini-2.0-flash-thinking gemini   1M ctx, CoT streaming  <-- KEY MODEL
gemini-2.0-flash-lite     gemini   1M ctx, fast
```

### 3. Basic prompt

```
$ llm -m gemini-2.0-flash "Explain quantum computing in one paragraph"
Quantum computing leverages quantum mechanical phenomena...
```

### 4. Reasoning token streaming (the headline feature)

```
$ llm -m gemini-2.0-flash-thinking "Prove there are infinitely many primes"

[reasoning]
  I need to prove there are infinitely many primes...
  The classic proof is by Euclid — a proof by contradiction...
  Assume there are finitely many primes: p1, p2, ..., pn...
  Consider N = p1 * p2 * ... * pn + 1...
[/reasoning]

[answer]
**Theorem.** There are infinitely many prime numbers.
**Proof (Euclid).** Suppose, for contradiction, that there are only
finitely many primes...
[/answer]
```

The reasoning tokens stream in real-time — you see the model's chain-of-thought as it generates, not just the final answer.

### 5. Pipe content in

```
$ cat myfile.py | llm -m gemini-2.0-flash "Review this code for bugs"
```

### 6. Continue a conversation

```
$ llm -c "Now simplify the proof"
```

## Running the Demo (no API key)

```bash
bash run.sh
```

This runs a mock demo showing the full workflow with simulated reasoning token streaming.

## Upgrading

```bash
llm install -U llm-gemini
```
