# How to Use — VisuAI Research Agent

## Install (Python 3.10+)

```bash
cd visuai_research_agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Dependencies: `pandas`, `numpy`, `plotly`, `kaleido` (for PNG export).

## One-command demo

```bash
bash run.sh
```

This generates a sample 200-row clinical-trial dataset, runs the 5-stage pipeline, and writes PNG + interactive HTML charts to `output/`.

## Using your own data

```bash
python main.py path/to/your_data.csv -o results/
```

Supports CSV, Excel (`.xlsx`), and JSON. The agent auto-detects column types, research domain, and best chart types.

## First 60 Seconds

```
$ bash run.sh

--- VisuAI Research Agent  |  Demo Run ---

[setup] Creating virtual environment ...
[setup] Installing dependencies ...
[data]  Generating sample clinical-trial dataset ...
Generated sample_clinical_trial.csv  (200 rows, 8 columns)

============================================================
  VisuAI Research Agent
============================================================

[1/5] Ingesting dataset ...
  Loaded 200 rows x 8 columns from sample_clinical_trial.csv

[2/5] Profiling data ...
  Numeric columns  : ['age', 'biomarker_baseline', 'biomarker_week12', 'survival_months']
  Categorical cols : ['patient_id', 'treatment', 'gender', 'response']
  Total missing    : 6

[3/5] Detecting research domain ...
  Domain: biomedical
  Palette: ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

[4/5] Recommending visualizations ...
  - histogram    | Distribution of age
  - histogram    | Distribution of biomarker_baseline
  - histogram    | Distribution of biomarker_week12
  - histogram    | Distribution of survival_months
  - scatter      | age vs biomarker_baseline
  - scatter      | biomarker_baseline vs biomarker_week12
  - box          | age by treatment
  - heatmap      | Correlation Matrix
  - bar          | Counts by treatment

[5/5] Rendering 9 visualizations to output/ ...
  [OK] fig_01_histogram  ->  PNG + HTML
  [OK] fig_02_histogram  ->  PNG + HTML
  ...
  [OK] fig_09_bar        ->  PNG + HTML

--- Summary Report ---
  Total files generated: 19
  Output directory: .../output

--- HTML files you can open in a browser: ---
output/fig_01_histogram.html
output/fig_02_histogram.html
...
```

Open any `.html` file in your browser for an interactive chart (zoom, hover tooltips, export).

## Integration as a Claude Skill

Drop the SKILL.md into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/visuai_research_agent
cp SKILL.md ~/.claude/skills/visuai_research_agent/SKILL.md
```

**Trigger phrases:**
- "Visualize this research dataset for a publication"
- "Generate interactive charts from my CSV research data"
- "Create publication-ready plots for my dataset"
- "Analyze my dataset and suggest the best visualization types"

## Customization

Pass your own data and output directory:

```bash
python main.py my_survey_data.csv -o survey_charts/
```

The agent automatically adapts:
- **Domain palette** — biomedical (blues/oranges), environmental (greens), economics (purples), etc.
- **Chart selection** — based on column types and cardinality
- **Labels & legends** — derived from column names
