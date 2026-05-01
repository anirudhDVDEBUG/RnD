"""
Adaptive Knowledge Graph Exploration (ARK Pattern)

Demonstrates the ARK framework's two-tool interface for adaptive breadth-depth
retrieval over a knowledge graph:
  1. global_search  — BM25 lexical search across all node descriptors (breadth)
  2. explore_neighbors — one-hop neighborhood expansion (depth)

A rule-based agent loop simulates LLM tool-calling, adaptively choosing between
breadth and depth operations to answer multi-hop questions over a science KG.
"""

import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

import networkx as nx

# ──────────────────────────────────────────────────────────────────────────────
# 1. Build a small science knowledge graph
# ──────────────────────────────────────────────────────────────────────────────

def build_science_kg() -> nx.DiGraph:
    """Build a small knowledge graph about scientists, discoveries, and fields."""
    G = nx.DiGraph()

    nodes = [
        ("einstein", {"label": "Albert Einstein", "type": "person",
         "desc": "Albert Einstein, theoretical physicist, developed the theory of relativity and contributed to quantum mechanics"}),
        ("relativity", {"label": "Theory of Relativity", "type": "theory",
         "desc": "Theory of Relativity, a physics theory by Einstein describing gravity as spacetime curvature"}),
        ("photoelectric", {"label": "Photoelectric Effect", "type": "discovery",
         "desc": "Photoelectric effect, the emission of electrons when light hits a material, explained by Einstein using quantum theory"}),
        ("nobel_1921", {"label": "Nobel Prize in Physics 1921", "type": "award",
         "desc": "Nobel Prize in Physics 1921, awarded to Albert Einstein for the photoelectric effect"}),
        ("quantum_mechanics", {"label": "Quantum Mechanics", "type": "field",
         "desc": "Quantum mechanics, a fundamental theory in physics describing nature at atomic and subatomic scales"}),
        ("bohr", {"label": "Niels Bohr", "type": "person",
         "desc": "Niels Bohr, Danish physicist, developed the Bohr model of the atom and contributed to quantum theory"}),
        ("bohr_model", {"label": "Bohr Model", "type": "theory",
         "desc": "Bohr model, a model of the atom with electrons orbiting the nucleus in quantized energy levels"}),
        ("nobel_1922", {"label": "Nobel Prize in Physics 1922", "type": "award",
         "desc": "Nobel Prize in Physics 1922, awarded to Niels Bohr for his atomic structure research"}),
        ("heisenberg", {"label": "Werner Heisenberg", "type": "person",
         "desc": "Werner Heisenberg, German physicist, formulated the uncertainty principle in quantum mechanics"}),
        ("uncertainty", {"label": "Uncertainty Principle", "type": "theory",
         "desc": "Heisenberg uncertainty principle, states that position and momentum of a particle cannot both be precisely known"}),
        ("nobel_1932", {"label": "Nobel Prize in Physics 1932", "type": "award",
         "desc": "Nobel Prize in Physics 1932, awarded to Werner Heisenberg for quantum mechanics"}),
        ("curie", {"label": "Marie Curie", "type": "person",
         "desc": "Marie Curie, Polish-French physicist and chemist, pioneer in radioactivity research"}),
        ("radioactivity", {"label": "Radioactivity", "type": "field",
         "desc": "Radioactivity, the spontaneous emission of radiation from unstable atomic nuclei"}),
        ("polonium", {"label": "Polonium", "type": "element",
         "desc": "Polonium, a radioactive chemical element discovered by Marie Curie, named after Poland"}),
        ("radium", {"label": "Radium", "type": "element",
         "desc": "Radium, a radioactive chemical element discovered by Marie and Pierre Curie"}),
        ("nobel_1903", {"label": "Nobel Prize in Physics 1903", "type": "award",
         "desc": "Nobel Prize in Physics 1903, awarded to Marie Curie, Pierre Curie, and Henri Becquerel for radioactivity research"}),
        ("nobel_chem_1911", {"label": "Nobel Prize in Chemistry 1911", "type": "award",
         "desc": "Nobel Prize in Chemistry 1911, awarded to Marie Curie for discovery of radium and polonium"}),
        ("planck", {"label": "Max Planck", "type": "person",
         "desc": "Max Planck, German physicist, originated quantum theory with Planck's constant"}),
        ("planck_constant", {"label": "Planck's Constant", "type": "concept",
         "desc": "Planck's constant, fundamental physical constant relating photon energy to frequency"}),
        ("black_body", {"label": "Black-body Radiation", "type": "discovery",
         "desc": "Black-body radiation, electromagnetic radiation emitted by an idealized opaque body, explained by Planck"}),
        ("nobel_1918", {"label": "Nobel Prize in Physics 1918", "type": "award",
         "desc": "Nobel Prize in Physics 1918, awarded to Max Planck for discovery of energy quanta"}),
        ("copenhagen", {"label": "Copenhagen Interpretation", "type": "theory",
         "desc": "Copenhagen interpretation of quantum mechanics, developed primarily by Bohr and Heisenberg"}),
    ]

    edges = [
        ("einstein", "relativity", "developed"),
        ("einstein", "photoelectric", "explained"),
        ("einstein", "nobel_1921", "received"),
        ("einstein", "quantum_mechanics", "contributed_to"),
        ("photoelectric", "quantum_mechanics", "part_of"),
        ("photoelectric", "nobel_1921", "basis_for"),
        ("bohr", "bohr_model", "developed"),
        ("bohr", "nobel_1922", "received"),
        ("bohr", "quantum_mechanics", "contributed_to"),
        ("bohr", "copenhagen", "developed"),
        ("bohr_model", "quantum_mechanics", "part_of"),
        ("heisenberg", "uncertainty", "formulated"),
        ("heisenberg", "nobel_1932", "received"),
        ("heisenberg", "quantum_mechanics", "contributed_to"),
        ("heisenberg", "copenhagen", "developed"),
        ("uncertainty", "quantum_mechanics", "part_of"),
        ("curie", "radioactivity", "researched"),
        ("curie", "polonium", "discovered"),
        ("curie", "radium", "discovered"),
        ("curie", "nobel_1903", "received"),
        ("curie", "nobel_chem_1911", "received"),
        ("polonium", "radioactivity", "exhibits"),
        ("radium", "radioactivity", "exhibits"),
        ("planck", "planck_constant", "introduced"),
        ("planck", "black_body", "explained"),
        ("planck", "nobel_1918", "received"),
        ("planck", "quantum_mechanics", "founded"),
        ("planck_constant", "quantum_mechanics", "fundamental_to"),
        ("planck_constant", "photoelectric", "used_in"),
        ("black_body", "planck_constant", "led_to"),
    ]

    for node_id, attrs in nodes:
        G.add_node(node_id, **attrs)
    for src, dst, rel in edges:
        G.add_edge(src, dst, relation=rel)

    return G


