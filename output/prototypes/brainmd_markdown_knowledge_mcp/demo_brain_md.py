#!/usr/bin/env python3
"""
demo_brain_md.py — Simulates the brain.md MCP server's core capabilities.

This demo showcases what brain.md does WITHOUT requiring Bun or a real install:
  1. Creates a sample markdown knowledge base on disk
  2. Simulates the 16 MCP tools (create, read, update, delete, search, list, tag, etc.)
  3. Demonstrates semantic search via TF-IDF similarity (stands in for LanceDB vectors)
  4. Shows per-folder permission enforcement
  5. Outputs results as if an MCP client (Claude Code) were calling the server

Run: python3 demo_brain_md.py
"""

import json
import math
import os
import re
import shutil
import sys
import textwrap
from collections import Counter
from datetime import datetime
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────────────────

DEMO_ROOT = Path(__file__).parent / "demo_vault"
PERMISSIONS = {
    "projects": {"read": True, "write": True},
    "journal": {"read": True, "write": True},
    "archive": {"read": True, "write": False},   # read-only folder
    "private": {"read": False, "write": False},   # blocked folder
}

# ─── Colour helpers (ANSI) ────────────────────────────────────────────────────

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def banner(text):
    width = 68
    print(f"\n{BOLD}{CYAN}{'=' * width}")
    print(f"  {text}")
    print(f"{'=' * width}{RESET}\n")


def tool_call(name, params=None):
    """Pretty-print an MCP tool invocation."""
    p = json.dumps(params, indent=2) if params else "{}"
    print(f"{DIM}───── MCP Tool Call ─────{RESET}")
    print(f"{BOLD}{YELLOW}tool:{RESET} {name}")
    print(f"{BOLD}{YELLOW}params:{RESET} {p}")


def tool_result(data, success=True):
    """Pretty-print an MCP tool result."""
    tag = f"{GREEN}OK{RESET}" if success else f"{RED}ERR{RESET}"
    print(f"{BOLD}{YELLOW}result [{tag}{BOLD}{YELLOW}]:{RESET}")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str))
    else:
        print(data)
    print()


# ─── Tiny TF-IDF Semantic Search ─────────────────────────────────────────────

def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def tf_idf_index(docs):
    """Build a minimal TF-IDF index. docs = {path: text}."""
    n = len(docs)
    df = Counter()
    tf = {}
    for path, text in docs.items():
        tokens = tokenize(text)
        tf[path] = Counter(tokens)
        for t in set(tokens):
            df[t] += 1
    idf = {t: math.log(n / (1 + c)) for t, c in df.items()}
    return tf, idf


def search(query, tf, idf, docs, top_k=3):
    q_tokens = tokenize(query)
    scores = {}
    for path in docs:
        score = 0.0
        total = sum(tf[path].values()) or 1
        for t in q_tokens:
            if t in tf[path]:
                score += (tf[path][t] / total) * idf.get(t, 0)
        if score > 0:
            scores[path] = score
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
    return [(str(p), round(s, 4)) for p, s in ranked]


# ─── Permission Check ────────────────────────────────────────────────────────

def check_perm(rel_path, action="read"):
    folder = Path(rel_path).parts[0] if Path(rel_path).parts else ""
    perms = PERMISSIONS.get(folder, {"read": True, "write": True})
    return perms.get(action, True)


# ─── Sample Notes ────────────────────────────────────────────────────────────

