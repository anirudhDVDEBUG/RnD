# How to Use datasette-agent-sprites

## Install

```bash
pip install datasette datasette-agent datasette-agent-sprites==0.1a0
```

## Prerequisites

1. A Fly.io account with Sprites access ([sprites.dev](https://sprites.dev))
2. A Fly API token:
   ```bash
   export FLY_API_TOKEN="your-fly-api-token"
   ```

## As a Claude Skill

Drop the skill folder into your skills directory:

```bash
mkdir -p ~/.claude/skills/datasette_agent_sprites_sandbox
cp SKILL.md ~/.claude/skills/datasette_agent_sprites_sandbox/SKILL.md
```

**Trigger phrases:**
- "Set up datasette-agent-sprites for sandboxed command execution"
- "Run Datasette Agent commands in a Fly Sprites sandbox"
- "Configure a Datasette plugin for isolated sandbox execution"
- "Install datasette-agent-sprites and connect it to Fly Sprites"

## First 60 Seconds

```bash
# 1. Install
pip install datasette datasette-agent datasette-agent-sprites==0.1a0

# 2. Set credentials
export FLY_API_TOKEN="fly_abc123..."

# 3. Verify plugin loaded
datasette plugins
# Output includes: datasette-agent-sprites 0.1a0

# 4. Run an agent command in sandbox
datasette agent run "ls /tmp" --sandbox sprites
# Output: command executes inside ephemeral Fly Sprites VM
```

## Local Demo (no API key needed)

```bash
bash run.sh
```

This runs a mock simulation showing the plugin lifecycle: registration, command dispatch, sandboxed execution, and result return.

## Configuration

The plugin auto-registers with Datasette Agent's plugin system. No additional configuration files are needed beyond the `FLY_API_TOKEN` environment variable.

Optional metadata.yaml settings:

```yaml
plugins:
  datasette-agent-sprites:
    default_region: "iad"       # Fly region for sprite VMs
    timeout: 30                 # Max seconds per command
    memory_mb: 256              # VM memory allocation
```