# ──────────────────────────────────────────────────────────────────────────────
# 2. BM25 Index for global lexical search
# ──────────────────────────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+', text.lower())


@dataclass
class BM25Index:
    """Simple BM25 index over node descriptors."""
    docs: dict[str, list[str]] = field(default_factory=dict)
    df: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    avgdl: float = 0.0
    k1: float = 1.5
    b: float = 0.75

    def build(self, graph: nx.DiGraph):
        for node_id, data in graph.nodes(data=True):
            tokens = tokenize(data.get("desc", "") + " " + data.get("label", ""))
            self.docs[node_id] = tokens

        seen = set()
        for doc_id, tokens in self.docs.items():
            seen.clear()
            for t in tokens:
                if t not in seen:
                    self.df[t] += 1
                    seen.add(t)

        total = sum(len(t) for t in self.docs.values())
        self.avgdl = total / max(len(self.docs), 1)

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        qtokens = tokenize(query)
        N = len(self.docs)
        scores = {}
        for doc_id, tokens in self.docs.items():
            score = 0.0
            dl = len(tokens)
            tf_map = defaultdict(int)
            for t in tokens:
                tf_map[t] += 1
            for qt in qtokens:
                if qt not in tf_map:
                    continue
                tf = tf_map[qt]
                df = self.df.get(qt, 0)
                idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                score += idf * numerator / denominator
            if score > 0:
                scores[doc_id] = score

        ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        return [{"node_id": nid, "score": round(s, 3)} for nid, s in ranked]


