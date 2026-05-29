# Technical Details

## What it does

The Agentic Organization Requirements Accelerator applies the parallel-agent pattern described in Endava's case study with OpenAI Codex to requirements engineering. Instead of a single analyst sequentially reading, decomposing, estimating, and writing specs, the tool spawns four specialized "agents" (analysis functions) that run concurrently via Python's `concurrent.futures`. Each agent reads the same structured input and produces a typed artifact; a cross-validation step then merges, deduplicates, and flags conflicts across all four outputs.

This mirrors Endava's reported approach: they reduced weeks-long requirements analysis to hours by decomposing the work into agentic tasks that run in parallel with human checkpoints at key stages rather than at every step.

## Architecture

```
sample_requirements.yaml
        |
        v
  +-----------+
  | intake.py |  Parse & normalize raw requirements
  +-----------+
        |
        v  (concurrent.futures.ThreadPoolExecutor)
  +-----+-----+-----+-----+
  |     |     |     |     |
  v     v     v     v     v
Decomp  Dep   Feas  Spec   (agents/*.py)
Agent   Agent Agent Agent
  |     |     |     |
  +-----+-----+-----+
        |
        v
  +----------------+
  | validator.py   |  Cross-reference, flag conflicts
  +----------------+
        |
        v
  output/analysis_report.md
```

### Key files

| File | Purpose |
|------|---------|
| `accelerator.py` | CLI entry point, orchestrates the pipeline |
| `intake.py` | YAML parser, normalizes requirements into internal format |
| `agents/decomposition.py` | Breaks requirements into atomic user stories |
| `agents/dependency.py` | Maps inter-requirement dependencies and conflicts |
| `agents/feasibility.py` | Estimates complexity (T-shirt sizing) and flags risks |
| `agents/specwriter.py` | Generates technical specifications with acceptance criteria |
| `validator.py` | Cross-validates agent outputs, produces final report |
| `sample_requirements.yaml` | Demo input (e-commerce platform) |

### Data flow

1. **Intake**: YAML -> list of `Requirement(id, source, text, domain, priority)` namedtuples
2. **Agents**: Each receives the full requirement list, returns typed dicts (stories, deps, estimates, specs)
3. **Validator**: Joins on requirement ID, checks for orphan references, conflicting priorities, unestimated stories
4. **Report**: Markdown with sections for backlog, dependencies, risks, and delivery phases

### Dependencies

- `pyyaml` — requirements file parsing
- `rich` — terminal output formatting
- Python 3.9+ standard library (`concurrent.futures`, `dataclasses`, `pathlib`)

### Model calls

The demo uses **no LLM calls** — all analysis is rule-based heuristics and keyword matching to keep it runnable without API keys. In a production setup, each agent function would be replaced with a Claude API call using structured output (tool_use) to produce the same typed artifacts. The orchestration, cross-validation, and report generation layers remain the same.

## Limitations

- **Mock analysis only**: The bundled agents use keyword heuristics, not LLM reasoning. Real-world requirements with ambiguity need an actual model backend.
- **No interactive refinement**: Step 4 of the skill (stakeholder feedback loop) is not implemented in the CLI — it's designed for the Claude Code interactive flow.
- **Single-file input**: Currently reads one YAML file. Production use would integrate with Jira, Confluence, or Google Docs APIs.
- **No persistent state**: Each run is stateless. Incremental re-analysis would need a local database or file cache.

## Why it matters for Claude-driven products

- **Agent factories**: The four-agent pipeline is a concrete template for building domain-specific agent orchestration. Fork it, swap the agent logic, and you have a reusable multi-agent scaffold.
- **Lead-gen / marketing**: Requirements acceleration is a high-value consulting deliverable. Wrapping this in a Claude Skill lets agencies offer "instant project scoping" as a differentiator.
- **Enterprise adoption**: Endava's case study shows that agentic coding patterns sell at the C-suite level when framed as "weeks to hours." This demo makes that pitch tangible.
- **Voice AI / ad creatives**: The parallel-agent + cross-validation pattern generalizes beyond requirements — apply it to script analysis, creative brief decomposition, or campaign planning.
