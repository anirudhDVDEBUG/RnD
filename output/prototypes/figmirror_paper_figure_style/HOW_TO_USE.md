# How to Use FigMirror Paper Figure Style

## Install

```bash
pip install matplotlib numpy pandas seaborn Pillow
```

No external API keys required for the demo.

## Run the Demo

```bash
bash run.sh
```

This generates:
- `reference_figure.png` — a synthetic "paper figure" to replicate
- `output_figure.png` / `output_figure.pdf` — your data plotted in the same style
- Console output showing the extracted style attributes

## Use as a Claude Skill

### 1. Drop the skill file

```bash
mkdir -p ~/.claude/skills/figmirror_paper_figure_style
cp SKILL.md ~/.claude/skills/figmirror_paper_figure_style/SKILL.md
```

### 2. Trigger phrases

Say any of these to Claude Code:

- "match this paper's figure style"
- "replicate figure style"
- "plot like this paper"
- "figmirror"
- "mirror figure style"
- "scientific figure replication"
- "paper figure styling"

### 3. What Claude will do

1. Ask for your reference figure (image/PDF) and data file (CSV/JSON)
2. Analyze the reference figure's visual style (colors, fonts, markers, layout)
3. Generate a self-contained matplotlib script
4. Run it, show you the result, and iterate until you're satisfied

## First 60 Seconds

**Input:**
```
You: "Plot my data like this paper's figure" [attach reference_figure.png + sample_data.csv]
```

**What happens:**
```
Claude analyzes reference_figure.png:
  → Chart type: line
  → Colors: #2166ac, #b2182b, #4dac26, #e08214
  → Font: serif, 14pt bold title
  → Grid: dashed, alpha=0.3
  → Markers: circle, square, triangle, diamond

Claude generates figmirror_output.py, runs it:
  → output_figure.png (300 DPI)
  → output_figure.pdf (vector)
```

**Output:** A publication-ready figure with your data styled exactly like the reference.

## Custom Usage (Without Claude Skill)

```bash
# Generate a reference figure (or use your own)
python generate_reference.py

# Apply its style to your data
python figmirror_demo.py reference_style.json your_data.csv my_output
```

Arguments:
1. Style JSON file (extracted from reference analysis)
2. CSV data file
3. Output filename prefix (produces `.png` + `.pdf`)
