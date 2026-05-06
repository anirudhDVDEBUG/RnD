# How to Use: Aula MCP School Platform

## Install

```bash
# Requires: Bun (https://bun.sh)
curl -fsSL https://bun.sh/install | bash

# Clone and install
git clone https://github.com/Casperjuel/aula-mcp.git
cd aula-mcp
bun install
bun run build
```

## Configure Credentials

Create `.env` in the `aula-mcp` directory:

```env
AULA_USERNAME=your_aula_username
AULA_PASSWORD=your_aula_password
```

These are your standard Aula/MitID credentials. The server handles MitID auth natively in TypeScript — no Puppeteer or headless browser required.

## Connect to Claude Desktop

Add this to your `~/.claude.json` under the `mcpServers` block:

```json
{
  "mcpServers": {
    "aula": {
      "command": "bun",
      "args": ["run", "start"],
      "cwd": "/absolute/path/to/aula-mcp",
      "env": {
        "AULA_USERNAME": "your_aula_username",
        "AULA_PASSWORD": "your_aula_password"
      }
    }
  }
}
```

Alternatively, if using Claude Desktop app, add to `claude_desktop_config.json` (same format).

## As a Claude Skill

Drop the skill file into:

```
~/.claude/skills/aula_mcp_school_platform/SKILL.md
```

Trigger phrases:
- "Set up an MCP server for Aula"
- "Connect Claude to Denmark's Aula school platform"
- "Help me configure aula-mcp with MitID authentication"
- "Access ugeplaner from Aula in my AI workflow"

## First 60 Seconds

Once the MCP server is connected, ask Claude:

**Input:**
> "Show me my children's weekly plan for this week"

**Output:**
```
Week 19 — Magnus (3.B, Skovlunde Skole)

Monday: Danish (reading comprehension), Math (fractions worksheet)
Tuesday: English (present tense exercises), Science (plant experiment)
Wednesday: PE, Art (watercolors)
Thursday: Danish (spelling test), History (Vikings project)
Friday: Music, Free play, Early dismissal 12:30
```

**Input:**
> "Any new messages from school?"

**Output:**
```
2 unread messages:

1. From: Lone Hansen (Klasselærer)
   Subject: Tur til Experimentarium d. 15/5
   "Kære forældre, vi skal på tur..."

2. From: SFO Skovlunde
   Subject: Sommerafslutning
   "Husk tilmelding senest fredag..."
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `get_profiles` | List children and parent profiles on your account |
| `get_calendar` | School calendar events for a date range |
| `get_messages` | Read inbox messages and threads |
| `get_ugeplaner` | Weekly plans from teachers |
