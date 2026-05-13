#!/usr/bin/env python3
"""
cord_demo.py — Local simulator for Cord distributed agent fabric.

Demonstrates Cord's core concepts:
  - Service registration (LLM backends, MCP servers, AI agents)
  - Semantic discovery via natural-language queries
  - Peer mesh topology and service routing

Uses TF-IDF cosine similarity for semantic matching (no external API keys).
"""

import json
import math
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# ── Data models ──────────────────────────────────────────────────────────────

@dataclass
class Service:
    name: str
    stype: str          # "mcp-server" | "llm-backend" | "agent"
    endpoint: str
    description: str
    peer: str = "local"
    registered_at: float = field(default_factory=time.time)


@dataclass
class Peer:
    address: str
    name: str
    services: List[str] = field(default_factory=list)


# ── TF-IDF semantic search (no API keys needed) ─────────────────────────────

def tokenize(text: str) -> List[str]:
    """Lowercase, strip punctuation, split into tokens."""
    return re.findall(r"[a-z0-9]+", text.lower())


def tf(tokens: List[str]) -> dict:
    counts = Counter(tokens)
    total = len(tokens)
    return {t: c / total for t, c in counts.items()}


def idf(corpus_tokens: List[List[str]]) -> dict:
    n = len(corpus_tokens)
    doc_freq: Counter = Counter()
    for tokens in corpus_tokens:
        doc_freq.update(set(tokens))
    return {t: math.log((1 + n) / (1 + df)) + 1 for t, df in doc_freq.items()}


def tfidf_vector(tokens: List[str], idf_map: dict) -> dict:
    tf_map = tf(tokens)
    return {t: tf_map[t] * idf_map.get(t, 1.0) for t in tf_map}


def cosine_sim(v1: dict, v2: dict) -> float:
    keys = set(v1) | set(v2)
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in keys)
    m1 = math.sqrt(sum(x ** 2 for x in v1.values())) or 1e-9
    m2 = math.sqrt(sum(x ** 2 for x in v2.values())) or 1e-9
    return dot / (m1 * m2)


# ── Cord Fabric Simulator ───────────────────────────────────────────────────

class CordFabric:
    """Simulates a local Cord mesh with registration and semantic discovery."""

    def __init__(self):
        self.services: List[Service] = []
        self.peers: List[Peer] = []

    # ── Registration ─────────────────────────────────────────────────────

    def register(self, name: str, stype: str, endpoint: str,
                 description: str, peer: str = "local") -> Service:
        svc = Service(name=name, stype=stype, endpoint=endpoint,
                      description=description, peer=peer)
        self.services.append(svc)
        return svc

    # ── Peer mesh ────────────────────────────────────────────────────────

    def add_peer(self, address: str, name: str,
                 service_names: Optional[List[str]] = None) -> Peer:
        p = Peer(address=address, name=name,
                 services=service_names or [])
        self.peers.append(p)
        return p

    # ── Semantic discovery ───────────────────────────────────────────────

    def discover(self, query: str, top_k: int = 3) -> List[dict]:
        if not self.services:
            return []

        corpus_tokens = [tokenize(s.description) for s in self.services]
        query_tokens = tokenize(query)
        all_tokens = corpus_tokens + [query_tokens]

        idf_map = idf(all_tokens)
        query_vec = tfidf_vector(query_tokens, idf_map)

        scored = []
        for i, svc in enumerate(self.services):
            doc_vec = tfidf_vector(corpus_tokens[i], idf_map)
            score = cosine_sim(query_vec, doc_vec)
            scored.append({"service": svc, "score": round(score, 4)})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    # ── List all ─────────────────────────────────────────────────────────

    def list_services(self) -> List[dict]:
        return [asdict(s) for s in self.services]

    def list_peers(self) -> List[dict]:
        return [asdict(p) for p in self.peers]


# ── Pretty output helpers ────────────────────────────────────────────────────

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


def banner(text: str):
    width = 64
    print(f"\n{CYAN}{'═' * width}")
    print(f"  {BOLD}{text}{RESET}{CYAN}")
    print(f"{'═' * width}{RESET}")


def section(text: str):
    print(f"\n{YELLOW}▸ {text}{RESET}")


def show_service(svc, score=None):
    score_str = f"  {DIM}(score: {score}){RESET}" if score is not None else ""
    print(f"  {GREEN}●{RESET} {BOLD}{svc.name}{RESET} [{svc.stype}]{score_str}")
    print(f"    endpoint:    {svc.endpoint}")
    print(f"    peer:        {svc.peer}")
    print(f"    description: {svc.description}")


# ── Demo scenario ────────────────────────────────────────────────────────────

