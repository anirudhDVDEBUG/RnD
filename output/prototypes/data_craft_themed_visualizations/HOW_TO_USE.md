# How to Use Data Craft

## Install

```bash
# No external dependencies — uses Python 3.7+ stdlib only
git clone https://github.com/yixiliu617/data-craft.git
cd data-craft
```

## Run the demo

```bash
bash run.sh
```

This generates three HTML dashboards with different idiom/voice/theme combos into the current directory. Open any `.html` file in a browser.

## Use as a Claude Code Skill

1. Create the skill directory and copy the skill file:

```bash
mkdir -p ~/.claude/skills/data-craft
cp SKILL.md ~/.claude/skills/data-craft/SKILL.md
```

2. Trigger phrases that activate the skill:

- "Create a data visualization for this dataset"
- "Build a themed dashboard with charts"
- "Generate a beautiful data report from this CSV"
- "Visualize this data with ECharts"
- "Make an interactive HTML data display"

3. Optional parameters you can include in your prompt:

| Parameter | Options | Default |
|-----------|---------|---------|
| Visual Idiom | Executive Dashboard, Infographic, Analytical Report, Comparison Matrix, Timeline/Flow, Scorecard | Auto-selected |
| Voice | Analyst, Storyteller, Executive, Teacher, Journalist, Minimalist | Auto-selected |
| Theme | Any color description ("dark mode", "ocean blues", etc.) | Professional |

## First 60 seconds

**Input** (paste into Claude with the skill active):

> Here is our Q1 sales data:
> ```
> Quarter,Revenue,Units,NewCustomers
> Q1,245000,1200,89
> Q2,312000,1580,124
> Q3,287000,1340,102
> Q4,398000,1920,167
> ```
> Create an Executive Dashboard with a Journalist voice using a dark theme.

**Output:** A single self-contained HTML file (`sales_dashboard.html`) containing:
- 4 KPI cards with trend arrows (Total Revenue +18.2%, Avg Order +5.7%, etc.)
- Interactive bar chart comparing Revenue/Units/Customers by quarter
- Smooth line chart showing trends over time
- Donut chart breaking down revenue by category
- Journalist-style annotations ("BREAKING: Revenue peaked at $398K in Q4")
- Dark theme with responsive layout — works on desktop and mobile

Open the file in any browser. No server required.

## Programmatic usage

```python
from data_craft import DataCraftConfig, generate_html

config = DataCraftConfig(
    dataset_key="quarterly_sales",  # or provide custom data
    idiom="executive_dashboard",
    voice="journalist",
    theme="dark",
    output_file="my_dashboard.html",
)
html = generate_html(config)
with open("my_dashboard.html", "w") as f:
    f.write(html)
```
