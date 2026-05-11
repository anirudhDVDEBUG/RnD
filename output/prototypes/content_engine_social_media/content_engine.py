#!/usr/bin/env python3
"""
Content Engine - Social Media Content Creation Pipeline

Generates 5 channel-adapted social media posts from a single topic,
creates an AI-generated image via fal-ai (nano-banana-2),
and optionally auto-publishes via Upload-Post.

Runs in mock mode when API keys are absent.
"""

import json
import os
import sys
import textwrap
import hashlib
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Channel definitions
# ---------------------------------------------------------------------------

CHANNELS = {
    "twitter": {
        "name": "Twitter / X",
        "max_chars": 280,
        "style": "punchy, concise, hashtag-heavy",
        "format": "short_post",
    },
    "linkedin": {
        "name": "LinkedIn",
        "max_chars": 1300,
        "style": "professional, insight-driven, paragraph breaks",
        "format": "long_post",
    },
    "instagram": {
        "name": "Instagram",
        "max_chars": 2200,
        "style": "visual-first caption, emoji-rich, hashtag block at end",
        "format": "caption",
    },
    "facebook": {
        "name": "Facebook",
        "max_chars": 500,
        "style": "conversational, question-driven, shareable",
        "format": "medium_post",
    },
    "newsletter": {
        "name": "Blog / Newsletter",
        "max_chars": 3000,
        "style": "long-form, educational, with clear structure",
        "format": "article_snippet",
    },
}

# ---------------------------------------------------------------------------
# Mock content generation (used when GROQ_API_KEY is not set)
# ---------------------------------------------------------------------------

MOCK_CONTENT = {
    "twitter": (
        "{emoji} {topic} is changing the game.\n\n"
        "Here's what you need to know:\n"
        "- It saves 10x time\n"
        "- It scales effortlessly\n"
        "- Early adopters are winning\n\n"
        "Don't sleep on this. {hashtags}"
    ),
    "linkedin": (
        "I've been diving deep into {topic} and the results are remarkable.\n\n"
        "After 3 months of testing, here's what I've learned:\n\n"
        "1. The productivity gains are real - our team saw a 40% improvement "
        "in output quality.\n\n"
        "2. The learning curve is shorter than expected. Most people get "
        "comfortable within a week.\n\n"
        "3. The ROI speaks for itself. We measured a 3x return in the first "
        "quarter.\n\n"
        "The key insight? {topic} isn't just a tool - it's a workflow "
        "transformation.\n\n"
        "What's your experience been? I'd love to hear how others are "
        "approaching this.\n\n"
        "{hashtags}"
    ),
    "instagram": (
        "{emoji} {topic} just hit different.\n\n"
        "We built something incredible and the response has been "
        "overwhelming. Swipe to see the results.\n\n"
        "The secret? Combining creativity with cutting-edge tech to deliver "
        "content that actually resonates.\n\n"
        "Tag someone who needs to see this!\n\n"
        ".\n.\n.\n{hashtags}"
    ),
    "facebook": (
        "Have you tried {topic} yet?\n\n"
        "We just wrapped up a pilot and honestly, the results blew us away. "
        "The team went from spending hours on manual work to having "
        "everything automated in minutes.\n\n"
        "If you're curious, drop a comment and I'll share what we learned. "
        "{emoji}\n\n"
        "{hashtags}"
    ),
    "newsletter": (
        "# {topic}: A Practical Guide\n\n"
        "## Why This Matters Now\n\n"
        "{topic} has moved from experimental to essential. In this piece, "
        "we break down what's changed and what you should do about it.\n\n"
        "## Key Takeaways\n\n"
        "- **Speed**: Tasks that took hours now take minutes\n"
        "- **Quality**: Output consistency has improved dramatically\n"
        "- **Scale**: What worked for 10 users now works for 10,000\n\n"
        "## What We Recommend\n\n"
        "Start small. Pick one workflow, automate it with {topic}, measure "
        "the results, and expand from there. The companies seeing the best "
        "returns are the ones that iterate quickly and stay focused on "
        "measurable outcomes.\n\n"
        "---\n"
        "*Read the full analysis on our blog.*"
    ),
}


def pick_emoji(topic: str) -> str:
    """Deterministic emoji from topic hash."""
    emojis = ["🚀", "⚡", "🔥", "💡", "🎯", "✨", "📈", "🧠", "🛠️", "🌟"]
    idx = int(hashlib.md5(topic.encode()).hexdigest(), 16) % len(emojis)
    return emojis[idx]


def generate_hashtags(topic: str) -> str:
    words = topic.lower().split()
    base = "#" + "".join(w.capitalize() for w in words)
    return f"{base} #ContentEngine #SocialMedia #AI"


def generate_content_mock(topic: str) -> dict:
    """Generate mock content for all channels."""
    emoji = pick_emoji(topic)
    hashtags = generate_hashtags(topic)
    results = {}
    for channel, template in MOCK_CONTENT.items():
        text = template.format(topic=topic, emoji=emoji, hashtags=hashtags)
        max_chars = CHANNELS[channel]["max_chars"]
        results[channel] = {
            "platform": CHANNELS[channel]["name"],
            "content": text[:max_chars],
            "char_count": min(len(text), max_chars),
            "max_chars": max_chars,
        }
    return results


# ---------------------------------------------------------------------------
# Live content generation via Groq API
# ---------------------------------------------------------------------------

