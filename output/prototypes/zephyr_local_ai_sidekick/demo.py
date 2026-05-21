#!/usr/bin/env python3
"""Zephyr Local AI Sidekick — standalone demo (no server required).

Exercises every subsystem: LLM, RAG, MCP client, skills, self-healing.
Produces colourful terminal output so you can evaluate in 60 seconds.
"""

import json
import os
import sys
import random

# Ensure reproducible demo output
random.seed(42)

# Make runtime importable when run from repo root
sys.path.insert(0, os.path.dirname(__file__))

from runtime.llm import LocalLLM
from runtime.rag import RAGPipeline
from runtime.mcp_client import MCPClient
from runtime.skills import SkillRegistry
from runtime.self_heal import SelfHealingEngine, flaky_operation

BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"
RESET = "\033[0m"

DIVIDER = f"{DIM}{'─' * 60}{RESET}"


def section(title: str):
    print(f"\n{DIVIDER}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(DIVIDER)


def pp(obj):
    print(json.dumps(obj, indent=2, default=str))


def main():
    print(f"\n{BOLD}{'=' * 60}")
    print(f"   ZEPHYR  —  Local-First AI Sidekick Demo")
    print(f"{'=' * 60}{RESET}\n")

    # ── 1. Local LLM ────────────────────────────────────────────
    section("1. Local LLM Orchestration")
    llm = LocalLLM(model_name="mock-7b-q4")
    for prompt in ["Hello Zephyr!", "Summarize this document for me", "Review my Python code"]:
        r = llm.generate(prompt)
        print(f"  {YELLOW}>{RESET} {prompt}")
        print(f"    {DIM}{r['thinking']}{RESET}")
        print(f"    {GREEN}{r['response']}{RESET}")
        print(f"    {DIM}tokens: {r['tokens']}  (total: {r['total_tokens']}){RESET}")
        print()

    # ── 2. RAG Pipeline ─────────────────────────────────────────
    section("2. RAG — Retrieval-Augmented Generation")
    rag = RAGPipeline()

    # Ingest sample docs bundled with the demo
    sample_dir = os.path.join(os.path.dirname(__file__), "sample_docs")
    if os.path.isdir(sample_dir):
        count = rag.ingest_directory(sample_dir)
        print(f"  Ingested {GREEN}{count}{RESET} documents from sample_docs/")
    else:
        # Inline samples
        for title, body in [
            ("architecture.md", "Zephyr has three layers: React control room, FastAPI bridge, Python runtime."),
            ("rag_explained.md", "RAG retrieves relevant chunks from local documents to ground LLM responses."),
            ("mcp_overview.md", "MCP (Model Context Protocol) lets agents discover and invoke external tools."),
            ("skills.md", "Skills are modular capabilities: summarize, code review, research, writing."),
        ]:
            rag.ingest_text(title, body)
        print(f"  Ingested {GREEN}{len(rag.documents)}{RESET} inline sample documents")

    query = "How does Zephyr use RAG to ground responses?"
    results = rag.retrieve(query, top_k=2)
    print(f"\n  {YELLOW}Query:{RESET} {query}")
    for r in results:
        print(f"    {DIM}[{r['source']}]{RESET} {r['text'][:100]}")

    # RAG-augmented generation
    context = " | ".join(d["text"] for d in results)
    answer = llm.generate(query, context=context)
    print(f"\n  {GREEN}Answer:{RESET} {answer['response']}")

    # ── 3. MCP Client ───────────────────────────────────────────
    section("3. MCP Client — Tool Discovery & Invocation")
    mcp = MCPClient()
    for srv in ("filesystem", "web_search", "database"):
        status = mcp.connect(srv)
        print(f"  Connected to {CYAN}{srv}{RESET}: tools={status['tools']}")

    inv = mcp.invoke("filesystem", "read_file", {"path": "/tmp/notes.txt"})
    print(f"\n  Invoke filesystem.read_file:")
    pp(inv)

    inv2 = mcp.invoke("database", "query", {"sql": "SELECT * FROM users LIMIT 5"})
    print(f"\n  Invoke database.query:")
    pp(inv2)

    # ── 4. Skills ────────────────────────────────────────────────
    section("4. Skills System")
    reg = SkillRegistry()
    print(f"  Registered skills: {GREEN}{len(reg.skills)}{RESET}")
    for s in reg.list_skills():
        print(f"    {CYAN}{s['name']}{RESET}: {s['description']}  triggers={s['triggers']}")

    test_query = "Please summarize the project README"
    match = reg.match(test_query)
    if match:
        out = match.execute(test_query)
        print(f"\n  {YELLOW}Query:{RESET} {test_query}")
        print(f"  {GREEN}Matched skill:{RESET} {match.name}")
        pp(out)

    # ── 5. Self-Healing ─────────────────────────────────────────
    section("5. Self-Healing Agentic Workflow")
    healer = SelfHealingEngine(max_retries=3)
    steps = ["fetch_data", "parse_response", "update_index", "notify_user"]
    for step in steps:
        result = healer.run_step(step, flaky_operation, step)
        status_str = f"{GREEN}OK{RESET}" if result else f"{RED}EXHAUSTED{RESET}"
        print(f"  Step {CYAN}{step}{RESET}: {status_str}  result={result}")

    print(f"\n  Execution log ({len(healer.get_log())} entries):")
    for entry in healer.get_log():
        color = GREEN if entry["status"] == "success" else (RED if "fail" in entry["status"] else YELLOW)
        print(f"    {color}{entry['status']:>10}{RESET}  {entry['step']} (attempt {entry['attempt']})")

    # ── Summary ─────────────────────────────────────────────────
    print(f"\n{BOLD}{'=' * 60}")
    print(f"   Demo complete — all 5 subsystems exercised.")
    print(f"   Total tokens consumed: {llm.total_tokens}")
    print(f"   RAG documents indexed: {len(rag.documents)}")
    print(f"   MCP servers connected: {len(mcp.connected_servers)}")
    print(f"   Skills available:      {len(reg.skills)}")
    print(f"   Self-heal log entries: {len(healer.get_log())}")
    print(f"{'=' * 60}{RESET}\n")


if __name__ == "__main__":
    main()
