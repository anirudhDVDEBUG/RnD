---
name: qobrix_crm_mcp
description: |
  Set up and use the Qobrix CRM MCP server for read-only access to real-estate CRM data across 13 entity groups with 42 tools, aligned with RESO DD 2.0 standards.
  Triggers: qobrix, qobrix crm, qobrix mcp, real estate crm mcp, reso crm
---

# Qobrix CRM MCP Server

Read-only MCP server for Qobrix CRM — 42 tools across 13 entity groups (contacts, properties, leads, listings, etc.), aligned with RESO DD 2.0 canonical real-estate workflows.

## When to use

- "Set up the Qobrix CRM MCP server for my project"
- "I need to query Qobrix CRM data from Claude"
- "Connect my real estate CRM to Claude via MCP"
- "Help me configure Qobrix MCP tools for property lookups"
- "I want to search contacts and listings in Qobrix from my AI agent"

## How to use

### 1. Install the MCP server

```bash
git clone https://github.com/sharpsir-group/qobrix-crm-mcp.git
cd qobrix-crm-mcp
npm install
npm run build
```

### 2. Configure environment variables

Create a `.env` file or set these variables:

```
QOBRIX_API_URL=https://your-instance.qobrix.com/api/v2
QOBRIX_API_TOKEN=your_api_token_here
```

### 3. Add to MCP configuration

Add the server to your MCP client config (e.g. `claude_desktop_config.json` or `.mcp.json`):

```json
{
  "mcpServers": {
    "qobrix-crm": {
      "command": "node",
      "args": ["path/to/qobrix-crm-mcp/dist/index.js"],
      "env": {
        "QOBRIX_API_URL": "https://your-instance.qobrix.com/api/v2",
        "QOBRIX_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

### 4. Available entity groups and tools

The server exposes **42 read-only tools** across **13 entity groups**:

- **Contacts** — search, get, list contacts
- **Properties** — search, get, list properties with RESO DD 2.0 fields
- **Leads** — query and retrieve lead records
- **Listings** — search active/sold/pending listings
- **Opportunities** — deal pipeline queries
- **Tasks** — CRM task lookups
- **Activities** — activity log retrieval
- **Documents** — document metadata queries
- **Notes** — note retrieval by entity
- **Users** — agent/user lookups
- **Teams** — team structure queries
- **Custom Fields** — custom field metadata
- **Saved Searches** — stored search retrieval

All tools are **read-only** — no data is modified through this MCP server.

### 5. Example usage patterns

Once configured, you can ask Claude to:

- "Find all properties in Dubai Marina under $2M"
- "Show me leads assigned to agent John from last week"
- "Get contact details for record ID abc-123"
- "List all active listings with 3+ bedrooms"
- "Search opportunities in the negotiation stage"

### 6. RESO DD 2.0 alignment

The server maps Qobrix CRM fields to RESO Data Dictionary 2.0 canonical names, ensuring consistent field naming across real-estate tooling (e.g., `ListPrice`, `PropertyType`, `StandardStatus`, `ListingId`).

## References

- **Source repository**: https://github.com/sharpsir-group/qobrix-crm-mcp
- **RESO Data Dictionary**: https://www.reso.org/data-dictionary/
- **MCP specification**: https://modelcontextprotocol.io
