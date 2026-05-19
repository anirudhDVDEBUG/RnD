---
name: awesome_weread_agent_skill
description: |
  Discover and integrate WeRead (微信读书) ecosystem tools. Curated list of projects built on WeChat Reading's official Agent Skill, including MCP servers, note-sync pipelines (Obsidian, Flomo), and reading data utilities.
  Triggers: weread, wechat reading, 微信读书, weread agent skill, weread mcp, reading notes sync
---

# Awesome WeRead Agent Skill

A curated guide for discovering and using projects built on WeChat Reading's (微信读书) official Agent Skill ecosystem.

## When to use

- "Help me set up WeRead note syncing to Obsidian"
- "What MCP servers exist for WeChat Reading / 微信读书?"
- "I want to export my WeRead highlights and annotations"
- "How do I integrate WeRead with my note-taking workflow (Flomo, Obsidian)?"
- "Show me tools built on the WeRead Agent Skill"

## How to use

### 1. Understand the WeRead Agent Skill ecosystem

WeChat Reading (微信读书) released an official Agent Skill on 2026-05-17, enabling programmatic access to reading data — highlights, annotations, bookmarks, and reading progress. A community of derivative projects has emerged around this skill.

### 2. Key ecosystem categories

**MCP Servers**
- WeRead MCP servers expose reading data (highlights, notes, bookshelf) to AI agents via the Model Context Protocol
- Look for repos tagged `mcp-server` + `weread` on GitHub

**Note Sync Pipelines**
- **Obsidian integration**: Sync WeRead highlights/annotations into Obsidian vaults as structured markdown
- **Flomo integration**: Push reading notes to Flomo for spaced review and knowledge management
- Custom sync scripts for other note-taking tools

**Reading Data Utilities**
- Export highlights and annotations in various formats (Markdown, JSON, CSV)
- Reading statistics and progress dashboards
- Book metadata extraction

### 3. Getting started with a WeRead integration

1. **Check the curated list** at the awesome-weread repository for vetted projects
2. **Choose your integration target** (Obsidian, Flomo, custom pipeline)
3. **Install the chosen tool** — most are JavaScript/Node.js based:
   ```bash
   git clone <chosen-project-url>
   cd <project>
   npm install
   ```
4. **Configure WeRead authentication** — follow the specific project's auth setup (typically cookie-based or token-based)
5. **Run the sync or start the MCP server** per project instructions

### 4. For MCP server integration with Claude

If using a WeRead MCP server with Claude Code:
1. Install the MCP server package
2. Add it to your Claude Code MCP configuration in `~/.claude/settings.json`:
   ```json
   {
     "mcpServers": {
       "weread": {
         "command": "node",
         "args": ["path/to/weread-mcp-server/index.js"],
         "env": {
           "WEREAD_TOKEN": "your-token-here"
         }
       }
     }
   }
   ```
3. Restart Claude Code to pick up the new MCP server

## References

- **Source repository**: [BENZEMA216/awesome-weread](https://github.com/BENZEMA216/awesome-weread) — Curated projects built on WeRead's official Agent Skill
- **Topics**: agent-skills, awesome-list, claude-skills, flomo, mcp, mcp-server, obsidian, wechat-reading, weread
- **Language**: JavaScript
