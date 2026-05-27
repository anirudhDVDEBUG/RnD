# How to Use: Authentic Founder Voice

## Install (Claude Code Skill)

```bash
# Clone this repo
git clone <this-repo> authentic_founder_voice
cd authentic_founder_voice

# Copy the skill into your Claude Code skills directory
mkdir -p ~/.claude/skills/authentic_founder_voice
cp SKILL.md ~/.claude/skills/authentic_founder_voice/SKILL.md
```

That's it. No pip install, no API keys, no dependencies for the skill itself.

## Where to put it

```
~/.claude/skills/
  authentic_founder_voice/
    SKILL.md          <-- this file drives Claude's behavior
```

## Trigger phrases

The skill activates automatically when you say things like:

- "Write an email to an investor about our progress"
- "Help me draft a cold outreach to a VC"
- "Make this founder update sound more natural"
- "Review my pitch email — does it sound AI-generated?"
- "Rewrite this so it doesn't sound like ChatGPT wrote it"
- "Draft a YC application response"

## First 60 seconds

**1. Open Claude Code in any project directory.**

**2. Paste a draft and ask for a rewrite:**

```
> Review my pitch email — does it sound AI-generated?

Dear Investors,

I hope this message finds you well. I'm excited to share that our
groundbreaking platform has achieved remarkable traction, with a
revolutionary approach to leveraging cutting-edge ML at the intersection
of real-time data and enterprise workflows. We've seen unprecedented
growth and are poised to disrupt the market.
```

**3. Claude responds with:**

- A list of specific AI red flags found (superlatives, corporate filler, vague claims)
- A rewritten version in authentic founder voice
- The Paul Graham test applied to the result

**Expected output:**

```
RED FLAGS FOUND:
- "I hope this message finds you well" — corporate filler
- "groundbreaking", "revolutionary", "unprecedented" — superlative stacking
- "at the intersection of" — AI cliche
- "leveraging cutting-edge ML" — buzzword density
- "poised to disrupt" — empty rhetoric

REWRITTEN:

Hi —

We built [product]. It [does specific thing]. [X] companies use it
and we're growing [Y]% month over month.

We're raising because [specific reason]. Happy to share a deck
if useful.

[Your name]
```

## Standalone demo (no Claude Code needed)

```bash
pip install -r requirements.txt
bash run.sh
```

This runs a local Python demo that scans sample founder emails for AI red flags and shows before/after rewrites using rule-based heuristics.