# ──────────────────────────────────────────────────────────────────────────────
# 3. ARK Two-Tool Interface
# ──────────────────────────────────────────────────────────────────────────────

class ARKTools:
    """The two ARK tools: global_search (breadth) and explore_neighbors (depth)."""

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.index = BM25Index()
        self.index.build(graph)

    def global_search(self, query: str, top_k: int = 5) -> list[dict]:
        """Lexical search over all node descriptors in the KG (breadth)."""
        results = self.index.search(query, top_k)
        for r in results:
            node_data = self.graph.nodes[r["node_id"]]
            r["label"] = node_data.get("label", "")
            r["type"] = node_data.get("type", "")
        return results

    def explore_neighbors(self, node_id: str, relation_filter: Optional[str] = None) -> list[dict]:
        """Return one-hop neighbors of a node (depth). Includes both outgoing and incoming edges."""
        if node_id not in self.graph:
            return [{"error": f"Node '{node_id}' not found"}]

        neighbors = []
        # Outgoing edges
        for _, target, data in self.graph.out_edges(node_id, data=True):
            rel = data.get("relation", "related_to")
            if relation_filter and rel != relation_filter:
                continue
            target_data = self.graph.nodes[target]
            neighbors.append({
                "node_id": target,
                "label": target_data.get("label", ""),
                "type": target_data.get("type", ""),
                "relation": rel,
                "direction": "outgoing",
            })
        # Incoming edges
        for source, _, data in self.graph.in_edges(node_id, data=True):
            rel = data.get("relation", "related_to")
            if relation_filter and rel != relation_filter:
                continue
            source_data = self.graph.nodes[source]
            neighbors.append({
                "node_id": source,
                "label": source_data.get("label", ""),
                "type": source_data.get("type", ""),
                "relation": rel,
                "direction": "incoming",
            })
        return neighbors


# ──────────────────────────────────────────────────────────────────────────────
# 4. Rule-based Agent (simulates LLM tool-calling)
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class AgentStep:
    tool: str
    args: dict
    result: list[dict]
    reasoning: str


