"""
CSS Architecture Guide - Tailwind-to-Structured-CSS Migration Tool

Analyzes HTML with Tailwind utility classes and generates structured CSS
following modern architecture patterns (cascade layers, custom properties,
layout primitives, component styles).
"""

import re
import sys
from collections import defaultdict

# Mapping of common Tailwind utilities to CSS properties
TAILWIND_MAP = {
    # Display
    "flex": ("display", "flex"),
    "grid": ("display", "grid"),
    "block": ("display", "block"),
    "inline": ("display", "inline"),
    "hidden": ("display", "none"),
    # Flex
    "flex-col": ("flex-direction", "column"),
    "flex-row": ("flex-direction", "row"),
    "flex-wrap": ("flex-wrap", "wrap"),
    "items-center": ("align-items", "center"),
    "items-start": ("align-items", "flex-start"),
    "items-end": ("align-items", "flex-end"),
    "justify-center": ("justify-content", "center"),
    "justify-between": ("justify-content", "space-between"),
    "justify-end": ("justify-content", "flex-end"),
    # Spacing
    "gap-1": ("gap", "var(--space-xs)"),
    "gap-2": ("gap", "var(--space-s)"),
    "gap-3": ("gap", "var(--space-s)"),
    "gap-4": ("gap", "var(--space-m)"),
    "gap-6": ("gap", "var(--space-l)"),
    "gap-8": ("gap", "var(--space-xl)"),
    # Padding
    "p-2": ("padding", "var(--space-s)"),
    "p-4": ("padding", "var(--space-m)"),
    "p-6": ("padding", "var(--space-l)"),
    "p-8": ("padding", "var(--space-xl)"),
    "px-4": ("padding-inline", "var(--space-m)"),
    "px-6": ("padding-inline", "var(--space-l)"),
    "py-2": ("padding-block", "var(--space-s)"),
    "py-4": ("padding-block", "var(--space-m)"),
    "py-8": ("padding-block", "var(--space-xl)"),
    # Margin
    "m-auto": ("margin", "auto"),
    "mx-auto": ("margin-inline", "auto"),
    "mt-4": ("margin-top", "var(--space-m)"),
    "mb-4": ("margin-bottom", "var(--space-m)"),
    "mb-2": ("margin-bottom", "var(--space-s)"),
    # Typography
    "text-sm": ("font-size", "var(--text-sm)"),
    "text-base": ("font-size", "var(--text-base)"),
    "text-lg": ("font-size", "var(--text-lg)"),
    "text-xl": ("font-size", "var(--text-xl)"),
    "text-2xl": ("font-size", "var(--text-2xl)"),
    "text-3xl": ("font-size", "var(--text-3xl)"),
    "font-bold": ("font-weight", "700"),
    "font-semibold": ("font-weight", "600"),
    "font-medium": ("font-weight", "500"),
    "text-center": ("text-align", "center"),
    "text-left": ("text-align", "left"),
    "leading-relaxed": ("line-height", "var(--leading-relaxed)"),
    "leading-tight": ("line-height", "var(--leading-tight)"),
    # Colors (mapped to custom properties)
    "text-white": ("color", "var(--color-white)"),
    "text-gray-500": ("color", "var(--color-gray-500)"),
    "text-gray-600": ("color", "var(--color-gray-600)"),
    "text-gray-700": ("color", "var(--color-gray-700)"),
    "text-gray-900": ("color", "var(--color-gray-900)"),
    "bg-white": ("background", "var(--color-white)"),
    "bg-gray-100": ("background", "var(--color-gray-100)"),
    "bg-gray-50": ("background", "var(--color-gray-50)"),
    "bg-blue-500": ("background", "var(--color-blue-500)"),
    "bg-blue-600": ("background", "var(--color-blue-600)"),
    # Borders
    "rounded": ("border-radius", "var(--radius-s)"),
    "rounded-md": ("border-radius", "var(--radius-m)"),
    "rounded-lg": ("border-radius", "var(--radius-l)"),
    "rounded-full": ("border-radius", "9999px"),
    "border": ("border", "1px solid var(--border-color)"),
    "border-gray-200": ("border-color", "var(--color-gray-200)"),
    # Shadows
    "shadow": ("box-shadow", "var(--shadow-sm)"),
    "shadow-md": ("box-shadow", "var(--shadow-md)"),
    "shadow-lg": ("box-shadow", "var(--shadow-lg)"),
    # Width/Height
    "w-full": ("width", "100%"),
    "h-full": ("height", "100%"),
    "max-w-md": ("max-width", "var(--measure-md)"),
    "max-w-lg": ("max-width", "var(--measure-lg)"),
    "max-w-xl": ("max-width", "var(--measure-xl)"),
    # Overflow
    "overflow-hidden": ("overflow", "hidden"),
    "overflow-auto": ("overflow", "auto"),
    # Position
    "relative": ("position", "relative"),
    "absolute": ("position", "absolute"),
    # Cursor
    "cursor-pointer": ("cursor", "pointer"),
    # Transitions
    "transition": ("transition", "all 150ms ease"),
}


