#!/usr/bin/env python3
"""YouTube Video Summarizer - fetches transcripts via yt-dlp and generates structured markdown notes."""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# --- Mock data for demo (no API keys or network needed) ---
MOCK_METADATA = {
    "title": "How Transformers Work - A Detailed Explanation",
    "channel": "AI Academy",
    "duration_string": "18:42",
    "webpage_url": "https://www.youtube.com/watch?v=EXAMPLE123",
    "upload_date": "20250310",
    "description": "A deep dive into the transformer architecture that powers modern LLMs.",
    "chapters": [
        {"start_time": 0, "title": "Introduction"},
        {"start_time": 120, "title": "Self-Attention Mechanism"},
        {"start_time": 420, "title": "Multi-Head Attention"},
        {"start_time": 660, "title": "Positional Encoding"},
        {"start_time": 900, "title": "Putting It All Together"},
    ],
}

MOCK_TRANSCRIPT_SEGMENTS = [
    {"start": 0, "text": "Welcome to this deep dive into transformers."},
    {"start": 5, "text": "Today we'll explore how the architecture behind ChatGPT and Claude actually works."},
    {"start": 15, "text": "Transformers were introduced in the landmark paper Attention Is All You Need in 2017."},
    {"start": 25, "text": "Before transformers, recurrent neural networks were the go-to for sequence modeling."},
    {"start": 35, "text": "But RNNs had a fundamental limitation: they process tokens one at a time."},
    {"start": 50, "text": "This sequential nature made them slow to train and hard to parallelize."},
    {"start": 65, "text": "Transformers solved this by replacing recurrence with a mechanism called self-attention."},
    {"start": 80, "text": "Self-attention lets every token in a sequence look at every other token simultaneously."},
    {"start": 95, "text": "This is a paradigm shift. Instead of passing information step by step, we compute relationships all at once."},
    {"start": 110, "text": "Let's get into the details of how self-attention actually works."},
    {"start": 125, "text": "The core idea is to compute three vectors for each token: a query, a key, and a value."},
    {"start": 140, "text": "The query represents what this token is looking for."},
    {"start": 150, "text": "The key represents what this token has to offer."},
    {"start": 160, "text": "And the value is the actual information that gets passed along."},
    {"start": 175, "text": "We compute attention scores by taking the dot product of queries with keys."},
    {"start": 190, "text": "Then we apply softmax to get a probability distribution."},
    {"start": 205, "text": "These probabilities tell us how much each token should attend to every other token."},
    {"start": 220, "text": "Finally, we multiply these attention weights by the values to get the output."},
    {"start": 240, "text": "This is the fundamental building block. But one head of attention isn't enough."},
    {"start": 260, "text": "Different relationships in language require different types of attention patterns."},
    {"start": 280, "text": "Subject-verb agreement needs one kind of attention. Coreference resolution needs another."},
    {"start": 300, "text": "That's why transformers use multi-head attention."},
    {"start": 320, "text": "Instead of one set of Q, K, V projections, we have multiple heads running in parallel."},
    {"start": 340, "text": "Each head learns to focus on different linguistic relationships."},
    {"start": 360, "text": "Typically a model might use 8, 12, or even 96 attention heads."},
    {"start": 380, "text": "The outputs from all heads are concatenated and projected back to the model dimension."},
    {"start": 400, "text": "This gives the model a rich, multi-faceted understanding of the input."},
    {"start": 425, "text": "One thing we haven't addressed yet is position. How does the model know word order?"},
    {"start": 450, "text": "Since attention is permutation-invariant, we need to explicitly encode positions."},
    {"start": 475, "text": "The original paper used sinusoidal positional encodings."},
    {"start": 500, "text": "These are fixed mathematical functions that give each position a unique signature."},
    {"start": 525, "text": "Modern models often use learned positional embeddings or rotary position encodings."},
    {"start": 550, "text": "RoPE, used in models like LLaMA, encodes relative positions through rotation matrices."},
    {"start": 575, "text": "This enables better generalization to longer sequences than seen during training."},
    {"start": 600, "text": "Positional encoding is crucial. Without it, the model treats the input as a bag of words."},
    {"start": 660, "text": "Now let's put everything together into the full transformer architecture."},
    {"start": 680, "text": "A transformer block consists of multi-head attention followed by a feed-forward network."},
    {"start": 700, "text": "Each sub-layer has a residual connection and layer normalization."},
    {"start": 720, "text": "The feed-forward network is typically a two-layer MLP with a nonlinear activation."},
    {"start": 740, "text": "Modern models stack dozens or even hundreds of these blocks."},
    {"start": 760, "text": "GPT-4 is rumored to have over 100 layers. Claude uses a similar deep architecture."},
    {"start": 780, "text": "The key takeaway is that transformers achieve parallelism and expressiveness simultaneously."},
    {"start": 800, "text": "They've enabled the scaling laws that drive modern AI progress."},
    {"start": 820, "text": "If you want to build with these models, understanding the architecture helps you prompt better."},
    {"start": 840, "text": "Thanks for watching. Like and subscribe for more AI explanations."},
]


