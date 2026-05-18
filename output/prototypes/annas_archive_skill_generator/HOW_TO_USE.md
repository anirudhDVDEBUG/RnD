# How to Use

## Install

```bash
git clone https://github.com/VKirill/mcp-annas-archive-create-skill.git
cd mcp-annas-archive-create-skill
npm install && npm run build
```

Requires: Node.js 18+, npm.

## Configure

### 1. Get a Gemini API key

Go to [Google AI Studio](https://aistudio.google.com/apikey) and create a key.

### 2. Register the MCP server

Add this to `~/.claude.json` (or project-level `.claude/settings.json`):

```json
{
  "mcpServers": {
    "annas-archive-create-skill": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-annas-archive-create-skill/dist/index.js"],
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
```

Replace `/absolute/path/to/` with the actual clone location.

## Trigger Phrases

Once configured, Claude Code will activate this tool when you say:

- "Extract a methodology from this book and create a skill"
- "Search Anna's Archive for books on [topic] and build a skill"
- "Generate a SKILL.md from a PDF/EPUB book"
- "Download a book and extract its key frameworks into a Claude skill"
- "Turn this book's methodology into an actionable Claude Code skill"

## First 60 Seconds

**Input (in Claude Code):**

```
Use the annas-archive-create-skill tool to find "Deep Work by Cal Newport",
download it, extract the deep work methodology, and generate a SKILL.md.
```

**Output:**

The MCP server will:
1. Search Anna's Archive for "Deep Work Cal Newport"
2. Download the best-matching PDF/EPUB
3. Send book content to Gemini for methodology extraction
4. Generate a structured SKILL.md file

Result appears as a complete skill file:

```yaml
---
name: deep_work_methodology
description: |
  Apply Cal Newport's Deep Work methodology...
---
```

With full "When to use", workflow steps, and actionable instructions extracted from the book.

## Output Location

The generated SKILL.md is written to your current working directory. To use it as a Claude Code skill, move it:

```bash
mkdir -p ~/.claude/skills/deep_work_methodology
mv SKILL.md ~/.claude/skills/deep_work_methodology/SKILL.md
```