def run_demo():
    banner("Cord Agent Fabric — Local Simulator")
    print(f"{DIM}Simulating a multi-machine agent mesh with semantic discovery.{RESET}")
    print(f"{DIM}No external API keys required — uses TF-IDF cosine similarity.{RESET}")

    fabric = CordFabric()

    # ── Step 1: Register services ────────────────────────────────────────
    section("Step 1 — Registering services across the mesh")

    registrations = [
        ("fs-tools-mcp", "mcp-server", "http://dev-box:3001",
         "MCP server providing file system read write and directory listing tools",
         "dev-box"),
        ("git-mcp", "mcp-server", "http://dev-box:3002",
         "MCP server for git operations including commit diff branch and merge",
         "dev-box"),
        ("codegen-llama", "llm-backend", "http://gpu-node-1:8080",
         "LLaMA 3 70B model fine-tuned for code generation and completion with GPU acceleration",
         "gpu-node-1"),
        ("embedding-svc", "llm-backend", "http://gpu-node-2:8081",
         "Text embedding model for semantic search and document similarity",
         "gpu-node-2"),
        ("db-agent", "agent", "http://ops-node:9000",
         "Autonomous agent that handles PostgreSQL database queries migrations and schema management",
         "ops-node"),
        ("deploy-agent", "agent", "http://ops-node:9001",
         "CI CD deployment agent managing Kubernetes rollouts and canary releases",
         "ops-node"),
        ("research-agent", "agent", "http://analyst-box:9010",
         "Deep research agent that searches the web summarizes papers and extracts key findings",
         "analyst-box"),
        ("image-gen", "llm-backend", "http://gpu-node-1:8082",
         "Stable Diffusion XL model for image generation and creative visual content",
         "gpu-node-1"),
    ]

    for name, stype, endpoint, desc, peer in registrations:
        svc = fabric.register(name, stype, endpoint, desc, peer)
        print(f"  {GREEN}+{RESET} registered {BOLD}{name}{RESET} ({stype}) on {peer}")
        time.sleep(0.08)

    # ── Step 2: Add peers ────────────────────────────────────────────────
    section("Step 2 — Joining peer mesh")

    peers_data = [
        ("192.168.1.10:7946", "dev-box", ["fs-tools-mcp", "git-mcp"]),
        ("192.168.1.20:7946", "gpu-node-1", ["codegen-llama", "image-gen"]),
        ("192.168.1.21:7946", "gpu-node-2", ["embedding-svc"]),
        ("192.168.1.30:7946", "ops-node", ["db-agent", "deploy-agent"]),
        ("192.168.1.40:7946", "analyst-box", ["research-agent"]),
    ]

    for addr, name, svcs in peers_data:
        fabric.add_peer(addr, name, svcs)
        print(f"  {GREEN}↔{RESET} peer {BOLD}{name}{RESET} ({addr}) — {len(svcs)} service(s)")
        time.sleep(0.05)

    print(f"\n  Mesh topology: {len(fabric.peers)} peers, {len(fabric.services)} services")

    # ── Step 3: Semantic discovery ───────────────────────────────────────
    section("Step 3 — Semantic discovery queries")

    queries = [
        "I need a tool that can read and write files on the filesystem",
        "code generation model with GPU acceleration",
        "agent that handles database operations and schema changes",
        "deploy my application to Kubernetes with canary rollout",
        "find research papers and summarize findings",
    ]

    for query in queries:
        print(f"\n  {BOLD}Query:{RESET} \"{query}\"")
        results = fabric.discover(query, top_k=3)
        for i, r in enumerate(results):
            svc = r["service"]
            score = r["score"]
            bar_len = int(score * 30)
            bar = "█" * bar_len + "░" * (30 - bar_len)
            print(f"    {i+1}. {BOLD}{svc.name}{RESET} [{svc.stype}] on {svc.peer}")
            print(f"       {DIM}{bar} {score:.2%}{RESET}")
        time.sleep(0.1)

    # ── Step 4: Full mesh listing ────────────────────────────────────────
    section("Step 4 — Full mesh service listing")

    by_type: dict = {}
    for svc in fabric.services:
        by_type.setdefault(svc.stype, []).append(svc)

    for stype, svcs in sorted(by_type.items()):
        print(f"\n  {CYAN}[{stype}]{RESET} — {len(svcs)} registered")
        for svc in svcs:
            show_service(svc)

    # ── Step 5: Export mesh state ────────────────────────────────────────
    section("Step 5 — Exporting mesh state to cord_mesh_state.json")

    state = {
        "mesh": {
            "peers": fabric.list_peers(),
            "services": fabric.list_services(),
            "total_peers": len(fabric.peers),
            "total_services": len(fabric.services),
        }
    }
    out_path = "cord_mesh_state.json"
    with open(out_path, "w") as f:
        json.dump(state, f, indent=2, default=str)
    print(f"  Wrote {out_path} ({len(fabric.services)} services, {len(fabric.peers)} peers)")

    # ── Done ─────────────────────────────────────────────────────────────
    banner("Demo complete")
    print(f"  {GREEN}✓{RESET} Registered {len(fabric.services)} services across {len(fabric.peers)} peers")
    print(f"  {GREEN}✓{RESET} Ran {len(queries)} semantic discovery queries")
    print(f"  {GREEN}✓{RESET} Exported mesh state to {out_path}")
    print(f"\n  {DIM}This is a local simulation. For the real Cord fabric,")
    print(f"  see https://github.com/fosenai/cord{RESET}\n")


if __name__ == "__main__":
    run_demo()
