"""
Example: How a Datasette plugin test suite would use fixtures.

This demonstrates the testing pattern — create a fixture DB, then assert
against its contents. Works with real Datasette or the bundled mock.
"""

import sqlite3
import os
import sys

# Import our demo's fixture creator
from demo_fixtures import create_fixture_db, MOCK_FIXTURES_SQL

TEST_DB = os.path.join(os.path.dirname(__file__), "test_fixtures.db")


def setup():
    """Create a fresh fixture database for tests."""
    create_fixture_db(TEST_DB)


def teardown():
    """Clean up test database."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_fixture_tables_exist():
    """Verify core fixture tables are present."""
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()

    required = {"roadside_attractions", "facetable", "searchable"}
    missing = required - tables
    assert not missing, f"Missing tables: {missing}"
    return True


def test_roadside_attractions_has_data():
    """Verify roadside_attractions has rows."""
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.execute("SELECT COUNT(*) FROM roadside_attractions")
    count = cursor.fetchone()[0]
    conn.close()

    assert count > 0, "roadside_attractions should have data"
    return True


def test_query_fixture_data():
    """Verify we can query and get expected columns."""
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.execute(
        "SELECT pk, name, address FROM roadside_attractions WHERE pk = 1"
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "Should find row with pk=1"
    assert row[1] == "The Mystery Spot", f"Expected 'The Mystery Spot', got '{row[1]}'"
    return True


def run_tests():
    """Simple test runner."""
    tests = [
        test_fixture_tables_exist,
        test_roadside_attractions_has_data,
        test_query_fixture_data,
    ]

    print("--- Running plugin test example ---")
    setup()

    passed = 0
    failed = 0

    for test_fn in tests:
        name = test_fn.__name__
        try:
            test_fn()
            print(f"  {name} ... PASSED")
            passed += 1
        except AssertionError as e:
            print(f"  {name} ... FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  {name} ... ERROR: {e}")
            failed += 1

    teardown()

    print()
    if failed == 0:
        print(f"All {passed} tests passed!")
    else:
        print(f"{passed} passed, {failed} failed.")

    return failed


if __name__ == "__main__":
    sys.exit(run_tests())
