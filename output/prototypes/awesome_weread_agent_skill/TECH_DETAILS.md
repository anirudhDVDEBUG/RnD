# Technical Details

## What the source actually does

[BENZEMA216/awesome-weread](https://github.com/BENZEMA216/awesome-weread) is a curated "awesome list" of community projects built on WeChat Reading's (微信读书) official Agent Skill, released on 2026-05-17. The Agent Skill provides programmatic access to a user's WeRead data — highlights, annotations, bookmarks, reading progress, and bookshelf metadata. The awesome-weread repo catalogs derivative tools across three categories: MCP servers (for AI agent integration), note-sync pipelines (Obsidian, Flomo, Notion), and data export utilities.

This demo prototype simulates the ecosystem by providing a mock WeRead data layer and implementing the three core workflows: catalog browsing, Obsidian-format highlight export with backlinks, and MCP server configuration generation. No real WeRead API calls are made — the demo uses realistic mock data so it runs without credentials.

## Architecture

```
weread_demo.py          # Single-file implementation
  |
  +-- CATALOG[]         # In-memory curated project list (6 entries)
  +-- MOCK_BOOKS[]      # Simulated WeRead reading data (3 books, 6 highlights)
  |
  +-- browse_catalog()        -> stdout (formatted catalog)
  +-- reading_stats()         -> stdout (reading statistics)
  +-- export_to_obsidian()    -> output/obsidian_vault/*.md
  +-- export_json()           -> output/weread_export.json
  +-- generate_mcp_config()   -> output/mcp_config_example.json
```

### Key files

| File | Role |
|------|------|
| `weread_demo.py` | All logic: catalog data, mock reading data, export functions |
| `run.sh` | Entry point, cleans output dir, runs demo, lists generated files |
| `SKILL.md` | Claude Code skill definition with trigger phrases |

### Data flow

1. Mock WeRead data (books, highlights, notes) is defined as Python dicts
2. `export_to_obsidian()` transforms each book into an Obsidian-compatible `.md` file with `[[backlinks]]`, blockquoted highlights, and metadata
3. `export_json()` produces a structured JSON export with aggregated stats
4. `generate_mcp_config()` outputs the exact JSON snippet to paste into Claude Code's MCP config

### Dependencies

- Python 3.10+ standard library only (`json`, `pathlib`, `datetime`)
- No external packages, no API keys, no network calls

## Limitations

- **Mock data only**: This demo does not connect to the real WeRead API. Actual WeRead integration requires cookie-based authentication, which varies by project.
- **Catalog is static**: The curated list is hardcoded. The real awesome-weread repo is the living source of truth.
- **No bidirectional sync**: The Obsidian export is one-way (WeRead -> Markdown). Real tools in the ecosystem may support two-way sync.
- **No MCP server runtime**: The demo generates MCP config but doesn't run an actual MCP server. You'd need to install a real WeRead MCP server from the catalog.
- **Chinese ecosystem**: Many projects in the real ecosystem have Chinese documentation. The WeRead platform itself is primarily Chinese-language.

## Why this matters for Claude-driven products

**Agent factories**: The WeRead Agent Skill is a concrete example of a consumer platform shipping an official skill API — a pattern likely to repeat across reading, productivity, and media apps. Teams building agent orchestration can study this ecosystem as a template.

**Knowledge pipelines**: Reading highlights are high-signal personal data. Syncing them into structured formats (Obsidian, Notion) creates knowledge bases that Claude can query via MCP, enabling personalized research assistants grounded in what the user has actually read.

**MCP ecosystem growth**: WeRead MCP servers demonstrate demand for domain-specific MCP connectors beyond developer tools. This signals opportunity for building MCP servers around other consumer data sources (fitness, finance, media consumption).

**Lead-gen / marketing angle**: Products that help knowledge workers capture and organize reading insights have strong adoption loops. A Claude skill that surfaces relevant highlights during writing or research tasks provides immediate, demonstrable value.