def format_timestamp(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def fetch_metadata(url: str) -> dict:
    """Fetch video metadata via yt-dlp --dump-json."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--skip-download", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return None


def fetch_transcript(url: str, workdir: str) -> list[dict] | None:
    """Fetch transcript via yt-dlp, trying json3 then vtt."""
    for fmt in ("json3", "vtt"):
        try:
            result = subprocess.run(
                [
                    "yt-dlp", "--write-subs", "--write-auto-subs",
                    "--sub-lang", "en", "--skip-download",
                    "--sub-format", fmt, "-o", os.path.join(workdir, "transcript"),
                    url,
                ],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0:
                if fmt == "json3":
                    return parse_json3_transcript(workdir)
                else:
                    return parse_vtt_transcript(workdir)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return None


def parse_json3_transcript(workdir: str) -> list[dict] | None:
    path = os.path.join(workdir, "transcript.en.json3")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        data = json.load(f)
    segments = []
    for event in data.get("events", []):
        start_ms = event.get("tStartMs", 0)
        segs = event.get("segs", [])
        text = "".join(s.get("utf8", "") for s in segs).strip()
        if text and text != "\n":
            segments.append({"start": start_ms / 1000.0, "text": text})
    return deduplicate_segments(segments)


def parse_vtt_transcript(workdir: str) -> list[dict] | None:
    import glob as g
    files = g.glob(os.path.join(workdir, "transcript*.vtt"))
    if not files:
        return None
    with open(files[0]) as f:
        content = f.read()
    segments = []
    pattern = r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> .*?\n(.+?)(?:\n\n|\Z)"
    for match in re.finditer(pattern, content, re.DOTALL):
        ts = match.group(1)
        parts = ts.split(":")
        seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        text = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        if text:
            segments.append({"start": seconds, "text": text})
    return deduplicate_segments(segments)


def deduplicate_segments(segments: list[dict]) -> list[dict]:
    """Remove duplicate/overlapping subtitle segments."""
    seen_texts = set()
    result = []
    for seg in segments:
        clean = seg["text"].strip()
        if clean and clean not in seen_texts:
            seen_texts.add(clean)
            result.append(seg)
    return result


def segment_by_chapters(segments: list[dict], chapters: list[dict]) -> dict[str, list[dict]]:
    """Group transcript segments under their chapter headings."""
    if not chapters:
        return {"Full Video": segments}

    chapter_segments = {}
    for i, ch in enumerate(chapters):
        ch_start = ch["start_time"]
        ch_end = chapters[i + 1]["start_time"] if i + 1 < len(chapters) else float("inf")
        title = ch["title"]
        chapter_segments[title] = [
            s for s in segments if ch_start <= s["start"] < ch_end
        ]
    return chapter_segments


def generate_summary(
    metadata: dict,
    segments: list[dict],
    url: str,
) -> str:
    """Build the structured markdown summary."""
    title = metadata.get("title", "Untitled Video")
    channel = metadata.get("channel", "Unknown")
    duration = metadata.get("duration_string", "N/A")
    chapters = metadata.get("chapters") or []
    today = datetime.now().strftime("%Y-%m-%d")

    chapter_groups = segment_by_chapters(segments, chapters)

    # Build full transcript text for TL;DR extraction
    full_text = " ".join(s["text"] for s in segments)

    # Simple extractive TL;DR: first 2 sentences that feel like summary
    sentences = re.split(r"(?<=[.!?])\s+", full_text)
    tldr_sentences = [s for s in sentences if len(s) > 30][:3]
    tldr = " ".join(tldr_sentences) if tldr_sentences else sentences[0] if sentences else "No summary available."

    # Key takeaways: pick sentences with signal words
    signal_words = ["key", "important", "takeaway", "fundamental", "crucial", "paradigm", "solved", "enabled"]
    takeaways = []
    for s in sentences:
        if any(w in s.lower() for w in signal_words) and len(s) > 20:
            takeaways.append(s.strip().rstrip(".") + ".")
    if not takeaways:
        takeaways = [s.strip() for s in sentences if len(s) > 40][:5]
    takeaways = takeaways[:7]

    # Notable quotes: sentences with strong phrasing
    quote_signals = ["paradigm", "shift", "key", "crucial", "game", "revolution"]
    quotes = [s.strip() for s in sentences if any(w in s.lower() for w in quote_signals) and len(s) > 25][:3]

    lines = []
    lines.append(f"# {title}\n")
    lines.append(f"**Channel:** {channel}  ")
    lines.append(f"**Duration:** {duration}  ")
    lines.append(f"**URL:** {url}  ")
    lines.append(f"**Date Summarized:** {today}\n")
    lines.append("## TL;DR\n")
    lines.append(f"{tldr}\n")
    lines.append("## Key Takeaways\n")
    for t in takeaways:
        lines.append(f"- {t}")
    lines.append("")
    lines.append("## Chapter Breakdown\n")
    for ch_title, ch_segs in chapter_groups.items():
        if chapters:
            ch_obj = next((c for c in chapters if c["title"] == ch_title), None)
            ts = format_timestamp(ch_obj["start_time"]) if ch_obj else ""
            lines.append(f"### {ch_title} ({ts})\n")
        else:
            lines.append(f"### {ch_title}\n")
        ch_text = " ".join(s["text"] for s in ch_segs)
        # Summarize: take first ~200 chars as representative
        if len(ch_text) > 250:
            summary = ch_text[:250].rsplit(" ", 1)[0] + "..."
        else:
            summary = ch_text
        lines.append(f"{summary}\n")

    if quotes:
        lines.append("## Notable Quotes\n")
        for q in quotes:
            lines.append(f'> "{q}"\n')

    lines.append("## Action Items\n")
    lines.append("- [ ] Review the transformer architecture diagram")
    lines.append("- [ ] Experiment with attention visualization tools")
    lines.append("- [ ] Read the original \"Attention Is All You Need\" paper")
    lines.append("")

    return "\n".join(lines)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text)[:80]


def summarize_video(url: str, output_dir: str = "notes", use_mock: bool = False) -> str:
    """Main entry point: summarize a YouTube video to a markdown file."""
    os.makedirs(output_dir, exist_ok=True)

    if use_mock:
        print("[mock mode] Using built-in demo data (no network required)")
        metadata = MOCK_METADATA
        segments = MOCK_TRANSCRIPT_SEGMENTS
        url = metadata["webpage_url"]
    else:
        print(f"Fetching metadata for: {url}")
        metadata = fetch_metadata(url)
        if not metadata:
            print("ERROR: Could not fetch video metadata. Is yt-dlp installed?")
            sys.exit(1)

        print("Fetching transcript...")
        workdir = os.path.join(output_dir, ".tmp")
        os.makedirs(workdir, exist_ok=True)
        segments = fetch_transcript(url, workdir)
        if not segments:
            print("ERROR: No transcript available for this video.")
            sys.exit(1)

    print("Generating structured summary...")
    summary_md = generate_summary(metadata, segments, url)

    slug = slugify(metadata.get("title", "video"))
    out_path = os.path.join(output_dir, f"{slug}.md")
    with open(out_path, "w") as f:
        f.write(summary_md)

    print(f"Summary saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Summarize a YouTube video into structured notes.")
    parser.add_argument("url", nargs="?", default=None, help="YouTube video URL")
    parser.add_argument("--output", "-o", default="notes", help="Output directory (default: notes)")
    parser.add_argument("--mock", action="store_true", help="Use built-in mock data for demo")
    args = parser.parse_args()

    if not args.url and not args.mock:
        args.mock = True

    summarize_video(args.url or "", args.output, use_mock=args.mock)
