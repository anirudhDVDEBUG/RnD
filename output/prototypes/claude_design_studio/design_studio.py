"""
Claude Design Studio - Template-based UI/UX generator.

Generates professional HTML/CSS mockups from structured design specifications.
No external API keys required; uses a composable template system.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DesignSpec:
    """Structured specification for a UI design."""
    title: str
    layout: str  # "dashboard", "landing", "form", "card-grid", "mobile"
    theme: str   # "light", "dark"
    accent: str  # hex color
    components: list[str] = field(default_factory=list)
    columns: int = 12
    description: str = ""


# ---------------------------------------------------------------------------
# Color palettes derived from a single accent
# ---------------------------------------------------------------------------

def palette_from_accent(accent: str, theme: str) -> dict:
    """Generate a full palette from one accent hex color and theme mode."""
    if theme == "dark":
        return {
            "bg": "#0f111a",
            "surface": "#1a1d2e",
            "surface2": "#242840",
            "text": "#e2e8f0",
            "text_secondary": "#94a3b8",
            "border": "#2d3154",
            "accent": accent,
            "accent_hover": accent + "cc",
        }
    return {
        "bg": "#f8fafc",
        "surface": "#ffffff",
        "surface2": "#f1f5f9",
        "text": "#1e293b",
        "text_secondary": "#64748b",
        "border": "#e2e8f0",
        "accent": accent,
        "accent_hover": accent + "cc",
    }


# ---------------------------------------------------------------------------
# Component renderers
# ---------------------------------------------------------------------------

def render_metric_card(label: str, value: str, delta: str, palette: dict) -> str:
    return f"""
    <div class="metric-card">
      <span class="metric-label">{label}</span>
      <span class="metric-value">{value}</span>
      <span class="metric-delta positive">{delta}</span>
    </div>"""


def render_sidebar(items: list[str], palette: dict) -> str:
    links = "\n".join(
        f'        <a href="#" class="nav-link{"" if i else " active"}">'
        f'<span class="nav-icon">{"&#9673;" if i else "&#9679;"}</span> {item}</a>'
        for i, item in enumerate(items)
    )
    return f"""
    <aside class="sidebar">
      <div class="sidebar-brand">Design Studio</div>
      <nav class="sidebar-nav">
{links}
      </nav>
    </aside>"""


def render_header(title: str, palette: dict) -> str:
    return f"""
    <header class="topbar">
      <h1 class="topbar-title">{title}</h1>
      <div class="topbar-actions">
        <span class="avatar">DS</span>
      </div>
    </header>"""


def render_chart_placeholder(palette: dict) -> str:
    bars = ""
    heights = [40, 65, 50, 80, 60, 90, 75, 55, 85, 70, 95, 60]
    for h in heights:
        bars += f'<div class="bar" style="height:{h}%"></div>\n'
    return f"""
    <div class="chart-card">
      <h3 class="chart-title">Revenue Overview</h3>
      <div class="chart-area">
        {bars}
      </div>
      <div class="chart-labels">
        <span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span>
        <span>May</span><span>Jun</span><span>Jul</span><span>Aug</span>
        <span>Sep</span><span>Oct</span><span>Nov</span><span>Dec</span>
      </div>
    </div>"""


def render_table(palette: dict) -> str:
    rows_data = [
        ("Acme Corp", "Enterprise", "$12,400", "Active"),
        ("Globex Inc", "Pro", "$8,200", "Active"),
        ("Initech", "Starter", "$2,100", "Pending"),
        ("Umbrella Ltd", "Enterprise", "$15,800", "Active"),
        ("Wonka Ind", "Pro", "$6,500", "Churned"),
    ]
    rows = ""
    for name, plan, rev, status in rows_data:
        badge_cls = {"Active": "badge-green", "Pending": "badge-yellow", "Churned": "badge-red"}.get(status, "")
        rows += f"""
        <tr>
          <td>{name}</td><td>{plan}</td><td>{rev}</td>
          <td><span class="badge {badge_cls}">{status}</span></td>
        </tr>"""
    return f"""
    <div class="table-card">
      <h3 class="table-title">Recent Customers</h3>
      <table class="data-table">
        <thead><tr><th>Company</th><th>Plan</th><th>Revenue</th><th>Status</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""


