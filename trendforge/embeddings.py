"""Lightweight embedding helpers — used by Mode B for k-NN retrieval.

We avoid heavyweight model deps (sentence-transformers, FAISS) and use a
hashed-bag-of-tokens cosine sim. It's not state-of-the-art but it works
out of the box with zero install footprint and is plenty for a 90-day
DB that already has Claude-generated tags.
"""
from __future__ import annotations

import math
import re
import struct
from typing import Iterable

import sqlite3

from trendforge import store

DIM = 256
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]+")


def _tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text or "")]


def embed(text: str) -> list[float]:
    """Hashed bag-of-tokens with L2 normalization."""
    vec = [0.0] * DIM
    for tok in _tokens(text):
        h = hash(tok) % DIM
        vec[h] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def to_blob(vec: list[float]) -> bytes:
    return struct.pack(f"{DIM}f", *vec)


def from_blob(blob: bytes) -> list[float]:
    return list(struct.unpack(f"{DIM}f", blob))


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def text_for_item(row: dict) -> str:
    parts = [
        row.get("title") or "",
        " ".join(row.get("tags") or []),
    ]
    md = row.get("raw_metadata") or {}
    parts.append(str(md.get("summary", "")))
    parts.append(str(md.get("description", "")))
    parts.append(" ".join(md.get("topics", []) or []))
    return " ".join(parts)


def backfill_embeddings(db_path=None, batch: int = 500) -> int:
    """Compute embeddings for any item that doesn't have one yet."""
    db = db_path or store.DB_PATH
    n = 0
    with store.get_conn(db) as conn:
        rows = conn.execute(
            "SELECT id, title, raw_metadata, tags FROM items WHERE embedding IS NULL"
        ).fetchall()
        for r in rows:
            d = store.row_to_dict(r) or {}
            vec = embed(text_for_item(d))
            conn.execute(
                "UPDATE items SET embedding = ? WHERE id = ?",
                (to_blob(vec), r["id"]),
            )
            n += 1
            if n % batch == 0:
                conn.commit()
        conn.commit()
    return n


def search(query: str, *, db_path=None, k: int = 30,
           tags_any: list[str] | None = None) -> list[tuple[int, float]]:
    """Return top-k (item_id, similarity) for a free-text query."""
    db = db_path or store.DB_PATH
    qvec = embed(query)
    out: list[tuple[int, float]] = []
    with store.get_conn(db) as conn:
        sql = "SELECT id, embedding, tags FROM items WHERE embedding IS NOT NULL"
        rows = conn.execute(sql).fetchall()
        for r in rows:
            if r["embedding"] is None:
                continue
            if tags_any:
                row_tags = []
                if r["tags"]:
                    try:
                        import json
                        row_tags = json.loads(r["tags"])
                    except Exception:
                        row_tags = []
                if not any(t in row_tags for t in tags_any):
                    continue
            v = from_blob(r["embedding"])
            sim = cosine(qvec, v)
            out.append((r["id"], sim))
    out.sort(key=lambda x: x[1], reverse=True)
    return out[:k]
