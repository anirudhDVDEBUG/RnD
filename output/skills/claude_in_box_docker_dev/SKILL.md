---
name: claude_in_box_docker_dev
description: |
  Set up a portable Claude Code dev environment in a Docker container with multi-session support, hook-driven automation, web management UI, and transparent SOCKS5 proxy. Runs on minimal hardware including Raspberry Pi.
  TRIGGER when: user wants to run Claude Code in Docker, set up a containerized dev environment, run Claude Code on a Raspberry Pi, create a portable AI coding setup, or manage multiple Claude Code sessions remotely.
  DO NOT TRIGGER when: user wants to use Claude Code locally without Docker, or is asking about Docker unrelated to Claude Code.
---

# Claude-in-Box: Portable Docker Dev Environment

Set up and manage a portable, containerized Claude Code development environment using Docker. Supports multi-session management, hook-driven automation, a web-based management UI, transparent SOCKS5 proxy, and runs on low-power hardware like a Raspberry Pi.

## When to use

- "I want to run Claude Code inside a Docker container"
- "Set up a portable Claude Code dev environment on my Raspberry Pi"
- "I need multi-session Claude Code with a web management interface"
- "How do I containerize my Claude Code workflow with proxy support?"
- "Help me deploy a remote Claude Code environment with Docker"

## How to use

### 1. Clone the repository

```bash
git clone https://github.com/jiangmuran/claude-in-box.git
cd claude-in-box
```

### 2. Configure environment

Create a `.env` file or set environment variables:

```bash
# Required: your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-...

# Optional: SOCKS5 proxy settings (for network-restricted environments)
SOCKS5_PROXY_HOST=0.0.0.0
SOCKS5_PROXY_PORT=1080

# Optional: web UI port
WEB_PORT=8080
```

### 3. Build and run

```bash
# Build the Docker image
docker build -t claude-in-box .

# Run the container
docker run -d \
  --name claude-in-box \
  -p 8080:8080 \
  -p 1080:1080 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $(pwd)/workspace:/workspace \
  claude-in-box
```

Or use Docker Compose:

```bash
docker compose up -d
```

### 4. Access the web management UI

Open `http://<host-ip>:8080` in your browser to:
- Create and manage multiple Claude Code sessions
- View session output in real-time via WebSocket
- Configure hooks and automation rules
- Monitor resource usage

### 5. Raspberry Pi deployment

For ARM-based devices like Raspberry Pi:

```bash
# The image supports multi-arch builds
docker buildx build --platform linux/arm64 -t claude-in-box .

# Run with resource limits appropriate for Pi
docker run -d \
  --name claude-in-box \
  --memory=2g \
  -p 8080:8080 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $(pwd)/workspace:/workspace \
  claude-in-box
```

### Key features

- **Multi-session**: Run multiple Claude Code instances simultaneously with isolated workspaces
- **Hook-driven**: Configure automation hooks that trigger on session events
- **Web UI**: Browser-based management interface with real-time WebSocket output
- **SOCKS5 proxy**: Transparent proxy support for network-restricted environments
- **PTY support**: Full terminal emulation for interactive Claude Code sessions
- **Lightweight**: Runs on hardware as minimal as a Raspberry Pi

## References

- **Source repository**: https://github.com/jiangmuran/claude-in-box
- **Language**: Go
- **Topics**: Docker, Claude Code, Remote Development, Raspberry Pi, WebSocket, SOCKS5
