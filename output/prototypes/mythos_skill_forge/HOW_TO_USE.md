# How to Use — Mythos Skill Forge

## Install

```bash
git clone https://github.com/rayhayqal/Mythos-Claude-Skill-Forge.git
cd Mythos-Claude-Skill-Forge
# No dependencies — Python 3.10+ stdlib only
```

Or use this prototype directly:

```bash
cd mythos_skill_forge
python3 skill_forge.py --help
```

## This is a Claude Code SKILL

### Where to drop the SKILL.md

Copy the skill folder to make it discoverable by Claude Code:

```bash
# Global (all projects):
cp -r skills/my_skill ~/.claude/skills/my_skill/

# Project-scoped:
cp -r skills/my_skill .claude/skills/my_skill/
```

Claude Code automatically discovers and loads skills from these directories.

### Trigger phrases

Say any of these to Claude Code to activate the skill:

- "create a new skill"
- "scaffold a claude skill"
- "build an agent plugin"
- "generate SKILL.md"
- "forge a skill"
- "skill forge"
- "mythos skill"

## CLI Usage

### Forge from a preset

```bash
python3 skill_forge.py forge --preset code_review --output ./skills
python3 skill_forge.py forge --preset deploy_checklist --output ./skills
python3 skill_forge.py forge --preset api_doc_gen --output ./skills
```

### Forge a custom skill

```bash
python3 skill_forge.py forge \
  --name lead_scorer \
  --title "Lead Scorer" \
  --desc "Scores inbound leads based on engagement and ICP fit." \
  --triggers "score these leads,rank my leads,evaluate lead quality" \
  --steps "Ingest lead data,Score on engagement,Rank by composite score,Generate outreach list" \
  --hooks --templates \
  --output ./skills
```

### Audit an existing skill

```bash
python3 skill_forge.py audit ./skills/code_review_agent
```

### List presets

```bash
python3 skill_forge.py list-presets
```

### Dry run (preview without writing)

```bash
python3 skill_forge.py forge --preset code_review --dry-run
```

## First 60 Seconds

```
$ python3 skill_forge.py forge --preset code_review --output ./skills

  Forging skill: code_review_agent
  Output: skills/code_review_agent

  Generated skill structure:
  ========================================
    code_review_agent
      CLAUDE.md
      SKILL.md
      hooks
        post_run.sh
        pre_run.sh
      templates
        default.md

  Wrote 5 files.

  ============================================================
    Skill Audit: skills/code_review_agent
    Score: 5/5
  ============================================================

    PASS:
      [+] YAML frontmatter has name and description
      [+] Triggers defined in frontmatter
      [+] 'When to use' has 4 trigger phrases
      [+] 'How to use' section present
      [+] No placeholder text detected

$ cp -r skills/code_review_agent ~/.claude/skills/
# Done — Claude Code will now respond to "review this code"
```

**Input:** A preset name or custom skill spec (name + description + triggers + steps).
**Output:** A complete, audit-passing skill directory ready for Claude Code.
