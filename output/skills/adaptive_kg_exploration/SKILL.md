---
name: adaptive_kg_exploration
description: |
  Implement adaptive breadth-depth knowledge graph retrieval inspired by the ARK (Adaptive Retriever of Knowledge) framework.
  TRIGGER when: user wants to explore or query a knowledge graph, needs multi-hop reasoning over graph structures, wants to balance breadth vs depth in graph search, mentions ARK or adaptive KG retrieval, or needs tool-using LLM agents for knowledge graph exploration.
  DO NOT TRIGGER when: simple vector similarity search suffices, no graph structure is involved, or user is doing general database queries.
---

# Adaptive Knowledge Graph Exploration (ARK Pattern)

Implement an adaptive breadth-depth retrieval system for knowledge graphs, based on the ARK framework.

## When to use

- "Explore this knowledge graph to answer a multi-hop question"
- "Build a retriever that balances breadth and depth search over a KG"
- "Implement tool-using LLM agent for knowledge graph traversal"
- "I need adaptive retrieval over a graph with global search and local exploration"
- "Set up ARK-style KG exploration with neighborhood expansion"

## How to use

### Core Concept

ARK gives a language model two complementary operations to explore a knowledge graph:

1. **Global Lexical Search** (breadth) — search node descriptors across the entire graph to find relevant entry points.
2. **One-Hop Neighborhood Exploration** (depth) — expand from a known node to its neighbors, composable into multi-hop traversal.

The LLM decides which tool to call at each step, adapting the breadth-depth tradeoff to the query.

### Implementation Steps

1. **Define the two-tool interface:**

```python
def global_search(query: str, top_k: int = 10) -> list[dict]:
    """Lexical/semantic search over all node descriptors in the KG.
    Returns matching nodes with their IDs, labels, and relevance scores.
    Use for broad discovery — especially language-heavy queries."""
    # Use BM25 or embedding similarity over node text descriptors
    pass

def explore_neighbors(node_id: str, relation_filter: str | None = None) -> list[dict]:
    """Return one-hop neighbors of a node, optionally filtered by relation type.
    Use for depth-oriented expansion — especially relation-heavy queries.
    Chain calls to compose multi-hop traversal."""
    # Query adjacency list / graph DB for neighbors
    pass
```

2. **Set up the agent loop:**

```python
tools = [
    {"name": "global_search", "description": "Search all nodes by text. Use for discovery.",
     "parameters": {"query": "str", "top_k": "int (default 10)"}},
    {"name": "explore_neighbors", "description": "Get one-hop neighbors of a node. Chain for multi-hop.",
     "parameters": {"node_id": "str", "relation_filter": "optional str"}},
]

system_prompt = """You are a knowledge graph explorer. Given a query, use the available tools to find the answer.

Strategy:
- Start with global_search to find relevant entry nodes.
- Use explore_neighbors to follow promising relations (multi-hop).
- Alternate between breadth (global_search) and depth (explore_neighbors) as needed.
- For language-heavy queries, lean on global_search.
- For relation-heavy queries, lean on explore_neighbors.
- Stop when you have sufficient evidence to answer."""
```

3. **Run the adaptive retrieval loop** with the LLM deciding tool calls until it produces a final answer or hits a step budget (typically 5-15 steps).

4. **Optional: Distill trajectories** — Collect (query, tool-call-trajectory) pairs from a large teacher model and fine-tune a smaller model (e.g., 8B) via imitation learning on the action sequences (label-free, no reward model needed).

### Key Design Decisions

| Decision | Recommendation |
|---|---|
| Node index | BM25 over concatenated node descriptors (name + attributes) |
| Graph store | NetworkX for small graphs, Neo4j/ArangoDB for large |
| Step budget | 5-15 tool calls per query |
| Stopping | LLM emits a `finish` action with collected evidence |
| Evaluation | Hit@1 and MRR on target node/answer retrieval |

### Advantages over alternatives

- No fragile seed-node selection required
- No pre-set hop depth — adapts per query
- No retrieval-specific training needed (training-free)
- Composes breadth and depth naturally via tool use

## References

- [ARK: Adaptive Retriever of Knowledge](https://arxiv.org/abs/2601.13969) — Original paper describing the adaptive breadth-depth retrieval framework, evaluated on the STaRK benchmark achieving 59.1% Hit@1 and 67.4 MRR.
