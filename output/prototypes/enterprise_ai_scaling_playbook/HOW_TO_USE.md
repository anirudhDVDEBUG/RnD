# How to Use

## Install

```bash
git clone <this-repo>
cd enterprise_ai_scaling_playbook
# No pip install needed — pure Python stdlib (3.10+)
```

## Run the Demo

```bash
bash run.sh
```

This runs three mock organization profiles and prints their AI maturity reports. A JSON report is also saved to `report.json`.

## Interactive Mode

```bash
python3 assess.py
```

Answer 12 questions (score 1-5 each) and get a custom playbook for your organization.

## Save as JSON

```bash
python3 assess.py --demo --json report.json
python3 assess.py --profile mid_journey --json mid.json
```

## Claude Code Skill Setup

This is a **Claude Code skill**. To install it:

1. Copy the `SKILL.md` file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/enterprise_ai_scaling_playbook
cp SKILL.md ~/.claude/skills/enterprise_ai_scaling_playbook/SKILL.md
```

2. Claude Code will automatically detect the skill. Trigger it with phrases like:
   - "How do we scale AI adoption across our enterprise?"
   - "We need an AI governance framework"
   - "What's the playbook for enterprise AI maturity?"
   - "How do we move from AI experiments to production at scale?"
   - "How do we maintain AI quality and trust as we scale?"

When triggered, Claude will walk you through the 5-phase scaling framework with tailored advice.

## First 60 Seconds

```
$ bash run.sh

==> Enterprise AI Scaling Playbook — Demo

############################################################
  ENTERPRISE AI SCALING PLAYBOOK — DEMO MODE
  Analyzing 3 sample organizations...
############################################################

============================================================
ENTERPRISE AI SCALING PLAYBOOK
Organization: Acme Widgets Inc. (Early-stage AI adoption)
============================================================

Overall AI Maturity Score: 1.3 / 5.0
  [########----------------------]
Current Phase: Phase 1 — Build Trust with Early Wins

------------------------------------------------------------
DIMENSION SCORES
------------------------------------------------------------
  Governance & Risk              1.5  [######--------------]
  Leadership & Strategy          1.5  [######--------------]
  Quality & Evaluation           1.5  [######--------------]
  Scale & Impact                 1.0  [####----------------]
  Talent & Culture               1.5  [######--------------]
  Workflow Integration           1.0  [####----------------]

------------------------------------------------------------
RECOMMENDATIONS
------------------------------------------------------------
  [HIGH PRIORITY]
  1. (Phase 1) Secure executive AI sponsorship
  2. (Phase 2) Establish AI governance framework
  3. (Phase 1) Launch AI upskilling program
  ...

------------------------------------------------------------
NEXT 90-DAY MILESTONES
------------------------------------------------------------
  1. Complete 2 pilot AI use cases with measurable ROI
  2. Present pilot results to leadership for buy-in
  ...
```

Two more profiles (mid-journey, advanced) follow with increasingly mature scores and different recommendations.
