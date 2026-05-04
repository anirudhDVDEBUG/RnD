# How to Use

## Installation

### As a Claude Skill (recommended)

```bash
# Clone the skill into your Claude skills directory
mkdir -p ~/.claude/skills/anthropic_grade_optimizer
cp SKILL.md ~/.claude/skills/anthropic_grade_optimizer/SKILL.md
```

### As a standalone CLI tool

```bash
git clone https://github.com/l0z4n0-a1/skill-anthropic-grade-optimizer.git
cd skill-anthropic-grade-optimizer
pip install -r requirements.txt
python audit.py path/to/your/CLAUDE.md
```

## Trigger Phrases (Skill Mode)

Once installed as a skill, say any of:

- "Audit my CLAUDE.md for Anthropic best practices"
- "Grade this SKILL.md against Anthropic prompt rules"
- "Lint my subagent prompts for compliance"
- "Optimize my MCP server config for Claude"
- "Review my hook definitions against Anthropic guidelines"

Claude will automatically invoke the skill and produce a structured audit report.

## First 60 Seconds

**Input:** Any Claude-directing artifact. Here's a minimal example:

```bash
$ python audit.py sample_claude.md
```

**Output:**

```
============================================================
ANTHROPIC GRADE OPTIMIZER — Audit Report
============================================================
Artifact: sample_claude.md
Artifact type: CLAUDE.md

SUMMARY
  Overall grade: B-
  Dimensions passing: 7/11
  Critical findings: 3
  Voice drift detected: Yes

FINDINGS BY DIMENSION

  1. Clarity [PASS]
     All instructions use unambiguous imperative form.

  2. Specificity [WARN]
     Line 8: "Try to be helpful" — vague guidance without concrete behavior.
     Rule: §3.1 (Specificity) — Use concrete examples over abstract directives.

  3. Structure [PASS]
     Well-organized with markdown headers and logical section flow.

  4. Completeness [WARN]
     Missing: error handling instructions, context management hints.
     Rule: §5.3 (Completeness) — Define behavior for edge cases.

  5. Consistency [PASS]
     No contradictory instructions detected.

  6. Voice Alignment [FAIL] *** CRITICAL ***
     Lines 12-14: Shifts from imperative ("Always respond...") to
     conversational ("You might want to..."). Voice drift detected.
     Rule: §4.2 (Voice Consistency) — Maintain uniform directive tone.

  ...

RECOMMENDED FIXES (priority order)
  1. [Voice] Lines 12-14: Replace "You might want to consider..." with
     "Consider..." — Rule §4.2
  2. [Specificity] Line 8: Replace "Try to be helpful" with specific
     behavior: "Provide actionable code examples for every suggestion" — Rule §3.1
  3. [Completeness] Add error-handling section — Rule §5.3
```

## CLI Options

```
python audit.py <file>           # Audit a single file
python audit.py <file> --json    # Output as JSON
python audit.py <file> --fix     # Show before/after diffs for each fix
python audit.py <dir>            # Audit all supported files in directory
```
