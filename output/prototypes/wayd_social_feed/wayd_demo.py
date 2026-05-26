#!/usr/bin/env python3
"""
WAYD Social Feed Demo - Mock implementation showing the feed experience.

Simulates the 'wayd' CLI tool: a meme-y social feed for programmers,
backed by GitHub Issues. This demo uses mock data so no API keys are needed.
"""

import json
import random
import textwrap
from datetime import datetime, timedelta

# ── Mock data representing GitHub Issues as social posts ──────────────────

MOCK_POSTS = [
    {
        "user": "debugDan",
        "avatar": "(>_<)",
        "time_ago": "12m",
        "body": "3 hours into a CSS bug. Turns out it was a missing semicolon. I'm going outside.",
        "reactions": {"laugh": 42, "heart": 5, "rocket": 1},
        "comments": 7,
    },
    {
        "user": "asyncAlice",
        "avatar": "(@_@)",
        "time_ago": "28m",
        "body": "Asked Claude to refactor my auth module. It deleted 400 lines and the tests still pass. I'm scared.",
        "reactions": {"laugh": 89, "heart": 23, "rocket": 14},
        "comments": 31,
    },
    {
        "user": "gitGary",
        "avatar": "(^_^)",
        "time_ago": "1h",
        "body": "Day 47 of 'I'll clean up the git history later'",
        "reactions": {"laugh": 67, "heart": 12, "rocket": 3},
        "comments": 15,
    },
    {
        "user": "containerCarla",
        "avatar": "(o_O)",
        "time_ago": "2h",
        "body": "My Docker image is 4GB. It contains a single Python script that prints 'hello world'.",
        "reactions": {"laugh": 112, "heart": 8, "rocket": 2},
        "comments": 22,
    },
    {
        "user": "pipelinePete",
        "avatar": "(-_-)",
        "time_ago": "3h",
        "body": "CI pipeline has been green for 6 straight days. Something is definitely wrong.",
        "reactions": {"laugh": 54, "heart": 19, "rocket": 7},
        "comments": 11,
    },
    {
        "user": "promptPriya",
        "avatar": "(~_~)",
        "time_ago": "4h",
        "body": "Wrote a 2000-word prompt to get Claude to write a 3-line function. Peak engineering.",
        "reactions": {"laugh": 203, "heart": 45, "rocket": 31},
        "comments": 48,
    },
    {
        "user": "kubeKyle",
        "avatar": "(T_T)",
        "time_ago": "5h",
        "body": "Accidentally kubectl delete'd prod. Updating LinkedIn as we speak.",
        "reactions": {"laugh": 340, "heart": 2, "rocket": 0},
        "comments": 67,
    },
    {
        "user": "mergeMika",
        "avatar": "(._. )",
        "time_ago": "6h",
        "body": "Merge conflict in package-lock.json again. Considering a career in farming.",
        "reactions": {"laugh": 78, "heart": 34, "rocket": 5},
        "comments": 19,
    },
]

# ── Rendering ─────────────────────────────────────────────────────────────

BORDER_CHAR = "-"
WIDTH = 64


def render_reaction(emoji_name: str, count: int) -> str:
    icons = {"laugh": "\U0001f602", "heart": "\u2764\ufe0f ", "rocket": "\U0001f680"}
    icon = icons.get(emoji_name, emoji_name)
    return f"{icon} {count}"


def render_post(post: dict) -> str:
    lines = []
    lines.append(BORDER_CHAR * WIDTH)
    header = f"  {post['avatar']}  @{post['user']}  ·  {post['time_ago']} ago"
    lines.append(header)
    lines.append("")
    wrapped = textwrap.wrap(post["body"], width=WIDTH - 4)
    for line in wrapped:
        lines.append(f"    {line}")
    lines.append("")
    reactions = "  ".join(
        render_reaction(k, v) for k, v in post["reactions"].items() if v > 0
    )
    lines.append(f"    {reactions}   \U0001f4ac {post['comments']} comments")
    lines.append("")
    return "\n".join(lines)


def render_feed(posts: list, title: str = "WAYD Feed") -> str:
    banner = f"""
{'=' * WIDTH}
   __        __    _   _ ____
   \\ \\      / /_ _| | | |  _ \\
    \\ \\ /\\ / / _` | |_| | | | |
     \\ V  V / (_| |\\__, | |_| |
      \\_/\\_/ \\__,_|  |_/|____/

   What Are You Doing?  --  The coffee break for coders
{'=' * WIDTH}
"""
    body = "\n".join(render_post(p) for p in posts)
    footer = (
        f"\n{BORDER_CHAR * WIDTH}\n"
        f"  Showing {len(posts)} posts  |  Powered by GitHub Issues\n"
        f"  Post yours: wayd post \"your status here\"\n"
        f"{BORDER_CHAR * WIDTH}\n"
    )
    return banner + body + footer


def simulate_post(message: str) -> str:
    """Simulate posting a status update."""
    now = datetime.now().strftime("%H:%M")
    return (
        f"\n{'=' * WIDTH}\n"
        f"  Posted to WAYD at {now}!\n"
        f"{'=' * WIDTH}\n\n"
        f"  (^_^)  @you  ·  just now\n\n"
        f"    {message}\n\n"
        f"    \u2764\ufe0f  0   \U0001f680 0   \U0001f4ac 0 comments\n"
        f"\n{BORDER_CHAR * WIDTH}\n"
        f"  Your post is live on the feed!\n"
        f"  View it: wayd feed\n"
        f"{BORDER_CHAR * WIDTH}\n"
    )


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("\n[1/3] Browsing the WAYD social feed...\n")
    # Show 5 random posts
    selected = random.sample(MOCK_POSTS, min(5, len(MOCK_POSTS)))
    print(render_feed(selected))

    print("\n[2/3] Posting a status update...\n")
    demo_message = "Building a prototype at 2am with Claude. Send coffee."
    print(simulate_post(demo_message))

    print("\n[3/3] Feed stats summary\n")
    total_laughs = sum(p["reactions"]["laugh"] for p in MOCK_POSTS)
    total_comments = sum(p["comments"] for p in MOCK_POSTS)
    print(f"  Total posts in feed:    {len(MOCK_POSTS)}")
    print(f"  Total laugh reactions:  {total_laughs}")
    print(f"  Total comments:         {total_comments}")
    print(f"  Most popular poster:    @{max(MOCK_POSTS, key=lambda p: sum(p['reactions'].values()))['user']}")
    print(f"\n  Coffee break complete. Back to coding!\n")


if __name__ == "__main__":
    main()
