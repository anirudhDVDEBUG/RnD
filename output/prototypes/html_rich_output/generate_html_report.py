#!/usr/bin/env python3
"""
generate_html_report.py — Demonstrates the HTML Rich Output skill for Claude Code.

Takes structured data (mock code review findings) and produces a single
self-contained HTML file with:
  - Sticky navigation / table of contents
  - Color-coded severity badges
  - Collapsible detail sections
  - Inline SVG architecture diagram
  - Syntax-highlighted code snippets
  - Interactive filtering via vanilla JS
  - Responsive layout
"""

import json
import html
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Mock data — simulates what Claude would analyze from a real PR
# ---------------------------------------------------------------------------

MOCK_REVIEW = {
    "pr_title": "feat: add streaming response handler for /api/chat",
    "pr_number": 247,
    "author": "dev-alice",
    "files_changed": 6,
    "additions": 189,
    "deletions": 42,
    "findings": [
        {
            "severity": "critical",
            "file": "src/handlers/stream.py",
            "line": 34,
            "title": "Unbounded buffer on slow consumers",
            "description": "The asyncio.Queue has no maxsize, so a slow consumer will cause memory to grow without limit. Set maxsize and handle QueueFull.",
            "code": 'self.buffer = asyncio.Queue()  # no maxsize!',
            "suggestion": 'self.buffer = asyncio.Queue(maxsize=1024)',
        },
        {
            "severity": "warning",
            "file": "src/handlers/stream.py",
            "line": 78,
            "title": "Missing timeout on upstream read",
            "description": "await resp.content.read() can hang forever if the upstream stops sending. Wrap in asyncio.wait_for with a timeout.",
            "code": 'chunk = await resp.content.read(4096)',
            "suggestion": 'chunk = await asyncio.wait_for(\n    resp.content.read(4096), timeout=30\n)',
        },
        {
            "severity": "info",
            "file": "src/handlers/stream.py",
            "line": 12,
            "title": "Consider structured logging",
            "description": "print() calls should be replaced with logging.getLogger(__name__) for production observability.",
            "code": 'print(f"Stream started for {user_id}")',
            "suggestion": 'logger.info("Stream started", extra={"user_id": user_id})',
        },
        {
            "severity": "warning",
            "file": "src/models/chat.py",
            "line": 55,
            "title": "N+1 query in message history loader",
            "description": "Each message loads its attachments individually. Use a JOIN or prefetch_related to batch the query.",
            "code": 'for msg in messages:\n    msg.attachments = db.query(Attachment).filter_by(msg_id=msg.id).all()',
            "suggestion": 'messages = (\n    db.query(Message)\n    .options(joinedload(Message.attachments))\n    .filter_by(chat_id=chat_id)\n    .all()\n)',
        },
        {
            "severity": "info",
            "file": "tests/test_stream.py",
            "line": 1,
            "title": "No tests for error/reconnect paths",
            "description": "Tests cover the happy path but not upstream failures, client disconnects, or queue-full scenarios.",
            "code": "",
            "suggestion": "",
        },
        {
            "severity": "critical",
            "file": "src/handlers/auth.py",
            "line": 22,
            "title": "JWT secret loaded from environment without validation",
            "description": "If JWT_SECRET is unset, os.getenv returns None and signing silently uses an empty key. Fail fast on startup.",
            "code": 'SECRET = os.getenv("JWT_SECRET")',
            "suggestion": 'SECRET = os.environ["JWT_SECRET"]  # crash on startup if missing',
        },
    ],
    "summary": "This PR adds Server-Sent Events (SSE) streaming for the chat endpoint. The approach is sound, but there are two critical issues around memory safety and secret handling that must be fixed before merge.",
}

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

