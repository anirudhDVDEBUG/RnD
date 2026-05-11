#!/usr/bin/env python3
"""
Deliberate Wheel Reinvention — a structured learning-through-reimplementation planner.

Given a domain, suggests the best "wheels" to reinvent, scopes a minimal version,
and generates a concrete learning plan with checkpoints.
"""

import json
import textwrap
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Domain knowledge base ────────────────────────────────────────────────────

DOMAINS: dict[str, list[dict]] = {
    "databases": [
        {
            "wheel": "B-tree index",
            "effort_days": 3,
            "essential_behaviors": [
                "Insert keys while maintaining sorted order",
                "Split nodes when they exceed capacity",
                "Search for a key in O(log n) time",
            ],
            "leave_out": [
                "Deletion / rebalancing",
                "Concurrency control",
                "Disk page management",
            ],
            "done_condition": "Can insert 10k random integers and retrieve any one in < 20 comparisons",
            "transferable_principles": [
                "Balanced tree data structures",
                "Amortized splitting / growth",
                "How indexes make queries fast",
            ],
            "next_wheels": ["simple query parser", "WAL journaling"],
        },
        {
            "wheel": "Simple query parser",
            "effort_days": 2,
            "essential_behaviors": [
                "Tokenize SQL-like SELECT/WHERE statements",
                "Build an AST from tokens",
                "Evaluate the AST against in-memory rows",
            ],
            "leave_out": [
                "JOINs and subqueries",
                "Query optimization",
                "Type coercion",
            ],
            "done_condition": "Can run SELECT name FROM users WHERE age > 30 on a list of dicts",
            "transferable_principles": [
                "Lexing and parsing fundamentals",
                "AST construction",
                "Declarative → imperative translation",
            ],
            "next_wheels": ["B-tree index", "WAL journaling"],
        },
        {
            "wheel": "WAL journaling",
            "effort_days": 4,
            "essential_behaviors": [
                "Append writes to a log file before modifying data",
                "Replay the log to recover after a crash",
                "Checkpoint: flush log to main data file",
            ],
            "leave_out": [
                "Concurrent writers",
                "Compression",
                "Partial page writes",
            ],
            "done_condition": "Kill the process mid-write, restart, and verify no data loss",
            "transferable_principles": [
                "Write-ahead logging pattern",
                "Crash recovery",
                "Durability guarantees",
            ],
            "next_wheels": ["B-tree index", "simple query parser"],
        },
    ],
    "networking": [
        {
            "wheel": "HTTP/1.1 server",
            "effort_days": 2,
            "essential_behaviors": [
                "Parse request line and headers from a TCP socket",
                "Route GET requests to handler functions",
                "Send properly-formatted HTTP responses with status codes",
            ],
            "leave_out": [
                "Keep-alive / pipelining",
                "Chunked transfer encoding",
                "TLS",
            ],
            "done_condition": "curl http://localhost:8080/hello returns a JSON body",
            "transferable_principles": [
                "Request/response protocol design",
                "Socket programming basics",
                "Header parsing and serialization",
            ],
            "next_wheels": ["DNS resolver", "TCP over UDP"],
        },
        {
            "wheel": "DNS resolver",
            "effort_days": 2,
            "essential_behaviors": [
                "Construct a DNS query packet (binary encoding)",
                "Send it via UDP to a recursive resolver",
                "Parse the response to extract A/AAAA records",
            ],
            "leave_out": [
                "DNSSEC validation",
                "Recursive resolution (just use 8.8.8.8)",
                "Caching / TTL management",
            ],
            "done_condition": "Resolve example.com to its IP address using raw sockets",
            "transferable_principles": [
                "Binary protocol encoding/decoding",
                "UDP socket programming",
                "DNS hierarchy and record types",
            ],
            "next_wheels": ["HTTP/1.1 server", "TCP over UDP"],
        },
        {
            "wheel": "TCP over UDP",
            "effort_days": 5,
            "essential_behaviors": [
                "Implement reliable delivery with ACKs and retransmission",
                "Sequence packets and reorder on receive",
                "Implement a sliding window for flow control",
            ],
            "leave_out": [
                "Congestion control (Reno, CUBIC)",
                "Connection teardown (FIN handshake)",
                "Nagle's algorithm",
            ],
            "done_condition": "Transfer a 1 MB file over lossy UDP (simulated 10% packet loss) without corruption",
            "transferable_principles": [
                "Reliability over unreliable channels",
                "Windowing and flow control",
                "State machine protocol design",
            ],
            "next_wheels": ["HTTP/1.1 server", "DNS resolver"],
        },
    ],
    "compilers": [
        {
            "wheel": "Lexer (tokenizer)",
            "effort_days": 1,
            "essential_behaviors": [
                "Scan source text character by character",
                "Emit typed tokens (number, string, keyword, operator)",
                "Track line/column for error reporting",
            ],
            "leave_out": [
                "Unicode beyond ASCII",
                "Heredocs / string interpolation",
                "Preprocessor directives",
            ],
            "done_condition": "Tokenize a 20-line program in a simple language and round-trip to source",
            "transferable_principles": [
                "Finite automata in practice",
                "Streaming text processing",
                "Foundation for all parsing",
            ],
            "next_wheels": ["recursive descent parser", "register allocator"],
        },
        {
            "wheel": "Recursive descent parser",
            "effort_days": 3,
            "essential_behaviors": [
                "Parse expressions with correct operator precedence",
                "Handle grouping with parentheses",
                "Build an AST from a token stream",
            ],
            "leave_out": [
                "Error recovery / synchronization",
                "Left-recursive grammars",
                "Macro expansion",
            ],
            "done_condition": "Parse and evaluate 3 + 4 * (2 - 1) correctly to 7",
            "transferable_principles": [
                "Grammar → code mapping",
                "Precedence climbing",
                "Tree-based intermediate representations",
            ],
            "next_wheels": ["lexer", "register allocator"],
        },
        {
            "wheel": "Register allocator",
            "effort_days": 4,
            "essential_behaviors": [
                "Build an interference graph from live variable analysis",
                "Color the graph with k registers",
                "Spill variables to stack when registers exhausted",
            ],
            "leave_out": [
                "Coalescing (move elimination)",
                "Splitting live ranges",
                "Platform-specific calling conventions",
            ],
            "done_condition": "Allocate 8 virtual registers to 4 physical registers for a 10-instruction block",
            "transferable_principles": [
                "Graph coloring algorithms",
                "Liveness analysis",
                "Resource allocation under constraints",
            ],
            "next_wheels": ["lexer", "recursive descent parser"],
        },
    ],
    "search": [
        {
            "wheel": "Inverted index",
            "effort_days": 2,
            "essential_behaviors": [
                "Tokenize documents into terms",
                "Build a term → document-id mapping",
                "Answer boolean AND/OR queries across terms",
            ],
            "leave_out": [
                "Positional indexes",
                "Compression (variable-byte encoding)",
                "Incremental updates",
            ],
            "done_condition": "Index 1000 documents and return results for a 2-term AND query in < 10ms",
            "transferable_principles": [
                "How search engines work at the core",
                "Posting list intersection",
                "Trade-off between index size and query speed",
            ],
            "next_wheels": ["TF-IDF scorer", "finite state transducer"],
        },
        {
            "wheel": "TF-IDF scorer",
            "effort_days": 1,
            "essential_behaviors": [
                "Compute term frequency per document",
                "Compute inverse document frequency across corpus",
                "Rank documents by TF-IDF score for a query",
            ],
            "leave_out": [
                "BM25 tuning parameters",
                "Length normalization",
                "Stemming / lemmatization",
            ],
            "done_condition": "Given 100 articles, rank them for a query and get intuitively correct top-3",
            "transferable_principles": [
                "Statistical relevance scoring",
                "Information retrieval fundamentals",
                "Foundation for understanding embeddings and vector search",
            ],
            "next_wheels": ["inverted index", "finite state transducer"],
        },
        {
            "wheel": "Finite state transducer",
            "effort_days": 5,
            "essential_behaviors": [
                "Build an FST from a sorted list of key-value pairs",
                "Lookup a key and return its associated value",
                "Demonstrate space savings vs. a hash map",
            ],
            "leave_out": [
                "Streaming construction",
                "Regex-based queries over the FST",
                "Levenshtein automaton intersection",
            ],
            "done_condition": "Store 100k English words → frequency in an FST smaller than the equivalent JSON",
            "transferable_principles": [
                "Compact data structures for ordered sets",
                "Shared-prefix compression",
                "Why Lucene/Tantivy use FSTs internally",
            ],
            "next_wheels": ["inverted index", "TF-IDF scorer"],
        },
    ],
    "web": [
        {
            "wheel": "Template engine",
            "effort_days": 2,
            "essential_behaviors": [
                "Parse {{ variable }} placeholders in HTML",
                "Support {% for item in list %} loops",
                "Support {% if condition %} conditionals",
            ],
            "leave_out": [
                "Template inheritance / blocks",
                "Auto-escaping",
                "Custom filters",
            ],
            "done_condition": "Render a user list page from a template + JSON data",
            "transferable_principles": [
                "Code generation from templates",
                "Separation of logic and presentation",
                "How Jinja2/Handlebars work under the hood",
            ],
            "next_wheels": ["URL router", "form validator"],
        },
        {
            "wheel": "URL router",
            "effort_days": 1,
            "essential_behaviors": [
                "Register routes with path parameters (/users/:id)",
                "Match incoming URL paths to registered handlers",
                "Extract path parameters into a dict",
            ],
            "leave_out": [
                "Regex-based routes",
                "Middleware chains",
                "Route groups / namespacing",
            ],
            "done_condition": "Route /users/42/posts/7 and extract {user_id: 42, post_id: 7}",
            "transferable_principles": [
                "Trie-based matching",
                "URL design and REST conventions",
                "How Express/Flask routing works",
            ],
            "next_wheels": ["template engine", "form validator"],
        },
        {
            "wheel": "Form validator",
            "effort_days": 1,
            "essential_behaviors": [
                "Define validation rules declaratively (required, min_length, pattern)",
                "Validate a dict of form data against rules",
                "Return structured error messages per field",
            ],
            "leave_out": [
                "Async validation (e.g., unique email check)",
                "Nested object validation",
                "i18n error messages",
            ],
            "done_condition": "Validate a signup form (name, email, password) with clear error messages",
            "transferable_principles": [
                "Declarative validation patterns",
                "Schema-driven programming",
                "How Pydantic/Zod work at the core",
            ],
            "next_wheels": ["template engine", "URL router"],
        },
    ],
    "os": [
        {
            "wheel": "Memory allocator",
            "effort_days": 4,
            "essential_behaviors": [
                "Implement malloc/free with a free list",
                "Split and coalesce free blocks",
                "Handle alignment requirements",
            ],
            "leave_out": [
                "Thread safety",
                "mmap-based large allocations",
                "Slab allocation",
            ],
            "done_condition": "Allocate and free 10k blocks of varying sizes without leaking or corrupting",
            "transferable_principles": [
                "How heap memory works",
                "Fragmentation and its mitigation",
                "Why Rust's ownership model matters",
            ],
            "next_wheels": ["simple filesystem", "shell"],
        },
        {
            "wheel": "Simple filesystem",
            "effort_days": 3,
            "essential_behaviors": [
                "Create/read/write/delete files in a flat namespace",
                "Store file data in fixed-size blocks",
                "Maintain a simple superblock + inode table",
            ],
            "leave_out": [
                "Directories / hierarchy",
                "Permissions",
                "Journaling",
            ],
            "done_condition": "Mount a file-backed filesystem, write 3 files, unmount, remount, read them back",
            "transferable_principles": [
                "Block-based storage",
                "Inodes and metadata",
                "How ext4/ZFS manage data at a high level",
            ],
            "next_wheels": ["memory allocator", "shell"],
        },
        {
            "wheel": "Shell",
            "effort_days": 2,
            "essential_behaviors": [
                "Read-eval-print loop with line editing",
                "Fork/exec external commands",
                "Implement pipes (cmd1 | cmd2)",
            ],
            "leave_out": [
                "Job control (bg/fg)",
                "Signal handling",
                "Scripting (if/for/while)",
            ],
            "done_condition": "Run ls -la | grep .py | wc -l and get the correct count",
            "transferable_principles": [
                "Process creation and management",
                "File descriptor plumbing",
                "How bash/zsh work under the hood",
            ],
            "next_wheels": ["memory allocator", "simple filesystem"],
        },
    ],
}


