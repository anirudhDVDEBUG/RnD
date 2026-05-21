---
name: Sprint Orchestrator
description: |
  Multi-chat sprint orchestration skill for Claude Code. Coordinates parallel agent work across multiple chat sessions in structured sprints.
  Triggers: sprint orchestration, multi-chat coordination, parallel agent workflow, sprint planning with agents, multi-agent sprint
---

# Sprint Orchestrator

Portable multi-chat sprint orchestration skill for Claude Code. Enables structured, parallel development sprints using multiple Claude Code chat sessions working together on coordinated tasks.

## When to use

- "Orchestrate a sprint across multiple agents"
- "Run a multi-chat development sprint"
- "Coordinate parallel work across Claude sessions"
- "Plan and execute a sprint with multiple agents"
- "Break this project into parallel tasks for a sprint"

## How to use

### 1. Sprint Planning

Break down the project goal into discrete, parallelizable tasks:

1. Analyze the user's objective and decompose it into independent work units
2. Identify dependencies between tasks and determine execution order
3. Group tasks into sprint phases that can be executed in parallel
4. Create a sprint plan document with clear task definitions, acceptance criteria, and assignments

```markdown
# Sprint Plan: [Sprint Name]

## Objective
[Clear description of the sprint goal]

## Phase 1 - Parallel Tasks
- [ ] Task 1.1: [Description] → Agent A
- [ ] Task 1.2: [Description] → Agent B
- [ ] Task 1.3: [Description] → Agent C

## Phase 2 - Integration (depends on Phase 1)
- [ ] Task 2.1: [Description] → Agent A
- [ ] Task 2.2: [Description] → Agent B

## Acceptance Criteria
- [Criterion 1]
- [Criterion 2]
```

### 2. Agent Coordination

For each chat session / agent:

1. Assign a specific role and task scope
2. Define clear boundaries so agents don't conflict on files
3. Specify the output format and integration points
4. Provide context about what other agents are working on to avoid merge conflicts

### 3. Sprint Execution

1. **Kickoff**: Launch parallel agent sessions with their assigned tasks
2. **Monitor**: Track progress across all agent sessions
3. **Synchronize**: At phase boundaries, verify all tasks completed before proceeding
4. **Integrate**: Merge work from parallel agents, resolving any conflicts
5. **Validate**: Run tests and verify acceptance criteria are met

### 4. Sprint Review

After sprint completion:

1. Verify all acceptance criteria are met
2. Run the full test suite to ensure integration correctness
3. Document any technical debt or follow-up items
4. Summarize what was accomplished and any lessons learned

### Best Practices

- **File isolation**: Assign different files/modules to different agents to minimize conflicts
- **Clear interfaces**: Define API contracts between components before parallel work begins
- **Small phases**: Keep sprint phases short (3-5 tasks per phase) for easier coordination
- **Dependency tracking**: Never start a dependent task until its prerequisites are verified complete
- **Progress artifacts**: Each agent should write progress to a known location for orchestrator visibility

## References

- Source: [lipefur/sprint-orchestrator](https://github.com/lipefur/sprint-orchestrator) — Validated in 17+ production sprints
