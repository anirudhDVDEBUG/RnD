# Technical Details

## What it does

This tool parses a structured JSON representation of the GPT-5.5 Instant System Card and produces a multi-section safety analysis report. It covers the Preparedness Framework risk ratings (CBRN, cybersecurity, persuasion, model autonomy), safety and capability benchmark comparisons across model generations (GPT-4o, GPT-5, GPT-5.5 Instant), red teaming findings, deployment mitigations, known limitations, and an executive summary with builder-oriented takeaways.

The analyzer is designed as a reference tool for teams evaluating whether to adopt GPT-5.5 Instant in production, or for anyone tracking OpenAI's safety evaluation methodology across model releases.

## Architecture

```
system_card_data.json   <-- Structured system card data (source of truth)
        |
   analyzer.py          <-- Single-file Python analyzer (stdlib only)
        |
   Terminal output      <-- Color-coded, sectioned safety report
```

**Key files:**
- `analyzer.py` -- Main analyzer (~200 lines). Loads JSON, runs analysis functions for each section, produces formatted terminal output.
- `system_card_data.json` -- Structured representation of the system card. Schema covers: overview, preparedness framework ratings, safety benchmarks, capability benchmarks, red teaming, deployment mitigations, and limitations.
- `SKILL.md` -- Claude Code skill definition with trigger phrases and usage guidance.

**Data flow:** JSON file -> Python dict -> section-by-section analysis functions -> colored terminal output. No network calls, no API keys, no external dependencies.

**Dependencies:** Python 3.10+ standard library only (json, sys, pathlib).

## Limitations

- **Mock data**: The included `system_card_data.json` contains representative data based on the system card structure. Official numbers should be verified against the published card at https://openai.com/index/gpt-5-5-instant-system-card.
- **Static analysis**: This is a structured data parser, not an LLM-powered summarizer. It doesn't interpret free-text sections of the system card.
- **No auto-fetch**: Does not scrape or auto-update from OpenAI's website. Data must be manually updated in the JSON file.
- **Single model**: Designed for GPT-5.5 Instant specifically. Analyzing other system cards requires adapting the JSON schema.

## Why it matters for Claude-driven products

- **Agent factories**: Teams building multi-model agent systems need to compare safety profiles across providers. This tool provides a structured framework for evaluating competitor model safety, helping decide which models to route which tasks to.
- **Lead-gen / marketing**: Understanding frontier model safety claims helps position Claude's safety advantages in competitive contexts. The benchmark comparison format makes it easy to create comparison content.
- **Voice AI / customer-facing**: Any production deployment needs safety-rated models. This analysis helps teams evaluate whether GPT-5.5 Instant meets their safety bar, or whether Claude's safety properties are a better fit.
- **Ad creatives**: Content generation at scale requires models with strong toxicity and bias controls. The safety benchmark section directly addresses these concerns with quantified comparisons.
