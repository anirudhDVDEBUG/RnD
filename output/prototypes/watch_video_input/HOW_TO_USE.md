# How to Use — Watch Video Input

## Install

### 1. System dependencies

```bash
# ffmpeg (required for frame extraction)
brew install ffmpeg          # macOS
# sudo apt install ffmpeg    # Ubuntu/Debian

# yt-dlp (required for video downloading)
pip install yt-dlp
```

### 2. Transcription engine

```bash
# Apple Silicon (M1/M2/M3/M4) — recommended
pip install mlx-whisper

# Linux / Intel Mac — use standard whisper instead
pip install openai-whisper
```

### 3. Clone the watch tool

```bash
git clone https://github.com/mathiaschu/watch.git
cd watch
pip install -e .
```

## Setting up as a Claude Code Skill

Drop the skill folder so Claude Code auto-discovers it:

```bash
mkdir -p ~/.claude/skills/watch_video_input
cp SKILL.md ~/.claude/skills/watch_video_input/SKILL.md
```

### Trigger phrases

Once installed, any of these will activate the skill:

- `/watch <URL>`
- "Watch this video and summarize it"
- "Transcribe this video"
- "Analyze this video"
- "Download and transcribe <URL>"
- "Extract frames from this video"
- "Get the transcript from this video"

## First 60 Seconds

**Input:**
```
/watch https://www.youtube.com/watch?v=abc123
```

**What happens:**

1. yt-dlp downloads the video to a temp directory
2. ffmpeg extracts one frame every N seconds (adaptive based on video length)
3. mlx-whisper transcribes the full audio track locally on your Mac
4. Claude receives both the extracted frames (as images) and the transcript text

**Output you see:**
```
Downloading video... done
  Title: "Example Video Title"
  Duration: 4m12s
  Resolution: 1080p

Extracting frames... done
  12 frames saved to .watch_output/frames/

Transcribing audio... done
  Transcript saved to .watch_output/transcript.txt

--- TRANSCRIPT ---
[00:00] Hello and welcome to today's video...
[00:15] We'll be covering three main topics...
[01:02] First, let's talk about...
...
```

**Then ask Claude anything about the video:**
- "Summarize the key points"
- "What was said at the 2-minute mark?"
- "Describe what's shown in the frames"
- "Create a blog post from this video"

## Usage Outside Claude Code

You can also run the tool standalone from the command line:

```bash
python watch.py "https://www.youtube.com/watch?v=abc123"
```

Options:
```
python watch.py <URL> [--output-dir DIR] [--frame-interval SECS] [--no-transcribe]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--output-dir` | `.watch_output` | Where to save frames and transcript |
| `--frame-interval` | auto | Seconds between extracted frames |
| `--no-transcribe` | false | Skip audio transcription, only extract frames |
