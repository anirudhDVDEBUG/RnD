# Tech Details: Claude Code Swarm Toolkit

## What it actually does

This is a **skill file** (structured markdown prompt) that instructs Claude Code to use its built-in Agent tool in coordinated parallel patterns. When triggered, Claude Code:

1. Analyzes the user's request for parallelizable subtasks
2. Identifies independent work units with clear file/module boundaries
3. Dispatches multiple Agent tool calls simultaneously (Claude Code natively supports parallel tool calls)
4. Collects outputs, checks for conflicts, and merges results

There is no runtime code, no external service, no additional API calls beyond what Claude Code already makes. The skill works by teaching Claude Code *when* and *how* to use its existing Agent tool in swarm patterns rather than sequentially.

## Architecture

```
User prompt
    |
    v
[Skill activation] — pattern matching on trigger phrases
    |
    v
[Task decomposition] — identify N independent subtasks
    |
    v
[Parallel dispatch] — N simultaneous Agent tool calls
    |         |         |
    v         v         v
 Agent 1   Agent 2   Agent 3   (each scoped to specific files)
    |         |         |
    v         v         v
[Result collection] — gather outputs
    |
    v
[Conflict resolution] — check shared types, imports, interfaces
    |
    v
[Validation] — run tests/linting across all changes
```

### Key files

- `SKILL.md` — The entire skill definition (single file, ~80 lines of instruction)
- No runtime dependencies, no config files, no build step

### Data flow

1. Trigger phrase detected → skill instructions loaded into context
2. Claude Code follows decomposition protocol from skill
3. Each Agent tool call gets an isolated prompt with file boundaries
4. Results stream back as each agent completes
5. Main Claude Code instance merges and validates

### Dependencies

- Claude Code (with Agent tool support — standard in all recent versions)
- No pip packages, no npm modules, no external APIs

## Limitations

- **Not real parallelism at the API level** — Claude Code's Agent tool calls may execute concurrently or sequentially depending on the SDK version and rate limits. The skill optimizes for the parallel case but degrades gracefully.
- **No shared state** — Agents cannot communicate mid-task. If subtask B depends on subtask A's output, use the Pipeline pattern (sequential), not Fan-out.
- **Context window per agent** — Each subagent gets its own context window but cannot see what other agents are doing. Cross-cutting concerns must be handled in the merge step.
- **3-5 agent practical limit** — More agents increase merge complexity and conflict probability. The skill recommends capping at 5.
- **No persistence** — No memory of previous swarms. Each invocation is stateless.
- **Edit conflicts** — If two agents touch the same file (even different functions), the second write may overwrite the first. The skill mitigates this by enforcing file boundaries in prompts.

## Why this matters for Claude-driven products

| Use case | Application |
|----------|-------------|
| **Agent factories** | Template for orchestrating multi-agent workflows — same pattern applies to any "spawn N workers" architecture |
| **Lead-gen / Marketing** | Parallelize research across multiple prospect companies, competitor analyses, or content generation for different channels |
| **Ad creatives** | Fan-out to generate variations (copy, image prompts, landing pages) simultaneously instead of sequentially |
| **Voice AI** | Pipeline pattern: transcribe → extract intent → generate response → synthesize — each stage as a specialized agent |
| **Code automation** | The primary use case — refactor, test, document across modules in parallel |

The core insight is **decomposition + parallel dispatch + merge** — a pattern that transfers to any domain where Claude agents do independent work. This skill is a reference implementation of that pattern inside Claude Code itself.
