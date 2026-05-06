# How to Use

## Option A: Install as a Claude Code Skill

1. Copy the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/yc_openai_stake_analysis
cp SKILL.md ~/.claude/skills/yc_openai_stake_analysis/SKILL.md
```

2. Restart Claude Code (or start a new session).

3. Trigger the skill with any of these phrases:
   - "What is Y Combinator's stake in OpenAI?"
   - "How much is YC's OpenAI investment worth?"
   - "What's the biggest YC return ever?"
   - "How does OpenAI's valuation affect its early backers?"

Claude will respond with sourced facts, valuation context, and analysis points drawn from the skill's knowledge base.

## Option B: Run the Standalone Demo

No API keys or external dependencies required — pure Python 3.10+ stdlib.

```bash
git clone <this-repo>
cd yc_openai_stake_analysis
bash run.sh
```

### First 60 seconds

**Input:**
```bash
bash run.sh
```

**Output:**
```
╔══════════════════════════════════════════════════════════════╗
║  Y COMBINATOR'S STAKE IN OPENAI — KEY NUMBERS              ║
╠══════════════════════════════════════════════════════════════╣
║  OpenAI valuation (May 2026):          $852.0B              ║
║  YC ownership stake:                      0.6%              ║
║  Implied stake value:                    $5.1B              ║
║  Estimated initial investment:           $0.2M              ║
║  Estimated return multiple:           34,080x               ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────┬──────────┬───────────────┬───────────────┐
│ Investment           │ Stake %  │ Stake Value   │ Return Mult.  │
├──────────────────────┼──────────┼───────────────┼───────────────┤
│ YC → OpenAI  ◀       │    0.6%  │         $5.1B │      34,080x  │
│ YC → Stripe          │    0.5%  │         $1.1B │       9,167x  │
│ YC → Airbnb          │    0.7%  │       $525.0M │  26,250,000x  │
│ ...                                                             │
└──────────────────────┴──────────┴───────────────┴───────────────┘

SENSITIVITY: Stake value at different valuations
──────────────────────────────────────────────────
  At  $300.0B valuation → stake = $1.8B
  At  $852.0B valuation → stake = $5.1B
  At $1,500.0B valuation → stake = $9.0B

Structured output written to output.json
```

The demo also writes `output.json` with machine-readable data for downstream pipelines.
