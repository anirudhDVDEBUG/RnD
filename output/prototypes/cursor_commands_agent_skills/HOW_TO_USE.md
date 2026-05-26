# How to Use

## Install

```bash
git clone <this-repo> cursor_commands_agent_skills
cd cursor_commands_agent_skills
pip install -r requirements.txt   # only pyyaml
```

## As a Claude Code Skill

Drop the skill folder into your skills directory:

```bash
cp -r . ~/.claude/skills/cursor_commands_agent_skills/
```

The SKILL.md at the root is auto-loaded by Claude Code. Trigger phrases that activate it:

- "Create a reusable slash command with quality evaluation criteria"
- "Set up CI ship-gate checks that validate agent output quality"
- "Define behavioral eval rubrics for my agent skills"
- "Build a structured agent skill with merge-safe installation"
- "Add prompt-based quality gates to my development workflow"

## CLI Usage (standalone)

### Run evals against mock outputs

```bash
python3 eval/run_evals.py \
  --rubrics-dir eval/rubrics \
  --mock-dir eval/mock_outputs \
  --output eval-results.json
```

### Check the ship-gate

```bash
python3 eval/check_gate.py --results eval-results.json
```

Exit code 0 = all gates pass. Non-zero = at least one command failed.

## First 60 Seconds

```
$ bash run.sh

============================================
  Agent Skills — Behavioral Eval Demo
============================================

[1/4] Installing dependencies ...
  Done.

[2/4] Discovered slash commands:
  - /review   (review.md)
  - /test-plan (test-plan.md)
  - /refactor  (refactor.md)

[3/4] Discovered eval rubrics:
  - review
  - test-plan
  - refactor

[4/4] Running behavioral evals against mock outputs ...

================================================================
  SHIP-GATE QUALITY REPORT
================================================================

  PASS  /review  (score: 92%  threshold: 80%)
  ────────────────────────────────────────────────
    PASS  identifies_real_issues     [████████████████████] 100%
    PASS  actionable_suggestions     [████████████████░░░░]  75%
    PASS  correct_severity           [████████████████████] 100%
    PASS  no_false_positives         [████████████████████] 100%
    PASS  format_compliance          [████████████████████] 100%

  ... (test-plan, refactor results follow)

  OVERALL: PASS
================================================================

Ship-gate PASSED. Safe to merge.
```

**What happened:** The eval runner loaded 3 rubrics, scored 3 mock agent outputs against 15 criteria using heuristic scorers, and the gate checker confirmed all commands pass their quality thresholds.

## Adding Your Own Command

1. Create `commands/your-command.md` following the template (Purpose, Inputs, Behavior, Output Format).
2. Create `eval/rubrics/your-command.yaml` with weighted criteria.
3. Create `eval/mock_outputs/your-command.md` with a sample agent output.
4. Run `bash run.sh` — your new command appears in the report.

## CI Integration

Copy `.github/workflows/skill-eval.yml` into your repo. The workflow runs on every PR and blocks merge if any command's eval score drops below its threshold.
