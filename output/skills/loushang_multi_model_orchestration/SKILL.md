---
name: loushang_multi_model_orchestration
description: |
  AI-native coding orchestration platform using zhnt/loushang for unified multi-model agent runtime with stateful sessions, tool governance, and traceable delivery.
  Triggers: multi-model agent orchestration, coding session management, agentic coding workflow, multi-agent runtime, tool governance
---

# Loushang: Multi-Model Coding Orchestration

Orchestrate multiple AI coding agents (Claude, DeepSeek, Qwen, Kimi, Minimax) through a unified runtime with stateful sessions, tool governance, and traceable delivery using [zhnt/loushang](https://github.com/zhnt/loushang).

## When to use

- "Set up a multi-model agent orchestration for my coding project"
- "I need stateful session management across different AI coding agents"
- "Orchestrate Claude, DeepSeek, and Qwen agents in a unified workflow"
- "Configure tool governance and traceability for agentic coding"
- "Run multiple AI coding models together with session persistence"

## How to use

### 1. Install Loushang

```bash
# Clone the repository
git clone https://github.com/zhnt/loushang.git
cd loushang

# Install dependencies (Python project)
pip install -e .
```

### 2. Configure Multi-Model Runtime

Loushang supports multiple model providers. Configure your desired agents:

- **Claude** (Anthropic)
- **DeepSeek**
- **Qwen**
- **Kimi**
- **Minimax**

Set API keys for each provider you want to use in your environment or configuration file.

### 3. Start an Orchestrated Session

```bash
# Launch the TUI (terminal UI) for interactive multi-agent coding
loushang

# Or run in CLI mode for automation
loushang --cli
```

### 4. Key Features

- **Stateful Sessions**: Each coding session maintains context, history, and state across interactions and model switches.
- **Tool Governance**: Define which tools each agent can access, enforce policies on tool usage, and audit tool invocations.
- **Traceable Delivery**: Every agent action, tool call, and output is logged for full traceability and reproducibility.
- **Multi-Agent Workflows**: Chain multiple models together — e.g., use one model for planning, another for implementation, and a third for review.
- **Harness Integration**: Works alongside Claude Code, Codex, and other coding harnesses.

### 5. Workflow Automation

Define reusable workflows that orchestrate multiple agents:

1. **Plan** — Use a reasoning-focused model to break down the task
2. **Implement** — Route implementation to the best-suited coding model
3. **Review** — Have a different model review the output
4. **Deliver** — Merge results with full session trace

### 6. Session Management

- Sessions persist across restarts
- Switch between models mid-session without losing context
- Fork sessions to explore alternative approaches
- Replay sessions for debugging or auditing

## References

- **Repository**: [zhnt/loushang](https://github.com/zhnt/loushang)
- **Language**: Python
- **Topics**: agentic-coding, multi-model, session-management, agent-orchestration, developer-tools, workflow-automation