def render_form(fields: list[str], palette: dict) -> str:
    inputs = ""
    for f in fields:
        ftype = "password" if "password" in f.lower() else "email" if "email" in f.lower() else "text"
        inputs += f"""
      <div class="form-group">
        <label class="form-label">{f}</label>
        <input type="{ftype}" class="form-input" placeholder="Enter {f.lower()}" />
      </div>"""
    return f"""
    <div class="form-card">
      <h2 class="form-title">Sign In</h2>
      {inputs}
      <button class="btn-primary">Continue</button>
      <p class="form-footer">Don't have an account? <a href="#">Sign up</a></p>
    </div>"""


def render_hero(title: str, subtitle: str, palette: dict) -> str:
    return f"""
    <section class="hero">
      <h1 class="hero-title">{title}</h1>
      <p class="hero-subtitle">{subtitle}</p>
      <div class="hero-actions">
        <button class="btn-primary">Get Started</button>
        <button class="btn-secondary">Learn More</button>
      </div>
    </section>"""


def render_feature_cards(palette: dict) -> str:
    features = [
        ("Lightning Fast", "Optimized for speed with sub-second response times across all endpoints."),
        ("Secure by Default", "End-to-end encryption and SOC 2 compliance built into every layer."),
        ("Scale Infinitely", "Auto-scaling infrastructure that grows with your business needs."),
    ]
    cards = ""
    for title, desc in features:
        cards += f"""
      <div class="feature-card">
        <div class="feature-icon">&#10004;</div>
        <h3>{title}</h3>
        <p>{desc}</p>
      </div>"""
    return f"""
    <section class="features">
      <h2 class="section-title">Why Choose Us</h2>
      <div class="feature-grid">{cards}
      </div>
    </section>"""


# ---------------------------------------------------------------------------
# CSS generator
# ---------------------------------------------------------------------------

