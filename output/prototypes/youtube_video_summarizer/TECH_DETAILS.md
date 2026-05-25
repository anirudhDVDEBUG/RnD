# Technical Details

## What It Does

This tool converts YouTube videos into structured markdown notes by extracting transcripts and metadata via `yt-dlp`, then applying extractive summarization heuristics to produce a TL;DR, key takeaways, chapter-by-chapter breakdown, notable quotes, and action items. It works entirely locally -- no LLM API calls are made for the summarization step (the skill is designed so that Claude itself acts as the summarizer when used as a Claude Code skill, but the standalone script uses rule-based extraction).

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `summarizer.py` | Main implementation: transcript fetching, parsing, summary generation |
| `SKILL.md` | Claude Code skill definition with trigger phrases and step-by-step instructions |
| `run.sh` | Demo runner using mock data |

### Data Flow

```
YouTube URL
    |
    v
yt-dlp --dump-json        -->  metadata (title, channel, duration, chapters)
yt-dlp --write-auto-subs  -->  transcript (json3 or vtt format)
    |
    v
Parse & deduplicate segments
    |
    v
Segment transcript by chapter timestamps
    |
    v
Extractive summarization (signal-word matching, sentence selection)
    |
    v
Markdown output --> notes/<slug>.md
```

### Dependencies

- **Python 3.10+** (stdlib only, no pip packages)
- **yt-dlp** (system tool) -- fetches transcripts and metadata from YouTube
- **ffmpeg** (optional) -- only needed for frame/slide extraction at chapter timestamps

### How the Skill Works with Claude

When installed as a Claude Code skill, the `SKILL.md` file instructs Claude to:
1. Run `yt-dlp` shell commands to fetch transcript and metadata
2. Parse the output itself (Claude reads the JSON/VTT)
3. Generate the summary using its own language understanding (much higher quality than the rule-based standalone version)

This means the **Claude-as-skill version produces LLM-quality summaries** while the standalone script uses simpler heuristics.

## Limitations

- **Transcript required**: Videos without auto-generated or manual subtitles cannot be summarized. The tool will fail gracefully with an error message.
- **English only**: Currently hardcoded to `--sub-lang en`. Other languages would need the flag changed.
- **No LLM in standalone mode**: The `summarizer.py` script uses simple extractive heuristics (signal-word matching). Summaries are functional but not as polished as when Claude generates them via the skill.
- **No speaker diarization**: Multi-speaker videos won't attribute quotes to specific speakers.
- **Rate limits**: YouTube may throttle or block `yt-dlp` requests if used heavily.
- **Slide extraction is basic**: Frame extraction via ffmpeg captures the frame at chapter timestamps, which may not correspond to actual slides.

## Why It Matters

For teams building Claude-driven products:

- **Content marketing / lead-gen**: Automatically summarize competitor webinars, conference talks, or product demos into digestible briefs. Feed summaries into content pipelines.
- **Agent factories**: Use as a building block in multi-step agents that research topics across YouTube, summarize findings, and synthesize reports.
- **Ad creative research**: Quickly extract key messages and hooks from competitor video ads or industry thought-leader content.
- **Knowledge management**: Build an Obsidian/Notion vault of video summaries that your team (or other agents) can search and reference.
- **Voice AI training data**: Extract structured content from YouTube to create training scenarios or knowledge bases for voice agents.

The skill pattern (SKILL.md instructing Claude to run shell commands) is reusable for any CLI-tool-backed workflow you want to expose to Claude Code.
