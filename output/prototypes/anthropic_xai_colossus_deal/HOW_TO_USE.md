# How to Use

## Installation (Claude Code Skill)

This is a **Claude Code skill** — a markdown file that teaches Claude domain-specific knowledge and behavior.

### 1. Copy the skill folder

```bash
mkdir -p ~/.claude/skills/anthropic_xai_colossus_deal
cp SKILL.md ~/.claude/skills/anthropic_xai_colossus_deal/SKILL.md
```

### 2. Verify

```bash
ls ~/.claude/skills/anthropic_xai_colossus_deal/SKILL.md
```

That's it. No packages to install, no API keys needed.

## Trigger Phrases

Claude will activate this skill when you ask about:

| Phrase | Example |
|---|---|
| Anthropic COLOSSUS deal | "What is the Anthropic COLOSSUS deal?" |
| SpaceX S-1 Anthropic | "What does the SpaceX S-1 say about Anthropic?" |
| xAI cloud compute agreement | "Tell me about xAI selling compute to Anthropic" |
| Anthropic infrastructure spend | "How much is Anthropic paying for compute?" |
| COLOSSUS II compute capacity | "What is COLOSSUS II and who uses it?" |

## First 60 Seconds

**Step 1:** Install the skill (see above).

**Step 2:** Open Claude Code and ask:

```
What is the Anthropic COLOSSUS deal?
```

**Expected output** (Claude will respond with something like):

> Anthropic signed a Cloud Services Agreement with xAI (disclosed in SpaceX's
> May 2026 S-1 filing) to access compute capacity across the COLOSSUS and
> COLOSSUS II data centers. Key terms:
>
> - **$1.25 billion/month** through May 2029 (~$45B total)
> - 90-day termination clause by either party
> - Ramp period at reduced fee in May-June 2026
>
> This is one of the largest known cloud compute contracts in the AI industry.
> It signals Anthropic is diversifying beyond AWS and that xAI is monetizing
> spare GPU capacity by leasing to a direct competitor.

**Step 3:** Try a follow-up:

```
How does this compare to Anthropic's AWS partnership?
```

Claude will explain that the COLOSSUS deal supplements (not replaces) the AWS relationship, suggesting AWS capacity alone is insufficient for Anthropic's training and inference needs.

## Running the Demo

To see a standalone analysis without Claude Code:

```bash
pip install -r requirements.txt
bash run.sh
```

This runs a local Python script that prints the deal summary, financial breakdown, and strategic analysis to stdout. No API keys required.
