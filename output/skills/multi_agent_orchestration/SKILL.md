---
name: multi_agent_orchestration
description: |
  Multi-agent orchestration engine for building and deploying AI agent swarms with Claude Code.
  Triggers: multi-agent, orchestration, agent swarm, agent pipeline, parallel agents, agent coordination, agent workflow
---

# Multi-Agent Orchestration

Orchestrate multiple AI agents working in concert to solve complex tasks. Based on the Harmonist Orchestral framework for building and deploying AI swarms with Claude Code.

## When to use

- "Set up a multi-agent pipeline to handle this task"
- "Orchestrate multiple agents to work on different parts of this project"
- "Build an agent swarm to process these items in parallel"
- "Create an agent workflow with coordination between steps"
- "Deploy a multi-agent system for this complex task"

## How to use

### 1. Define Agent Roles

Break down the task into distinct agent roles, each with a clear responsibility:

```yaml
agents:
  - name: researcher
    role: Gather information and context
    tools: [WebSearch, WebFetch, Grep, Glob]
  - name: planner
    role: Analyze findings and create execution plan
    tools: [Read, TodoWrite]
  - name: implementer
    role: Execute the plan by writing code
    tools: [Edit, Write, Bash]
  - name: reviewer
    role: Validate output quality and correctness
    tools: [Read, Bash, Grep]
```

### 2. Orchestration Patterns

**Sequential Pipeline** — agents execute in order, each receiving output from the previous:
1. Researcher gathers context
2. Planner creates strategy from research
3. Implementer executes the plan
4. Reviewer validates the result

**Parallel Fan-out** — distribute independent subtasks across agents:
- Split work into independent units
- Assign each unit to a separate agent (use the Agent tool with subagents)
- Collect and merge results

**Hierarchical** — coordinator agent delegates to specialized sub-agents:
- Top-level agent breaks down the problem
- Delegates specific subtasks to specialized agents
- Aggregates results and handles conflicts

### 3. Implementation with Claude Code

Use the Agent tool to spawn sub-agents for parallel work:

```
# For independent research tasks, spawn parallel agents:
Agent(prompt="Research X", subagent_type="Explore")
Agent(prompt="Research Y", subagent_type="Explore")

# For implementation tasks:
Agent(prompt="Implement feature A in module X")
Agent(prompt="Implement feature B in module Y")
```

### 4. Coordination Strategies

- **Shared context**: Use TodoWrite to maintain shared task state
- **Dependency management**: Ensure dependent tasks run sequentially
- **Conflict resolution**: When agents modify overlapping files, review and merge
- **Quality gates**: Use reviewer agents before finalizing output

### 5. Best Practices

- Keep each agent's scope focused and well-defined
- Use parallel execution only for truly independent tasks
- Include a validation/review step in every pipeline
- Document agent roles and their expected inputs/outputs
- Start simple (2-3 agents) and scale up as needed

## References

- Source: [2508965-ship-it/harmonist-orchestral](https://github.com/2508965-ship-it/harmonist-orchestral) — Multi-Agent Orchestration Engine 2026
