# How to Use ERPAVal Workflow

## What this is

A **Claude Code skill** that teaches Claude to follow a disciplined six-phase development loop instead of jumping straight to code. It classifies each task, routes it through the right phases with the right emphasis, and compounds lessons for future tasks.

## Install the skill

```bash
# 1. Create the skill directory
mkdir -p ~/.claude/skills/erpaval_workflow

# 2. Copy the skill file
cp SKILL.md ~/.claude/skills/erpaval_workflow/SKILL.md
```

That's it. Claude Code automatically discovers skills in `~/.claude/skills/`.

## Trigger phrases

Say any of these to Claude Code to activate the ERPAVal workflow:

- `"use erpaval"` or `"erpaval workflow"`
- `"explore research plan act validate"`
- `"autonomous development workflow"`
- `"six-phase development"`
- `"compound lessons"`

### Examples

```
> Use ERPAVal to fix the login timeout bug
> Apply the six-phase workflow to implement Stripe integration
> Run the explore-research-plan-act-validate-compound cycle on this refactor
```

## First 60 seconds

**Step 1:** Install the skill (see above).

**Step 2:** Open Claude Code in any project.

**Step 3:** Type:

```
Use ERPAVal to fix the login timeout bug
```

**What happens:**

1. **Classifier** detects "bug fix" pattern, sets emphasis on Explore + Validate.
2. **Explore** — Claude reads auth module, maps dependencies, identifies timeout handling.
3. **Research** — Checks the lessons store for prior fixes, finds similar retry patterns.
4. **Plan** — Defines exact changes: increase timeout in config, add retry in auth.py:45, write test.
5. **Act** — Implements the three changes with minimal diff.
6. **Validate** — Runs test suite, reviews diff, confirms no regressions.
7. **Compound** — Writes lesson: "Auth module uses 30s default timeout; retry pattern at auth.py:45".

Next time you hit a timeout issue, the Research phase will surface that lesson automatically.

## Run the standalone demo

```bash
bash run.sh
```

This runs three demo tasks (bug fix, feature, refactor) through the workflow engine with mock data. No API keys or external services needed. Output shows classifier routing, phase execution, and the compounded lessons store.

## Lessons store location

The skill stores lessons in `.claude/lessons.md` (or your project's preferred location). You can also configure it to use `lessons.json` for structured access. The demo uses a temporary JSON file that is cleaned up after each run.

## Customization

The workflow is defined entirely in `SKILL.md`. To adjust phase behavior:

- Edit the phase descriptions to match your team's conventions
- Add or remove classifier keywords in the routing section
- Change the lessons store path to fit your project structure
