# How to Use Hermes Code Bridge

## Install the real project

```bash
# 1. Clone
git clone https://github.com/xuyang-liu16/hermes-code-bridge.git
cd hermes-code-bridge

# 2. Install (editable mode)
pip install -e .
```

### Prerequisites

- Python 3.10+
- At least one supported CLI agent installed:
  - **Claude Code**: `npm install -g @anthropic-ai/claude-code`
  - **Codex**: `npm install -g @openai/codex`
  - **Kimi Code**: see [Moonshot docs](https://platform.moonshot.cn/)
  - **OpenCode**: `go install github.com/opencode-ai/opencode@latest`
  - **Gemini CLI**: `npm install -g @anthropic-ai/gemini-cli` or via Google Cloud SDK

## This is a Python package (not a Claude Skill or MCP server)

Hermes Code Bridge is a standalone Python CLI/library. You invoke it directly:

```bash
# After pip install -e .
hermes-bridge run "Build a full-stack dashboard with auth"
```

Or import it in Python:

```python
from hermes_code_bridge import orchestrate
result = orchestrate("Refactor the payment module")
```

### If you want to reference it as a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/hermes_code_bridge
cp SKILL.md ~/.claude/skills/hermes_code_bridge/SKILL.md
```

**Trigger phrases**: "orchestrate coding agents", "hermes agent",
"multi-agent coding", "coordinate CLI agents", "hermes code bridge"

## First 60 seconds

### 1. Run the local demo (no keys needed)

```bash
bash run.sh
```

**Input**: Three hardcoded prompts simulating real coding tasks.

**Output**:

```
======================================================================
  Hermes Code Bridge — Multi-Agent Orchestration Demo
======================================================================

TASK: Build a full-stack web app with user auth and dashboards
  Strategy : parallel
  Agents   : Claude Code, Codex CLI, Gemini CLI, OpenCode
  Time     : 412 ms

  [1] Design API schema
      Agent: Claude Code  Tags: ['architecture', 'documentation']
      -> [Claude Code] Completed 'Design API schema' ... via `claude --print`

  [2] Scaffold frontend
      Agent: Codex CLI  Tags: ['frontend', 'boilerplate']
      -> [Codex CLI] Completed 'Scaffold frontend' ... via `codex --quiet`
  ...
```

### 2. Try with the real repo

```bash
git clone https://github.com/xuyang-liu16/hermes-code-bridge.git
cd hermes-code-bridge
pip install -e .

# Make sure at least one agent CLI is on your PATH
hermes-bridge run "Fix the bug in my async task queue"
```

Hermes will decompose the task, pick agents, dispatch via subprocess, and
collect results.

## Configuration

The bridge reads agent availability from your `PATH`. If an agent CLI binary
is not found, it is marked `available: false` and skipped during selection.

You can override agent preferences in a config file:

```yaml
# ~/.hermes-bridge.yaml (example)
preferred_agents:
  - claude-code
  - codex
strategy: parallel   # or sequential
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `hermes-bridge: command not found` | Run `pip install -e .` in the cloned repo |
| Agent not dispatched | Ensure the agent CLI is installed and on `PATH` |
| Slow execution | Switch `strategy: sequential` to `parallel` |