def generate_css(palette: dict, layout: str) -> str:
    p = palette
    sidebar_css = ""
    if layout == "dashboard":
        sidebar_css = f"""
    .sidebar {{
      width: 240px; background: {p['surface']}; border-right: 1px solid {p['border']};
      display: flex; flex-direction: column; padding: 1.5rem 0; position: fixed;
      top: 0; left: 0; bottom: 0; z-index: 10;
    }}
    .sidebar-brand {{
      font-size: 1.25rem; font-weight: 700; padding: 0 1.5rem 1.5rem;
      color: {p['accent']}; border-bottom: 1px solid {p['border']};
      margin-bottom: 1rem;
    }}
    .nav-link {{
      display: flex; align-items: center; gap: 0.75rem;
      padding: 0.6rem 1.5rem; color: {p['text_secondary']};
      text-decoration: none; font-size: 0.9rem; transition: all 0.15s;
    }}
    .nav-link:hover, .nav-link.active {{
      color: {p['accent']}; background: {p['surface2']};
    }}
    .main-area {{ margin-left: 240px; }}
    """

    return f"""
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: {p['bg']}; color: {p['text']}; min-height: 100vh;
    }}
    {sidebar_css}
    .topbar {{
      display: flex; justify-content: space-between; align-items: center;
      padding: 1rem 2rem; background: {p['surface']};
      border-bottom: 1px solid {p['border']};
    }}
    .topbar-title {{ font-size: 1.2rem; font-weight: 600; }}
    .avatar {{
      width: 36px; height: 36px; border-radius: 50%; background: {p['accent']};
      color: #fff; display: flex; align-items: center; justify-content: center;
      font-size: 0.8rem; font-weight: 700;
    }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem; padding: 1.5rem 2rem; }}
    .metric-card {{
      background: {p['surface']}; border: 1px solid {p['border']};
      border-radius: 12px; padding: 1.25rem; display: flex; flex-direction: column; gap: 0.4rem;
    }}
    .metric-label {{ font-size: 0.8rem; color: {p['text_secondary']}; text-transform: uppercase; letter-spacing: 0.05em; }}
    .metric-value {{ font-size: 1.75rem; font-weight: 700; }}
    .metric-delta {{ font-size: 0.8rem; }}
    .metric-delta.positive {{ color: #22c55e; }}
    .chart-card, .table-card {{
      background: {p['surface']}; border: 1px solid {p['border']};
      border-radius: 12px; padding: 1.5rem; margin: 0 2rem 1.5rem;
    }}
    .chart-title, .table-title {{ font-size: 1rem; font-weight: 600; margin-bottom: 1rem; }}
    .chart-area {{
      display: flex; align-items: flex-end; gap: 8px; height: 180px;
      padding: 0.5rem 0; border-bottom: 1px solid {p['border']};
    }}
    .bar {{
      flex: 1; background: {p['accent']}; border-radius: 4px 4px 0 0;
      opacity: 0.85; transition: opacity 0.2s;
    }}
    .bar:hover {{ opacity: 1; }}
    .chart-labels {{
      display: flex; justify-content: space-between;
      font-size: 0.7rem; color: {p['text_secondary']}; padding-top: 0.5rem;
    }}
    .data-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    .data-table th {{
      text-align: left; padding: 0.75rem; border-bottom: 2px solid {p['border']};
      color: {p['text_secondary']}; font-weight: 600; font-size: 0.8rem;
      text-transform: uppercase; letter-spacing: 0.04em;
    }}
    .data-table td {{ padding: 0.75rem; border-bottom: 1px solid {p['border']}; }}
    .badge {{
      display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px;
      font-size: 0.75rem; font-weight: 600;
    }}
    .badge-green {{ background: #22c55e22; color: #22c55e; }}
    .badge-yellow {{ background: #eab30822; color: #eab308; }}
    .badge-red {{ background: #ef444422; color: #ef4444; }}

    /* Landing page */
    .hero {{
      text-align: center; padding: 5rem 2rem 3rem;
      background: linear-gradient(135deg, {p['surface']} 0%, {p['surface2']} 100%);
    }}
    .hero-title {{ font-size: 3rem; font-weight: 800; line-height: 1.1; max-width: 700px; margin: 0 auto; }}
    .hero-subtitle {{ font-size: 1.15rem; color: {p['text_secondary']}; margin: 1.25rem auto; max-width: 520px; }}
    .hero-actions {{ display: flex; gap: 1rem; justify-content: center; margin-top: 2rem; }}
    .btn-primary {{
      padding: 0.75rem 1.75rem; background: {p['accent']}; color: #fff;
      border: none; border-radius: 8px; font-size: 1rem; font-weight: 600;
      cursor: pointer;
    }}
    .btn-secondary {{
      padding: 0.75rem 1.75rem; background: transparent; color: {p['text']};
      border: 1px solid {p['border']}; border-radius: 8px; font-size: 1rem;
      cursor: pointer;
    }}
    .features {{ padding: 3rem 2rem; max-width: 1000px; margin: 0 auto; }}
    .section-title {{ text-align: center; font-size: 1.75rem; font-weight: 700; margin-bottom: 2rem; }}
    .feature-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }}
    .feature-card {{
      background: {p['surface']}; border: 1px solid {p['border']};
      border-radius: 12px; padding: 1.5rem;
    }}
    .feature-icon {{ font-size: 1.5rem; color: {p['accent']}; margin-bottom: 0.75rem; }}
    .feature-card h3 {{ margin-bottom: 0.5rem; }}
    .feature-card p {{ color: {p['text_secondary']}; font-size: 0.9rem; line-height: 1.5; }}

    /* Form */
    .form-card {{
      max-width: 400px; margin: 4rem auto; background: {p['surface']};
      border: 1px solid {p['border']}; border-radius: 16px; padding: 2.5rem;
    }}
    .form-title {{ margin-bottom: 1.5rem; font-size: 1.5rem; font-weight: 700; text-align: center; }}
    .form-group {{ margin-bottom: 1rem; }}
    .form-label {{ display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.35rem; }}
    .form-input {{
      width: 100%; padding: 0.65rem 0.9rem; border: 1px solid {p['border']};
      border-radius: 8px; font-size: 0.95rem; background: {p['bg']}; color: {p['text']};
    }}
    .form-input:focus {{ outline: 2px solid {p['accent']}; border-color: transparent; }}
    .form-card .btn-primary {{ width: 100%; margin-top: 0.5rem; }}
    .form-footer {{ text-align: center; margin-top: 1rem; font-size: 0.85rem; color: {p['text_secondary']}; }}
    .form-footer a {{ color: {p['accent']}; text-decoration: none; }}
    """


