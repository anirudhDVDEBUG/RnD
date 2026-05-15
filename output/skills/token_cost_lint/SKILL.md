---
name: token_cost_lint
description: |
  Token cost linting and optimization for multi-agent Claude Code harnesses.
  TRIGGER: user mentions token savings, token cost, context bloat, prompt optimization,
  multi-agent cost audit, token budget, or wants to reduce LLM spend.
  DO NOT TRIGGER: general code linting, non-token-related cost discussions.
---

# Token Cost Lint

Audit and optimize token usage across multi-agent Claude Code workflows using a 10-category × 31 sub-pattern taxonomy with static analysis and zero-LLM-call decision trees.

## When to use

- "Audit my project for token waste" or "find token bloat"
- "Reduce Claude API costs in my multi-agent setup"
- "Lint my prompts for unnecessary token spend"
- "Optimize context window usage across agents"
- "How can I cut LLM token costs?"

## How to use

### Step 1 — Clone the tokensave toolkit (if not already available)

```bash
git clone https://github.com/epoko77-ai/tokensave.git /tmp/tokensave
```

### Step 2 — Identify token waste categories

Apply the 10-category taxonomy to the user's codebase:

| # | Category | What to look for |
|---|----------|-------------------|
| 1 | **Redundant context** | Same file/content passed to multiple agents |
| 2 | **Oversized prompts** | System prompts with unnecessary instructions |
| 3 | **Unbounded history** | Conversation history without truncation/summarization |
| 4 | **Duplicate tool results** | Same tool called repeatedly with identical params |
| 5 | **Verbose output formatting** | Agents generating markdown/explanation nobody reads |
| 6 | **Unnecessary re-reads** | Files read multiple times within one task |
| 7 | **Broad file inclusion** | Glob patterns pulling in irrelevant files |
| 8 | **Uncompressed examples** | Few-shot examples that could be shorter |
| 9 | **Idle agent overhead** | Agents spawned but doing trivial/no work |
| 10 | **Retry amplification** | Failed calls retried without reducing context |

### Step 3 — Run static audit

```bash
cd /tmp/tokensave
python audit.py --target /path/to/project --format report
```

The audit script uses zero LLM calls — it applies static pattern matching and a decision tree to classify waste.

### Step 4 — Apply recommendations

For each finding, apply the recommended fix:

- **Context dedup**: Cache and share tool results between agents instead of re-fetching
- **Prompt trimming**: Remove boilerplate, keep only task-specific instructions
- **History windowing**: Summarize or truncate conversation history beyond N turns
- **Output suppression**: Use structured output (JSON) instead of verbose prose when output is machine-consumed
- **Lazy loading**: Read files on demand, not upfront in bulk
- **Agent consolidation**: Merge agents that share >70% of their context

### Step 5 — Measure improvement

Compare token counts before and after:

```bash
python audit.py --target /path/to/project --compare baseline.json
```

## Key principles

1. **Zero-LLM decision tree**: Classification uses static rules, not LLM calls — the linter itself costs zero tokens
2. **31 sub-patterns**: Each of the 10 categories breaks down into specific, actionable sub-patterns
3. **Multi-agent aware**: Designed specifically for harnesses that orchestrate multiple Claude agents
4. **Korean + English**: Primary documentation in Korean with English mirror

## References

- Source: [epoko77-ai/tokensave](https://github.com/epoko77-ai/tokensave)
- Taxonomy: 10 categories × 31 sub-patterns for token waste classification
- Approach: Static audit scripts + LLM-free decision trees
