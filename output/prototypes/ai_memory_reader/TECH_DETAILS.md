# Technical Details — AI Memory Reader

## What It Does

AI Memory Reader scans well-known filesystem paths where AI coding agents store persistent memory (preferences, project context, debugging notes, rules). It aggregates these into a single browsable view, giving developers visibility into what their AI tools "remember" without opening each agent's config directory manually.

The original project is a native SwiftUI app for macOS/iOS. This prototype reimplements the core discovery and display logic as a Python CLI for cross-platform portability and scripting.

## Architecture

```
ai_memory_reader.py
├── AgentConfig[]         # Declarative list of agents + their known paths/patterns
├── discover_memory_files()  # Walks directories, glob-matches, reads previews
├── generate_mock_files()    # Creates demo data in .mock_memory/ for testing
├── display_rich()           # Rich library output (tables, trees, panels)
└── display_plain()          # Fallback plain-text output
```

### Data Flow

1. **Config** — `AGENT_CONFIGS` defines agent name, base directories, and file glob patterns
2. **Discovery** — Each base path is expanded (`~` → home), checked for existence, then globbed
3. **Reading** — Files are opened read-only; first 200 bytes captured as preview
4. **Dedup** — Files seen via multiple patterns are deduplicated by absolute path
5. **Display** — Results rendered as summary table + file tree + optional content panels

### Dependencies

| Package | Purpose |
|---------|---------|
| `rich` | Terminal formatting (tables, trees, Markdown rendering) |
| Python 3.10+ | dataclasses, Path, type hints |

No network calls. No API keys. No database. Pure filesystem reads.

## Limitations

- **Path assumptions** — only scans hardcoded default directories; custom agent installs in non-standard locations will be missed
- **Shallow scan** — goes one level deep into subdirectories (not recursive) to avoid scanning large project trees
- **No write/edit** — strictly read-only; cannot modify or delete memory files
- **No semantic search** — just file listing and preview; no embedding-based search across memory content
- **macOS/Linux only** — Windows paths not yet mapped (original app is macOS/iOS only)
- **Preview truncation** — shows first 200 characters only; no full-file viewer in CLI mode

## Why It Matters for Claude-Driven Products

1. **Agent factories** — When deploying multiple Claude Code instances across projects, this tool lets you audit what each instance has learned and ensure CLAUDE.md configs are consistent.

2. **Memory hygiene** — AI agents accumulate stale or incorrect memories. A quick scan reveals outdated preferences or wrong architectural assumptions before they cause problems.

3. **Multi-agent workflows** — If you use Claude Code + Cursor + Codex on the same project, you can compare what each agent "knows" and identify conflicts or gaps.

4. **Compliance/security** — Before sharing a machine or repo, verify that agent memory doesn't contain sensitive data (API keys, credentials, internal URLs) that shouldn't persist.

5. **Lead-gen / marketing context** — For teams building AI-powered tools, understanding the memory model of competing agents informs feature differentiation and integration strategy.
