#!/usr/bin/env python3
"""
Demo script for Social Media Scraper.

Uses mock data to demonstrate the full pipeline output without requiring
yt-dlp, Whisper, or API keys. Pass a real URL as argv[1] to scrape live
(requires yt-dlp installed).
"""

import sys
import shutil

from social_media_scraper import (
    detect_platform, check_dependencies, format_results, scrape_url
)

# ── Mock data for demo (no external tools needed) ──────────────────────

MOCK_POSTS = {
    "youtube": {
        "metadata": {
            "title": "How I Built an AI Agent That Runs My Business",
            "uploader": "TechFounderAI",
            "uploader_id": "techfounderai",
            "upload_date": "20260501",
            "view_count": 284_000,
            "like_count": 12_400,
            "comment_count": 873,
            "description": (
                "In this video I walk through how I built an autonomous AI agent "
                "using Claude that handles customer support, lead qualification, "
                "and weekly reporting — completely hands-off.\n\n"
                "Tools used: Claude API, Zapier, Notion, Slack."
            ),
        },
        "comments": [
            {"author": "agent_builder_99", "text": "This is exactly what I've been trying to build. What model are you using for the lead scoring?", "like_count": 142},
            {"author": "sarah_devops", "text": "The Slack integration part is genius. Saved me hours of work.", "like_count": 89},
            {"author": "nocode_nick", "text": "Can this work without coding? I'm a marketer not a dev.", "like_count": 67},
            {"author": "ai_skeptic_42", "text": "How do you handle hallucinations in the customer support replies?", "like_count": 54},
            {"author": "startup_jane", "text": "Been running something similar for 3 months. ROI is insane.", "like_count": 41},
        ],
        "transcription": (
            "So I've been running this AI agent for about six weeks now, and it's "
            "completely changed how I operate my business. Let me show you exactly "
            "how I built it. First, I set up a Claude-based pipeline that monitors "
            "incoming emails and Slack messages. It classifies each message as either "
            "a support request, a sales lead, or internal communication. For support "
            "requests, it drafts a response using our knowledge base. For leads, it "
            "scores them on a 1-to-10 scale and routes hot leads directly to my "
            "calendar. The whole thing runs 24/7 and I check in maybe once a day."
        ),
        "analysis": (
            "The video shows a screen recording of a dashboard application with "
            "multiple panels. The presenter demonstrates an AI agent workflow with "
            "a Slack interface on the left, a Notion database in the center showing "
            "lead scores, and a terminal running Python scripts on the right. "
            "Text overlays highlight key metrics: '94% accuracy on lead scoring' "
            "and '3.2 minute average response time'. The presenter occasionally "
            "appears via webcam in the corner, gesturing at different parts of the screen."
        ),
    },
    "tiktok": {
        "metadata": {
            "title": "POV: Your AI agent closes a deal while you sleep",
            "uploader": "hustlebot",
            "uploader_id": "hustlebot",
            "upload_date": "20260509",
            "view_count": 1_200_000,
            "like_count": 98_000,
            "comment_count": 4_200,
            "description": "AI agent just closed a $5k deal at 3am. I was asleep. #aiagent #automation #hustle",
        },
        "comments": [
            {"author": "skeptical_sam", "text": "no way this is real lol", "like_count": 2100},
            {"author": "buildwithclaude", "text": "what stack are you using?", "like_count": 890},
            {"author": "marketing_maya", "text": "I need this for my agency ASAP", "like_count": 670},
        ],
        "transcription": "Bro, I literally woke up to a Stripe notification. Five thousand dollars. My AI agent qualified the lead, sent the proposal, handled three follow-up emails, and closed the deal. All while I was sleeping.",
        "analysis": "Short-form vertical video showing a phone screen with a Stripe payment notification for $5,000. Quick cuts to a laptop showing an email thread between an AI agent and a client. Upbeat background music. Text overlays: 'AI closed this deal at 3AM' and 'I was literally asleep'.",
    },
    "instagram": {
        "metadata": {
            "title": "The future of marketing is autonomous agents",
            "uploader": "digital_marketing_pro",
            "uploader_id": "digital_marketing_pro",
            "upload_date": "20260507",
            "view_count": 45_000,
            "like_count": 3_200,
            "comment_count": 187,
            "description": "Just shipped an AI agent that writes, schedules, and optimizes ad copy across 4 platforms. Results after 2 weeks: 34% lower CPA, 2.1x ROAS improvement. The game has changed.\n\n#marketing #ai #adtech #automation",
        },
        "comments": [
            {"author": "adtech_alex", "text": "What platforms does it support?", "like_count": 45},
            {"author": "growthguru", "text": "This is the direction everything is heading. Early movers win.", "like_count": 38},
        ],
        "transcription": None,
        "analysis": None,
    },
    "twitter": {
        "metadata": {
            "title": "Thread on AI agent architectures",
            "uploader": "ai_eng_lead",
            "uploader_id": "ai_eng_lead",
            "upload_date": "20260510",
            "view_count": 89_000,
            "like_count": 5_600,
            "comment_count": 342,
            "description": "Hot take: Most 'AI agents' are just glorified if-else chains with an LLM in the middle.\n\nReal agents need: memory, tool use, planning, and self-correction.\n\nHere's the architecture we use in production (thread):",
        },
        "comments": [
            {"author": "ml_researcher", "text": "Agree on the self-correction part. That's the hardest to get right.", "like_count": 234},
            {"author": "claude_fan", "text": "Claude with tool use + extended thinking is the closest I've seen to real agency", "like_count": 189},
        ],
        "transcription": None,
        "analysis": None,
    },
}


