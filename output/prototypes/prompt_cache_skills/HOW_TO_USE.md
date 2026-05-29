# How to Use — Prompt Cache Skills

## What This Is

A Claude Code **skill** (not an MCP server). It teaches Claude how to audit and patch prompt-caching configurations in any LLM agent harness.

## Install

### Option A: As a Claude Code Skill (recommended)

1. Clone or copy the skill folder:

```bash
mkdir -p ~/.claude/skills/prompt_cache_skills
cp SKILL.md ~/.claude/skills/prompt_cache_skills/SKILL.md
```

2. That's it. Claude Code will pick up the skill automatically.

### Option B: As a standalone Python tool

```bash
git clone https://github.com/OnlyTerp/prompt-cache-skills.git
cd prompt-cache-skills
python3 demo.py
```

No pip install needed — zero external dependencies, Python 3.9+ stdlib only.

## Trigger Phrases

Once the skill is installed, say any of these to Claude Code:

- "Optimize my agent's prompt caching to reduce token costs"
- "Apply prompt-cache patches to my Claude Code setup"
- "Reduce API token usage in my LLM agent pipeline"
- "Set up prompt caching for my coding agent harness"
- "Fix prompt caching configuration for my AI assistant"

Claude will then audit your current setup and suggest/apply patches.

## First 60 Seconds

### Input

```bash
bash run.sh
```

### Output

```
=== Prompt Cache Skills — Demo ===
Running prompt-cache analysis on 3 mock agent configs...

──────────────────────────────────────────────────────────
  Analyzing: Claude Code
──────────────────────────────────────────────────────────
============================================================
  Prompt Cache Analysis: Claude Code
============================================================
  Total tokens (est.):          832
  Cache-eligible tokens (est.):  518
  Estimated savings:             0%
  Issues found:                  4
============================================================

  [!] Issue #1 (HIGH) — system_prompt
      Dynamic timestamp in cached prefix
      Fix: Move dynamic element out of the cached prefix...

  [!] Issue #2 (HIGH) — system_prompt
      Session-specific ID in cached prefix
      Fix: Move dynamic element out of the cached prefix...

  ...

  Applying optimizations...
  Moved 2 dynamic element(s) out of cached prefix.
    - Removed: {timestamp}
    - Removed: {session_id}

  AFTER optimization:
    Issues remaining: 1
    Estimated savings: 56%

  Cost estimate (per turn, Claude 3.5 Sonnet pricing):
    Without caching:  $0.0025 per 1K turns
    With caching:     $0.0011 per 1K turns  (after warm-up)
    Savings:          56%
```

### Using as a Python library

```python
from prompt_cache_analyzer import analyze, optimize_config, format_report

config = {
    "system_prompt": "You are a helpful assistant. Time: {timestamp}",
    "messages": [
        {"role": "user", "content": "Hello"},
    ],
}

result = analyze(config)
print(format_report(result))

patched = optimize_config(config)
# patched["system_prompt"] now has {timestamp} removed
# patched has cache_control breakpoints added
```

## Verification

After applying caching patches to a real agent, check API response headers:

```python
# Look for these fields in the Anthropic API response:
response.usage.cache_creation_input_tokens  # > 0 on first call (cache write)
response.usage.cache_read_input_tokens      # > 0 on subsequent calls (cache hit!)
```

A successful cache hit shows `cache_read_input_tokens > 0` on the second and subsequent requests with the same prefix.
