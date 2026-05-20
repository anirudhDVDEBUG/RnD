#!/usr/bin/env python3
"""
Demo: How datasette-llm's llm_prompt_context() hook works.

This simulates the plugin architecture of datasette-llm, showing how
multiple plugins can contribute context to an LLM prompt via the
llm_prompt_context() hook -- and how the v0.1a8 fix ensures chained
(iterable) responses are fully collected.

No Datasette or API keys required. Pure simulation.
"""

import sqlite3
import os
import textwrap

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.db")

# ─── Simulated Datasette Plugin Hook System ───────────────────────────────────

class MockDatasette:
    """Minimal stand-in for the Datasette instance."""

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._setup_db()

    def _setup_db(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL,
                stock INTEGER
            );
            DELETE FROM products;
            INSERT INTO products VALUES
                (1, 'Mechanical Keyboard', 'Electronics', 89.99, 42),
                (2, 'Standing Desk', 'Furniture', 449.00, 15),
                (3, 'USB-C Hub', 'Electronics', 34.50, 108),
                (4, 'Ergonomic Chair', 'Furniture', 599.00, 7),
                (5, 'Monitor Light Bar', 'Electronics', 54.99, 63),
                (6, 'Cable Organizer', 'Accessories', 12.99, 200),
                (7, 'Webcam HD', 'Electronics', 79.00, 31),
                (8, 'Desk Mat', 'Accessories', 24.99, 85);
        """)
        self.conn.commit()

    def execute_sql(self, sql):
        return self.conn.execute(sql).fetchall()

    def get_schema(self):
        rows = self.conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='products'"
        ).fetchone()
        return rows[0] if rows else ""


class MockRequest:
    """Simulates a Datasette HTTP request."""

    def __init__(self, query):
        self.query = query
        self.url = f"/products?_llm={query}"


# ─── Example plugins that implement llm_prompt_context() ──────────────────────

def plugin_schema_context(datasette, request):
    """Plugin A: returns the table schema as a plain string."""
    schema = datasette.get_schema()
    return f"Database schema:\n{schema}"


def plugin_sample_rows(datasette, request):
    """Plugin B: returns sample rows as an iterable (generator).
    This is the pattern that was BROKEN before v0.1a8 -- generators
    were not fully consumed, so only the first chunk was included."""
    rows = datasette.execute_sql("SELECT * FROM products LIMIT 3")
    yield "Sample data from products table:"
    for row in rows:
        yield f"  id={row[0]}, name={row[1]}, category={row[2]}, price=${row[3]}, stock={row[4]}"


def plugin_query_hint(datasette, request):
    """Plugin C: returns contextual hint based on the user's query."""
    return f"The user is asking: \"{request.query}\"\nHelp them write a SQL query for the products table."


# ─── The core llm_prompt_context() collection logic ───────────────────────────

def collect_prompt_context_BROKEN(plugins, datasette, request):
    """BEFORE v0.1a8: Did not exhaust generators/iterables.
    Only the first yielded value from iterable responses was captured."""
    context_parts = []
    for plugin_fn in plugins:
        result = plugin_fn(datasette, request)
        if isinstance(result, str):
            context_parts.append(result)
        else:
            # BUG: only took the first item from the iterator
            try:
                first = next(iter(result))
                context_parts.append(first)
            except StopIteration:
                pass
    return "\n\n".join(context_parts)


def collect_prompt_context_FIXED(plugins, datasette, request):
    """AFTER v0.1a8: Fully collects chained/iterable responses.
    All yielded values from generators are joined into the context."""
    context_parts = []
    for plugin_fn in plugins:
        result = plugin_fn(datasette, request)
        if isinstance(result, str):
            context_parts.append(result)
        else:
            # FIX: exhaust the entire iterator
            chunks = list(result)
            context_parts.append("\n".join(chunks))
    return "\n\n".join(context_parts)


# ─── Mock LLM response (no real API call) ─────────────────────────────────────

def mock_llm_response(prompt_context, user_query):
    """Simulates what an LLM would generate given the assembled context."""
    # In real datasette-llm, this calls llm.get_model().prompt(...)
    return textwrap.dedent(f"""\
    -- Generated SQL for: "{user_query}"
    SELECT category,
           COUNT(*) AS num_products,
           ROUND(AVG(price), 2) AS avg_price,
           SUM(stock) AS total_stock
    FROM products
    GROUP BY category
    ORDER BY avg_price DESC;
    """)


# ─── Main demo ───────────────────────────────────────────────────────────────

def main():
    ds = MockDatasette(DB_PATH)
    request = MockRequest("Show me average price by category")
    plugins = [plugin_schema_context, plugin_sample_rows, plugin_query_hint]

    print("=" * 72)
    print("  datasette-llm  --  llm_prompt_context() Hook Demo")
    print("  Demonstrates the v0.1a8 fix for chained response collection")
    print("=" * 72)

    # ── Show the bug ──
    print("\n[1] BEFORE v0.1a8 — broken chain collection")
    print("-" * 50)
    broken_ctx = collect_prompt_context_BROKEN(plugins, ds, request)
    print(broken_ctx)
    print()
    print("  ^^^ NOTICE: Plugin B (sample rows) only shows the header line.")
    print("      The actual row data from the generator was LOST.")

    # ── Show the fix ──
    print("\n[2] AFTER v0.1a8 — fixed chain collection")
    print("-" * 50)
    fixed_ctx = collect_prompt_context_FIXED(plugins, ds, request)
    print(fixed_ctx)
    print()
    print("  ^^^ All 3 sample rows are now included in the context.")

    # ── Show mock LLM output ──
    print("\n[3] Mock LLM response (using full context)")
    print("-" * 50)
    sql = mock_llm_response(fixed_ctx, request.query)
    print(sql)

    # ── Run the generated SQL ──
    print("[4] Executing generated SQL against demo.db")
    print("-" * 50)
    results = ds.execute_sql(sql.strip().rstrip(";"))
    print(f"  {'Category':<15} {'Products':>8} {'Avg Price':>10} {'Stock':>8}")
    print(f"  {'-'*15} {'-'*8} {'-'*10} {'-'*8}")
    for r in results:
        print(f"  {r[0]:<15} {r[1]:>8} ${r[2]:>9.2f} {r[3]:>8}")

    # ── Show plugin listing ──
    print("\n[5] Registered plugins (simulated `datasette plugins` output)")
    print("-" * 50)
    for name, ver, desc in [
        ("datasette-llm", "0.1a8", "LLM prompting capabilities for Datasette"),
        ("plugin-schema-ctx", "0.1.0", "Injects table schema into LLM context"),
        ("plugin-sample-rows", "0.1.0", "Injects sample rows into LLM context"),
        ("plugin-query-hint", "0.1.0", "Adds user query hint to LLM context"),
    ]:
        print(f"  {name:<25} v{ver:<8} {desc}")

    print("\n" + "=" * 72)
    print("  datasette-llm lets any plugin inject context into LLM prompts.")
    print("  v0.1a8 fixed a bug where generator-based context was truncated.")
    print("  Install:  pip install datasette-llm")
    print("=" * 72)

    ds.conn.close()


if __name__ == "__main__":
    main()
