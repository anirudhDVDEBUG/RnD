# How to Use

## This is a Claude Skill

### Install the skill

```bash
mkdir -p ~/.claude/skills/datasette_jump_menu_plugin
cp SKILL.md ~/.claude/skills/datasette_jump_menu_plugin/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code and the skill activates:

- "Add custom items to Datasette's Jump to menu"
- "Create a Datasette plugin with jump_items_sql"
- "Make my Datasette tables searchable from the Jump menu"
- "Build a Datasette plugin for quick search/navigation"

---

## Running the Demo Plugin Directly

### Install

```bash
pip install -r requirements.txt
cd datasette-jump-bookmarks
pip install -e .
```

### Run

```bash
bash run.sh
```

This creates a sample SQLite database with bookmark items, installs the plugin, and launches Datasette on port 8001.

---

## First 60 Seconds

**Input:** Run `bash run.sh` in this directory.

**Output:**
```
Creating sample database with bookmarks...
Installing plugin...
Starting Datasette on http://127.0.0.1:8001
Press / to open the Jump menu, then type to search bookmarks!

Jump menu items registered:
  - Claude Docs -> /bookmarks/claude-docs
  - Datasette Plugins -> /bookmarks/datasette-plugins
  - MCP Specification -> /bookmarks/mcp-spec
  - Agent SDK Guide -> /bookmarks/agent-sdk
  - Simon Willison Blog -> /bookmarks/simonwillison
```

The plugin adds all bookmarks to the Jump menu. Press `/` on any Datasette page and type "claude" to see matching items appear instantly.
