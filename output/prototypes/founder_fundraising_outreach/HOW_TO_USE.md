# How to Use

## Install the Claude Skill

This is a **Claude Code skill** — a prompt-based template that Claude loads when it detects fundraising-related requests.

### 1. Copy the skill folder

```bash
mkdir -p ~/.claude/skills/founder-fundraising-outreach
cp SKILL.md ~/.claude/skills/founder-fundraising-outreach/SKILL.md
```

### 2. Verify installation

```bash
ls ~/.claude/skills/founder-fundraising-outreach/SKILL.md
```

That's it. No packages to install, no API keys, no server to run.

## Trigger Phrases

The skill activates when you ask Claude things like:

- "Help me write a cold email to a VC partner"
- "Draft a follow-up email after my investor meeting"
- "Prepare my due diligence documents for fundraising"
- "Write an intro blurb for a warm investor introduction"
- "Help me craft outreach for my seed round"

It does **not** activate for general email writing, sales outreach, or marketing copy.

## First 60 Seconds

**Input** (paste into Claude Code):

```
Help me write a cold email to Maria Rodriguez at Gradient Ventures.
My company is Lattice AI — we build real-time compliance monitoring
for fintech companies. We have 18 paying customers and $380K ARR.
We're raising a $3M seed round.
```

**Output** (Claude generates):

```
Subject: Lattice AI — 42% MoM growth in fintech compliance

Hi Maria,

I noticed Gradient Ventures' investment in ComplianceBot — our
approach to real-time compliance monitoring is adjacent.

Lattice AI builds real-time compliance monitoring for fintech
companies, cutting audit prep from weeks to hours. We're raising
a $3M seed round.

Here's where we are:
  - 42% MoM revenue growth over the last 6 months
  - 18 paying enterprise customers including 2 Fortune 500 pilots
  - $380K ARR, up from $45K ARR 9 months ago

Would you have 15 minutes this week or next for a quick intro call?

Best,
Sarah Chen
CEO & Co-Founder, Lattice AI
```

## Running the Standalone Demo

The repo also includes a Python demo that generates all four outreach types with mock data:

```bash
bash run.sh
```

No dependencies beyond Python 3.10+.
