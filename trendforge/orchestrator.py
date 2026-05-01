"""Mode A orchestrator — runs the full daily pipeline."""
from __future__ import annotations

import argparse
import logging
import os
from datetime import date
from pathlib import Path

from trendforge import store
from trendforge.config_loader import load_dotenv

log = logging.getLogger(__name__)


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def run(dry_run: bool = False, top_k: int = 5, skip_video: bool = False,
        skip_skill: bool = False, skip_email: bool = False) -> dict:
    load_dotenv()
    # Force Max-plan auth for any Claude subprocess.
    os.environ.pop("ANTHROPIC_API_KEY", None)

    summary: dict = {"dry_run": dry_run, "date": date.today().isoformat()}

    # Stage 1
    from trendforge.stage1_ingest import run_ingest
    summary["ingest"] = run_ingest()

    # Stage 2 (score; tagging via Claude can be skipped if claude CLI absent)
    from trendforge.stage2_distill import run_distill
    summary["selected"] = run_distill(top_k=top_k)

    # Stage 2.5 — watch videos
    if not skip_video:
        from trendforge.stage2_5_watch import watch_selected
        summary["watched"] = watch_selected()
    else:
        # Promote selected -> watched without doing anything
        with store.get_conn() as conn:
            for r in store.get_items_by_status(conn, "selected"):
                store.update_status(conn, r["id"], "watched")
        summary["watched"] = 0

    # Stage 3 — skillify
    if not skip_skill:
        from trendforge.stage3_skillify import skillify_watched
        summary["skill_ids"] = skillify_watched()
    else:
        summary["skill_ids"] = []

    # Stage 4 — prototypes + decks
    if not skip_skill:
        from trendforge.stage4_prototype import build_prototypes, build_decks
        summary["prototypes"] = [str(p) for p in build_prototypes()]
        summary["decks"] = [str(p) for p in build_decks()]

    # Stage 5 — brief, GitHub issue, email
    from trendforge.stage5_digest import render_brief, open_issue, send_daily_email
    brief_text, top_item_ids = render_brief()
    summary["brief_chars"] = len(brief_text)
    summary["top_item_ids"] = top_item_ids

    # Cross-cutting: regenerate backlog + knowledge graph every run
    try:
        from trendforge import backlog, graphify
        backlog.write_markdown()
        graph_paths = graphify.write_all()
        summary["graph_nodes"] = sum(1 for _ in open(graph_paths["json"]))
    except Exception as e:
        log.warning("backlog/graphify regen failed: %s", e)

    if dry_run:
        log.info("DRY-RUN: skipping issue + email")
        return summary

    brief_path = Path("output/briefs") / f"{date.today().isoformat()}.md"
    issue_url = open_issue(brief_path)
    summary["github_issue_url"] = issue_url

    if not skip_email:
        emailed = send_daily_email(github_issue_url=issue_url)
        summary["email_sent"] = emailed
    else:
        summary["email_sent"] = False

    # Sticky backlog issue: upsert (create-or-edit) on every run.
    try:
        from trendforge import backlog
        backlog_url = backlog.upsert_github_issue()
        summary["backlog_issue_url"] = backlog_url
    except Exception as e:
        log.warning("backlog issue upsert failed: %s", e)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="TrendForge Mode A daily run")
    parser.add_argument("--dry-run", action="store_true",
                        help="Skip GitHub issue + email")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--skip-video", action="store_true",
                        help="Skip /watch step (faster, no Claude CLI required)")
    parser.add_argument("--skip-skill", action="store_true",
                        help="Skip skillify+prototype+deck (faster, no Claude CLI required)")
    parser.add_argument("--skip-email", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    configure_logging(args.log_level)
    summary = run(
        dry_run=args.dry_run,
        top_k=args.top_k,
        skip_video=args.skip_video,
        skip_skill=args.skip_skill,
        skip_email=args.skip_email,
    )
    log.info("Run summary: %s", summary)


if __name__ == "__main__":
    main()
