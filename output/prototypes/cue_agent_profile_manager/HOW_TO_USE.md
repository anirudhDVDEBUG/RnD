# How to Use Cue

## Install

```bash
npm install -g cue-ai
```

Requires Node.js 18+. No other dependencies.

## Core CLI commands

| Command | What it does |
|---------|-------------|
| `cue init` | Creates a `.cue/` directory with a default profile in the current project |
| `cue list` | Lists all profiles defined in the current `.cue/` directory |
| `cue use <name>` | Sets `<name>` as the active profile |
| `cue status` | Shows the active profile and its loaded skills/MCPs/plugins |
| `cue config` | Opens the active profile JSON for editing |
| `cue add skill <name>` | Adds a skill to the active profile |
| `cue add mcp <server>` | Adds an MCP server to the active profile |

## First 60 seconds

```bash
# 1. Install
npm install -g cue-ai

# 2. Go to your project
cd ~/projects/my-api

# 3. Initialize
cue init
# => Created .cue/default.json

# 4. Add tools for this project
cue add skill sql-query-builder
cue add mcp postgres-mcp
cue add mcp redis-mcp

# 5. Check what's loaded
cue status
# => Profile: default
#    Skills: sql-query-builder
#    MCP Servers: postgres-mcp, redis-mcp

# 6. Create a second profile for staging work
cue init --name staging
cue use staging
cue add mcp datadog-mcp
cue add skill log-analyzer
```

Now when you launch Claude Code from `~/projects/my-api`, Cue detects the `.cue/` directory and loads the active profile's skills and MCP servers automatically.

## Profile file format

Profiles live in `.cue/<profile-name>.json`:

```json
{
  "name": "default",
  "description": "Profile for my-api",
  "skills": ["sql-query-builder", "api-design-reviewer"],
  "mcpServers": ["postgres-mcp", "redis-mcp"],
  "plugins": ["eslint-autofix"],
  "env": {}
}
```

The active profile is tracked in `.cue/active.json`:

```json
{ "active": "default" }
```

## How auto-activation works

Cue hooks into your shell (via a shell integration or Claude Code's pre-launch hooks). When you `cd` into a directory containing a `.cue/` folder, it reads `active.json` and configures the agent's skill/MCP/plugin set accordingly. No manual `cue use` required after initial setup.

## Running the demo (this repo)

```bash
bash run.sh
```

This runs a self-contained demo that creates two mock project directories, sets up profiles with different skills/MCPs/plugins, switches between them, and shows auto-detection — all without needing `cue-ai` installed globally.
