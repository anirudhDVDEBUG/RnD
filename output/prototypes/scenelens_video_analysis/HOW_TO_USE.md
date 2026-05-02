# How to Use SceneLens

## Install

```bash
# System dependencies
sudo apt-get install -y ffmpeg tesseract-ocr

# Python package
pip install scenelens

# Optional extras
pip install yt-dlp          # YouTube support
pip install openai-whisper   # Audio transcription
```

## Use as a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/scenelens_video_analysis
cp SKILL.md ~/.claude/skills/scenelens_video_analysis/SKILL.md
```

### Trigger phrases

Say any of these to Claude and the skill activates:

- "Analyze this video and extract key frames"
- "Transcribe the audio from this video file"
- "Extract text/OCR from video frames"
- "Get scene-by-scene breakdown of this video"
- "video analysis", "video OCR", "scenelens"

## CLI Usage (without Claude)

```bash
# Scene-aware frame extraction
scenelens extract video.mp4 --output-dir ./frames

# Frames + OCR
scenelens extract video.mp4 --ocr --output-dir ./frames

# Audio transcription
scenelens transcribe video.mp4 --output transcript.txt

# Full pipeline
scenelens analyze video.mp4 --ocr --transcribe --output-dir ./output
```

## Python API

```python
from scenelens import SceneLens

lens = SceneLens()
frames = lens.extract_frames("video.mp4")

for frame in frames:
    print(frame.timestamp, frame.ocr_text)

transcript = lens.transcribe("video.mp4")
print(transcript.text)
```

## First 60 Seconds

```bash
# 1. Install
pip install scenelens

# 2. Point at any video
scenelens analyze demo.mp4 --ocr --transcribe --output-dir ./out

# 3. See results
ls ./out/
#   frames/
#     frame_001_00m12s.png
#     frame_002_00m34s.png
#     ...
#   ocr_results.json
#   transcript.txt
#   summary.json

cat ./out/ocr_results.json | python -m json.tool
# {
#   "frame_001_00m12s.png": "Welcome to the Demo",
#   "frame_002_00m34s.png": "pip install mypackage",
#   ...
# }
```

**Input:** A video file (local or YouTube URL)
**Output:** Keyframes as PNGs + OCR JSON + chunked transcript text

## Demo (no real video needed)

```bash
bash run.sh
```

Runs a mock pipeline showing the full extraction flow with synthetic data.
