#!/usr/bin/env python3
"""
Stand-alone demo — exercises every YouTube Research MCP tool and prints
structured output.  Works without API keys (uses built-in mock data).
"""

import json
import textwrap

from youtube_research_mcp.server import (
    analyze_channel,
    get_comments,
    get_transcript,
    search_videos,
)

DIVIDER = "=" * 60


def section(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def pretty(obj):
    print(json.dumps(obj, indent=2))


def main():
    print("YouTube Research MCP — Demo Run")
    print("(No API key required — uses mock data for demo purposes)\n")

    # ── 1. Transcript ─────────────────────────────────────────────
    section("1. GET TRANSCRIPT")
    result = get_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Video ID : {result['video_id']}")
    print(f"Segments : {result['segments']}")
    print(f"Source   : {result['source']}")
    print(f"\nFull text (first 200 chars):")
    print(textwrap.fill(result["full_text"][:200], width=72))

    # ── 2. Comments ───────────────────────────────────────────────
    section("2. GET COMMENTS")
    result = get_comments("dQw4w9WgXcQ")
    print(f"Video ID : {result['video_id']}")
    print(f"Count    : {result['count']}")
    print(f"Source   : {result['source']}")
    print("\nTop comments:")
    for c in result["comments"][:3]:
        print(f"  [{c['likes']} likes] @{c['author']}: {c['text']}")

    # ── 3. Channel Analysis ───────────────────────────────────────
    section("3. ANALYZE CHANNEL")
    result = analyze_channel("UC_mock_channel_id")
    print(f"Channel  : {result['title']}")
    print(f"Subs     : {result['subscriber_count']:,}")
    print(f"Videos   : {result['video_count']}")
    print(f"Views    : {result['view_count']:,}")
    print(f"\nTop topics: {', '.join(result['top_topics'])}")
    print("\nRecent uploads:")
    for v in result["recent_uploads"][:3]:
        print(f"  - {v['title']} ({v['views']:,} views, {v['published']})")

    # ── 4. Search Videos ──────────────────────────────────────────
    section("4. SEARCH VIDEOS")
    result = search_videos("transformers AI")
    print(f"Query    : {result['query']}")
    print(f"Results  : {result['count']}")
    print("\nMatches:")
    for v in result["results"]:
        print(f"  - [{v['video_id']}] {v['title']} by {v['channel']} ({v['views']:,} views)")

    # ── Summary ───────────────────────────────────────────────────
    section("DEMO COMPLETE")
    print("All 4 MCP tools executed successfully.")
    print("With a YOUTUBE_API_KEY, comments/search/channel use live data.")
    print("Transcript extraction works on real videos via youtube-transcript-api.")


if __name__ == "__main__":
    main()
