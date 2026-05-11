"""
Vibe Bar Quota Monitor — Terminal Demo

Simulates the core features of Vibe Bar (a native macOS menu-bar app)
using mock data: quota tracking, usage pace, token cost estimation,
and service status checks.
"""

import json
import math
import random
import sys
import time
from datetime import datetime, timedelta


# ── Mock billing data ────────────────────────────────────────────────

def generate_mock_usage():
    """Simulate a billing period with realistic usage patterns."""
    billing_start = datetime.now() - timedelta(days=12)
    billing_end = billing_start + timedelta(days=30)
    days_elapsed = (datetime.now() - billing_start).days
    days_total = (billing_end - billing_start).days
    time_fraction = days_elapsed / days_total

    providers = {
        "claude_code": {
            "name": "Claude Code (Max)",
            "plan": "Max $200/mo",
            "quota_dollars": 200.00,
            "used_dollars": round(random.uniform(70, 130), 2),
            "billing_start": billing_start.strftime("%Y-%m-%d"),
            "billing_end": billing_end.strftime("%Y-%m-%d"),
            "days_elapsed": days_elapsed,
            "days_total": days_total,
            "time_fraction": round(time_fraction, 3),
            "sessions_today": random.randint(3, 18),
            "tokens_today": {
                "input": random.randint(40000, 250000),
                "output": random.randint(15000, 90000),
            },
        },
        "codex": {
            "name": "OpenAI Codex (Pro)",
            "plan": "Pro $200/mo",
            "quota_dollars": 200.00,
            "used_dollars": round(random.uniform(40, 110), 2),
            "billing_start": billing_start.strftime("%Y-%m-%d"),
            "billing_end": billing_end.strftime("%Y-%m-%d"),
            "days_elapsed": days_elapsed,
            "days_total": days_total,
            "time_fraction": round(time_fraction, 3),
            "sessions_today": random.randint(1, 10),
            "tokens_today": {
                "input": random.randint(20000, 150000),
                "output": random.randint(8000, 60000),
            },
        },
    }

    for p in providers.values():
        p["used_fraction"] = round(p["used_dollars"] / p["quota_dollars"], 3)
        remaining = p["days_total"] - p["days_elapsed"]
        if remaining > 0:
            p["projected_total"] = round(
                p["used_dollars"] / p["time_fraction"], 2
            )
            daily_budget = (p["quota_dollars"] - p["used_dollars"]) / remaining
            p["daily_budget_remaining"] = round(daily_budget, 2)
        else:
            p["projected_total"] = p["used_dollars"]
            p["daily_budget_remaining"] = 0.0

    return providers


def check_service_status():
    """Simulate service status checks."""
    services = [
        {"name": "Anthropic API", "url": "api.anthropic.com", "status": "operational"},
        {"name": "Claude Code", "url": "claude.ai", "status": "operational"},
        {"name": "OpenAI API", "url": "api.openai.com", "status": random.choice(["operational", "operational", "degraded"])},
        {"name": "Codex CLI", "url": "codex.openai.com", "status": "operational"},
    ]
    return services


# ── Display helpers ──────────────────────────────────────────────────

def bar(fraction, width=30):
    filled = int(fraction * width)
    filled = max(0, min(filled, width))
    empty = width - filled
    if fraction > 0.9:
        return f"[{'#' * filled}{'.' * empty}] ALERT"
    elif fraction > 0.7:
        return f"[{'#' * filled}{'.' * empty}] HIGH"
    else:
        return f"[{'#' * filled}{'.' * empty}]"


def pace_indicator(used_frac, time_frac):
    if time_frac == 0:
        return "N/A"
    ratio = used_frac / time_frac
    if ratio > 1.3:
        return "!! OVER-PACE  (slow down)"
    elif ratio > 1.05:
        return "~  SLIGHTLY AHEAD"
    elif ratio > 0.85:
        return "=  ON PACE   (good)"
    else:
        return "++ UNDER-PACE (room to spare)"


def format_tokens(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def estimate_cost(tokens_in, tokens_out, provider):
    """Rough local token cost estimate (simulated rates)."""
    if "claude" in provider:
        cost_in = tokens_in * 3.0 / 1_000_000   # $3/M input
        cost_out = tokens_out * 15.0 / 1_000_000  # $15/M output
    else:
        cost_in = tokens_in * 2.5 / 1_000_000
        cost_out = tokens_out * 10.0 / 1_000_000
    return round(cost_in + cost_out, 4)


# ── Main output ──────────────────────────────────────────────────────

def render_dashboard(output_format="terminal"):
    providers = generate_mock_usage()
    services = check_service_status()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if output_format == "json":
        data = {
            "timestamp": now,
            "providers": providers,
            "services": services,
        }
        print(json.dumps(data, indent=2))
        return data

    # Terminal dashboard
    width = 62
    print("=" * width)
    print("  VIBE BAR  —  Quota Monitor Dashboard (Terminal Demo)")
    print(f"  {now}")
    print("=" * width)

    for key, p in providers.items():
        print()
        print(f"  {p['name']}  [{p['plan']}]")
        print(f"  {'-' * (width - 4)}")

        # Quota bar
        pct = p["used_fraction"] * 100
        print(f"  Quota used:  ${p['used_dollars']:.2f} / ${p['quota_dollars']:.2f}  ({pct:.1f}%)")
        print(f"  {bar(p['used_fraction'])}")

        # Pace
        pace = pace_indicator(p["used_fraction"], p["time_fraction"])
        time_pct = p["time_fraction"] * 100
        print(f"  Billing day: {p['days_elapsed']} / {p['days_total']}  ({time_pct:.1f}% elapsed)")
        print(f"  Pace:        {pace}")

        # Projection
        print(f"  Projected:   ${p['projected_total']:.2f} by end of period")
        print(f"  Daily budget remaining: ${p['daily_budget_remaining']:.2f}/day")

        # Today's tokens
        tin = p["tokens_today"]["input"]
        tout = p["tokens_today"]["output"]
        cost = estimate_cost(tin, tout, key)
        print(f"  Today:       {p['sessions_today']} sessions, "
              f"{format_tokens(tin)} in / {format_tokens(tout)} out")
        print(f"  Est. cost:   ${cost:.4f} today")

    # Service status
    print()
    print(f"  {'SERVICE STATUS':^{width - 4}}")
    print(f"  {'-' * (width - 4)}")
    for svc in services:
        icon = "[OK]" if svc["status"] == "operational" else "[!!]"
        print(f"  {icon}  {svc['name']:<20s}  {svc['status']}")

    print()
    print("=" * width)
    print("  Vibe Bar: github.com/AstroQore/vibe-bar")
    print("  This is a terminal demo — the real app is a native macOS menu-bar widget.")
    print("=" * width)

    return {"providers": providers, "services": services}


def main():
    fmt = "terminal"
    if "--json" in sys.argv:
        fmt = "json"
    render_dashboard(output_format=fmt)


if __name__ == "__main__":
    main()
