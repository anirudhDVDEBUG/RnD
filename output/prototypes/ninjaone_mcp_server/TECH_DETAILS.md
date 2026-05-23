# Technical Details — NinjaOne MCP Server

## What it does

Bezalu.NinjaOne.MCP is a C#/.NET 8 MCP server that bridges AI assistants (Claude, etc.) to the NinjaOne RMM platform via the Model Context Protocol's stdio transport. It authenticates to the NinjaOne REST API using OAuth2 client credentials, then exposes six read-only tools — organizations, devices, alerts, activities, software inventory, and OS patches — as structured MCP tool calls. The assistant sends a tool invocation, the server calls the NinjaOne API, and returns typed JSON results. No raw HTTP required on the assistant side.

The server enforces user-delegated access: the OAuth2 credentials determine which organizations, devices, and data the assistant can see. This means the assistant inherits the same permission boundary as the API application configured in the NinjaOne admin portal.

## Architecture

```
Claude (MCP client)
  │  stdio (JSON-RPC)
  ▼
Bezalu.NinjaOne.MCP (.NET 8 process)
  │  OAuth2 client_credentials
  ▼
NinjaOne REST API
  │
  ▼
NinjaOne RMM Platform (organizations, devices, alerts...)
```

**Key components:**

- **MCP transport:** stdio-based JSON-RPC, conforming to the MCP specification. The server is launched as a child process by Claude Code.
- **Auth layer:** OAuth2 client credentials flow against the NinjaOne token endpoint. Tokens are cached and refreshed automatically.
- **Tool handlers:** Each tool maps to one or more NinjaOne API endpoints (`/v2/organizations`, `/v2/devices`, `/v2/alerts`, etc.), with parameter validation and response shaping.
- **Dependencies:** .NET 8 SDK. No additional NuGet packages beyond the standard `System.Net.Http` and JSON serialization.

**Data flow for a typical query:**

1. User asks Claude: "Which devices are offline?"
2. Claude invokes MCP tool `get_devices` with `{ "status": "offline" }`.
3. The .NET server receives the JSON-RPC call, calls `GET /v2/devices?status=offline` on the NinjaOne API.
4. NinjaOne returns device records; the server shapes them into the MCP tool response schema.
5. Claude renders the result to the user.

## Limitations

- **Read-only:** The server exposes query tools only. It cannot create tickets, run scripts on endpoints, reboot devices, or modify configurations. This is a deliberate safety choice.
- **No webhook/push support:** The server polls on demand — it does not subscribe to NinjaOne webhooks for real-time alerts.
- **Single-tenant:** One set of API credentials per server instance. To serve multiple NinjaOne tenants you'd run multiple MCP server instances.
- **No caching:** Each tool call hits the NinjaOne API directly. For large fleets (1000+ devices), latency may be noticeable.
- **C# only:** The server requires .NET 8 SDK. There's no Python or Node.js alternative provided by the upstream project.
- **No pagination controls exposed:** The tools return up to the NinjaOne API's default page size. Large result sets may be truncated.

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **MSP / IT agent factories** | An AI agent that can triage alerts, check device health, and look up software versions autonomously — reducing L1 support load. |
| **Lead-gen for IT services** | Demonstrate NinjaOne integration as a differentiator when pitching AI-powered IT management to MSP prospects. |
| **Compliance / audit workflows** | Claude can answer "are all servers patched?" or "which devices are running outdated Chrome?" from structured data instead of manual dashboard checks. |
| **Multi-tool orchestration** | Combine NinjaOne device data with other MCP servers (ticketing, documentation, billing) for end-to-end IT operations agents. |

The server is a good example of a narrowly scoped, read-only MCP integration — low risk, high utility, and easy to evaluate before committing to a broader deployment.
