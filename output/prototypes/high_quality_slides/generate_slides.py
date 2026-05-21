#!/usr/bin/env python3
"""
High-Quality Slides Generator
Research-first, narrative-driven 5-phase workflow that produces
self-contained HTML slide presentations.

This demo generates a sample presentation to showcase the skill's output format.
"""

import argparse
import json
import html
import os
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# Phase 1 – Research (mock data for demo; real skill uses web search / files)
# ---------------------------------------------------------------------------

SAMPLE_TOPICS = {
    "ai-agents": {
        "title": "The Rise of AI Agents in 2026",
        "subtitle": "From Chatbots to Autonomous Workflows",
        "audience": "Technical leaders & product managers",
        "color_primary": "#6C5CE7",
        "color_secondary": "#A29BFE",
        "color_accent": "#00CEC9",
        "sections": [
            {
                "title": "What Changed?",
                "bullets": [
                    "LLMs gained tool-use & memory",
                    "MCP standardized integrations",
                    "Cost per token dropped 90% in 18 months",
                    "Enterprise trust crossed the adoption threshold",
                ],
                "speaker_notes": "The shift from chat-based AI to agentic AI happened faster than most predicted.",
            },
            {
                "title": "Anatomy of an AI Agent",
                "bullets": [
                    "Planner \u2192 breaks goals into steps",
                    "Executor \u2192 calls tools & APIs",
                    "Memory \u2192 persists context across sessions",
                    "Evaluator \u2192 checks output quality",
                ],
                "speaker_notes": "Think of agents as the orchestration layer on top of foundation models.",
            },
            {
                "title": "Real-World Impact",
                "bullets": [
                    "Customer support: 40% ticket deflection",
                    "Code review: 3x faster PR turnaround",
                    "Sales: automated lead qualification",
                    "Marketing: personalized content at scale",
                ],
                "speaker_notes": "These are conservative numbers from public case studies.",
            },
            {
                "title": "The Agent Stack",
                "bullets": [
                    "Foundation model (Claude, GPT, Gemini)",
                    "Skill / tool layer (MCP servers)",
                    "Orchestrator (Claude Code, LangGraph)",
                    "Human-in-the-loop guardrails",
                ],
                "speaker_notes": "The stack is stabilizing around these four layers.",
            },
            {
                "title": "Key Metrics to Watch",
                "bullets": [
                    "Task completion rate (aim > 85%)",
                    "Human escalation frequency",
                    "Cost per resolved task",
                    "Time-to-value for new agent skills",
                ],
                "speaker_notes": "Measurement is still immature \u2014 these four metrics give a solid baseline.",
            },
            {
                "title": "Risks & Guardrails",
                "bullets": [
                    "Hallucination in high-stakes domains",
                    "Prompt injection & adversarial inputs",
                    "Runaway costs from recursive loops",
                    "Regulatory uncertainty (EU AI Act, etc.)",
                ],
                "speaker_notes": "Every agent deployment needs a kill switch and cost ceiling.",
            },
            {
                "title": "What\u2019s Next (2026-2027)",
                "bullets": [
                    "Multi-agent collaboration protocols",
                    "On-device agents for privacy",
                    "Agent-to-agent marketplaces",
                    "Formal verification of agent behavior",
                ],
                "speaker_notes": "The next frontier is agents that can safely delegate to other agents.",
            },
        ],
    },
    "claude-skills": {
        "title": "Building Claude Code Skills",
        "subtitle": "Extend Claude with Domain-Specific Superpowers",
        "audience": "Developers & AI engineers",
        "color_primary": "#D4A574",
        "color_secondary": "#E8C9A0",
        "color_accent": "#2D3436",
        "sections": [
            {
                "title": "What Are Skills?",
                "bullets": [
                    "Markdown files that extend Claude Code",
                    "Triggered by natural language phrases",
                    "Live in ~/.claude/skills/<name>/",
                    "No API keys or servers required",
                ],
                "speaker_notes": "Skills are the simplest way to customize Claude Code for your workflow.",
            },
            {
                "title": "Skill Anatomy",
                "bullets": [
                    "YAML front-matter: name, description, triggers",
                    "Markdown body: instructions & examples",
                    "Optional: file templates, checklists",
                    "Versioned alongside your project",
                ],
                "speaker_notes": "A skill is just a well-structured prompt with metadata.",
            },
            {
                "title": "When to Build a Skill",
                "bullets": [
                    "Repeated multi-step workflows",
                    "Domain-specific quality standards",
                    "Team knowledge you want to codify",
                    "Processes that need consistent output",
                ],
                "speaker_notes": "If you find yourself writing the same prompt twice, make it a skill.",
            },
            {
                "title": "Best Practices",
                "bullets": [
                    "Be specific about output format",
                    "Include examples of good output",
                    "Define phases / checkpoints",
                    "Keep skills focused (single responsibility)",
                ],
                "speaker_notes": "The best skills read like a detailed checklist for a junior developer.",
            },
            {
                "title": "Distribution & Discovery",
                "bullets": [
                    "Share via Git repos",
                    "Community skill directories emerging",
                    "skills.sh \u2014 one-line install",
                    "Audit before installing third-party skills",
                ],
                "speaker_notes": "The skill ecosystem is growing fast \u2014 treat them like dependencies.",
            },
        ],
    },
}


