---
name: high_quality_slides
description: |
  Research-first, narrative-driven 5-phase workflow that produces high-quality HTML slide presentations.
  Triggers: "create a presentation", "make slides", "build a slide deck", "generate a presentation about", "make a pitch deck"
---

# High-Quality Slides

A Claude Code skill that produces presentations worth sending — a research-first, narrative-driven 5-phase workflow inspired by Genspark AI Slides.

## When to use

- "Create a presentation about [topic]"
- "Make slides for my talk on [subject]"
- "Build a pitch deck for [product/idea]"
- "Generate a slide deck summarizing [content]"
- "Turn this research into a presentation"

## How to use

This skill follows a strict **5-phase workflow** to ensure every presentation is well-researched, narratively coherent, and visually polished.

### Phase 1: Research

Gather comprehensive information on the topic before writing a single slide.

1. Identify the core topic, audience, and presentation goal from the user's request.
2. Use available tools (web search, file reading, codebase exploration) to collect relevant facts, data points, quotes, and examples.
3. Organize findings into key themes and supporting evidence.
4. Save research notes in a structured format for reference.

### Phase 2: Narrative Architecture

Design the story arc and logical flow of the presentation.

1. Define the **opening hook** — a compelling question, statistic, or story.
2. Structure the **body** into 3-5 main sections, each with a clear point.
3. Plan the **conclusion** with a strong call-to-action or takeaway.
4. Create a slide-by-slide outline with titles and key messages.
5. Ensure smooth transitions between sections.

### Phase 3: Content Writing

Write concise, impactful content for each slide.

1. Follow the **one idea per slide** principle.
2. Use short bullet points (max 6 per slide, max 8 words each).
3. Write speaker notes with deeper context where appropriate.
4. Include data visualizations descriptions where numbers tell the story.
5. Add relevant quotes or case studies to support key points.

### Phase 4: Visual Design & HTML Generation

Produce a self-contained HTML slide deck with professional styling.

1. Generate a single `.html` file with all CSS and JS inline.
2. Use a clean, modern design system:
   - Consistent color palette (derive from topic or user preference)
   - Professional typography (system fonts for portability)
   - Generous whitespace and visual hierarchy
   - Slide dimensions optimized for 16:9 aspect ratio
3. Implement keyboard navigation (arrow keys, spacebar).
4. Add slide number indicators and progress bar.
5. Include a title slide, content slides, and a closing slide.
6. Use CSS animations for subtle slide transitions.
7. Support fullscreen mode (F key or button).

### Phase 5: Review & Polish

Audit the deck for quality, coherence, and correctness.

1. Verify all facts and data points from Phase 1 research.
2. Check narrative flow — does each slide lead naturally to the next?
3. Proofread all text for grammar, spelling, and clarity.
4. Test HTML rendering and navigation functionality.
5. Ensure the presentation can stand alone without a presenter.
6. Present the final file path to the user and offer refinements.

## Output Format

The skill produces a single self-contained HTML file (e.g., `slides.html`) that:
- Works in any modern browser with no dependencies
- Supports keyboard navigation (Left/Right arrows, Space, Escape)
- Has a responsive 16:9 layout
- Includes print-friendly styles
- Can be opened directly or served locally

## Tips for Best Results

- Provide a clear topic and target audience
- Mention the desired number of slides (default: 10-15)
- Specify any branding colors or style preferences
- Share source material or links for the research phase
- Indicate whether this is for a live talk, async reading, or a pitch

## References

- Source: [andyqiu847-ai/high-quality-slides](https://github.com/andyqiu847-ai/high-quality-slides) — Research-first, narrative-driven 5-phase workflow inspired by Genspark AI Slides
