# How to Use

## Install

```bash
git clone <this-repo>
cd company_execution_layer
# No dependencies — Python 3.8+ stdlib only
```

## Quick Demo

```bash
bash run.sh
```

This scaffolds a full company brain at `demo_company_brain/`, validates it, runs skills, and adds a custom skill — all with visible output.

## CLI Commands

```bash
# Scaffold a new company brain
python3 execution_layer.py scaffold my-company

# List available skills
python3 execution_layer.py list my-company

# Inspect a specific skill
python3 execution_layer.py inspect my-company content-creation

# Validate all references (context files exist, SKILL.md present, etc.)
python3 execution_layer.py validate my-company

# Dry-run a skill (shows steps + context without producing output)
python3 execution_layer.py run my-company content-creation --dry-run

# Execute a skill (creates output file)
python3 execution_layer.py run my-company weekly-report

# Add a new custom skill
python3 execution_layer.py add-skill my-company "seo-audit" "Audit a page for SEO issues using brand and product context."
```

## Using as a Claude Code Skill

This is designed to be used as a **Claude Code skill**. Drop the SKILL.md into your skills directory:

```bash
mkdir -p ~/.claude/skills/company_execution_layer
cp SKILL.md ~/.claude/skills/company_execution_layer/SKILL.md
```

**Trigger phrases** (type these in Claude Code):
- "set up execution layer"
- "create skills marketplace"
- "wire skills to company brain"
- "build company playbook"
- "turn our docs into runnable skills"

Claude Code will read the SKILL.md and walk you through scaffolding your own execution layer.

## Using the Generated Structure with Claude Code

After scaffolding, the generated `CLAUDE.md` at the root of your company brain becomes your Claude Code config. Open a Claude Code session in that directory and Claude will:

1. See all available skills via the `CLAUDE.md` registry
2. Read live context from `context/` when running any skill
3. Output finished work to `output/` with dated filenames

## First 60 Seconds

```
$ bash run.sh

============================================================
  Company Execution Layer — Full Demo
============================================================

Step 1: Scaffold Company Brain
  Created 4 skills + 4 context files

Step 2: Skills Marketplace
  4 skills available:
    /client-onboarding        6 steps | 3 context refs
    /content-creation         5 steps | 2 context refs
    /proposal-generator       5 steps | 2 context refs
    /weekly-report            5 steps | 1 context refs

Step 3: Validate Execution Layer
  Valid: YES
  4 skills, 4 context files, 0 broken refs

Step 4: Dry-Run 'content-creation' Skill
  Context loaded:
    context/brand/voice-and-tone.md — 623 bytes
    context/products/product-specs.md — 512 bytes

Step 5: Execute 'weekly-report' Skill
  Output: demo_company_brain/output/weekly-report/weekly-report_2026-05-15.md

Step 6: Add Custom Skill 'competitor-analysis'
  Registered in CLAUDE.md: True

DEMO COMPLETE
```

## Customizing for Your Company

1. **Replace context files** — swap `context/brand/voice-and-tone.md` etc. with your real docs
2. **Edit skills** — modify `skills/*/SKILL.md` to match your actual SOPs
3. **Add skills** — use `python3 execution_layer.py add-skill` or create `skills/<name>/SKILL.md` manually
4. **CLAUDE.md auto-updates** — the tool regenerates `CLAUDE.md` when you add skills
