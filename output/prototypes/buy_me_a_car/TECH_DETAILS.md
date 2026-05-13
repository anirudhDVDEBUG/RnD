# Technical Details

## What It Does

`buy-me-a-car` is a Claude Code skill that gives Claude structured knowledge for the entire used-car-buying pipeline: multi-site listing search, CARFAX/history-report triage, out-the-door (OTD) price calculation with 50-state tax and fee data, dealer outreach message generation, negotiation strategy anchored to KBB/Edmunds/NADA market values, and a decision tracker that updates as offers progress. The skill is a markdown prompt -- Claude's reasoning does the work, guided by the procedures and data embedded in the skill file.

In production use, Claude combines this skill with web search and file-reading tools to pull real listings, parse actual CARFAX PDFs, and maintain a live negotiation spreadsheet. The demo included here simulates the full pipeline with mock data so the workflow is visible without API keys.

## Architecture

```
SKILL.md              Skill definition: trigger rules, 6-step procedure
state_fees.py         50-state sales tax, title/reg fees, doc fee caps
mock_data.py          5 mock listings, 2 CARFAX reports, market valuations
car_buyer.py          Demo runner: executes all 6 steps with formatted output
run.sh                Entry point
```

**Data flow (demo):**

```
mock_data.py ─> car_buyer.py ─┬─ search_listings()      -> comparison table
                               ├─ analyze_carfax()       -> risk rating (GREEN/YELLOW/RED)
                               ├─ calculate_otd()        -> price breakdown via state_fees.py
                               ├─ draft_outreach()       -> email/text/phone templates
                               ├─ negotiation_strategy() -> anchor/target/walkaway prices
                               └─ decision_tracker()     -> ranked recommendation table
```

**Data flow (production via Claude Code):**

```
User prompt ─> Claude (with SKILL.md loaded)
  ├─ WebSearch: listing sites (CarGurus, Autotrader, Cars.com, etc.)
  ├─ Read: CARFAX PDF or pasted report text
  ├─ state_fees.py: OTD calculation with real state + local rates
  ├─ Claude reasoning: negotiation strategy, offer amounts
  └─ Output: tables, emails, tracker (markdown or file)
```

## Key Files

| File | Purpose |
|------|---------|
| `state_fees.py` | `STATE_SALES_TAX` (50 states), `STATE_TITLE_REG` (title + registration), `STATE_DOC_FEE_CAP` (10 states with caps), `COMMON_ADDONS` (7 add-ons with decline scripts), `calc_otd()` function |
| `mock_data.py` | 5 realistic listings, 2 CARFAX reports (clean + risky), KBB/Edmunds/NADA mock valuations, buyer profile |
| `car_buyer.py` | Six functions mapping to the six skill steps, plus `main()` that runs the full demo |

## Dependencies

None. Python 3.8+ standard library only. The skill itself is just a markdown file -- Claude does the reasoning.

## Limitations

- **No live scraping.** The skill tells Claude *how* to search listing sites, but actual data retrieval depends on Claude's web-search tool or user-pasted URLs. It cannot bypass site anti-scraping measures.
- **Fee data is approximate.** State-level tax rates are included but local/county rates vary. The skill prompts Claude to ask for the buyer's zip code and adjust, but the bundled data covers state-level only.
- **CARFAX parsing is heuristic.** Claude reads CARFAX PDFs or pasted text and applies the red-flag checklist from the skill. It does not have direct CARFAX API access.
- **No real dealer communication.** Outreach templates are generated but not sent. The user must copy-paste or connect their own email/SMS tooling.
- **Market values are estimates.** KBB, Edmunds, and NADA values are referenced by name but not fetched live in the demo. In production, Claude uses web search to look up current values.

## Why It Matters for Claude-Driven Products

- **Lead-gen / marketing:** The outreach template engine and mass-contact workflow pattern is directly reusable for any domain where you need to contact N vendors with a structured ask (e.g., supplier sourcing, real estate offers, vendor RFPs).
- **Agent factories:** The six-step pipeline (search -> analyze -> calculate -> draft -> negotiate -> decide) is a reusable agent architecture pattern. Each step could be a separate tool or sub-agent.
- **Structured data extraction:** The CARFAX analysis and listing normalization demonstrate how to turn unstructured documents into structured tables with risk ratings -- applicable to any document-triage workflow.
- **Domain-specific knowledge injection:** The 50-state fee database shows how to embed reference data into a skill so Claude doesn't need to look it up every time, reducing latency and improving accuracy.
