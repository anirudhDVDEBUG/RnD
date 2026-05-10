# Tech Details: Browse Anthropic Skills Marketplace

## What it does

This prototype is a local CLI browser for the Anthropic Agent Skills catalog at `anthropics/skills` on GitHub (browsable at `skills.sh/b/anthropics/skills`). It bundles a snapshot of the official skill catalog and exposes functions to list categories, search by keyword, view skill details, and generate platform-specific install instructions for Claude Code, Claude.ai, and the API.

The underlying **skill** (`browse-anthropic-skills-marketplace`) is designed to be loaded into Claude Code so that conversational prompts like "find a skill for PDF generation" trigger an automated browse-and-install workflow — no manual GitHub browsing required.

## Architecture

```
skills_browser.py          # Single-file implementation (~200 lines)
├── CATALOG (list[dict])   # Embedded skill metadata snapshot
├── list_categories()      # Returns unique category names
├── list_skills(cat?)      # Returns skills, optional category filter
├── search_skills(query)   # Full-text search across name/desc/triggers
├── get_skill_detail(name) # Lookup by exact skill name
├── install_instructions() # Generates install steps per platform
└── run_demo()             # End-to-end CLI demonstration
```

**Key files:**
- `skills_browser.py` — all logic, zero external dependencies
- `run.sh` — entrypoint, calls `python3 skills_browser.py`
- `requirements.txt` — empty (stdlib only)

**Data flow:** Catalog is hardcoded → functions filter/search in-memory → output is printed to stdout or returned as dicts/strings.

**Dependencies:** Python 3.8+ stdlib only (`json`, `textwrap`, `dataclasses`). No network calls, no API keys.

## Limitations

- **Static catalog:** The embedded snapshot covers 12 representative skills. The live `anthropics/skills` repo may have more. A production version would fetch from the GitHub API.
- **No actual install:** The tool generates install *instructions* but does not execute `git clone` or copy files. This is intentional for safety in a demo context.
- **No SKILL.md parsing:** Does not fetch or parse the actual `SKILL.md` files from GitHub; metadata is pre-extracted.
- **No authentication:** GitHub API rate limits apply if extended to live fetching (60 req/hr unauthenticated).

## Why it matters

For teams building Claude-driven products:

- **Agent factories:** Skills are the plugin system for Claude agents. Browsing and installing skills programmatically is the first step toward building agent factories that auto-configure themselves with the right capabilities.
- **Lead-gen / marketing:** Skills like `email-campaign` and `brand-guidelines` enable automated content production pipelines. Knowing what's available in the official catalog helps teams avoid reinventing existing tools.
- **Ad creatives:** The `svg-art` and `ui-design-to-html` skills can feed creative asset generation workflows.
- **Voice AI / MCP:** The `create-mcp-server` skill is directly relevant to anyone building tool-using agents — it scaffolds the server-side infrastructure that voice or chat agents connect to.

The skill marketplace is Anthropic's answer to "what can Claude do out of the box?" — and this browser makes the answer discoverable.
