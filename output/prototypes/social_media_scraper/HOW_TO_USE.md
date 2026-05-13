# How to Use

## This is a Claude Code Skill

It's not a standalone CLI — it teaches Claude Code how to scrape social media posts when you paste a link.

## Install the Skill

### 1. Create the skill directory

```bash
mkdir -p ~/.claude/skills/social_media_scraper
```

### 2. Copy the skill file

```bash
cp SKILL.md ~/.claude/skills/social_media_scraper/SKILL.md
```

Or clone the source repo directly:

```bash
git clone https://github.com/elbis330/social-media-scraper-skill.git
cp social-media-scraper-skill/SKILL.md ~/.claude/skills/social_media_scraper/SKILL.md
```

### 3. Install system dependencies

```bash
# Required: media downloader
pip install yt-dlp

# Optional: audio transcription
pip install openai-whisper

# Optional: video processing (pick your OS)
# macOS:
brew install ffmpeg jq
# Ubuntu/Debian:
sudo apt install ffmpeg jq

# Optional: AI video analysis
export GEMINI_API_KEY="your-key-here"
```

### 4. Restart Claude Code

The skill activates automatically — no config file edits needed.

## Trigger Phrases

Claude will invoke this skill when you:

- Paste any Instagram, TikTok, Twitter/X, or YouTube URL
- Say "scrape this post"
- Say "extract metadata from this video"
- Say "transcribe this YouTube video"
- Say "analyze this TikTok"
- Say "get the comments from this post"

## First 60 Seconds

After installing the skill and dependencies:

```
You:  Scrape this: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Claude: [runs yt-dlp to extract metadata]
        [downloads audio, runs Whisper for transcription]
        [extracts frames, sends to Gemini for visual analysis]

        ### Post Metadata
        - Author: @RickAstley
        - Platform: youtube
        - Date: 2009-10-25
        - Views: 1,600,000,000 | Likes: 16,000,000 | Comments: 3,200,000

        ### Content
        Rick Astley - Never Gonna Give You Up (Official Music Video)

        ### Transcription
        We're no strangers to love, you know the rules and so do I...

        ### Video Analysis
        Music video featuring a man in a trench coat dancing in various
        urban locations. 1980s aesthetic with warm color grading...

        ### Top Comments
        1. @musicfan: This song never gets old (234k likes)
        2. @rickrolled: I came here voluntarily this time (189k likes)
```

**What you get:** structured markdown with metadata, full transcription, AI visual analysis, and top comments — all from a single URL.

## Running the Demo (No Dependencies)

```bash
bash run.sh
```

This runs `demo.py` with mock data so you can see the output format without installing anything beyond Python 3.

## Live Scraping (With Dependencies)

```bash
pip install yt-dlp openai-whisper requests
python3 demo.py https://www.youtube.com/watch?v=VIDEO_ID
```
