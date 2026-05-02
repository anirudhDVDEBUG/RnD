# How to Use

## This is a Claude Skill

### Install the Skill

1. Copy the `SKILL.md` file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/ai_native_dev_workflow
cp SKILL.md ~/.claude/skills/ai_native_dev_workflow/SKILL.md
```

2. That's it. No dependencies, no API keys.

### Trigger Phrases

Once installed, Claude will activate this skill when you say things like:

- "How do I set up a multi-agent AI development workflow?"
- "I want AI agents to work in parallel on my project"
- "What's the 4-phase framework for AI-native development?"
- "How do I structure a new project for AI agent collaboration?"
- "How do I onboard AI agents to an existing codebase?"

Claude will then walk you through the Align > Design > Build > Integrate phases, generating the contract artifacts for your specific project.

## Running the Standalone Demo

The demo requires no external packages (Python 3.10+ stdlib only).

```bash
git clone https://github.com/tianji-qingtian/AI-Native.git  # optional — for the source methodology
cd ai_native_dev_workflow
bash run.sh
```

### First 60 Seconds

**Input:** Run `bash run.sh` — no arguments needed. The demo uses a built-in e-commerce API scenario.

**Output:** The script runs both scenarios (greenfield + existing codebase) and generates artifacts:

```
demo_output/
  ARCHITECTURE.md          # Module map, tech stack, ownership
  CONVENTIONS.md           # Branch naming, commit format, file patterns
  CLAUDE.md                # Shared context file for all agents
  TASK_BOARD.md            # Parallelizable task batches with agent assignments
  INTEGRATION_REPORT.md    # Merge order, contract check results
  contracts/
    contracts.json         # Machine-readable interface definitions
  existing_codebase/       # Same artifacts for the "add to monolith" scenario
    ...
```

The terminal also prints the full task board and anti-pattern quick reference.

## Using the Engine Programmatically

```python
from workflow_engine import run_full_pipeline

plan, integration = run_full_pipeline(
    project_name="My SaaS",
    description="Multi-tenant analytics dashboard",
    tech_stack=["Python", "FastAPI", "React", "PostgreSQL"],
    modules_spec=[
        {"name": "auth", "responsibility": "User auth + RBAC", "dependencies": []},
        {"name": "ingest", "responsibility": "Data pipeline", "dependencies": ["auth"]},
        {"name": "dashboard", "responsibility": "Charts + queries", "dependencies": ["auth", "ingest"]},
    ],
    output_dir="my_output",
)
```

This generates all Phase 1-4 artifacts in `my_output/`.
