#!/usr/bin/env python3
"""
SceneLens Demo — Mock pipeline showing the full extraction flow.
Produces realistic output without requiring actual video files or system deps.
"""

import json
import os
import time
import random

# Mock data simulating real SceneLens output
MOCK_VIDEO = {
    "filename": "product_demo_2024.mp4",
    "duration_seconds": 150,
    "resolution": "1920x1080",
    "fps": 30,
}

MOCK_KEYFRAMES = [
    {"index": 1, "timestamp": "00:00:03", "scene_score": 0.82, "ocr_text": "ProductName v2.0 - Getting Started"},
    {"index": 2, "timestamp": "00:00:18", "scene_score": 0.65, "ocr_text": ""},
    {"index": 3, "timestamp": "00:00:42", "scene_score": 0.71, "ocr_text": "pip install productname"},
    {"index": 4, "timestamp": "00:01:05", "scene_score": 0.58, "ocr_text": "from productname import Client\nclient = Client(api_key='...')"},
    {"index": 5, "timestamp": "00:01:22", "scene_score": 0.77, "ocr_text": "$ curl -X POST https://api.example.com/v1/analyze"},
    {"index": 6, "timestamp": "00:01:48", "scene_score": 0.63, "ocr_text": "Response: {\"status\": \"success\", \"results\": 42}"},
    {"index": 7, "timestamp": "00:02:10", "scene_score": 0.69, "ocr_text": ""},
    {"index": 8, "timestamp": "00:02:28", "scene_score": 0.85, "ocr_text": "Try it free at productname.io/signup"},
]

MOCK_TRANSCRIPT_CHUNKS = [
    {
        "chunk": 1,
        "start": "00:00:00",
        "end": "00:00:55",
        "text": "Welcome to ProductName version two point zero. In this demo, I'll show you how to get started in under five minutes. First, let's install the package using pip. It's a single command and pulls in all dependencies automatically."
    },
    {
        "chunk": 2,
        "start": "00:00:55",
        "end": "00:01:50",
        "text": "Now let's write some code. Import the client, pass your API key, and you're ready to make requests. Here I'm sending a POST request to the analyze endpoint. Notice how the response comes back in under two hundred milliseconds with structured JSON."
    },
    {
        "chunk": 3,
        "start": "00:01:50",
        "end": "00:02:30",
        "text": "That's really all there is to it. Three lines of code to get production-ready analysis. Head to productname dot io slash signup to get your free API key. Thanks for watching and happy building."
    },
]


def simulate_extraction():
    """Simulate the SceneLens extraction pipeline with realistic timing."""
    output_dir = "demo_output"
    os.makedirs(f"{output_dir}/frames", exist_ok=True)

    print(f"{'='*60}")
    print(f"  SceneLens Demo — Mock Video Analysis Pipeline")
    print(f"{'='*60}\n")

    # Step 1: Video info
    print(f"[SceneLens] Input: {MOCK_VIDEO['filename']}")
    print(f"[SceneLens] Duration: {MOCK_VIDEO['duration_seconds']}s | "
          f"Resolution: {MOCK_VIDEO['resolution']} | FPS: {MOCK_VIDEO['fps']}")
    print()

    # Step 2: Scene detection
    print("[SceneLens] Running scene-change detection (threshold=0.3)...")
    time.sleep(0.3)
    total_possible = MOCK_VIDEO['duration_seconds'] * 1  # 1fps baseline
    print(f"[SceneLens] Extracted {len(MOCK_KEYFRAMES)} keyframes "
          f"(vs {total_possible} at 1fps) — {len(MOCK_KEYFRAMES)/total_possible*100:.0f}% reduction")
    print()

    # Step 3: OCR
    print("[SceneLens] Running OCR on extracted frames...")
    time.sleep(0.2)
    frames_with_text = sum(1 for f in MOCK_KEYFRAMES if f["ocr_text"])
    print(f"[SceneLens] OCR detected text in {frames_with_text}/{len(MOCK_KEYFRAMES)} frames")
    print()

    # Step 4: Transcription
    print("[SceneLens] Transcribing audio (Whisper base model, auto-chunked)...")
    time.sleep(0.3)
    total_words = sum(len(c["text"].split()) for c in MOCK_TRANSCRIPT_CHUNKS)
    print(f"[SceneLens] Transcript: {len(MOCK_TRANSCRIPT_CHUNKS)} chunks, {total_words} words")
    print()

    # Step 5: Display results
    print(f"{'─'*60}")
    print("KEYFRAMES WITH OCR TEXT:")
    print(f"{'─'*60}")
    for frame in MOCK_KEYFRAMES:
        ocr = frame["ocr_text"] if frame["ocr_text"] else "(no text detected)"
        marker = "*" if frame["ocr_text"] else " "
        print(f"  {marker} Frame {frame['index']:2d} [{frame['timestamp']}] "
              f"(score: {frame['scene_score']:.2f})")
        if frame["ocr_text"]:
            for line in frame["ocr_text"].split("\n"):
                print(f"      OCR: \"{line}\"")
    print()

    print(f"{'─'*60}")
    print("TRANSCRIPT:")
    print(f"{'─'*60}")
    for chunk in MOCK_TRANSCRIPT_CHUNKS:
        print(f"  [{chunk['start']} - {chunk['end']}]")
        print(f"  {chunk['text']}")
        print()

    # Step 6: Write output files
    ocr_results = {
        f"frame_{f['index']:03d}_{f['timestamp'].replace(':', 'm', 1).replace(':', 's')}.png": f["ocr_text"]
        for f in MOCK_KEYFRAMES
    }

    with open(f"{output_dir}/ocr_results.json", "w") as fp:
        json.dump(ocr_results, fp, indent=2)

    full_transcript = "\n\n".join(
        f"[{c['start']} - {c['end']}]\n{c['text']}" for c in MOCK_TRANSCRIPT_CHUNKS
    )
    with open(f"{output_dir}/transcript.txt", "w") as fp:
        fp.write(full_transcript)

    summary = {
        "video": MOCK_VIDEO,
        "keyframes_extracted": len(MOCK_KEYFRAMES),
        "frames_with_ocr_text": frames_with_text,
        "transcript_chunks": len(MOCK_TRANSCRIPT_CHUNKS),
        "total_words": total_words,
        "ocr_highlights": [f["ocr_text"] for f in MOCK_KEYFRAMES if f["ocr_text"]],
    }
    with open(f"{output_dir}/summary.json", "w") as fp:
        json.dump(summary, fp, indent=2)

    # Create placeholder frame files
    for frame in MOCK_KEYFRAMES:
        fname = f"frame_{frame['index']:03d}_{frame['timestamp'].replace(':', 'm', 1).replace(':', 's')}.png"
        with open(f"{output_dir}/frames/{fname}", "w") as fp:
            fp.write(f"[placeholder for keyframe at {frame['timestamp']}]\n")

    print(f"{'─'*60}")
    print("OUTPUT FILES:")
    print(f"{'─'*60}")
    print(f"  {output_dir}/frames/          — {len(MOCK_KEYFRAMES)} keyframe images")
    print(f"  {output_dir}/ocr_results.json — OCR text per frame")
    print(f"  {output_dir}/transcript.txt   — Full transcript with timestamps")
    print(f"  {output_dir}/summary.json     — Analysis summary")
    print()
    print(f"{'='*60}")
    print("  Done. In production, replace mock data with:")
    print("    scenelens analyze <video.mp4> --ocr --transcribe --output-dir ./out")
    print(f"{'='*60}")


if __name__ == "__main__":
    simulate_extraction()