SEVERITY_COLORS = {
    "critical": {"bg": "#fde8e8", "border": "#e53e3e", "badge": "#c53030", "text": "#742a2a"},
    "warning":  {"bg": "#fefce8", "border": "#d69e2e", "badge": "#b7791f", "text": "#744210"},
    "info":     {"bg": "#ebf8ff", "border": "#3182ce", "badge": "#2b6cb0", "text": "#2a4365"},
}


def severity_icon(sev: str) -> str:
    icons = {"critical": "&#9888;", "warning": "&#9670;", "info": "&#9432;"}
    return icons.get(sev, "")


def build_html(review: dict) -> str:
    findings = review["findings"]
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITY_COLORS}
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Build findings HTML
    findings_html = []
    for i, f in enumerate(findings):
        sev = f["severity"]
        c = SEVERITY_COLORS[sev]
        code_block = ""
        if f["code"]:
            code_block = f"""
            <div class="code-section">
              <div class="code-label">Current</div>
              <pre><code>{html.escape(f['code'])}</code></pre>
            </div>"""
        suggestion_block = ""
        if f["suggestion"]:
            suggestion_block = f"""
            <div class="code-section suggestion">
              <div class="code-label">Suggested</div>
              <pre><code>{html.escape(f['suggestion'])}</code></pre>
            </div>"""

        file_link = f'<span class="file-path">{html.escape(f["file"])}:{f["line"]}</span>'
        findings_html.append(f"""
        <article class="finding" data-severity="{sev}" id="finding-{i}"
                 style="border-left: 4px solid {c['border']}; background: {c['bg']};">
          <div class="finding-header">
            <span class="badge" style="background:{c['badge']}">{severity_icon(sev)} {sev.upper()}</span>
            <strong>{html.escape(f['title'])}</strong>
          </div>
          <p class="finding-location">{file_link}</p>
          <details open>
            <summary>Details</summary>
            <p>{html.escape(f['description'])}</p>
            {code_block}
            {suggestion_block}
          </details>
        </article>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PR Review: {html.escape(review['pr_title'])}</title>
<style>
  :root {{
    --bg: #f7f8fa;
    --card-bg: #ffffff;
    --text: #1a202c;
    --muted: #718096;
    --border: #e2e8f0;
    --nav-bg: #2d3748;
  }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: var(--bg); color: var(--text); line-height: 1.6; }}
  header.top-bar {{
    position: sticky; top: 0; z-index: 100;
    background: var(--nav-bg); color: #fff; padding: 12px 24px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,.15);
  }}
  header.top-bar h1 {{ font-size: 1.1rem; font-weight: 600; }}
  header.top-bar .meta {{ font-size: .85rem; opacity: .8; }}
  main {{ max-width: 900px; margin: 0 auto; padding: 24px 16px; }}

  /* Summary card */
  .summary-card {{
    background: var(--card-bg); border-radius: 8px; padding: 20px 24px;
    margin-bottom: 24px; border: 1px solid var(--border);
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
  }}
  .summary-card h2 {{ font-size: 1rem; margin-bottom: 8px; }}
  .stats {{ display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; }}
  .stat {{ background: var(--bg); border-radius: 6px; padding: 8px 14px; font-size: .9rem; }}
  .stat strong {{ font-size: 1.2rem; display: block; }}

  /* SVG diagram */
  .diagram-section {{ margin-bottom: 24px; }}
  .diagram-section h2 {{ font-size: 1rem; margin-bottom: 12px; }}
  .diagram-wrapper {{
    background: var(--card-bg); border-radius: 8px; padding: 16px;
    border: 1px solid var(--border); overflow-x: auto;
  }}

  /* Filter bar */
  .filter-bar {{
    display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; align-items: center;
  }}
  .filter-bar label {{ font-size: .85rem; font-weight: 600; margin-right: 4px; }}
  .filter-btn {{
    border: 1px solid var(--border); background: var(--card-bg);
    border-radius: 20px; padding: 4px 14px; font-size: .82rem;
    cursor: pointer; transition: .15s;
  }}
  .filter-btn:hover {{ background: #edf2f7; }}
  .filter-btn.active {{ background: var(--nav-bg); color: #fff; border-color: var(--nav-bg); }}

  /* Findings */
  .finding {{
    border-radius: 8px; padding: 16px 20px; margin-bottom: 14px;
    transition: .2s;
  }}
  .finding.hidden {{ display: none; }}
  .finding-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }}
  .badge {{
    color: #fff; font-size: .7rem; font-weight: 700; padding: 2px 10px;
    border-radius: 12px; text-transform: uppercase; letter-spacing: .04em;
    white-space: nowrap;
  }}
  .finding-location {{ font-size: .82rem; color: var(--muted); margin-bottom: 6px; }}
  .file-path {{
    font-family: 'SF Mono', 'Fira Code', monospace; background: rgba(0,0,0,.06);
    padding: 1px 6px; border-radius: 4px; font-size: .8rem;
  }}
  details summary {{ cursor: pointer; font-size: .9rem; font-weight: 600; margin-bottom: 6px; }}
  details p {{ font-size: .9rem; margin-bottom: 10px; }}

  .code-section {{ margin-bottom: 10px; }}
  .code-label {{ font-size: .75rem; font-weight: 600; color: var(--muted); margin-bottom: 2px; }}
  .code-section pre {{
    background: #1a202c; color: #e2e8f0; padding: 12px 16px;
    border-radius: 6px; overflow-x: auto; font-size: .82rem; line-height: 1.5;
  }}
  .suggestion pre {{ background: #1c3a2a; color: #c6f6d5; }}

  /* Footer */
  footer {{ text-align: center; padding: 24px; font-size: .8rem; color: var(--muted); }}

  @media (max-width: 600px) {{
    header.top-bar {{ flex-direction: column; gap: 4px; }}
    .stats {{ flex-direction: column; }}
  }}
</style>
</head>
<body>
<header class="top-bar">
  <h1>PR #{review['pr_number']}: {html.escape(review['pr_title'])}</h1>
  <span class="meta">by @{html.escape(review['author'])} &middot; {review['files_changed']} files &middot; +{review['additions']} -{review['deletions']}</span>
</header>

<main>
  <section class="summary-card">
    <h2>Review Summary</h2>
    <p>{html.escape(review['summary'])}</p>
    <div class="stats">
      <div class="stat"><strong style="color:{SEVERITY_COLORS['critical']['badge']}">{counts['critical']}</strong>Critical</div>
      <div class="stat"><strong style="color:{SEVERITY_COLORS['warning']['badge']}">{counts['warning']}</strong>Warnings</div>
      <div class="stat"><strong style="color:{SEVERITY_COLORS['info']['badge']}">{counts['info']}</strong>Info</div>
    </div>
  </section>

  <section class="diagram-section">
    <h2>Data Flow: Streaming Architecture</h2>
    <div class="diagram-wrapper">
      <svg viewBox="0 0 780 170" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
        <!-- Boxes -->
        <rect x="10" y="55" width="130" height="60" rx="8" fill="#ebf8ff" stroke="#3182ce" stroke-width="2"/>
        <text x="75" y="82" text-anchor="middle" font-size="13" font-weight="600" fill="#2b6cb0">Client</text>
        <text x="75" y="100" text-anchor="middle" font-size="10" fill="#4a5568">SSE listener</text>

        <rect x="200" y="55" width="150" height="60" rx="8" fill="#fefce8" stroke="#d69e2e" stroke-width="2"/>
        <text x="275" y="82" text-anchor="middle" font-size="13" font-weight="600" fill="#b7791f">Stream Handler</text>
        <text x="275" y="100" text-anchor="middle" font-size="10" fill="#4a5568">asyncio.Queue</text>

        <rect x="410" y="55" width="150" height="60" rx="8" fill="#f0fff4" stroke="#38a169" stroke-width="2"/>
        <text x="485" y="82" text-anchor="middle" font-size="13" font-weight="600" fill="#276749">LLM API</text>
        <text x="485" y="100" text-anchor="middle" font-size="10" fill="#4a5568">upstream chunks</text>

        <rect x="620" y="55" width="140" height="60" rx="8" fill="#fde8e8" stroke="#e53e3e" stroke-width="2"/>
        <text x="690" y="82" text-anchor="middle" font-size="13" font-weight="600" fill="#c53030">Auth</text>
        <text x="690" y="100" text-anchor="middle" font-size="10" fill="#4a5568">JWT verify</text>

        <!-- Arrows -->
        <line x1="140" y1="85" x2="195" y2="85" stroke="#4a5568" stroke-width="2" marker-end="url(#arr)"/>
        <line x1="350" y1="85" x2="405" y2="85" stroke="#4a5568" stroke-width="2" marker-end="url(#arr)"/>
        <line x1="620" y1="75" x2="355" y2="75" stroke="#e53e3e" stroke-width="1.5" stroke-dasharray="6 3" marker-end="url(#arr-red)"/>
        <text x="490" y="68" text-anchor="middle" font-size="9" fill="#e53e3e">validates token</text>

        <!-- Markers -->
        <defs>
          <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <path d="M0,0 L8,3 L0,6 Z" fill="#4a5568"/>
          </marker>
          <marker id="arr-red" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <path d="M0,0 L8,3 L0,6 Z" fill="#e53e3e"/>
          </marker>
        </defs>

        <!-- Annotations -->
        <rect x="170" y="130" width="220" height="28" rx="4" fill="#fde8e8" stroke="#e53e3e" stroke-width="1"/>
        <text x="280" y="149" text-anchor="middle" font-size="10" fill="#c53030">&#9888; Queue unbounded (Critical #1)</text>
        <line x1="275" y1="115" x2="275" y2="130" stroke="#e53e3e" stroke-width="1" stroke-dasharray="3 2"/>
      </svg>
    </div>
  </section>

  <section>
    <div class="filter-bar">
      <label>Filter:</label>
      <button class="filter-btn active" data-filter="all">All ({len(findings)})</button>
      <button class="filter-btn" data-filter="critical">Critical ({counts['critical']})</button>
      <button class="filter-btn" data-filter="warning">Warning ({counts['warning']})</button>
      <button class="filter-btn" data-filter="info">Info ({counts['info']})</button>
    </div>

    {"".join(findings_html)}
  </section>
</main>

<footer>
  Generated by <strong>html_rich_output</strong> skill demo &middot; {generated}
</footer>

<script>
(function() {{
  const btns = document.querySelectorAll('.filter-btn');
  const items = document.querySelectorAll('.finding');
  btns.forEach(btn => {{
    btn.addEventListener('click', () => {{
      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;
      items.forEach(el => {{
        el.classList.toggle('hidden', f !== 'all' && el.dataset.severity !== f);
      }});
    }});
  }});
}})();
</script>
</body>
</html>"""


def main():
    out_path = Path(__file__).parent / "pr_review_output.html"
    html_content = build_html(MOCK_REVIEW)
    out_path.write_text(html_content, encoding="utf-8")
    print(f"[html_rich_output] Generated: {out_path}")
    print(f"[html_rich_output] File size: {out_path.stat().st_size:,} bytes")
    print(f"[html_rich_output] Findings: {len(MOCK_REVIEW['findings'])} "
          f"({sum(1 for f in MOCK_REVIEW['findings'] if f['severity']=='critical')} critical, "
          f"{sum(1 for f in MOCK_REVIEW['findings'] if f['severity']=='warning')} warning, "
          f"{sum(1 for f in MOCK_REVIEW['findings'] if f['severity']=='info')} info)")
    print()
    print("Open in a browser:")
    print(f"  xdg-open {out_path}   # Linux")
    print(f"  open {out_path}       # macOS")


if __name__ == "__main__":
    main()