SAMPLE_NOTES = {
    "projects/api-design.md": textwrap.dedent("""\
        ---
        title: API Design Decisions
        tags: [architecture, api, rest]
        created: 2026-01-15
        ---
        # API Design Decisions

        We chose REST over GraphQL for the public API because:
        - Simpler caching at the CDN layer
        - Better tooling for rate limiting
        - Team familiarity

        The internal service mesh uses gRPC for performance.
    """),
    "projects/deployment-checklist.md": textwrap.dedent("""\
        ---
        title: Deployment Checklist
        tags: [devops, deployment, ci-cd]
        created: 2026-02-10
        ---
        # Deployment Checklist

        1. Run full test suite
        2. Check migration status
        3. Update environment variables
        4. Deploy to staging first
        5. Smoke test critical paths
        6. Promote to production
        7. Monitor error rates for 30 min
    """),
    "projects/vector-search-notes.md": textwrap.dedent("""\
        ---
        title: Vector Search Implementation
        tags: [ai, embeddings, lancedb]
        created: 2026-03-01
        ---
        # Vector Search Implementation

        Using LanceDB for local vector storage. Embeddings generated
        with a lightweight model at index time. Supports semantic
        similarity queries across all markdown notes.

        Key advantage: no external API calls needed for search —
        everything runs locally with sub-100ms latency.
    """),
    "journal/2026-05-28.md": textwrap.dedent("""\
        ---
        title: Daily Journal
        tags: [journal, daily]
        created: 2026-05-28
        ---
        # 2026-05-28

        Explored brain.md as a second-brain tool for Claude Code.
        The MCP integration is seamless — 16 tools available out of
        the box. Semantic search over notes is surprisingly fast.
    """),
    "archive/old-meeting-notes.md": textwrap.dedent("""\
        ---
        title: Q1 Meeting Notes
        tags: [meetings, archive]
        created: 2026-01-05
        ---
        # Q1 Meeting Notes

        Archived meeting notes from Q1. Read-only reference material.
    """),
    "private/credentials.md": textwrap.dedent("""\
        ---
        title: Credentials
        tags: [private, secrets]
        created: 2026-01-01
        ---
        # Credentials

        This file should NOT be accessible via the MCP server.
    """),
}


# ─── Demo Runner ─────────────────────────────────────────────────────────────

def setup_vault():
    if DEMO_ROOT.exists():
        shutil.rmtree(DEMO_ROOT)
    for rel, content in SAMPLE_NOTES.items():
        p = DEMO_ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    return {rel: content for rel, content in SAMPLE_NOTES.items()}


