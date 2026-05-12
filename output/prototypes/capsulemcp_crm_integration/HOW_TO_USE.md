# How to Use capsulemcp

## Install

No global install needed. The server runs via `npx`:

```bash
npx capsulemcp
```

This downloads and starts the MCP server locally. Requires Node.js 18+.

## Configure Claude Code

Add this block to your MCP config — either project-level `.mcp.json` or user-level `~/.claude.json` under the `mcpServers` key:

```json
{
  "mcpServers": {
    "capsulemcp": {
      "command": "npx",
      "args": ["-y", "capsulemcp"],
      "env": {
        "CAPSULE_API_TOKEN": "<your-capsule-api-token>"
      }
    }
  }
}
```

### Read-only mode

To prevent any write operations (safe for exploration / auditing):

```json
{
  "mcpServers": {
    "capsulemcp": {
      "command": "npx",
      "args": ["-y", "capsulemcp", "--read-only"],
      "env": {
        "CAPSULE_API_TOKEN": "<your-capsule-api-token>"
      }
    }
  }
}
```

## Get your Capsule API token

1. Log in to [Capsule CRM](https://capsulecrm.com).
2. Go to **My Preferences** > **API Authentication Tokens**.
3. Click **Generate new token**.
4. Paste it into `CAPSULE_API_TOKEN` above.

## First 60 seconds

Once configured, restart Claude Code and try these prompts:

```
You: "List all my CRM contacts"
Claude: (calls list_parties tool) → table of contacts with names, orgs, tags

You: "Show me the sales pipeline"
Claude: (calls list_opportunities tool) → deals with stages, values, close dates

You: "Create a contact: Jane Park, CTO at StreamCo, tag as enterprise"
Claude: (calls create_party tool) → confirms contact created with ID

You: "What open cases do I have?"
Claude: (calls list_kases tool) → open support cases with status and assignee

You: "Add a task: follow up with Jane next Tuesday"
Claude: (calls create_task tool) → task created with due date
```

## Available MCP tools

| Tool               | Description                        | Read-only |
|--------------------|------------------------------------|-----------|
| `list_parties`     | Search/list contacts & orgs        | Yes       |
| `get_party`        | Get a single contact by ID         | Yes       |
| `create_party`     | Create a new person or org         | No        |
| `update_party`     | Update contact fields              | No        |
| `list_opportunities` | List deals in the pipeline       | Yes       |
| `list_kases`       | List cases/projects                | Yes       |
| `list_tasks`       | List tasks                         | Yes       |
| `create_task`      | Create a new task                  | No        |

## Org-wide deployment

For teams, Capsule CRM can be configured as a **Custom Connector** in Claude's organization settings, removing the need for per-user local installs. See [Claude docs on custom connectors](https://docs.anthropic.com/en/docs/claude-code/tutorials#set-up-model-context-protocol-mcp).

## Run the local demo (no API key)

```bash
bash run.sh
```

This starts a mock Capsule CRM API and exercises all operations.
