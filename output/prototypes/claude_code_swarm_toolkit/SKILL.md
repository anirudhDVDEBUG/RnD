---
name: Claude Code Swarm Toolkit
description: |
  Multi-agent swarm orchestration for Claude Code. Coordinates parallel subagents to divide and conquer complex tasks using swarm-style patterns.
  Triggers: swarm agents, parallel agent orchestration, multi-agent coordination, divide task among agents, fan-out subagents
---

# Claude Code Swarm Toolkit

Orchestrate multiple Claude Code subagents in a swarm pattern to tackle complex, parallelizable tasks. This skill enables you to decompose large problems into independent subtasks, dispatch them to parallel agents, and merge results.

## When to use

- "Break this task into parallel agents and run them as a swarm"
- "Use swarm orchestration to refactor these modules simultaneously"
- "Fan out subagents to research multiple topics in parallel"
- "Coordinate multiple agents to implement features across different files"
- "Run a multi-agent pipeline for this complex task"

## How to use

### 1. Decompose the task

Analyze the user's request and identify independent subtasks that can run in parallel without dependencies:

```
Task: "Refactor auth, payments, and notifications modules"
-> Subtask A: Refactor auth module
-> Subtask B: Refactor payments module
-> Subtask C: Refactor notifications module
```

### 2. Dispatch parallel subagents

Use the Agent tool to launch independent subagents simultaneously. Each agent gets:
- A focused, self-contained prompt
- Clear boundaries (which files/modules to touch)
- Specific success criteria

```
Agent 1: "Refactor auth module - update to use new session pattern..."
Agent 2: "Refactor payments module - migrate to Stripe v3 API..."
Agent 3: "Refactor notifications module - switch to event-driven..."
```

### 3. Collect and merge results

After all subagents complete:
- Review each agent's output for conflicts or integration issues
- Resolve any cross-cutting concerns (shared types, imports, interfaces)
- Verify the combined changes are coherent

### 4. Validate the swarm output

Run tests or checks to confirm the merged work is correct:
- Type checking / linting across modified files
- Integration tests that span multiple modules
- Ensure no circular dependencies were introduced

## Swarm patterns

| Pattern | Use case |
|---------|----------|
| **Fan-out/Fan-in** | Parallel independent tasks, merge at end |
| **Pipeline** | Sequential stages, each agent builds on prior output |
| **Map-Reduce** | Same operation across many files, aggregate results |
| **Explore-then-Act** | Research agents gather info, action agent executes |

## Best practices

- Only parallelize truly independent work — shared state requires sequential handling
- Keep each subagent's scope small and well-defined
- Include file boundaries in each agent's prompt to avoid edit conflicts
- Use the Explore subagent type for research, default type for actions
- Limit swarm size to 3-5 agents to manage complexity
