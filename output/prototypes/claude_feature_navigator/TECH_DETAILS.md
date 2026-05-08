# Technical Details -- Claude Feature Navigator

## What it does

The Claude Feature Navigator is a skill-discovery layer for Claude Code. It maintains an embedded catalog of 18 Claude Code skills and MCP servers sourced from the ComposioHQ/awesome-claude-skills awesome list and the Composio marketplace. When a user asks Claude to find, browse, or recommend skills, the navigator searches this catalog by keyword, category, or workflow type and returns ranked results with install instructions.

The SKILL.md file is pure prompt augmentation -- it teaches Claude a structured procedure for skill discovery. The companion `navigator.py` implements the same logic as a standalone CLI for demo and evaluation purposes.

## Architecture

```
~/.claude/skills/claude_feature_navigator/
  SKILL.md            <- Prompt-based skill (the "app")

navigator.py          <- CLI demo implementing the same catalog + search logic
run.sh                <- Entry point: bash run.sh
```

### Key components

| Component | Role |
|-----------|------|
| **Skill catalog** | 18 entries with name, repo URL, category, description, star count, install type (skill vs MCP), and tags. Embedded as structured data. |
| **Search engine** | Token-based keyword matching across name, description, tags, and category. Results ranked by match score then star count. |
| **Category browser** | Groups skills into 6 categories: Code Quality, DevOps, Documentation, Integrations, Productivity, Testing. |
| **Workflow recommender** | Maps workflow descriptions ("code review", "deployment", "documentation") to pre-curated skill bundles. Falls back to keyword search. |
| **Install generator** | Produces exact shell commands for skills (git clone + cp) or JSON snippets for MCP servers (~/.claude.json config). |

### Data flow

1. User asks Claude to find/recommend skills (trigger phrase matches SKILL.md description)
2. Claude's skill loader injects SKILL.md into context
3. Claude follows the embedded procedure: parse the query, search/filter the catalog, rank results
4. Claude presents results with descriptions, star counts, and install commands
5. No external API calls -- the catalog is embedded in the skill file itself

### Dependencies

- **Runtime:** None. The SKILL.md is a Markdown file consumed by Claude's skill system.
- **Demo CLI:** Python 3.10+ (stdlib only: `json`, `sys`, `textwrap`).

### Model calls

Zero. The skill shapes Claude's behavior through prompt context, not API calls. Claude itself does the reasoning.

## Limitations

- **Static catalog.** The 18 entries are a point-in-time snapshot. New skills require manual catalog updates.
- **No live GitHub data.** Star counts, commit activity, and compatibility checks are embedded, not fetched in real time.
- **Keyword search only.** No semantic/vector search -- relies on token overlap. Unusual phrasings may miss relevant results.
- **No skill verification.** The navigator recommends skills but cannot test them. Users must review SKILL.md source before installing.
- **English only.** Search and category names are English; non-English queries will perform poorly.

## Why this matters for builders

### Lead generation & marketing
A curated skill marketplace is a distribution channel. If you build Claude Code skills, a navigator like this is how users find you. The pattern generalizes to any "awesome list" that needs search + install UX.

### Agent factories
The catalog + search + install pattern is a template for agent tool stores. Replace skills with agent tools, MCP servers, or API connectors and the same architecture powers an agent marketplace.

### Ad creatives & content
Each skill entry (name + one-line description + star count) is structured metadata ready for programmatic ad copy: "Top Claude skill this week: test-gen (870 stars) -- auto-generate unit tests."

### Voice AI
The category browsing and recommendation flow maps to voice-agent dialog: "What kind of task? ... Here are three skills for that. Want me to install the first one?" Natural turn-taking with structured options.

## References

- [Composio Top Claude Skills](https://composio.dev/content/top-claude-skills)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [Anthropic Skills conventions](https://github.com/anthropics/skills)
