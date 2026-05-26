---
name: Claude Writing Skills
description: |
  A toolkit for long-form content creators: research topics (including YouTube transcripts via yt-dlp), score content quality, rewrite and improve drafts, and publish polished markdown.
  Triggers: "research a topic", "score my article", "rewrite this draft", "publish content", "long-form writing", "content pipeline", "YouTube transcript research"
---

# Claude Writing Skills

A comprehensive toolkit of Claude Code skills for long-form content creators. Covers the full writing pipeline: research, score, rewrite, and publish.

## When to use

- "Research this topic and summarize key points for an article"
- "Score my draft and suggest improvements"
- "Rewrite this section to be more engaging and polished"
- "Help me publish this article as clean markdown"
- "Pull a YouTube transcript and turn it into a blog post"

## How to use

### 1. Research
Gather source material for long-form content:
- Provide a topic, URL, or YouTube video link to research
- The skill uses `yt-dlp` to extract YouTube transcripts when a video URL is given
- Outputs structured research notes in markdown with key themes, quotes, and facts
- Can integrate with NotebookLM-style workflows for deep research synthesis

```bash
# Ensure yt-dlp is installed for YouTube transcript extraction
pip install yt-dlp
```

### 2. Score
Evaluate content quality before publishing:
- Analyzes drafts for clarity, structure, engagement, and completeness
- Returns a numerical score with detailed feedback per dimension
- Highlights weak sections and suggests specific improvements
- Use iteratively to track quality improvements across rewrites

### 3. Rewrite
Improve and polish draft content:
- Rewrites sections or full articles for better flow, tone, and readability
- Preserves the author's voice while enhancing clarity
- Supports style targets (e.g., conversational, formal, technical)
- Can target specific issues flagged by the scoring step

### 4. Publish
Prepare final content for distribution:
- Formats content as clean, well-structured markdown
- Generates frontmatter metadata (title, description, tags, date)
- Creates table of contents for long-form pieces
- Outputs publish-ready files to a specified directory

### Typical Workflow

1. **Research**: `/user:claude_writing_skills` → research a topic or YouTube video
2. **Draft**: Write an initial draft based on research notes
3. **Score**: Evaluate the draft quality and identify weak spots
4. **Rewrite**: Improve flagged sections iteratively
5. **Publish**: Format and export the final article

### Dependencies

- Python 3.x
- `yt-dlp` (for YouTube transcript extraction)
- Markdown-compatible output environment

## References

- Source: [xiaomoBoy/claude-writing-skills](https://github.com/xiaomoBoy/claude-writing-skills)
- Topics: ai-writing, claude-code, claude-skills, content-creation, markdown, notebooklm, publishing, writing, yt-dlp
