# Technical Details — AnyDesign Analyzer

## What It Does

AnyDesign Analyzer reverse-engineers visual designs (screenshots, live websites, Figma files) into structured design system documentation. It extracts color palettes via pixel sampling and clustering, pulls typography/spacing/shadow values from computed CSS (for websites), and organizes everything into a `design.md` file using DTCG (Design Token Community Group) format. The output is immediately usable for rebuilding the UI or seeding a design token pipeline.

The core insight is that most design systems follow predictable patterns — a 4px spacing scale, a limited color palette, a handful of font sizes — and these can be reliably extracted from any visual representation, not just Figma source files.

## Architecture

### Key Files

| File | Purpose |
|------|---------|
| `analyzer.py` | Single-file implementation: token extraction, clustering, markdown generation |
| `SKILL.md` | Claude Code skill definition with trigger phrases and step-by-step instructions |
| `run.sh` | Demo runner that exercises mock mode |

### Data Flow

```
Input Source                  Extraction              Output
-----------                  ----------              ------
Image file    -->  PIL pixel sampling  \
Website URL   -->  Playwright capture   }--> Token clustering --> design.md
Figma URL     -->  Figma REST API      /      + classification
(mock data)   -->  Built-in fixtures  /
```

### Key Algorithms

- **Color clustering**: Euclidean distance in RGB space with a threshold of 30 units. Colors within this distance are merged. The top 12 clusters become the palette.
- **Color classification**: Heuristic based on luminance (>240 = background, <30 = text) and dominant channel (R = warm accent, B = primary, G = success).
- **Website extraction**: Playwright iterates all DOM elements, collects `getComputedStyle()` values for color, font, spacing, shadow, and radius properties. These raw CSS values are then parsed and clustered.

### Dependencies

| Dependency | Required? | Purpose |
|------------|-----------|---------|
| Python 3.8+ | Yes | Runtime |
| Pillow | Optional | Image pixel analysis |
| Playwright + Chromium | Optional | Live website capture |
| Figma API token | Optional | Figma file extraction |

No dependencies are needed for demo mode — the analyzer includes realistic mock data.

### Model Calls

The standalone `analyzer.py` makes **zero LLM API calls**. All extraction is algorithmic. When used as a Claude Code skill, Claude itself acts as the vision model — it reads the SKILL.md instructions and uses its multimodal capabilities to visually analyze images, augmenting the algorithmic extraction with semantic understanding (e.g., identifying a component as a "card" vs. a "modal").

## Limitations

- **Image-only analysis** produces approximate colors only — no typography, spacing, or component detection without Claude's vision capabilities.
- **Color clustering** uses simple Euclidean distance in RGB, not perceptual color space (CIELAB). Visually distinct colors with similar RGB values may be merged.
- **Website capture** only sees computed styles, not design intent. A `16px` padding and a `1rem` padding both appear as `16px` — the semantic scale must be inferred.
- **Figma extraction** requires a personal access token and only retrieves file-level data via REST API. It does not extract Figma variables or design tokens natively defined in Figma.
- **Component detection** in algorithmic mode is basic — the mock data shows what Claude's vision can produce, but the standalone script cannot identify UI components from pixels alone.
- **No CSS variable mapping** — tokens are extracted as raw values, not mapped to existing CSS custom properties or Tailwind classes.

## Why This Matters

### For Claude-driven product builders

- **Lead-gen / marketing sites**: Point at a competitor's landing page, get a complete design system in 3 seconds. Rebuild or riff on it immediately with accurate tokens instead of eyeballing hex codes.
- **Ad creatives**: Extract brand colors and typography from a client's existing site to ensure ad designs match their visual identity. Feed tokens directly into ad template generation.
- **Agent factories**: Design extraction becomes a composable step in multi-agent pipelines. An agent that builds UIs can first run AnyDesign to understand the target aesthetic, then generate code that matches it.
- **White-label products**: Quickly extract a customer's design language from their existing product and apply it to your platform — automating the brand customization step.

### DTCG format advantage

The DTCG JSON output is compatible with tools like Style Dictionary, Tokens Studio, and Figma's native token format. This means extracted tokens can flow directly into a build pipeline without manual translation.
