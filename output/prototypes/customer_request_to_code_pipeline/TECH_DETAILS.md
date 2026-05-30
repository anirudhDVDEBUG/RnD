# Technical Details

## What It Does

This pipeline takes structured customer requests (feature asks, bug reports, support tickets) and produces prioritized implementation plans with concrete code changes. It simulates the workflow described in [Braintrust's engineering process](https://openai.com/index/braintrust) where AI agents convert customer input into shipped experiments and features.

The demo runs entirely offline with mock data and a simulated codebase. In production, you would wire in a real LLM (Claude, GPT) for natural-language parsing and a real codebase for file mapping — but the pipeline structure, prioritization logic, and output format are production-ready patterns.

## Architecture

```
sample_requests.json
        │
        ▼
┌─── pipeline.py ────────────────────────────┐
│                                             │
│  1. PARSE     → CustomerRequest dataclass   │
│                 Extract what/why/where       │
│                                             │
│  2. MAP       → mock_codebase.py            │
│                 Keyword → file mapping       │
│                 Complexity assessment        │
│                                             │
│  3. PRIORITIZE → Score 0-100                │
│                  (requesters, revenue,       │
│                   urgency, complexity)       │
│                                             │
│  4. PLAN      → Implementation steps        │
│                 Test strategy                │
│                 Risk assessment              │
│                 Code generation              │
│                                             │
│  5. RENDER    → Terminal (color-coded)       │
│                 Markdown file                │
└─────────────────────────────────────────────┘
        │
        ▼
  output_plans.md  +  stdout
```

### Key Files

| File | Purpose |
|---|---|
| `pipeline.py` | Main pipeline: parse, prioritize, plan, render |
| `mock_codebase.py` | Simulated SaaS codebase structure + keyword-to-file mapping |
| `sample_requests.json` | 5 realistic customer requests with priority signals |
| `SKILL.md` | Claude Code skill definition for integrating into agent workflows |

### Data Flow

1. **Input**: JSON array of customer requests with structured priority signals
2. **Parsing**: Regex-based extraction of what/why/where from natural language
3. **File Mapping**: Keyword matching against `KEYWORD_FILE_MAP` to find affected source files
4. **Prioritization**: Weighted scoring — requesters (30%), revenue (35%), urgency (25%), complexity bonus (10%)
5. **Code Generation**: Template-based code patches matched to request type
6. **Output**: Color terminal display + `output_plans.md` markdown report

### Dependencies

None beyond Python 3.10+ stdlib (`json`, `csv`, `re`, `dataclasses`, `pathlib`, `typing`, `io`, `secrets`, `hashlib`, `enum`).

## Limitations

- **No real LLM calls**: Parsing uses regex heuristics, not language models. In production, swap `parse_request()` for a Claude API call to handle ambiguous customer language.
- **Static codebase**: Uses a mock file map. In production, integrate with `git ls-files` + AST analysis or a code search index.
- **Template code generation**: Generated code comes from predefined templates, not dynamic synthesis. Replace with Claude/Codex for real implementations.
- **No git/PR integration**: Outputs plans as text/markdown. A real pipeline would create branches, commits, and PRs via GitHub API.
- **English only**: Regex patterns assume English customer input.

## Why This Matters for Claude-Driven Products

This pattern is directly applicable to several high-value use cases:

- **Agent factories**: The parse → map → plan → implement pipeline is a reusable skeleton for any "input → structured action" agent. Swap the codebase map for an ad creative library, marketing template set, or lead database.
- **Lead-gen / marketing**: The priority scoring model (requesters x revenue x urgency) translates directly to lead scoring. The "customer request" input could be inbound form submissions triaged into marketing automation actions.
- **Support automation**: Customer support tickets parsed into implementation plans = fewer hops from "customer says X" to "engineer ships Y." The generated markdown report is ready for Slack bots or Linear/Jira integrations.
- **Ad creative pipelines**: Replace "code changes" with "ad variations" — the same parse-and-plan structure works for turning campaign briefs into creative assets.
