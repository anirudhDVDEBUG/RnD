# Tech Details — Hypothesis Validator

## What It Does

Hypothesis Validator is a **Claude Code skill** — a structured prompt file (`SKILL.md`) that guides Claude through a 6-step startup validation framework. When a user describes a business idea, Claude systematically evaluates Ideal Customer Profile clarity, market evidence, willingness-to-pay signals, and go-to-market feasibility, then produces a scorecard with a green/yellow/red verdict and concrete next steps.

It is not a standalone application. It extends Claude Code's behavior via the skills system, turning Claude into a structured business-analysis agent that follows established frameworks (Jobs-to-be-Done, Customer Discovery, The Mom Test).

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `SKILL.md` | The skill prompt — installed at `~/.claude/skills/hypothesis_validator/SKILL.md`. Contains the 6-step framework, scoring rubrics, and output template. |
| `validate_hypothesis.py` | Standalone demo script. Python dataclasses model the same 6-step structure; runs two mock hypotheses to show the output format. No external deps. |
| `run.sh` | Wrapper to execute the demo. |

### Data Flow (when used as a Claude Code skill)

```
User states hypothesis
  -> Claude parses into structured format (target customer / problem / action / solution / assumption)
  -> Step 2: ICP clarity check (Claude evaluates specificity, reachability, urgency)
  -> Step 3: Evidence scan (Claude uses web search for demand signals, alternatives, failed predecessors)
  -> Step 4: Money signals (Claude assesses willingness-to-pay from competitor pricing, budget lines, JTBD value)
  -> Step 5: GTM reality check (Claude evaluates channels, first-10-customers path, solo feasibility)
  -> Step 6: Scoring + verdict (4 dimensions, each rated, combined into green/yellow/red)
  -> Output: Markdown report with scorecard, verdict, next steps, risks
```

### Dependencies

- **Skill mode**: Zero dependencies. Pure prompt; Claude's built-in web search handles evidence gathering.
- **Demo script**: Python 3.10+ (uses `dataclasses`, `json`, `textwrap` from stdlib). No `pip install` needed.

### Model Calls

The skill itself makes no API calls — it runs inside Claude Code's existing conversation. Claude may invoke its web-search tool during Step 3 (evidence scan) to look up Google Trends data, Reddit threads, competitor pricing, etc. This is Claude's native capability, not an external integration.

## Limitations

- **No live data in the demo**: `validate_hypothesis.py` uses hardcoded mock data. The real value comes from the Claude Code skill, which uses live web search.
- **Quality depends on Claude's search**: Evidence scan quality is bounded by what Claude can find via web search. Niche B2B markets may have sparse public data.
- **No persistence**: The skill doesn't track hypotheses over time or compare multiple runs. Each validation is a one-shot report.
- **Subjective scoring**: The ICP/evidence/money/GTM ratings are Claude's judgment calls, not computed from quantitative data. Two runs on the same hypothesis may produce slightly different assessments.
- **No integrations**: Doesn't connect to CRMs, analytics tools, or survey platforms. It's a thinking framework, not a data pipeline.

## Why It Matters for Claude-Driven Products

| Use case | Relevance |
|---|---|
| **Agent factories** | Shows how a structured prompt-skill can turn Claude into a domain-specific analyst without any code. Template for building other business-analysis agents. |
| **Lead-gen / marketing** | The ICP clarity and GTM steps are directly applicable to qualifying leads and planning outbound campaigns. |
| **Ad creatives** | Understanding JTBD and money signals feeds directly into messaging — knowing what customers value and will pay for shapes ad copy. |
| **Voice AI** | The 6-step framework could be adapted for a voice-driven founder coaching agent that walks through validation interactively. |
