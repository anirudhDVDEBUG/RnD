# How to Use: Claude Code Swarm Toolkit

## What this is

A **Claude Code Skill** — a markdown instruction file that teaches Claude Code how to orchestrate multiple parallel subagents in swarm patterns. No external dependencies or API keys required beyond your existing Claude Code setup.

## Install

### 1. Create the skill directory

```bash
mkdir -p ~/.claude/skills/claude-code-swarm-toolkit
```

### 2. Copy the skill file

```bash
cp SKILL.md ~/.claude/skills/claude-code-swarm-toolkit/SKILL.md
```

Or clone from source:

```bash
git clone https://github.com/keerthanapranesh/Claude-Code-Swarm-Toolkit.git
cp Claude-Code-Swarm-Toolkit/SKILL.md ~/.claude/skills/claude-code-swarm-toolkit/SKILL.md
```

### 3. Verify

```bash
cat ~/.claude/skills/claude-code-swarm-toolkit/SKILL.md
```

That's it. Claude Code will now pick up the skill automatically.

## Trigger Phrases

Say any of these to Claude Code to activate swarm orchestration:

| Phrase | What happens |
|--------|-------------|
| "Break this task into parallel agents and run them as a swarm" | Full swarm decomposition |
| "Use swarm orchestration to refactor these modules simultaneously" | Fan-out pattern on modules |
| "Fan out subagents to research multiple topics in parallel" | Explore-type swarm |
| "Coordinate multiple agents to implement features across different files" | Multi-file fan-out |
| "Run a multi-agent pipeline for this complex task" | Pipeline pattern |

## First 60 Seconds

**Input (you type in Claude Code):**

```
Break this into a swarm: add unit tests for the auth module,
payments module, and notifications module in parallel.
```

**What Claude Code does:**

1. Decomposes into 3 independent subtasks
2. Launches 3 parallel Agent tool calls:
   - Agent 1: "Write unit tests for auth module in tests/test_auth.py..."
   - Agent 2: "Write unit tests for payments module in tests/test_payments.py..."
   - Agent 3: "Write unit tests for notifications module in tests/test_notifications.py..."
3. Collects results from all 3 agents
4. Reviews for conflicts (shared fixtures, imports)
5. Reports: "All 3 test files created. Running pytest... 24 tests pass."

**Output you see:**

```
Swarm completed: 3/3 agents succeeded
- tests/test_auth.py: 8 tests (all pass)
- tests/test_payments.py: 9 tests (all pass)
- tests/test_notifications.py: 7 tests (all pass)
No conflicts detected across modules.
```

## Swarm Patterns Quick Reference

| Pattern | When to use | Example prompt |
|---------|-------------|----------------|
| **Fan-out/Fan-in** | Independent parallel tasks | "Refactor these 4 modules simultaneously" |
| **Pipeline** | Sequential dependent stages | "Research, then design, then implement" |
| **Map-Reduce** | Same op on many files | "Add type hints to all 20 service files" |
| **Explore-then-Act** | Research before action | "Find all security issues, then fix them" |
