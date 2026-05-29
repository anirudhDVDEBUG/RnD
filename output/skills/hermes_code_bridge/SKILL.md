---
name: hermes_code_bridge
description: |
  Use Hermes Agent as a control plane to orchestrate local coding agents (Claude Code, Codex, Kimi Code, OpenCode, Gemini CLI).
  Triggers: "orchestrate coding agents", "hermes agent", "multi-agent coding", "coordinate CLI agents", "hermes code bridge"
---

# Hermes Code Bridge

Orchestrate multiple local coding agents (Claude Code, Codex, Kimi Code, OpenCode, Gemini CLI) using [Hermes Agent](https://github.com/xuyang-liu16/hermes-code-bridge) as the control plane.

## When to use

- "Set up Hermes to orchestrate my coding agents"
- "Use hermes-code-bridge to coordinate Claude Code and Codex"
- "I want a multi-agent coding setup with a control plane"
- "Orchestrate multiple CLI coding agents on my project"
- "Connect Hermes Agent to my local coding tools"

## How to use

### 1. Install hermes-code-bridge

```bash
# Clone the repository
git clone https://github.com/xuyang-liu16/hermes-code-bridge.git
cd hermes-code-bridge

# Install dependencies
pip install -e .
```

### 2. Supported Coding Agents

Hermes Code Bridge supports orchestrating the following CLI coding agents:

| Agent | Description |
|-------|-------------|
| **Claude Code** | Anthropic's CLI coding agent |
| **Codex** | OpenAI's CLI coding agent |
| **Kimi Code** | Moonshot AI's coding agent |
| **OpenCode** | Open-source coding agent |
| **Gemini CLI** | Google's CLI coding agent |

### 3. Configure the bridge

Set up your Hermes Agent as the control plane that delegates tasks to the appropriate local coding agent based on the task requirements:

- **Task routing**: Hermes decides which coding agent is best suited for each subtask
- **Multi-agent coordination**: Run multiple agents in parallel or sequentially on different parts of a project
- **Unified interface**: Single control plane to manage all your coding agents

### 4. Run with Hermes

Use Hermes Agent as the orchestrator to dispatch coding tasks to the appropriate local agent. Hermes acts as the control plane, analyzing the task and routing it to the best-fit coding agent.

### Key Concepts

- **Control Plane**: Hermes Agent serves as the central coordinator, making decisions about which coding agent to invoke
- **Bridge Plugin**: The hermes-code-bridge package acts as a Hermes plugin, enabling communication between Hermes and local CLI agents
- **Agent Selection**: Hermes can select agents based on task type, model capabilities, or user preferences
- **Parallel Execution**: Multiple coding agents can work on different parts of a codebase simultaneously

## References

- **Repository**: [xuyang-liu16/hermes-code-bridge](https://github.com/xuyang-liu16/hermes-code-bridge)
- **Topics**: multi-agent, cli-agents, agent-orchestration, coding-agents, hermes-agent, developer-tools
- **Language**: Python
