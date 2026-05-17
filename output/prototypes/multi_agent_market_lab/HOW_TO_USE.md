# How to Use — Multi-Agent Market Lab

## Install

```bash
# No external deps — Python 3.10+ stdlib only
git clone https://github.com/johnicassere/lab-rat-race.git
cd lab-rat-race
```

Or use this prototype directly:

```bash
cd output/prototypes/multi_agent_market_lab
bash run.sh
```

## As a Claude Skill

Drop into your skills directory:

```bash
cp -r skills/multi_agent_market_lab ~/.claude/skills/multi_agent_market_lab
```

**Trigger phrases:**
- "Set up a multi-agent research pipeline for market analysis"
- "Run autonomous market experiments with multiple agents"
- "Manage research experiments and track agent allocations"
- "Build an auto-research system with experiment tracking"
- "Coordinate AI agents for competitive market intelligence"

## First 60 Seconds

**Input:** `bash run.sh`

**Output:**
```
============================================================
  MULTI-AGENT MARKET LAB — Demo Run
============================================================

Initializing orchestrator with 4 agents...

--- Agent Fleet ---
  [30%] voice_ai_scout            | segment: voice_ai
  [25%] ad_creative_analyst       | segment: ad_creatives
  [25%] agent_factory_watcher     | segment: agent_factories
  [20%] leadgen_researcher        | segment: lead_generation

============================================================
  EXPERIMENT: Market Signal Discovery
============================================================
  Hypothesis: Multi-agent parallel research discovers 20+ signals in 5 iterations
  ...

  [PASS] min_signals: target=20, actual=34
  [PASS] min_confidence: target=0.5, actual=0.612

============================================================
  DYNAMIC REBALANCING
============================================================
  + voice_ai_scout           : 30% -> 42% (score-based)
  - ad_creative_analyst      : 25% -> 18% (score-based)
  ...
```

## Programmatic Usage

```python
from market_lab import Orchestrator

config = {
    "agents": [
        {"name": "my_agent", "segment": "fintech", "budget": 0.5},
        {"name": "other_agent", "segment": "healthtech", "budget": 0.5},
    ],
    "allocation_cap": 0.7,
    "allocation_floor": 0.1,
}

orch = Orchestrator(config)
results = orch.run_iteration()
orch.rebalance()
print(orch.status())
```

## Configuration Options

| Key | Type | Description |
|-----|------|-------------|
| `agents[].name` | str | Unique agent identifier |
| `agents[].segment` | str | Market segment to research |
| `agents[].budget` | float | Initial allocation (0.0-1.0) |
| `agents[].capabilities` | list | Agent research capabilities |
| `allocation_cap` | float | Max budget any agent can receive |
| `allocation_floor` | float | Min budget to keep agent alive |
