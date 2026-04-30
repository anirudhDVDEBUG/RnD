"""Smoke tests — verify storage and config plumbing."""
from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

import pytest

from trendforge import store
from trendforge.config_loader import (
    load_interests,
    load_sources,
    load_watched_repos,
)


def test_init_db_creates_tables(tmp_path):
    db = tmp_path / "test.db"
    store.init_db(db)
    with sqlite3.connect(db) as conn:
        names = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    expected = {
        "items",
        "transcripts",
        "skills",
        "prototypes",
        "star_snapshots",
        "digests",
        "research_runs",
    }
    assert expected.issubset(names)


def test_insert_item_dedupes(tmp_path):
    db = tmp_path / "test.db"
    with store.get_conn(db) as conn:
        a = store.insert_item(conn, url="https://example.com/x", source="rss", title="X")
        b = store.insert_item(conn, url="https://example.com/x", source="rss", title="X")
    assert a is not None
    assert b is None  # dup


def test_status_transitions(tmp_path):
    db = tmp_path / "test.db"
    with store.get_conn(db) as conn:
        item_id = store.insert_item(
            conn, url="https://example.com/y", source="rss", title="Y"
        )
        assert item_id is not None
        store.update_score(
            conn, item_id, score=0.8, reasoning="match", tags=["agent"]
        )
        scored = store.get_items_by_status(conn, "scored")
        assert len(scored) == 1
        assert scored[0]["score"] == 0.8


def test_load_sources():
    cfg = load_sources()
    assert "rss" in cfg
    assert isinstance(cfg["rss"], list) and len(cfg["rss"]) > 0


def test_load_interests():
    cfg = load_interests()
    assert "high_signal_keywords" in cfg
    assert "active_projects" in cfg


def test_load_watched_repos():
    repos = load_watched_repos()
    assert isinstance(repos, list)
    assert len(repos) > 0


def test_url_hash_stable():
    a = store.url_hash("https://example.com/PATH")
    b = store.url_hash("https://example.com/path")
    assert a == b  # case-insensitive
