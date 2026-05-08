# How to Use

## This is a Claude Code Skill

The `datacenter_deal_analyst` is a **Claude Code skill** — a markdown instruction file that teaches Claude how to analyze data center deals when triggered by natural language.

## Installation

### 1. Copy the skill folder

```bash
mkdir -p ~/.claude/skills/datacenter_deal_analyst
cp SKILL.md ~/.claude/skills/datacenter_deal_analyst/SKILL.md
```

### 2. Verify it's picked up

Open Claude Code in any project. The skill auto-loads from `~/.claude/skills/`.

### 3. (Optional) Run the standalone demo

```bash
git clone <this-repo>
cd datacenter_deal_analyst
bash run.sh
```

No API keys, no external dependencies — Python 3.10+ stdlib only.

## Trigger Phrases

Say any of these (or similar) to Claude Code to activate the skill:

- "Evaluate this data center partnership for risks"
- "What are the environmental concerns with this compute facility?"
- "Analyze the trade-offs of this infrastructure deal"
- "Assess political and regulatory risk for a data center arrangement"
- "Compare colocation options considering ESG factors"
- Any mention of: data center deal, compute infrastructure partnership, colocation agreement, environmental impact of AI infrastructure

## First 60 Seconds

**Input** (paste into Claude Code):

```
Evaluate this data center deal:
- Anthropic leasing 150 MW from xAI's Colossus facility in Memphis, TN
- Powered by gas turbines operating under temporary construction permits
- Local community has reported air quality complaints
- 100,000 GPUs, 2-year term
```

**Output** (Claude produces a structured report):

```
## Deal Summary
  Parties: Anthropic leasing capacity from xAI (Colossus facility)
  Facility: Colossus Data Center, Memphis, Tennessee
  Capacity: 150 MW, 100,000 GPUs
  Power source: Natural gas turbines (bypass generators) + grid

## Environmental Risk  [CRITICAL]
  Power generation: Gas-fired turbine generators classified as
    'temporary', bypassing standard emission controls
  Emissions profile: High NOx and particulate matter
  Permit status: Operated under temporary 'construction' permits
  Compliance issues:
    - Facility operated for months under temporary permits
    - Shelby County Health Department issued violation notices
  Health impacts:
    - Residents reported increased respiratory symptoms
    - Environmental justice concerns — low-income area

## Regulatory / Compliance Status  [HIGH]
  ...

## Political / Reputational Risk  [HIGH]
  ...

## Business Trade-offs
  Compute constraint: HIGH — GPU scarcity is acute
  Alternatives:
    - AWS Trainium — available but lower performance
    - Google TPU v5p — limited allocation
    - Build own facility — 18-24 month timeline

## Recommendation: Seek alternatives
  The facility's documented air quality violations create critical
  reputational and regulatory risk for a safety-focused AI lab.
```

## Using the Python Analyzer Directly

You can also import the analyzer in your own scripts:

```python
from analyzer import DealParameters, analyze_deal

deal = DealParameters(
    party_a="MyCompany",
    party_b="DataCenterCorp",
    facility_name="Facility X",
    location="Austin, TX",
    capacity_mw=50,
    power_source="grid (ERCOT)",
)

context = {
    "env_risk_level": "MEDIUM",
    "power_gen": "ERCOT grid mix (40% gas, 30% wind, 20% solar, 10% nuclear)",
    "emissions": "Moderate — grid-dependent",
    "permit_status": "All permits current",
    # ... fill in other fields
}

analysis = analyze_deal(deal, context)
print(analysis.render_report())
```
