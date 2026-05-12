---
name: goalkeeper_goal_execution
description: |
  Durable contract-driven goal execution with a subagent judge that gates completion against an explicit Definition of Done (DoD).
  Triggers: goal execution, definition of done, contract-driven tasks, autonomous goal completion, goalkeeper workflow
---

# Goalkeeper: Contract-Driven Goal Execution

Durable contract-driven goal execution for Claude Code. A subagent judge gates completion against an explicit Definition of Done.

## When to use

- "Execute this goal with a definition of done"
- "Use goalkeeper to track and verify task completion"
- "Set up a contract-driven goal with acceptance criteria"
- "Run a goal with a subagent judge to verify completion"
- "Break down this task with a definition of done and verify each criterion"

## How to use

### 1. Define the Goal and Definition of Done (DoD)

Create a clear goal with explicit, verifiable acceptance criteria:

```markdown
## Goal
<Describe the objective clearly>

## Definition of Done
- [ ] Criterion 1: <specific, verifiable condition>
- [ ] Criterion 2: <specific, verifiable condition>
- [ ] Criterion 3: <specific, verifiable condition>
```

Each criterion must be concrete and independently verifiable -- avoid vague language like "works well" or "is clean."

### 2. Execute the Goal

Work through the goal systematically:

1. **Plan**: Break the goal into subtasks aligned with the DoD criteria
2. **Implement**: Execute each subtask, tracking progress against the DoD
3. **Self-check**: After implementation, review each DoD criterion before judging

### 3. Judge Completion with Subagent

Use a subagent to act as an independent judge that evaluates completion against the DoD:

- Spawn a subagent with the role of "judge"
- Provide it the original goal, the Definition of Done, and the current state of the work
- The judge evaluates each DoD criterion as PASS or FAIL
- The goal is only considered complete when ALL criteria pass
- If any criterion fails, the judge provides specific feedback on what needs to be fixed

### 4. Iterate if Needed

If the judge identifies failures:
1. Review the judge's feedback for each failed criterion
2. Address the specific gaps identified
3. Re-submit for judging
4. Repeat until all criteria pass

## Key Principles

- **Contract-first**: Always define the DoD before starting work
- **Durable execution**: Track progress persistently so goals survive context switches
- **Independent judgment**: The judge subagent evaluates objectively against the contract
- **All-or-nothing**: The goal is not done until every DoD criterion passes

## References

- Source: [itsuzef/goalkeeper](https://github.com/itsuzef/goalkeeper)
