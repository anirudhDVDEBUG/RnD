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
from trendforge.topics import classify, topic_label, all_topic_slugs

log = logging.getLogger(__name__)


def build_email_body(selected_by_topic: dict[str, list[dict]],
                     top_picks: set[int],
                     github_issue_url: str | None,
                     total_ingested: int) -> str:
    today = date.today().isoformat()
    n_picks = sum(len([i for i in v if i["id"] in top_picks])
                  for v in selected_by_topic.values())
    n_selected = sum(len(v) for v in selected_by_topic.values())

    lines = [
        "Hi Anirudh,",
        "",
        f"TrendForge — {today}. {total_ingested} items ingested, "
        f"{n_selected} selected across topics, {n_picks} got full mini-repos.",
        "* = full mini-repo (SKILL + HOW_TO_USE + TECH_DETAILS + demo)",
        "",
    ]

    # Render in topic order from interests.yaml
    for slug in all_topic_slugs():
        items = selected_by_topic.get(slug, [])
        if not items:
            continue
        lbl = topic_label(slug)
        lines.append(f"== {lbl} ({len(items)}) ==")
        for it in items:
            star = "* " if it["id"] in top_picks else "  "
            score = float(it.get("score") or 0)
            lines.append(f"{star}[{score:.2f}] {one_line(it)}")
            lines.append(f"      {it['url']}")
        lines.append("")

    lines.append("-" * 32)
    if github_issue_url:
        lines.append(f"Full brief & mini-repos: {github_issue_url}")
    lines.append("Vault: anirudhDVDEBUG/RnD/topics/  (open as Obsidian or browse on GitHub)")
    lines.append("Graph: anirudhDVDEBUG/RnD/output/graph.html")
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
        # Selected = items the per-topic top-K logic kept this morning
        selected = [
            store.row_to_dict(r)
            for r in conn.execute(
                """SELECT * FROM items
                   WHERE status IN ('selected','watched','skillified')
                     AND date(fetched_at) = date(?)""",
                (today,),
            ).fetchall()
        ]
        selected = [s for s in selected if s is not None]
        # Top picks = items that got a full mini-repo (skill row exists today)
        top_ids = {
            r["item_id"]
            for r in conn.execute(
                "SELECT item_id FROM skills WHERE date(generated_at) = date(?)", (today,)
            ).fetchall()
        }

    by_topic: dict[str, list[dict]] = defaultdict(list)
    for it in selected:
        by_topic[classify(it)].append(it)
    # sort each topic by score desc
    for k in by_topic:
        by_topic[k].sort(key=lambda i: float(i.get("score") or 0), reverse=True)

    body = build_email_body(by_topic, top_ids, github_issue_url, total_ingested=len(recent))
    total = len(recent)
    msg = MIMEMultipart()
    n_topics = len(by_topic)
    msg["Subject"] = (f"TrendForge — {today} — {len(selected)} picks across "
                      f"{n_topics} topics ({len(top_ids)} mini-repos)")
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
