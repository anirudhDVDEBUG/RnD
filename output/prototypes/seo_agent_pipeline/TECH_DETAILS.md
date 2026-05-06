# Technical Details — SEO Agent Pipeline

## What It Does

The SEO Agent Pipeline is a 10-stage sequential content pipeline that transforms a raw topic string into a publish-ready static-site article. Each stage produces structured output (keyword lists, competitor data, outlines, drafts, SEO metadata) that feeds into the next. The pipeline generates YAML frontmatter with JSON-LD schema markup, Open Graph tags, and optimized meta tags — everything a static site generator needs to publish an SEO-optimized page.

In production, each stage calls Claude (or another LLM) for intelligent content generation — keyword research pulls from real SEO APIs, SERP analysis scrapes actual search results, and content drafting produces original long-form articles. This demo uses realistic mock data to show the pipeline mechanics without requiring API keys.

## Architecture

```
pipeline.py          — Single-file pipeline: all 10 stages + runner
SKILL.md             — Claude Code skill definition (trigger phrases, docs)
run.sh               — Demo runner

Input:  topic string  →  PipelineConfig dataclass
Output: pipeline_output/<slug>/
          ├── index.md              (article + YAML frontmatter)
          ├── pipeline_manifest.json (config + metadata)
          └── stage_log.json        (per-stage audit trail)
```

### Data Flow

```
Topic → [1. Keywords] → [2. SERP] → [3. Strategy] → [4. Outline]
      → [5. Draft] → [6. SEO Opt] → [7. Media] → [8. Tech SEO]
      → [9. QA Review] → [10. Deploy] → index.md
```

Each stage receives the `PipelineConfig` and the previous stage's `StageResult`. Stage 10 (Deployment) receives all prior results to assemble the final article.

### Key Files

| File | Purpose |
|------|---------|
| `pipeline.py` | Core pipeline — 10 stage functions, `PipelineConfig` dataclass, `StageResult` dataclass, CLI entrypoint |
| `SKILL.md` | Claude Code skill metadata — name, description, trigger phrases |
| `run.sh` | Installs deps, runs demo, prints output preview |

### Dependencies

- **Python 3.8+**
- **PyYAML** — YAML frontmatter serialization for the output article
- No external APIs, no LLM calls in demo mode

### Where LLM Calls Would Go

In a production version, stages 1-9 would each call Claude via the Anthropic SDK:

- **Stage 1** (Keywords): Claude analyzes the topic + SEO tool data to pick target keywords
- **Stage 3** (Strategy): Claude defines angle and differentiator based on SERP gaps
- **Stage 5** (Drafting): Claude writes the full article following the outline
- **Stage 6** (SEO Opt): Claude optimizes title/meta for CTR while hitting keyword targets
- **Stage 9** (QA): Claude reviews the draft against a quality rubric

## Limitations

- **Mock data only** — This demo doesn't call real SEO APIs (Ahrefs, SEMrush) or LLMs. All keyword volumes, competitor data, and article content are simulated.
- **No actual SERP scraping** — Stage 2 uses hardcoded competitor data rather than live search results.
- **No real quality scoring** — Stage 9 reports fixed scores rather than running actual readability/grammar analysis.
- **Single-article scope** — No content calendar, topic clustering, or internal linking graph across multiple articles.
- **No CMS integration** — Outputs Markdown files to disk; doesn't push to WordPress, Ghost, or a headless CMS.
- **No image generation** — Media planning produces alt text and placement specs, but no actual images.

## Why It Matters

For teams building Claude-driven products:

- **Lead-gen / content marketing**: Automate the research-to-publish pipeline for SEO content at scale. A marketing team could run this for 50 topics/week with human review only at approval gates.
- **Agent factories**: The stage-based architecture with structured I/O between stages is a reusable pattern for any multi-step agent workflow — swap the 10 SEO stages for any domain-specific pipeline.
- **Skill composition**: Shows how Claude Code skills can orchestrate complex, multi-stage workflows with a single trigger phrase, turning "generate an SEO article about X" into a fully automated pipeline.
- **Approval gates**: The `each_stage` mode demonstrates human-in-the-loop patterns — critical for production content pipelines where brand voice and factual accuracy require human oversight.

## Source

[loganriebel/seo_agent_pipeline](https://github.com/loganriebel/seo_agent_pipeline)