class ARKAgent:
    """
    A rule-based agent that simulates adaptive breadth-depth retrieval.
    In production, an LLM would decide tool calls; here we use heuristics.
    """

    def __init__(self, tools: ARKTools, max_steps: int = 10):
        self.tools = tools
        self.max_steps = max_steps

    def run(self, query: str) -> dict:
        """Execute the adaptive retrieval loop for a query."""
        steps: list[AgentStep] = []
        visited_nodes: set[str] = set()
        evidence: list[dict] = []
        collected_labels: set[str] = set()

        print(f"\n{'='*70}")
        print(f"QUERY: {query}")
        print(f"{'='*70}")

        # Step 1: Always start with global search (breadth)
        reasoning = "Starting with global_search to find relevant entry points."
        print(f"\n  Step 1 | global_search(query={query!r})")
        print(f"         | Reasoning: {reasoning}")
        results = self.tools.global_search(query, top_k=5)
        steps.append(AgentStep("global_search", {"query": query}, results, reasoning))
        self._print_results(results)

        # Collect top entry nodes
        entry_nodes = [r["node_id"] for r in results[:3]]

        step_num = 2
        # Step 2+: Explore neighbors of top results (depth)
        for node_id in entry_nodes:
            if step_num > self.max_steps:
                break
            if node_id in visited_nodes:
                continue
            visited_nodes.add(node_id)

            reasoning = f"Exploring neighbors of '{node_id}' to find related entities (depth)."
            print(f"\n  Step {step_num} | explore_neighbors(node_id={node_id!r})")
            print(f"         | Reasoning: {reasoning}")
            neighbors = self.tools.explore_neighbors(node_id)
            steps.append(AgentStep("explore_neighbors", {"node_id": node_id}, neighbors, reasoning))
            self._print_results(neighbors)

            # Collect evidence
            for n in neighbors:
                if "error" not in n:
                    evidence.append(n)
                    collected_labels.add(n["label"])

            step_num += 1

            # Adaptive: if we found promising nodes, do a second hop
            for neighbor in neighbors[:2]:
                if step_num > self.max_steps:
                    break
                nid = neighbor.get("node_id", "")
                if nid in visited_nodes or not nid:
                    continue
                visited_nodes.add(nid)

                reasoning = f"Second-hop expansion from '{nid}' for deeper evidence."
                print(f"\n  Step {step_num} | explore_neighbors(node_id={nid!r})")
                print(f"         | Reasoning: {reasoning}")
                hop2 = self.tools.explore_neighbors(nid)
                steps.append(AgentStep("explore_neighbors", {"node_id": nid}, hop2, reasoning))
                self._print_results(hop2)

                for n in hop2:
                    if "error" not in n:
                        evidence.append(n)
                        collected_labels.add(n["label"])

                step_num += 1

        # Synthesize answer
        answer = self._synthesize(query, evidence)
        print(f"\n  ANSWER: {answer}")
        print(f"  Total steps: {len(steps)}")
        print(f"  Nodes visited: {visited_nodes}")
        print(f"  Evidence entities: {collected_labels}")

        return {
            "query": query,
            "answer": answer,
            "steps": [(s.tool, s.args) for s in steps],
            "num_steps": len(steps),
            "evidence_count": len(evidence),
        }

    def _print_results(self, results: list[dict]):
        if not results:
            print("         | (no results)")
            return
        for r in results[:5]:
            parts = []
            if "label" in r:
                parts.append(r["label"])
            if "relation" in r:
                arrow = "->" if r.get("direction") == "outgoing" else "<-"
                parts.append(f"[{arrow} {r['relation']}]")
            if "score" in r:
                parts.append(f"(score={r['score']})")
            if "type" in r:
                parts.append(f"({r['type']})")
            print(f"         |   - {' '.join(parts)}")

    def _synthesize(self, query: str, evidence: list[dict]) -> str:
        """Simple rule-based answer synthesis from collected evidence."""
        query_lower = query.lower()

        # Collect unique entities by type
        by_type: dict[str, list[str]] = defaultdict(list)
        for e in evidence:
            t = e.get("type", "unknown")
            label = e.get("label", "")
            if label and label not in by_type[t]:
                by_type[t].append(label)

        if "nobel" in query_lower and "prize" in query_lower:
            awards = by_type.get("award", [])
            if awards:
                return f"Related Nobel Prizes found: {', '.join(awards)}"

        if "who" in query_lower and ("discover" in query_lower or "develop" in query_lower):
            people = by_type.get("person", [])
            if people:
                return f"Key figures: {', '.join(people)}"

        if "connect" in query_lower or "relation" in query_lower or "link" in query_lower:
            all_entities = []
            for entities in by_type.values():
                all_entities.extend(entities)
            return f"Connected entities: {', '.join(all_entities[:8])}"

        # Default: summarize what we found
        summary_parts = []
        for t, entities in by_type.items():
            summary_parts.append(f"{t}: {', '.join(entities[:3])}")
        return "Found: " + "; ".join(summary_parts) if summary_parts else "No relevant evidence found."


# ──────────────────────────────────────────────────────────────────────────────
# 5. Demo Queries
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Adaptive Knowledge Graph Exploration (ARK Pattern) Demo")
    print("Breadth (global search) + Depth (neighbor exploration)")
    print("=" * 70)

    # Build graph and tools
    graph = build_science_kg()
    print(f"\nKnowledge Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")

    tools = ARKTools(graph)
    agent = ARKAgent(tools, max_steps=10)

    # Demo queries showing different breadth-depth patterns
    queries = [
        "What Nobel Prize did Einstein receive and what was it for?",
        "How are Planck's constant and the photoelectric effect connected?",
        "Who contributed to quantum mechanics and what did they develop?",
    ]

    results = []
    for q in queries:
        result = agent.run(q)
        results.append(result)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for r in results:
        print(f"\n  Q: {r['query']}")
        print(f"  A: {r['answer']}")
        print(f"  Steps: {r['num_steps']} | Evidence entities: {r['evidence_count']}")
        tool_counts = defaultdict(int)
        for tool, _ in r["steps"]:
            tool_counts[tool] += 1
        print(f"  Tool mix: {dict(tool_counts)}")

    print(f"\n{'='*70}")
    print("Demo complete. The agent adaptively mixed breadth (global_search)")
    print("and depth (explore_neighbors) to answer each query.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
