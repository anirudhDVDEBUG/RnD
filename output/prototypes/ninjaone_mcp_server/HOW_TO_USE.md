# How to Use — NinjaOne MCP Server

## Prerequisites

- **.NET 8.0 SDK** or later ([download](https://dotnet.microsoft.com/download))
- A **NinjaOne account** with API access enabled
- **NinjaOne API credentials**: Client ID + Client Secret from the NinjaOne admin portal (*Configuration > API > Client App IDs*)

## Install

```bash
git clone https://github.com/BezaluLLC/Bezalu.NinjaOne.MCP.git
cd Bezalu.NinjaOne.MCP
dotnet build
```

## Configure Claude Code (MCP server)

Add the following to your `~/.claude.json` inside the `mcpServers` block:

```json
{
  "mcpServers": {
    "ninjaone": {
      "command": "dotnet",
      "args": ["run", "--project", "/absolute/path/to/Bezalu.NinjaOne.MCP"],
      "env": {
        "NINJAONE_CLIENT_ID": "your-client-id",
        "NINJAONE_CLIENT_SECRET": "your-client-secret",
        "NINJAONE_INSTANCE_URL": "https://app.ninjarmm.com"
      }
    }
  }
}
```

**Instance URL by region:**

| Region | URL |
|--------|-----|
| US | `https://app.ninjarmm.com` |
| EU | `https://eu.ninjarmm.com` |
| Oceania | `https://oc.ninjarmm.com` |

Replace `/absolute/path/to/Bezalu.NinjaOne.MCP` with the actual path where you cloned the repo.

## First 60 seconds

After adding the MCP config and restarting Claude Code:

**Input (to Claude):**
```
List all organizations in NinjaOne
```

**Output (structured JSON via MCP tool):**
```json
{
  "organizations": [
    { "id": 1, "name": "Acme Corp", "nodeCount": 47 },
    { "id": 2, "name": "Globex Industries", "nodeCount": 123 }
  ],
  "totalCount": 2
}
```

**Input:**
```
Show me devices with active critical alerts
```

**Output:**
```json
{
  "alerts": [
    {
      "severity": "CRITICAL",
      "message": "Device offline for >12 hours",
      "deviceId": 103,
      "status": "ACTIVE"
    }
  ],
  "totalCount": 1
}
```

**Input:**
```
What software is installed on device 101?
```

**Output:**
```json
{
  "deviceId": 101,
  "deviceName": "ACME-WS-001",
  "software": [
    { "name": "Google Chrome", "version": "130.0.6723.92" },
    { "name": "Microsoft 365 Apps", "version": "16.0.18324" },
    { "name": "Zoom", "version": "6.3.1" }
  ],
  "totalCount": 3
}
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_organizations` | List all managed organizations |
| `get_devices` | Query devices, filter by org or online/offline status |
| `get_alerts` | View alerts filtered by severity or status |
| `get_activities` | Query activity logs and events |
| `get_software_inventory` | List installed software on a specific device |
| `get_os_patches` | Check OS patch status and pending updates |

## Trigger phrases

These natural-language queries will cause Claude to invoke the NinjaOne MCP tools:

- "List all organizations in NinjaOne"
- "Which devices are offline?"
- "Show me critical alerts"
- "What software is installed on device X?"
- "Show patch status for server Y"
- "What happened recently on device Z?"

## Running the mock demo

To try the tool surface without a live NinjaOne account:

```bash
bash run.sh
```

This runs `ninjaone_mcp_server.py` which exercises all 6 tools with realistic mock data.
