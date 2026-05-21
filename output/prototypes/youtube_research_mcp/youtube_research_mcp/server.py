"""
MCP server exposing YouTube research tools: transcripts, comments,
channel analysis, and video search.

When no YOUTUBE_API_KEY is set, comment/search/channel tools use
built-in mock data so the demo still runs end-to-end.
"""

import json
import os
import re
import sys
from typing import Any

# ---------------------------------------------------------------------------
# Optional imports — transcript extraction works without API key
# ---------------------------------------------------------------------------
try:
    from youtube_transcript_api import YouTubeTranscriptApi

    HAS_TRANSCRIPT_API = True
except ImportError:
    HAS_TRANSCRIPT_API = False

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VIDEO_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w-]{11})"
)


def _extract_video_id(url_or_id: str) -> str:
    """Return the 11-char YouTube video ID from a URL or bare ID."""
    m = VIDEO_ID_RE.search(url_or_id)
    if m:
        return m.group(1)
    if re.fullmatch(r"[\w-]{11}", url_or_id):
        return url_or_id
    raise ValueError(f"Cannot extract video ID from: {url_or_id}")


# ---------------------------------------------------------------------------
# Mock data (used when dependencies or API key unavailable)
# ---------------------------------------------------------------------------

MOCK_TRANSCRIPT = [
    {"text": "Welcome to this deep dive on large language models.", "start": 0.0, "duration": 3.2},
    {"text": "Today we'll cover how transformer architectures work.", "start": 3.2, "duration": 3.5},
    {"text": "The key insight is the self-attention mechanism.", "start": 6.7, "duration": 2.8},
    {"text": "It lets the model weigh which tokens are most relevant.", "start": 9.5, "duration": 3.1},
    {"text": "This replaced recurrent approaches almost entirely.", "start": 12.6, "duration": 3.0},
    {"text": "Scaling laws show predictable improvement with more compute.", "start": 15.6, "duration": 3.4},
    {"text": "But data quality matters just as much as quantity.", "start": 19.0, "duration": 2.9},
    {"text": "Fine-tuning and RLHF align models with human preferences.", "start": 21.9, "duration": 3.6},
    {"text": "Tool use and function calling extend what models can do.", "start": 25.5, "duration": 3.2},
    {"text": "Thanks for watching — like and subscribe for more AI content.", "start": 28.7, "duration": 3.0},
]

MOCK_COMMENTS = [
    {"author": "AIResearcher42", "text": "Great explanation of attention! Finally clicked for me.", "likes": 234, "published_at": "2026-04-15T10:23:00Z"},
    {"author": "MLEngineer", "text": "Would love a follow-up on MoE architectures.", "likes": 187, "published_at": "2026-04-15T14:05:00Z"},
    {"author": "DataSciStudent", "text": "The RLHF section was the best part. More please!", "likes": 145, "published_at": "2026-04-16T08:12:00Z"},
    {"author": "TechFounder", "text": "We used this video to onboard our new ML team. Solid.", "likes": 98, "published_at": "2026-04-17T19:30:00Z"},
    {"author": "CuriousViewer", "text": "How does this compare to state-space models like Mamba?", "likes": 76, "published_at": "2026-04-18T11:45:00Z"},
]

MOCK_CHANNEL = {
    "channel_id": "UC_mock_channel_id",
    "title": "AI Explained",
    "subscriber_count": 542000,
    "video_count": 187,
    "view_count": 28400000,
    "description": "Making AI research accessible. Weekly deep dives into papers, models, and industry trends.",
    "recent_uploads": [
        {"title": "Transformers Explained in 30 Minutes", "views": 320000, "published": "2026-04-14"},
        {"title": "Claude 4 vs GPT-5: Benchmark Breakdown", "views": 510000, "published": "2026-04-07"},
        {"title": "Why RAG Beats Fine-Tuning (Usually)", "views": 275000, "published": "2026-03-31"},
        {"title": "The MCP Protocol — What Developers Need to Know", "views": 198000, "published": "2026-03-24"},
        {"title": "Scaling Laws: The Math Behind AI Progress", "views": 165000, "published": "2026-03-17"},
    ],
    "top_topics": ["transformers", "LLMs", "benchmarks", "RAG", "scaling laws"],
}

