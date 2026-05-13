"""Demonstrate Datasette's JSON API by querying the running instance."""
import urllib.request
import json
import sys
import time

BASE = "http://localhost:8001"


def query(path, label):
    url = f"{BASE}{path}"
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"  GET {path}")
    print(f"{'=' * 60}")
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print(json.dumps(data, indent=2)[:1500])
            if len(json.dumps(data)) > 1500:
                print("  ... (truncated)")
            return data
    except Exception as e:
        print(f"  Error: {e}")
        return None


def wait_for_server(max_wait=15):
    print(f"Waiting for Datasette at {BASE} ...")
    for i in range(max_wait):
        try:
            urllib.request.urlopen(f"{BASE}/-/versions.json", timeout=2)
            print("Datasette is ready!\n")
            return True
        except Exception:
            time.sleep(1)
    print("Datasette did not start in time.")
    return False


def main():
    if not wait_for_server():
        sys.exit(1)

    # 1. List databases
    query("/-/databases.json", "List all databases")

    # 2. List tables in the demo database
    query("/demo.json", "Tables in demo.db")

    # 3. Query AI tools sorted by stars
    query(
        "/demo/ai_tools.json?_sort_desc=stars&_size=5",
        "Top 5 AI tools by GitHub stars",
    )

    # 4. Filter by category
    query(
        "/demo/ai_tools.json?category=coding-agent",
        "Coding agent tools",
    )

    # 5. SQL query via API
    sql = "select tool_name, sum(value) as total_signals from trend_signals group by tool_name order by total_signals desc limit 5"
    encoded = urllib.request.quote(sql)
    query(
        f"/demo.json?sql={encoded}&_shape=array",
        "Top 5 tools by total trend signal volume (custom SQL)",
    )

    # 6. Show empty table (1.0a29 feature: headers still display)
    query(
        "/demo/upcoming_reviews.json",
        "Empty table - headers shown (1.0a29 fix #2701)",
    )

    print("\n" + "=" * 60)
    print("  Demo complete! Datasette is still running at:")
    print(f"  {BASE}")
    print("  Open in your browser to explore the web UI.")
    print("  Press Ctrl+C to stop.")
    print("=" * 60)


if __name__ == "__main__":
    main()
