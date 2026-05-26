---
name: cursor_commands_agent_skills
description: |
  Implements generic agent slash commands and skills with behavioral eval rubrics and CI ship-gate checks. Adapts the cursor-commands pattern for Claude Code: structured command definitions, quality rubrics for agent output evaluation, and CI integration for shipping gates.
  
  Triggers: agent skill commands, slash command definitions, behavioral eval rubrics, CI ship-gate quality checks, agent prompt engineering patterns
---

# Cursor Commands & Agent Skills

A structured approach to defining reusable agent slash commands and skills with built-in behavioral evaluation rubrics and CI ship-gate checks.

## When to use

- "Create a reusable slash command with quality evaluation criteria"
- "Set up CI ship-gate checks that validate agent output quality"
- "Define behavioral eval rubrics for my agent skills"
- "Build a structured agent skill with merge-safe installation"
- "Add prompt-based quality gates to my development workflow"

## How to use

### 1. Define a Slash Command

Create a command definition with clear structure:

```markdown
# /command-name

## Purpose
One-line description of what this command does.

## Inputs
- `arg1`: Description (required)
- `arg2`: Description (optional, default: value)

## Behavior
1. Step-by-step instructions for the agent
2. Include constraints and guardrails
3. Specify output format expectations

## Output Format
Describe the expected structure of the response.
```

### 2. Create Behavioral Eval Rubrics

For each command, define evaluation criteria:

```yaml
eval:
  command: /command-name
  rubric:
    - criterion: "Output follows specified format"
      weight: 0.3
      pass_threshold: 0.8
    - criterion: "All required sections present"
      weight: 0.3
      pass_threshold: 1.0
    - criterion: "No hallucinated information"
      weight: 0.2
      pass_threshold: 1.0
    - criterion: "Actionable and specific guidance"
      weight: 0.2
      pass_threshold: 0.7
  overall_pass_threshold: 0.8
```

### 3. Add CI Ship-Gate Checks

Integrate quality gates into your CI pipeline:

```yaml
# .github/workflows/skill-eval.yml
name: Skill Quality Gate
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run behavioral evals
        run: |
          python eval/run_evals.py \
            --commands-dir ./commands/ \
            --rubrics-dir ./eval/rubrics/ \
            --threshold 0.8
      - name: Check results
        run: |
          python eval/check_gate.py --results eval-results.json
```

### 4. Merge-Safe Installation

Structure commands for safe installation without conflicts:

```bash
# Install commands to user config (non-destructive merge)
project_root/
  commands/
    /review.md        # Code review command
    /test-plan.md     # Test plan generation
    /refactor.md      # Refactoring guidance
    /explain.md       # Code explanation
  eval/
    rubrics/          # Eval criteria per command
    run_evals.py      # Evaluation runner
    check_gate.py     # CI gate checker
  CLAUDE.md           # Project instructions
```

### 5. Example: Code Review Command with Rubric

**Command** (`commands/review.md`):
```markdown
# /review

## Purpose
Perform a structured code review on staged changes.

## Behavior
1. Analyze git diff for staged changes
2. Check for: security issues, performance problems, style violations, logic errors
3. Rate severity: critical, warning, info
4. Provide specific fix suggestions with code snippets

## Output Format
- Summary (1-2 sentences)
- Findings list with severity, file, line, description, suggestion
- Overall assessment: ship / needs-work / block
```

**Rubric** (`eval/rubrics/review.yaml`):
```yaml
criterion:
  - name: identifies_real_issues
    description: "Findings reference actual problems in the diff"
    weight: 0.4
  - name: actionable_suggestions
    description: "Each finding includes a concrete fix"
    weight: 0.3
  - name: correct_severity
    description: "Severity ratings match issue impact"
    weight: 0.2
  - name: no_false_positives
    description: "No fabricated issues that don't exist in the code"
    weight: 0.1
```

## Key Principles

- **Composable**: Each command is self-contained and can be used independently
- **Evaluable**: Every command has measurable quality criteria
- **CI-integrated**: Ship-gate checks prevent regression in agent output quality
- **Merge-safe**: Installation never overwrites existing user configuration
- **Versioned**: Commands and rubrics are version-controlled alongside code

## References

- Source: [emaraschio/cursor-commands](https://github.com/emaraschio/cursor-commands) - Generic Cursor slash commands and Agent Skills with behavioral eval rubrics and CI ship-gate checks
