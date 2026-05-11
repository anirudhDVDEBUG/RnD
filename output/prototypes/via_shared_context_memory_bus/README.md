# Via — Shared Context & Memory Bus for AI Tools

**One-liner:** Via is an MCP server that gives Claude Code, Cursor, Windsurf, and any other AI tool a shared memory, task list, and context bus — so decisions made in one tool are instantly visible in all others.

## Headline Result

```
  Memory entries:  3    (architectural decisions stored by Claude Code)
  Tasks tracked:   3    (created across Claude Code, Cursor, Windsurf)
  Context entries: 4    (cross-tool findings, questions, decisions)

  All data persisted to .via_data.json
  Any MCP-compatible tool can connect and see this shared state.
```

Three AI tools sharing one brain. No API keys, no cloud — just a local MCP bus.

## Quick Start

```bash
bash run.sh
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
