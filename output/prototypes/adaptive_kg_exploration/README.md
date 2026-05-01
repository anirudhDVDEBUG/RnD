# Adaptive Knowledge Graph Exploration (ARK Pattern)

A self-contained demo of the ARK (Adaptive Retriever of Knowledge) framework
for knowledge graph exploration, based on [arXiv:2601.13969](https://arxiv.org/abs/2601.13969).

## What it does

The demo builds a small science knowledge graph (22 nodes, 30 edges) covering
physicists, discoveries, theories, and Nobel Prizes. An agent explores this
graph using two complementary tools:

| Tool | Mode | Purpose |
|------|------|---------|
| `global_search` | Breadth | BM25 lexical search over all node descriptors to find entry points |
| `explore_neighbors` | Depth | One-hop neighborhood expansion, composable into multi-hop traversal |

A rule-based agent loop (simulating LLM tool-calling) adaptively mixes breadth
and depth operations to answer three multi-hop queries, printing its reasoning
trace at each step.

## Install

```bash
pip install -r requirements.txt
```

Only dependency: `networkx` (for graph storage). BM25 is implemented from
scratch — no external search library needed.

## Run

```bash
bash run.sh
```

## Expected output

The demo runs 3 queries and prints:

1. **Step-by-step trace** — each tool call with reasoning, arguments, and results
2. **Final answer** — synthesized from collected evidence
3. **Summary table** — steps taken, evidence count, and breadth/depth tool mix

```
QUERY: What Nobel Prize did Einstein receive and what was it for?

  Step 1 | global_search(query='What Nobel Prize did Einstein receive...')
         | Reasoning: Starting with global_search to find relevant entry points.
         |   - Albert Einstein (person) (score=...)
         |   - Nobel Prize in Physics 1921 (award) (score=...)
         ...
  Step 2 | explore_neighbors(node_id='einstein')
         | Reasoning: Exploring neighbors of 'einstein' to find related entities (depth).
         |   - Theory of Relativity [-> developed] (theory)
         |   - Photoelectric Effect [-> explained] (discovery)
         |   - Nobel Prize in Physics 1921 [-> received] (award)
         ...

  ANSWER: Related Nobel Prizes found: Nobel Prize in Physics 1921, ...
```

## Key concepts

- **No API keys needed** — uses a rule-based agent and built-in BM25
- **Adaptive breadth-depth** — the agent starts broad (global search), then
  goes deep (neighbor exploration), with second-hop expansion for promising nodes
- **Step budget** — capped at 10 tool calls per query
- **Composable multi-hop** — `explore_neighbors` chains naturally for 2+ hop paths

## Reference

> ARK: Adaptive Retriever of Knowledge — [arXiv:2601.13969](https://arxiv.org/abs/2601.13969)
