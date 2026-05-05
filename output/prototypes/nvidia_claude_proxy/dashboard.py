"""Analytics dashboard for nvidia_claude_proxy."""

from flask import render_template_string

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head><title>nvidia_claude_proxy Dashboard</title>
<style>
body { font-family: monospace; background: #1a1a2e; color: #eee; padding: 2rem; }
h1 { color: #00d4aa; }
.stat { display: inline-block; background: #16213e; padding: 1rem 2rem;
        margin: 0.5rem; border-radius: 8px; min-width: 150px; }
.stat .value { font-size: 2rem; color: #00d4aa; }
.stat .label { font-size: 0.8rem; color: #888; }
table { border-collapse: collapse; margin-top: 1rem; width: 100%; max-width: 800px; }
th, td { padding: 0.5rem 1rem; text-align: left; border-bottom: 1px solid #333; }
th { color: #00d4aa; }
</style></head>
<body>
<h1>nvidia_claude_proxy Analytics</h1>
<div>
  <div class="stat"><div class="value">{{ total }}</div><div class="label">Total Requests</div></div>
  <div class="stat"><div class="value">{{ avg_latency }}s</div><div class="label">Avg Latency</div></div>
  <div class="stat"><div class="value">{{ total_tokens }}</div><div class="label">Total Tokens</div></div>
  <div class="stat"><div class="value">{{ errors }}</div><div class="label">Errors</div></div>
</div>
<h2>Recent Requests</h2>
<table>
<tr><th>Model</th><th>Latency</th><th>Input Tokens</th><th>Output Tokens</th></tr>
{% for r in recent %}
<tr><td>{{ r.model }}</td><td>{{ r.latency }}s</td><td>{{ r.input_tokens }}</td><td>{{ r.output_tokens }}</td></tr>
{% endfor %}
</table>
<h2>Model Distribution</h2>
<table>
<tr><th>Model</th><th>Count</th></tr>
{% for model, count in model_dist.items() %}
<tr><td>{{ model }}</td><td>{{ count }}</td></tr>
{% endfor %}
</table>
</body></html>
"""


def render_dashboard(stats):
    requests = stats.get("requests", [])
    total = stats.get("total", 0)
    errors = stats.get("errors", 0)

    avg_latency = 0
    total_tokens = 0
    model_dist = {}

    for r in requests:
        avg_latency += r["latency"]
        total_tokens += r["input_tokens"] + r["output_tokens"]
        model_dist[r["model"]] = model_dist.get(r["model"], 0) + 1

    if requests:
        avg_latency = round(avg_latency / len(requests), 3)

    recent = list(reversed(requests[-10:]))

    return render_template_string(
        DASHBOARD_HTML,
        total=total,
        avg_latency=avg_latency,
        total_tokens=total_tokens,
        errors=errors,
        recent=recent,
        model_dist=model_dist,
    )
