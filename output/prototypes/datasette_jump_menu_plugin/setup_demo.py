"""Create a sample SQLite database with bookmarks for the jump menu demo."""
import sqlite_utils

DB_PATH = "sample.db"

BOOKMARKS = [
    {"label": "Claude Docs", "url": "/bookmarks/claude-docs", "description": "Anthropic Claude documentation"},
    {"label": "Datasette Plugins", "url": "/bookmarks/datasette-plugins", "description": "Official Datasette plugin directory"},
    {"label": "MCP Specification", "url": "/bookmarks/mcp-spec", "description": "Model Context Protocol spec"},
    {"label": "Agent SDK Guide", "url": "/bookmarks/agent-sdk", "description": "Claude Agent SDK getting started"},
    {"label": "Simon Willison Blog", "url": "/bookmarks/simonwillison", "description": "Creator of Datasette"},
]


def main():
    db = sqlite_utils.Database(DB_PATH)
    if "bookmarks" in db.table_names():
        db["bookmarks"].drop()
    db["bookmarks"].insert_all(BOOKMARKS)
    db["bookmarks"].create_index(["label"], if_not_exists=True)
    print("Created sample.db with bookmarks table")
    print("\nJump menu items registered:")
    for b in BOOKMARKS:
        print(f"  - {b['label']} -> {b['url']}")


if __name__ == "__main__":
    main()
