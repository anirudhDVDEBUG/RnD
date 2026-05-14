# remote-shell-mcp

**Persistent SSH, SFTP, port forwarding, and Docker management over MCP.**
A long-running Go daemon that keeps sessions, tunnels, and PTY shells alive
across Claude Code / Claude Desktop / Cursor / Codex CLI restarts.

## Headline result

> Claude Code connects to `prod-web-01`, runs diagnostics, tunnels Postgres
> to localhost, restarts a Docker container — and the session survives a
> full IDE restart without re-authenticating.

## Quick links

| Doc | What it covers |
|-----|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, MCP config, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations |

## Run the demo

```bash
bash run.sh
```

No Go binary, SSH keys, or remote servers required — the demo simulates the
full MCP tool surface so you can see exactly what the server exposes.
