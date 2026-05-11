---
name: ccgx_multi_model_workflow
description: |
  Multi-model dev workflow for Claude Code — auto-routes frontend tasks to Gemini, backend tasks to Codex, with quality tiers and autonomous long-runs.
  TRIGGER when: user wants to route tasks to different AI models, set up multi-model workflows, use Gemini for frontend and Codex for backend, or configure quality tiers for AI-assisted development.
  DO NOT TRIGGER when: user is doing single-model work, simple code edits, or tasks unrelated to multi-model orchestration.
---

# CCGX Multi-Model Workflow

Successor to ccg-workflow. Orchestrates multiple AI models within Claude Code — automatically routing frontend work to Gemini, backend work to Codex, with configurable quality tiers and support for autonomous long-running tasks.

## When to use

- "Set up multi-model routing for my project"
- "Route frontend tasks to Gemini and backend to Codex"
- "Configure a ccgx workflow with quality tiers"
- "Run an autonomous long-running dev workflow across models"
- "Orchestrate multiple AI models for different parts of my codebase"

## How to use

### 1. Install ccgx-workflow

```bash
git clone https://github.com/wzyxdwll/ccgx-workflow.git
cd ccgx-workflow
npm install
npm run build
```

### 2. Configure model routing

Create or edit the workflow configuration to define routing rules:

- **Frontend tasks** (React, Vue, CSS, HTML, UI components) → routed to **Gemini**
- **Backend tasks** (APIs, databases, server logic, infrastructure) → routed to **Codex**
- **Quality tiers** allow you to set different levels of review and iteration per task type

### 3. Run the workflow

```bash
# Start the multi-model workflow
npx ccgx-workflow start

# Or run with a specific task
npx ccgx-workflow run --task "Build the user dashboard"

# Autonomous long-run mode
npx ccgx-workflow run --autonomous
```

### 4. Quality tiers

Configure quality tiers to control how thoroughly each model handles its tasks:

- **Draft**: Fast iteration, minimal review
- **Standard**: Balanced speed and quality
- **Production**: Full review, testing, and validation

### 5. Integration with Claude Code

The workflow integrates directly with Claude Code, allowing you to:

- Use Claude as the orchestrator that dispatches to specialized models
- Maintain a unified development context across all models
- Track progress and results from all model interactions in one place

## Key features

- **Auto-routing**: Detects task type (frontend/backend) and routes to the optimal model
- **Quality tiers**: Configurable levels of thoroughness per task
- **Autonomous mode**: Long-running tasks that proceed without manual intervention
- **Multi-model orchestration**: Coordinates Gemini, Codex, and Claude in a single workflow

## References

- Source repository: https://github.com/wzyxdwll/ccgx-workflow
- Language: TypeScript
- Topics: agent, ai-orchestration, claude-code, cli, codex, gemini, workflow
