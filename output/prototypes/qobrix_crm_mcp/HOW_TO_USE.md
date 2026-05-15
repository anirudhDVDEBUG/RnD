# How to Use — Qobrix CRM MCP Server

## Option A: Run this evaluation demo (no API keys)

```bash
cd qobrix_crm_mcp
npm install
bash run.sh
```

This runs 7 query scenarios against mock CRM data and prints formatted results.

## Option B: Install the real MCP server

### 1. Clone and build

```bash
git clone https://github.com/sharpsir-group/qobrix-crm-mcp.git
cd qobrix-crm-mcp
npm install
npm run build
```

### 2. Get your Qobrix API credentials

You need:
- `QOBRIX_API_URL` — Your instance's API endpoint (e.g. `https://yourco.qobrix.com/api/v2`)
- `QOBRIX_API_TOKEN` — API token from Qobrix admin panel

### 3. Add to Claude Desktop / Claude Code

Paste this into `~/.claude.json` under the `mcpServers` key:

```json
{
  "mcpServers": {
    "qobrix-crm": {
      "command": "node",
      "args": ["/absolute/path/to/qobrix-crm-mcp/dist/index.js"],
      "env": {
        "QOBRIX_API_URL": "https://your-instance.qobrix.com/api/v2",
        "QOBRIX_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

For Claude Desktop, put the same block in `claude_desktop_config.json`.

### 4. Test the mock server locally (MCP stdio)

To try the mock server included in this repo as a real MCP server:

```json
{
  "mcpServers": {
    "qobrix-crm-mock": {
      "command": "node",
      "args": ["/absolute/path/to/qobrix_crm_mcp/mock-server.js"],
      "env": {}
    }
  }
}
```

This exposes the same tool names (`properties_search`, `contacts_get`, etc.) backed by mock data — useful for testing prompts and workflows before connecting to a live CRM.

## First 60 Seconds

After configuring the MCP server, ask Claude:

| You say | What happens |
|---------|-------------|
| "Find properties in Dubai Marina under $2M" | Calls `properties_search` with location + maxPrice filters |
| "Show leads assigned to John from last week" | Calls `leads_search` with agent filter |
| "Get contact cnt-001" | Calls `contacts_get` with the ID |
| "List active listings with 3+ bedrooms" | Calls `properties_search` with minBedrooms + status |
| "What deals are in negotiation?" | Calls `opportunities_search` with stage filter |

All 42 tools are read-only. Claude cannot modify CRM data through this server.

## Available Tool Groups (42 tools total)

| Entity Group | Tools | Examples |
|-------------|-------|---------|
| Contacts | search, get, list | Find buyers, look up by ID |
| Properties | search, get, list | Filter by price/beds/location |
| Leads | search, get, list | Pipeline by status/agent |
| Listings | search, get, list | Active/sold/pending listings |
| Opportunities | search, get, list | Deal stage queries |
| Tasks | search, get, list | Agent task management |
| Activities | search, get, list | Activity log retrieval |
| Documents | search, get, list | Document metadata |
| Notes | search, get, list | Entity-linked notes |
| Users | search, get, list | Agent/user lookups |
| Teams | search, get, list | Team structure |
| Custom Fields | search, get, list | Field metadata |
| Saved Searches | search, get, list | Stored search retrieval |
