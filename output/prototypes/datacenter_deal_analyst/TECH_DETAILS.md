# Technical Details

## What It Does

The Data Center Deal Analyst is a structured risk-assessment framework for evaluating compute infrastructure deals. It takes deal parameters (parties, location, capacity, power source) and contextual intelligence (permit history, community sentiment, regulatory status) and produces a multi-axis risk report with an actionable recommendation.

The skill was created in response to reporting on Anthropic's deal with xAI's Colossus data center in Memphis, TN — a facility that operated gas turbines under temporary construction permits, bypassing Clean Air Act emission controls, while causing documented air quality problems in a low-income neighborhood. The analysis framework captures the specific failure modes exposed by that deal: environmental shortcuts disguised as temporary measures, regulatory gaps exploited under compute scarcity pressure, and the reputational cost of associating a "safety-first" brand with a facility that harmed a vulnerable community.

## Architecture

```
SKILL.md                  Claude Code skill definition (trigger + instructions)
analyzer.py               Core analysis engine
  DealParameters          Dataclass: parties, location, capacity, power source
  EnvironmentalRisk       Risk assessment: emissions, permits, health impacts
  RegulatoryRisk          Violations, exemptions, pending enforcement
  PoliticalRisk           Sentiment, media, controversial associations
  BusinessTradeoffs       Constraint severity, alternatives, lock-in
  DealAnalysis            Composite report with recommendation logic
  analyze_deal()          Main entry point: params + context -> analysis
  to_json()               JSON serialization for programmatic use
demo.py                   Demo script with two mock deals
run.sh                    One-command runner
```

### Data Flow

1. User describes a deal (natural language to Claude, or structured `DealParameters` to Python)
2. Contextual intelligence is gathered (by Claude via the skill instructions, or provided as a dict)
3. `analyze_deal()` constructs risk objects for each axis
4. Overall risk = max of environmental, regulatory, political risk levels
5. Recommendation is derived: CRITICAL -> Seek alternatives, HIGH -> Proceed with mitigations, else Proceed
6. Output is a formatted report (text) or JSON

### Dependencies

- Python 3.10+ (for `list[str]` type syntax in dataclasses)
- No external packages — stdlib only (`dataclasses`, `json`, `enum`)

## Limitations

- **No live data**: The demo uses mock data. In production, Claude would research the deal using web search, news, and regulatory databases via the skill instructions.
- **No quantitative modeling**: Does not model financial NPV, carbon tonnage, or health outcome projections. Risk levels are qualitative (LOW/MEDIUM/HIGH/CRITICAL).
- **US-centric regulatory knowledge**: The skill references Clean Air Act, EPA EJScreen, and US state-level agencies. International deals would need adapted regulatory frameworks.
- **No real-time permit lookups**: Claude cannot query EPA ECHO or state permit databases directly (no MCP server for that yet).
- **Recommendation logic is simple**: Max-of-risks heuristic. A production version could weight axes differently based on company risk tolerance.

## Why It Matters for Claude-Driven Products

**Lead-gen / marketing agencies**: If you're selling to data center operators, cloud providers, or AI companies, this skill demonstrates how Claude can automate due-diligence reports that would otherwise require a consultant. A "deal risk score" could be a lead-gen magnet.

**Agent factories**: This is a template for any structured-assessment skill — swap "data center deal" for "vendor contract", "M&A target", or "regulatory filing" and the same multi-axis risk framework applies. The pattern of `parameters + context -> structured report with recommendation` is reusable.

**Ad creatives / content**: The xAI/Anthropic deal is a hot topic. A tool that lets people run their own analysis generates shareable outputs — each report is a content piece.

**Voice AI**: The structured output (especially the side-by-side comparison and recommendation) is well-suited for voice summarization: "The Colossus deal scores CRITICAL environmental risk. I recommend seeking alternatives because..."

## References

- [Notes on the xAI/Anthropic data center deal — Simon Willison](https://simonwillison.net/2026/May/7/xai-anthropic/#atom-everything)
