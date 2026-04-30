"""Send the firehose email digest to anirudh.royyuru@gmail.com.

Best-effort: if SMTP fails, we log and move on. The brief and the GitHub
issue still exist regardless.
"""
from __future__ import annotations

import logging
import os
import smtplib
from collections import defaultdict
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from trendforge import store
from trendforge.config_loader import DIGEST_RECIPIENT, load_dotenv
from trendforge.stage2_distill.brief import one_line

log = logging.getLogger(__name__)


SOURCE_LABELS = {
    "rss": "ANTHROPIC / RSS",
    "github": "GITHUB TRENDING",
    "hn": "HACKER NEWS",
    "youtube": "YOUTUBE",
    "awesome_list": "AWESOME LISTS",
}


def build_email_body(items_by_source: dict[str, list[dict]],
                     top_picks: set[int],
                     github_issue_url: str | None) -> str:
    today = date.today().isoformat()
    total = sum(len(v) for v in items_by_source.values())
    n_proto = sum(1 for v in items_by_source.values() for it in v if it["id"] in top_picks)
    lines = [
        "Hi Anirudh,",
        "",
        "Here's everything TrendForge picked up in the last 24 hours.",
        "* = top picks (full prototypes built, see GitHub issue)",
        "",
    ]
    for src in ("rss", "github", "hn", "youtube", "awesome_list"):
        items = items_by_source.get(src, [])
        if not items:
            continue
        label = SOURCE_LABELS.get(src, src.upper())
        lines.append(f"== {label} ({len(items)}) ==")
        for it in items[:30]:  # cap per section
            star = "* " if it["id"] in top_picks else "  "
            lines.append(f"{star}{one_line(it)}")
            lines.append(f"      {it['url']}")
        if len(items) > 30:
            lines.append(f"  ... and {len(items) - 30} more")
        lines.append("")

    lines.append("-" * 32)
    if github_issue_url:
        lines.append(f"Full brief & prototypes: {github_issue_url}")
    else:
        lines.append("Full brief: output/briefs/" + today + ".md")
    lines.append("")
    lines.append("- TrendForge")
    return "\n".join(lines)


def send_daily_email(github_issue_url: str | None = None,
                     digest_date: str | None = None,
                     db_path=None) -> bool:
    load_dotenv()
    sender = os.environ.get("GMAIL_SENDER")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not sender or not password:
        log.warning("GMAIL_SENDER / GMAIL_APP_PASSWORD not set — skipping email")
        return False

    today = digest_date or date.today().isoformat()
    db = db_path or store.DB_PATH
    with store.get_conn(db) as conn:
        recent = [store.row_to_dict(r) for r in store.get_recent_items(conn, hours=24)]
        recent = [r for r in recent if r is not None]
        # Top picks = items that became skills today
        top_ids = {
            r["item_id"]
            for r in conn.execute(
                "SELECT item_id FROM skills WHERE date(generated_at) = date(?)", (today,)
            ).fetchall()
        }

    items_by_source: dict[str, list[dict]] = defaultdict(list)
    for it in recent:
        items_by_source[it["source"]].append(it)

    body = build_email_body(items_by_source, top_ids, github_issue_url)
    total = len(recent)
    msg = MIMEMultipart()
    msg["Subject"] = f"TrendForge Daily — {today} — {total} new items ({len(top_ids)} prototyped)"
    msg["From"] = sender
    msg["To"] = DIGEST_RECIPIENT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
    except Exception as e:
        log.warning("SMTP send failed: %s", e)
        return False

    with store.get_conn(db) as conn:
        store.mark_digest_emailed(conn, today)
    log.info("Emailed digest to %s", DIGEST_RECIPIENT)
    return True
