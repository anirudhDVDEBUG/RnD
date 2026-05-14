# Technical Details — remote-shell-mcp

## What it does

remote-shell-mcp is a Go-based MCP (Model Context Protocol) server that
exposes persistent SSH sessions, SFTP transfers, SSH tunnels, and Docker
management as tool calls. It runs as a long-lived background daemon: when
Claude Code (or any MCP client) restarts, existing sessions, tunnels, and
PTY shells survive without re-authentication.

The server speaks the MCP stdio transport — it reads JSON-RPC requests from
stdin, performs SSH/SFTP/Docker operations, and writes results to stdout.
A separate daemon process owns the actual network connections, so the MCP
front-end can restart independently.

## Architecture

```
┌──────────────┐       stdio (JSON-RPC)       ┌──────────────────┐
│  Claude Code  │ ◄──────────────────────────► │  MCP front-end   │
│  (MCP client) │                              │  (Go binary)     │
└──────────────┘                              └────────┬─────────┘
                                                       │ IPC
                                              ┌────────▼─────────┐
                                              │  Daemon process   │
                                              │  (long-lived)     │
                                              │                   │
                                              │  SSH sessions ──► │──► Remote hosts
                                              │  SFTP channels    │
                                              │  Port forwards    │
                                              │  Docker exec      │
                                              └───────────────────┘
```

### Key components

| Component | Role |
|-----------|------|
| `main.go` | Entry point; starts MCP stdio server or daemon |
| SSH session manager | Pools `golang.org/x/crypto/ssh` connections keyed by session ID |
| SFTP handler | Wraps `pkg/sftp` for upload/download over existing sessions |
| Tunnel manager | Goroutines that accept on local ports and proxy to remote endpoints |
| Docker bridge | Runs `docker` CLI commands over the SSH session |
| Daemon IPC | Unix socket or named pipe connecting the MCP front-end to the daemon |

### Dependencies

- **Go 1.21+** (build-time)
- `golang.org/x/crypto/ssh` — SSH client
- `github.com/pkg/sftp` — SFTP protocol
- MCP SDK (stdio JSON-RPC transport)
- No Python, Node, or external runtime required at runtime

### Data flow (tool call lifecycle)

1. Claude Code sends a JSON-RPC `tools/call` request via stdin.
2. The MCP front-end deserialises the request and forwards it over IPC to the daemon.
3. The daemon performs the SSH/SFTP/Docker operation using a pooled connection.
4. The result (stdout, exit code, transfer status) is returned via IPC.
5. The MCP front-end serialises the result as JSON-RPC and writes it to stdout.

## Limitations

- **No password auth in the default flow.** The server relies on SSH keys or
  an SSH agent. Password-based auth may require extra configuration.
- **No built-in secret management.** SSH keys must already exist on disk or
  be loaded in an agent. The server does not store credentials.
- **Docker management is CLI-based.** It shells out `docker` commands over SSH
  rather than using the Docker API directly, so the remote host must have the
  `docker` CLI installed and the SSH user must have Docker permissions.
- **Single-machine daemon.** The daemon runs on your local machine. It does
  not federate across multiple developer workstations.
- **No Windows daemon support yet.** The daemon uses Unix sockets; Windows
  support (named pipes) is planned but not complete.
- **Session cleanup.** Idle sessions are not automatically reaped. Long-running
  forgotten tunnels consume local ports until explicitly disconnected.

## Why this matters for Claude-driven products

| Use case | How remote-shell-mcp helps |
|----------|---------------------------|
| **Agent factories** | Agents can provision, configure, and monitor remote VMs without manual SSH. Session persistence means multi-step deployments survive agent restarts. |
| **Lead-gen & marketing** | Deploy and manage scraping infrastructure, analytics pipelines, or ad-serving stacks on remote servers — all through natural language. |
| **Ad creatives** | Push generated assets to CDN origins or staging servers via SFTP without leaving the Claude session. |
| **Voice AI** | Manage Asterisk/FreeSWITCH/Opal servers: restart services, tail logs, update configs — hands-free via voice-driven Claude. |
| **DevOps automation** | Replace Ansible ad-hoc commands with conversational infrastructure management: "restart nginx on prod", "show container logs for app-backend". |

## Source

- Repository: https://github.com/jaenster/remote-shell-mcp
- Language: Go
- License: See repository for license details