def run_demo():
    print(f"{BOLD}{CYAN}")
    print(r"   _               _                       _ ")
    print(r"  | |__  _ __ __ _(_)_ __    _ __ ___   __| |")
    print(r"  | '_ \| '__/ _` | | '_ \  | '_ ` _ \ / _` |")
    print(r"  | |_) | | | (_| | | | | |_| | | | | | (_| |")
    print(r"  |_.__/|_|  \__,_|_|_| |_(_)_| |_| |_|\__,_|")
    print(f"{RESET}")
    print(f"  {DIM}Local-first markdown knowledge base + MCP server{RESET}")
    print(f"  {DIM}Demo mode — simulating 16 MCP tools{RESET}\n")

    docs = setup_vault()
    tf, idf = tf_idf_index(docs)

    # ── 1. List notes ─────────────────────────────────────────────────────
    banner("1. Tool: brain_list_notes — List all accessible notes")
    tool_call("brain_list_notes", {"folder": "/"})
    accessible = [p for p in docs if check_perm(p, "read")]
    blocked = [p for p in docs if not check_perm(p, "read")]
    tool_result({
        "notes": accessible,
        "count": len(accessible),
        "blocked_by_permissions": len(blocked),
    })

    # ── 2. Read a note ────────────────────────────────────────────────────
    banner("2. Tool: brain_read_note — Read a specific note")
    target = "projects/api-design.md"
    tool_call("brain_read_note", {"path": target})
    tool_result({"path": target, "content": docs[target].strip()})

    # ── 3. Semantic search ────────────────────────────────────────────────
    banner("3. Tool: brain_search — Semantic search across notes")
    query = "vector embeddings local search"
    tool_call("brain_search", {"query": query, "top_k": 3})
    results = search(query, tf, idf, {p: t for p, t in docs.items() if check_perm(p)})
    tool_result({
        "query": query,
        "results": [{"path": p, "score": s} for p, s in results],
    })

    # ── 4. Create a note ──────────────────────────────────────────────────
    banner("4. Tool: brain_create_note — Create a new note")
    new_path = "projects/new-feature-spec.md"
    new_content = textwrap.dedent("""\
        ---
        title: New Feature Spec
        tags: [feature, spec]
        created: 2026-05-29
        ---
        # New Feature Spec

        Claude created this note via brain.md MCP.
        Demonstrates write access through the MCP tool interface.
    """)
    tool_call("brain_create_note", {"path": new_path, "content": "(markdown content)"})
    (DEMO_ROOT / new_path).parent.mkdir(parents=True, exist_ok=True)
    (DEMO_ROOT / new_path).write_text(new_content)
    tool_result({"created": new_path, "size_bytes": len(new_content)})

    # ── 5. Update a note ──────────────────────────────────────────────────
    banner("5. Tool: brain_update_note — Append to an existing note")
    update_path = "journal/2026-05-28.md"
    append_text = "\n\n## Evening Update\nFinished evaluating brain.md. Decision: adopt it."
    tool_call("brain_update_note", {"path": update_path, "append": append_text.strip()})
    updated = docs[update_path] + append_text
    (DEMO_ROOT / update_path).write_text(updated)
    tool_result({"updated": update_path, "new_size_bytes": len(updated)})

    # ── 6. Tag search ─────────────────────────────────────────────────────
    banner("6. Tool: brain_search_by_tag — Find notes by tag")
    tool_call("brain_search_by_tag", {"tag": "architecture"})
    tagged = [p for p, t in docs.items() if "architecture" in t and check_perm(p)]
    tool_result({"tag": "architecture", "matches": tagged})

    # ── 7. Permission denied ──────────────────────────────────────────────
    banner("7. Permission enforcement — blocked folder")
    tool_call("brain_read_note", {"path": "private/credentials.md"})
    tool_result({
        "error": "PermissionDenied",
        "message": "Folder 'private' is not readable by this MCP client.",
    }, success=False)

    # ── 8. Write to read-only folder ──────────────────────────────────────
    banner("8. Permission enforcement — read-only folder")
    tool_call("brain_create_note", {"path": "archive/new-note.md", "content": "..."})
    tool_result({
        "error": "PermissionDenied",
        "message": "Folder 'archive' is read-only. Write access denied.",
    }, success=False)

    # ── 9. Delete a note ──────────────────────────────────────────────────
    banner("9. Tool: brain_delete_note — Delete a note")
    del_path = "projects/new-feature-spec.md"
    tool_call("brain_delete_note", {"path": del_path})
    (DEMO_ROOT / del_path).unlink(missing_ok=True)
    tool_result({"deleted": del_path})

    # ── 10. Resource: note index ──────────────────────────────────────────
    banner("10. MCP Resource: brain://index — Full note index")
    tool_call("brain_resource_read", {"uri": "brain://index"})
    index = []
    for p in sorted(docs.keys()):
        if check_perm(p):
            title_match = re.search(r"title:\s*(.+)", docs[p])
            title = title_match.group(1) if title_match else p
            tags_match = re.search(r"tags:\s*\[(.+?)\]", docs[p])
            tags = [t.strip() for t in tags_match.group(1).split(",")] if tags_match else []
            index.append({"path": p, "title": title, "tags": tags})
    tool_result({"resource": "brain://index", "notes": index})

    # ── Summary ───────────────────────────────────────────────────────────
    banner("Demo Complete")
    print(f"  {GREEN}Demonstrated 8 of brain.md's 16 MCP tools + 1 resource:{RESET}")
    print(f"    brain_list_notes      brain_read_note")
    print(f"    brain_search          brain_create_note")
    print(f"    brain_update_note     brain_search_by_tag")
    print(f"    brain_delete_note     brain_resource_read")
    print()
    print(f"  {GREEN}Also demonstrated:{RESET}")
    print(f"    Per-folder permission enforcement (read-only, blocked)")
    print(f"    Semantic search via TF-IDF (simulates LanceDB vectors)")
    print()
    print(f"  {DIM}Vault created at: {DEMO_ROOT}{RESET}")
    print(f"  {DIM}See HOW_TO_USE.md to install the real brain.md MCP server.{RESET}")
    print()


if __name__ == "__main__":
    run_demo()
