"""Mode B CLI entry point: research mode."""
from __future__ import annotations

import argparse
import json
import logging
import re
from datetime import date
from pathlib import Path

from trendforge import embeddings, store
from trendforge.config_loader import load_dotenv
from trendforge.stage6_research import (
    build_corpus,
    build_slides_and_notes,
    expand,
    predict_qa,
    synthesize,
)

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "output" / "research"


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s[:60] or "topic"


def run_research(topic: str, audience: str | None, duration: int | None,
                 depth: str = "standard", db_path=None) -> Path:
    load_dotenv()

    today = date.today().isoformat()
    slug = f"{today}_{slugify(topic)}"
    out = RESEARCH_DIR / slug
    out.mkdir(parents=True, exist_ok=True)

    log.info("Backfilling embeddings...")
    embeddings.backfill_embeddings(db_path=db_path)

    log.info("Expanding topic...")
    facets = expand(topic)
    (out / "facets.json").write_text(json.dumps(facets, indent=2), encoding="utf-8")

    log.info("Building corpus (%d facets, depth=%s)...", len(facets), depth)
    corpus = build_corpus(facets, depth=depth)

    item_ids_used = [it["id"] for it in corpus.get("db", []) if it.get("id") is not None]
    sources_manifest = {
        "topic": topic,
        "audience": audience,
        "duration": duration,
        "depth": depth,
        "facets": facets,
        "db_items": [
            {"id": it.get("id"), "url": it.get("url"), "title": it.get("title"),
             "similarity": it.get("_similarity")}
            for it in corpus.get("db", [])
        ],
        "github": [
            {"url": it.get("url"), "title": it.get("title")}
            for it in corpus.get("github", [])
        ],
    }
    (out / "sources.json").write_text(
        json.dumps(sources_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    log.info("Synthesizing dossier...")
    dossier_path = synthesize(topic, audience, duration, corpus, out)

    if depth != "quick":
        log.info("Building slides + notes...")
        build_slides_and_notes(dossier_path, out, topic, audience, duration)
        log.info("Predicting Q&A...")
        predict_qa(topic, audience, dossier_path, out)

    with store.get_conn(db_path) as conn:
        store.insert_research_run(
            conn,
            topic=topic,
            audience=audience,
            duration_min=duration,
            depth=depth,
            output_dir=str(out),
            item_ids_used=item_ids_used,
        )

    log.info("Research complete: %s", out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="TrendForge Mode B — research")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", default=None)
    parser.add_argument("--duration", type=int, default=30)
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    out = run_research(
        topic=args.topic,
        audience=args.audience,
        duration=args.duration,
        depth=args.depth,
    )
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
