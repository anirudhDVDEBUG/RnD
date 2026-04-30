"""SQLite storage layer for TrendForge."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "trendforge.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    url_hash TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    title TEXT,
    author TEXT,
    published_at TEXT,
    raw_metadata JSON,
    status TEXT DEFAULT 'new',
    score REAL,
    score_reasoning TEXT,
    cluster_id INTEGER,
    tags JSON,
    embedding BLOB,
    fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);
CREATE INDEX IF NOT EXISTS idx_items_source ON items(source);
CREATE INDEX IF NOT EXISTS idx_items_fetched_at ON items(fetched_at);

CREATE TABLE IF NOT EXISTS transcripts (
    item_id INTEGER PRIMARY KEY REFERENCES items(id),
    transcript_text TEXT,
    frames_dir TEXT,
    watch_summary TEXT,
    watched_at TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items(id),
    skill_name TEXT NOT NULL,
    skill_path TEXT NOT NULL,
    skill_md TEXT,
    generated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prototypes (
    id INTEGER PRIMARY KEY,
    skill_id INTEGER REFERENCES skills(id),
    repo_path TEXT NOT NULL,
    deck_path TEXT,
    runs_successfully INTEGER,
    notes TEXT,
    built_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS star_snapshots (
    repo TEXT,
    stars INTEGER,
    snapshot_date TEXT,
    PRIMARY KEY (repo, snapshot_date)
);

CREATE TABLE IF NOT EXISTS digests (
    id INTEGER PRIMARY KEY,
    digest_date TEXT UNIQUE,
    brief_md TEXT,
    github_issue_url TEXT,
    email_sent_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS research_runs (
    id INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,
    audience TEXT,
    duration_min INTEGER,
    depth TEXT,
    output_dir TEXT,
    item_ids_used JSON,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def url_hash(url: str) -> str:
    return hashlib.sha256(url.strip().lower().encode()).hexdigest()


def init_db(db_path: Path | str | None = None) -> Path:
    p = Path(db_path or DB_PATH)
    p.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(p) as conn:
        conn.executescript(SCHEMA)
        conn.commit()
    return p


@contextmanager
def get_conn(db_path: Path | str | None = None) -> Iterator[sqlite3.Connection]:
    p = init_db(db_path)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def insert_item(
    conn: sqlite3.Connection,
    *,
    url: str,
    source: str,
    title: str | None = None,
    author: str | None = None,
    published_at: str | None = None,
    raw_metadata: dict | None = None,
) -> int | None:
    """Insert an item; returns row id, or None if duplicate."""
    h = url_hash(url)
    try:
        cur = conn.execute(
            """
            INSERT INTO items (url, url_hash, source, title, author, published_at, raw_metadata, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'new')
            """,
            (
                url,
                h,
                source,
                title,
                author,
                published_at,
                json.dumps(raw_metadata or {}, ensure_ascii=False),
            ),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def update_status(conn: sqlite3.Connection, item_id: int, status: str) -> None:
    conn.execute("UPDATE items SET status = ? WHERE id = ?", (status, item_id))
    conn.commit()


def update_score(
    conn: sqlite3.Connection,
    item_id: int,
    *,
    score: float,
    reasoning: str | None,
    tags: list[str] | None,
    status: str = "scored",
) -> None:
    conn.execute(
        "UPDATE items SET score = ?, score_reasoning = ?, tags = ?, status = ? WHERE id = ?",
        (score, reasoning, json.dumps(tags or []), status, item_id),
    )
    conn.commit()


def get_items_by_status(
    conn: sqlite3.Connection, status: str, limit: int | None = None
) -> list[sqlite3.Row]:
    sql = "SELECT * FROM items WHERE status = ? ORDER BY fetched_at DESC"
    params: tuple = (status,)
    if limit is not None:
        sql += " LIMIT ?"
        params = (status, limit)
    return list(conn.execute(sql, params).fetchall())


def get_recent_items(conn: sqlite3.Connection, hours: int = 24) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            "SELECT * FROM items WHERE fetched_at >= datetime('now', ?) ORDER BY score DESC NULLS LAST, fetched_at DESC",
            (f"-{hours} hours",),
        ).fetchall()
    )


def get_item(conn: sqlite3.Connection, item_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()


def save_transcript(
    conn: sqlite3.Connection,
    item_id: int,
    *,
    transcript_text: str | None,
    frames_dir: str | None,
    watch_summary: str | None,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT OR REPLACE INTO transcripts
            (item_id, transcript_text, frames_dir, watch_summary, watched_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (item_id, transcript_text, frames_dir, watch_summary, now),
    )
    conn.commit()


def get_transcript(conn: sqlite3.Connection, item_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM transcripts WHERE item_id = ?", (item_id,)
    ).fetchone()


def insert_skill(
    conn: sqlite3.Connection,
    *,
    item_id: int,
    skill_name: str,
    skill_path: str,
    skill_md: str | None,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO skills (item_id, skill_name, skill_path, skill_md)
        VALUES (?, ?, ?, ?)
        """,
        (item_id, skill_name, skill_path, skill_md),
    )
    conn.commit()
    return cur.lastrowid  # type: ignore[return-value]


