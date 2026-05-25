---
name: cue_agent_profile_manager
description: |
  Agent profile manager for Claude Code & Codex. Per-directory profiles select which skills, MCP servers, and plugins load automatically before launch.
  Triggers: agent profiles, cue profiles, manage skills per directory, switch MCP servers by project, plugin management CLI
---

# Cue — Agent Profile Manager

Cue is a CLI tool that manages agent profiles for Claude Code and Codex. It lets you define per-directory profiles that control which skills, MCP servers, and plugins load — automatically, before launch.

## When to use

- "Set up different agent profiles for different projects"
- "Automatically load specific MCP servers when I enter a directory"
- "Manage which Claude Code skills are active per project"
- "Switch between plugin configurations based on the current repo"
- "Create a cue profile for this workspace"

## How to use

### 1. Install Cue globally

```bash
npm install -g cue-ai
```

### 2. Initialize a profile in your project directory

```bash
cue init
```

This creates a `.cue/` directory with a profile configuration file.

### 3. Configure your profile

Edit the generated profile to specify which skills, MCP servers, and plugins should load for this directory:

```bash
cue config
```

A profile can include:
- **Skills** — Which SKILL.md files or skill packages to activate
- **MCP Servers** — Which MCP servers to connect when working in this directory
- **Plugins** — Additional plugins or extensions to load

### 4. List and switch profiles

```bash
# List available profiles
cue list

# Use a specific profile
cue use <profile-name>

# Show current active profile
cue status
```

### 5. Automatic profile activation

When you enter a directory with a `.cue/` configuration, Cue automatically selects the matching profile before Claude Code or Codex launches, loading the right set of skills and servers for that project.

### Key commands

| Command | Description |
|---------|-------------|
| `cue init` | Initialize a new profile in the current directory |
| `cue list` | List all available profiles |
| `cue use <name>` | Activate a specific profile |
| `cue status` | Show the currently active profile |
| `cue config` | Edit profile configuration |
| `cue add skill <name>` | Add a skill to the current profile |
| `cue add mcp <server>` | Add an MCP server to the current profile |

## References

- **Repository**: https://github.com/opencue/cue
- **Install**: `npm install -g cue-ai`
- **Language**: TypeScript
- **Supports**: Claude Code, Codex CLI
