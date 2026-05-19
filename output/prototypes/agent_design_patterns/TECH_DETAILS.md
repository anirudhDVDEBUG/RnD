# Technical Details — Agent Design Patterns

## What It Does

The source repository (`huangjia2019/agent-design-patterns`) provides a **7x6 coordinate framework** for agent architecture: 7 architectural layers (Single Agent, Multi-Agent, Planning, Tool Use, Memory, Guardrails, Harness) crossed with 6 design concerns (Decomposition, Orchestration, Context Engineering, Evaluation, Error Recovery, Human-in-the-Loop). Of the 42 possible cells, 28 contain named, documented patterns — each with runnable Python code and "engineering slices" showing how Claude Code, Aider, OpenHands, and DeerFlow implement them.

This prototype distills the framework into a **zero-dependency Python module** (`agent_patterns.py`) that lets you query, search, and compose patterns programmatically. The demo (`demo.py`) exercises every API: grid view, layer/concern drill-down, keyword search, architecture presets, and 2-hop composition analysis.

## Architecture

```
agent_patterns.py     Core module: Pattern dataclass, PatternFramework class
                      28 patterns defined as structured data
                      Query methods: by_layer, by_concern, by_coordinate, search, recommend
                      4 architecture presets (autonomous, swarm, research, pipeline)

demo.py               CLI demo exercising all API methods
                      Colored terminal output, no interactivity required

run.sh                Entry point — runs demo.py with Python 3
```

**Key design decisions:**
- Patterns stored as `dataclass` instances with typed fields (name, layer, concern, summary, when_to_use, example_frameworks, composable_with)
- `recommend()` uses weighted keyword scoring across all pattern fields — no LLM call required
- Composition graph is explicit: each pattern lists `composable_with` references to other pattern names
- Architecture presets are curated pattern bundles for common agent archetypes

**Dependencies:** None beyond Python 3.8+ stdlib (`dataclasses`, `typing`, `json`, `textwrap`).

## Limitations

- The 28 patterns and their metadata are a curated summary — the full source repo has runnable implementations with real LLM calls (requires API keys for OpenAI/Anthropic).
- The `recommend()` function uses keyword matching, not semantic search. For production use, pair with an embedding model.
- Composition chains (`composable_with`) are hand-curated, not exhaustive — any two patterns can technically be combined.
- The framework is descriptive, not prescriptive — it doesn't auto-generate agent code from a pattern selection.

## Why It Matters for Claude-Driven Products

**Agent factories:** If you're building tools that generate agents (lead-gen bots, marketing agents, ad creative pipelines), this framework gives you a structured vocabulary for what patterns to compose. Instead of ad-hoc architectures, you pick coordinates from the grid.

**Context engineering:** Column 3 (Context Engineering) directly addresses the biggest challenge in agent quality — how context flows between steps, agents, and memory. Patterns like Prompt Chaining, Shared Blackboard, Goal-Context Alignment, and Sliding Window Memory are the building blocks for reliable Claude-powered workflows.

**Production hardening:** Layers 6 (Guardrails) and 7 (Harness) cover what most agent tutorials skip — input/output validation, escalation to humans, conflict resolution, and the orchestration infrastructure. Essential for shipping agents to real users.

**Multi-agent coordination:** If you're building agent swarms (e.g. parallel research agents, review pipelines), Layer 2 patterns (Divide and Conquer, Supervisor Orchestrator, Consensus Evaluator) provide proven coordination strategies that map directly to Claude Code's sub-agent capabilities.