@dataclass
class LearningPlan:
    domain: str
    wheel: str
    effort_days: int
    essential_behaviors: list[str]
    leave_out: list[str]
    done_condition: str
    transferable_principles: list[str]
    next_wheels: list[str]
    checkpoints: list[str] = field(default_factory=list)

    def generate_checkpoints(self):
        """Generate day-by-day checkpoints."""
        self.checkpoints = []
        if self.effort_days == 1:
            self.checkpoints = [
                "Morning: Attempt implementation from mental model alone",
                "Afternoon: Compare with reference, note deltas",
                "Evening: Refactor, then verify done-condition passes",
            ]
        else:
            self.checkpoints.append(
                "Day 1: Sketch data structures and API surface. "
                "Attempt the first essential behavior without references."
            )
            for i, behavior in enumerate(self.essential_behaviors):
                day = min(i + 2, self.effort_days)
                self.checkpoints.append(
                    f"Day {day}: Implement \"{behavior}\". "
                    f"Compare your approach with a reference implementation."
                )
            self.checkpoints.append(
                f"Day {self.effort_days}: Polish, verify done-condition, "
                f"and write down what you learned."
            )

    def to_dict(self) -> dict:
        return asdict(self)


def list_domains() -> list[str]:
    return sorted(DOMAINS.keys())


