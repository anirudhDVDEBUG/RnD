"""Claude Writing Skills — full pipeline demo with mock data."""

from scoring import score_content
from publisher import publish

# --- Stage 1: Research (mock YouTube transcript) ---

MOCK_TRANSCRIPT = """
Today we're going to talk about building AI-powered content pipelines.
The key insight is that you can break writing into discrete stages.
First, research. Gather your sources, pull transcripts, read papers.
Second, draft. Get words on the page without worrying about quality.
Third, evaluate. Score your draft against a rubric.
Fourth, revise. Fix the weak spots identified by scoring.
Fifth, publish. Format, add metadata, and ship.
The most common mistake is trying to do all five at once.
Separation of concerns applies to writing just as much as code.
Let me show you how each stage works in practice.
When you research, focus on extracting themes, not copying text.
Pull out quotes that support your argument.
Note statistics and data points you can reference.
For scoring, I recommend four dimensions: clarity, structure, engagement, completeness.
Each one is independently measurable and improvable.
The rewrite step should target specific weaknesses, not rewrite everything.
And finally, publishing means clean markdown with proper frontmatter.
"""

MOCK_RESEARCH_NOTES = """# Research Notes: AI Content Pipelines

## Key Themes
1. **Stage separation** — Break writing into discrete, focused stages
2. **Rubric-based evaluation** — Score on clarity, structure, engagement, completeness
3. **Targeted revision** — Fix specific weaknesses rather than rewriting from scratch
4. **Automation-friendly** — Each stage can be handled by AI tooling
5. **Publishing standards** — Clean markdown with frontmatter and metadata

## Notable Quotes
- "Separation of concerns applies to writing just as much as code"
- "The most common mistake is trying to do all five at once"
- "Focus on extracting themes, not copying text"

## Facts & Data Points
- 5-stage pipeline: Research → Draft → Evaluate → Revise → Publish
- 4 scoring dimensions: clarity, structure, engagement, completeness
- Each dimension is independently measurable and improvable
"""

# --- Stage 2: Draft (simulated initial draft) ---

MOCK_DRAFT = """# How to Build an AI Content Pipeline

Writing long-form content is hard and takes forever. Most people just stare at a blank page. This article explains a better approach using AI tools.

## The Problem

Content creators struggle with writer's block. They try to research, write, edit, and publish all at once. This leads to burnout and inconsistent quality.

## The Solution: A 5-Stage Pipeline

You can break the writing process into five discrete stages:

- Research: Gather sources and extract key themes
- Draft: Get words on the page without judgment
- Score: Evaluate quality on multiple dimensions
- Rewrite: Target specific weaknesses
- Publish: Format and ship clean markdown

## How Scoring Works

Score your content on four dimensions: clarity, structure, engagement, and completeness. Each dimension gets a 1-10 rating. Focus your rewrites on the lowest-scoring areas.

## Getting Started

Install the Claude Writing Skills toolkit and start with the research stage. Feed it a YouTube video or topic and let it extract structured notes.
"""

# --- Stage 3: Rewrite (improved version after scoring) ---

MOCK_REWRITE = """# How to Build an AI Content Pipeline

Have you ever spent three hours writing a blog post, only to realize it's unfocused and flat? You're not alone — and there's a systematic fix.

## The Problem

Content creators burn out because they try to do everything at once: research, write, edit, format, publish. Each task requires a different mindset, and context-switching between them kills both quality and speed.

## The Solution: A 5-Stage Pipeline

What if you could break writing into discrete, automatable stages — just like a CI/CD pipeline for code?

- **Research**: Extract themes, quotes, and data from sources (including YouTube transcripts)
- **Draft**: Get words on the page without self-editing
- **Score**: Rate quality on clarity, structure, engagement, and completeness
- **Rewrite**: Target only the weakest sections for improvement
- **Publish**: Auto-generate frontmatter, TOC, and clean markdown

## How Scoring Works

Each dimension gets a 1-10 rating based on measurable signals:

- **Clarity** (sentence length, jargon density)
- **Structure** (headings, lists, paragraph breaks)
- **Engagement** (hooks, questions, reader address)
- **Completeness** (intro, body coverage, conclusion)

Focus your rewrites on the lowest-scoring areas — don't waste time polishing what already works.

## Getting Started

Install the toolkit, feed it a YouTube video URL, and watch it extract structured research notes in seconds. Then iterate through score → rewrite cycles until you hit your quality threshold.

In short, stop treating writing as a monolithic task. Pipeline it, score it, ship it.
"""


def run_pipeline():
    """Execute the full demo pipeline."""
    print("=" * 60)
    print("CLAUDE WRITING SKILLS — Pipeline Demo")
    print("=" * 60)

    # Stage 1: Research
    print("\n[1/4] RESEARCH")
    print("-" * 40)
    print(f"Source: YouTube transcript (mock, {len(MOCK_TRANSCRIPT.split())} words)")
    print("Extracted 5 key themes, 3 quotes, 3 data points")
    print("\nResearch notes preview:")
    for line in MOCK_RESEARCH_NOTES.split('\n')[1:8]:
        if line.strip():
            print(f"  {line}")

    # Stage 2: Score the initial draft
    print("\n[2/4] SCORE (initial draft)")
    print("-" * 40)
    scores = score_content(MOCK_DRAFT)
    print(f"  Clarity:      {scores['clarity']}/10")
    print(f"  Structure:    {scores['structure']}/10")
    print(f"  Engagement:   {scores['engagement']}/10")
    print(f"  Completeness: {scores['completeness']}/10")
    print(f"  OVERALL:      {scores['overall']}/10")
    if scores['feedback']:
        print("\n  Feedback:")
        for fb in scores['feedback']:
            print(f"    - {fb}")

    # Stage 3: Rewrite and re-score
    print("\n[3/4] REWRITE + RE-SCORE")
    print("-" * 40)
    new_scores = score_content(MOCK_REWRITE)
    print(f"  Clarity:      {scores['clarity']} -> {new_scores['clarity']}")
    print(f"  Structure:    {scores['structure']} -> {new_scores['structure']}")
    print(f"  Engagement:   {scores['engagement']} -> {new_scores['engagement']}")
    print(f"  Completeness: {scores['completeness']} -> {new_scores['completeness']}")
    print(f"  OVERALL:      {scores['overall']} -> {new_scores['overall']}")

    # Stage 4: Publish
    print("\n[4/4] PUBLISH")
    print("-" * 40)
    tags = ["ai-writing", "content-pipeline", "claude-skills", "productivity"]
    filepath = publish("How to Build an AI Content Pipeline", MOCK_REWRITE, tags)
    print(f"  Published to: {filepath}")
    print(f"  Tags: {', '.join(tags)}")
    print(f"  Frontmatter: title, date, tags, description")
    print(f"  Table of contents: auto-generated from headings")

    print("\n" + "=" * 60)
    print("DONE. Check output/published/ for the final article.")
    print("=" * 60)


if __name__ == '__main__':
    run_pipeline()
