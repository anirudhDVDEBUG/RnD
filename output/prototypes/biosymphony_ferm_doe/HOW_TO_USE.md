# How to Use — BioSymphony Fermentation DoE

## Install (this prototype)

```bash
# No external dependencies — pure Python 3.8+ stdlib
git clone <this-repo>
cd biosymphony_ferm_doe
bash run.sh
```

## Install (full BioSymphony repo)

```bash
git clone https://github.com/BioSymphony/biosymphony-ferm-doe.git
cd biosymphony-ferm-doe
pip install -e .
```

Dependencies for the full repo: `pyDOE2`, `numpy`, `pandas`, `scipy`.

## Claude Code Skill setup

This is a **Claude Code Skill**. To install it:

1. Copy the skill folder to your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/biosymphony_ferm_doe
   cp SKILL.md ~/.claude/skills/biosymphony_ferm_doe/SKILL.md
   ```

2. The skill activates on these trigger phrases:
   - "Plan a DoE for my fed-batch fermentation experiment"
   - "Generate a design of experiments matrix for bioreactor scale-up"
   - "Run biosafety readiness gating before starting my bioprocess experiment"
   - "Bridge my bench-scale DoE to pilot-scale biomanufacturing"
   - "Create a DoE for optimizing kLa in perfusion cell culture"

3. Once triggered, Claude will walk you through:
   - Defining factors (temperature, pH, DO, feed rate, agitation, etc.) with ranges
   - Selecting a DoE type (full factorial, CCD, Box-Behnken)
   - Running biosafety gating against your organism/facility limits
   - Optionally bridging the plan to a different bioreactor scale

## First 60 seconds

```bash
$ bash run.sh

══════════════════════════════════════════════════════════════════════
  BioSymphony Fermentation DoE Demo
══════════════════════════════════════════════════════════════════════
  Scenario: Optimize fed-batch CHO cell culture for mAb titer
  Organism: CHO-K1 (BSL-1)

  Factors (5):
    - temperature_C: 33.0-37.0 degC  [safety: 30.0-39.0 degC]
    - pH: 6.8-7.4                     [safety: 6.5-7.6]
    - DO_pct: 30.0-60.0 %            [safety: 20.0-80.0 %]
    - feed_rate_mL_h: 5.0-15.0 mL/h  [safety: 1.0-25.0 mL/h]
    - agitation_rpm: 100-250 rpm      [safety: 50-400 rpm]

══════════════════════════════════════════════════════════════════════
  Step 1: Central Composite Design (CCD)
══════════════════════════════════════════════════════════════════════
  Generated 47 runs (2^5 factorial + 10 axial + 5 center)
  Run    Design            temperature_C   pH   DO_pct   ...
  ---    ------            -------------  ----  ------
    1    CCD-factorial           33.00    6.80   30.00   ...
    2    CCD-factorial           37.00    6.80   30.00   ...
  ...

══════════════════════════════════════════════════════════════════════
  Step 2: Biosafety Readiness Gating
══════════════════════════════════════════════════════════════════════
  [BLOCK] Run 37: DO_pct = 12.74 (below_min limit 20.0)
  [ WARN] Run 38: temperature_C = 39.24 (above_max limit 39.0)
  ...

══════════════════════════════════════════════════════════════════════
  Step 3: Scale-Up Bridging (Bench -> Pilot)
══════════════════════════════════════════════════════════════════════
  Source: Bench (2L) | Target: Pilot (200L)
  Strategy: constant kLa | Volume ratio: 100x
```

**Input**: Factor definitions with ranges and safety bounds.
**Output**: Numbered DoE matrix with safety status and scaled parameters, plus JSON export.

## Customization

Edit `doe_engine.py` to change:
- **Factors**: Modify the `factors` list in `run_demo()` — add/remove factors, change ranges and safety limits
- **DoE type**: Call `full_factorial()`, `central_composite()`, or `box_behnken()` directly
- **Scale configs**: Change `ScaleConfig` parameters for your bench/pilot/manufacturing vessels
- **Bridging strategy**: Choose `"constant_kLa"`, `"constant_PV"`, or `"constant_tip_speed"`