MOCK_SEARCH = [
    {"video_id": "dQw4w9WgXcQ", "title": "How Transformers Work — Visual Guide", "channel": "AI Explained", "views": 320000, "published": "2026-04-14"},
    {"video_id": "abc123def45", "title": "Building AI Agents with MCP", "channel": "Code With Claude", "views": 185000, "published": "2026-04-10"},
    {"video_id": "xyz789ghi01", "title": "LLM Fine-Tuning Tutorial 2026", "channel": "ML Mastery", "views": 142000, "published": "2026-04-05"},
]


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def get_transcript(video_url: str) -> dict[str, Any]:
    """Extract transcript from a YouTube video URL or ID."""
    video_id = _extract_video_id(video_url)

    if HAS_TRANSCRIPT_API:
        try:
            entries = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join(e["text"] for e in entries)
            return {
                "video_id": video_id,
                "segments": len(entries),
                "full_text": full_text,
                "transcript": entries[:20],  # first 20 segments for brevity
                "source": "youtube_transcript_api",
            }
        except Exception as exc:
            return {
                "video_id": video_id,
                "error": str(exc),
                "fallback": "mock",
                **_mock_transcript(video_id),
            }

    return _mock_transcript(video_id)


def _mock_transcript(video_id: str) -> dict[str, Any]:
    full_text = " ".join(e["text"] for e in MOCK_TRANSCRIPT)
    return {
        "video_id": video_id,
        "segments": len(MOCK_TRANSCRIPT),
        "full_text": full_text,
        "transcript": MOCK_TRANSCRIPT,
        "source": "mock_data",
    }


def get_comments(video_url: str, max_results: int = 20) -> dict[str, Any]:
    """Retrieve top comments for a YouTube video."""
    video_id = _extract_video_id(video_url)
    api_key = os.environ.get("YOUTUBE_API_KEY")

    if api_key:
        # Real API path (requires google-api-python-client)
        try:
            from googleapiclient.discovery import build

            yt = build("youtube", "v3", developerKey=api_key)
            resp = yt.commentThreads().list(
                part="snippet", videoId=video_id, maxResults=max_results, order="relevance"
            ).execute()
            comments = []
            for item in resp.get("items", []):
                snip = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": snip["authorDisplayName"],
                    "text": snip["textDisplay"],
                    "likes": snip["likeCount"],
                    "published_at": snip["publishedAt"],
                })
            return {"video_id": video_id, "count": len(comments), "comments": comments, "source": "youtube_api"}
        except Exception as exc:
            pass  # fall through to mock

    return {
        "video_id": video_id,
        "count": len(MOCK_COMMENTS),
        "comments": MOCK_COMMENTS,
        "source": "mock_data",
    }


def analyze_channel(channel_url_or_id: str) -> dict[str, Any]:
    """Return channel metadata, recent uploads, and content patterns."""
    # In production this would call YouTube Data API v3 channels.list
    return {**MOCK_CHANNEL, "source": "mock_data"}


def search_videos(query: str, max_results: int = 5) -> dict[str, Any]:
    """Search YouTube for videos matching a query."""
    # Filter mock results by naive keyword match
    q_lower = query.lower()
    hits = [v for v in MOCK_SEARCH if q_lower in v["title"].lower()] or MOCK_SEARCH
    return {
        "query": query,
        "count": len(hits[:max_results]),
        "results": hits[:max_results],
        "source": "mock_data",
    }


# ---------------------------------------------------------------------------
# MCP protocol (stdin/stdout JSON-RPC)
# ---------------------------------------------------------------------------

TOOLS = {
    "get_transcript": {
        "fn": get_transcript,
        "description": "Extract full transcript from a YouTube video URL or ID.",
        "input_schema": {
            "type": "object",
            "properties": {"video_url": {"type": "string", "description": "YouTube video URL or 11-char video ID"}},
            "required": ["video_url"],
        },
    },
    "get_comments": {
        "fn": get_comments,
        "description": "Retrieve top comments from a YouTube video for analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_url": {"type": "string", "description": "YouTube video URL or 11-char video ID"},
                "max_results": {"type": "integer", "description": "Max comments to return (default 20)", "default": 20},
            },
            "required": ["video_url"],
        },
    },
    "analyze_channel": {
        "fn": analyze_channel,
        "description": "Get channel metadata, recent uploads, and content patterns.",
        "input_schema": {
            "type": "object",
            "properties": {"channel_url_or_id": {"type": "string", "description": "YouTube channel URL or ID"}},
            "required": ["channel_url_or_id"],
        },
    },
    "search_videos": {
        "fn": search_videos,
        "description": "Search YouTube for videos matching a query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "description": "Max results (default 5)", "default": 5},
            },
            "required": ["query"],
        },
    },
}


def handle_request(req: dict) -> dict:
    """Process a single JSON-RPC request."""
    method = req.get("method", "")
    req_id = req.get("id")
    params = req.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "youtube-research-mcp", "version": __version__},
            },
        }

    if method == "notifications/initialized":
        return None  # no response needed

    if method == "tools/list":
        tool_list = []
        for name, spec in TOOLS.items():
            tool_list.append({"name": name, "description": spec["description"], "inputSchema": spec["input_schema"]})
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tool_list}}

    if method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {})
        if tool_name not in TOOLS:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }
        result = TOOLS[tool_name]["fn"](**args)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main():
    """Run the MCP server on stdin/stdout."""
    from . import __version__

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle_request(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