# ---------------------------------------------------------------------------
# Phase 2-3 – Narrative Architecture & Content Writing (template-driven)
# ---------------------------------------------------------------------------

def build_slide_data(topic_key: str) -> dict:
    """Assemble the full slide deck data from research."""
    topic = SAMPLE_TOPICS[topic_key]
    slides = []

    # Title slide
    slides.append({
        "type": "title",
        "title": topic["title"],
        "subtitle": topic["subtitle"],
        "meta": f"Audience: {topic['audience']}  |  {datetime.now().strftime('%B %Y')}",
    })

    # Content slides
    for i, section in enumerate(topic["sections"], 1):
        slides.append({
            "type": "content",
            "number": i,
            "title": section["title"],
            "bullets": section["bullets"],
            "speaker_notes": section.get("speaker_notes", ""),
        })

    # Closing slide
    slides.append({
        "type": "closing",
        "title": "Thank You",
        "subtitle": "Questions & Discussion",
        "cta": "Try it: github.com/andyqiu847-ai/high-quality-slides",
    })

    return {
        "meta": topic,
        "slides": slides,
        "total": len(slides),
    }


# ---------------------------------------------------------------------------
# Phase 4 – Visual Design & HTML Generation
# ---------------------------------------------------------------------------

def generate_html(deck: dict) -> str:
    """Produce a self-contained HTML slide deck."""
    meta = deck["meta"]
    slides_html_parts = []

    for idx, slide in enumerate(deck["slides"]):
        if slide["type"] == "title":
            inner = f"""
            <div class="slide slide-title" data-index="{idx}">
                <div class="slide-inner">
                    <h1>{html.escape(slide['title'])}</h1>
                    <p class="subtitle">{html.escape(slide['subtitle'])}</p>
                    <p class="meta">{html.escape(slide['meta'])}</p>
                </div>
            </div>"""
        elif slide["type"] == "closing":
            inner = f"""
            <div class="slide slide-closing" data-index="{idx}">
                <div class="slide-inner">
                    <h1>{html.escape(slide['title'])}</h1>
                    <p class="subtitle">{html.escape(slide['subtitle'])}</p>
                    <p class="cta">{html.escape(slide['cta'])}</p>
                </div>
            </div>"""
        else:
            bullets = "\n".join(
                f'                        <li>{html.escape(b)}</li>'
                for b in slide["bullets"]
            )
            notes_attr = html.escape(slide.get("speaker_notes", ""), quote=True)
            inner = f"""
            <div class="slide slide-content" data-index="{idx}" data-notes="{notes_attr}">
                <div class="slide-inner">
                    <h2>{html.escape(slide['title'])}</h2>
                    <ul>
{bullets}
                    </ul>
                    <div class="slide-number">{slide['number']} / {deck['total'] - 2}</div>
                </div>
            </div>"""
        slides_html_parts.append(inner)

    slides_joined = "\n".join(slides_html_parts)
    primary = meta["color_primary"]
    secondary = meta["color_secondary"]
    accent = meta["color_accent"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(meta['title'])}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --primary: {primary};
    --secondary: {secondary};
    --accent: {accent};
    --bg: #0F0F1A;
    --text: #F0F0F5;
    --text-muted: #A0A0B0;
  }}

  html, body {{ height: 100%; overflow: hidden; background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}

  .deck {{ position: relative; width: 100vw; height: 100vh; }}

  .slide {{
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    opacity: 0; visibility: hidden;
    transition: opacity 0.45s ease, transform 0.45s ease;
    transform: translateX(40px);
    padding: 5vh 8vw;
  }}
  .slide.active {{
    opacity: 1; visibility: visible; transform: translateX(0);
  }}
  .slide.prev {{
    opacity: 0; transform: translateX(-40px);
  }}

  .slide-inner {{ max-width: 960px; width: 100%; }}

  /* Title slide */
  .slide-title h1 {{
    font-size: clamp(2rem, 5vw, 4rem); font-weight: 800;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.15; margin-bottom: 0.4em;
  }}
  .slide-title .subtitle {{
    font-size: clamp(1rem, 2.2vw, 1.6rem); color: var(--text-muted); margin-bottom: 1.5em;
  }}
  .slide-title .meta {{ font-size: 0.9rem; color: var(--text-muted); opacity: 0.7; }}

  /* Content slides */
  .slide-content h2 {{
    font-size: clamp(1.4rem, 3vw, 2.4rem); font-weight: 700;
    color: var(--primary); margin-bottom: 0.8em;
    border-left: 4px solid var(--accent); padding-left: 0.6em;
  }}
  .slide-content ul {{ list-style: none; padding: 0; }}
  .slide-content li {{
    font-size: clamp(1rem, 1.8vw, 1.35rem); padding: 0.55em 0 0.55em 1.4em;
    position: relative; color: var(--text); line-height: 1.4;
  }}
  .slide-content li::before {{
    content: ""; position: absolute; left: 0; top: 50%;
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--accent); transform: translateY(-50%);
  }}
  .slide-number {{
    position: absolute; bottom: 3vh; right: 4vw;
    font-size: 0.85rem; color: var(--text-muted); opacity: 0.6;
  }}

  /* Closing slide */
  .slide-closing {{ text-align: center; }}
  .slide-closing h1 {{
    font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800; color: var(--primary);
    margin-bottom: 0.3em;
  }}
  .slide-closing .subtitle {{ font-size: 1.4rem; color: var(--text-muted); margin-bottom: 1.5em; }}
  .slide-closing .cta {{
    display: inline-block; padding: 0.7em 1.6em; border-radius: 8px;
    background: var(--primary); color: #fff; font-size: 1rem; font-weight: 600;
  }}

  /* Progress bar */
  #progress {{
    position: fixed; top: 0; left: 0; height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    transition: width 0.4s ease; z-index: 100;
  }}

  /* Controls hint */
  #controls {{
    position: fixed; bottom: 1.5vh; left: 50%; transform: translateX(-50%);
    font-size: 0.75rem; color: var(--text-muted); opacity: 0.5;
    pointer-events: none;
  }}

  /* Fullscreen */
  .slide:-webkit-full-screen {{ background: var(--bg); }}
  .slide:fullscreen {{ background: var(--bg); }}

  /* Print */
  @media print {{
    .slide {{ position: relative; opacity: 1; visibility: visible;
      transform: none; page-break-after: always; height: 100vh; }}
    #progress, #controls {{ display: none; }}
  }}
