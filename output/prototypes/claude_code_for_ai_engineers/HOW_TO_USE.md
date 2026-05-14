# How to Use

## What this is

A **Claude Code skill** — a markdown file you drop into your skills directory that teaches Claude Code structured methodologies for AI engineering tasks. No pip packages, no servers, no API keys.

## Install (30 seconds)

```bash
# Clone or copy the skill file
git clone https://github.com/surpradhan/claude-code-for-ai-engineers.git
cp -r claude-code-for-ai-engineers/skill/ ~/.claude/skills/ai-engineering-skill-pack/

# That's it. Claude Code reads SKILL.md automatically.
```

Alternatively, copy `skill/SKILL.md` from this repo to `~/.claude/skills/ai-engineering-skill-pack/SKILL.md`.

## Trigger phrases

Once installed, these phrases activate the skill inside Claude Code:

| Phrase | Workflow |
|--------|----------|
| `evaluate my RAG pipeline` | Retrieval + generation metrics, per-query breakdown, recommendations |
| `debug this agent` | Execution trace, failure point detection, root cause classification |
| `build an MCP server for X` | Scaffold resources/tools, transport setup, handler implementation |
| `reproduce results from this paper` | Parse claims, set up env, run experiments, compare to paper |
| `run benchmark report` | Execute eval suites, aggregate stats, generate comparison tables |
| `RAG eval` | Short alias for RAG evaluation |
| `agent trace debugging` | Short alias for agent debugging |

## First 60 seconds

### Run the demo (no Claude Code needed)

```bash
bash run.sh
```

Output: three formatted reports printed to terminal + JSON files:
- **RAG Evaluation** — precision@k, recall@k, MRR, faithfulness, relevance, hallucination risk for 5 queries against 8 documents
- **Agent Debug** — 11-step execution trace showing a retry-loop bug, with root cause analysis and 5 fix recommendations
- **Benchmark Report** — 3 models compared across 4 benchmarks with mean/std/latency per run

### Use with Claude Code (after installing the skill)

```
$ claude
> evaluate my RAG pipeline in src/rag/ using the test queries in eval/queries.json
```

Claude will:
1. Read your retriever and generator code
2. Identify your eval dataset (or help you create one)
3. Measure retrieval quality (recall@k, precision@k, MRR)
4. Measure generation quality (faithfulness, relevance, hallucination detection)
5. Produce a structured report with per-query breakdowns
6. Suggest concrete improvements based on failure patterns

### Another example

```
> debug why my agent in src/agent/ fails on task_003
```

Claude will:
1. Trace the agent's execution step by step
2. Identify the failure point (tool error, loop, context overflow)
3. Classify the root cause
4. Recommend specific fixes

## Requirements

- Python 3.10+ (for the demo scripts — stdlib only, no pip packages)
- Claude Code CLI (for using the skill in practice)
- No API keys needed for the demo; the skill itself uses Claude's built-in capabilities
