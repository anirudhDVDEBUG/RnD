---
name: Data Craft - Themed Data Visualizations
description: |
  Generate beautiful, themed data displays using six visual idioms and six narrative voices.
  Creates self-contained HTML files with ECharts-powered dashboards, reports, and data visualizations.
  Triggers: "create a data visualization", "build a themed dashboard", "generate a data report",
  "visualize this data beautifully", "make an ECharts display"
---

# Data Craft - Themed Data Visualizations

Generate beautiful, themed data displays with Claude. Six visual idioms, six voices, one skill.

## When to use

- "Create a data visualization for this dataset"
- "Build a themed dashboard with charts"
- "Generate a beautiful data report from this CSV"
- "Visualize this data with ECharts"
- "Make an interactive HTML data display"

## Visual Idioms

Choose from six distinct visual styles:

1. **Executive Dashboard** — Clean, corporate KPI panels with summary metrics and trend charts
2. **Infographic** — Story-driven, scroll-based visual narrative with bold colors and icons
3. **Analytical Report** — Dense, multi-chart layout for deep data exploration
4. **Comparison Matrix** — Side-by-side visual comparisons across categories or time periods
5. **Timeline / Flow** — Chronological or process-oriented data storytelling
6. **Scorecard** — Compact, at-a-glance metric cards with sparklines and status indicators

## Narrative Voices

Choose from six tones for the text and annotations:

1. **Analyst** — Precise, data-driven commentary with statistical observations
2. **Storyteller** — Narrative arc that guides the reader through insights
3. **Executive** — Bottom-line focused, action-oriented summaries
4. **Teacher** — Explanatory, breaking down what the data means and why
5. **Journalist** — Headline-driven, emphasizing newsworthy findings
6. **Minimalist** — Let the data speak; sparse labels, no fluff

## How to use

1. **Provide your data**: Share a CSV file, JSON data, a table, or describe the data you want visualized. The skill works with any structured data.

2. **Choose your idiom and voice** (optional): Specify a visual idiom (e.g., "Executive Dashboard") and a narrative voice (e.g., "Storyteller"). If not specified, the skill will select the best match for your data.

3. **Choose a color theme** (optional): Request a specific color palette or theme (e.g., "dark mode", "ocean blues", "corporate neutral"). Defaults to a clean, professional palette.

4. **Generate the output**: The skill produces a single self-contained HTML file that includes:
   - All CSS styles inlined
   - ECharts library loaded via CDN
   - Responsive layout that works on desktop and mobile
   - Interactive charts with tooltips, zoom, and filtering
   - Themed typography and color scheme throughout

5. **Open and share**: Open the HTML file in any browser. No server or dependencies required.

### Example prompt

> Here is our Q1 sales data (paste CSV). Create an Executive Dashboard with a Journalist voice using a dark theme.

### Output structure

The generated HTML file follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Report Title]</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>
    /* Themed CSS: layout, typography, colors */
  </style>
</head>
<body>
  <!-- Header with title and subtitle -->
  <!-- KPI / metric summary cards -->
  <!-- ECharts containers with responsive sizing -->
  <!-- Narrative annotations in chosen voice -->
  <!-- Footer with data source attribution -->
  <script>
    // ECharts initialization and configuration
    // Responsive resize handlers
  </script>
</body>
</html>
```

### Key guidelines

- Always use ECharts (v5+) for chart rendering
- Make the HTML fully self-contained — inline all CSS, use CDN for ECharts only
- Ensure responsive design with `window.addEventListener('resize', ...)`
- Apply the chosen visual idiom consistently across all layout elements
- Write annotations and labels in the chosen narrative voice
- Use semantic HTML and accessible color contrasts
- Include interactive features: tooltips, legend toggles, data zoom where appropriate

## References

- Source: [yixiliu617/data-craft](https://github.com/yixiliu617/data-craft) — Beautiful, themed data displays with Claude. Six visual idioms, six voices, one skill.
- [Apache ECharts Documentation](https://echarts.apache.org/en/index.html)
