# How to Use Kodro SDD

## This is a Claude Code Skill

Kodro is installed as a **SKILL.md** file that teaches Claude Code the 6-phase spec-driven development workflow. It does not require a server or runtime — it's a prompt-based skill.

## Install

### 1. Drop the skill file

```bash
mkdir -p ~/.claude/skills/kodro_spec_driven_dev
cp SKILL.md ~/.claude/skills/kodro_spec_driven_dev/SKILL.md
```

Or clone from source:

```bash
git clone https://github.com/mharoon1578/kodro.git
cp kodro/SKILL.md ~/.claude/skills/kodro_spec_driven_dev/SKILL.md
```

### 2. Restart Claude Code

The skill is picked up automatically on next session start.

### 3. Trigger phrases

Say any of these to Claude Code:

- "Build this feature using spec-driven development"
- "I want a structured pipeline to develop this — no vibe coding"
- "Generate code from a specification with minimal token usage"
- "Use a multi-phase autonomous approach to build this module"
- "Help me implement this with a disciplined SDD workflow"

The skill will NOT trigger for simple one-off snippets, exploratory prototyping, or when you explicitly want freeform coding.

## First 60 Seconds

**Input** (you say this to Claude Code):

> Build a user authentication module with JWT tokens using spec-driven development

**What happens** (Claude follows the 6 phases):

```
Phase 1 -> Claude writes a structured spec:
           - 7 requirements (REQ-1 through REQ-7)
           - User and Token data models
           - 4 API endpoints
           - 4 constraints

Phase 2 -> Architecture decomposition:
           - user_model, token_model, service, validator, tests
           - Dependency graph and build order

Phase 3 -> Implementation plan:
           - 5 ordered tasks with requirement tracing

Phase 4 -> Code generation:
           - One file per component, each traced to requirements

Phase 5 -> Verification:
           - 100% requirement coverage check
           - BDD-style test stubs for every REQ

Phase 6 -> Integration review:
           - Summary of coverage, deviations, and next steps
```

**Output**: Structured code files with full requirement traceability, generated in focused chunks instead of one massive unstructured blob.

## Running the Local Demo

No API keys needed — the demo runs the pipeline on mock data:

```bash
# Python 3.8+ required, no pip installs needed
bash run.sh
```

This executes the 6-phase pipeline on a sample JWT auth spec and prints:
- The parsed specification
- Architecture decomposition
- Implementation plan with task ordering
- Generated code samples (models, service, tests, validator)
- Requirement coverage report
- Token cost comparison (SDD vs vibe coding)

## Using as a Python Library

```python
from kodro.pipeline import run_pipeline

spec = {
    "name": "My Feature",
    "purpose": "Does X for Y",
    "requirements": [
        {"id": "REQ-1", "text": "Must do A"},
        {"id": "REQ-2", "text": "Must do B"},
    ],
    "data_models": [...],
    "api_endpoints": [...],
    "constraints": [...],
}

result = run_pipeline(spec)
print(result.summary())

for f in result.files:
    print(f.path, len(f.content), "bytes")
```
