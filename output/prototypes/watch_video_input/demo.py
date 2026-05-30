#!/usr/bin/env python3
"""Demo of the Watch pipeline using mock data.

Simulates the full download -> extract frames -> transcribe flow
without requiring yt-dlp, ffmpeg, or mlx-whisper to be installed.
Produces realistic terminal output so you can see what the tool does.
"""

import os
import sys
import time
from pathlib import Path

OUTPUT_DIR = Path(".watch_output_demo")
FRAMES_DIR = OUTPUT_DIR / "frames"

# Simulated transcript from a tech talk
MOCK_TRANSCRIPT = """[00:00] Welcome everyone. Today we're going to talk about building AI-powered workflows.
[00:08] The key insight is that large language models work best when you give them structured context.
[00:15] Instead of dumping raw data, you should preprocess it into the modalities the model handles well.
[00:23] For video, that means extracting key frames as images and transcribing the audio to text.
[00:31] This is exactly what tools like Watch do — they bridge the gap between video and LLM input.
[00:40] Let me show you a quick demo of how this works in practice.
[00:47] First, we download the video using yt-dlp, which supports over a thousand websites.
[00:55] Then ffmpeg extracts frames at adaptive intervals — shorter videos get more frames per minute.
[01:03] Finally, mlx-whisper runs the transcription entirely on your local machine.
[01:10] No API keys, no cloud services, no data leaving your laptop.
[01:17] The result is a set of JPEG frames plus a timestamped transcript, both ready for Claude.
[01:25] You can then ask Claude to summarize, analyze, or generate content from the video.
[01:33] This is particularly powerful for content teams who need to process competitor videos,
[01:40] extract key quotes from conference talks, or generate blog posts from webinars.
[01:48] Let's look at the architecture in more detail..."""

MOCK_METADATA = {
    "title": "Building AI-Powered Workflows with Video Input",
    "duration": 312,
    "resolution": "1080p",
    "uploader": "TechTalks",
    "view_count": 14200,
}


def create_mock_frame(path, index, total):
    """Create a small placeholder JPEG-like file."""
    # Write a minimal valid file to represent a frame
    content = f"[Mock frame {index}/{total} — extracted at {index * 5}s]\n"
    content += f"Resolution: 1280x720\n"
    content += f"Scene: Slide {index} of presentation\n"
    path.write_text(content)


def animate(msg, duration=0.3):
    """Print with a brief pause to simulate work."""
    print(msg, end="", flush=True)
    time.sleep(duration)


def main():
    url = "https://www.youtube.com/watch?v=DEMO_VIDEO_ID"
    print("=" * 60)
    print("  Watch — Video Input for Claude Code (DEMO MODE)")
    print("=" * 60)
    print()
    print(f"  URL: {url}")
    print()

    # Clean up previous demo output
    if OUTPUT_DIR.exists():
        import shutil
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True)
    FRAMES_DIR.mkdir(parents=True)

    # Step 1: Simulate download
    animate("Downloading video... ")
    duration = MOCK_METADATA["duration"]
    duration_str = f"{duration // 60}m{duration % 60:02d}s"
    print("done")
    print(f'  Title: "{MOCK_METADATA["title"]}"')
    print(f"  Duration: {duration_str}")
    print(f"  Resolution: {MOCK_METADATA['resolution']}")
    print()

    # Step 2: Simulate frame extraction
    num_frames = 12
    animate("Extracting frames... ")
    for i in range(1, num_frames + 1):
        frame_path = FRAMES_DIR / f"frame_{i:03d}.jpg"
        create_mock_frame(frame_path, i, num_frames)
    print(f"done ({num_frames} frames)")
    print(f"  Saved to: {FRAMES_DIR}/")
    print()

    # Step 3: Simulate transcription
    animate("Transcribing audio... ")
    transcript_path = OUTPUT_DIR / "transcript.txt"
    transcript_path.write_text(MOCK_TRANSCRIPT)
    print("done (mlx-whisper, local)")
    print(f"  Saved to: {transcript_path}")

    # Show transcript
    print()
    print("-" * 60)
    print("TRANSCRIPT")
    print("-" * 60)
    print(MOCK_TRANSCRIPT)

    # Show frame listing
    print("-" * 60)
    print("EXTRACTED FRAMES")
    print("-" * 60)
    for f in sorted(FRAMES_DIR.glob("frame_*.jpg")):
        print(f"  {f.name}")

    # Summary
    print()
    print("-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"  Video: {MOCK_METADATA['title']}")
    print(f"  Duration: {duration_str}")
    print(f"  Frames extracted: {num_frames}")
    print(f"  Transcript length: {len(MOCK_TRANSCRIPT)} chars")
    print(f"  Output directory: {OUTPUT_DIR}/")
    print()
    print("In production, Claude would now receive these frames as images")
    print("and the transcript as text, enabling multimodal video analysis.")
    print()
    print("Try with a real video:")
    print(f'  python watch.py "https://www.youtube.com/watch?v=..."')

    # Cleanup note
    return 0


if __name__ == "__main__":
    sys.exit(main())