def get_wheels(domain: str) -> list[dict]:
    return DOMAINS.get(domain.lower(), [])


def create_plan(domain: str, wheel_name: str) -> Optional[LearningPlan]:
    wheels = get_wheels(domain)
    for w in wheels:
        if w["wheel"].lower() == wheel_name.lower():
            plan = LearningPlan(
                domain=domain,
                wheel=w["wheel"],
                effort_days=w["effort_days"],
                essential_behaviors=w["essential_behaviors"],
                leave_out=w["leave_out"],
                done_condition=w["done_condition"],
                transferable_principles=w["transferable_principles"],
                next_wheels=w["next_wheels"],
            )
            plan.generate_checkpoints()
            return plan
    return None


def format_plan(plan: LearningPlan) -> str:
    lines = []
    lines.append(f"{'=' * 64}")
    lines.append(f"  LEARNING PLAN: Reinvent the {plan.wheel}")
    lines.append(f"  Domain: {plan.domain}  |  Estimated effort: {plan.effort_days} day(s)")
    lines.append(f"{'=' * 64}")

    lines.append(f"\n  DONE CONDITION (how you know you've internalized it):")
    lines.append(f"  >>> {plan.done_condition}")

    lines.append(f"\n  ESSENTIAL BEHAVIORS (implement these):")
    for i, b in enumerate(plan.essential_behaviors, 1):
        lines.append(f"    {i}. {b}")

    lines.append(f"\n  EXPLICITLY LEAVE OUT (resist the urge):")
    for item in plan.leave_out:
        for line in textwrap.wrap(f"- {item}", width=58):
            lines.append(f"    {line}")

    lines.append(f"\n  TRANSFERABLE PRINCIPLES (why this is worth your time):")
    for p in plan.transferable_principles:
        lines.append(f"    * {p}")

    lines.append(f"\n  CHECKPOINTS:")
    for cp in plan.checkpoints:
        lines.append(f"    {cp}")

    lines.append(f"\n  WHAT TO REINVENT NEXT:")
    for nw in plan.next_wheels:
        lines.append(f"    -> {nw}")

    lines.append(f"\n{'=' * 64}")
    lines.append(
        '  "Reinvent 4-5 wheels in a domain and you reach the frontier\n'
        '   faster than any amount of idle study." — Andrew Quinn'
    )
    lines.append(f"{'=' * 64}")
    return "\n".join(lines)


