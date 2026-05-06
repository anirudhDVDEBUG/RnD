"""
SEO Agent Pipeline — 10-stage content pipeline from keyword research to deployment.

Each stage produces structured output that feeds into the next stage.
In production, each stage calls Claude for intelligent content generation.
This demo uses realistic mock data to show the full pipeline flow.
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
import yaml

# ── Stage colours (ANSI) ─────────────────────────────────────────────
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


@dataclass
class PipelineConfig:
    topic: str
    target_word_count: int = 2000
    content_format: str = "markdown"
    site_framework: str = "hugo"
    content_dir: str = "./content/posts/"
    approval_mode: str = "auto"  # auto | each_stage


@dataclass
class StageResult:
    stage_num: int
    stage_name: str
    status: str = "pending"
    output: dict = field(default_factory=dict)


def slugify(text: str) -> str:
    return text.lower().replace(" ", "-").replace("'", "").replace('"', "")


def print_stage_header(num: int, name: str):
    bar = "━" * 60
    print(f"\n{CYAN}{bar}{RESET}")
    print(f"{BOLD}  Stage {num}/10 │ {name}{RESET}")
    print(f"{CYAN}{bar}{RESET}")


def print_kv(key: str, value, indent: int = 2):
    pad = " " * indent
    if isinstance(value, list):
        print(f"{pad}{DIM}{key}:{RESET}")
        for item in value:
            if isinstance(item, dict):
                parts = " | ".join(f"{k}: {v}" for k, v in item.items())
                print(f"{pad}  - {parts}")
            else:
                print(f"{pad}  - {item}")
    elif isinstance(value, dict):
        print(f"{pad}{DIM}{key}:{RESET}")
        for k, v in value.items():
            print(f"{pad}  {k}: {v}")
    else:
        print(f"{pad}{DIM}{key}:{RESET} {value}")


# ── Pipeline Stages ──────────────────────────────────────────────────

def stage_keyword_research(config: PipelineConfig) -> StageResult:
    print_stage_header(1, "Keyword Research")
    slug = slugify(config.topic)
    keywords = [
        {"keyword": config.topic, "volume": 12100, "difficulty": 45, "intent": "informational"},
        {"keyword": f"best {config.topic}", "volume": 6600, "difficulty": 38, "intent": "commercial"},
        {"keyword": f"{config.topic} guide", "volume": 3200, "difficulty": 32, "intent": "informational"},
        {"keyword": f"{config.topic} comparison", "volume": 2400, "difficulty": 41, "intent": "commercial"},
        {"keyword": f"how to choose {config.topic}", "volume": 1900, "difficulty": 28, "intent": "informational"},
    ]
    result = StageResult(1, "Keyword Research", "complete", {
        "primary_keyword": config.topic,
        "slug": slug,
        "keywords": keywords,
    })
    print_kv("Primary keyword", config.topic)
    print_kv("Keywords found", keywords)
    print(f"  {GREEN}✓ Identified 5 target keywords{RESET}")
    return result


def stage_serp_analysis(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(2, "SERP Analysis")
    competitors = [
        {"rank": 1, "url": "techreviewer.com", "word_count": 2800, "headings": 12, "images": 8},
        {"rank": 2, "url": "gadgetguide.io", "word_count": 2200, "headings": 9, "images": 5},
        {"rank": 3, "url": "digitaltrends.com", "word_count": 3100, "headings": 14, "images": 11},
        {"rank": 4, "url": "wirecutter.com", "word_count": 4200, "headings": 18, "images": 15},
        {"rank": 5, "url": "pcmag.com", "word_count": 1800, "headings": 7, "images": 4},
    ]
    avg_words = sum(c["word_count"] for c in competitors) // len(competitors)
    result = StageResult(2, "SERP Analysis", "complete", {
        "competitors": competitors,
        "avg_word_count": avg_words,
        "avg_headings": sum(c["headings"] for c in competitors) // len(competitors),
        "recommended_word_count": max(avg_words + 300, config.target_word_count),
        "content_gap": "Lack of hands-on comparison tables and decision frameworks",
    })
    print_kv("Top competitors analyzed", len(competitors))
    print_kv("Average word count", avg_words)
    print_kv("Content gap identified", result.output["content_gap"])
    print(f"  {GREEN}✓ SERP analysis complete{RESET}")
    return result


def stage_content_strategy(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(3, "Content Strategy")
    strategy = {
        "angle": f"Practical buyer's guide with hands-on testing data for {config.topic}",
        "target_audience": "Tech-savvy professionals researching before purchase",
        "unique_value": "Side-by-side comparison matrix with real-world test results",
        "tone": "Expert but accessible — data-driven without jargon",
        "differentiator": "Interactive comparison table + decision flowchart",
    }
    result = StageResult(3, "Content Strategy", "complete", strategy)
    for k, v in strategy.items():
        print_kv(k.replace("_", " ").title(), v)
    print(f"  {GREEN}✓ Content strategy defined{RESET}")
    return result


def stage_outline_creation(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(4, "Outline Creation")
    outline = [
        {"heading": "Introduction", "level": "H2", "target_words": 200, "points": ["Hook with key statistic", "What this guide covers"]},
        {"heading": f"What to Look for in {config.topic.title()}", "level": "H2", "target_words": 350, "points": ["Key features", "Common pitfalls"]},
        {"heading": "Top Picks Compared", "level": "H2", "target_words": 600, "points": ["Comparison table", "Individual reviews", "Pros/cons"]},
        {"heading": "How to Choose", "level": "H2", "target_words": 300, "points": ["Decision framework", "Use-case matching"]},
        {"heading": "Setup and Getting Started", "level": "H2", "target_words": 250, "points": ["Quick start guide", "Pro tips"]},
        {"heading": "FAQ", "level": "H2", "target_words": 200, "points": ["Top 5 questions from SERP PAA"]},
        {"heading": "Conclusion", "level": "H2", "target_words": 100, "points": ["Summary", "Final recommendation"]},
    ]
    total = sum(s["target_words"] for s in outline)
    result = StageResult(4, "Outline Creation", "complete", {
        "sections": outline,
        "total_target_words": total,
    })
    for s in outline:
        print(f"  {s['level']} {s['heading']} ({s['target_words']} words)")
    print(f"\n  Total target: {total} words")
    print(f"  {GREEN}✓ Outline with {len(outline)} sections created{RESET}")
    return result


def stage_content_drafting(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(5, "Content Drafting")
    topic_title = config.topic.title()
    draft = f"""# The Ultimate Guide to {topic_title} in 2026

