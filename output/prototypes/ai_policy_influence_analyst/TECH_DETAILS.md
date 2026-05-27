# Technical Details

## What It Does

The AI Policy Influence Analyst is a structured reasoning framework (implemented as a Claude Code skill) that decomposes policy documents into their constituent vendor interests. It applies a four-category taxonomy of influence strategies — Limitation Laundering, Safety Capture, Standards Setting, and Institutional Blessing — to map how AI companies convert technical constraints into ethical imperatives and regulatory advantages.

The standalone Python implementation (`analyst.py`) demonstrates the analysis pipeline using rule-based heuristics and keyword extraction against a corpus of mock policy documents. In production (as a Claude skill), the LLM itself performs the reasoning using the structured framework.

## Architecture

```
┌─────────────────────────────────────────────┐
│  SKILL.md (Claude Code skill definition)     │
│  - Trigger conditions                        │
│  - Analysis framework (5-step process)       │
│  - Strategy taxonomy                         │
│  - Output template                           │
└─────────────────┬───────────────────────────┘
                  │ (activates Claude reasoning)
                  ▼
┌─────────────────────────────────────────────┐
│  analyst.py (standalone demo)                │
│  - PolicyDocument dataclass                  │
│  - InfluenceAnalyzer class                   │
│  - Strategy classification engine            │
│  - Vendor-interest mapper                    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  mock_data.py                                │
│  - Sample policy documents                   │
│  - Known vendor positions database           │
│  - Influence channel registry                │
└─────────────────────────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Claude Code skill definition with taxonomy and process |
| `analyst.py` | Demo implementation of the analysis pipeline |
| `mock_data.py` | Sample policy docs and vendor interest mappings |
| `run.sh` | End-to-end demo runner |

### Data Flow

1. Input: policy document text + metadata (author, date, institutional context)
2. Keyword extraction: identify technical terms that map to vendor architectures
3. Vendor matching: cross-reference principles against known company positions
4. Strategy classification: categorize the influence technique used
5. Output: structured brief with mappings, channels, and effectiveness score

### Dependencies

- Python 3.8+
- `dataclasses` (stdlib)
- `textwrap` (stdlib)
- `json` (stdlib)

No external packages required for the demo. No API keys needed.

## Limitations

- **No real-time data:** The demo uses mock policy documents. Real analysis requires feeding actual documents to Claude via the skill.
- **No lobbying database:** Does not connect to OpenSecrets, FARA filings, or other lobbying registries.
- **Subjective framing:** Influence analysis involves interpretation. The framework provides structure but the conclusions depend on the analyst (human or LLM).
- **US/EU-centric:** The vendor interest mappings assume Western regulatory contexts.
- **No document ingestion:** The skill relies on the user providing or describing the policy document; it cannot fetch URLs autonomously.

## Why This Matters for Claude-Driven Products

| Use Case | Application |
|----------|-------------|
| **Lead-gen** | Identify companies actively lobbying on AI policy — they have budget and urgency |
| **Marketing** | Understand how competitors frame their technical choices as ethical imperatives |
| **Agent factories** | Build policy-monitoring agents that flag vendor influence in new regulations |
| **Ad creatives** | Craft messaging that positions your product's constraints as principled choices (the same technique being analyzed) |
| **Voice AI** | Detect when policy language favors specific modality constraints (text-only vs. multimodal) |

The core insight: understanding how the game is played lets you either play it better or build tools that make the game transparent to others.
