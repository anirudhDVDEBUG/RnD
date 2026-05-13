# How to Use OpenClaw Orchestra

## Install

### Option A: This prototype (quick demo)

```bash
cd openclaw_orchestra/
pip install pyyaml           # only required dependency for mock mode
bash run.sh                  # runs end-to-end, no API key needed
```

### Option B: Full OpenClaw Orchestra from source

```bash
git clone https://github.com/parijatmukherjee/openclaw-orchestra.git
cd openclaw-orchestra
pip install -e .
export ANTHROPIC_API_KEY="sk-ant-..."          # required for real agent work
export LINEAR_API_KEY="lin_api_..."             # optional: ticket oversight
export LINEAR_TEAM_ID="TEAM-123"               # optional: ticket oversight
```

## As a Claude Skill

Drop the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/openclaw_orchestra
cp SKILL.md ~/.claude/skills/openclaw_orchestra/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code to activate the skill:

- "Set up multi-agent orchestration with isolated workspaces"
- "Spawn specialist agents that each handle a different part of the task"
- "Use openclaw orchestra to delegate work across multiple agents"
- "Create an autonomous workflow with Linear ticket tracking"
- "Orchestrate Claude-powered agents with separate memory and tools"

## First 60 Seconds

**Input:**
```bash
python3 orchestrator.py --task "Implement user authentication flow"
```

**Output:**
```
============================================================
OPENCLAW ORCHESTRA - Multi-Agent Orchestration
============================================================
Task: Implement user authentication flow
Agents: backend-specialist, frontend-specialist, reviewer
Mode: Mock (no API key needed)
Linear: Mock mode
============================================================

[Orchestrator] Decomposing task into subtasks...
[Orchestrator] Created 3 subtasks:

  - subtask_001: [backend-specialist] Implement user authentication flow (priority: high)
  - subtask_002: [frontend-specialist] Implement user authentication flow (priority: medium)
  - subtask_003: [reviewer] Review: Implement user authentication flow (priority: medium)

[Orchestrator] Creating oversight tickets...

  [Linear-Mock] Created ticket LIN-100: [backend-specialist] Implement user authentication flow
  [Linear-Mock] Created ticket LIN-101: [frontend-specialist] Implement user authentication flow
  [Linear-Mock] Created ticket LIN-102: [reviewer] Review: Implement user authentication flow

[Orchestrator] Executing specialist agent subtasks...

  [Linear-Mock] LIN-100 -> In Progress
  [backend-specialist] Starting subtask: [backend-specialist] Implement user authentication flow
  [backend-specialist] Completed: completed (0.10s)
  [Linear-Mock] LIN-100 -> Done

  [Linear-Mock] LIN-101 -> In Progress
  [frontend-specialist] Starting subtask: [frontend-specialist] Implement user authentication flow
  [frontend-specialist] Completed: completed (0.10s)
  [Linear-Mock] LIN-101 -> Done

[Orchestrator] Running review agent...

  [Linear-Mock] LIN-102 -> In Progress
  [reviewer] Starting subtask: [reviewer] Review: Implement user authentication flow
  [reviewer] Completed: completed (0.10s)
  [Linear-Mock] LIN-102 -> Done

============================================================
ORCHESTRATION SUMMARY
============================================================

  Total subtasks: 3
  Completed:      3
  Failed:         0

  Agent Workspaces:
    backend-specialist: ./workspaces/backend (1 artifacts)
    frontend-specialist: ./workspaces/frontend (1 artifacts)
    reviewer: ./workspaces/review (1 artifacts)

  Linear Tickets:
    LIN-100: [Done] [backend-specialist] Implement user authentication flow
    LIN-101: [Done] [frontend-specialist] Implement user authentication flow
    LIN-102: [Done] [reviewer] Review: Implement user authentication flow

============================================================
All agents finished. Artifacts written to ./workspaces/
============================================================
```

Each agent writes its output as a Markdown artifact in its workspace directory. The reviewer agent produces a pass/fail summary with actionable suggestions.

## Using with Real Claude API

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python3 orchestrator.py --use-api --task "Build a REST API for todo items"
```

This sends each subtask to Claude for real reasoning, producing actual code and review output.

## Custom Agent Topologies

Edit `orchestra.yaml` to define your own agents:

```yaml
agents:
  - name: data-engineer
    workspace: ./workspaces/data
    tools: [sql, code-edit, git]
    prompt: "You handle database schemas, migrations, and data pipelines."
  - name: devops
    workspace: ./workspaces/infra
    tools: [docker, terraform, git]
    prompt: "You handle infrastructure, CI/CD, and deployment."
  - name: reviewer
    workspace: ./workspaces/review
    tools: [code-read, lint, git]
    prompt: "You review all changes for correctness and best practices."
```
