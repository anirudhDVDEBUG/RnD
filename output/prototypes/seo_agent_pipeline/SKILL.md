---
name: seo_agent_pipeline
description: |
  10-stage SEO content pipeline that takes a topic from research to deployment on a static site.
  Triggers: SEO content pipeline, generate SEO article, keyword research to publish, content pipeline with approval gates, static site SEO workflow
---

# SEO Agent Pipeline

A 10-stage SEO content pipeline built with Claude Code skills. Manages the full workflow from keyword research to deployment on a static site, with human approval gates after each stage.

## When to use

- "Run the SEO content pipeline for [topic]"
- "Generate an SEO-optimized article from research to publish"
- "Start keyword research and content creation pipeline"
- "Create and deploy SEO content to the static site"
- "Run the full content pipeline with approval gates"

## How to use

This skill orchestrates a 10-stage pipeline. Each stage produces output that feeds the next, with a human approval gate between stages.

### Pipeline Stages

1. **Keyword Research** — Identify target keywords, search volume, difficulty, and intent.
2. **SERP Analysis** — Analyze top-ranking pages: content structure, word count, headings, media usage.
3. **Content Strategy** — Define article angle, target audience, unique value proposition.
4. **Outline Creation** — Build detailed content outline with H2/H3 structure and target word counts.
5. **Content Drafting** — Write the full article following the outline.
6. **SEO Optimization** — Optimize title tag, meta description, URL slug, keyword density.
7. **Media Planning** — Identify image/video opportunities, write alt text.
8. **Technical SEO** — Generate schema markup (JSON-LD), Open Graph tags, canonical URLs.
9. **Quality Review** — Run final checks: grammar, SEO score, readability, compliance.
10. **Deployment** — Format as static site content with frontmatter, commit, and deploy.

### Running the Pipeline

Provide a target topic or keyword seed:

```
/seo_agent_pipeline
Topic: "best ergonomic keyboards 2026"
Site framework: hugo
Content directory: ./content/posts/
```

### Configuration

- `target_word_count`: Target article length (default: 2000)
- `content_format`: `markdown` or `html` (default: markdown)
- `site_framework`: `hugo`, `astro`, `jekyll`, `eleventy`
- `approval_mode`: `each_stage` or `auto`
