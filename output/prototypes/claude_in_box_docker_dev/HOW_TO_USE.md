# How to Use Claude-in-Box

## Install the real project

```bash
git clone https://github.com/jiangmuran/claude-in-box.git
cd claude-in-box

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Build & run
docker compose up -d

# Open the web UI
open http://localhost:8080
```

### Raspberry Pi / ARM64

```bash
docker buildx build --platform linux/arm64 -t claude-in-box .
docker run -d --name claude-in-box --memory=2g \
  -p 8080:8080 -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $(pwd)/workspace:/workspace claude-in-box
```

## Using as a Claude Code Skill

Drop the skill file so Claude Code can trigger containerized dev environments on demand:

```bash
mkdir -p ~/.claude/skills/claude_in_box_docker_dev
cp SKILL.md ~/.claude/skills/claude_in_box_docker_dev/SKILL.md
```

**Trigger phrases:**
- "Run Claude Code inside a Docker container"
- "Set up a portable Claude Code dev environment on my Raspberry Pi"
- "I need multi-session Claude Code with a web management interface"
- "Help me deploy a remote Claude Code environment with Docker"

## Run this simulator (no Docker, no API key)

```bash
bash run.sh              # CLI-only summary
python simulator.py --serve   # Start web UI on port 9080
```

## First 60 seconds

1. Run `bash run.sh` — you see three simulated sessions with live output, resource stats, and hook execution logs.
2. Run `python simulator.py --serve` and open `http://localhost:9080` — a dark-themed management dashboard shows all sessions, hook rules, execution history, and API endpoints.
3. Hit the JSON APIs:
   ```bash
   curl http://localhost:9080/api/sessions | python -m json.tool
   curl http://localhost:9080/api/stats
   curl http://localhost:9080/api/hooks
   ```

### Example CLI output

```
================================================================
  CLAUDE-IN-BOX  |  Portable Docker Dev Environment Simulator
================================================================

  Sessions: 3  |  Running: 3  |  Memory: 151 MB  |  CPU: 9.1%

  [+] frontend-refactor      id:a1b2c3d4e5f6  mem:62MB  cpu:4.2%
      workspace: /workspace/frontend-refactor_a1b2c3
      last output: [hook:resource-monitor] Memory: 62MB | CPU: 4.2%

  [+] api-bugfix              id:d4e5f6a7b8c9  mem:51MB  cpu:3.1%
      workspace: /workspace/api-bugfix_d4e5f6
      last output: [hook:resource-monitor] Memory: 51MB | CPU: 3.1%

  [+] docs-generator          id:g7h8i9j0k1l2  mem:38MB  cpu:1.8%
      workspace: /workspace/docs-generator_g7h8i9
      last output: [hook:resource-monitor] Memory: 38MB | CPU: 1.8%
```

## Key environment variables (real project)

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | (required) | Your Anthropic API key |
| `WEB_PORT` | `8080` | Web management UI port |
| `SOCKS5_PROXY_HOST` | `0.0.0.0` | SOCKS5 proxy bind address |
| `SOCKS5_PROXY_PORT` | `1080` | SOCKS5 proxy port |
