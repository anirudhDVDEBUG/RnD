---
name: opus_compatibility_scanner
description: |
  Audits CLAUDE.md, AGENTS.md, subagents, settings.json, hooks, and Anthropic SDK call sites for Claude Opus 4.6 to 4.7 compatibility issues. Covers 70+ patterns including deprecated model IDs, removed API parameters, changed hook behaviors, MCP configuration changes, and SDK breaking changes.
  TRIGGER when: user mentions "upgrade to opus 4.7", "compatibility check", "migration scan", "opus breaking changes", "check my project for opus 4.7 issues"
---

# Opus Compatibility Scanner

Scan your Claude Code project for compatibility issues when migrating from Claude Opus 4.6 to Opus 4.7.

## When to use

- "Scan my project for Opus 4.7 compatibility issues"
- "Check if my CLAUDE.md and settings are compatible with the new Opus"
- "Audit my Anthropic SDK calls for breaking changes in 4.7"
- "What do I need to change before upgrading to Opus 4.7?"
- "Run a migration check on my Claude Code configuration"

## How to use

1. **Scan configuration files** — Check `CLAUDE.md`, `AGENTS.md`, and `.claude/settings.json` for deprecated directives, removed options, and changed behaviors between Opus 4.6 and 4.7.

2. **Audit SDK call sites** — Search for Anthropic SDK imports (`anthropic`, `@anthropic-ai/sdk`, `claude_agent_sdk`) and flag deprecated model IDs (e.g., `claude-opus-4-6-20250115` → `claude-opus-4-7-*`), removed parameters, and changed response shapes.

3. **Check hooks and subagents** — Inspect hook definitions in `settings.json` and any subagent configurations for compatibility with the new event model and permission system in 4.7.

4. **Review MCP server configs** — Validate MCP tool definitions and server configurations against 4.7's updated MCP protocol requirements.

5. **Generate a report** — Produce a categorized list of issues found:
   - **Critical**: Will break immediately (removed APIs, renamed model IDs)
   - **Warning**: Behavior changed (different defaults, deprecated but still functional)
   - **Info**: Recommended updates (new best practices, performance improvements)

### Pattern categories scanned (70+ patterns)

- Model ID references (`claude-opus-4-6` variants)
- Deprecated API parameters and response fields
- Changed `settings.json` schema keys
- Hook event name changes
- MCP protocol version mismatches
- Subagent configuration format changes
- Permission model updates
- Token counting and context window differences
- Tool use schema changes
- Streaming protocol updates

### Example usage

```
Scan this project for Opus 4.7 compatibility:
- Check all .md config files
- Check settings.json and hooks
- Check any Python/TypeScript files using the Anthropic SDK
- Report issues by severity
```

## References

- Source: https://github.com/readysolutionsai/opus-compatibility-scanner
- License: MIT
- Tags: claude-skill, compatibility-scanner, migration-tool, claude-code, version-upgrade