def insert_prototype(
    conn: sqlite3.Connection,
    *,
    skill_id: int,
    repo_path: str,
    deck_path: str | None,
    runs_successfully: bool,
    notes: str | None,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO prototypes (skill_id, repo_path, deck_path, runs_successfully, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (skill_id, repo_path, deck_path, int(bool(runs_successfully)), notes),
    )
    conn.commit()
    return cur.lastrowid  # type: ignore[return-value]


def insert_digest(
    conn: sqlite3.Connection,
    *,
    digest_date: str,
    brief_md: str,
    github_issue_url: str | None = None,
) -> int:
    cur = conn.execute(
        """
        INSERT OR REPLACE INTO digests (digest_date, brief_md, github_issue_url)
        VALUES (?, ?, ?)
        """,
        (digest_date, brief_md, github_issue_url),
    )
    conn.commit()
    return cur.lastrowid  # type: ignore[return-value]


def mark_digest_emailed(conn: sqlite3.Connection, digest_date: str) -> None:
    conn.execute(
        "UPDATE digests SET email_sent_at = datetime('now') WHERE digest_date = ?",
        (digest_date,),
    )
    conn.commit()


def snapshot_stars(conn: sqlite3.Connection, repo: str, stars: int) -> None:
    today = datetime.now(timezone.utc).date().isoformat()
    conn.execute(
        "INSERT OR REPLACE INTO star_snapshots (repo, stars, snapshot_date) VALUES (?, ?, ?)",
        (repo, stars, today),
    )
    conn.commit()


def star_velocity(conn: sqlite3.Connection, repo: str) -> int | None:
    """Δ stars between today and yesterday's snapshot, if both exist."""
    rows = conn.execute(
        "SELECT stars, snapshot_date FROM star_snapshots WHERE repo = ? ORDER BY snapshot_date DESC LIMIT 2",
        (repo,),
    ).fetchall()
    if len(rows) < 2:
        return None
    return rows[0]["stars"] - rows[1]["stars"]


def insert_research_run(
    conn: sqlite3.Connection,
    *,
    topic: str,
    audience: str | None,
    duration_min: int | None,
    depth: str,
    output_dir: str,
    item_ids_used: Iterable[int],
) -> int:
    cur = conn.execute(
        """
        INSERT INTO research_runs (topic, audience, duration_min, depth, output_dir, item_ids_used)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            topic,
            audience,
            duration_min,
            depth,
            output_dir,
            json.dumps(list(item_ids_used)),
        ),
    )
    conn.commit()
    return cur.lastrowid  # type: ignore[return-value]


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    d = dict(row)
    for k in ("raw_metadata", "tags"):
        if k in d and isinstance(d[k], str) and d[k]:
            try:
                d[k] = json.loads(d[k])
            except json.JSONDecodeError:
                pass
    return d