def extract_components(html: str) -> dict:
    """Extract elements with class attributes from HTML, grouping by semantic role."""
    pattern = r'<(\w+)\s[^>]*class="([^"]+)"[^>]*>'
    matches = re.findall(pattern, html)

    components = defaultdict(list)
    for tag, classes in matches:
        class_list = classes.split()
        # Try to find a semantic class name (non-Tailwind)
        semantic = [c for c in class_list if c not in TAILWIND_MAP and not re.match(r'^(hover|focus|md|lg|sm|xl):', c)]
        tailwind = [c for c in class_list if c in TAILWIND_MAP]

        if semantic:
            name = semantic[0]
        else:
            name = f"{tag}-component"

        components[name].append(tailwind)

    return components


def generate_tokens() -> str:
    """Generate design token layer."""
    return """@layer tokens {
  :root {
    /* Spacing scale */
    --space-xs: 0.25rem;
    --space-s: 0.5rem;
    --space-m: 1rem;
    --space-l: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;

    /* Typography scale */
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;
    --text-3xl: 1.875rem;
    --leading-tight: 1.25;
    --leading-relaxed: 1.625;

    /* Colors */
    --color-white: #ffffff;
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-200: #e5e7eb;
    --color-gray-500: #6b7280;
    --color-gray-600: #4b5563;
    --color-gray-700: #374151;
    --color-gray-900: #111827;
    --color-blue-500: #3b82f6;
    --color-blue-600: #2563eb;

    /* Borders & Shadows */
    --radius-s: 0.25rem;
    --radius-m: 0.375rem;
    --radius-l: 0.5rem;
    --border-color: var(--color-gray-200);
    --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px rgb(0 0 0 / 0.07);
    --shadow-lg: 0 10px 15px rgb(0 0 0 / 0.1);

    /* Measures */
    --measure-md: 28rem;
    --measure-lg: 32rem;
    --measure-xl: 36rem;
  }
}"""


def generate_component_css(name: str, utility_lists: list) -> str:
    """Convert a list of Tailwind utilities into a named component class."""
    # Merge all utility occurrences
    all_utils = set()
    for utils in utility_lists:
        all_utils.update(utils)

    properties = {}
    for util in sorted(all_utils):
        if util in TAILWIND_MAP:
            prop, value = TAILWIND_MAP[util]
            properties[prop] = value

    if not properties:
        return ""

    lines = [f"  .{name} {{"]
    for prop, value in sorted(properties.items()):
        lines.append(f"    {prop}: {value};")
    lines.append("  }")

    return "\n".join(lines)


