---
name: ERPAVal Workflow
description: |
  Autonomous software development using the ERPAVal six-phase workflow: Explore, Research, Plan, Act, Validate, Compound. Uses classifier-driven routing to select the right phase and maintains a compounding lessons store for continuous improvement.

  Triggers:
  - "use erpaval" or "erpaval workflow"
  - "explore research plan act validate"
  - "autonomous development workflow"
  - "six-phase development"
  - "compound lessons"
---

# ERPAVal Workflow

A structured six-phase autonomous software development workflow with classifier-driven routing and a compounding lessons store.

## When to use

- "Use the ERPAVal workflow to implement this feature"
- "Run the explore-research-plan-act-validate-compound cycle"
- "Apply the six-phase autonomous development process"
- "Use structured agentic development with lesson compounding"
- "I want classifier-driven routing for this task"

## How to use

ERPAVal operates as a six-phase autonomous development loop. For each task, follow these phases in order:

### Phase 1: Explore
Understand the codebase and problem space before doing anything.
- Read relevant files, understand architecture and conventions
- Identify the scope of what needs to change
- Map dependencies and potential impact areas
- Output: A clear understanding of the current state

### Phase 2: Research
Gather the knowledge needed to solve the problem correctly.
- Search for similar patterns already in the codebase
- Review documentation, tests, and prior solutions
- Check the **lessons store** for relevant past learnings
- Identify constraints, edge cases, and best practices
- Output: Research findings that inform the plan

### Phase 3: Plan
Create a concrete, actionable plan before writing any code.
- Define the specific changes needed (files, functions, logic)
- Sequence the changes to minimize risk
- Identify validation criteria (how will you know it works?)
- Consider rollback strategy
- Output: A step-by-step implementation plan

### Phase 4: Act
Execute the plan with precision.
- Implement changes according to the plan
- Make minimal, focused changes — avoid scope creep
- Follow existing code conventions and patterns discovered in Explore
- Output: Implemented code changes

### Phase 5: Validate
Verify the changes work correctly and haven't broken anything.
- Run existing tests to check for regressions
- Test the specific functionality that was changed
- Review the diff for unintended changes
- Verify edge cases identified during Research
- Output: Validated, working changes

### Phase 6: Compound
Capture lessons learned for future tasks.
- Document what worked well and what didn't
- Record any surprising discoveries about the codebase
- Note patterns that could be reused
- Add findings to the **lessons store** (a persistent file, e.g., `LESSONS.md` or `.claude/lessons.md`)
- Output: Updated lessons store

### Classifier-Driven Routing

When receiving a new task, classify it first to determine the best entry point:
- **Bug fix**: Start at Explore to understand the bug, then full cycle
- **New feature**: Start at Explore, emphasize Research and Plan phases
- **Refactor**: Start at Explore, emphasize Plan and Validate phases
- **Simple change**: May skip Research if the change is trivial, but always Validate
- **Unknown/complex**: Always run the full six-phase cycle

### Lessons Store

Maintain a compounding lessons file that grows over time:
- Store in `.claude/lessons.md` or project-appropriate location
- Consult it during the Research phase of every task
- Update it during the Compound phase
- Categories: architecture patterns, gotchas, testing strategies, conventions

## Example Usage

```
User: Use ERPAVal to fix the login timeout bug

Classifier -> Bug fix -> Start at Explore

1. Explore: Read auth module, identify timeout handling
2. Research: Check lessons store, find similar past fixes
3. Plan: Increase timeout + add retry logic in auth.js:45
4. Act: Implement the fix
5. Validate: Run auth tests, manual verification
6. Compound: "Auth module uses 30s default timeout; retry logic pattern at auth.js:45"
```

## References

- Source: [theagenticguy/erpaval](https://github.com/theagenticguy/erpaval)
- Tags: agentic-sdlc, autonomous-agents, subagents, lesson-compounding, claude-code
