# SEO Agent Pipeline

**10-stage SEO content pipeline that takes any topic from keyword research to a deployed static-site article — fully automated, with optional human approval gates between stages.** Built as a Claude Code skill so you can trigger it with natural language inside your editor.

```
$ bash run.sh
  ✓ Pipeline Complete — All 10 stages finished
  Output: ./pipeline_output/ai-powered-code-review-tools/
  Article: index.md (450+ words, YAML frontmatter, JSON-LD schema, OG tags)
```

**One command produces:** keyword research, SERP competitor analysis, content strategy, structured outline, full draft, on-page SEO optimization, media plan, technical SEO markup, quality review, and a publish-ready Markdown file with frontmatter for Hugo/Astro/Jekyll.

## Quick Start

```bash
bash run.sh
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, why it matters

## Source

[loganriebel/seo_agent_pipeline](https://github.com/loganriebel/seo_agent_pipeline) — 10-stage SEO content pipeline built using Claude Code skills
