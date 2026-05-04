# Technical Details

## What It Does

The Anthropic Grade Optimizer is a rule-based linter for Claude-directing artifacts. It parses markdown/JSON/YAML config files and evaluates them against a curated ruleset of 189 Anthropic best-practice rules organized into 11 quality dimensions. Each finding must cite a specific rule — no uncited opinions are emitted. The system prioritizes voice drift detection as the most critical signal, since inconsistent tone in directives causes unpredictable Claude behavior regardless of other quality scores.

## Architecture

```
audit.py              — CLI entry point, file detection, output formatting
rules.py              — 189 rules organized by dimension, each with ID, description, check function
analyzers/
  clarity.py          — Ambiguity detection (passive voice, hedging, double negatives)
  specificity.py      — Vague-phrase detection, missing-example checks
  structure.py        — Header hierarchy, section ordering, markdown lint
  completeness.py     — Required-section checklist per artifact type
  consistency.py      — Contradiction detection across instructions
  voice.py            — Tone classifier, drift detection across sections
  safety.py           — Refusal boundary checks, safety instruction presence
  tool_use.py         — Tool instruction validation, scope checks
  context_mgmt.py     — Context window efficiency patterns
  error_handling.py   — Fallback/failure mode instruction checks
  conventions.py      — Anthropic-specific format/convention validation
sample_claude.md      — Example artifact for demo
```

### Data Flow

1. **Parse** — Detect artifact type (CLAUDE.md, SKILL.md, hook JSON, MCP config, etc.)
2. **Tokenize** — Split into semantic blocks (sections, directives, examples)
3. **Analyze** — Run each dimension's analyzer against the token stream
4. **Score** — Aggregate per-dimension PASS/WARN/FAIL with cited rules
5. **Prioritize** — Voice drift findings bubble to top regardless of other scores
6. **Report** — Structured markdown or JSON output

### Dependencies

- Python 3.9+
- `pyyaml` — for parsing YAML-frontmatter in SKILL.md files
- `regex` — for advanced pattern matching in voice analysis
- No LLM API calls required — all analysis is rule-based and deterministic

### Model Calls

None. This is a static analysis tool. When used as a Claude Skill, Claude itself performs the analysis following the skill instructions — no additional API calls are made.

## Limitations

- **Rule coverage**: The 189 rules are derived from publicly available Anthropic documentation and prompt engineering guides. They may not cover internal or unpublished guidelines.
- **Voice drift detection**: Uses heuristic tone classification (imperative vs. conversational vs. formal). May produce false positives on intentionally multi-voice artifacts.
- **No semantic understanding**: Cannot detect logical contradictions that require deep reasoning — only surface-level pattern conflicts.
- **Artifact types**: Optimized for markdown-based artifacts. Binary configs or compiled prompts are not supported.
- **No auto-fix execution**: The tool recommends fixes but does not automatically apply them without user confirmation.

## Why It Matters

For teams building Claude-driven products (agent factories, marketing automation, ad-creative generators, voice AI systems):

- **Consistent agent behavior** — Voice drift in CLAUDE.md directly causes inconsistent agent outputs, which breaks user trust in production systems.
- **Faster iteration** — Instead of trial-and-error prompt tuning, get deterministic feedback on what violates known best practices.
- **Team alignment** — Shared ruleset means all team members write Claude-directing artifacts to the same standard.
- **Audit trail** — Cited rules create accountability for why each directive exists, useful for compliance-heavy domains.
