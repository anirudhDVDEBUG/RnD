---
name: capsulemcp_crm_integration
description: |
  Set up and use Capsule CRM MCP server for Claude.
  TRIGGER when: user mentions Capsule CRM, capsulemcp, CRM contacts/opportunities/cases in Capsule, or wants to connect Claude to Capsule CRM.
  DO NOT TRIGGER when: user is working with other CRMs (Salesforce, HubSpot) or general database queries.
---

# Capsule CRM Integration via MCP

Integrate Claude with Capsule CRM using the capsulemcp MCP server. Supports read-only and full access modes.

## When to use

- "Connect Claude to Capsule CRM"
- "Set up capsulemcp MCP server"
- "Query my Capsule CRM contacts and opportunities"
- "I want to manage CRM data from Claude using Capsule"
- "Install the Capsule CRM MCP server for Claude Code"

## How to use

### 1. Install and configure the MCP server

The server runs locally via `npx`. Add it to your Claude Code MCP config (`.mcp.json` or project settings):

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

### 2. Get your Capsule API token

1. Log in to your Capsule CRM account.
2. Go to **My Preferences** > **API Authentication Tokens**.
3. Generate a new token and paste it into the config above.

### 3. Read-only mode (optional)

To restrict the server to read-only operations, add the `--read-only` flag:

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

### 4. Available CRM tools

Once configured, Claude can interact with Capsule CRM data including:

- **Contacts/Parties** — search, list, create, and update people and organizations
- **Opportunities** — manage sales pipeline and deals
- **Cases** — track support cases and projects
- **Tasks** — create and manage CRM tasks
- **Tags & Custom Fields** — organize and enrich CRM records

### 5. Org-wide deployment

For team-wide access, Capsule CRM can also be configured as a Custom Connector in Claude for organizations, removing the need for individual local installs.

## References

- Source: [soil-dev/capsulemcp](https://github.com/soil-dev/capsulemcp)
- [Capsule CRM API Documentation](https://developer.capsulecrm.com/)
- [MCP Server Configuration for Claude Code](https://docs.anthropic.com/en/docs/claude-code/tutorials#set-up-model-context-protocol-mcp)
