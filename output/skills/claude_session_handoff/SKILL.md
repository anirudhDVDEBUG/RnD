---
name: Claude Session Handoff
description: |
  Switch Claude Code sessions without losing context. Auto-generates handoff documentation, maintains STATUS.md project logs, and snapshots commits so the next agent starts in seconds.
  Triggers: session handoff, context handoff, switch session, hand off to next agent, save session state, pass context
---

# Claude Session Handoff

A skill for seamless session transitions between Claude Code agents. Generates structured handoff documents that capture current project state, progress, and next steps.

## When to use

- "Hand off this session to the next agent"
- "Save my session context for later"
- "Generate a handoff document"
- "I'm ending this session, prepare a handoff"
- "Switch sessions without losing context"

## How to use

### 1. Generate a Handoff Document

When ending a session or switching context, create a handoff document:

1. Review current git status and recent changes
2. Create/update `STATUS.md` in the project root with:
   - **Current State**: What was being worked on, branch name, last commit
   - **Progress**: Completed tasks and their outcomes
   - **Blockers**: Any issues encountered or unresolved problems
   - **Next Steps**: Clear actionable items for the next session
   - **Context**: Key decisions made, important file paths, architecture notes

### 2. Create the Handoff

```markdown
# STATUS.md format:

## Project Status
- **Branch**: <current branch>
- **Last Commit**: <short hash + message>
- **Date**: <timestamp>

## What Was Done
- <completed task 1>
- <completed task 2>

## Current State
- <what's in progress, any uncommitted changes>

## Blockers / Issues
- <any problems encountered>

## Next Steps
- [ ] <actionable task 1>
- [ ] <actionable task 2>

## Key Context
- <important decisions, file paths, patterns to know>
```

### 3. Snapshot the State

- Stage and commit any work-in-progress with a clear `[WIP]` prefix
- Ensure STATUS.md is committed so the next agent can read it immediately
- Include relevant file paths and line numbers for in-progress work

### 4. Starting a New Session (for the receiving agent)

When starting fresh, the new agent should:
1. Read `STATUS.md` to understand current project state
2. Check `git log --oneline -10` for recent activity
3. Review any uncommitted changes with `git status` and `git diff`
4. Continue from the documented next steps

## Best Practices

- Keep STATUS.md concise — focus on what the next agent needs to know
- Include specific file paths and line numbers for in-progress work
- Document "why" decisions were made, not just "what" was done
- Commit STATUS.md so it persists across sessions
- Use `[WIP]` commit prefix for incomplete work snapshots

## References

- Source: https://github.com/Phat-Po/claude-skill-handoff
- Topics: session-management, context-management, agent-handoff, developer-tools
