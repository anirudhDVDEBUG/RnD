# Technical Details — Hermes Code Bridge

## What it does

Hermes Code Bridge is a Python package that turns
[Hermes Agent](https://github.com/xuyang-liu16/hermes-code-bridge) into a
**control plane for local CLI coding agents**. Given a high-level coding task
(e.g., "build a dashboard"), it:

1. **Decomposes** the task into subtasks using an LLM planner.
2. **Selects** the best-fit CLI agent for each subtask (Claude Code for
   architecture, Codex for boilerplate, Gemini CLI for data work, etc.).
3. **Dispatches** each subtask to the selected agent via subprocess.
4. **Merges** results back into a unified output.

The key insight is treating each coding agent as a *tool* with different
strengths, rather than using a single agent for everything. Hermes acts as the
"brain" that decides which tool to use and when.

## Architecture

```
                    +-----------------+
  User prompt --->  |  Hermes Agent   |  (control plane / LLM planner)
                    |  - decompose()  |
                    |  - select()     |
                    |  - dispatch()   |
                    |  - merge()      |
                    +--------+--------+
                             |
              +--------------+--------------+
              |       |       |      |      |
           Claude   Codex   Kimi  Open   Gemini
           Code     CLI     Code  Code    CLI
              |       |       |      |      |
              v       v       v      v      v
          (subprocess calls to each agent's CLI)
```

### Key files (in the real repo)

| File / Module | Purpose |
|--------------|---------|
| `hermes_code_bridge/` | Main Python package |
| `hermes_code_bridge/agents/` | Agent profiles, CLI wrappers, availability checks |
| `hermes_code_bridge/planner.py` | LLM-based task decomposition |
| `hermes_code_bridge/router.py` | Agent selection / scoring logic |
| `hermes_code_bridge/executor.py` | Subprocess dispatch, timeout handling |
| `hermes_code_bridge/merger.py` | Result aggregation |
| `setup.py` / `pyproject.toml` | Package metadata |

### Data flow

1. **Input**: Natural-language prompt string.
2. **Planner** calls an LLM (e.g., Claude or GPT) to break the prompt into
   a `TaskPlan` with subtask descriptions and tags.
3. **Router** scores each available agent against subtask tags (keyword
   overlap + optional user preference weights) and picks the top match.
4. **Executor** spawns the agent CLI as a subprocess
   (`subprocess.run(["claude", "--print", subtask_prompt])`), captures stdout,
   and enforces a per-task timeout.
5. **Merger** collects all subtask outputs, deduplicates file changes, and
   presents a unified diff or summary.

### Dependencies

- **Python 3.10+** (stdlib only for the core; optional `pyyaml` for config)
- **At least one CLI agent binary** on `PATH`
- **LLM API access** for the planner step (Anthropic or OpenAI key)

### Model calls

The planner step makes 1 LLM call per orchestration request (to decompose the
task). Each agent CLI then makes its own model calls internally. So a typical
5-subtask run = 1 planner call + 5 agent calls.

## Limitations

- **No shared state between agents** — each agent works in isolation on its
  subtask. Cross-agent coordination is limited to the planner's instructions.
- **CLI-only** — agents must have a CLI interface that accepts a prompt and
  returns text. GUI-only tools are not supported.
- **Planner quality** — the decomposition is only as good as the planner LLM.
  Poorly decomposed tasks lead to redundant or conflicting agent work.
- **No conflict resolution** — if two agents edit the same file, the merger
  takes the last write. There is no automatic conflict detection yet.
- **Agent availability** — you need each agent's CLI installed and
  authenticated. If only one agent is available, you lose the multi-agent
  advantage.

## Why this matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Hermes demonstrates a reusable orchestration pattern: decompose-select-dispatch-merge. This is the same pattern used in multi-agent lead-gen pipelines, ad-creative generators, and automated QA systems. |
| **Marketing / ad creatives** | Instead of coding agents, swap in content-generation agents (copy, images, layout). The control-plane architecture is identical. |
| **Voice AI** | Voice-driven dev assistants could use Hermes to route transcribed commands to the right coding agent without the user needing to know which tool to use. |
| **Lead-gen** | Multi-agent orchestration for research tasks (scrape, enrich, score, outreach) follows the same decompose-and-dispatch pattern. |
| **Cost optimization** | Route cheap tasks to cheaper/faster agents (Codex, OpenCode) and reserve expensive agents (Claude) for complex subtasks. |

The transferable lesson: **don't build one monolithic agent — build a control
plane that coordinates specialists.** Hermes Code Bridge is a clean,
open-source reference implementation of this pattern.
