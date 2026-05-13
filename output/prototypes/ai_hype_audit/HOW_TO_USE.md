# How to Use — AI Hype Audit

## Option A: As a Claude Code Skill

### Install

```bash
mkdir -p ~/.claude/skills/ai_hype_audit
cp SKILL.md ~/.claude/skills/ai_hype_audit/SKILL.md
```

### Trigger Phrases

Once installed, Claude Code activates this skill when you say:

- "Review this AI proposal for substance vs. hype"
- "Audit these automation claims — are they realistic?"
- "Check if this AI strategy memo has any technical grounding"
- "Score this AI initiative pitch for buzzword density"
- "Is this automation plan credible or just career theater?"

Claude will then apply the 5-dimension scoring rubric from the skill and return a structured audit report.

### Example Session

```
You: Review this proposal for substance vs. hype:
     "We're deploying an agentic AI system to 10x our pipeline
      and fully automate all outreach. Game-changing paradigm shift."

Claude: SUBSTANCE SCORE: 2/10 — Career Theater
        Flagged: "agentic AI system" (buzzword), "10x" (buzzword),
        "fully automate all" (infeasible claim), "game-changing
        paradigm shift" (double buzzword).
        Suggested: Define what "outreach" steps are automated,
        expected accuracy, cost per message, and human review cadence.
```

## Option B: As a Standalone CLI Tool

### Install

```bash
git clone <this-repo> ai_hype_audit
cd ai_hype_audit
pip install -r requirements.txt  # no external deps needed
```

### Usage

```bash
# Audit from file
python3 audit.py proposal.txt

# Audit from stdin
cat memo.md | python3 audit.py

# Pipe from clipboard (macOS)
pbpaste | python3 audit.py
```

### Output

The tool prints a formatted report with:
- Substance score (1–10)
- Verdict (Ship It / Needs Work / Career Theater)
- Per-dimension scores (buzzword density, specificity, feasibility, ROI, human impact)
- Flagged phrases with explanations and suggested rewrites

## First 60 Seconds

```bash
$ bash run.sh

======================================
 AI Hype Audit — Demo Run
======================================

--------------------------------------
 SAMPLE 1: Hype-Heavy Proposal
--------------------------------------
============================================================
  AI HYPE AUDIT REPORT
============================================================

  SUBSTANCE SCORE: 2/10
  VERDICT: Career Theater

------------------------------------------------------------
  DIMENSION SCORES
------------------------------------------------------------
  Buzzword Density:      85% (lower is better)
  Specificity:           0%
  Feasibility:           40%
  ROI Grounding:         0%
  Human Impact Honesty:  20%

------------------------------------------------------------
  FLAGGED PHRASES
------------------------------------------------------------

  [1] (BUZZWORD)
      "revolutionary AI-first"
      -> "revolutionary" is a buzzword...

--------------------------------------
 SAMPLE 2: Grounded Pilot Proposal
--------------------------------------
  SUBSTANCE SCORE: 8/10
  VERDICT: Ship It
```