</style>
</head>
<body>

<div id="progress" style="width: 0%;"></div>

<div class="deck" id="deck">
{slides_joined}
</div>

<div id="controls">\u2190 / \u2192 navigate &middot; F fullscreen &middot; Space next</div>

<script>
(function() {{
  const slides = document.querySelectorAll('.slide');
  const total = slides.length;
  let current = 0;

  function go(n) {{
    if (n < 0 || n >= total) return;
    slides[current].classList.remove('active');
    slides[current].classList.add('prev');
    current = n;
    slides.forEach((s, i) => {{
      s.classList.remove('active', 'prev');
      if (i === current) s.classList.add('active');
      else if (i < current) s.classList.add('prev');
    }});
    document.getElementById('progress').style.width =
      ((current / (total - 1)) * 100) + '%';
  }}

  go(0);

  document.addEventListener('keydown', function(e) {{
    if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); go(current + 1); }}
    else if (e.key === 'ArrowLeft') {{ e.preventDefault(); go(current - 1); }}
    else if (e.key === 'f' || e.key === 'F') {{
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }}
    else if (e.key === 'Escape' && document.fullscreenElement) document.exitFullscreen();
  }});

  // Touch support
  let touchStartX = 0;
  document.addEventListener('touchstart', e => {{ touchStartX = e.touches[0].clientX; }});
  document.addEventListener('touchend', e => {{
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) go(current + (dx < 0 ? 1 : -1));
  }});
}})();
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Phase 5 – Review & Polish (automated checks)
# ---------------------------------------------------------------------------

