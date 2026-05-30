"""Create and seed the demo SQLite database."""
import sqlite_utils
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "demo.db")


def setup():
    # Remove existing db for clean demo
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    db = sqlite_utils.Database(DB_PATH)

    # Enable WAL mode for concurrent read/write
    db.execute("PRAGMA journal_mode=WAL")

    # Create documents table
    db["documents"].create(
        {
            "id": int,
            "title": str,
            "body": str,
            "created_at": str,
        },
        pk="id",
    )

    # Create tags table
    db["tags"].create(
        {
            "id": int,
            "document_id": int,
            "tag": str,
        },
        pk="id",
        foreign_keys=[("document_id", "documents", "id")],
    )

    # Seed with sample data
    db["documents"].insert_all(
        [
            {"title": "Getting Started", "body": "Welcome to Datasette write queries.", "created_at": "2026-05-29T10:00:00Z"},
            {"title": "API Design", "body": "RESTful patterns for AI agents.", "created_at": "2026-05-29T11:00:00Z"},
        ]
    )

    db["tags"].insert_all(
        [
            {"document_id": 1, "tag": "tutorial"},
            {"document_id": 1, "tag": "datasette"},
            {"document_id": 2, "tag": "api"},
        ]
    )

    print(f"Database created at {DB_PATH}")
    print(f"  documents: {db['documents'].count} rows")
    print(f"  tags: {db['tags'].count} rows")


if __name__ == "__main__":
    setup()
