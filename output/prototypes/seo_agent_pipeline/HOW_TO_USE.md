# How to Use — SEO Agent Pipeline

## Install

```bash
git clone https://github.com/loganriebel/seo_agent_pipeline.git
cd seo_agent_pipeline
pip install -r requirements.txt   # only pyyaml
```

## As a Claude Code Skill

This is a **Claude Code skill**. To install it:

1. Copy the `SKILL.md` file into your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/seo_agent_pipeline
   cp SKILL.md ~/.claude/skills/seo_agent_pipeline/SKILL.md
   ```

2. Copy `pipeline.py` into the same directory (or your project root):
   ```bash
   cp pipeline.py ~/.claude/skills/seo_agent_pipeline/
   ```

3. **Trigger phrases** that activate this skill in Claude Code:
   - "Run the SEO content pipeline for [topic]"
   - "Generate an SEO article from research to publish"
   - "Start keyword research and content creation pipeline"
   - "Create and deploy SEO content to the static site"
   - "Run the full content pipeline with approval gates"

## As a Standalone CLI

Run directly without Claude Code:

```bash
python3 pipeline.py "your target topic here"
```

Output lands in `./pipeline_output/<slug>/` with:
- `index.md` — publish-ready article with YAML frontmatter
- `pipeline_manifest.json` — config + metadata
- `stage_log.json` — what each stage produced

## First 60 Seconds

```bash
# 1. Run the demo
$ bash run.sh

# 2. See the output (takes ~1 second)
═══════════════════════════════════════════════════
  SEO Agent Pipeline
  Topic: ai-powered code review tools
═══════════════════════════════════════════════════

  Stage 1/10 │ Keyword Research
  Primary keyword: ai-powered code review tools
  Keywords found:
    - keyword: ai-powered code review tools | volume: 12100 | difficulty: 45
    - keyword: best ai-powered code review tools | volume: 6600 | difficulty: 38
    ...
  ✓ Identified 5 target keywords

  Stage 2/10 │ SERP Analysis
  ...

  [stages 3-9 run sequentially]

  Stage 10/10 │ Deployment
  Output directory: ./pipeline_output/ai-powered-code-review-tools
  Files written:
    - pipeline_output/ai-powered-code-review-tools/index.md
    - pipeline_output/ai-powered-code-review-tools/pipeline_manifest.json
    - pipeline_output/ai-powered-code-review-tools/stage_log.json
  ✓ Content deployed

# 3. Inspect the article
$ cat pipeline_output/ai-powered-code-review-tools/index.md
---
title: "Best Ai-Powered Code Review Tools in 2026: Expert Guide & Top Picks"
slug: ai-powered-code-review-tools
date: '2026-05-06'
keywords: [ai-powered code review tools, best ai-powered code review tools, ...]
schema: { "@type": "Article", ... }
---
# The Ultimate Guide to Ai-Powered Code Review Tools in 2026
...
```

## Configuration Options

Pass keyword arguments when calling programmatically:

```python
from pipeline import run_pipeline

run_pipeline(
    "ergonomic keyboards",
    target_word_count=2500,
    content_format="markdown",
    site_framework="astro",
    approval_mode="each_stage",  # pauses after each stage
)
```

| Parameter | Default | Options |
|-----------|---------|---------|
| `target_word_count` | 2000 | Any integer |
| `content_format` | `markdown` | `markdown`, `html` |
| `site_framework` | `hugo` | `hugo`, `astro`, `jekyll`, `eleventy` |
| `approval_mode` | `auto` | `auto`, `each_stage` |