def convert_html_to_css(html: str) -> str:
    """Main conversion: HTML with Tailwind -> structured CSS architecture."""
    components = extract_components(html)

    output_parts = []

    # Layer declaration
    output_parts.append("@layer reset, tokens, layout, components, utilities;\n")

    # Tokens
    output_parts.append(generate_tokens())
    output_parts.append("")

    # Components
    component_styles = []
    for name, utility_lists in components.items():
        css = generate_component_css(name, utility_lists)
        if css:
            component_styles.append(css)

    if component_styles:
        output_parts.append("@layer components {")
        output_parts.append("\n\n".join(component_styles))
        output_parts.append("}")

    return "\n\n".join(output_parts)


SAMPLE_HTML = """\
<div class="card flex flex-col gap-4 p-6 rounded-lg shadow-md bg-white">
  <h2 class="card-title text-2xl font-bold text-gray-900">
    Getting Started with CSS Architecture
  </h2>
  <p class="card-body text-base leading-relaxed text-gray-700">
    Modern CSS has powerful features like cascade layers, container queries,
    and native nesting. You don't need a utility framework to write
    maintainable styles.
  </p>
  <button class="btn px-6 py-2 bg-blue-600 text-white rounded-md font-semibold cursor-pointer transition">
    Learn More
  </button>
</div>

<nav class="nav-bar flex items-center justify-between p-4 bg-gray-50 border border-gray-200 rounded-lg">
  <a class="nav-logo text-xl font-bold text-gray-900" href="/">CSS Guide</a>
  <ul class="nav-links flex gap-4 items-center">
    <li><a class="nav-link text-gray-600 font-medium" href="/docs">Docs</a></li>
    <li><a class="nav-link text-gray-600 font-medium" href="/examples">Examples</a></li>
  </ul>
</nav>

<section class="hero flex flex-col items-center justify-center py-8 gap-6 text-center max-w-xl mx-auto">
  <h1 class="hero-title text-3xl font-bold text-gray-900 leading-tight">
    Structure Your CSS Without Tailwind
  </h1>
  <p class="hero-subtitle text-lg text-gray-600 leading-relaxed">
    Learn how to architect maintainable stylesheets using modern CSS features:
    cascade layers, custom properties, and layout primitives.
  </p>
</section>
"""


def main():
    print("=" * 70)
    print("  CSS Architecture Guide - Tailwind to Structured CSS Converter")
    print("=" * 70)
    print()

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath) as f:
            html = f.read()
        print(f"[Reading from {filepath}]")
    else:
        html = SAMPLE_HTML
        print("[Using built-in sample HTML with Tailwind classes]")

    print()
    print("-" * 70)
    print("INPUT HTML (with Tailwind utilities):")
    print("-" * 70)
    # Show first 30 lines
    for i, line in enumerate(html.strip().split("\n")[:30]):
        print(f"  {line}")
    print()

    result = convert_html_to_css(html)

    print("-" * 70)
    print("OUTPUT: Structured CSS (cascade layers + custom properties)")
    print("-" * 70)
    print()
    print(result)
    print()
    print("-" * 70)
    print("ARCHITECTURE SUMMARY:")
    print("-" * 70)

    components = extract_components(html)
    print(f"  Components extracted: {len(components)}")
    for name in sorted(components.keys()):
        count = len(components[name])
        print(f"    .{name} (found {count}x)")

    print()
    print("  Layer order: reset -> tokens -> layout -> components -> utilities")
    print("  Design tokens: spacing (6), typography (8), colors (10), effects (6)")
    print()
    print("  Key principles applied:")
    print("    1. Cascade layers for specificity control")
    print("    2. Custom properties for design tokens (no magic numbers)")
    print("    3. Semantic class names replacing utility clusters")
    print("    4. Native CSS nesting-ready structure")
    print()

    # Write output file
    with open("output.css", "w") as f:
        f.write(result)
    print("  Written to: output.css")
    print()


if __name__ == "__main__":
    main()
