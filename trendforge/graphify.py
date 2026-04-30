"""Graphify — build a knowledge graph of TrendForge data.

Three outputs:
  - output/graph.md         Mermaid diagram (renders natively on GitHub)
                            Shows pinned items + their tags + skills +
                            prototypes + Adroitec projects (Pitchbot,
                            ARIA, smart_glasses, TrendForge).
  - output/graph.json       Full adjacency JSON for external graph tools
                            (Neo4j, vis.js, Obsidian Canvas, etc.)
  - output/graph.html       Interactive vis.js explorer — open in a
                            browser to pan/zoom the full graph.

Node types:
  - item       (TrendForge ingest item)
  - tag        (topical tag attached by tagger.py)
  - skill      (generated SKILL.md folder)
  - prototype  (generated demo)
  - project    (PitchBot / ARIA / smart_glasses / TrendForge)
  - source     (RSS / GitHub / HN / YouTube / awesome_list)

Edges:
  item -[:HAS_TAG]-> tag
  item -[:FROM_SOURCE]-> source
  item -[:RELEVANT_TO]-> project
  skill -[:GENERATED_FROM]-> item
  prototype -[:DEMOS]-> skill
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from trendforge import store
from trendforge.config_loader import load_interests

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
GRAPH_MD = ROOT / "output" / "graph.md"
GRAPH_JSON = ROOT / "output" / "graph.json"
GRAPH_HTML = ROOT / "output" / "graph.html"

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]+")


def _project_for(item: dict, projects: dict[str, str]) -> list[str]:
    """Heuristic project relevance: title text + tags hits."""
    text = (item.get("title") or "").lower()
    tags = item.get("tags") or []
    if isinstance(tags, str):
        try:
            tags = json.loads(tags)
        except json.JSONDecodeError:
            tags = []
    blob = text + " " + " ".join(tags).lower()
    hits: list[str] = []
    keys = {
        "pitchbot": ["sales", "lead", "outreach", "crm", "b2b", "cold-email", "rag"],
        "aria": ["voice", "tts", "stt", "interview", "audio", "vlsi", "pipecat", "livekit"],
        "smart_glasses": ["risc-v", "soc", "npu", "vision", "edge", "embedded"],
        "trendforge": ["rss", "ingest", "agent", "research", "skill", "mcp"],
    }
    for proj, kws in keys.items():
        if proj not in projects:
            continue
        if any(k in blob for k in kws):
            hits.append(proj)
    return hits


def build_graph(db_path=None, max_items: int = 200) -> dict:
    """Build a node-and-edge dict from the DB."""
    db = db_path or store.DB_PATH
    interests = load_interests()
    projects = interests.get("active_projects", {}) or {}

    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(node_id: str, **attrs) -> None:
        if node_id in nodes:
            nodes[node_id].update({k: v for k, v in attrs.items() if v is not None})
        else:
            nodes[node_id] = {"id": node_id, **attrs}

    # Project nodes
    for proj, desc in projects.items():
        add_node(f"project:{proj}", type="project", label=proj, description=desc)

    with store.get_conn(db) as conn:
        # Pinned items first (always include), then top by score
        pinned = conn.execute(
            "SELECT * FROM items WHERE pinned = 1 ORDER BY id"
        ).fetchall()
        ranked = conn.execute(
            "SELECT * FROM items WHERE pinned = 0 AND score IS NOT NULL "
            "ORDER BY score DESC LIMIT ?",
            (max_items,),
        ).fetchall()
        rows = list(pinned) + list(ranked)

        for r in rows:
            d = store.row_to_dict(r) or {}
            iid = f"item:{d['id']}"
            add_node(
                iid, type="item",
                label=(d.get("title") or "")[:80],
                url=d.get("url"),
                source=d.get("source"),
                score=d.get("score"),
                pinned=bool(d.get("pinned")),
                pitch=d.get("business_pitch"),
                notes=d.get("notes"),
            )

            # Source edge
            src = d.get("source")
            if src:
                add_node(f"source:{src}", type="source", label=src)
                edges.append({"from": iid, "to": f"source:{src}", "rel": "FROM_SOURCE"})

            # Tag edges
            tags = d.get("tags") or []
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except json.JSONDecodeError:
                    tags = []
            for t in tags[:8]:
                tid = f"tag:{t}"
                add_node(tid, type="tag", label=t)
                edges.append({"from": iid, "to": tid, "rel": "HAS_TAG"})

            # Project relevance
            for proj in _project_for(d, projects):
                edges.append({"from": iid, "to": f"project:{proj}", "rel": "RELEVANT_TO"})

        # Skills + prototypes
        skill_rows = conn.execute("SELECT * FROM skills").fetchall()
        for sr in skill_rows:
            sid = f"skill:{sr['id']}"
            add_node(sid, type="skill", label=sr["skill_name"], path=sr["skill_path"])
            edges.append({"from": sid, "to": f"item:{sr['item_id']}", "rel": "GENERATED_FROM"})

        proto_rows = conn.execute("SELECT * FROM prototypes").fetchall()
        for pr in proto_rows:
            pid = f"prototype:{pr['id']}"
            add_node(
                pid, type="prototype",
                label=Path(pr["repo_path"]).name,
                runs_ok=bool(pr["runs_successfully"]),
                deck=pr["deck_path"],
            )
            edges.append({"from": pid, "to": f"skill:{pr['skill_id']}", "rel": "DEMOS"})

    return {"nodes": list(nodes.values()), "edges": edges}


# ---------- Mermaid emitter ----------

def _esc(s: str) -> str:
    """Mermaid-safe label."""
    return (s or "").replace('"', "'").replace("\n", " ")[:60]


def emit_mermaid(graph: dict) -> str:
    """Compact Mermaid graph showing pinned items + their tags + projects.

    The full graph would be too dense for Mermaid; we surface the part
    Anirudh cares about most: backlog + their cross-references.
    """
    pinned = [n for n in graph["nodes"] if n["type"] == "item" and n.get("pinned")]
    pinned_ids = {n["id"] for n in pinned}
    if not pinned:
        return "## Knowledge Graph\n\n_(no pinned items yet — pin some via `scripts/seed_backlog.py`)_\n"

    # Edges that touch pinned items
    relevant_edges = [
        e for e in graph["edges"]
        if e["from"] in pinned_ids or e["to"] in pinned_ids
    ]
    relevant_node_ids = pinned_ids.copy()
    for e in relevant_edges:
        relevant_node_ids.add(e["from"])
        relevant_node_ids.add(e["to"])

    # Also include any project / source / tag nodes referenced
    nodes_by_id = {n["id"]: n for n in graph["nodes"]}

    lines = [
        "## Knowledge Graph — Backlog View",
        "",
        "Auto-generated from `data/trendforge.db`. Re-runs nightly.",
        "",
        "```mermaid",
        "graph LR",
        "  classDef item fill:#fde68a,stroke:#92400e,color:#000",
        "  classDef pin fill:#fca5a5,stroke:#7f1d1d,color:#000,stroke-width:3px",
        "  classDef tag fill:#bfdbfe,stroke:#1e3a8a,color:#000",
        "  classDef proj fill:#86efac,stroke:#14532d,color:#000",
        "  classDef src fill:#e9d5ff,stroke:#581c87,color:#000",
        "  classDef skill fill:#fed7aa,stroke:#7c2d12,color:#000",
        "  classDef proto fill:#fcd34d,stroke:#78350f,color:#000",
        "",
    ]

    def node_decl(n: dict) -> tuple[str, str]:
        nid_clean = re.sub(r"[^A-Za-z0-9]", "_", n["id"])
        lbl = _esc(n.get("label", n["id"]))
        cls_map = {
            "item": "item", "tag": "tag", "project": "proj",
            "source": "src", "skill": "skill", "prototype": "proto",
        }
        cls = cls_map.get(n["type"], "item")
        if n.get("pinned"):
            cls = "pin"
        return nid_clean, f'  {nid_clean}["{lbl}"]:::{cls}'

    decls: dict[str, str] = {}
    for nid in relevant_node_ids:
        n = nodes_by_id.get(nid)
        if not n:
            continue
        clean, decl = node_decl(n)
        decls[nid] = clean
        lines.append(decl)

    lines.append("")
    seen_pairs: set[tuple[str, str, str]] = set()
    for e in relevant_edges:
        a = decls.get(e["from"])
        b = decls.get(e["to"])
        if not a or not b:
            continue
        key = (a, b, e["rel"])
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        rel_label = e["rel"].lower().replace("_", " ")
        lines.append(f"  {a} -- \"{rel_label}\" --> {b}")

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# ---------- HTML (vis.js) emitter ----------

VIS_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=utf-8>
<title>TrendForge Knowledge Graph</title>
<script src=https://unpkg.com/vis-network/standalone/umd/vis-network.min.js></script>
<style>
  body { margin: 0; font-family: -apple-system, system-ui, sans-serif; background: #0b1020; color: #e5e7eb; }
  #toolbar { padding: 8px 12px; border-bottom: 1px solid #1f2937; display: flex; gap: 12px; align-items: center; }
  #toolbar input { background: #1f2937; color: #fff; border: 1px solid #374151; padding: 6px 8px; border-radius: 4px; }
  #network { width: 100vw; height: calc(100vh - 56px); }
  .legend { font-size: 12px; }
  .legend span { display: inline-block; padding: 2px 8px; margin: 0 4px; border-radius: 3px; color: #000; }
</style>
</head>
<body>
<div id=toolbar>
  <strong>TrendForge</strong>
  <input id=q placeholder="filter by label..." />
  <span class=legend>
    <span style="background:#fde68a">item</span>
    <span style="background:#fca5a5">pinned</span>
    <span style="background:#bfdbfe">tag</span>
    <span style="background:#86efac">project</span>
    <span style="background:#e9d5ff">source</span>
    <span style="background:#fed7aa">skill</span>
    <span style="background:#fcd34d">prototype</span>
  </span>
</div>
<div id=network></div>
<script>
const DATA = __GRAPH_JSON__;
const COLORS = { item: '#fde68a', tag: '#bfdbfe', project: '#86efac', source: '#e9d5ff', skill: '#fed7aa', prototype: '#fcd34d' };
const visNodes = DATA.nodes.map(n => ({
  id: n.id,
  label: (n.label || n.id).slice(0, 40),
  color: n.pinned ? '#fca5a5' : (COLORS[n.type] || '#fde68a'),
  borderWidth: n.pinned ? 3 : 1,
  title: (n.url || '') + '\\n' + (n.pitch || n.notes || ''),
  shape: n.type === 'project' ? 'box' : (n.type === 'tag' ? 'ellipse' : 'dot'),
  value: n.pinned ? 30 : 10,
}));
const visEdges = DATA.edges.map(e => ({
  from: e.from, to: e.to, label: e.rel.toLowerCase(),
  arrows: 'to', color: { color: '#374151' }, font: { size: 9, color: '#9ca3af', strokeWidth: 0 }
}));
const network = new vis.Network(document.getElementById('network'),
  { nodes: new vis.DataSet(visNodes), edges: new vis.DataSet(visEdges) },
  { physics: { stabilization: { iterations: 200 } },
    nodes: { font: { color: '#e5e7eb', size: 12 } } });
network.on('click', p => {
  if (p.nodes.length) {
    const n = DATA.nodes.find(x => x.id === p.nodes[0]);
    if (n && n.url) window.open(n.url, '_blank');
  }
});
document.getElementById('q').addEventListener('input', ev => {
  const q = ev.target.value.toLowerCase();
  if (!q) { network.body.data.nodes.update(visNodes); return; }
  const matched = visNodes.filter(n => (n.label || '').toLowerCase().includes(q));
  network.selectNodes(matched.map(n => n.id));
});
</script>
</body>
</html>
"""


def emit_html(graph: dict) -> str:
    return VIS_HTML_TEMPLATE.replace(
        "__GRAPH_JSON__", json.dumps(graph, ensure_ascii=False)
    )


def write_all(db_path=None) -> dict[str, Path]:
    graph = build_graph(db_path=db_path)
    GRAPH_MD.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_MD.write_text(emit_mermaid(graph), encoding="utf-8")
    GRAPH_JSON.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    GRAPH_HTML.write_text(emit_html(graph), encoding="utf-8")
    log.info("Graph: %d nodes, %d edges", len(graph["nodes"]), len(graph["edges"]))
    return {"md": GRAPH_MD, "json": GRAPH_JSON, "html": GRAPH_HTML}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    paths = write_all()
    for k, v in paths.items():
        print(f"{k}: {v}")
