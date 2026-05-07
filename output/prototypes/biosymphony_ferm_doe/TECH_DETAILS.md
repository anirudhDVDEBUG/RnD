# Technical Details — BioSymphony Fermentation DoE

## What it does

BioSymphony Fermentation DoE is an agentic AI harness for pre-experiment Design-of-Experiments planning in fermentation and biomanufacturing. It generates statistically rigorous experimental matrices (Central Composite, Box-Behnken, full/fractional factorial) and passes every proposed run through biosafety-aware gating before the experiment reaches the bench. For scale-up or scale-down studies, it automatically translates operating parameters between bioreactor volumes using standard chemical engineering correlations (constant kLa, constant P/V, constant tip speed).

The core value proposition is that a scientist describes their factors, ranges, and safety constraints in natural language, and the system produces a ready-to-execute experiment plan — with dangerous conditions flagged or blocked — in seconds rather than hours of manual spreadsheet work.

## Architecture

### Key files (this prototype)

| File | Role |
|------|------|
| `doe_engine.py` | All logic: DoE generators, biosafety gate, scale-up bridge, CLI demo |
| `run.sh` | Entry point — runs the demo end-to-end |
| `requirements.txt` | Dependency declaration (stdlib-only for demo) |

### Data flow

```
User defines factors + safety limits
        |
        v
DoE Generator (CCD / BB / FF)
        |
        v
Raw experiment matrix (N runs x K factors)
        |
        v
Biosafety Gate
  - Checks each run against safety_min / safety_max per factor
  - Flags: "warning" (within 5% of limit) or "block" (beyond 5%)
  - Blocked runs removed from plan
        |
        v
[Optional] Scale-Up Bridge
  - Translates volumetric params (feed rate) by volume ratio
  - Translates agitation (rpm) by engineering correlation
  - Strategies: constant_kLa, constant_PV, constant_tip_speed
        |
        v
Final DoE plan (JSON / table) -> LIMS / ELN / bioreactor controller
```

### DoE types implemented

- **Full Factorial**: All combinations of coded levels (-1, 0, +1). Grows as `levels^k` — feasible for k <= 4.
- **Central Composite Design (CCD)**: 2^k factorial + 2k axial (star) points + center replicates. Supports rotatable and face-centered alpha. Good for response surface modeling with 3-6 factors.
- **Box-Behnken**: Pairs of factors at extremes, rest at center. Requires k >= 3. Fewer runs than CCD, avoids extreme corners.

### Scale-up correlations

The bridging module uses these relationships:

- **Constant tip speed**: `N_target = N_source * (D_source / D_target)` — preserves shear at impeller tip.
- **Constant P/V**: Power per unit volume held constant — `N_target` derived from `N^3 * D^5 / V = const`.
- **Constant kLa**: Oxygen transfer coefficient held constant — combines P/V and superficial gas velocity correlations.

### Dependencies

- **This prototype**: Python 3.8+ stdlib only (itertools, math, json, dataclasses).
- **Full BioSymphony repo**: pyDOE2 (design generation), numpy, pandas, scipy.

## Limitations

- **No actual model fitting**: This is a DoE *planning* tool, not an analysis tool. It generates the experiment matrix but does not fit response surface models to results.
- **Simplified scale-up**: The bridging correlations are textbook approximations. Real scale-up requires vessel-specific characterization (e.g., measured kLa curves).
- **No LIMS/ELN integration**: The output is JSON/tabular. Actual integration with lab systems would need connectors (REST APIs, CSV export to specific formats).
- **No randomization/blocking optimization**: Run order is sequential. A production system would apply proper randomization and blocking for time-varying nuisance factors.
- **Biosafety limits are user-defined**: The system checks against limits you provide — it does not have an internal database of organism-specific safety constraints.

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Demonstrates a domain-specific agentic loop: define constraints -> generate plan -> gate for safety -> bridge scales. This pattern (constraint-aware plan generation with safety checks) generalizes to any regulated domain. |
| **Lead-gen / marketing for biotech** | A biotech company offering "AI-powered DoE planning" could use this as the backend for a lead-gen tool — prospects enter their factors, get a sample DoE plan, then convert to paid service for full analysis. |
| **Voice AI for lab scientists** | Scientists at the bench could dictate factor ranges and constraints via voice, and a Claude-powered agent could generate and read back the DoE plan — hands-free experiment planning. |
| **Regulated-industry patterns** | The biosafety gating pattern (pre-check all proposed actions against hard safety constraints, block violations) is directly applicable to any Claude agent operating in regulated environments (pharma, finance, manufacturing). |
