# How to Use — Build DNA Business Ideation

## This is a Claude Code Skill

No pip/npm install required. The skill is a `SKILL.md` file that Claude Code loads as a prompt template.

### Install

1. Create the skill directory:

```bash
mkdir -p ~/.claude/skills/build_dna_business_ideation
```

2. Copy the skill file:

```bash
cp SKILL.md ~/.claude/skills/build_dna_business_ideation/SKILL.md
```

3. Restart Claude Code (or open a new session).

### Trigger Phrases

Say any of these in a Claude Code session:

- **"build a business around my skills"**
- "find startup ideas for me"
- "what business should I build"
- "business DNA"
- "founder ideation"
- "side hustle ideas"
- "MVP roadmap from my strengths"

Claude will begin the 3-phase intake automatically.

## First 60 Seconds

```
You:    "build a business around my skills"

Claude: "Let's extract your founder DNA. I'll ask 5 categories of questions..."

        Phase 1 — Skills & Expertise
        Claude asks: "What are your top 3-5 professional skills?"
        You answer: "Python, data analysis, technical writing"
        Claude asks: "What industries have you worked in?"
        ...

        Phase 2 — Claude generates 4 personalized ideas:
        [1] DevDash Templates — "Pre-built dashboards for eng teams"
            Why YOU: You built dashboards used by 200+ engineers...
            Difficulty: Tech 2/5 | Mktg 3/5 | Ops 1/5

        [2] MicroMove Advisor — "Paid newsletter on monolith migrations"
        ...

        Phase 3 — You pick an idea, Claude produces:
        - Market analysis (TAM, competitors, timing)
        - GTM plan (pre-launch → launch → post-launch)
        - MVP roadmap (week-by-week, 4 weeks)
        - 72-hour action plan (hour-by-hour to first $)
```

## Running the Demo

The demo simulates all 3 phases with a mock founder profile (no API keys needed):

```bash
bash run.sh
```

Output is printed to the terminal and also saved as `output.json` for programmatic use.
