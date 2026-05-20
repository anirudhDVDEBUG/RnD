---
name: anydesign_analyzer
description: |
  Analyzes images, websites, and Figma files to generate a structured design.md with a design token system (DTCG format), component inventory, and reconstruction notes.
  Triggers: "analyze this design", "extract design tokens", "generate design.md", "reverse-engineer this UI", "create design system from"
---

# AnyDesign Analyzer

Analyze images, live websites, and Figma files to produce a structured `design.md` containing a complete design token system, component inventory, and reconstruction notes.

## When to use

- "Analyze this design and extract tokens" — when given a screenshot, image, or mockup
- "Generate a design.md from this website" — when pointed at a live URL to reverse-engineer
- "Extract the design system from this Figma file" — when given a Figma URL or file
- "Create design tokens from this UI" — when the user wants DTCG-format tokens from any visual source
- "Reverse-engineer this interface" — when the user wants a component inventory and reconstruction plan

## How to use

### Step 1: Identify the source type

Determine whether the input is:
- **Image/screenshot** — a local file path (PNG, JPG, WebP, etc.)
- **Website URL** — a live page to capture via Playwright
- **Figma URL** — a Figma file, frame, or component URL

### Step 2: Capture the design

**For websites**, use Playwright to capture a full-page screenshot and extract computed styles:

```bash
pip install playwright && python -m playwright install chromium
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url)
    page.screenshot(path="capture.png", full_page=True)
    styles = page.evaluate('''
        () => {
            const allElements = document.querySelectorAll('*');
            const colors = new Set();
            const fonts = new Set();
            const spacings = new Set();
            allElements.forEach(el => {
                const s = getComputedStyle(el);
                colors.add(s.color);
                colors.add(s.backgroundColor);
                fonts.add(s.fontFamily);
                spacings.add(s.padding);
                spacings.add(s.margin);
            });
            return { colors: [...colors], fonts: [...fonts], spacings: [...spacings] };
        }
    ''')
    browser.close()
```

**For Figma files**, use the Figma REST API (requires `FIGMA_ACCESS_TOKEN` env var):

```bash
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/{file_key}?geometry=paths"
```

**For images**, read the file directly and analyze visually.

### Step 3: Analyze and extract design tokens

Extract the following token categories in **DTCG** format:

- **Colors**: primary, secondary, neutral, semantic (success, warning, error, info)
- **Typography**: font families, sizes, weights, line heights, letter spacing
- **Spacing**: padding, margin, gap values (map to a scale like 4px base)
- **Border radius**: corner radius values
- **Shadows**: box-shadow and drop-shadow definitions
- **Breakpoints**: responsive breakpoints if detectable

### Step 4: Generate `design.md`

Produce a structured markdown file with these sections:

```markdown
# Design System — [Project Name]

## Design Tokens

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| `color.primary.500` | #3B82F6 | Primary actions, links |

### Typography
| Token | Value |
|-------|-------|
| `font.family.body` | Inter, sans-serif |

### Spacing
| Token | Value |
|-------|-------|
| `space.1` | 4px |

### Shadows
| Token | Value |
|-------|-------|
| `shadow.sm` | 0 1px 2px rgba(0,0,0,0.05) |

## Component Inventory

| Component | Variants | Tokens Used |
|-----------|----------|-------------|
| Button | primary, secondary, ghost | color.primary.500, font.size.base |

## Reconstruction Notes

- Layout: CSS Grid / Flexbox patterns observed
- Framework hints: detected class naming conventions
- Responsive strategy: breakpoints and layout shifts
```

### Step 5: Save the output

Write the generated file to `design.md` in the project root (or a user-specified path).

## References

- Source repository: https://github.com/uxKero/anydesign
- [DTCG Design Tokens Spec](https://design-tokens.github.io/community-group/format/)
- [Playwright Python docs](https://playwright.dev/python/)
- [Figma REST API](https://www.figma.com/developers/api)
