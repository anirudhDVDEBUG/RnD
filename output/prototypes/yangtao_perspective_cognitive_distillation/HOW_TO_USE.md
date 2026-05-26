# How to Use

## Installation (Claude Code Skill)

This is a **Claude Code Skill** — a markdown-based prompt enhancement that loads automatically when trigger phrases are detected.

### Step 1: Clone the skill folder

```bash
git clone https://github.com/situker/situk-yangtao-perspective.git
mkdir -p ~/.claude/skills/yangtao-perspective
cp situk-yangtao-perspective/SKILL.md ~/.claude/skills/yangtao-perspective/SKILL.md
```

### Step 2: Verify installation

```bash
ls ~/.claude/skills/yangtao-perspective/SKILL.md
```

The skill is now active in all Claude Code sessions.

## Trigger Phrases

Claude Code will automatically activate this skill when you use phrases like:

- `"Analyze this using Yang Tao's perspective"`
- `"yangtao perspective on [topic]"`
- `"杨涛视角"`
- `"How would 涛哥 approach this?"`
- `"Apply grassroots entrepreneurship thinking"`
- `"personal IP strategy"`
- `"grassroots business thinking"`

## First 60 Seconds

After installing the skill, open Claude Code and try:

```
> yangtao perspective: I have 5000 Twitter followers and want to monetize with a paid community

Expected output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sharp Insight (锐利洞察):
"5000 followers is not an audience — it's a distribution channel.
 The question isn't 'how to charge them' but 'what trust debt have you accumulated?'"

Framework Analysis:
1. Trust Accumulation Assessment (信任积累评估)
   - Engagement rate → real audience size estimate
   - Content consistency score → trust depth

2. Monetization Path (生财路径)
   - Phase 1: Free high-value resource → email list (2 weeks)
   - Phase 2: Low-ticket offer $29 → validate demand (1 week)
   - Phase 3: Community at $99/quarter → only after 50+ low-ticket sales

3. Immediate Actions (立即行动):
   ☐ Post a "best of" thread linking your top 10 insights
   ☐ Add a free PDF lead magnet to your bio link
   ☐ DM your 20 most engaged followers asking what they'd pay for
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Using the Python Demo Locally

The included `yangtao_engine.py` demonstrates the cognitive framework logic offline:

```bash
pip install -r requirements.txt
python yangtao_engine.py "I want to sell an online course about prompt engineering"
```

This runs without API keys using the built-in framework templates.
