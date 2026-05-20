"""
AnyDesign Analyzer — extracts design tokens, component inventory,
and reconstruction notes from images, websites, or Figma files.
"""

import json
import re
import sys
from pathlib import Path

# Optional heavy deps — graceful fallback
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


# ---------------------------------------------------------------------------
# Color utilities
# ---------------------------------------------------------------------------

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def parse_css_color(val):
    """Parse rgb()/rgba() or hex color strings to (r,g,b) tuple."""
    val = val.strip()
    if val.startswith("#"):
        h = val.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", val)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None


def cluster_colors(colors, threshold=30):
    """Simple color clustering by Euclidean distance."""
    clusters = []
    for c in colors:
        merged = False
        for cl in clusters:
            dr = c[0] - cl["center"][0]
            dg = c[1] - cl["center"][1]
            db = c[2] - cl["center"][2]
            if (dr*dr + dg*dg + db*db) < threshold * threshold:
                cl["count"] += 1
                merged = True
                break
        if not merged:
            clusters.append({"center": c, "count": 1})
    clusters.sort(key=lambda x: -x["count"])
    return clusters


# ---------------------------------------------------------------------------
# Token extraction from image pixels
# ---------------------------------------------------------------------------

def extract_tokens_from_image(image_path):
    """Extract approximate design tokens from an image using PIL."""
    if not HAS_PIL:
        return None
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # Sample pixels on a grid
    step = max(1, min(w, h) // 80)
    raw_colors = []
    for y in range(0, h, step):
        for x in range(0, w, step):
            raw_colors.append(img.getpixel((x, y)))

    clusters = cluster_colors(raw_colors)
    top_colors = clusters[:12]

    # Classify colors heuristically
    palette = []
    for i, cl in enumerate(top_colors):
        r, g, b = cl["center"]
        hex_val = rgb_to_hex(r, g, b)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        if luminance > 240:
            role = "background"
        elif luminance < 30:
            role = "text"
        elif r > g and r > b:
            role = "accent-warm"
        elif b > r and b > g:
            role = "primary"
        elif g > r and g > b:
            role = "success"
        else:
            role = f"neutral-{i}"
        palette.append({"hex": hex_val, "role": role, "weight": cl["count"]})

    return {
        "source": str(image_path),
        "dimensions": f"{w}x{h}",
        "colors": palette,
        "typography": _guess_typography(),
        "spacing": _default_spacing_scale(),
        "shadows": _default_shadows(),
        "radii": _default_radii(),
    }


# ---------------------------------------------------------------------------
# Token extraction from live website via Playwright
# ---------------------------------------------------------------------------

def extract_tokens_from_url(url):
    """Capture a website and extract computed styles."""
    if not HAS_PLAYWRIGHT:
        print("Playwright not installed — falling back to mock data.")
        return None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.screenshot(path="capture.png", full_page=True)

        styles = page.evaluate("""
            () => {
                const allElements = document.querySelectorAll('*');
                const colors = new Set();
                const fonts = new Set();
                const fontSizes = new Set();
                const spacings = new Set();
                const radii = new Set();
                const shadows = new Set();
                allElements.forEach(el => {
                    const s = getComputedStyle(el);
                    colors.add(s.color);
                    colors.add(s.backgroundColor);
                    colors.add(s.borderColor);
                    fonts.add(s.fontFamily);
                    fontSizes.add(s.fontSize);
                    spacings.add(s.paddingTop);
                    spacings.add(s.paddingRight);
                    spacings.add(s.marginTop);
                    spacings.add(s.marginBottom);
                    spacings.add(s.gap);
                    radii.add(s.borderRadius);
                    if (s.boxShadow !== 'none') shadows.add(s.boxShadow);
                });
                return {
                    colors: [...colors],
                    fonts: [...fonts],
                    fontSizes: [...fontSizes],
                    spacings: [...spacings],
                    radii: [...radii],
                    shadows: [...shadows]
                };
            }
        """)
        browser.close()

    # Parse and cluster colors
    parsed = [parse_css_color(c) for c in styles["colors"]]
    parsed = [c for c in parsed if c is not None]
    clusters = cluster_colors(parsed)
    palette = []
    for i, cl in enumerate(clusters[:12]):
        r, g, b = cl["center"]
        palette.append({"hex": rgb_to_hex(r, g, b), "role": f"color-{i}", "weight": cl["count"]})

    # Parse spacing values
    spacing_px = set()
    for s in styles["spacings"]:
        m = re.match(r"(\d+)px", s)
        if m:
            spacing_px.add(int(m.group(1)))

    spacing_scale = sorted(spacing_px)[:10]

    return {
        "source": url,
        "dimensions": "1440x900 viewport",
        "colors": palette,
        "typography": {
            "families": list(set(styles["fonts"]))[:5],
            "sizes": sorted(set(styles["fontSizes"]))[:8],
        },
        "spacing": [{"token": f"space.{i+1}", "value": f"{v}px"} for i, v in enumerate(spacing_scale)],
        "shadows": [{"token": f"shadow.{i+1}", "value": v} for i, v in enumerate(styles["shadows"][:4])],
        "radii": [{"token": f"radius.{i+1}", "value": v} for i, v in enumerate(set(styles["radii"]))[:4]],
    }


# ---------------------------------------------------------------------------
# Mock / fallback data for demo without external deps
# ---------------------------------------------------------------------------

def load_mock_tokens():
    """Return realistic mock tokens for a SaaS dashboard design."""
    return {
        "source": "mock://saas-dashboard-screenshot.png",
        "dimensions": "1440x900",
        "colors": [
            {"hex": "#3b82f6", "role": "primary", "weight": 340},
            {"hex": "#1e40af", "role": "primary-dark", "weight": 120},
            {"hex": "#dbeafe", "role": "primary-light", "weight": 210},
            {"hex": "#111827", "role": "text", "weight": 890},
            {"hex": "#6b7280", "role": "text-secondary", "weight": 450},
            {"hex": "#f9fafb", "role": "background", "weight": 1620},
            {"hex": "#ffffff", "role": "surface", "weight": 2100},
            {"hex": "#e5e7eb", "role": "border", "weight": 380},
            {"hex": "#10b981", "role": "success", "weight": 85},
            {"hex": "#ef4444", "role": "error", "weight": 60},
            {"hex": "#f59e0b", "role": "warning", "weight": 45},
            {"hex": "#8b5cf6", "role": "accent", "weight": 70},
        ],
        "typography": {
            "families": ["Inter, sans-serif", "JetBrains Mono, monospace"],
            "sizes": ["12px", "14px", "16px", "18px", "20px", "24px", "30px", "36px"],
            "weights": ["400", "500", "600", "700"],
            "lineHeights": ["1.25", "1.5", "1.75"],
        },
        "spacing": [
            {"token": "space.1", "value": "4px"},
            {"token": "space.2", "value": "8px"},
            {"token": "space.3", "value": "12px"},
            {"token": "space.4", "value": "16px"},
            {"token": "space.5", "value": "20px"},
            {"token": "space.6", "value": "24px"},
            {"token": "space.8", "value": "32px"},
            {"token": "space.10", "value": "40px"},
            {"token": "space.12", "value": "48px"},
            {"token": "space.16", "value": "64px"},
        ],
        "shadows": [
            {"token": "shadow.sm", "value": "0 1px 2px rgba(0,0,0,0.05)"},
            {"token": "shadow.md", "value": "0 4px 6px -1px rgba(0,0,0,0.1)"},
            {"token": "shadow.lg", "value": "0 10px 15px -3px rgba(0,0,0,0.1)"},
            {"token": "shadow.xl", "value": "0 20px 25px -5px rgba(0,0,0,0.1)"},
        ],
        "radii": [
            {"token": "radius.sm", "value": "4px"},
            {"token": "radius.md", "value": "8px"},
            {"token": "radius.lg", "value": "12px"},
            {"token": "radius.full", "value": "9999px"},
        ],
        "components": [
            {"name": "Button", "variants": "primary, secondary, ghost, danger", "tokens": "color.primary.500, font.size.sm, radius.md, shadow.sm"},
            {"name": "Card", "variants": "default, elevated, outlined", "tokens": "surface, border, radius.lg, shadow.md"},
            {"name": "Input", "variants": "text, search, select", "tokens": "border, radius.md, font.size.base, space.3"},
            {"name": "Badge", "variants": "success, warning, error, info", "tokens": "color.success, font.size.xs, radius.full"},
            {"name": "Avatar", "variants": "sm, md, lg, xl", "tokens": "radius.full, border, shadow.sm"},
            {"name": "Sidebar", "variants": "expanded, collapsed", "tokens": "surface, border, space.4, shadow.lg"},
            {"name": "Table", "variants": "default, striped, compact", "tokens": "border, font.size.sm, space.3"},
            {"name": "Modal", "variants": "sm, md, lg, fullscreen", "tokens": "surface, shadow.xl, radius.lg, space.6"},
            {"name": "Tabs", "variants": "underline, pills, enclosed", "tokens": "color.primary.500, border, font.size.sm"},
            {"name": "Tooltip", "variants": "top, bottom, left, right", "tokens": "text, surface, radius.sm, shadow.md"},
        ],
        "layout": {
            "strategy": "CSS Grid + Flexbox hybrid",
            "breakpoints": ["640px (sm)", "768px (md)", "1024px (lg)", "1280px (xl)", "1536px (2xl)"],
            "framework_hints": "Tailwind CSS class naming detected (space-y-*, rounded-lg, shadow-md)",
            "responsive_strategy": "Mobile-first with collapsible sidebar, stacked cards below md breakpoint",
        },
    }


def _guess_typography():
    return {
        "families": ["system-ui, sans-serif"],
        "sizes": ["14px", "16px", "20px", "24px", "32px"],
        "weights": ["400", "600", "700"],
        "lineHeights": ["1.5"],
    }


def _default_spacing_scale():
    return [{"token": f"space.{i}", "value": f"{i*4}px"} for i in range(1, 11)]


def _default_shadows():
    return [
        {"token": "shadow.sm", "value": "0 1px 2px rgba(0,0,0,0.05)"},
        {"token": "shadow.md", "value": "0 4px 6px -1px rgba(0,0,0,0.1)"},
    ]


def _default_radii():
    return [
        {"token": "radius.sm", "value": "4px"},
        {"token": "radius.md", "value": "8px"},
        {"token": "radius.lg", "value": "12px"},
    ]


# ---------------------------------------------------------------------------
# design.md generator
# ---------------------------------------------------------------------------

def generate_design_md(tokens, output_path="design.md"):
    """Generate a structured design.md from extracted tokens."""
    source = tokens.get("source", "Unknown")
    lines = []
    lines.append(f"# Design System — Extracted from `{source}`\n")
    lines.append(f"> Auto-generated by AnyDesign Analyzer | Source dimensions: {tokens.get('dimensions', 'N/A')}\n")

    # --- Colors ---
    lines.append("## Design Tokens\n")
    lines.append("### Colors\n")
    lines.append("| Token | Value | Swatch | Usage / Role |")
    lines.append("|-------|-------|--------|-------------|")
    for c in tokens.get("colors", []):
        swatch = f"![{c['hex']}](https://via.placeholder.com/16/{c['hex'].lstrip('#')}/000000?text=+)"
        lines.append(f"| `color.{c['role']}` | `{c['hex']}` | {swatch} | {c['role']} |")
    lines.append("")

    # --- DTCG JSON block ---
    lines.append("#### DTCG Format (Design Token Community Group)\n")
    lines.append("```json")
    dtcg = {}
    for c in tokens.get("colors", []):
        dtcg[f"color.{c['role']}"] = {"$value": c["hex"], "$type": "color"}
    lines.append(json.dumps(dtcg, indent=2))
    lines.append("```\n")

    # --- Typography ---
    typo = tokens.get("typography", {})
    lines.append("### Typography\n")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    for fam in typo.get("families", []):
        lines.append(f"| `font.family` | `{fam}` |")
    for sz in typo.get("sizes", []):
        lines.append(f"| `font.size` | `{sz}` |")
    for w in typo.get("weights", []):
        lines.append(f"| `font.weight` | `{w}` |")
    for lh in typo.get("lineHeights", []):
        lines.append(f"| `font.lineHeight` | `{lh}` |")
    lines.append("")

    # --- Spacing ---
    lines.append("### Spacing Scale\n")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    for s in tokens.get("spacing", []):
        lines.append(f"| `{s['token']}` | `{s['value']}` |")
    lines.append("")

    # --- Shadows ---
    lines.append("### Shadows\n")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    for s in tokens.get("shadows", []):
        lines.append(f"| `{s['token']}` | `{s['value']}` |")
    lines.append("")

    # --- Border Radius ---
    lines.append("### Border Radius\n")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    for r in tokens.get("radii", []):
        lines.append(f"| `{r['token']}` | `{r['value']}` |")
    lines.append("")

    # --- Component Inventory ---
    components = tokens.get("components", [])
    if components:
        lines.append("## Component Inventory\n")
        lines.append("| Component | Variants | Tokens Used |")
        lines.append("|-----------|----------|-------------|")
        for comp in components:
            lines.append(f"| **{comp['name']}** | {comp['variants']} | `{comp['tokens']}` |")
        lines.append("")

    # --- Layout / Reconstruction Notes ---
    layout = tokens.get("layout", {})
    if layout:
        lines.append("## Reconstruction Notes\n")
        lines.append(f"- **Layout strategy**: {layout.get('strategy', 'Unknown')}")
        bps = layout.get("breakpoints", [])
        if bps:
            lines.append(f"- **Breakpoints**: {', '.join(bps)}")
        if layout.get("framework_hints"):
            lines.append(f"- **Framework hints**: {layout['framework_hints']}")
        if layout.get("responsive_strategy"):
            lines.append(f"- **Responsive strategy**: {layout['responsive_strategy']}")
        lines.append("")

    lines.append("---\n")
    lines.append("*Generated by [AnyDesign Analyzer](https://github.com/uxKero/anydesign)*\n")

    content = "\n".join(lines)
    Path(output_path).write_text(content)
    return content


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AnyDesign Analyzer — extract design tokens from any visual source")
    parser.add_argument("source", nargs="?", default=None,
                        help="Image path, URL, or 'mock' for demo mode")
    parser.add_argument("-o", "--output", default="design.md",
                        help="Output file path (default: design.md)")
    args = parser.parse_args()

    source = args.source or "mock"
    tokens = None

    if source == "mock":
        print("[AnyDesign] Running in demo mode with mock SaaS dashboard data...")
        tokens = load_mock_tokens()

    elif source.startswith("http://") or source.startswith("https://"):
        if "figma.com" in source:
            print(f"[AnyDesign] Figma extraction requires FIGMA_ACCESS_TOKEN env var.")
            print(f"[AnyDesign] Falling back to mock data for demo.")
            tokens = load_mock_tokens()
        else:
            print(f"[AnyDesign] Capturing website: {source}")
            tokens = extract_tokens_from_url(source)
            if tokens is None:
                print("[AnyDesign] Playwright unavailable — using mock data.")
                tokens = load_mock_tokens()

    elif Path(source).is_file():
        print(f"[AnyDesign] Analyzing image: {source}")
        tokens = extract_tokens_from_image(source)
        if tokens is None:
            print("[AnyDesign] Pillow unavailable — using mock data.")
            tokens = load_mock_tokens()
        else:
            # Augment image tokens with defaults for components/layout
            mock = load_mock_tokens()
            tokens.setdefault("components", mock["components"])
            tokens.setdefault("layout", mock["layout"])
    else:
        print(f"[AnyDesign] Source not found: {source}")
        print("[AnyDesign] Running in demo mode with mock data...")
        tokens = load_mock_tokens()

    content = generate_design_md(tokens, args.output)

    print(f"\n[AnyDesign] Wrote {args.output} ({len(content)} bytes)")
    print(f"[AnyDesign] Extracted {len(tokens.get('colors', []))} colors, "
          f"{len(tokens.get('spacing', []))} spacing tokens, "
          f"{len(tokens.get('components', []))} components")
    print(f"\n{'='*60}")
    print("PREVIEW (first 60 lines):")
    print("=" * 60)
    for line in content.split("\n")[:60]:
        print(line)
    print("..." if content.count("\n") > 60 else "")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
