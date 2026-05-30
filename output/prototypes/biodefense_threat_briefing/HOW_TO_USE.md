# How to Use

## Install

```bash
git clone <this-repo>
cd biodefense_threat_briefing
# No pip install needed — Python 3.8+ stdlib only
```

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/biodefense_threat_briefing
cp SKILL.md ~/.claude/skills/biodefense_threat_briefing/SKILL.md
```

### Trigger phrases

Say any of these in Claude Code to activate the skill:

- "Create a biodefense threat briefing"
- "Generate a biosurveillance intelligence report"
- "Summarize pandemic preparedness posture for our region"
- "Assess public health readiness for emerging biological threats"
- "Draft a biosecurity risk analysis document"

Claude will ask you for scope, audience, focus, and time horizon, then produce a structured Markdown briefing.

## CLI usage (standalone)

```bash
# Default: national-scope briefing to stdout
python3 generate_briefing.py

# Custom scope + audience, save to file
python3 generate_briefing.py \
  --scope "Regional (Pacific Northwest)" \
  --audience "State epidemiologists" \
  --output briefing.md

# JSON output (for downstream pipelines)
python3 generate_briefing.py --format json > briefing.json
```

## First 60 seconds

```
$ bash run.sh

=== Biodefense Threat Briefing Generator ===

# Biodefense Threat Briefing

**Date:** 2026-05-30
**Classification:** UNCLASSIFIED
**Scope:** National (United States)
**Prepared for:** Senior public health leadership

---

## Executive Summary

The biological threat landscape shows elevated risk driven by sustained
H5N1 zoonotic transmission, expanding antifungal resistance, and persistent
gaps in global biosurveillance coverage. ...

## Current Threat Landscape

### Natural Biological Threats

- **H5N1 Avian Influenza** (trend: increasing, confidence: high): ...
- **Mpox (Clade Ib)** (trend: stable, confidence: moderate): ...
- **Candida auris** (trend: increasing, confidence: high): ...

### Deliberate / Engineered Threats
...

## Preparedness Assessment

| Domain | Status | Key Gaps | Priority |
|--------|--------|----------|----------|
| Medical countermeasures | Partial | ... | **High** |
| Supply chain resilience | At Risk | ... | **Critical** |
...

## Recommended Actions

1. **Immediate (0-30 days)** ...
2. **Short-term (30-90 days)** ...
3. **Long-term (6-18 months)** ...
```

Output is standard Markdown — pipe to `pandoc` for PDF, paste into a slide deck, or feed into a downstream LLM chain.
