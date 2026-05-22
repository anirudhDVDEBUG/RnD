# Technical Details: Claude-in-Box

## What it does

Claude-in-Box is a Go application that wraps Claude Code inside a Docker container, exposing a web-based management UI over HTTP/WebSocket. It manages multiple concurrent Claude Code sessions, each running in an isolated PTY with its own workspace directory. A built-in hook engine fires callbacks on session lifecycle events (create, start, stop, error), and a transparent SOCKS5 proxy handles outbound network traffic for environments behind firewalls or in restricted networks.

The core value proposition: run Claude Code headlessly on any machine (including a Raspberry Pi), manage sessions from a browser, and automate workflows via hooks — without SSH or direct terminal access.

## Architecture

```
┌─────────────────────────────────────────────┐
│  Docker Container                           │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Session 1 │  │ Session 2 │  │ Session 3 │  │
│  │ (PTY)     │  │ (PTY)     │  │ (PTY)     │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │              │        │
│  ┌────▼──────────────▼──────────────▼────┐  │
│  │         Session Manager (Go)          │  │
│  │  - Lifecycle: create/start/stop       │  │
│  │  - Workspace isolation per session    │  │
│  │  - Resource monitoring (mem/cpu)      │  │
│  └────────────────┬──────────────────────┘  │
│                   │                          │
│  ┌────────────────▼──────────────────────┐  │
│  │          Hook Engine                  │  │
│  │  - Event pattern matching             │  │
│  │  - Configurable callbacks             │  │
│  │  - Audit trail / execution log        │  │
│  └────────────────┬──────────────────────┘  │
│                   │                          │
│  ┌────────────────▼──────┐  ┌────────────┐  │
│  │  Web UI (HTTP + WS)   │  │ SOCKS5     │  │
│  │  :8080                │  │ Proxy :1080│  │
│  └───────────────────────┘  └────────────┘  │
└─────────────────────────────────────────────┘
```

### Key files in the source repo

| File/Dir | Purpose |
|---|---|
| `main.go` | Entry point; wires up session manager, hook engine, web server, SOCKS5 proxy |
| `session/` | Session lifecycle, PTY allocation, workspace init |
| `hooks/` | Event-driven hook engine with pattern matching |
| `web/` | HTTP handlers, WebSocket upgrade for real-time output streaming |
| `proxy/` | Transparent SOCKS5 proxy implementation |
| `Dockerfile` | Multi-stage build; Node.js + Go runtime |
| `docker-compose.yml` | One-command deployment with volume mounts and env vars |

### Data flow

1. User opens web UI or calls REST API
2. Session manager allocates a PTY and workspace directory
3. Claude Code process spawns inside the PTY
4. Output streams to the browser via WebSocket
5. Hook engine fires on lifecycle events (create/start/stop/error)
6. SOCKS5 proxy transparently routes Claude's outbound HTTP through the configured proxy chain

### Dependencies

- **Runtime:** Go 1.21+, Node.js 20+ (for Claude Code), Docker
- **This simulator:** Python 3.8+ (stdlib only, no pip packages)

## Limitations

- **No built-in auth.** The web UI has no login — anyone who can reach port 8080 can manage sessions. Use a reverse proxy or firewall in production.
- **Single-node only.** No clustering or multi-host session distribution. Each container runs independently.
- **No persistent session state.** If the container restarts, running sessions are lost. Workspace files survive via volume mounts.
- **SOCKS5 only.** HTTP/HTTPS proxies are not supported natively; only SOCKS5.
- **ARM support is best-effort.** The Dockerfile builds for ARM64 but some Claude Code dependencies may not have ARM binaries.

## Why it matters

For teams building Claude-driven products (lead-gen pipelines, marketing automation, agent factories), Claude-in-Box solves the "where does Claude Code run?" problem:

- **Remote dev environments:** Give each team member a containerized Claude Code instance without local setup.
- **Agent factories:** Spin up disposable sessions for batch code-generation tasks, tear them down via hooks.
- **CI/CD integration:** Run Claude Code as a step in a pipeline inside a container, with hook-driven notifications on completion.
- **Edge deployment:** Run on a Raspberry Pi or NUC at the edge for on-prem AI coding assistance without cloud dependencies.
