# Technical Details — Claude Writing Skills

## What It Does

Claude Writing Skills is a SKILL.md-based toolkit that extends Claude Code with a structured long-form writing pipeline. It provides four discrete capabilities — research, score, rewrite, publish — that Claude invokes based on natural-language trigger phrases. The research stage can pull YouTube transcripts via `yt-dlp`, while scoring uses a rubric-based evaluation (clarity, structure, engagement, completeness) to guide iterative improvement.

The skill itself contains no runtime code — it's a prompt engineering artifact (SKILL.md) that shapes Claude's behavior. The demo in this repo simulates the pipeline in Python to show the data flow and output format.

## Architecture

```
User prompt
    │
    ▼
SKILL.md (loaded by Claude Code when trigger phrase matches)
    │
    ├─ Research ──► yt-dlp subprocess (YouTube) or web search
    │               └─► Structured notes (themes, quotes, facts)
    │
    ├─ Score ─────► Rubric evaluation (4 dimensions, 1-10 each)
    │               └─► Per-section feedback + overall score
    │
    ├─ Rewrite ──► Targeted section improvement
    │               └─► Preserves voice, targets flagged issues
    │
    └─ Publish ──► Markdown formatter
                    └─► Frontmatter + TOC + clean output file
```

### Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The actual skill definition loaded by Claude Code |
| `pipeline.py` | Demo implementation of all 4 stages |
| `scoring.py` | Content quality rubric and scoring logic |
| `publisher.py` | Markdown frontmatter generation + TOC builder |
| `run.sh` | End-to-end demo runner |

### Dependencies

- **yt-dlp** — YouTube transcript/subtitle extraction (spawned as subprocess)
- **Python 3.x** — Pipeline logic
- No external API keys required for the skill itself (Claude provides the LLM)

## Limitations

- **No actual LLM calls in demo** — the demo uses heuristic scoring and mock rewrites; in production, Claude handles all generation.
- **YouTube only** — research currently supports YouTube transcripts via yt-dlp; no general web scraping built in (relies on Claude's web search or MCP tools for other sources).
- **English-centric** — scoring rubric and rewrite prompts are tuned for English prose.
- **No version tracking** — doesn't persist draft history or score progression across sessions.
- **Skill, not agent** — it guides Claude's behavior but doesn't orchestrate multi-step workflows autonomously; the user drives each stage.

## Why It Matters

For teams building Claude-driven products:

- **Content marketing / lead-gen**: Automates the research-to-publish pipeline for SEO blog posts, reducing time-to-publish from hours to minutes.
- **Agent factories**: Demonstrates the SKILL.md pattern — a zero-code way to add domain expertise to Claude Code agents without building MCP servers.
- **Quality gates**: The scoring rubric pattern is reusable for any content QA workflow (ad copy, email sequences, documentation).
- **YouTube-to-content**: The yt-dlp integration pattern shows how skills can shell out to CLI tools, useful for any media-to-text pipeline (podcasts, webinars → blog posts).
