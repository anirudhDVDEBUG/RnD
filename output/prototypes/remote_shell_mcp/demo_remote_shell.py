#!/usr/bin/env python3
"""
Demo simulator for remote-shell-mcp.

Since the real tool requires a Go binary + actual SSH targets, this script
simulates the MCP tool surface to show what capabilities it exposes and
how a Claude Code session would interact with it.

It walks through each major feature:
  1. SSH session management (connect, run commands, persist)
  2. SFTP file transfers (upload / download)
  3. Port forwarding / SSH tunnels
  4. Docker container management over SSH
"""

import json
import time
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime

# ── Simulated MCP tool registry ──────────────────────────────────────────────

TOOLS = {
    "ssh_connect": {
        "description": "Open a persistent SSH session to a remote host",
        "inputSchema": {
            "type": "object",
            "properties": {
                "host": {"type": "string"},
                "user": {"type": "string", "default": "root"},
                "port": {"type": "integer", "default": 22},
                "identity_file": {"type": "string", "description": "Path to SSH private key"},
            },
            "required": ["host"],
        },
    },
    "ssh_exec": {
        "description": "Execute a command in an existing SSH session",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "command": {"type": "string"},
            },
            "required": ["session_id", "command"],
        },
    },
    "ssh_disconnect": {
        "description": "Close an SSH session",
        "inputSchema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    "sftp_upload": {
        "description": "Upload a file to a remote host via SFTP",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "local_path": {"type": "string"},
                "remote_path": {"type": "string"},
            },
            "required": ["session_id", "local_path", "remote_path"],
        },
    },
    "sftp_download": {
        "description": "Download a file from a remote host via SFTP",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "remote_path": {"type": "string"},
                "local_path": {"type": "string"},
            },
            "required": ["session_id", "remote_path", "local_path"],
        },
    },
    "port_forward": {
        "description": "Create an SSH tunnel (local or remote port forwarding)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "direction": {"type": "string", "enum": ["local", "remote"]},
                "local_port": {"type": "integer"},
                "remote_host": {"type": "string", "default": "localhost"},
                "remote_port": {"type": "integer"},
            },
            "required": ["session_id", "direction", "local_port", "remote_port"],
        },
    },
    "docker_list": {
        "description": "List Docker containers on the remote host",
        "inputSchema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    "docker_exec": {
        "description": "Execute a command inside a Docker container on the remote host",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string"},
                "container": {"type": "string"},
                "command": {"type": "string"},
            },
            "required": ["session_id", "container", "command"],
        },
    },
}

# ── Simulated state ─────────────────────────────────────────────────────────

@dataclass
class SSHSession:
    session_id: str
    host: str
    user: str
    port: int
    connected_at: str
    status: str = "connected"

@dataclass
class Tunnel:
    tunnel_id: str
    session_id: str
    direction: str
    local_port: int
    remote_port: int
    remote_host: str = "localhost"

sessions: dict[str, SSHSession] = {}
tunnels: list[Tunnel] = []
next_id = 1

def new_id(prefix: str) -> str:
    global next_id
    sid = f"{prefix}-{next_id:04d}"
    next_id += 1
    return sid

# ── Simulated tool handlers ─────────────────────────────────────────────────

def handle_ssh_connect(params: dict) -> dict:
    sid = new_id("ssh")
    sess = SSHSession(
        session_id=sid,
        host=params["host"],
        user=params.get("user", "root"),
        port=params.get("port", 22),
        connected_at=datetime.now().isoformat(),
    )
    sessions[sid] = sess
    return {"session_id": sid, "status": "connected", "message": f"Connected to {sess.user}@{sess.host}:{sess.port}"}

def handle_ssh_exec(params: dict) -> dict:
    sid = params["session_id"]
    cmd = params["command"]
    if sid not in sessions:
        return {"error": f"No session {sid}"}
    # Simulate common commands
    mock_outputs = {
        "uname -a": "Linux prod-web-01 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux",
        "uptime": " 14:23:07 up 47 days,  3:12,  2 users,  load average: 0.42, 0.38, 0.35",
        "df -h /": "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1       100G   34G   62G  36% /",
        "whoami": sessions[sid].user,
        "docker ps --format '{{.Names}}'": "nginx-proxy\napp-backend\nredis-cache\npostgres-db",
        "cat /etc/hostname": sessions[sid].host,
    }
    output = mock_outputs.get(cmd, f"[simulated output for: {cmd}]")
    return {"stdout": output, "exit_code": 0}

def handle_ssh_disconnect(params: dict) -> dict:
    sid = params["session_id"]
    if sid in sessions:
        sessions[sid].status = "disconnected"
        del sessions[sid]
        return {"status": "disconnected", "session_id": sid}
    return {"error": f"No session {sid}"}

def handle_sftp_upload(params: dict) -> dict:
    return {
        "status": "uploaded",
        "local_path": params["local_path"],
        "remote_path": params["remote_path"],
        "bytes_transferred": 14823,
    }

def handle_sftp_download(params: dict) -> dict:
    return {
        "status": "downloaded",
        "remote_path": params["remote_path"],
        "local_path": params["local_path"],
        "bytes_transferred": 52190,
    }

def handle_port_forward(params: dict) -> dict:
    tid = new_id("tun")
    t = Tunnel(
        tunnel_id=tid,
        session_id=params["session_id"],
        direction=params["direction"],
        local_port=params["local_port"],
        remote_port=params["remote_port"],
        remote_host=params.get("remote_host", "localhost"),
    )
    tunnels.append(t)
    arrow = f"localhost:{t.local_port} -> {t.remote_host}:{t.remote_port}" if t.direction == "local" else f"{t.remote_host}:{t.remote_port} -> localhost:{t.local_port}"
    return {"tunnel_id": tid, "direction": t.direction, "mapping": arrow, "status": "active"}