Finding the right {config.topic} can transform your workflow. After testing 15+ options
over 3 months, here's what actually matters — and which ones deliver.

## What to Look for in {topic_title}

The market is crowded, but the differences that matter come down to three areas:
build quality, software ecosystem, and long-term value. Here's how to evaluate each.

**Key features to prioritize:**
- Compatibility with your existing stack
- Active development and community support
- Performance benchmarks under real workloads
- Total cost of ownership over 2+ years

## Top Picks Compared

| Option | Rating | Best For | Price |
|--------|--------|----------|-------|
| Option A | 9.2/10 | Power users | $$$ |
| Option B | 8.8/10 | Best value | $$ |
| Option C | 8.5/10 | Beginners | $ |
| Option D | 9.0/10 | Enterprise | $$$$ |

### Option A — Best Overall
The clear winner for most users. Excellent build quality and a mature ecosystem.

### Option B — Best Value
80% of the performance at 50% of the price. Hard to beat for budget-conscious buyers.

## How to Choose

Start with your primary use case. If you need X, go with Option A. If budget matters
most, Option B delivers surprisingly well. Enterprise teams should evaluate Option D
for its management features.

## Setup and Getting Started

1. Unbox and inspect for damage
2. Download the companion app
3. Run the initial configuration wizard
4. Customize settings for your workflow

**Pro tip:** Spend 10 minutes on the advanced settings — the defaults leave performance
on the table.

## Frequently Asked Questions

**Q: Is {config.topic} worth the investment?**
A: For professionals who use it daily, absolutely. The productivity gains pay for
themselves within 2-3 months.

**Q: How long does {config.topic} typically last?**
A: With proper care, expect 3-5 years of reliable use from any of our top picks.

**Q: Can I try before buying?**
A: Options A and B both offer 30-day return policies. Option D has a free trial tier.

## Conclusion

