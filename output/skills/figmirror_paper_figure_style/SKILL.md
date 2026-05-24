---
name: figmirror_paper_figure_style
description: |
  Replicate the visual style of any scientific paper figure onto your own data using AI-driven analysis and matplotlib code generation.
  Triggers: "match this paper's figure style", "replicate figure style", "plot like this paper", "figmirror", "mirror figure style", "scientific figure replication", "paper figure styling"
---

# FigMirror: Paper Figure Style Replication

An AI agent skill that analyzes the visual style of figures from scientific papers and generates matplotlib code to plot your own data in the same style.

## When to use

- "Replicate the style of this paper's figure with my data"
- "Plot my data to match the figure style from this PDF/image"
- "Mirror the figure style from this research paper"
- "Generate a chart that looks like Figure 3 from this paper"
- "Create a publication-quality plot matching this reference figure"

## How to use

### Step 1: Gather Inputs

Collect from the user:
1. **Reference figure** — an image file (PNG, JPG, PDF screenshot) of the target paper figure whose style to replicate
2. **User data** — a CSV, JSON, or other data file containing the data to plot
3. **Optional context** — any specific style preferences, axis labels, or legend text

### Step 2: Analyze the Reference Figure

Examine the reference figure and extract visual style attributes:
- **Chart type**: line, bar, scatter, heatmap, box plot, violin, area, etc.
- **Color palette**: exact colors used for data series, background, gridlines
- **Typography**: font family, sizes for title/axis labels/tick labels/legend
- **Layout**: subplot arrangement, aspect ratio, margins, spacing
- **Line/marker styles**: line widths, marker shapes/sizes, dash patterns
- **Axes**: scale (linear/log), tick formatting, grid style, spine visibility
- **Legend**: position, frame, font size, column layout
- **Annotations**: arrows, text boxes, shaded regions, reference lines

Document these attributes in a structured style specification.

### Step 3: Generate Matplotlib Code

Write a self-contained Python script that:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

# Load user data
data = pd.read_csv("user_data.csv")  # adapt to actual format

# Apply extracted style settings
plt.rcParams.update({
    'font.family': 'serif',           # match paper font
    'font.size': 10,                   # match paper font size
    'axes.linewidth': 0.8,             # match axis line weight
    'axes.grid': True,                 # match grid visibility
    'grid.alpha': 0.3,                 # match grid opacity
    'figure.figsize': (7, 5),          # match aspect ratio
    'figure.dpi': 300,                 # publication quality
})

# Define color palette extracted from reference
colors = ['#2166ac', '#b2182b', '#4dac26', '#e08214']  # example

fig, ax = plt.subplots()

# Plot data matching the reference chart type and style
# ... (adapt to actual chart type)

ax.set_xlabel('X Label', fontsize=11)
ax.set_ylabel('Y Label', fontsize=11)
ax.set_title('Title', fontsize=13, fontweight='bold')
ax.legend(frameon=True, fontsize=9)

plt.tight_layout()
plt.savefig('output_figure.png', dpi=300, bbox_inches='tight')
plt.savefig('output_figure.pdf', bbox_inches='tight')
plt.show()
```

### Step 4: Iterate and Refine

1. Run the generated script and display the output figure
2. Compare side-by-side with the reference figure
3. Adjust colors, spacing, fonts, and other style details to improve fidelity
4. Repeat until the user is satisfied with the style match

### Key Principles

- **Pixel-level fidelity**: Match colors by extracting hex values from the reference image
- **Publication-ready output**: Always save at 300+ DPI with tight bounding boxes
- **Dual format**: Save both PNG (for preview) and PDF (for publication)
- **Self-contained scripts**: All generated code should run independently with standard Python scientific stack
- **Preserve data integrity**: Never distort or misrepresent the user's actual data values; only the visual styling is mirrored

### Dependencies

Ensure these Python packages are installed:
```bash
pip install matplotlib numpy pandas seaborn
```

Optional for advanced figure analysis:
```bash
pip install Pillow scikit-image
```

## References

- Source repository: https://github.com/VILA-Lab/FigMirror
- Description: An Automated AI Agent Tool for Plotting Your Data in Any Paper's Figure Style
- Topics: data-visualization, scientific-plotting, matplotlib, python, research-tools