def generate_content_groq(topic: str) -> dict:
    """Generate content using Groq's fast LLM inference."""
    try:
        from groq import Groq
    except ImportError:
        print("[WARN] groq package not installed, falling back to mock mode")
        return generate_content_mock(topic)

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    results = {}

    for channel_id, channel in CHANNELS.items():
        prompt = (
            f"Write a {channel['format']} for {channel['name']} about: {topic}\n"
            f"Style: {channel['style']}\n"
            f"Max {channel['max_chars']} characters.\n"
            f"Include relevant hashtags. Return ONLY the post text."
        )
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        text = resp.choices[0].message.content.strip()
        results[channel_id] = {
            "platform": channel["name"],
            "content": text[:channel["max_chars"]],
            "char_count": min(len(text), channel["max_chars"]),
            "max_chars": channel["max_chars"],
        }
    return results


# ---------------------------------------------------------------------------
# Image generation via fal-ai
# ---------------------------------------------------------------------------

def generate_image_mock(topic: str, output_dir: Path) -> dict:
    """Create a placeholder SVG image when FAL_KEY is not set."""
    svg = textwrap.dedent(f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024"
             viewBox="0 0 1024 1024">
          <defs>
            <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#6366f1"/>
              <stop offset="100%" style="stop-color:#8b5cf6"/>
            </linearGradient>
          </defs>
          <rect width="1024" height="1024" fill="url(#bg)" rx="24"/>
          <text x="512" y="460" text-anchor="middle" fill="white"
                font-family="Arial, sans-serif" font-size="48"
                font-weight="bold">Content Engine</text>
          <text x="512" y="540" text-anchor="middle" fill="rgba(255,255,255,0.8)"
                font-family="Arial, sans-serif" font-size="28">{topic[:60]}</text>
          <text x="512" y="620" text-anchor="middle" fill="rgba(255,255,255,0.5)"
                font-family="Arial, sans-serif" font-size="20">[AI Image Placeholder - set FAL_KEY for real generation]</text>
        </svg>""")
    path = output_dir / "generated_image.svg"
    path.write_text(svg)
    return {
        "path": str(path),
        "model": "mock-placeholder",
        "note": "Set FAL_KEY for real nano-banana-2 image generation",
    }


def generate_image_fal(topic: str, output_dir: Path) -> dict:
    """Generate an image using fal-ai's nano-banana-2 model."""
    try:
        import fal_client
    except ImportError:
        print("[WARN] fal-client not installed, using placeholder image")
        return generate_image_mock(topic, output_dir)

    prompt = (
        f"Professional social media visual for: {topic}. "
        f"Modern, clean, vibrant colors, suitable for LinkedIn and Instagram."
    )
    result = fal_client.subscribe(
        "fal-ai/nano-banana-2",
        arguments={"prompt": prompt, "image_size": "square"},
    )
    image_url = result["images"][0]["url"]

    # Download image
    import urllib.request
    path = output_dir / "generated_image.png"
    urllib.request.urlretrieve(image_url, str(path))

    return {
        "path": str(path),
        "model": "nano-banana-2",
        "prompt": prompt,
        "url": image_url,
    }


# ---------------------------------------------------------------------------
# Publishing stub (Upload-Post integration)
# ---------------------------------------------------------------------------

def publish_content(posts: dict, image_info: dict) -> dict:
    """Publish via Upload-Post (stub — returns mock results)."""
    results = {}
    for channel_id, post in posts.items():
        results[channel_id] = {
            "platform": post["platform"],
            "status": "published (mock)",
            "timestamp": datetime.now().isoformat(),
            "url": f"https://example.com/{channel_id}/mock-post-id",
        }
    return results


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(topic: str, output_dir: str = "output") -> dict:
    """Run the full content engine pipeline."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Content Engine - Social Media Pipeline")
    print(f"{'='*60}")
    print(f"\n  Topic: {topic}")
    print(f"  Date:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- Step 1: Content generation ---
    has_groq = bool(os.environ.get("GROQ_API_KEY"))
    print(f"\n[1/3] Generating content for 5 channels", end="")
    print(f" ({'Groq API' if has_groq else 'mock mode'})...")

    if has_groq:
        posts = generate_content_groq(topic)
    else:
        posts = generate_content_mock(topic)

    for cid, post in posts.items():
        print(f"\n  --- {post['platform']} ({post['char_count']}/{post['max_chars']} chars) ---")
        preview = post["content"][:120].replace("\n", " ")
        print(f"  {preview}...")

    # --- Step 2: Image generation ---
    has_fal = bool(os.environ.get("FAL_KEY"))
    print(f"\n[2/3] Generating image", end="")
    print(f" ({'fal-ai nano-banana-2' if has_fal else 'mock SVG'})...")

    if has_fal:
        image_info = generate_image_fal(topic, out)
    else:
        image_info = generate_image_mock(topic, out)

    print(f"  Image saved: {image_info['path']}")

    # --- Step 3: Publish ---
    print(f"\n[3/3] Publishing to channels (mock mode)...")
    pub_results = publish_content(posts, image_info)
    for cid, res in pub_results.items():
        print(f"  {res['platform']}: {res['status']}")

    # --- Save full output ---
    manifest = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "mode": {
            "content": "groq" if has_groq else "mock",
            "image": "fal-ai" if has_fal else "mock",
        },
        "posts": posts,
        "image": image_info,
        "publish_results": pub_results,
    }
    manifest_path = out / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    # Save individual posts
    for cid, post in posts.items():
        post_path = out / f"post_{cid}.txt"
        post_path.write_text(post["content"])

    print(f"\n{'='*60}")
    print(f"  Pipeline complete!")
    print(f"  Output directory: {out}")
    print(f"  Manifest: {manifest_path}")
    print(f"  Posts: {len(posts)} files")
    print(f"  Image: {image_info['path']}")
    print(f"{'='*60}\n")

    return manifest


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "AI-Powered Analytics Dashboard"
    )
    run_pipeline(topic)
