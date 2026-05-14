# How to Use remote-shell-mcp

## Install the MCP server

The server is a single Go binary. You need Go 1.21+.

```bash
# Option A — go install (recommended)
go install github.com/jaenster/remote-shell-mcp@latest

# Option B — build from source
git clone https://github.com/jaenster/remote-shell-mcp.git
cd remote-shell-mcp
go build -o remote-shell-mcp .
```

Verify:

```bash
remote-shell-mcp --help
```

## Configure as an MCP server in Claude Code

Add the following to **`~/.claude.json`** (or project-level `.claude/settings.json`):

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

If you built from source, use the full path:

```json
{
  "mcpServers": {
    "remote-shell": {
      "command": "/home/you/remote-shell-mcp/remote-shell-mcp",
      "args": []
    }
  }
}
```

Restart Claude Code after saving the config.

## Using as a Claude Skill

Drop the skill file into Claude's skill directory:

```bash
mkdir -p ~/.claude/skills/remote_shell_mcp
cp SKILL.md ~/.claude/skills/remote_shell_mcp/SKILL.md
```

### Trigger phrases

Claude will activate this skill when you say things like:

- "Set up persistent SSH access to my remote server"
- "Transfer files to a remote host via SFTP"
- "Create an SSH tunnel / port forward"
- "Manage Docker containers on a remote machine"
- "Install remote-shell-mcp"

## First 60 seconds

Once the MCP server is running and Claude Code is restarted:

**1. Connect to a host**

> You: "Connect to deploy@prod-web-01.example.com via SSH"

Claude calls `ssh_connect` with `{"host": "prod-web-01.example.com", "user": "deploy"}`.
Returns a `session_id` (e.g. `ssh-0001`).

**2. Run a command**

> You: "Show disk usage on that server"

Claude calls `ssh_exec` with `{"session_id": "ssh-0001", "command": "df -h /"}`.
Returns the output inline.

**3. Set up a tunnel**

> You: "Forward the remote Postgres port 5432 to my local 5433"

Claude calls `port_forward` with:
```json
{
  "session_id": "ssh-0001",
  "direction": "local",
  "local_port": 5433,
  "remote_host": "localhost",
  "remote_port": 5432
}
```

Now `psql -h localhost -p 5433` connects to the remote database.

**4. Restart Claude Code**

Close and reopen Claude Code. The SSH session and tunnel are still alive
because the daemon persists in the background.

> You: "Run uptime on prod-web-01"

Claude reuses `ssh-0001` — no re-authentication needed.

## MCP tools exposed

| Tool | Purpose |
|------|---------|
| `ssh_connect` | Open a persistent SSH session |
| `ssh_exec` | Run a command in an existing session |
| `ssh_disconnect` | Close a session |
| `sftp_upload` | Upload a file via SFTP |
| `sftp_download` | Download a file via SFTP |
| `port_forward` | Create local or remote SSH tunnel |
| `docker_list` | List Docker containers on remote host |
| `docker_exec` | Run a command inside a remote container |

## Running the demo (no real server needed)

```bash
bash run.sh
```

This runs a Python simulator that exercises every MCP tool with mock data,
so you can see the full input/output contract without any infrastructure.
