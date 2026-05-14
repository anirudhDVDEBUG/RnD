# Technical Details

## What it actually does

The AI Engineering Skill Pack is a Claude Code **skill file** — a structured markdown document (`SKILL.md`) that Claude Code loads into context when trigger phrases match. It contains no executable code itself; instead, it provides detailed methodology checklists that guide Claude through five AI engineering workflows: RAG evaluation, agent debugging, MCP server development, paper reproduction, and benchmark reporting.

When you say "evaluate my RAG pipeline," Claude reads the skill's RAG evaluation section and follows its steps: define eval dataset, measure retrieval quality (recall@k, precision@k, MRR), measure generation quality (faithfulness, relevance, hallucination risk), produce structured output, and suggest improvements. The skill turns Claude from a general-purpose assistant into a domain-specific AI engineering co-pilot that follows repeatable methodology instead of improvising.

## Architecture

```
~/.claude/skills/ai-engineering-skill-pack/
  SKILL.md          # The skill definition — all methodology lives here
                    # ~200 lines of structured markdown
                    # Claude Code auto-loads this on trigger phrase match
```

**Key files in this demo repo:**

| File | Purpose |
|------|---------|
| `skill/SKILL.md` | The actual skill file to install |
| `demo_rag_eval.py` | Mock RAG pipeline + evaluation metrics (precision@k, recall@k, MRR, faithfulness, hallucination) |
| `demo_agent_debug.py` | Simulated agent trace with retry-loop bug + root cause analyzer |
| `demo_benchmark.py` | Mock 3-model x 4-benchmark evaluation with statistical aggregation |
| `run.sh` | Runs all three demos sequentially |

**Data flow (when used as a skill):**

1. User types a trigger phrase in Claude Code (e.g., "evaluate my RAG pipeline")
2. Claude Code matches the phrase against `SKILL.md` frontmatter triggers
3. The skill's methodology section loads into Claude's context
4. Claude reads the user's actual codebase and applies the methodology steps
5. Output: structured report (terminal + JSON/CSV) with actionable recommendations

**Dependencies:** None. The skill is pure markdown. The demo scripts use Python 3.10+ stdlib only (json, random, math, dataclasses, collections, datetime).

## What it does NOT do

- **Does not run evaluations automatically.** It guides Claude through evaluation methodology — Claude reads your code and writes/runs the eval. There is no eval harness binary.
- **Does not include pre-built metrics libraries.** It defines what metrics to compute (recall@k, faithfulness, etc.) and Claude implements them for your specific pipeline.
- **Does not connect to model APIs.** The skill works within Claude Code's existing capabilities. It does not call OpenAI, HuggingFace, or other APIs on its own.
- **Does not replace RAGAS, DeepEval, or LangSmith.** It's a lightweight methodology layer. For production-grade eval pipelines, you'd use those tools — but this skill can help you set them up.
- **Does not persist eval history.** Each evaluation is a one-shot report. If you want tracking over time, you'll need to save the JSON outputs yourself.

## Limitations

- Skill quality depends on Claude's ability to follow methodology steps — complex pipelines with unusual architectures may need manual guidance.
- The "paper reproduction" workflow is aspirational for papers requiring specialized hardware (TPU pods, multi-node training).
- MCP server scaffolding produces starter code, not production-ready servers — you still need to handle auth, rate limiting, and deployment.

## Why it might matter

**For agent factories:** The agent debugging methodology (trace capture, failure classification, retry-loop detection) is directly applicable to anyone building and operating LLM agents at scale. The structured approach to root cause analysis reduces debugging time from hours to minutes.

**For RAG-powered products (lead-gen, marketing, ad creatives):** If you're serving AI-generated content grounded in a knowledge base, the RAG evaluation workflow gives you a repeatable quality gate — measure retrieval recall, generation faithfulness, and hallucination risk before shipping.

**For Claude-driven product builders:** The skill demonstrates how Claude Code skills work as a distribution mechanism. Instead of building a separate CLI tool, you write a methodology doc and Claude becomes your specialized co-pilot. Low distribution friction, zero runtime dependencies.

**For voice AI / real-time systems:** The benchmark reporting workflow (latency percentiles, multi-run statistical aggregation) applies to any system where you need to track and compare model performance under latency constraints.
