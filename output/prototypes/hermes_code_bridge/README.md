# Hermes Code Bridge — Multi-Agent Coding Orchestrator

**One control plane to rule them all.** Hermes Code Bridge lets you orchestrate
multiple CLI coding agents (Claude Code, Codex, Kimi Code, OpenCode, Gemini CLI)
from a single command, routing each subtask to the best-fit agent automatically.

## Headline result

```
TASK: Build a full-stack web app with user auth and dashboards
  Strategy : parallel
  Agents   : Claude Code, Codex CLI, Gemini CLI, OpenCode
  Time     : 412 ms

  [1] Design API schema        -> Claude Code
  [2] Scaffold frontend        -> Codex CLI
  [3] Implement backend        -> OpenCode
  [4] Write tests              -> Claude Code
  [5] Analyze data layer       -> Gemini CLI
```

One prompt in, five agents coordinated, results merged.

## Quick links

| Doc | What you get |
|-----|-------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install steps, config, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations |

## Run the demo

```bash
bash run.sh
```

No API keys required — the demo uses mock dispatch to show the orchestration
pattern end-to-end.
