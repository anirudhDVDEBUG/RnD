# How to Use

## Install

Python 3.10+ required. No external packages needed.

```bash
git clone <this-repo>
cd awesome_weread_agent_skill
```

## This is a Claude Skill

Drop the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/awesome_weread_agent_skill
cp SKILL.md ~/.claude/skills/awesome_weread_agent_skill/SKILL.md
```

### Trigger phrases that activate it

- "Help me set up WeRead note syncing to Obsidian"
- "What MCP servers exist for WeChat Reading?"
- "I want to export my WeRead highlights"
- "Show me tools built on the WeRead Agent Skill"
- Keywords: `weread`, `wechat reading`, `微信读书`, `weread mcp`, `reading notes sync`

## MCP Server Integration (from ecosystem)

If you install one of the WeRead MCP servers from the catalog, add this to `~/.claude.json` in the `mcpServers` block:

```json
{
  "mcpServers": {
    "weread": {
      "command": "node",
      "args": ["path/to/weread-mcp-server/index.js"],
      "env": {
        "WEREAD_TOKEN": "your-weread-token-here",
        "WEREAD_COOKIE": "your-weread-cookie-here"
      }
    }
  }
}
```

Then restart Claude Code to pick up the server.

## First 60 Seconds

**Input:**

```bash
bash run.sh
```

**Output (abbreviated):**

```
============================================================
  Awesome WeRead Agent Skill Demo
  WeRead (微信读书) Ecosystem Explorer
============================================================

============================================================
  WeRead Ecosystem Catalog
============================================================

  [MCP Server]
  ──────────────────────────────────────────────────────
  ★  342  weread-mcp-server
         Expose WeRead highlights, bookshelf, and annotations to AI agents via MCP

  [Note Sync]
  ──────────────────────────────────────────────────────
  ★  521  weread-obsidian-sync
         Sync WeRead highlights and annotations into Obsidian vaults
  ★  289  weread-notion-sync
         Two-way sync between WeRead annotations and Notion databases
  ★  198  weread-flomo-bridge
         Push WeRead reading notes to Flomo for spaced review

  [Data Utility]
  ──────────────────────────────────────────────────────
  ★  415  weread-export-cli
         Export highlights and annotations in Markdown, JSON, or CSV formats

============================================================
  Export WeRead Highlights -> Obsidian
============================================================
  [OK] output/obsidian_vault/Thinking_Fast_and_Slow.md  (3 highlights)
  [OK] output/obsidian_vault/The_Design_of_Everyday_Things.md  (2 highlights)
  [OK] output/obsidian_vault/Atomic_Habits.md  (1 highlights)
  [OK] output/obsidian_vault/WeRead_Reading_Log.md  (index)

  Exported 6 highlights from 3 books
```

**Generated files:**

```
output/
  obsidian_vault/
    Thinking_Fast_and_Slow.md      # Obsidian note with highlights + backlinks
    The_Design_of_Everyday_Things.md
    Atomic_Habits.md
    WeRead_Reading_Log.md           # Index with table linking all books
  weread_export.json                # Structured JSON export
  mcp_config_example.json           # Ready-to-paste MCP config
```

Each Obsidian markdown file includes frontmatter-style metadata, blockquoted highlights with chapter/page references, personal notes, and `[[backlinks]]` for Obsidian's graph view.

## Using with Real WeRead Data

To move beyond the demo to real data:

1. Pick a project from the catalog (e.g., `weread-obsidian-sync`)
2. Clone it and follow its auth setup (typically WeRead cookie extraction from browser)
3. Configure your sync target (Obsidian vault path, Flomo API key, etc.)
4. Run the sync on a schedule or manually
