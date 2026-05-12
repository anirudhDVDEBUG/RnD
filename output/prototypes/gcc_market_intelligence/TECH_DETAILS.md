# Tech Details — GCC Market Intelligence

## What it does

GCC Market Intelligence is a Claude Code skill (a `SKILL.md` knowledge file) that equips Claude with structured, reference-grade knowledge about entering GCC markets as a B2B or B2G founder. When triggered, Claude draws on the skill's embedded playbook to produce country-specific briefings covering sovereign wealth funds, procurement portals, data residency rules, labor localization quotas, entity setup options, and a step-by-step soft-landing plan.

The companion `gcc_intel.py` CLI mirrors this intelligence as a standalone tool, using the same embedded data to generate briefings, country comparisons, and JSON output — all without API calls.

## Architecture

```
SKILL.md               # Claude Code skill — the core asset
  |                      Trigger-phrase matching via frontmatter description
  |                      Structured sections: country profiles, SWFs,
  |                      procurement, compliance, soft-landing playbook
  |
gcc_intel.py            # Standalone Python CLI demo
  |                      ~350 lines, pure stdlib (argparse, json, dataclasses)
  |                      Embedded dicts for all 6 GCC countries
  |                      Modes: --country, --compare, --all, --json
  |
run.sh                  # End-to-end demo runner
```

**Key files:**

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill itself — drop into `~/.claude/skills/` |
| `gcc_intel.py` | CLI demo with embedded GCC reference data |
| `run.sh` | Runs three demo scenarios (briefing, comparison, JSON) |

**Data flow (skill mode):** User prompt → Claude detects GCC/Gulf/MENA trigger → skill content injected into context → Claude generates structured answer using skill knowledge + its own training data.

**Data flow (CLI mode):** CLI args → `generate_briefing()` → `print_briefing()` or JSON dump. No network calls.

**Dependencies:** None. Python 3.10+ stdlib only. No model calls in the CLI — it's pure reference data.

## Limitations

- **Static data:** SWF AUM figures, incentive programs, and regulatory details are point-in-time snapshots. The GCC regulatory landscape changes fast (e.g., KSA Regional HQ mandate, evolving PDPL enforcement). Users should verify critical details against official sources.
- **No live data feeds:** The skill doesn't pull real-time procurement listings, fund announcements, or regulatory updates. It provides the framework and context; users must check Etimad/TEJARI/Daman for live tenders.
- **Breadth over depth:** Covers all 6 GCC countries but at overview level. Deep-dive topics (e.g., KSA NCA cybersecurity certification process, UAE CBUAE open-banking framework) need additional research.
- **English only:** The skill content is English. It references Arabic localization as a requirement but doesn't provide Arabic translations.
- **No CRM/pipeline integration:** Generates intelligence but doesn't track deals, contacts, or follow-ups.

## Why it matters for Claude-driven products

- **Lead-gen / sales intelligence:** Teams building AI-assisted sales tools for MENA markets can use this skill's data structure as a template — country profiles, stakeholder maps, and compliance checklists are directly reusable.
- **Agent factories:** A "GCC market entry agent" could combine this skill with web-search MCP and CRM MCP to automate the full research → outreach → compliance pipeline.
- **Marketing / content:** Content teams targeting GCC audiences can use the skill to generate region-specific blog posts, whitepapers, or pitch decks with accurate local context.
- **Consulting automation:** Strategy consultants doing GCC market-entry engagements can use this as a first-draft generator, then layer on proprietary research.