def run_mock_demo():
    """Run the demo using mock data."""
    print("=" * 64)
    print("  Social Media Scraper — Demo (Mock Data)")
    print("=" * 64)
    print()

    # Show dependency check
    print("Checking installed tools...")
    deps = check_dependencies()
    for tool, available in deps.items():
        status = "OK" if available else "not found (optional for demo)"
        print(f"  {tool}: {status}")
    print()

    # Show platform detection
    test_urls = [
        "https://www.youtube.com/watch?v=abc123",
        "https://www.tiktok.com/@user/video/123",
        "https://www.instagram.com/p/ABC123/",
        "https://x.com/user/status/123456",
        "https://example.com/not-social",
    ]
    print("Platform detection:")
    for url in test_urls:
        platform = detect_platform(url)
        print(f"  {url}")
        print(f"    -> {platform or 'unsupported'}")
    print()

    # Demonstrate formatted output for each platform
    for platform, mock in MOCK_POSTS.items():
        print("-" * 64)
        print(f"  Scraping {platform.upper()} post (mock)")
        print("-" * 64)
        print()
        output = format_results(
            metadata=mock["metadata"],
            comments=mock["comments"],
            transcription=mock["transcription"],
            analysis=mock["analysis"],
            platform=platform,
        )
        print(output)
        print()

    print("=" * 64)
    print("  Demo complete. To scrape a real URL:")
    print("  python demo.py https://www.youtube.com/watch?v=...")
    print("=" * 64)


def run_live(url: str):
    """Scrape a real URL (requires yt-dlp)."""
    platform = detect_platform(url)
    if not platform:
        print(f"Error: Unsupported URL — {url}")
        print("Supported: Instagram, TikTok, Twitter/X, YouTube")
        sys.exit(1)

    deps = check_dependencies()
    if not deps["yt-dlp"]:
        print("Error: yt-dlp is required for live scraping.")
        print("Install: pip install yt-dlp")
        sys.exit(1)

    print(f"Scraping {platform} post: {url}")
    print("This may take a moment...")
    print()
    result = scrape_url(url)
    print(result)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        run_live(sys.argv[1])
    else:
        run_mock_demo()
