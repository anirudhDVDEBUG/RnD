# How To Use

## As a standalone analysis tool

### Install

```bash
git clone <this-repo>
cd hbm_memory_shortage_analysis
# No pip install needed — stdlib only (Python 3.8+)
```

### Run

```bash
# Human-readable tables
python3 hbm_analysis.py

# Machine-readable JSON
python3 hbm_analysis.py --json

# Or use the wrapper
bash run.sh
```

### First 60 seconds

**Input:** Just run it — no arguments needed for the default analysis.

**Output:**
```
======== HBM MEMORY SHORTAGE ANALYSIS ========

  By end of 2026, HBM is projected to consume ~20% of memory wafer capacity
  (up from ~2% in 2022). Due to HBM's 3.2x wafer intensity, this effectively
  reduces consumer memory supply by ~76%, hitting sub-$100 smartphones in
  Africa and South Asia hardest.

======== MANUFACTURER WAFER ALLOCATION (Current) ========
  Manufacturer   Capacity    HBM    DDR   LPDDR   Consumer
  Samsung             550  18.0%  42.0%   40.0%      82.0%
  SK Hynix            420  25.0%  38.0%   37.0%      75.0%
  Micron              380  15.0%  45.0%   40.0%      85.0%
  ...
```

For JSON, pipe through `jq` for specific fields:
```bash
python3 hbm_analysis.py --json | jq '.consumer_segment_impacts[] | {segment, retail_price_increase_usd}'
```

---

## As a Claude Code Skill

### Install the skill

```bash
mkdir -p ~/.claude/skills/hbm_memory_shortage_analysis
cp SKILL.md ~/.claude/skills/hbm_memory_shortage_analysis/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code to activate the skill:

- "Why are smartphones getting more expensive?"
- "Explain the HBM memory shortage"
- "How is AI GPU demand affecting memory wafer allocation?"
- "What's happening with DDR and LPDDR supply due to HBM?"
- "Analyze the impact of memory constraints on sub-$100 smartphones"
- "memory shortage"
- "HBM allocation"
- "consumer electronics repricing"
- "wafer capacity constraints"
- "smartphone affordability"

### What happens

Claude will use the skill's structured knowledge to walk through the supply-side economics: the 3-manufacturer oligopoly, the wafer capacity tradeoff, HBM's disproportionate silicon consumption, and the downstream pricing effects on consumer devices — with specific focus on equity implications in emerging markets.

---

## As a data source for other tools

Import directly in Python:

```python
from hbm_analysis import run_full_analysis

result = run_full_analysis()
# result["supply_trajectory"] — list of supply index by year
# result["consumer_segment_impacts"] — per-segment price effects
# result["equity_implications"] — digital divide analysis
```