def format_domain_overview(domain: str) -> str:
    wheels = get_wheels(domain)
    if not wheels:
        return f"Unknown domain: {domain}. Available: {', '.join(list_domains())}"

    lines = []
    lines.append(f"\n  Wheels worth reinventing in [{domain.upper()}]:\n")
    for w in wheels:
        lines.append(f"    {w['wheel']:<30s} ({w['effort_days']} day{'s' if w['effort_days'] != 1 else ''})")
        lines.append(f"      Done when: {w['done_condition']}")
        lines.append("")
    return "\n".join(lines)


def interactive_mode():
    """Run an interactive session to pick a domain and wheel."""
    print("\n" + "=" * 64)
    print("  DELIBERATE WHEEL REINVENTION")
    print("  Learn by building — pick the right wheels to reinvent")
    print("=" * 64)

    domains = list_domains()
    print(f"\n  Available domains:\n")
    for i, d in enumerate(domains, 1):
        wheels = get_wheels(d)
        print(f"    {i}. {d:<15s} ({len(wheels)} wheels)")

    print(f"\n  Enter a domain name (or number) to explore, or 'all' for everything:")

    try:
        choice = input("  > ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "all"

    if choice.lower() == "all":
        for d in domains:
            print(format_domain_overview(d))
        return

    # Resolve numeric choice
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(domains):
            choice = domains[idx]

    domain = choice.lower()
    if domain not in DOMAINS:
        print(f"  Unknown domain: {choice}. Available: {', '.join(domains)}")
        return

    print(format_domain_overview(domain))

    wheels = get_wheels(domain)
    print(f"  Pick a wheel to generate a full learning plan (or 'all'):")

    try:
        wheel_choice = input("  > ").strip()
    except (EOFError, KeyboardInterrupt):
        wheel_choice = "all"

    if wheel_choice.lower() == "all":
        for w in wheels:
            plan = create_plan(domain, w["wheel"])
            if plan:
                print(format_plan(plan))
        return

    plan = create_plan(domain, wheel_choice)
    if plan:
        print(format_plan(plan))
    else:
        print(f"  Unknown wheel: {wheel_choice}")
        print(f"  Available: {', '.join(w['wheel'] for w in wheels)}")


def demo_mode():
    """Non-interactive demo: show all domains then a sample plan."""
    print("\n" + "=" * 64)
    print("  DELIBERATE WHEEL REINVENTION")
    print("  Learn by building — pick the right wheels to reinvent")
    print("=" * 64)

    domains = list_domains()
    print(f"\n  Available domains ({len(domains)} total):\n")
    for d in domains:
        wheels = get_wheels(d)
        names = ", ".join(w["wheel"] for w in wheels)
        print(f"    {d:<15s} -> {names}")

    # Show one full plan as an example
    print("\n" + "-" * 64)
    print("  EXAMPLE: Full learning plan for 'inverted index' (search domain)")
    print("-" * 64)
    plan = create_plan("search", "Inverted index")
    if plan:
        print(format_plan(plan))

    # Show JSON export
    print("\n" + "-" * 64)
    print("  Plans are also exportable as JSON for programmatic use:")
    print("-" * 64)
    plan2 = create_plan("web", "URL router")
    if plan2:
        print(json.dumps(plan2.to_dict(), indent=2))

    # Summary stats
    total_wheels = sum(len(ws) for ws in DOMAINS.values())
    total_days = sum(
        w["effort_days"] for ws in DOMAINS.values() for w in ws
    )
    print(f"\n  Catalog: {total_wheels} wheels across {len(DOMAINS)} domains")
    print(f"  Total estimated effort: {total_days} days")
    print(f"  Andrew Quinn's sweet spot: 4-5 wheels per domain\n")


def main():
    if "--interactive" in sys.argv:
        interactive_mode()
    elif "--json" in sys.argv:
        # Export full catalog as JSON
        output = {}
        for domain, wheels in DOMAINS.items():
            output[domain] = []
            for w in wheels:
                plan = create_plan(domain, w["wheel"])
                if plan:
                    output[domain].append(plan.to_dict())
        print(json.dumps(output, indent=2))
    elif "--domain" in sys.argv:
        idx = sys.argv.index("--domain")
        if idx + 1 < len(sys.argv):
            domain = sys.argv[idx + 1]
            print(format_domain_overview(domain))
        else:
            print("Usage: --domain <name>")
    elif "--plan" in sys.argv:
        idx = sys.argv.index("--plan")
        if idx + 2 < len(sys.argv):
            domain = sys.argv[idx + 1]
            wheel = " ".join(sys.argv[idx + 2:])
            plan = create_plan(domain, wheel)
            if plan:
                print(format_plan(plan))
            else:
                print(f"No wheel '{wheel}' found in domain '{domain}'")
        else:
            print("Usage: --plan <domain> <wheel name>")
    else:
        demo_mode()


if __name__ == "__main__":
    main()
