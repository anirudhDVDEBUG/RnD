# How to Use — Hypothesis Validator

## What this is

A **Claude Code skill** (a SKILL.md prompt file) that teaches Claude to run a structured startup-hypothesis validation when triggered by natural language.

## Install (30 seconds)

### 1. Clone or copy the skill file

```bash
# Option A: clone the repo
git clone https://github.com/evgeniy038/hypothesis-validator.git
cp -r hypothesis-validator/SKILL.md ~/.claude/skills/hypothesis_validator/SKILL.md

# Option B: copy from this prototype
mkdir -p ~/.claude/skills/hypothesis_validator
cp SKILL.md ~/.claude/skills/hypothesis_validator/SKILL.md
```

### 2. Verify Claude sees it

Open Claude Code and type:

```
validate my hypothesis
```

Claude should respond by asking you to state your hypothesis in the structured format. If it doesn't, check that `~/.claude/skills/hypothesis_validator/SKILL.md` exists and restart Claude Code.

### 3. No dependencies

This is a pure prompt skill — no `pip install`, no `npm install`, no API keys. Claude uses its built-in web-search capability for the evidence-scan step.

## Trigger Phrases

Any of these will activate the skill:

- "Validate my startup hypothesis"
- "Is this idea worth building?"
- "Who is my ideal customer and will they pay?"
- "Run a go-to-market reality check"
- "Help me find product-market fit signals"

## First 60 Seconds

**Input** (paste into Claude Code):

```
Validate my hypothesis: Solo SaaS founders (bootstrapped, $0-10K MRR) have
trouble writing cold outreach emails that convert, and will pay $19/mo for
an AI tool that generates personalized cold emails from LinkedIn profile data,
because founders waste 3+ hours/week on manual prospecting.
```

**Output** (Claude produces a report like this):

```
## Hypothesis Validation Report -- 2026-05-14

### Hypothesis
Solo SaaS founders (bootstrapped, $0-10K MRR) have trouble writing cold
outreach emails that convert...

### Scorecard
| Dimension       | Rating              | Key Finding                              |
|-----------------|---------------------|------------------------------------------|
| ICP Clarity     | Sharp               | Named segment on IH, Twitter, YC forums  |
| Evidence        | Supporting          | Reddit/IH threads, competitors exist     |
| Money Signals   | Strong              | Lemlist $30/mo, Instantly $29/mo         |
| GTM Feasibility | Needs experimentation | Crowded space, need differentiation    |

### Overall Verdict
[YELLOW] Pivot needed -- Strong demand but crowded market; need unique angle

### Recommended Next Steps
1. [ ] Interview 10 founders about what existing tools miss
2. [ ] Test differentiation: "LinkedIn-native" angle vs general cold email
3. [ ] Build landing page, measure waitlist conversion vs competitors
```

## Running the Standalone Demo

To see the output format without installing the skill:

```bash
bash run.sh
```

This runs two mock validations (strong and weak hypotheses) using Python 3 with no external dependencies.
