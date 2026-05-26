# How to Use — Claude Writing Skills

## Install

```bash
# Clone the skill source
git clone https://github.com/xiaomoBoy/claude-writing-skills.git

# Install Python dependency (for YouTube transcript extraction)
pip install yt-dlp
```

## Deploy as a Claude Code Skill

Copy the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/claude_writing_skills
cp claude-writing-skills/SKILL.md ~/.claude/skills/claude_writing_skills/SKILL.md
```

### Trigger Phrases

Once installed, these phrases activate the skill in Claude Code:

| Phrase | Action |
|--------|--------|
| "research a topic" | Gather notes from web/YouTube |
| "score my article" | Rate draft on clarity/structure/engagement |
| "rewrite this draft" | Improve flagged sections |
| "publish content" | Export as clean markdown with frontmatter |
| "long-form writing" | General pipeline guidance |
| "YouTube transcript research" | Extract + summarize a video |
| "content pipeline" | Full end-to-end workflow |

## First 60 Seconds

### 1. Research a YouTube video

```
You: "Research this YouTube video for a blog post: https://youtube.com/watch?v=example"

Claude: Extracting transcript via yt-dlp...
        Found 5 key themes:
        1. Theme A — "notable quote here"
        2. Theme B — supporting data point
        ...
        Research notes saved to research_notes.md
```

### 2. Score a draft

```
You: "Score my article" (with draft.md open or pasted)

Claude: Content Quality Score: 6.2 / 10
        - Clarity:     7/10
        - Structure:   8/10
        - Engagement:  4/10  ← weak intro, no hook
        - Completeness: 6/10 ← missing conclusion
        Suggested fixes: [list]
```

### 3. Rewrite weak sections

```
You: "Rewrite the intro to be more engaging"

Claude: [Rewrites intro with a hook and thesis statement]
        Re-scoring... Engagement improved from 4 → 7.
```

### 4. Publish

```
You: "Publish this article"

Claude: Generated frontmatter (title, tags, date).
        Added table of contents.
        Saved to output/published/article.md
```

## Running the Demo Locally

```bash
bash run.sh
```

This runs the full pipeline with mock data (no API keys needed) and produces visible output in `output/published/`.
