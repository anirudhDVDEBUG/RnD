# How to Use brain.md

## Install (real server)

brain.md requires [Bun](https://bun.sh) as its runtime.

```bash
# 1. Install Bun
curl -fsSL https://bun.sh/install | bash

# 2. Clone and install brain.md
git clone https://github.com/mi4uu/brain.md.git
cd brain.md
bun install
```

## Configure as MCP Server for Claude Code

Add this JSON block to your **`~/.claude.json`** under `mcpServers`:

```json
{
  "mcpServers": {
    "brain-md": {
      "command": "bun",
      "args": ["run", "/absolute/path/to/brain.md/src/index.ts"],
      "env": {
        "BRAIN_MD_ROOT": "/absolute/path/to/your/notes"
      }
    }
  }
}
```

Replace both paths with your actual locations. `BRAIN_MD_ROOT` is the folder containing your markdown notes.

For **Claude Desktop**, add the same block to `claude_desktop_config.json`.

For **project-level** config, put it in `.claude/settings.json` inside your repo.

## First 60 Seconds

After adding the MCP config and restarting Claude Code:

```
You:    "Search my notes for anything about API design"
Claude: [calls brain_search with query "API design"]
        → Found 2 results:
          1. projects/api-design.md (score: 0.91)
          2. projects/deployment-checklist.md (score: 0.23)

You:    "Create a note summarizing today's standup"
Claude: [calls brain_create_note]
        → Created journal/2026-05-29-standup.md

You:    "What tags exist across my notes?"
Claude: [calls brain_list_tags]
        → architecture, api, rest, devops, deployment, ci-cd, ai, embeddings
```

All 16 tools are available immediately. The vector index builds automatically on first startup (takes a few seconds depending on vault size).

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `brain_list_notes` | List all notes (respects folder permissions) |
| `brain_read_note` | Read a single note by path |
| `brain_create_note` | Create a new markdown note |
| `brain_update_note` | Update/append to a note |
| `brain_delete_note` | Delete a note |
| `brain_search` | Semantic vector search across all notes |
| `brain_search_by_tag` | Find notes by frontmatter tag |
| `brain_list_tags` | List all tags in the vault |
| `brain_move_note` | Move/rename a note |
| `brain_list_folders` | List folders in the vault |
| `brain_get_metadata` | Get frontmatter metadata for a note |
| `brain_set_metadata` | Update frontmatter fields |
| `brain_get_backlinks` | Find notes linking to a given note |
| `brain_get_links` | Get outbound links from a note |
| `brain_reindex` | Force rebuild of the vector index |
| `brain_get_stats` | Vault statistics (note count, size, etc.) |

## MCP Resources

| Resource URI | Description |
|---|---|
| `brain://index` | Full note index with paths, titles, tags |
| `brain://stats` | Vault statistics |

## Running the Demo (no install needed)

```bash
bash run.sh
```

This runs a pure-Python simulation of the MCP tools against a sample vault. No Bun, no API keys, no external dependencies.

## Per-Folder Permissions

Configure which folders the MCP server can access by setting permissions in the brain.md config. Example:

- `projects/` → read + write
- `archive/` → read only
- `private/` → blocked entirely

This prevents AI agents from accessing sensitive notes.
