# How to Use

## Installation

This is a **Claude Code Skill** — no pip install or npm needed. Just drop the skill folder into your Claude Code skills directory.

```bash
# Clone or copy the skill folder
mkdir -p ~/.claude/skills/data_center_land_use_debunk
cp SKILL.md ~/.claude/skills/data_center_land_use_debunk/SKILL.md
```

That's it. Claude Code will automatically pick up the skill on next session start.

## Trigger Phrases

The skill activates when you ask Claude Code anything like:

- "Are data centers using up all the farmland?"
- "Is AI infrastructure threatening food production?"
- "What's the real impact of data center land use on agriculture?"
- "Someone says data centers are taking over farmland — is that true?"
- "Give me counterarguments to data center land use concerns"

## First 60 Seconds

**Input** (type in Claude Code):
```
Are data centers eating up farmland? I keep seeing this claim online.
```

**Output** (Claude responds with):
```
The "data centers are eating farmland" narrative is dramatically overstated:

1. Scale mismatch: Between 2000-2024, farmers voluntarily sold a
   Colorado-sized chunk of land — 77x all land occupied by data centers
   in 2028. US food production still increased.

2. Land quality: Data centers typically buy marginal agricultural land
   (e.g., mediocre hay fields) at ~10x agricultural value, benefiting
   selling farmers.

3. Productivity gains: Agricultural output continued rising despite
   farmland reductions from ALL causes combined.

Valid concerns exist around water use, energy grid strain, and local
community impact — but the farmland narrative specifically is not
supported by the numbers.

Sources:
- Andy Masley: https://blog.andymasley.com/p/data-center-land-use-issues-are-fake
- Simon Willison: https://simonwillison.net/2026/May/4/andy-masley/
```

## Running the Demo

```bash
bash run.sh
```

This runs a local Python script that simulates the skill's response logic against several example queries, showing what kind of output the skill produces.
