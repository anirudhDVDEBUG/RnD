# Pi Plugin for Claude Code

**Route code reviews, rescues, and refactoring tasks through the Pi coding agent (DeepSeek V4) — right from Claude Code slash commands.** This plugin adds `/pi:review`, `/pi:rescue`, `/pi:explain`, and `/pi:refactor` commands that forward work to a second AI agent, enabling multi-agent coding workflows.

## Headline Result

```
/pi:review function getUser(id) { ... }

Review Score: 6.5/10
  [error]   Line 41: SQL injection risk — use parameterized queries
  [warning] Line 12: Potential null dereference on user.profile
  [info]    Line 27: Replace magic number 86400 with named constant
```

One slash command, instant second opinion from DeepSeek V4.

## Quick Start

```bash
bash run.sh
```

No API keys needed — the demo uses mock responses to show the full routing flow.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
