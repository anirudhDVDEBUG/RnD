"""
Demo: datasette-agent chat interaction (offline simulation).

This script simulates the kind of natural-language-to-SQL workflow that
datasette-agent performs inside Datasette's Jump menu. It reads the sample
database created by create_sample_db.py, accepts natural-language queries,
translates them to SQL, and prints formatted results -- mirroring what the
real agent chat does via the browser UI.

No API key is required; the NL->SQL mapping uses keyword heuristics so the
demo runs fully offline.
"""
import sqlite3
import os
import sys
import re

DB_PATH = os.environ.get("DEMO_DB", "demo.db")

# ---------------------------------------------------------------------------
# Lightweight NL -> SQL mapper (offline heuristic, NOT an LLM)
# ---------------------------------------------------------------------------

QUERY_MAP = [
    {
        "patterns": [r"count.*product", r"how many.*product", r"total.*product"],
        "sql": "SELECT count(*) AS product_count FROM products",
        "description": "Count all products",
    },
    {
        "patterns": [r"count.*order", r"how many.*order", r"total.*order"],
        "sql": "SELECT count(*) AS order_count FROM orders",
        "description": "Count all orders",
    },
    {
        "patterns": [r"top.*expensive", r"most expensive", r"highest price"],
        "sql": "SELECT name, category, price FROM products ORDER BY price DESC LIMIT 5",
        "description": "Top 5 most expensive products",
    },
    {
        "patterns": [r"cheapest", r"lowest price", r"least expensive"],
        "sql": "SELECT name, category, price FROM products ORDER BY price ASC LIMIT 5",
        "description": "Top 5 cheapest products",
    },
    {
        "patterns": [r"revenue.*category", r"sales.*category", r"total.*category"],
        "sql": (
            "SELECT p.category, sum(o.total) AS revenue, count(o.id) AS num_orders "
            "FROM orders o JOIN products p ON o.product_id = p.id "
            "GROUP BY p.category ORDER BY revenue DESC"
        ),
        "description": "Revenue by category",
    },
    {
        "patterns": [r"top.*customer", r"best.*customer", r"biggest.*buyer"],
        "sql": (
            "SELECT customer_email, count(*) AS orders, sum(total) AS spent "
            "FROM orders GROUP BY customer_email ORDER BY spent DESC LIMIT 5"
        ),
        "description": "Top customers by spend",
    },
    {
        "patterns": [r"low.*stock", r"out of stock", r"inventory"],
        "sql": "SELECT name, category, stock FROM products ORDER BY stock ASC LIMIT 5",
        "description": "Products with lowest stock",
    },
    {
        "patterns": [r"recent.*order", r"latest.*order", r"new.*order"],
        "sql": (
            "SELECT o.id, p.name, o.quantity, o.total, o.customer_email, o.ordered_at "
            "FROM orders o JOIN products p ON o.product_id = p.id "
            "ORDER BY o.ordered_at DESC LIMIT 5"
        ),
        "description": "5 most recent orders",
    },
    {
        "patterns": [r"schema", r"tables", r"structure", r"describe"],
        "sql": "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
        "description": "List tables",
    },
    {
        "patterns": [r"all product", r"show.*product", r"list.*product"],
        "sql": "SELECT id, name, category, price, stock FROM products ORDER BY id",
        "description": "All products",
    },
]


def match_query(nl_input: str) -> dict | None:
    text = nl_input.lower().strip()
    for entry in QUERY_MAP:
        for pat in entry["patterns"]:
            if re.search(pat, text):
                return entry
    return None


def format_results(cursor: sqlite3.Cursor, rows: list) -> str:
    if not rows:
        return "  (no results)"
    cols = [desc[0] for desc in cursor.description]
    widths = [len(c) for c in cols]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
    sep = "-+-".join("-" * w for w in widths)
    lines = [header, sep]
    for row in rows:
        lines.append(" | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)))
    return "\n".join("  " + l for l in lines)


def run_interactive():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}. Run create_sample_db.py first.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    print("=" * 64)
    print("  datasette-agent Chat Demo (offline simulation)")
    print("=" * 64)
    print()
    print("This simulates the agent chat that datasette-agent adds to")
    print("Datasette's Jump menu. Type a natural-language query below.")
    print()
    print("Example queries:")
    print('  "How many products do we have?"')
    print('  "Show me the most expensive products"')
    print('  "Revenue by category"')
    print('  "Top customers by spend"')
    print('  "Recent orders"')
    print('  "Low stock items"')
    print()

    queries = [
        "How many products do we have?",
        "Show me the most expensive products",
        "Revenue by category",
        "Top customers by spend",
        "Recent orders",
    ]

    for q in queries:
        print("-" * 64)
        print(f"  User:  {q}")
        matched = match_query(q)
        if matched:
            print(f"  Agent: {matched['description']}")
            print(f"  SQL:   {matched['sql']}")
            print()
            cur = conn.execute(matched["sql"])
            rows = cur.fetchall()
            print(format_results(cur, rows))
        else:
            print("  Agent: I don't understand that query. Try rephrasing.")
        print()

    conn.close()
    print("=" * 64)
    print("  Demo complete. In a live datasette-agent setup, these")
    print("  queries run via an LLM inside Datasette's browser UI.")
    print("=" * 64)


if __name__ == "__main__":
    run_interactive()
