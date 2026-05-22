"""
Mock Datasette Agent — demonstrates the conversational data exploration
workflow without requiring an LLM API key.

Simulates: natural-language question -> SQL generation -> query execution -> formatted results.
This mirrors how the real Datasette Agent works under the hood.
"""
import sqlite3
import sys
import os
import textwrap

DB_PATH = os.path.join(os.path.dirname(__file__), "power_plants.db")

# Pre-defined question->SQL mappings that mirror what the real agent generates
CONVERSATIONS = [
    {
        "question": "What are the top 5 countries by total power plant capacity?",
        "thinking": "I'll query the power_plants table, summing capacity_mw grouped by country, ordered descending.",
        "sql": """
            SELECT country,
                   COUNT(*) AS num_plants,
                   ROUND(SUM(capacity_mw), 0) AS total_capacity_mw
            FROM power_plants
            GROUP BY country
            ORDER BY total_capacity_mw DESC
            LIMIT 5
        """,
    },
    {
        "question": "Show me the breakdown of renewable vs fossil fuel capacity by region.",
        "thinking": "I'll classify fuel types as renewable or fossil, then aggregate by region.",
        "sql": """
            SELECT region,
                   ROUND(SUM(CASE WHEN fuel_type IN ('Hydro','Wind','Solar','Geothermal') THEN capacity_mw ELSE 0 END), 0) AS renewable_mw,
                   ROUND(SUM(CASE WHEN fuel_type IN ('Coal','Gas','Oil','Oil Shale') THEN capacity_mw ELSE 0 END), 0) AS fossil_mw,
                   ROUND(SUM(CASE WHEN fuel_type = 'Nuclear' THEN capacity_mw ELSE 0 END), 0) AS nuclear_mw
            FROM power_plants
            GROUP BY region
            ORDER BY renewable_mw DESC
        """,
    },
    {
        "question": "Which power plants were commissioned after 2015?",
        "thinking": "Simple filter on commissioned_year > 2015, ordered by date.",
        "sql": """
            SELECT name, country, fuel_type, capacity_mw, commissioned_year
            FROM power_plants
            WHERE commissioned_year > 2015
            ORDER BY commissioned_year DESC
        """,
    },
    {
        "question": "What's the average capacity by fuel type?",
        "thinking": "Aggregate average capacity grouped by fuel_type.",
        "sql": """
            SELECT fuel_type,
                   COUNT(*) AS count,
                   ROUND(AVG(capacity_mw), 0) AS avg_capacity_mw,
                   ROUND(MIN(capacity_mw), 0) AS min_mw,
                   ROUND(MAX(capacity_mw), 0) AS max_mw
            FROM power_plants
            GROUP BY fuel_type
            ORDER BY avg_capacity_mw DESC
        """,
    },
    {
        "question": "What percentage of global capacity is renewable?",
        "thinking": "Calculate total renewable capacity as a share of overall capacity.",
        "sql": """
            SELECT
                ROUND(SUM(CASE WHEN fuel_type IN ('Hydro','Wind','Solar','Geothermal') THEN capacity_mw ELSE 0 END), 0) AS renewable_mw,
                ROUND(SUM(capacity_mw), 0) AS total_mw,
                ROUND(100.0 * SUM(CASE WHEN fuel_type IN ('Hydro','Wind','Solar','Geothermal') THEN capacity_mw ELSE 0 END) / SUM(capacity_mw), 1) AS renewable_pct
            FROM power_plants
        """,
    },
]


def print_header(text):
    width = 70
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def print_table(headers, rows):
    """Simple ASCII table formatter."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    def fmt_row(vals):
        return " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(vals))

    sep = "-+-".join("-" * w for w in col_widths)
    print(f"  {fmt_row(headers)}")
    print(f"  {sep}")
    for row in rows:
        print(f"  {fmt_row(row)}")


def render_bar_chart(headers, rows_list, label_idx, value_idx, max_bar=30):
    """Render a simple horizontal bar chart in the terminal."""
    if not rows_list:
        return
    max_val = max(r[value_idx] for r in rows_list) or 1
    print()
    print("  Chart:")
    for row in rows_list:
        label = str(row[label_idx])
        val = row[value_idx]
        bar_len = int((val / max_val) * max_bar)
        bar = "#" * bar_len
        print(f"  {label:>20s} | {bar} {val}")
    print()


def run_conversation():
    if not os.path.exists(DB_PATH):
        print("ERROR: Database not found. Run demo_data.py first.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print_header("Datasette Agent  --  Mock Data Explorer Demo")
    print()
    print("  This demo simulates Datasette Agent's conversational flow:")
    print("  natural-language question -> SQL generation -> query execution -> results")
    print()
    print("  Database: power_plants.db (30 global power plants)")
    print("  In production, the LLM generates SQL dynamically via tool-calling.")
    print()

    # Show schema first (like the real agent inspects it)
    print("-" * 70)
    print("  [Agent] Inspecting database schema...")
    cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='power_plants'")
    schema = cursor.fetchone()[0]
    print(f"  {schema}")
    print()
    row_count = conn.execute("SELECT COUNT(*) FROM power_plants").fetchone()[0]
    print(f"  Found 1 table with {row_count} rows.")
    print("-" * 70)

    for i, conv in enumerate(CONVERSATIONS, 1):
        print()
        print(f"  USER ({i}/{len(CONVERSATIONS)}): {conv['question']}")
        print()
        print(f"  [Agent thinking] {conv['thinking']}")
        print()
        sql_display = textwrap.dedent(conv["sql"]).strip()
        print(f"  [Agent] Executing SQL:")
        for line in sql_display.split("\n"):
            print(f"    {line}")
        print()

        cursor = conn.execute(conv["sql"])
        headers = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        rows_list = [tuple(r) for r in rows]

        print(f"  [Results] {len(rows_list)} row(s):")
        print()
        print_table(headers, rows_list)

        # Add a chart for select queries
        if i == 1:
            render_bar_chart(headers, rows_list, 0, 2, max_bar=35)
        elif i == 5:
            row = rows_list[0]
            renewable = row[0]
            total = row[1]
            pct = row[2]
            print()
            print(f"  Summary: {renewable:,.0f} MW renewable out of {total:,.0f} MW total = {pct}%")

    print()
    print_header("Demo Complete")
    print()
    print("  With the real Datasette Agent you can:")
    print("    - Ask ANY question in plain English")
    print("    - Get interactive charts (with datasette-agent-charts)")
    print("    - Explore multiple tables and databases")
    print("    - Deploy publicly with `datasette publish`")
    print()
    print("  Try it live: https://agent.datasette.io/")
    print()

    conn.close()


if __name__ == "__main__":
    run_conversation()
