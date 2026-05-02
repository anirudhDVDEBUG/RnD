---
name: scenelens_video_analysis
description: |
  Scene-aware video analysis with frame extraction, per-frame OCR, and auto-chunked Whisper transcripts.
  TRIGGER: video analysis, extract frames from video, video OCR, transcribe video, video scene detection, analyze video content, video-to-text, extract text from video frames, whisper transcript from video, scenelens
---

# SceneLens Video Analysis

Give Claude smarter video input. Scene-aware frame extraction, per-frame OCR, and auto-chunked Whisper transcripts.

## When to use

- "Analyze this video and extract key frames"
- "Transcribe the audio from this video file"
- "Extract text/OCR from video frames"
- "Summarize what happens in this video"
- "Get scene-by-scene breakdown of this video"

## How to use

### Prerequisites

Ensure the following system dependencies are installed:

```bash
# Install system dependencies
sudo apt-get install -y ffmpeg tesseract-ocr

# Install Python package
pip install scenelens

# Optional: for YouTube video support
pip install yt-dlp

# Optional: for audio transcription
pip install openai-whisper
```

### Step 1: Install SceneLens

```bash
pip install scenelens
```

If not yet installed, install it before proceeding.

### Step 2: Extract frames and analyze video

Use the `scenelens` CLI or Python API to process video files:

**CLI usage:**

```bash
# Scene-aware frame extraction
scenelens extract <video_path> --output-dir ./frames

# Extract frames with OCR text from each frame
scenelens extract <video_path> --ocr --output-dir ./frames

# Transcribe audio using Whisper
scenelens transcribe <video_path> --output transcript.txt

# Full analysis: frames + OCR + transcript
scenelens analyze <video_path> --ocr --transcribe --output-dir ./output
```

**Python API usage:**

```python
from scenelens import SceneLens

lens = SceneLens()

# Extract scene-aware keyframes
frames = lens.extract_frames("video.mp4")

# Get OCR text from each frame
for frame in frames:
    print(frame.timestamp, frame.ocr_text)

# Get Whisper transcript (auto-chunked for long videos)
transcript = lens.transcribe("video.mp4")
print(transcript.text)
```

### Step 3: Use extracted data

Once frames and transcripts are extracted, you can:

- Read the OCR text and transcript to summarize video content
- Analyze individual keyframes as images for visual understanding
- Combine OCR text + transcript for comprehensive video-to-text conversion
- Process YouTube URLs directly (requires `yt-dlp`)

### Working with YouTube videos

```bash
# Download and analyze a YouTube video
scenelens analyze "https://youtube.com/watch?v=..." --ocr --transcribe --output-dir ./output
```

### Tips

- Scene-aware extraction picks visually distinct keyframes rather than fixed intervals, reducing redundant frames
- For long videos, Whisper transcripts are auto-chunked to handle memory constraints
- OCR works best on frames with clear, readable text (slides, terminals, captions)
- Use `--output-dir` to organize extracted frames and metadata

## References

- Source repository: https://github.com/ravindranathpathi/scenelens
- Dependencies: ffmpeg, tesseract-ocr, yt-dlp (optional), openai-whisper (optional)
