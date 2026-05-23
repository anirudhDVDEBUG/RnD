---
name: ninjaone_mcp_server
description: |
  Set up and configure the Bezalu NinjaOne MCP server for secure, user-delegated access to the NinjaOne RMM platform from AI assistants.
  Triggers: ninjaone, rmm, ninja mcp, it management mcp, ninjaone api
---

# NinjaOne MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with secure, user-delegated access to the NinjaOne RMM (Remote Monitoring and Management) platform. Built in C# by Bezalu LLC.

## When to use

- "Set up NinjaOne MCP server for managing devices and endpoints"
- "Connect Claude to my NinjaOne RMM platform"
- "Configure MCP server for IT management and device monitoring via NinjaOne"
- "Query NinjaOne organizations, devices, and alerts from Claude"
- "Integrate NinjaOne API access into my AI assistant workflow"

## How to use

### 1. Prerequisites

- .NET 8.0 SDK or later
- A NinjaOne account with API access
- NinjaOne API credentials (Client ID and Client Secret) from the NinjaOne administration portal

### 2. Clone and build

```bash
git clone https://github.com/BezaluLLC/Bezalu.NinjaOne.MCP.git
cd Bezalu.NinjaOne.MCP
dotnet build
```

### 3. Configure NinjaOne API credentials

Set up your NinjaOne API credentials. You will need:

- **Client ID** and **Client Secret** from your NinjaOne API application
- **Instance URL** for your NinjaOne region (e.g., `https://app.ninjarmm.com`, `https://eu.ninjarmm.com`, or `https://oc.ninjarmm.com`)

Configure these via environment variables or the project's configuration file:

```bash
export NINJAONE_CLIENT_ID="your-client-id"
export NINJAONE_CLIENT_SECRET="your-client-secret"
export NINJAONE_INSTANCE_URL="https://app.ninjarmm.com"
```

### 4. Add to Claude Code MCP configuration

Add the server to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "ninjaone": {
      "command": "dotnet",
      "args": ["run", "--project", "/path/to/Bezalu.NinjaOne.MCP"],
      "env": {
        "NINJAONE_CLIENT_ID": "your-client-id",
        "NINJAONE_CLIENT_SECRET": "your-client-secret",
        "NINJAONE_INSTANCE_URL": "https://app.ninjarmm.com"
      }
    }
  }
}
```

### 5. Available capabilities

Once connected, the MCP server provides tools to interact with the NinjaOne platform:

- **Organizations** — List and query organizations managed in NinjaOne
- **Devices/Endpoints** — Retrieve device information, status, and details
- **Alerts** — View and manage alerts from monitored endpoints
- **Activities** — Query activity logs and events
- **Software inventory** — List installed software across devices
- **OS patches** — Check patch status and updates

### 6. Usage example

Once configured, ask Claude to interact with your NinjaOne environment:

- "List all organizations in NinjaOne"
- "Show me devices with active alerts"
- "What software is installed on device X?"
- "Show recent activity for organization Y"

## References

- **Repository**: [BezaluLLC/Bezalu.NinjaOne.MCP](https://github.com/BezaluLLC/Bezalu.NinjaOne.MCP)
- **NinjaOne API docs**: [NinjaOne API Reference](https://app.ninjarmm.com/apidocs/)
- **MCP specification**: [Model Context Protocol](https://modelcontextprotocol.io)
