# How to Use: Sprint Orchestrator

## What It Is

A **Claude Code skill** (not an MCP server). It teaches Claude Code how to break a project into parallel tasks, assign them to multiple chat sessions, and coordinate execution in phased sprints.

## Install

### 1. Clone the skill

```bash
git clone https://github.com/lipefur/sprint-orchestrator.git
```

### 2. Drop the SKILL.md into your skills directory

```bash
mkdir -p ~/.claude/skills/sprint-orchestrator
cp sprint-orchestrator/SKILL.md ~/.claude/skills/sprint-orchestrator/SKILL.md
```

That's it. No `pip install`, no `npm install`, no API keys. Claude Code reads the SKILL.md file and learns the orchestration workflow.

### 3. Verify

Open Claude Code and type one of the trigger phrases below. Claude should respond with a sprint planning workflow.

## Trigger Phrases

These phrases activate the skill inside Claude Code:

- "Orchestrate a sprint across multiple agents"
- "Run a multi-chat development sprint"
- "Coordinate parallel work across Claude sessions"
- "Plan and execute a sprint with multiple agents"
- "Break this project into parallel tasks for a sprint"

## First 60 Seconds

**Input** (type into Claude Code):

```
Orchestrate a sprint to build a SaaS landing page with pricing,
testimonials, and a signup form. Use 3 agents.
```

**What happens:**

1. Claude generates a **sprint plan** with phases and task assignments
2. Each task is scoped to specific files to avoid merge conflicts
3. Claude tells you which commands to run in each chat session
4. At phase boundaries, it verifies all tasks before moving on
5. After completion, it runs acceptance criteria checks

**Output** (you'll see something like):

```
# Sprint Plan: SaaS Landing Page

## Phase 1 - Foundation (parallel)
- Task 1.1: Hero section & nav       -> Agent A  [Hero.tsx, Nav.tsx]
- Task 1.2: Pricing cards             -> Agent B  [Pricing.tsx, plans.json]
- Task 1.3: Testimonials carousel     -> Agent C  [Testimonials.tsx]

## Phase 2 - Integration (depends on Phase 1)
- Task 2.1: Signup form               -> Agent A  [SignupForm.tsx]
- Task 2.2: Page assembly & routing   -> Agent B  [App.tsx]

## Phase 3 - QA & Polish
- Task 3.1: Responsive testing        -> Agent A
- Task 3.2: Accessibility audit       -> Agent C

All acceptance criteria verified. Sprint complete.
```

## Running the Demo

```bash
bash run.sh
```

This runs a self-contained simulation with two demo projects, showing:
- Dependency graph visualization
- Gantt chart of parallel execution
- File isolation matrix (conflict detection)
- Live progress tracking per agent
- Markdown sprint report generation

No external API keys or services required.
