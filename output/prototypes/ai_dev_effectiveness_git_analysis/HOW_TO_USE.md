# How to Use

## Install (30 seconds)

The analyzer is pure Python 3.10+ stdlib -- no pip install required.

```bash
# Option A: use this prototype directly
cd ai_dev_effectiveness_git_analysis/
python3 analyze.py --repo /path/to/repo

# Option B: clone upstream (has Jupyter notebooks + subagent support)
git clone https://github.com/denn-gubsky/ai-dev-effectiveness.git
cd ai-dev-effectiveness
pip install -r requirements.txt
python analyze.py --repo /path/to/repo
```

## Using as a Claude Code Skill

Drop the skill file so Claude Code can invoke it automatically:

```bash
mkdir -p ~/.claude/skills/ai_dev_effectiveness_git_analysis
cp SKILL.md ~/.claude/skills/ai_dev_effectiveness_git_analysis/SKILL.md
```

### Trigger phrases that activate the skill

- "How much of this repo was written with AI assistance?"
- "Measure AI coding productivity on this project"
- "Detect Claude or Copilot commits in git history"
- "Calculate developer productivity multiplier from AI tools"
- "Audit AI-generated code percentage in this repository"

Claude will clone the tool, run it against the target repo, and summarize the results.

## CLI Reference

```
python3 analyze.py [OPTIONS]

--repo PATH       Git repo to analyze (omit for demo mode)
--since DATE      Start date, e.g. 2025-01-01
--author "name"   Filter to one developer
--output text|json Output format (default: text)
--demo            Force demo mode with mock data
```

## First 60 Seconds

```bash
$ bash run.sh

==========================================
  AI Dev Effectiveness Analyzer
==========================================

[1/3] Running demo analysis with mock data...

================================================================
  AI Dev Effectiveness Report
================================================================
  Repository : /demo/acme-saas-platform
  Window     : since 2025-01-01 (demo data)
  Total commits analyzed: 347

  AI-assisted commits : 142 (40.9%)
  Manual commits      : 205 (59.1%)

  AI Tools Detected:
    - Claude Code: 89 commits
    - GitHub Copilot: 41 commits
    - Cursor: 12 commits

  Lines of Code Breakdown:
    AI-assisted insertions : 28,450
    Manual insertions      : 19,200
    AI-assisted deletions  : 8,120
    Manual deletions       : 6,340

  Productivity Multiplier Estimates:
    Top-down (role-based)  : 1.33x
    Bottom-up (LOC-based)  : 2.14x
    Combined estimate      : 1.73x

  Per-Author Breakdown:
    Alice Chen: 124 commits, 78 AI-assisted (63%)
    Bob Martinez: 98 commits, 34 AI-assisted (35%)
    Carol Nguyen: 75 commits, 22 AI-assisted (29%)
    Dave Kim: 50 commits, 8 AI-assisted (16%)

================================================================

[2/3] JSON output (first 30 lines):
  { "repo_path": "/demo/acme-saas-platform", ... }

[3/3] Analyzing current repo...
  (live results from your actual git history)

Done.
```

## Interpreting the Multipliers

| Metric | What it means |
|--------|---------------|
| **Top-down** | If X% of commits are AI-assisted and AI makes devs ~2.5x faster on those commits, overall throughput = `1/(1 - X*(1-1/2.5))` |
| **Bottom-up** | Compares average LOC-per-commit for AI vs manual commits directly |
| **Combined** | Simple average of the two -- use as a ballpark |

Typical range: **1.3x -- 3.5x** for teams actively using AI coding tools.
