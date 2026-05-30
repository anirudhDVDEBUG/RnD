"""
Demonstrate Datasette write queries and stored queries via the JSON API.
Requires a running Datasette instance on localhost:8001.
"""
import httpx
import sys
import time

BASE_URL = "http://localhost:8001"


def wait_for_server(max_wait=15):
    """Wait for Datasette to be ready."""
    for i in range(max_wait):
        try:
            r = httpx.get(f"{BASE_URL}/-/versions.json", timeout=2)
            if r.status_code == 200:
                version = r.json().get("datasette", {}).get("version", "unknown")
                print(f"Datasette is running (version: {version})")
                return True
        except (httpx.ConnectError, httpx.ReadTimeout):
            pass
        time.sleep(1)
    print("ERROR: Datasette did not start in time")
    return False


def execute_write_query(sql, params=None):
    """Execute a write SQL query via Datasette API."""
    payload = {"sql": sql}
    if params:
        payload["params"] = params

    r = httpx.post(
        f"{BASE_URL}/demo/-/query.json",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    return r.status_code, r.json() if r.status_code == 200 else r.text


def execute_read_query(sql):
    """Execute a read SQL query via Datasette API."""
    r = httpx.get(
        f"{BASE_URL}/demo.json",
        params={"sql": sql, "_shape": "array"},
        timeout=10,
    )
    return r.status_code, r.json() if r.status_code == 200 else r.text


def demo_write_queries():
    """Demonstrate INSERT, UPDATE, DELETE via the API."""
    print("\n" + "=" * 60)
    print("DEMO: Write Queries via Datasette API")
    print("=" * 60)

    # INSERT
    print("\n1. INSERT a new document:")
    status, result = execute_write_query(
        "INSERT INTO documents (title, body, created_at) VALUES (:title, :body, :created_at)",
        {"title": "Agent Memory", "body": "Storing agent state in SQLite via Datasette.", "created_at": "2026-05-29T12:00:00Z"},
    )
    print(f"   Status: {status}")
    if status == 200:
        print(f"   Result: {result}")

    # INSERT another
    print("\n2. INSERT with tags:")
    status, result = execute_write_query(
        "INSERT INTO documents (title, body, created_at) VALUES (:title, :body, :created_at)",
        {"title": "Voice AI Logs", "body": "Call transcripts and intent data.", "created_at": "2026-05-29T13:00:00Z"},
    )
    print(f"   Status: {status}")

    status, result = execute_write_query(
        "INSERT INTO tags (document_id, tag) VALUES (:doc_id, :tag)",
        {"doc_id": 4, "tag": "voice-ai"},
    )
    print(f"   Tag insert status: {status}")

    # UPDATE
    print("\n3. UPDATE a document:")
    status, result = execute_write_query(
        "UPDATE documents SET body = :body WHERE title = :title",
        {"title": "Getting Started", "body": "Updated: Now with write query support!"},
    )
    print(f"   Status: {status}")

    # DELETE
    print("\n4. DELETE a tag:")
    status, result = execute_write_query(
        "DELETE FROM tags WHERE tag = :tag",
        {"tag": "tutorial"},
    )
    print(f"   Status: {status}")


def demo_read_results():
    """Read back data to confirm writes."""
    print("\n" + "=" * 60)
    print("DEMO: Verify Writes (Read Back)")
    print("=" * 60)

    print("\n  All documents:")
    status, result = execute_read_query("SELECT * FROM documents ORDER BY id")
    if status == 200:
        for row in result:
            print(f"    [{row['id']}] {row['title']}: {row['body'][:50]}...")
    else:
        print(f"    Error: {result}")

    print("\n  All tags:")
    status, result = execute_read_query("SELECT t.tag, d.title FROM tags t JOIN documents d ON t.document_id = d.id")
    if status == 200:
        for row in result:
            print(f"    {row['title']} -> #{row['tag']}")
    else:
        print(f"    Error: {result}")


def demo_stored_query_concept():
    """Show what a stored query looks like (conceptual — API may vary by version)."""
    print("\n" + "=" * 60)
    print("DEMO: Stored Query Concept")
    print("=" * 60)
    print("""
  Stored queries save parameterized SQL for reuse. Example:

  Name: "Add Document"
  SQL:  INSERT INTO documents (title, body, created_at)
        VALUES (:title, :body, datetime('now'))

  When accessed via the UI, Datasette renders a form with fields:
    - title: [___________]
    - body:  [___________]
    - [Execute]

  This turns Datasette into a zero-code CRUD app for any table.

  In Datasette 1.0a31+, stored queries can be:
    - Private (only visible to the creator)
    - Shared (visible to all instance users)
    - Write-enabled (execute INSERT/UPDATE/DELETE)
""")


def main():
    if not wait_for_server():
        sys.exit(1)

    demo_write_queries()
    demo_read_results()
    demo_stored_query_concept()

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
