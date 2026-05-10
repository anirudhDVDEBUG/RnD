# How to Use: Overseas Sales Research Skill

## What this is

This is a **Claude Code Skill** — a SKILL.md file that teaches Claude how to perform structured overseas sales research using the 五看六定 (Five Perspectives, Six Decisions) framework. When installed, Claude responds to natural-language prompts by conducting web research and producing a comprehensive Markdown report.

## Installation (Claude Code Skill)

### 1. Clone the skill

```bash
git clone https://github.com/xxyshawn-creator/claude-skill-overseas-sales-research.git
```

### 2. Copy SKILL.md into your Claude skills directory

```bash
mkdir -p ~/.claude/skills/overseas_sales_research
cp claude-skill-overseas-sales-research/SKILL.md \
   ~/.claude/skills/overseas_sales_research/SKILL.md
```

### 3. Restart Claude Code

The skill is loaded automatically on next session start. No configuration changes to `~/.claude.json` are needed — skills are file-based.

## Trigger phrases

Say any of these to Claude Code and it will activate the skill:

- "Research this overseas company before our sales visit"
- "Do due diligence on a potential international distributor"
- "Generate a competitor analysis report for this foreign market"
- "Help me prepare a 五看六定 report for market entry"
- "Analyze this company as a B2B sales prospect"

## First 60 seconds

```
You:    Research Siemens AG for a distributor evaluation
        in Southeast Asia. Report in English.

Claude: I'll prepare a 五看六定 report for Siemens AG.
        Let me gather information on:
        1. Industry landscape (看行业)
        2. Market segmentation (看市场)
        3. Competitive positioning (看竞争)
        4. Company profile (看客户)
        5. SWOT analysis (看自身)

        [Claude performs web searches, compiles data...]

        ✓ Report saved: overseas_sales_research_siemens_ag_2026-05-10.md

        The report includes:
        - Executive summary
        - 5 research perspectives with data tables
        - 6 strategic recommendations with 30/60/90-day plan
        - Risk assessment matrix
        - Source appendix

        Would you like me to expand any section or adjust
        the format?
```

**Output:** A single Markdown file (`overseas_sales_research_<company>_<date>.md`) containing the full report.

## Running the standalone demo

The demo uses mock data to show the report structure without requiring API keys or web access:

```bash
# No dependencies to install (Python 3.10+ stdlib only)
bash run.sh
```

This generates a sample report for Siemens AG in Southeast Asia and prints a preview to the terminal.

### Custom parameters

```bash
python3 generate_report.py \
  --company "ABB Ltd" \
  --industry "Robotics & Automation" \
  --market "Latin America" \
  --purpose "Competitive Analysis" \
  --lang en
```

| Flag | Default | Description |
|------|---------|-------------|
| `--company` | Siemens AG | Target company name |
| `--industry` | Industrial Automation | Industry / product category |
| `--market` | Southeast Asia | Target region |
| `--purpose` | Distributor Evaluation | Research context |
| `--lang` | zh | Report language: `zh` (bilingual) or `en` |
| `--output` | auto-generated | Custom output file path |

## Report structure

The generated report follows this outline:

```
# Overseas Sales Research Report
## Target / Date / Purpose
### Executive Summary
### 1. 看行业 — Industry View        (market size, trends, regulations)
### 2. 看市场 — Market View          (segments, buyer profiles, cycles)
### 3. 看竞争 — Competition View     (competitor benchmarking table)
### 4. 看客户 — Customer View        (target company profile)
### 5. 看自身 — Self View (SWOT)     (strengths/weaknesses/opportunities/threats)
### 6. Six Decisions
####   6.1 定目标 — Objectives       (revenue targets, KPIs)
####   6.2 定策略 — Strategy         (go-to-market model)
####   6.3 定市场 — Market Focus     (priority sub-segments)
####   6.4 定打法 — Tactics          (pricing, demos, POCs)
####   6.5 定资源 — Resources        (team, budget, timeline)
####   6.6 定节奏 — Cadence          (30/60/90-day milestones)
### Risk Assessment                  (risk matrix with mitigations)
### Appendix & Sources
```
