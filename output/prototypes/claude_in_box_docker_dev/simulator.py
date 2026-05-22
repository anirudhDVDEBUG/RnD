"""
simulator.py — Claude-in-Box management UI simulator.

Starts a local HTTP server that mimics the claude-in-box web management
interface: session CRUD, real-time output, hook configuration, and resource
monitoring.  No Docker or API keys required — uses mock data throughout.
"""

import json
import http.server
import socketserver
import textwrap
import time
import sys
from session_manager import SessionManager, SessionState
from hook_engine import HookEngine

# ── Globals ──────────────────────────────────────────────────────────────
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9080
hook_engine = HookEngine()


def on_session_event(event, session, detail=""):
    hook_engine.fire(event, session.id, detail)


mgr = SessionManager(on_event=on_session_event)

# ── Seed demo sessions ──────────────────────────────────────────────────
DEMO_OUTPUTS = {
    "frontend-refactor": [
        "$ claude --model opus 'Refactor React components to use hooks'",
        "[session] Workspace: /workspace/frontend-refactor_a1b2c3",
        "[claude] Analyzing 47 component files...",
        "[claude] Converting class components: UserProfile, Dashboard, Settings",
        "[claude] 12/47 components converted to functional + hooks",
        "[hook:resource-monitor] Memory: 62MB | CPU: 4.2%",
    ],
    "api-bugfix": [
        "$ claude 'Fix the 500 error on /api/orders endpoint'",
        "[session] Workspace: /workspace/api-bugfix_d4e5f6",
        "[claude] Reading server/routes/orders.ts ...",
        "[claude] Found null-pointer on line 142: order.customer?.address",
        "[claude] Applying fix + adding regression test",
        "[hook:resource-monitor] Memory: 51MB | CPU: 3.1%",
    ],
    "docs-generator": [
        "$ claude 'Generate API documentation from OpenAPI spec'",
        "[session] Workspace: /workspace/docs-generator_g7h8i9",
        "[claude] Parsing openapi.yaml (87 endpoints)",
        "[claude] Generating markdown docs for v2 API",
        "[claude] Writing output to docs/api-reference.md",
        "[hook:resource-monitor] Memory: 38MB | CPU: 1.8%",
    ],
}


def seed_sessions():
    for name, outputs in DEMO_OUTPUTS.items():
        s = mgr.create_session(name)
        mgr.start_session(s.id)
        for line in outputs:
            mgr.append_output(s.id, line)
        # Add a per-session hook
        mgr.add_hook(s.id, "session.stopped", f"echo '{name} session ended' >> /var/log/claude.log")


