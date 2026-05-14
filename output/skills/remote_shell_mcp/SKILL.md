---
name: remote_shell_mcp
description: |
  Set up and use persistent SSH sessions, SFTP file transfers, port forwarding, and Docker management over MCP using remote-shell-mcp.
  TRIGGER: user wants persistent SSH sessions, remote shell access via MCP, SFTP transfers, SSH tunnels/port forwarding, or Docker management on remote hosts through Claude Code.
---

# Remote Shell MCP Skill

Persistent SSH, SFTP, port forwarding, and Docker over MCP. A long-running daemon so sessions, tunnels, and PTY shells survive across Claude Code restarts.

## When to use

- "Set up persistent SSH access to my remote server"
- "I need to transfer files to a remote host via SFTP"
- "Create an SSH tunnel / port forward to my server"
- "Manage Docker containers on a remote machine"
- "Install remote-shell-mcp for persistent remote sessions"

## How to use

### 1. Install the MCP server

The server is a Go binary. Install it:

```bash
go install github.com/jaenster/remote-shell-mcp@latest
```

Or clone and build:

```bash
git clone https://github.com/jaenster/remote-shell-mcp.git
cd remote-shell-mcp
go build -o remote-shell-mcp .
```

### 2. Configure as an MCP server

Add to your Claude Code MCP settings (`.claude/settings.json` or global):

```json
{
  "mcpServers": {
    "remote-shell": {
      "command": "remote-shell-mcp",
      "args": []
    }
  }
}
```

If built locally, use the full path to the binary.

### 3. Use the MCP tools

Once configured, the following MCP tools become available:

- **SSH sessions**: Open persistent SSH connections that survive restarts. Run commands on remote hosts.
- **SFTP**: Transfer files to/from remote servers.
- **Port forwarding**: Create SSH tunnels (local and remote port forwarding).
- **Docker**: Manage Docker containers on remote hosts.
- **PTY shells**: Interactive terminal sessions over SSH.

### 4. Key capabilities

- **Persistent daemon**: Sessions, tunnels, and shells survive across Claude Code / Claude Desktop / Cursor restarts.
- **SSH key & agent support**: Uses standard SSH authentication (keys, agent, config).
- **Multiple sessions**: Manage multiple concurrent SSH connections.
- **Cross-platform**: Written in Go, works on Linux, macOS, and Windows.

### Example workflows

**Connect to a server and run commands:**
Use the SSH tool to establish a connection, then execute commands in the persistent session.

**Set up a tunnel:**
Create a port forward (e.g., forward local port 8080 to remote port 80) that persists across restarts.

**Transfer files:**
Use SFTP tools to upload or download files between local and remote hosts.

**Manage remote Docker:**
List, start, stop, or inspect Docker containers on a remote host through the SSH connection.

## References

- Source: https://github.com/jaenster/remote-shell-mcp
- Topics: MCP server, SSH, SFTP, port forwarding, Docker, Go
