# Technical Details

## What It Does

This is a Claude Code skill that orchestrates four CLI tools to scrape social media posts end-to-end. When a user pastes a URL from Instagram, TikTok, Twitter/X, or YouTube, Claude runs a pipeline: (1) extract metadata and comments via `yt-dlp --dump-json`, (2) download the media file, (3) transcribe audio with OpenAI Whisper, (4) extract video frames with `ffmpeg` and analyze them via the Gemini multimodal API. Results are compiled into structured markdown.

The skill itself contains no code — it's a prompt-based instruction file (`SKILL.md`) that teaches Claude which shell commands to run and in what order. The Python module in this prototype (`social_media_scraper.py`) wraps the same pipeline programmatically for use outside Claude Code.

## Architecture

```
User pastes URL
    |
    v
Platform detection (regex on URL)
    |
    v
yt-dlp --dump-json        -->  metadata (title, author, views, likes, date)
yt-dlp --write-comments   -->  comments array
yt-dlp -o <path>          -->  downloaded media file
    |
    v
whisper <file>             -->  text transcription
ffmpeg -vf fps=1           -->  extracted frames (1/sec)
    |
    v
Gemini API (multimodal)    -->  visual analysis summary
    |
    v
Formatted markdown output
    |
    v
Cleanup temp files
```

### Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill definition — drop into `~/.claude/skills/social_media_scraper/` |
| `social_media_scraper.py` | Python module wrapping the full pipeline |
| `demo.py` | Demo script with mock data + live scraping mode |
| `run.sh` | One-command demo runner |

### Dependencies

| Tool | Role | Required? |
|------|------|-----------|
| `yt-dlp` | Media download + metadata extraction | Yes (for live use) |
| `whisper` | Audio-to-text transcription | Optional |
| `ffmpeg` | Video frame extraction | Optional (needed for Gemini analysis) |
| `jq` | JSON processing in shell | Optional (Claude can parse JSON directly) |
| `GEMINI_API_KEY` | Multimodal video analysis via Gemini | Optional |

### Model Calls

- **Whisper** (local): runs entirely on-device. Model sizes range from `tiny` (39M params) to `large` (1.5B). The skill defaults to `base` (74M) for speed.
- **Gemini API** (remote): sends up to 10 extracted JPEG frames for multimodal analysis. Requires `GEMINI_API_KEY` env var. Uses `gemini-2.0-flash` for cost efficiency.
- **No Claude API calls** — the skill runs inside Claude Code's existing session; Claude itself is the orchestrator.

## Limitations

- **Authentication-gated content**: private Instagram accounts, subscriber-only YouTube videos, and protected tweets require cookies passed to yt-dlp (`--cookies`). The skill mentions this but doesn't automate cookie extraction.
- **Rate limits**: heavy use will hit platform rate limits. No built-in retry/backoff logic.
- **Ephemeral stories**: Instagram/TikTok stories may expire before scraping completes.
- **No structured data storage**: results are returned as markdown text in the chat. There's no database, no export to CSV/JSON, no integration with downstream tools.
- **Whisper accuracy**: the `base` model struggles with non-English content, heavy accents, and background music. Users must manually switch to `medium` or `large` for better accuracy.
- **Frame-based video analysis**: extracting 1 frame/sec misses fast cuts and motion. Not a substitute for full video understanding.
- **No sentiment analysis or trend detection** — it extracts raw data but doesn't analyze it.

## Why It Matters for Claude-Driven Products

**Lead generation**: Scrape competitor social posts to identify engaged prospects in comments. Extract contact-adjacent signals (company mentions, pain points) from comment threads.

**Marketing & ad creatives**: Pull top-performing post metadata (engagement ratios, caption styles) to inform content strategy. Transcribe competitor video ads to reverse-engineer messaging frameworks.

**Agent factories**: This skill is a building block for social listening agents. Combine with scheduling (cron) and a database to build an autonomous monitor that tracks competitor posts, extracts trends, and surfaces insights daily.

**Voice AI**: Whisper transcriptions can feed voice-AI training pipelines or be used to generate synthetic voice scripts based on what's performing well on social media.
