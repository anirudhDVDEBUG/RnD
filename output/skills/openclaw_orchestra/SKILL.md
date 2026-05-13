---
name: openclaw_orchestra
description: |
  Multi-agent orchestration using OpenClaw Orchestra — spawn isolated specialist agents with dedicated workspaces, memory, and tools. Supports Linear-backed ticket oversight and Claude-powered autonomous workflows.
  Triggers: multi-agent orchestration, openclaw orchestra, agent delegation, spawn specialist agents, workflow automation with multiple agents
---

# OpenClaw Orchestra — Multi-Agent Orchestration

Orchestrate multiple isolated specialist agents using [OpenClaw Orchestra](https://github.com/parijatmukherjee/openclaw-orchestra). Each agent gets its own workspace, memory, and tooling. Supports Linear-backed ticket oversight and Claude-powered autonomous workflows.

## When to use

- "Set up multi-agent orchestration with isolated workspaces"
- "Spawn specialist agents that each handle a different part of the task"
- "Use openclaw orchestra to delegate work across multiple agents"
- "Create an autonomous workflow with Linear ticket tracking and agent delegation"
- "Orchestrate Claude-powered agents with separate memory and tools"

## How to use

### 1. Clone and install OpenClaw Orchestra

```bash
git clone https://github.com/parijatmukherjee/openclaw-orchestra.git
cd openclaw-orchestra
pip install -e .
```

### 2. Configure the orchestration environment

- Set your Anthropic API key:
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-..."
  ```
- (Optional) Configure Linear integration for ticket-backed oversight by setting `LINEAR_API_KEY` and `LINEAR_TEAM_ID` environment variables.

### 3. Define your agent topology

OpenClaw Orchestra uses specialist agents, each with:
- **Isolated workspace**: Agents operate in separate directories to avoid conflicts.
- **Dedicated memory**: Each agent maintains its own context and state.
- **Specific tools**: Agents are provisioned with only the tools they need.

Define agents in your orchestration config (typically `orchestra.yaml` or equivalent):

```yaml
agents:
  - name: backend-specialist
    workspace: ./workspaces/backend
    tools: [code-edit, test-runner, git]
    prompt: "You handle backend API changes."
  - name: frontend-specialist
    workspace: ./workspaces/frontend
    tools: [code-edit, browser-preview, git]
    prompt: "You handle frontend UI changes."
  - name: reviewer
    workspace: ./workspaces/review
    tools: [code-read, lint, git]
    prompt: "You review PRs and provide feedback."
```

### 4. Run the orchestrator

```bash
python -m openclaw_orchestra run --config orchestra.yaml --task "Implement user authentication flow"
```

The orchestrator will:
1. Parse the task and decompose it into subtasks.
2. Assign subtasks to the appropriate specialist agents.
3. Spin up each agent in its isolated workspace with its own memory.
4. Monitor progress and coordinate handoffs between agents.
5. (If Linear is configured) Create and update tickets for oversight.

### 5. Monitor and interact

- Check agent status and logs in the `./workspaces/` directories.
- The orchestrator provides a summary when all agents complete their work.
- Linear tickets (if configured) are updated in real-time with agent progress.

### Key features

| Feature | Description |
|---|---|
| Isolated workspaces | Each agent works in its own directory — no cross-contamination |
| Agent memory | Persistent memory per agent across task steps |
| Tool provisioning | Agents only get the tools they need |
| Linear integration | Optional ticket-backed oversight and tracking |
| Claude-powered | Uses Claude for autonomous reasoning and task execution |
| Task decomposition | Automatically breaks complex tasks into specialist subtasks |

## References

- **Repository**: [parijatmukherjee/openclaw-orchestra](https://github.com/parijatmukherjee/openclaw-orchestra)
- **Topics**: multi-agent systems, agent orchestration, workflow automation, task delegation, LLM orchestration
- **Language**: Python
