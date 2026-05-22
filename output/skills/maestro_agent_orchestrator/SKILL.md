---
name: maestro_agent_orchestrator
description: |
  Multi-agent orchestration skill for coordinating AI coding agents (Claude, Codex, Cursor, Gemini, Windsurf) with routing rules, hooks, and profiles on Windows/cross-platform projects.
  Triggers: agent orchestration, multi-agent workflow, route prompts between agents, coordinate AI tools, manage agent profiles
---

# Maestro Agent Orchestrator

Orchestrate multiple AI coding agents with intelligent prompt routing, shared hooks, and coordinated profiles. Route tasks to the best-suited agent based on context, manage handoffs between agents, and maintain consistent project state across tools.

## When to use

- "Set up multi-agent orchestration for my project"
- "Route this task to the best AI agent"
- "Coordinate Claude, Codex, and Cursor on this codebase"
- "Create agent profiles and routing rules for my workflow"
- "Manage hooks and handoffs between AI coding tools"

## How to use

### 1. Define Agent Profiles

Create a `.maestro/profiles/` directory with a config for each agent you use:

```yaml
# .maestro/profiles/claude.yaml
agent: claude
strengths:
  - complex reasoning
  - architecture design
  - code review
  - refactoring
context_window: large
preferred_tasks:
  - system design
  - debugging complex issues
  - multi-file refactoring
```

```yaml
# .maestro/profiles/codex.yaml
agent: codex
strengths:
  - rapid prototyping
  - boilerplate generation
  - simple CRUD operations
context_window: medium
preferred_tasks:
  - scaffolding
  - repetitive code generation
  - simple feature implementation
```

### 2. Configure Routing Rules

Define rules that determine which agent handles which type of task:

```yaml
# .maestro/routing.yaml
rules:
  - pattern: "architect|design|refactor|review"
    route_to: claude
    priority: high

  - pattern: "scaffold|generate|boilerplate|crud"
    route_to: codex
    priority: medium

  - pattern: "ui|component|style|layout"
    route_to: cursor
    priority: medium

  - pattern: "search|research|explore"
    route_to: gemini
    priority: low

fallback: claude
```

### 3. Set Up Orchestration Hooks

Create hooks that fire before/after agent tasks to maintain state:

```yaml
# .maestro/hooks.yaml
pre_task:
  - sync_context: "git diff --cached > .maestro/context/staged_changes.txt"
  - update_state: "python .maestro/scripts/update_project_state.py"

post_task:
  - validate: "python .maestro/scripts/validate_output.py"
  - log: "python .maestro/scripts/log_agent_action.py"

handoff:
  - export_context: "python .maestro/scripts/export_context.py --from $SOURCE_AGENT --to $TARGET_AGENT"
```

### 4. Run the Orchestrator

To route a task through the orchestrator:

1. Analyze the task description against routing rules
2. Select the target agent based on pattern matching and priority
3. Prepare context (run pre-task hooks, gather relevant files)
4. Dispatch to the chosen agent with formatted context
5. Validate output (run post-task hooks)
6. If handoff needed, export context and route to next agent

```bash
# Example: orchestration command
python .maestro/orchestrate.py --task "Refactor the auth module for better testability" --auto-route
```

### 5. Multi-Agent Workflow Example

For complex tasks requiring multiple agents:

```yaml
# .maestro/workflows/feature_implementation.yaml
name: full_feature
steps:
  - agent: claude
    task: "Design the architecture and define interfaces"
    output: ".maestro/artifacts/design.md"

  - agent: codex
    task: "Implement the scaffolding based on design"
    input: ".maestro/artifacts/design.md"
    output: "src/"

  - agent: claude
    task: "Review implementation and suggest improvements"
    input: "src/"
    output: ".maestro/artifacts/review.md"

  - agent: cursor
    task: "Apply UI refinements based on review"
    input: ".maestro/artifacts/review.md"
```

## Key Concepts

- **Profiles**: Define each agent's strengths and preferred task types
- **Routing Rules**: Pattern-based rules that match tasks to agents
- **Hooks**: Pre/post scripts that maintain project state across agents
- **Handoffs**: Context export/import between agents during multi-step workflows
- **Workflows**: Multi-step pipelines that chain agents together

## References

- Source: [FernandoBolzan/Orquestrador-Maestro](https://github.com/FernandoBolzan/Orquestrador-Maestro)
- Topics: agent-orchestration, ai-agents, claude-code, codex, cursor, gemini-cli, opencode, windsurf, hooks, skills