def handle_docker_list(params: dict) -> dict:
    return {
        "containers": [
            {"name": "nginx-proxy",  "image": "nginx:1.25",       "status": "Up 12 days", "ports": "0.0.0.0:80->80/tcp"},
            {"name": "app-backend",  "image": "myapp:latest",     "status": "Up 12 days", "ports": "8080/tcp"},
            {"name": "redis-cache",  "image": "redis:7-alpine",   "status": "Up 12 days", "ports": "6379/tcp"},
            {"name": "postgres-db",  "image": "postgres:16",      "status": "Up 12 days", "ports": "5432/tcp"},
        ]
    }

def handle_docker_exec(params: dict) -> dict:
    cmd = params["command"]
    mock = {
        "redis-cli PING": "PONG",
        "psql -U postgres -c 'SELECT version();'": "PostgreSQL 16.1 on x86_64-pc-linux-gnu",
        "nginx -t": "nginx: configuration file /etc/nginx/nginx.conf test is successful",
    }
    return {"stdout": mock.get(cmd, f"[simulated: {cmd}]"), "exit_code": 0, "container": params["container"]}

HANDLERS = {
    "ssh_connect": handle_ssh_connect,
    "ssh_exec": handle_ssh_exec,
    "ssh_disconnect": handle_ssh_disconnect,
    "sftp_upload": handle_sftp_upload,
    "sftp_download": handle_sftp_download,
    "port_forward": handle_port_forward,
    "docker_list": handle_docker_list,
    "docker_exec": handle_docker_exec,
}

# ── Demo runner ──────────────────────────────────────────────────────────────

def banner(text: str):
    w = 70
    print()
    print("=" * w)
    print(f"  {text}")
    print("=" * w)

def step(tool: str, params: dict):
    print(f"\n>>> MCP call: {tool}")
    print(f"    params:   {json.dumps(params, indent=None)}")
    result = HANDLERS[tool](params)
    print(f"    result:   {json.dumps(result, indent=2)}")
    return result

def run_demo():
    banner("remote-shell-mcp  —  Capability Demo (simulated)")
    print()
    print("This demo walks through all four pillars of remote-shell-mcp:")
    print("  1. Persistent SSH sessions")
    print("  2. SFTP file transfers")
    print("  3. SSH tunnel / port forwarding")
    print("  4. Docker management over SSH")
    print()
    print("All calls below mirror the real MCP tool interface.")
    print("In production, replace the simulator with the Go daemon.\n")

    # ── 1. SSH ───────────────────────────────────────────────────────────────
    banner("1. SSH Session Management")

    res = step("ssh_connect", {"host": "prod-web-01.example.com", "user": "deploy", "port": 22})
    sid = res["session_id"]

    step("ssh_exec", {"session_id": sid, "command": "uname -a"})
    step("ssh_exec", {"session_id": sid, "command": "uptime"})
    step("ssh_exec", {"session_id": sid, "command": "df -h /"})

    print("\n  ** The session persists even if Claude Code restarts. **")
    print(f"  ** Session {sid} stays alive in the background daemon. **")

    # ── 2. SFTP ──────────────────────────────────────────────────────────────
    banner("2. SFTP File Transfers")

    step("sftp_upload", {
        "session_id": sid,
        "local_path": "./deploy/app.tar.gz",
        "remote_path": "/opt/releases/app-v2.3.tar.gz",
    })
    step("sftp_download", {
        "session_id": sid,
        "remote_path": "/var/log/app/error.log",
        "local_path": "./debug/error.log",
    })

    # ── 3. Tunnels ───────────────────────────────────────────────────────────
    banner("3. Port Forwarding / SSH Tunnels")

    step("port_forward", {
        "session_id": sid,
        "direction": "local",
        "local_port": 5433,
        "remote_host": "localhost",
        "remote_port": 5432,
    })
    print("\n  ** Postgres is now reachable at localhost:5433 **")

    step("port_forward", {
        "session_id": sid,
        "direction": "local",
        "local_port": 6380,
        "remote_host": "localhost",
        "remote_port": 6379,
    })
    print("\n  ** Redis is now reachable at localhost:6380 **")

    # ── 4. Docker ────────────────────────────────────────────────────────────
    banner("4. Docker Management over SSH")

    step("docker_list", {"session_id": sid})

    step("docker_exec", {
        "session_id": sid,
        "container": "redis-cache",
        "command": "redis-cli PING",
    })
    step("docker_exec", {
        "session_id": sid,
        "container": "postgres-db",
        "command": "psql -U postgres -c 'SELECT version();'",
    })

    # ── Cleanup ──────────────────────────────────────────────────────────────
    banner("5. Cleanup")
    step("ssh_disconnect", {"session_id": sid})

    # ── Tool registry ────────────────────────────────────────────────────────
    banner("MCP Tool Registry (tools exposed by the server)")
    for name, spec in TOOLS.items():
        props = list(spec["inputSchema"]["properties"].keys())
        print(f"  {name:20s}  params: {', '.join(props)}")

    banner("Demo Complete")
    print()
    print("To use the real server, install the Go binary and add it to")
    print("your Claude Code MCP config. See HOW_TO_USE.md for details.")
    print()


if __name__ == "__main__":
    run_demo()
