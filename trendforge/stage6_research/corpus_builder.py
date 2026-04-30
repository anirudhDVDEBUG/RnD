"""Build a research corpus from the local DB + live GitHub + (optionally) web search."""
from __future__ import annotations

import logging
from typing import Iterable

from trendforge import embeddings, store
from trendforge.stage1_ingest.github_fetcher import search_repositories, search_to_items

log = logging.getLogger(__name__)


def db_search(facets: Iterable[str], per_facet: int = 10) -> list[dict]:
    """k-NN over local items for each facet; dedup by id."""
    seen: set[int] = set()
    out: list[dict] = []
    for f in facets:
        hits = embeddings.search(f, k=per_facet)
        with store.get_conn() as conn:
            for iid, sim in hits:
                if iid in seen:
                    continue
                row = store.get_item(conn, iid)
                if not row:
                    continue
                d = store.row_to_dict(row) or {}
                d["_similarity"] = sim
                d["_facet"] = f
                out.append(d)
                seen.add(iid)
    return out


def github_search(facets: Iterable[str], per_facet: int = 10) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for f in facets:
        repos = search_repositories(f, sort="stars", per_page=per_facet)
        for it in search_to_items(repos):
            url = it.get("url")
            if not url or url in seen:
                continue
            it["_facet"] = f
            it["_source_kind"] = "github_live"
            out.append(it)
            seen.add(url)
    return out


def build_corpus(facets: list[str], depth: str = "standard") -> dict:
    """Returns {'db': [...], 'github': [...], 'facets': [...]}.

    Live web search is left to the synthesizer step (where Claude has
    access to the WebSearch tool natively).
    """
    per_facet = {"quick": 5, "standard": 10, "deep": 20}.get(depth, 10)
    db_items = db_search(facets, per_facet=per_facet)
    if depth == "quick":
        return {"db": db_items, "github": [], "facets": facets}
    gh = github_search(facets, per_facet=max(5, per_facet // 2))
    return {"db": db_items, "github": gh, "facets": facets}