def review(deck: dict, html_content: str) -> list:
    """Run automated quality checks on the generated deck."""
    issues = []
    for slide in deck["slides"]:
        if slide["type"] == "content":
            if len(slide["bullets"]) > 6:
                issues.append(f"Slide '{slide['title']}': more than 6 bullets")
            for b in slide["bullets"]:
                if len(b.split()) > 12:
                    issues.append(f"Slide '{slide['title']}': bullet too long \u2014 '{b[:40]}...'")
    if "<script>" not in html_content:
        issues.append("Missing navigation script")
    if "keyboard" not in html_content.lower() and "keydown" not in html_content.lower():
        issues.append("Missing keyboard navigation")
    return issues


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate a high-quality HTML slide deck (demo)"
    )
    parser.add_argument(
        "topic",
        nargs="?",
        default="ai-agents",
        choices=list(SAMPLE_TOPICS.keys()),
        help="Topic to generate slides for (default: ai-agents)",
    )
    parser.add_argument(
        "-o", "--output",
        default="slides.html",
        help="Output HTML file path (default: slides.html)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Also emit slide data as JSON",
    )
    args = parser.parse_args()

    print(f"=== High-Quality Slides Generator ===\n")

    # Phase 1
    print("[Phase 1] Research: loading topic data for '{}'...".format(args.topic))
    topic_data = SAMPLE_TOPICS[args.topic]
    print(f"  \u2713 Title: {topic_data['title']}")
    print(f"  \u2713 Audience: {topic_data['audience']}")
    print(f"  \u2713 Sections: {len(topic_data['sections'])}\n")

    # Phase 2-3
    print("[Phase 2] Narrative Architecture: building slide outline...")
    print("[Phase 3] Content Writing: composing bullets & speaker notes...")
    deck = build_slide_data(args.topic)
    print(f"  \u2713 Total slides: {deck['total']} (1 title + {deck['total']-2} content + 1 closing)\n")

    # Phase 4
    print("[Phase 4] Visual Design & HTML Generation...")
    html_content = generate_html(deck)
    out_path = os.path.abspath(args.output)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    size_kb = len(html_content.encode("utf-8")) / 1024
    print(f"  \u2713 Generated {size_kb:.1f} KB HTML file\n")

    # Phase 5
    print("[Phase 5] Review & Polish...")
    issues = review(deck, html_content)
    if issues:
        for issue in issues:
            print(f"  \u26a0 {issue}")
    else:
        print("  \u2713 All quality checks passed")

    # Optional JSON export
    if args.json:
        json_path = out_path.replace(".html", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(deck, f, indent=2)
        print(f"  \u2713 JSON data: {json_path}")

    print(f"\n\u2705 Done! Open in your browser:")
    print(f"   file://{out_path}")
    print(f"\n   Controls: \u2190/\u2192 navigate | Space next | F fullscreen")


if __name__ == "__main__":
    main()