# ── HTML UI ──────────────────────────────────────────────────────────────
def render_html():
    sessions = mgr.list_sessions()
    stats = mgr.get_stats()
    hooks = hook_engine.list_rules()
    history = hook_engine.get_history()

    session_rows = ""
    for s in sessions:
        state_color = "#22c55e" if s.state == SessionState.RUNNING else "#ef4444"
        output_preview = s.output_lines[-1] if s.output_lines else "(no output)"
        session_rows += f"""
        <div class="card">
          <div class="card-header">
            <span class="badge" style="background:{state_color}">{s.state.value.upper()}</span>
            <strong>{s.name}</strong>
            <span class="dim">id:{s.id}</span>
          </div>
          <div class="card-meta">
            Workspace: <code>{s.workspace}</code> |
            Mem: {s.memory_mb:.0f}MB | CPU: {s.cpu_pct:.1f}% |
            Uptime: {time.time() - s.started_at:.0f}s |
            Hooks: {sum(len(v) for v in s.hooks.values())}
          </div>
          <div class="terminal">{'<br>'.join(s.output_lines)}</div>
        </div>"""

    hook_rows = "".join(
        f"<tr><td>{h['name']}</td><td><code>{h['pattern']}</code></td><td>{h['action']}</td></tr>"
        for h in hooks
    )
    history_rows = "".join(
        f"<tr><td>{h['hook']}</td><td>{h['event']}</td><td>{h['session'][:8]}</td>"
        f"<td>{h['duration_ms']}ms</td></tr>"
        for h in history[-10:]
    )

    return textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html><head>
    <meta charset="utf-8"><title>Claude-in-Box Management UI</title>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
             background:#0f172a; color:#e2e8f0; padding:24px; }}
      h1 {{ font-size:1.5rem; margin-bottom:4px; }}
      .subtitle {{ color:#94a3b8; margin-bottom:20px; }}
      .stats {{ display:flex; gap:16px; margin-bottom:24px; flex-wrap:wrap; }}
      .stat {{ background:#1e293b; padding:16px 24px; border-radius:8px; min-width:140px; }}
      .stat .val {{ font-size:1.8rem; font-weight:700; color:#38bdf8; }}
      .stat .label {{ font-size:0.8rem; color:#94a3b8; text-transform:uppercase; }}
      .card {{ background:#1e293b; border-radius:8px; padding:16px; margin-bottom:16px;
               border-left:3px solid #38bdf8; }}
      .card-header {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
      .card-meta {{ font-size:0.8rem; color:#94a3b8; margin-bottom:10px; }}
      .badge {{ padding:2px 8px; border-radius:4px; font-size:0.7rem; color:#fff; font-weight:600; }}
      .dim {{ color:#64748b; font-size:0.8rem; }}
      .terminal {{ background:#020617; padding:12px; border-radius:4px; font-family:monospace;
                   font-size:0.8rem; color:#22d3ee; line-height:1.6; max-height:180px; overflow-y:auto; }}
      h2 {{ font-size:1.1rem; margin:24px 0 12px; color:#38bdf8; }}
      table {{ width:100%; border-collapse:collapse; background:#1e293b; border-radius:8px; overflow:hidden; }}
      th {{ text-align:left; padding:10px 14px; background:#334155; font-size:0.8rem;
           text-transform:uppercase; color:#94a3b8; }}
      td {{ padding:8px 14px; border-top:1px solid #334155; font-size:0.85rem; }}
      code {{ background:#334155; padding:2px 6px; border-radius:3px; font-size:0.8rem; }}
      .footer {{ margin-top:32px; text-align:center; color:#475569; font-size:0.75rem; }}
    </style>
    </head><body>
    <h1>Claude-in-Box Management UI</h1>
    <p class="subtitle">Portable Docker Dev Environment &mdash; Simulator Mode</p>

    <div class="stats">
      <div class="stat"><div class="val">{stats['total_sessions']}</div><div class="label">Sessions</div></div>
      <div class="stat"><div class="val">{stats['running']}</div><div class="label">Running</div></div>
      <div class="stat"><div class="val">{stats['total_memory_mb']:.0f} MB</div><div class="label">Memory</div></div>
      <div class="stat"><div class="val">{stats['total_cpu_pct']:.1f}%</div><div class="label">CPU</div></div>
    </div>

    <h2>Active Sessions</h2>
    {session_rows}

    <h2>Hook Rules</h2>
    <table>
      <tr><th>Name</th><th>Pattern</th><th>Action</th></tr>
      {hook_rows}
    </table>

    <h2>Hook Execution Log</h2>
    <table>
      <tr><th>Hook</th><th>Event</th><th>Session</th><th>Duration</th></tr>
      {history_rows}
    </table>

    <h2>API Endpoints</h2>
    <table>
      <tr><th>Method</th><th>Path</th><th>Description</th></tr>
      <tr><td>GET</td><td><code>/</code></td><td>Web management UI (this page)</td></tr>
      <tr><td>GET</td><td><code>/api/sessions</code></td><td>List all sessions as JSON</td></tr>
      <tr><td>GET</td><td><code>/api/stats</code></td><td>Resource usage summary</td></tr>
      <tr><td>GET</td><td><code>/api/hooks</code></td><td>Hook rules and execution history</td></tr>
    </table>

    <div class="footer">claude-in-box simulator &mdash; no Docker or API key required</div>
    </body></html>""")


# ── HTTP Handler ─────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/sessions":
            self._json([s.to_dict() for s in mgr.list_sessions()])
        elif self.path == "/api/stats":
            self._json(mgr.get_stats())
        elif self.path == "/api/hooks":
            self._json({"rules": hook_engine.list_rules(), "history": hook_engine.get_history()})
        else:
            self._html(render_html())

    def _json(self, data):
        body = json.dumps(data, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # silence per-request logs


# ── Main ─────────────────────────────────────────────────────────────────
def print_summary():
    """Print CLI summary before starting server."""
    stats = mgr.get_stats()
    print("=" * 64)
    print("  CLAUDE-IN-BOX  |  Portable Docker Dev Environment Simulator")
    print("=" * 64)
    print()
    print(f"  Sessions: {stats['total_sessions']}  |  "
          f"Running: {stats['running']}  |  "
          f"Memory: {stats['total_memory_mb']:.0f} MB  |  "
          f"CPU: {stats['total_cpu_pct']:.1f}%")
    print()

    for s in mgr.list_sessions():
        state_icon = "+" if s.state == SessionState.RUNNING else "-"
        print(f"  [{state_icon}] {s.name:<22} id:{s.id}  mem:{s.memory_mb:.0f}MB  "
              f"cpu:{s.cpu_pct:.1f}%")
        print(f"      workspace: {s.workspace}")
        if s.output_lines:
            print(f"      last output: {s.output_lines[-1]}")
        print()

    print("-" * 64)
    print("  Hook Rules:")
    for r in hook_engine.list_rules():
        print(f"    {r['name']:<22} {r['pattern']:<18} {r['action']}")
    print()
    print("-" * 64)
    print(f"  Hook executions fired: {len(hook_engine.get_history(limit=100))}")
    print()
    history = hook_engine.get_history(limit=5)
    for h in history:
        print(f"    [{h['hook']}] {h['event']} -> session:{h['session'][:8]}  "
              f"({h['duration_ms']}ms)")
    print()


def main():
    seed_sessions()
    print_summary()

    serve = "--serve" in sys.argv
    if serve:
        print(f"  Web UI: http://localhost:{PORT}")
        print(f"  API:    http://localhost:{PORT}/api/sessions")
        print(f"          http://localhost:{PORT}/api/stats")
        print(f"          http://localhost:{PORT}/api/hooks")
        print()
        print("  Press Ctrl+C to stop.")
        print("=" * 64)
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.allow_reuse_address = True
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n  Shutting down.")
    else:
        print("  Run with --serve to start the web management UI.")
        print(f"  Example: python simulator.py --serve")
        print("=" * 64)


if __name__ == "__main__":
    main()
