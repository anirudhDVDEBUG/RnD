# How to Use

## Install

```bash
pip install matplotlib
```

Or use the provided script:

```bash
bash run.sh
```

This installs dependencies and runs the tracker end-to-end.

## As a Claude Code Skill

### 1. Install the skill

```bash
mkdir -p ~/.claude/skills/revenue_run_rate_tracker
cp SKILL.md ~/.claude/skills/revenue_run_rate_tracker/SKILL.md
```

### 2. Trigger phrases

Say any of these to Claude Code:

- "Plot run-rate revenue over time"
- "Chart revenue growth"
- "Visualize financial milestones"
- "Track revenue announcements"
- "Make a revenue trajectory chart from press releases"

### 3. What happens

Claude reads the skill, generates a Python script with your data points, runs it, and produces a `.png` chart in your working directory.

## As a standalone script

```bash
python3 revenue_tracker.py
```

Edit the `DATA` dictionary at the top of `revenue_tracker.py` to use your own company's data:

```python
DATA = {
    "company": "Your Company",
    "dates": ["2025-06-01", "2025-12-01", "2026-03-01"],
    "revenues_bn": [2.0, 5.0, 8.5],
}
```

## First 60 seconds

```
$ bash run.sh
Installing dependencies...
Generating run-rate revenue chart for Anthropic...
Chart saved to run_rate_revenue.png
Done. Open run_rate_revenue.png to see the result.
```

Output: a `run_rate_revenue.png` file showing Anthropic's run-rate revenue from $9B to $47B across four announced milestones (Dec 2025 - May 2026).
