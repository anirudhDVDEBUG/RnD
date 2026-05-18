#!/usr/bin/env python3
"""
HTML Slide Generator — standalone demo.

Generates a self-contained HTML slide deck from structured data.
This demonstrates the same output that the Claude Code skill produces,
but driven by a Python script with mock content instead of Claude.
"""

import html
import os
from pathlib import Path


def generate_slide_html(title: str, slides: list[dict], theme: dict | None = None) -> str:
    """Generate a complete HTML slide deck.

    Args:
        title: Presentation title
        slides: List of dicts with keys: type, heading, content
                type: 'title' | 'content' | 'quote' | 'code' | 'two-column' | 'cta'
                heading: slide heading text
                content: varies by type (str, list, or dict)
        theme: Optional dict with bg, text, accent colors
    """
    if theme is None:
        theme = {"bg": "#0f172a", "text": "#f8fafc", "accent": "#3b82f6"}

    slides_html = []
    for i, slide in enumerate(slides):
        active = ' active' if i == 0 else ''
        slide_type = slide.get("type", "content")
        heading = html.escape(slide.get("heading", ""))

        if slide_type == "title":
            subtitle = html.escape(slide.get("content", ""))
            inner = f'<h1>{heading}</h1>\n        <p style="opacity:0.7;font-size:clamp(1rem,2.5vw,1.75rem)">{subtitle}</p>'

        elif slide_type == "content":
            content = slide.get("content", [])
            if isinstance(content, list):
                items = "\n          ".join(f"<li>{html.escape(item)}</li>" for item in content)
                inner = f'<h2>{heading}</h2>\n        <ul>\n          {items}\n        </ul>'
            else:
                inner = f'<h2>{heading}</h2>\n        <p>{html.escape(str(content))}</p>'

        elif slide_type == "quote":
            quote_text = html.escape(slide.get("content", ""))
            author = html.escape(slide.get("author", ""))
            inner = (
                f'<blockquote style="font-size:clamp(1.25rem,3vw,2rem);font-style:italic;'
                f'border-left:4px solid {theme["accent"]};padding-left:1.5rem;max-width:70%">'
                f'"{quote_text}"</blockquote>\n'
                f'        <p style="margin-top:1rem;opacity:0.7">— {author}</p>'
            )

        elif slide_type == "code":
            code = slide.get("content", "")
            inner = (
                f'<h2>{heading}</h2>\n'
                f'        <pre style="background:#1e293b;padding:2rem;border-radius:0.5rem;'
                f'overflow-x:auto;max-width:80%;font-size:clamp(0.75rem,1.5vw,1.1rem);'
                f'text-align:left"><code>{html.escape(code)}</code></pre>'
            )

        elif slide_type == "cta":
            content = html.escape(slide.get("content", ""))
            inner = (
                f'<h2>{heading}</h2>\n'
                f'        <p style="font-size:clamp(1rem,2vw,1.5rem);opacity:0.8;margin-top:1rem">{content}</p>'
            )

        else:
            inner = f'<h2>{heading}</h2>'

        slides_html.append(
            f'    <div class="slide{active}">\n        {inner}\n      </div>'
        )

    all_slides = "\n      ".join(slides_html)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; overflow: hidden;
      font-family: system-ui, -apple-system, sans-serif;
      background: {theme["bg"]}; color: {theme["text"]}; }}
    .deck {{ height: 100vh; position: relative; }}
    .slide {{ position: absolute; inset: 0; display: flex; flex-direction: column;
      justify-content: center; align-items: center; padding: 4rem;
      opacity: 0; transition: opacity 0.4s ease; pointer-events: none; text-align: center; }}
    .slide.active {{ opacity: 1; pointer-events: auto; }}
    h1 {{ font-size: clamp(2rem, 5vw, 4rem); font-weight: 700; margin-bottom: 1rem; }}
    h2 {{ font-size: clamp(1.5rem, 3.5vw, 2.5rem); font-weight: 600; margin-bottom: 0.75rem; }}
    p, li {{ font-size: clamp(1rem, 2vw, 1.5rem); line-height: 1.6; }}
    ul {{ text-align: left; max-width: 70%; list-style: none; }}
    ul li::before {{ content: "\\2022"; color: {theme["accent"]}; font-weight: bold;
      display: inline-block; width: 1em; margin-left: -1em; }}
    ul li {{ padding: 0.3rem 0; padding-left: 1em; }}
    .progress {{ position: fixed; bottom: 0; left: 0; height: 4px;
      background: {theme["accent"]}; transition: width 0.3s ease; z-index: 10; }}
    .counter {{ position: fixed; bottom: 1rem; right: 1rem;
      font-size: 0.875rem; opacity: 0.5; }}
    @media print {{
      .slide {{ position: relative; opacity: 1; page-break-after: always;
        min-height: 100vh; pointer-events: auto; }}
      .progress, .counter {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="deck">
      {all_slides}
  </div>
  <div class="progress" id="progress"></div>
  <div class="counter" id="counter"></div>
  <script>
    const slides = document.querySelectorAll('.slide');
    let current = 0;
    function goTo(n) {{
      slides[current].classList.remove('active');
      current = Math.max(0, Math.min(n, slides.length - 1));
      slides[current].classList.add('active');
      document.getElementById('progress').style.width =
        ((current + 1) / slides.length * 100) + '%';
      document.getElementById('counter').textContent =
        (current + 1) + ' / ' + slides.length;
    }}
    document.addEventListener('keydown', e => {{
      if (['ArrowRight','Space','Enter'].includes(e.key)) {{ e.preventDefault(); goTo(current + 1); }}
      if (['ArrowLeft','Backspace'].includes(e.key)) {{ e.preventDefault(); goTo(current - 1); }}
    }});
    let touchStartX = 0;
    document.addEventListener('touchstart', e => touchStartX = e.touches[0].clientX);
    document.addEventListener('touchend', e => {{
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) goTo(current + (diff > 0 ? 1 : -1));
    }});
    goTo(0);
  </script>
</body>
</html>'''


# --- Demo content ---
DEMO_SLIDES = [
    {"type": "title", "heading": "AI Trends 2026", "content": "What builders need to know right now"},
    {"type": "content", "heading": "Agents Are Everywhere", "content": [
        "Autonomous coding agents ship production code daily",
        "Multi-agent orchestration is the new microservices",
        "Skills/plugins replace traditional SaaS integrations",
    ]},
    {"type": "content", "heading": "The Skill Economy", "content": [
        "Single-file markdown skills replace entire apps",
        "Curated skill registries rival package managers",
        "Zero-install, zero-dependency, instant capability",
    ]},
    {"type": "quote", "heading": "", "content": "The best interface is no interface. The best dependency is no dependency.", "author": "The Skill Economy Manifesto"},
    {"type": "code", "heading": "A Skill Is Just a Prompt", "content": "~/.claude/skills/my_skill/SKILL.md\n\n---\nname: My Skill\ndescription: Does amazing things\n---\n\n# Instructions\n1. When the user says X...\n2. Do Y...\n3. Output Z..."},
    {"type": "content", "heading": "HTML as Universal Output", "content": [
        "Self-contained, works offline, zero build step",
        "Runs in any browser on any device",
        "Printable, shareable, archivable",
        "Perfect for presentations, reports, dashboards",
    ]},
    {"type": "content", "heading": "Why This Matters for You", "content": [
        "Lead-gen: auto-generate pitch decks from CRM data",
        "Marketing: notes-to-slides in seconds, not hours",
        "Agent factories: skills compose into pipelines",
        "Ship faster by letting agents handle boilerplate",
    ]},
    {"type": "cta", "heading": "Get Started Today", "content": "Drop SKILL.md into ~/.claude/skills/ and say 'make me a deck'"},
]


def main():
    output_dir = Path("demo-output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "ai-trends-2026-slides.html"
    result = generate_slide_html("AI Trends 2026", DEMO_SLIDES)
    output_file.write_text(result, encoding="utf-8")

    print(f"Generated: {output_file}")
    print(f"File size: {output_file.stat().st_size:,} bytes")
    print(f"Slides: {len(DEMO_SLIDES)}")
    print(f"\nOpen in browser: file://{output_file.resolve()}")
    print("\nNavigation: Arrow keys | Space | Enter | Swipe")


if __name__ == "__main__":
    main()
