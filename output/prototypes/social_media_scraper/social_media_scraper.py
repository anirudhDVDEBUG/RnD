"""
Social Media Scraper - Core module.

Wraps yt-dlp, Whisper, ffmpeg, and Gemini API to extract metadata,
comments, transcriptions, and AI video analysis from social media posts.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional


SUPPORTED_PLATFORMS = {
    "instagram": re.compile(r"(instagram\.com|instagr\.am)/"),
    "tiktok": re.compile(r"tiktok\.com/"),
    "twitter": re.compile(r"(twitter\.com|x\.com)/"),
    "youtube": re.compile(r"(youtube\.com|youtu\.be)/"),
}


def detect_platform(url: str) -> Optional[str]:
    """Detect which social media platform a URL belongs to."""
    for platform, pattern in SUPPORTED_PLATFORMS.items():
        if pattern.search(url):
            return platform
    return None


def check_dependencies() -> dict:
    """Check which required tools are available on PATH."""
    tools = ["yt-dlp", "whisper", "ffmpeg", "jq"]
    results = {}
    for tool in tools:
        results[tool] = shutil.which(tool) is not None
    results["gemini_api_key"] = bool(os.environ.get("GEMINI_API_KEY"))
    return results


def extract_metadata(url: str) -> dict:
    """Extract post metadata using yt-dlp --dump-json."""
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-download", url],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp metadata extraction failed: {result.stderr}")
    return json.loads(result.stdout)


def extract_comments(url: str) -> list:
    """Extract comments using yt-dlp --write-comments."""
    result = subprocess.run(
        ["yt-dlp", "--write-comments", "--dump-json", "--no-download", url],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        return []
    data = json.loads(result.stdout)
    return data.get("comments", [])


def download_media(url: str, output_dir: str) -> str:
    """Download media file using yt-dlp. Returns path to downloaded file."""
    template = os.path.join(output_dir, "scrape_%(id)s.%(ext)s")
    result = subprocess.run(
        ["yt-dlp", "-o", template, url],
        capture_output=True, text=True, timeout=300
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp download failed: {result.stderr}")
    # Find the downloaded file
    for f in Path(output_dir).glob("scrape_*"):
        return str(f)
    raise RuntimeError("Download completed but no file found")


def transcribe_audio(media_path: str, model: str = "base") -> str:
    """Transcribe audio from media file using OpenAI Whisper."""
    output_dir = os.path.dirname(media_path)
    result = subprocess.run(
        ["whisper", media_path, "--model", model,
         "--output_format", "txt", "--output_dir", output_dir],
        capture_output=True, text=True, timeout=600
    )
    if result.returncode != 0:
        raise RuntimeError(f"Whisper transcription failed: {result.stderr}")
    txt_path = Path(media_path).with_suffix(".txt")
    if txt_path.exists():
        return txt_path.read_text().strip()
    return result.stdout.strip()


def extract_frames(media_path: str, output_dir: str, fps: float = 1.0) -> list:
    """Extract key frames from video using ffmpeg."""
    frame_pattern = os.path.join(output_dir, "frames_%04d.jpg")
    subprocess.run(
        ["ffmpeg", "-i", media_path, "-vf", f"fps={fps}",
         frame_pattern, "-y", "-loglevel", "quiet"],
        capture_output=True, timeout=120
    )
    return sorted(Path(output_dir).glob("frames_*.jpg"))


def analyze_with_gemini(frame_paths: list, prompt: str = None) -> str:
    """Send frames to Gemini API for multimodal video analysis."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "(Gemini API key not set — skipping video analysis)"

    import base64
    try:
        import requests
    except ImportError:
        return "(requests library not available for Gemini API call)"

    if not prompt:
        prompt = "Analyze these video frames. Describe the content, setting, actions, and any text visible."

    # Encode frames as base64
    parts = [{"text": prompt}]
    for fp in frame_paths[:10]:  # Limit to 10 frames
        with open(fp, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        parts.append({
            "inline_data": {"mime_type": "image/jpeg", "data": b64}
        })

    payload = {"contents": [{"parts": parts}]}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def format_results(metadata: dict, comments: list = None,
                   transcription: str = None, analysis: str = None,
                   platform: str = None) -> str:
    """Format scraped results as structured markdown."""
    lines = []
    lines.append("### Post Metadata")
    lines.append(f"- **Author:** @{metadata.get('uploader', metadata.get('uploader_id', 'unknown'))}")
    lines.append(f"- **Platform:** {platform or 'Unknown'}")
    lines.append(f"- **Date:** {metadata.get('upload_date', 'N/A')}")
    views = metadata.get("view_count", "N/A")
    likes = metadata.get("like_count", "N/A")
    comment_count = metadata.get("comment_count", len(comments) if comments else "N/A")
    lines.append(f"- **Views:** {views} | **Likes:** {likes} | **Comments:** {comment_count}")
    lines.append("")

    lines.append("### Content")
    lines.append(metadata.get("description", metadata.get("title", "(no caption)")))
    lines.append("")

    if transcription:
        lines.append("### Transcription")
        lines.append(transcription)
        lines.append("")

    if analysis:
        lines.append("### Video Analysis")
        lines.append(analysis)
        lines.append("")

    if comments:
        lines.append("### Top Comments")
        for i, c in enumerate(comments[:10], 1):
            author = c.get("author", "anonymous")
            text = c.get("text", "")
            clikes = c.get("like_count", 0)
            lines.append(f"{i}. @{author}: {text} ({clikes} likes)")
        lines.append("")

    return "\n".join(lines)


def scrape_url(url: str, transcribe: bool = True, analyze_video: bool = True) -> str:
    """Full pipeline: scrape a social media URL and return formatted results."""
    platform = detect_platform(url)
    if not platform:
        raise ValueError(f"Unsupported URL: {url}")

    deps = check_dependencies()
    if not deps["yt-dlp"]:
        raise RuntimeError("yt-dlp is required but not found. Install: pip install yt-dlp")

    metadata = extract_metadata(url)
    comments = extract_comments(url)

    transcription = None
    analysis = None

    if transcribe or analyze_video:
        tmpdir = tempfile.mkdtemp(prefix="scrape_")
        try:
            media_path = download_media(url, tmpdir)

            if transcribe and deps.get("whisper", False):
                transcription = transcribe_audio(media_path)

            if analyze_video and deps.get("gemini_api_key"):
                frames = extract_frames(media_path, tmpdir)
                if frames:
                    analysis = analyze_with_gemini(frames)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    return format_results(metadata, comments, transcription, analysis, platform)
