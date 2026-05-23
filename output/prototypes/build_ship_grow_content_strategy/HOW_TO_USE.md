# How to Use: Build Ship Grow Content Strategy

## Installation (Claude Code Skill)

This is a **Claude Code skill** -- a markdown file that teaches Claude Code new capabilities via its skill system.

### Step 1: Create the skill directory

```bash
mkdir -p ~/.claude/skills/build-ship-grow/
```

### Step 2: Copy the skill file

```bash
cp SKILL.md ~/.claude/skills/build-ship-grow/SKILL.md
```

That's it. No packages, no API keys, no build step.

### Step 3: Verify

Open Claude Code and type one of the trigger phrases (see below). Claude will pick up the skill automatically.

## Trigger Phrases

Any of these will activate the skill:

| Phrase | What it does |
|--------|-------------|
| "Help me create a content strategy for my product launch" | Full Build->Ship->Grow strategy |
| "Build a growth plan to acquire my first 1000 users" | 90-day growth plan with KPIs |
| "Generate a launch checklist for shipping my side project" | Launch-day checklist with owners and timing |
| "Plan a content calendar focused on audience building" | 4-week content calendar with channels |
| "Create a distribution strategy for my new feature release" | Multi-channel distribution plan |

You can also use the keywords: **content strategy**, **growth plan**, **launch checklist**, **ship product**, **audience building**.

## First 60 Seconds

**Input** (type this in Claude Code):

```
Help me create a content strategy for SkillForge, a tool that helps
indie hackers ship Claude Code skills in minutes. We're about to launch.
Target audience: AI-tool builders. Main pain point: creating polished
skills takes too long.
```

**Output** (Claude produces all of this):

```
## Content Pillars
Pillar                                              | Format                 | Frequency
----------------------------------------------------+------------------------+-----------
How SkillForge solves creating polished skills...   | Tutorial / walkthrough | Weekly
Building in public updates                          | Dev log / thread       | 2x per week
Industry trends for indie hackers                   | Curated roundup        | Weekly

## 4-Week Content Calendar
### Week 1 (starts 2026-05-23)
  Theme: Introduce SkillForge -- what problem it solves
  Channels: Blog, Twitter/X
    - 1 blog post
    - 3 social posts repurposed from blog
    - 1 newsletter issue
...

## Launch Checklist
  [ ] Finalize landing page copy and CTA  (Marketing, T-7 days)
  [ ] Write launch announcement blog post  (Content, T-5 days)
  [ ] Draft Twitter/X launch thread  (Content, T-3 days)
  ...

## 90-Day Growth Plan
Objective: Acquire first 1,000 users for SkillForge
  Phase 1 (Week 1-2): Foundation -- 200 signups target
  Phase 2 (Week 3-6): Amplify -- 500 signups, 3% referral rate
  Phase 3 (Week 7-12): Scale -- 1,000 signups, <$5 CAC

## Ready-to-Post Social Copy
  1/ I just shipped SkillForge -- Ship Claude Code skills in minutes...
  2/ The problem: creating polished Claude Code skills takes too long.
  ...

## SEO Blog Outline
  Title: How to Solve Creating Polished Claude Code Skills Takes Too Long
  Target keyword: creating-polished-claude-code-skills-takes-too-long
  ...
```

## Running the Standalone Demo

The repo also includes a Python demo that generates the same outputs offline:

```bash
# No dependencies needed (stdlib only)
bash run.sh

# Or run directly with custom inputs:
python3 content_strategy.py --name "MyApp" --audience "developers" --stage build

# JSON output for programmatic use:
python3 content_strategy.py --json
```

## Customizing the Skill

Edit `~/.claude/skills/build-ship-grow/SKILL.md` to:

- Add your own content pillar templates
- Change default channels (e.g., add TikTok, YouTube)
- Adjust the growth plan timeline
- Add industry-specific launch tactics
