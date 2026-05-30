#!/usr/bin/env python3
"""Watch — Video Input for Claude Code.

Downloads video from any yt-dlp supported site, extracts key frames,
and transcribes audio locally with mlx-whisper / openai-whisper.
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_dependency(name, check_cmd):
    """Check if a system dependency is available."""
    try:
        subprocess.run(check_cmd, capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_video(url, output_dir):
    """Download video using yt-dlp. Returns path to downloaded file and metadata."""
    output_template = str(output_dir / "video.%(ext)s")
    info_file = str(output_dir / "info.json")

    print("Downloading video...", end=" ", flush=True)

    # First get metadata
    cmd_info = [
        "yt-dlp", "--dump-json", "--no-download", url
    ]
    result = subprocess.run(cmd_info, capture_output=True, text=True)
    if result.returncode != 0:
        print("FAILED")
        print(f"  Error: {result.stderr.strip()}")
        sys.exit(1)

    metadata = json.loads(result.stdout)
    title = metadata.get("title", "Unknown")
    duration = metadata.get("duration", 0)

    # Download the video
    cmd_download = [
        "yt-dlp",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--no-playlist",
        url
    ]
    result = subprocess.run(cmd_download, capture_output=True, text=True)
    if result.returncode != 0:
        print("FAILED")
        print(f"  Error: {result.stderr.strip()}")
        sys.exit(1)

    # Find the downloaded file
    video_files = list(output_dir.glob("video.*"))
    if not video_files:
        print("FAILED")
        print("  Error: No video file found after download")
        sys.exit(1)

    video_path = video_files[0]
    duration_str = f"{int(duration // 60)}m{int(duration % 60):02d}s" if duration else "unknown"
    print("done")
    print(f"  Title: \"{title}\"")
    print(f"  Duration: {duration_str}")

    return video_path, metadata


def extract_frames(video_path, frames_dir, interval=None, duration=None):
    """Extract frames from video using ffmpeg."""
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Adaptive interval: aim for ~10-20 frames
    if interval is None:
        if duration and duration > 0:
            interval = max(2, duration / 15)
        else:
            interval = 5

    print("Extracting frames...", end=" ", flush=True)

    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        str(frames_dir / "frame_%03d.jpg"),
        "-y", "-loglevel", "error"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FAILED")
        print(f"  Error: {result.stderr.strip()}")
        return []

    frames = sorted(frames_dir.glob("frame_*.jpg"))
    print(f"done ({len(frames)} frames)")
    return frames


def extract_audio(video_path, audio_path):
    """Extract audio track from video using ffmpeg."""
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        str(audio_path),
        "-y", "-loglevel", "error"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def transcribe_audio(audio_path, output_path):
    """Transcribe audio using mlx-whisper or openai-whisper."""
    print("Transcribing audio...", end=" ", flush=True)

    # Try mlx-whisper first (Apple Silicon)
    try:
        import mlx_whisper
        result = mlx_whisper.transcribe(
            str(audio_path),
            path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
        )
        segments = result.get("segments", [])
        transcript_lines = []
        for seg in segments:
            start = seg.get("start", 0)
            text = seg.get("text", "").strip()
            mins, secs = divmod(int(start), 60)
            transcript_lines.append(f"[{mins:02d}:{secs:02d}] {text}")

        transcript = "\n".join(transcript_lines)
        output_path.write_text(transcript)
        print("done (mlx-whisper, local)")
        return transcript

    except ImportError:
        pass

    # Fallback to openai-whisper
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path))
        segments = result.get("segments", [])
        transcript_lines = []
        for seg in segments:
            start = seg.get("start", 0)
            text = seg.get("text", "").strip()
            mins, secs = divmod(int(start), 60)
            transcript_lines.append(f"[{mins:02d}:{secs:02d}] {text}")

        transcript = "\n".join(transcript_lines)
        output_path.write_text(transcript)
        print("done (openai-whisper, local)")
        return transcript

    except ImportError:
        print("FAILED")
        print("  Error: Neither mlx-whisper nor openai-whisper is installed.")
        print("  Install with: pip install mlx-whisper  (Apple Silicon)")
        print("            or: pip install openai-whisper  (other platforms)")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Watch — Download, extract frames, and transcribe video"
    )
    parser.add_argument("url", help="Video URL to process")
    parser.add_argument(
        "--output-dir", default=".watch_output",
        help="Output directory (default: .watch_output)"
    )
    parser.add_argument(
        "--frame-interval", type=float, default=None,
        help="Seconds between frame captures (default: auto)"
    )
    parser.add_argument(
        "--no-transcribe", action="store_true",
        help="Skip audio transcription"
    )
    args = parser.parse_args()

    # Check dependencies
    if not check_dependency("yt-dlp", ["yt-dlp", "--version"]):
        print("Error: yt-dlp is not installed. Run: pip install yt-dlp")
        sys.exit(1)
    if not check_dependency("ffmpeg", ["ffmpeg", "-version"]):
        print("Error: ffmpeg is not installed. Run: brew install ffmpeg")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = output_dir / "frames"

    # Step 1: Download
    video_path, metadata = download_video(args.url, output_dir)
    duration = metadata.get("duration", 0)

    # Step 2: Extract frames
    frames = extract_frames(video_path, frames_dir, args.frame_interval, duration)

    # Step 3: Transcribe
    if not args.no_transcribe:
        audio_path = output_dir / "audio.wav"
        if extract_audio(video_path, audio_path):
            transcript_path = output_dir / "transcript.txt"
            transcript = transcribe_audio(audio_path, transcript_path)
            if transcript:
                print(f"\n--- TRANSCRIPT ---")
                print(transcript[:2000])
                if len(transcript) > 2000:
                    print(f"\n... ({len(transcript)} chars total, see {transcript_path})")
        else:
            print("Warning: Could not extract audio track")

    print(f"\nOutput saved to: {output_dir}/")
    print(f"  Frames: {len(frames)} files in {frames_dir}/")
    if not args.no_transcribe:
        print(f"  Transcript: {output_dir / 'transcript.txt'}")


if __name__ == "__main__":
    main()
