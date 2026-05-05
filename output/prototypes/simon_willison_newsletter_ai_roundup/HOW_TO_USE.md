# How to Use

## Option A: Install as a Claude Code Skill

### 1. Drop the skill file

```bash
mkdir -p ~/.claude/skills/simon_willison_newsletter_ai_roundup
cp SKILL.md ~/.claude/skills/simon_willison_newsletter_ai_roundup/SKILL.md
```

### 2. Trigger phrases that activate it

- "What were the big LLM releases this month?"
- "Summarize Simon Willison's latest newsletter"
- "Give me an AI industry roundup for April 2026"
- "What's new with Opus 4.7, GPT-5.5, or Claude Mythos?"
- "What models launched recently and how do prices compare?"

### 3. What Claude does when triggered

Claude will fetch the latest newsletter content (or use the free archive for previous months), extract model releases, pricing, security findings, and tool picks, then present a structured summary matching the newsletter's own sections.

---

## Option B: Run Standalone (Demo)

### Install

```bash
git clone <this-repo>
cd simon_willison_newsletter_ai_roundup
pip install -r requirements.txt  # no external deps needed
```

### Run

```bash
bash run.sh
```

Or directly:

```bash
python3 roundup.py           # Pretty-printed roundup
python3 roundup.py --json    # Structured JSON output
python3 roundup.py --export  # Save JSON to file
```

---

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output:**
```
============================================================
  SIMON WILLISON'S AI ROUNDUP - APRIL 2026
============================================================
  Source: https://simonwillison.net/2026/May/4/april-newsletter/

## Major Model Releases
   Two headline launches dominated April: Anthropic's Opus 4.7 and
   OpenAI's GPT-5.5. Both arrived with significant price increases...

   - Opus 4.7 launched at $25/$75 per M tokens (up from $15/$75)
   - GPT-5.5 launched at $20/$60 per M tokens with 1M context window
   ...

## Model Pricing Comparison
  Model              Provider     Input      Output     Delta
  Opus 4.7           Anthropic    $25/M      $75/M      +67% input vs Opus 4.5
  GPT-5.5            OpenAI       $20/M      $60/M      +33% vs GPT-5
  ...
```

---

## Access Notes

- **Current month newsletter:** Requires [GitHub Sponsors ($10/month)](https://github.com/sponsors/simonw/)
- **Previous months (free):** [simonw/monthly-newsletter-archive](https://github.com/simonw/monthly-newsletter-archive)
- **Blog feed (always free):** `https://simonwillison.net/atom/everything/`
