"""
Demo: Create and explore a Datasette fixture database locally.

This script uses datasette's populate_fixture_database to create the same
tables used by Datasette's own test suite, then inspects and queries them.
Falls back to a bundled mock if datasette is not installed (for CI/demo).
"""

import sqlite3
import os
import sys

DEMO_DB = os.path.join(os.path.dirname(__file__), "demo_fixtures.db")

# Fixture table definitions for mock mode (subset of what Datasette provides)
MOCK_FIXTURES_SQL = """
CREATE TABLE IF NOT EXISTS roadside_attractions (
    pk INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    latitude REAL,
    longitude REAL
);
INSERT INTO roadside_attractions VALUES
    (1, 'The Mystery Spot', '465 Mystery Spot Road, Santa Cruz, CA 95065', 37.0167, -122.0024),
    (2, 'Winchester Mystery House', '525 S Winchester Blvd, San Jose, CA 95128', 37.3184, -121.9511),
    (3, 'Burlingame Museum of PEZ Memorabilia', '214 California Drive, Burlingame, CA 94010', 37.5793, -122.3440),
    (4, 'Salvation Mountain', 'Beal Road, Niland, CA 92257', 33.2544, -115.4728);

CREATE TABLE IF NOT EXISTS facetable (
    pk INTEGER PRIMARY KEY,
    planet_int INTEGER,
    on_earth INTEGER,
    state TEXT,
    city_id INTEGER,
    neighborhood TEXT,
    tags TEXT
);
INSERT INTO facetable VALUES
    (1, 1, 1, 'CA', 1, 'Downtown', '["tag1","tag2"]'),
    (2, 1, 1, 'CA', 1, 'Uptown', '["tag1"]'),
    (3, 1, 1, 'MI', 2, 'Downtown', '["tag3"]'),
    (4, 1, 1, 'MC', 3, 'East Side', '[]');

CREATE TABLE IF NOT EXISTS searchable (
    pk INTEGER PRIMARY KEY,
    text1 TEXT,
    text2 TEXT
);
INSERT INTO searchable VALUES
    (1, 'How to train your dragon', 'This is a movie about dragons'),
    (2, 'Datasette for data exploration', 'A tool for exploring SQLite databases'),
    (3, 'Plugin testing patterns', 'Writing tests for Datasette plugins');

CREATE TABLE IF NOT EXISTS binary_data (
    hash TEXT PRIMARY KEY,
    data BLOB
);
INSERT INTO binary_data VALUES ('abc123', X'48656C6C6F');

CREATE TABLE IF NOT EXISTS compound_primary_key (
    pk1 TEXT,
    pk2 TEXT,
    content TEXT,
    PRIMARY KEY (pk1, pk2)
);
INSERT INTO compound_primary_key VALUES ('a', 'b', 'compound row 1'),
                                        ('c', 'd', 'compound row 2');
"""


def create_fixture_db(db_path):
    """Create the fixture database, using Datasette's built-in fixtures if available."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    use_real = False

    try:
        from datasette.fixtures import populate_fixture_database
        populate_fixture_database(conn)
        use_real = True
        print("  (Using real Datasette fixtures via populate_fixture_database)")
    except (ImportError, Exception) as e:
        print(f"  (Datasette not available: {e})")
        print("  (Using bundled mock fixtures for demo purposes)")
        conn.executescript(MOCK_FIXTURES_SQL)

    conn.close()
    return use_real


def list_tables(db_path):
    """List all tables in the fixture database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


def query_roadside_attractions(db_path):
    """Query sample data from roadside_attractions."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT pk, name, address FROM roadside_attractions LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    return rows


def main():
    print("=== datasette-fixtures Demo ===\n")

    # Step 1: Create fixture database
    print("--- Creating fixture database ---")
    used_real = create_fixture_db(DEMO_DB)
    print(f"  Created fixture database: {os.path.basename(DEMO_DB)}\n")

    # Step 2: List tables
    print("--- Tables in fixture database ---")
    tables = list_tables(DEMO_DB)
    for i, table in enumerate(tables, 1):
        print(f"  {i:3d}. {table}")
    print(f"\n  Total: {len(tables)} tables\n")

    # Step 3: Query sample data
    print("--- Sample data from roadside_attractions ---")
    rows = query_roadside_attractions(DEMO_DB)
    for row in rows:
        print(f"  Row {row[0]}: {row[1]} | {row[2]}")
    print()

    # Summary
    if used_real:
        print("Used REAL Datasette fixtures (datasette >= 1.0a30 detected).")
    else:
        print("Used MOCK fixtures (install datasette >= 1.0a30 for the full set).")
        print("  pip install --pre datasette datasette-fixtures")

    return 0


if __name__ == "__main__":
    sys.exit(main())
