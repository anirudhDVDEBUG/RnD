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

1. **Keyword Research** — Identify target keywords, search volume, difficulty, and intent using available SEO data sources.
2. **SERP Analysis** — Analyze top-ranking pages for target keywords: content structure, word count, headings, media usage.
3. **Content Strategy** — Define article angle, target audience, unique value proposition, and content outline.
4. **Outline Creation** — Build a detailed content outline with H2/H3 structure, key points per section, and target word counts.
5. **Content Drafting** — Write the full article following the outline, incorporating target keywords naturally.
6. **SEO Optimization** — Optimize title tag, meta description, URL slug, internal links, keyword density, and readability.
7. **Media Planning** — Identify image/video opportunities, write alt text, and plan visual content placement.
8. **Technical SEO** — Generate schema markup (JSON-LD), Open Graph tags, canonical URLs, and structured data.
9. **Quality Review** — Run final checks: grammar, factual accuracy, SEO score, readability score, and compliance.
10. **Deployment** — Format as static site content (Markdown/HTML with frontmatter), commit, and deploy.

### Running the Pipeline

1. **Initialize**: Provide a target topic or keyword seed.
   ```
   Topic: "best ergonomic keyboards 2026"
   Target site: ./content/blog/
   ```

2. **Execute stages sequentially**: Each stage writes output to a working directory (e.g., `./pipeline_output/<slug>/`).

3. **Approval gates**: After each stage completes, review the output. Approve to continue or request revisions before proceeding.

4. **Final output**: A publish-ready static site page with:
   - Markdown/HTML content with YAML frontmatter
   - Optimized meta tags and structured data
   - Image placeholders with alt text
   - Internal linking suggestions

### Configuration

Set pipeline parameters in your project:
- `target_word_count`: Target article length (default: 1500-2500)
- `content_format`: Output format — `markdown` or `html` (default: markdown)
- `site_framework`: Static site generator — `hugo`, `astro`, `jekyll`, `eleventy`
- `approval_mode`: `each_stage` (default) or `batch` (approve groups of stages)

### Example Usage

```
/seo_agent_pipeline
Topic: "AI-powered code review tools"
Site framework: hugo
Content directory: ./content/posts/
```

The pipeline will create `./pipeline_output/ai-powered-code-review-tools/` with stage outputs and a final deployable article.

## References

- Source: [loganriebel/seo_agent_pipeline](https://github.com/loganriebel/seo_agent_pipeline) — 10-stage SEO content pipeline built using Claude Code skills
- Architecture: Research → Deploy with human approval gates after each step
- Stack: Python, Claude Code skills, static site generators