{topic_title} has never been better. Our top pick (Option A) leads the pack, but
Option B offers incredible value. Whatever you choose, the key is matching the tool
to your specific workflow needs.
"""
    word_count = len(draft.split())
    result = StageResult(5, "Content Drafting", "complete", {
        "draft_word_count": word_count,
        "sections_written": 7,
        "draft_preview": draft[:200] + "...",
        "full_draft": draft,
    })
    print_kv("Words written", word_count)
    print_kv("Sections completed", 7)
    print(f"  {DIM}Preview: {draft[:120].strip()}...{RESET}")
    print(f"  {GREEN}✓ Full draft complete{RESET}")
    return result


def stage_seo_optimization(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(6, "SEO Optimization")
    topic_title = config.topic.title()
    slug = slugify(config.topic)
    seo = {
        "title_tag": f"Best {topic_title} in 2026: Expert Guide & Top Picks",
        "meta_description": f"Compare the top {config.topic} with hands-on test results. Our expert guide covers features, pricing, and which option fits your needs.",
        "url_slug": slug,
        "keyword_density": "1.8% (target: 1-2%)",
        "readability_score": "Grade 8 (Flesch-Kincaid)",
        "internal_links": [
            f"/blog/how-to-use-{slug}/",
            f"/blog/{slug}-vs-alternatives/",
            f"/reviews/{slug}/",
        ],
    }
    result = StageResult(6, "SEO Optimization", "complete", seo)
    for k, v in seo.items():
        print_kv(k.replace("_", " ").title(), v)
    print(f"  {GREEN}✓ On-page SEO optimized{RESET}")
    return result


def stage_media_planning(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(7, "Media Planning")
    media = [
        {"type": "hero_image", "placement": "Above fold", "alt": f"Top {config.topic} lined up for comparison testing"},
        {"type": "comparison_table", "placement": "Section 3", "alt": f"Side-by-side feature comparison of best {config.topic}"},
        {"type": "infographic", "placement": "Section 4", "alt": f"Decision flowchart for choosing the right {config.topic}"},
        {"type": "product_photo", "placement": "Each review", "alt": f"Close-up of [product name] showing build quality"},
        {"type": "video_embed", "placement": "Introduction", "alt": f"2-minute video overview of our {config.topic} testing process"},
    ]
    result = StageResult(7, "Media Planning", "complete", {"media_items": media})
    print_kv("Media items planned", media)
    print(f"  {GREEN}✓ {len(media)} media placements defined{RESET}")
    return result


def stage_technical_seo(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(8, "Technical SEO")
    slug = slugify(config.topic)
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"Best {config.topic.title()} in 2026: Expert Guide & Top Picks",
        "author": {"@type": "Organization", "name": "TechReview"},
        "datePublished": "2026-05-06",
        "image": f"https://example.com/images/{slug}-hero.jpg",
    }
    og_tags = {
        "og:title": f"Best {config.topic.title()} in 2026",
        "og:description": f"Expert comparison of top {config.topic} with test data.",
        "og:type": "article",
        "og:image": f"https://example.com/images/{slug}-og.jpg",
    }
    result = StageResult(8, "Technical SEO", "complete", {
        "schema_json_ld": schema,
        "open_graph": og_tags,
        "canonical_url": f"https://example.com/blog/{slug}/",
    })
    print_kv("JSON-LD Schema", json.dumps(schema, indent=2)[:200] + "...")
    print_kv("Open Graph tags", og_tags)
    print_kv("Canonical URL", result.output["canonical_url"])
    print(f"  {GREEN}✓ Structured data generated{RESET}")
    return result


def stage_quality_review(config: PipelineConfig, prev: StageResult) -> StageResult:
    print_stage_header(9, "Quality Review")
    checks = {
        "grammar_score": "98/100 (0 errors, 2 suggestions)",
        "seo_score": "92/100",
        "readability": "Grade 8 — accessible to general audience",
        "keyword_coverage": "5/5 target keywords present",
        "meta_tags": "Title (58 chars ✓), Description (155 chars ✓)",
        "schema_valid": True,
        "mobile_preview": "Passes — responsive layout verified",
        "link_check": "3 internal links valid, 0 broken",
    }
    result = StageResult(9, "Quality Review", "complete", checks)
    for k, v in checks.items():
        status = "✓" if v is not False else "✗"
        print_kv(k.replace("_", " ").title(), f"{v}")
    print(f"  {GREEN}✓ All quality checks passed{RESET}")
    return result


def stage_deployment(config: PipelineConfig, prev: StageResult, all_results: list) -> StageResult:
    print_stage_header(10, "Deployment")
    slug = slugify(config.topic)
    output_dir = Path(f"./pipeline_output/{slug}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Gather data from previous stages
    seo_data = all_results[5].output  # stage 6
    schema_data = all_results[7].output  # stage 8
    draft = all_results[4].output.get("full_draft", "# Draft content")

    # Build frontmatter
    frontmatter = {
        "title": seo_data.get("title_tag", config.topic.title()),
        "slug": slug,
        "date": "2026-05-06",
        "description": seo_data.get("meta_description", ""),
        "keywords": [kw["keyword"] for kw in all_results[0].output.get("keywords", [])],
        "schema": schema_data.get("schema_json_ld", {}),
        "open_graph": schema_data.get("open_graph", {}),
        "draft": False,
    }

    # Write the final article
    article_path = output_dir / "index.md"
    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    article_content = f"---\n{frontmatter_yaml}---\n\n{draft}"
    article_path.write_text(article_content)

    # Write pipeline manifest
    manifest = {
        "topic": config.topic,
        "slug": slug,
        "stages_completed": 10,
        "output_file": str(article_path),
        "config": asdict(config),
    }
    manifest_path = output_dir / "pipeline_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    # Write stage outputs log
    stage_log = []
    for r in all_results:
        safe_output = {k: v for k, v in r.output.items() if k != "full_draft"}
        stage_log.append({"stage": r.stage_num, "name": r.stage_name, "status": r.status, "output_keys": list(r.output.keys())})
    log_path = output_dir / "stage_log.json"
    log_path.write_text(json.dumps(stage_log, indent=2))

    result = StageResult(10, "Deployment", "complete", {
        "output_dir": str(output_dir),
        "files_written": [str(article_path), str(manifest_path), str(log_path)],
        "article_word_count": len(draft.split()),
    })

    print_kv("Output directory", str(output_dir))
    print_kv("Files written", result.output["files_written"])
    print_kv("Article word count", result.output["article_word_count"])
    print(f"  {GREEN}✓ Content deployed to {article_path}{RESET}")
    return result


# ── Main Pipeline Runner ─────────────────────────────────────────────

def run_pipeline(topic: str, **kwargs):
    config = PipelineConfig(topic=topic, **kwargs)
    slug = slugify(topic)

    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"{BOLD}  SEO Agent Pipeline{RESET}")
    print(f"{BOLD}  Topic: {topic}{RESET}")
    print(f"{BOLD}{'═' * 60}{RESET}")
    print(f"  Framework: {config.site_framework} | Format: {config.content_format}")
    print(f"  Target words: {config.target_word_count} | Mode: {config.approval_mode}")

    stages = [
        ("Keyword Research", stage_keyword_research),
        ("SERP Analysis", stage_serp_analysis),
        ("Content Strategy", stage_content_strategy),
        ("Outline Creation", stage_outline_creation),
        ("Content Drafting", stage_content_drafting),
        ("SEO Optimization", stage_seo_optimization),
        ("Media Planning", stage_media_planning),
        ("Technical SEO", stage_technical_seo),
        ("Quality Review", stage_quality_review),
        ("Deployment", None),  # handled specially
    ]

    results = []
    for i, (name, func) in enumerate(stages):
        if i == 0:
            result = func(config)
        elif i == 9:
            result = stage_deployment(config, results[-1], results)
        else:
            result = func(config, results[-1])
        results.append(result)

        if config.approval_mode == "each_stage" and i < 9:
            print(f"\n  {YELLOW}⏸  Approval gate — review stage {i+1} output before continuing{RESET}")

    # Final summary
    output_dir = f"./pipeline_output/{slug}"
    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"{GREEN}{BOLD}  ✓ Pipeline Complete — All 10 stages finished{RESET}")
    print(f"{BOLD}{'═' * 60}{RESET}")
    print(f"  Output: {output_dir}/")
    print(f"  Article: {output_dir}/index.md")
    print(f"  Manifest: {output_dir}/pipeline_manifest.json")
    print(f"  Stage log: {output_dir}/stage_log.json\n")

    return results


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "ai-powered code review tools"
    run_pipeline(topic)
