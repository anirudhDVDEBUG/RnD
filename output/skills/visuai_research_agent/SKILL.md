---
name: visuai_research_agent
description: |
  An AI-powered autonomous agent that transforms raw research datasets into publication-ready, interactive visualizations tailored to your research domain, methodology, and audience.
  Triggers: research visualization, dataset visualization, interactive charts from data, publication-ready plots, research data analysis
---

# VisuAI Research Agent

Transform raw research datasets into publication-ready, interactive visualizations using an autonomous AI agent pipeline.

## When to use

- "Visualize this research dataset for a publication"
- "Generate interactive charts from my CSV/Excel research data"
- "Create publication-ready plots tailored to my research domain"
- "Analyze my dataset and suggest the best visualization types"
- "Turn this raw data into presentation-ready interactive visualizations"

## How to use

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/muhammadyasirimam/visuai-research-agent.git
cd visuai-research-agent

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare your dataset

Place your research dataset (CSV, Excel, JSON, or other tabular format) in the project directory or provide its path when prompted.

### 3. Run the agent

```bash
python main.py
```

The agent will:

1. **Ingest & Profile** — Load your dataset, detect column types, distributions, and missing values.
2. **Domain Detection** — Identify the research domain (biomedical, social science, engineering, etc.) to apply domain-appropriate visual conventions.
3. **Visualization Recommendation** — Suggest chart types (scatter, heatmap, violin, network graph, etc.) based on data structure, variable relationships, and audience.
4. **Rendering** — Generate interactive visualizations using libraries like Plotly, Matplotlib, Seaborn, or Altair.
5. **Export** — Output publication-ready figures (PNG, SVG, HTML) with proper labels, legends, and styling.

### 4. Customize

- Specify your target audience (journal reviewers, conference attendees, general public)
- Choose your preferred visualization libraries
- Set color palettes, themes, and export formats
- Define which variables to visualize and how

## Key Features

- **Autonomous pipeline**: End-to-end from raw data to finished charts
- **Domain-aware**: Adapts visual style to research field conventions
- **Interactive output**: Generates interactive HTML charts alongside static images
- **Publication-ready**: Proper axis labels, legends, annotations, and DPI settings
- **Multi-format export**: PNG, SVG, PDF, and interactive HTML

## References

- Source repository: [muhammadyasirimam/visuai-research-agent](https://github.com/muhammadyasirimam/visuai-research-agent)
- Topics: AI agents, dataset generation, research tools, visualization
