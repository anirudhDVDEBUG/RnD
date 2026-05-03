# Technical Details

## What It Does

Founder Fundraising Outreach is a Claude Code skill — a structured prompt template that guides Claude to generate investor communications following proven cold-email best practices. When a founder describes their company and target investor, the skill enforces a strict framework: 5-8 sentences max, one specific CTA, metrics instead of adjectives, and investor-specific personalization (portfolio references, thesis alignment). It covers four outreach types: cold emails, follow-ups, warm intro requests, and due diligence prep documents.

The companion Python module (`outreach.py`) implements the same logic as deterministic string templates, useful for batch generation or integration into pipelines without LLM calls.

## Architecture

```
SKILL.md                    # Claude skill prompt (drop into ~/.claude/skills/)
outreach.py                 # Standalone Python implementation
  ├── CompanyProfile        # Dataclass: name, stage, traction, raising amount
  ├── InvestorProfile       # Dataclass: name, firm, thesis, portfolio
  ├── generate_cold_email() # 5-8 sentence cold outreach
  ├── generate_followup()   # Shorter follow-up with new traction
  ├── generate_warm_intro() # Third-person forwardable blurb
  ├── generate_dd_prep()    # Due diligence markdown template
  └── run_demo()            # End-to-end demo with mock data
```

**Data flow:**
1. User provides company context (name, stage, traction metrics, raise details)
2. User provides investor target (name, firm, thesis, portfolio companies)
3. Skill/module selects the appropriate template (cold / follow-up / warm intro / DD)
4. Output is a ready-to-send email or markdown document

**Dependencies:** Python 3.10+ stdlib only (`json`, `textwrap`, `dataclasses`). No external packages. No API keys. No model calls in the Python module.

**Key files:**
| File | Purpose |
|---|---|
| `SKILL.md` | Claude skill prompt — the core asset |
| `outreach.py` | Python implementation with templates + demo |
| `run.sh` | One-command demo runner |

## Limitations

- **No CRM integration** — generates text, doesn't send emails or sync with Salesforce/HubSpot.
- **No investor database** — you provide the investor details; it doesn't look up firms or partners.
- **No A/B testing** — generates one variant per request; no subject-line optimization.
- **Template-bound** — the Python module uses fixed templates. The Claude skill is more flexible but still follows the structured framework.
- **English only** — templates and guidance are English-language.

## Why It Matters

For teams building Claude-driven products in **lead-gen and marketing automation**: this skill demonstrates a pattern — structured prompt templates that enforce domain-specific best practices (brevity, specificity, single CTA) while remaining flexible to user input. The same architecture applies to sales outreach, recruiter emails, partnership proposals, or any high-stakes communication where generic LLM output falls flat. The Python companion module shows how to implement the same logic deterministically for batch/pipeline use without LLM calls.
