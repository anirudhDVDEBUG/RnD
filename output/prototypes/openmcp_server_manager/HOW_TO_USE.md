# How to Use

## Install (this demo)

```bash
# No install needed -- zero external dependencies
git clone <this-repo> && cd openmcp_server_manager
bash run.sh
```

Requires Node.js >= 16.

## Install the full OpenMCP desktop app

```bash
git clone https://github.com/hacimertgokhan/openmcp.git
cd openmcp
npm install
npm run dev        # launches Electron desktop UI
```

## As a Claude Code Skill

Drop the skill file so Claude can manage MCP servers on demand:

```bash
mkdir -p ~/.claude/skills/openmcp_server_manager
cp SKILL.md ~/.claude/skills/openmcp_server_manager/SKILL.md
```

**Trigger phrases:**
- "Set up OpenMCP to manage my MCP servers"
- "I need a desktop app to manage MCP server configurations"
- "Help me install and configure OpenMCP"
- "I want a CLI tool to manage my MCP servers"

## MCP server JSON for Claude Code

If you're adding MCP servers directly to `~/.claude.json`, use this shape in the `mcpServers` block:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

The demo's `export` command generates this format automatically.

## CLI Reference

```bash
node src/cli.js add <name> <command> [args...]   # Add a server
node src/cli.js remove <name>                     # Remove a server
node src/cli.js list                              # List all servers
node src/cli.js show <name>                       # Show server details
node src/cli.js validate <name>                   # Check config validity
node src/cli.js export                            # Export for Claude Code
node src/cli.js update <name> <field>=<value>     # Update a field

# Options
--config <path>      # Custom config file (default: ./mcp-servers.json)
--env KEY=VAL        # Set env var when adding
--type stdio|sse     # Transport type (default: stdio)
```

## First 60 seconds

```bash
# 1. Run the demo
$ bash run.sh

# 2. Add your own server
$ node src/cli.js add my-server npx -y @modelcontextprotocol/server-brave-search \
    --env BRAVE_API_KEY=your_key

# 3. Export for Claude
$ node src/cli.js export
# -> Paste the output into ~/.claude.json

# 4. Validate
$ node src/cli.js validate my-server
# -> Server "my-server" is valid.
```

**Input:** CLI commands to register MCP servers with name, command, args, and env vars.
**Output:** A managed JSON config file + ready-to-paste Claude Code configuration.
