# How to Use AnyDesign Analyzer

## Installation

### As a Claude Code Skill (recommended)

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/anydesign_analyzer
   ```

2. Copy the SKILL.md file into it:
   ```bash
   cp SKILL.md ~/.claude/skills/anydesign_analyzer/SKILL.md
   ```

3. That's it. Claude Code will automatically detect and load the skill.

### For standalone use (optional)

```bash
# Clone or copy this directory
cd anydesign_analyzer

# No dependencies needed for demo mode
# For real image analysis, install Pillow:
pip install Pillow

# For real website capture, install Playwright:
pip install playwright
python -m playwright install chromium
```

## Trigger Phrases

Once the skill is installed, say any of these to Claude Code:

| Phrase | What happens |
|--------|-------------|
| "Analyze this design" | Analyzes an image/screenshot you provide |
| "Extract design tokens" | Pulls color, type, spacing tokens from a visual |
| "Generate design.md" | Produces the full structured output |
| "Reverse-engineer this UI" | Component inventory + reconstruction notes |
| "Create design system from [URL]" | Captures a live site via Playwright |

## First 60 Seconds

### Demo mode (no setup needed)

```bash
bash run.sh
```

This runs the analyzer with built-in mock data (a SaaS dashboard) and writes `design.md` to the current directory. Open it to see the full token system.

### With a real image

```bash
python3 analyzer.py screenshot.png -o design.md
```

Requires `Pillow`. The analyzer samples pixel colors, clusters them, and builds a palette.

### With a live website

```bash
python3 analyzer.py https://example.com -o design.md
```

Requires `playwright` with Chromium installed. Captures the page, extracts all computed CSS styles, and clusters them into tokens.

### With Figma

Set your Figma API token, then point Claude at a Figma URL:

```bash
export FIGMA_ACCESS_TOKEN=your_token_here
# Then tell Claude: "Extract design tokens from https://figma.com/file/..."
```

## Output

The generated `design.md` contains:

1. **Design Tokens** — Colors, typography, spacing, shadows, radii in table format
2. **DTCG JSON** — Machine-readable token block in the Design Token Community Group format
3. **Component Inventory** — Table of detected UI components with variants and token references
4. **Reconstruction Notes** — Layout strategy, breakpoints, framework hints, responsive approach

## File Placement

```
~/.claude/skills/
  anydesign_analyzer/
    SKILL.md          <-- The skill definition Claude reads
```

The skill tells Claude how to use Playwright, Pillow, and the Figma API to capture designs. The `analyzer.py` in this prototype is a standalone implementation of the same logic.
