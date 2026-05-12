# How to Use

## Installation

No dependencies required — pure Python 3.10+ stdlib.

```bash
git clone <this-repo>
cd ai_maintenance_cost_auditor
python3 auditor.py --help
```

## As a Claude Code Skill

This is primarily designed as a **Claude Code skill**. To install:

1. Copy the `SKILL.md` file into your skills directory:

```bash
mkdir -p ~/.claude/skills/ai_maintenance_cost_auditor
cp SKILL.md ~/.claude/skills/ai_maintenance_cost_auditor/SKILL.md
```

2. Claude Code will automatically pick up the skill. Trigger it with phrases like:

- "Review this AI-generated code for maintainability"
- "Audit the technical debt impact of these changes"
- "Is this AI-written code going to cost us later?"
- "Assess maintenance cost of this PR"
- "Check if our AI coding output is sustainable"

Claude will walk through the 5-step audit process from the skill: identify scope, run the checklist, calculate the maintenance ratio, produce recommendations, and deliver a verdict.

## As a CLI Tool

Run against any file or directory:

```bash
# Audit a single file (assumes 3x AI speed gain)
python3 auditor.py src/app.py

# Audit a directory with a custom speed multiplier
python3 auditor.py ./src --speed 5

# JSON output for CI integration
python3 auditor.py ./src --speed 3 --json

# Disable color (for piping)
python3 auditor.py ./src --no-color > report.txt
```

**Supported languages:** `.py`, `.js`, `.ts`, `.jsx`, `.tsx`

## First 60 Seconds

```bash
$ bash run.sh

--- Auditing CLEAN sample (good_code.py) at 3x speed ---

======================================================================
  AI MAINTENANCE COST AUDIT REPORT
======================================================================

  Files scanned:     1
  Total lines:       37
  Findings:          0
  Speed multiplier:  3.0x

  samples/good_code.py  (37 lines)
    Maintenance multiplier: 0.8x
    Speed x Maintenance:    2.4x  [RISKY]

======================================================================
  OVERALL VERDICT
======================================================================

  Average maintenance multiplier:  0.8x
  Speed multiplier:               3.0x
  Product (speed x maintenance):  2.4x

  Shore's Rule: speed x maintenance must be <= 1.0
  Result: RISKY

--- Auditing MESSY sample (bad_code.py) at 3x speed ---

  ... (multiple findings: dead code, bare excepts, deep nesting, duplication) ...

  Result: UNSUSTAINABLE
```

Even the clean code is "RISKY" at 3x speed — Shore's bar is deliberately high. The point isn't to ban AI coding; it's to make the maintenance cost tradeoff explicit.

## CI Integration

Add to your pipeline:

```bash
result=$(python3 auditor.py ./src --speed 3 --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data['overall']['verdict'])
")

if [ "$result" = "UNSUSTAINABLE" ]; then
    echo "Maintenance cost audit failed"
    exit 1
fi
```