# ---------------------------------------------------------------------------
# Page assembler
# ---------------------------------------------------------------------------

def generate_design(spec: DesignSpec) -> str:
    """Generate a complete HTML page from a DesignSpec."""
    palette = palette_from_accent(spec.accent, spec.theme)
    css = generate_css(palette, spec.layout)
    body_parts: list[str] = []

    if spec.layout == "dashboard":
        nav_items = ["Dashboard", "Analytics", "Customers", "Products", "Settings"]
        body_parts.append(render_sidebar(nav_items, palette))
        body_parts.append('<div class="main-area">')
        body_parts.append(render_header(spec.title, palette))
        body_parts.append('<div class="metrics">')
        metrics = [
            ("Total Revenue", "$48,250", "+12.5%"),
            ("Active Users", "2,847", "+8.2%"),
            ("Conversion", "3.24%", "+0.8%"),
            ("Avg Order", "$68.40", "+4.1%"),
        ]
        for label, value, delta in metrics:
            body_parts.append(render_metric_card(label, value, delta, palette))
        body_parts.append("</div>")
        body_parts.append(render_chart_placeholder(palette))
        body_parts.append(render_table(palette))
        body_parts.append("</div>")

    elif spec.layout == "landing":
        body_parts.append(render_hero(spec.title,
            spec.description or "Build better products faster with our modern platform.", palette))
        body_parts.append(render_feature_cards(palette))

    elif spec.layout == "form":
        body_parts.append(render_form(["Email Address", "Password"], palette))

    elif spec.layout == "card-grid":
        body_parts.append(render_header(spec.title, palette))
        body_parts.append(render_feature_cards(palette))

    body_html = "\n".join(body_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{spec.title}</title>
  <style>{css}</style>
</head>
<body>
{body_html}
</body>
</html>"""


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Claude Design Studio - UI/UX Generator")
    parser.add_argument("--layout", choices=["dashboard", "landing", "form", "card-grid"],
                        default="dashboard", help="Layout type")
    parser.add_argument("--theme", choices=["light", "dark"], default="dark", help="Color theme")
    parser.add_argument("--accent", default="#6366f1", help="Accent color (hex)")
    parser.add_argument("--title", default="Design Studio Dashboard", help="Page title")
    parser.add_argument("--description", default="", help="Subtitle / description")
    parser.add_argument("--output", "-o", default=None, help="Output HTML file path")
    parser.add_argument("--json-spec", default=None, help="Path to JSON spec file")
    args = parser.parse_args()

    if args.json_spec:
        with open(args.json_spec) as f:
            data = json.load(f)
        spec = DesignSpec(**data)
    else:
        spec = DesignSpec(
            title=args.title,
            layout=args.layout,
            theme=args.theme,
            accent=args.accent,
            description=args.description,
        )

    html = generate_design(spec)
    out_path = args.output or f"output_{spec.layout}_{spec.theme}.html"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    with open(out_path, "w") as f:
        f.write(html)

    file_size = os.path.getsize(out_path)
    print(f"[Claude Design Studio]")
    print(f"  Layout : {spec.layout}")
    print(f"  Theme  : {spec.theme}")
    print(f"  Accent : {spec.accent}")
    print(f"  Output : {out_path}  ({file_size:,} bytes)")
    print(f"  Open in a browser to preview the design.")


if __name__ == "__main__":
    main()
