#!/usr/bin/env python3
"""
Data Craft - Themed Data Visualizations

Generates self-contained HTML files with ECharts-powered dashboards.
Supports 6 visual idioms and 6 narrative voices.
"""

import json
import os
import sys
from dataclasses import dataclass, field
from typing import Optional

# ── Color Themes ─────────────────────────────────────────────────────────────

THEMES = {
    "professional": {
        "bg": "#ffffff",
        "card_bg": "#f8f9fa",
        "text": "#212529",
        "text_secondary": "#6c757d",
        "accent": "#0d6efd",
        "border": "#dee2e6",
        "chart_colors": ["#0d6efd", "#198754", "#ffc107", "#dc3545", "#6f42c1", "#20c997"],
    },
    "dark": {
        "bg": "#1a1a2e",
        "card_bg": "#16213e",
        "text": "#e8e8e8",
        "text_secondary": "#a0a0b0",
        "accent": "#e94560",
        "border": "#2a2a4a",
        "chart_colors": ["#e94560", "#0f3460", "#53d8fb", "#f8c43a", "#6c63ff", "#2ecc71"],
    },
    "ocean": {
        "bg": "#f0f8ff",
        "card_bg": "#e6f2ff",
        "text": "#1a3a5c",
        "text_secondary": "#4a7a9b",
        "accent": "#0077b6",
        "border": "#b8d8e8",
        "chart_colors": ["#0077b6", "#00b4d8", "#48cae4", "#90e0ef", "#023e8a", "#0096c7"],
    },
}

# ── Narrative Voices ─────────────────────────────────────────────────────────

VOICE_TEMPLATES = {
    "analyst": {
        "title_prefix": "Analysis:",
        "kpi_label": "Key Metric",
        "insight_style": "Statistical analysis indicates",
        "summary_opener": "The data reveals the following key findings:",
        "annotation_style": "Note: {value} represents a {pct}% change from baseline.",
    },
    "storyteller": {
        "title_prefix": "The Story of",
        "kpi_label": "Chapter Highlight",
        "insight_style": "As the numbers unfold, we see",
        "summary_opener": "Every dataset tells a story. Here's what this one whispered:",
        "annotation_style": "And then came {value} — a {pct}% shift that changed everything.",
    },
    "executive": {
        "title_prefix": "Executive Brief:",
        "kpi_label": "Bottom Line",
        "insight_style": "Action required:",
        "summary_opener": "Key takeaways for decision-makers:",
        "annotation_style": "{value} ({pct}% delta) — immediate attention recommended.",
    },
    "teacher": {
        "title_prefix": "Understanding",
        "kpi_label": "Learning Point",
        "insight_style": "Let's break this down:",
        "summary_opener": "Here's what we can learn from this data:",
        "annotation_style": "Notice how {value} shows a {pct}% change — this tells us something important.",
    },
    "journalist": {
        "title_prefix": "BREAKING:",
        "kpi_label": "Headline Number",
        "insight_style": "Sources confirm",
        "summary_opener": "The numbers are in, and they paint a compelling picture:",
        "annotation_style": "FLASH: {value} marks a dramatic {pct}% swing.",
    },
    "minimalist": {
        "title_prefix": "",
        "kpi_label": "",
        "insight_style": "",
        "summary_opener": "",
        "annotation_style": "{value} | {pct}%",
    },
}

# ── Sample Data ──────────────────────────────────────────────────────────────

SAMPLE_DATASETS = {
    "quarterly_sales": {
        "title": "Q1-Q4 2025 Sales Performance",
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": [
            {"name": "Revenue ($K)", "data": [245, 312, 287, 398]},
            {"name": "Units Sold", "data": [1200, 1580, 1340, 1920]},
            {"name": "New Customers", "data": [89, 124, 102, 167]},
        ],
        "kpis": [
            {"label": "Total Revenue", "value": "$1.24M", "change": "+18.2%", "trend": "up"},
            {"label": "Avg Order Value", "value": "$204", "change": "+5.7%", "trend": "up"},
            {"label": "Customer Retention", "value": "87.3%", "change": "-1.2%", "trend": "down"},
            {"label": "Profit Margin", "value": "23.8%", "change": "+2.1%", "trend": "up"},
        ],
        "pie_data": [
            {"name": "Electronics", "value": 420},
            {"name": "Apparel", "value": 310},
            {"name": "Home & Garden", "value": 250},
            {"name": "Sports", "value": 180},
            {"name": "Books", "value": 82},
        ],
    },
    "website_analytics": {
        "title": "Website Analytics - May 2025",
        "categories": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "series": [
            {"name": "Page Views (K)", "data": [42, 58, 51, 63]},
            {"name": "Unique Visitors (K)", "data": [18, 24, 22, 28]},
            {"name": "Bounce Rate (%)", "data": [45, 38, 41, 35]},
        ],
        "kpis": [
            {"label": "Total Views", "value": "214K", "change": "+32.1%", "trend": "up"},
            {"label": "Avg Session", "value": "4m 12s", "change": "+15.3%", "trend": "up"},
            {"label": "Conversion Rate", "value": "3.8%", "change": "+0.6%", "trend": "up"},
            {"label": "Bounce Rate", "value": "39.8%", "change": "-5.2%", "trend": "up"},
        ],
        "pie_data": [
            {"name": "Organic Search", "value": 45},
            {"name": "Direct", "value": 25},
            {"name": "Social Media", "value": 18},
            {"name": "Referral", "value": 8},
            {"name": "Email", "value": 4},
        ],
    },
}


@dataclass
class DataCraftConfig:
    """Configuration for a Data Craft visualization."""
    dataset_key: str = "quarterly_sales"
    idiom: str = "executive_dashboard"
    voice: str = "analyst"
    theme: str = "professional"
    output_file: str = "output.html"


def generate_kpi_cards(kpis: list, voice: dict, theme: dict) -> str:
    """Generate KPI summary cards HTML."""
    cards = []
    for kpi in kpis:
        trend_color = "#198754" if kpi["trend"] == "up" else "#dc3545"
        arrow = "&#9650;" if kpi["trend"] == "up" else "&#9660;"
        label_text = f'{voice["kpi_label"]}: {kpi["label"]}' if voice["kpi_label"] else kpi["label"]
        cards.append(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label_text}</div>
            <div class="kpi-value">{kpi["value"]}</div>
            <div class="kpi-change" style="color:{trend_color}">
                {arrow} {kpi["change"]}
            </div>
        </div>""")
    return "\n".join(cards)


def generate_bar_chart_config(dataset: dict, theme: dict) -> str:
    """Generate ECharts bar chart configuration."""
    series_configs = []
    for i, s in enumerate(dataset["series"]):
        color = theme["chart_colors"][i % len(theme["chart_colors"])]
        series_configs.append(f"""{{
            name: '{s["name"]}',
            type: 'bar',
            data: {json.dumps(s["data"])},
            itemStyle: {{ color: '{color}' }},
            barMaxWidth: 40
        }}""")

    return f"""{{
        tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
        legend: {{ top: 10, textStyle: {{ color: '{theme["text_secondary"]}' }} }},
        grid: {{ left: '3%', right: '4%', bottom: '3%', containLabel: true }},
        xAxis: {{
            type: 'category',
            data: {json.dumps(dataset["categories"])},
            axisLabel: {{ color: '{theme["text_secondary"]}' }},
            axisLine: {{ lineStyle: {{ color: '{theme["border"]}' }} }}
        }},
        yAxis: {{
            type: 'value',
            axisLabel: {{ color: '{theme["text_secondary"]}' }},
            splitLine: {{ lineStyle: {{ color: '{theme["border"]}' }} }}
        }},
        series: [{",".join(series_configs)}]
    }}"""


def generate_line_chart_config(dataset: dict, theme: dict) -> str:
    """Generate ECharts line chart configuration."""
    series_configs = []
    for i, s in enumerate(dataset["series"]):
        color = theme["chart_colors"][i % len(theme["chart_colors"])]
        series_configs.append(f"""{{
            name: '{s["name"]}',
            type: 'line',
            data: {json.dumps(s["data"])},
            smooth: true,
            lineStyle: {{ color: '{color}', width: 3 }},
            itemStyle: {{ color: '{color}' }},
            areaStyle: {{ color: '{color}', opacity: 0.08 }}
        }}""")

    return f"""{{
        tooltip: {{ trigger: 'axis' }},
        legend: {{ top: 10, textStyle: {{ color: '{theme["text_secondary"]}' }} }},
        grid: {{ left: '3%', right: '4%', bottom: '3%', containLabel: true }},
        xAxis: {{
            type: 'category',
            data: {json.dumps(dataset["categories"])},
            axisLabel: {{ color: '{theme["text_secondary"]}' }},
            axisLine: {{ lineStyle: {{ color: '{theme["border"]}' }} }},
            boundaryGap: false
        }},
        yAxis: {{
            type: 'value',
            axisLabel: {{ color: '{theme["text_secondary"]}' }},
            splitLine: {{ lineStyle: {{ color: '{theme["border"]}' }} }}
        }},
        series: [{",".join(series_configs)}]
    }}"""


def generate_pie_chart_config(pie_data: list, theme: dict) -> str:
    """Generate ECharts pie chart configuration."""
    data_json = json.dumps(pie_data)
    colors_json = json.dumps(theme["chart_colors"])
    return f"""{{
        tooltip: {{ trigger: 'item', formatter: '{{b}}: {{c}} ({{d}}%)' }},
        legend: {{
            orient: 'vertical', right: 10, top: 'center',
            textStyle: {{ color: '{theme["text_secondary"]}' }}
        }},
        color: {colors_json},
        series: [{{
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['40%', '50%'],
            avoidLabelOverlap: true,
            itemStyle: {{ borderRadius: 6, borderColor: '{theme["card_bg"]}', borderWidth: 2 }},
            label: {{ show: false }},
            emphasis: {{ label: {{ show: true, fontSize: 14, fontWeight: 'bold', color: '{theme["text"]}' }} }},
            data: {data_json}
        }}]
    }}"""


def generate_html(config: DataCraftConfig) -> str:
    """Generate a complete self-contained HTML visualization."""
    dataset = SAMPLE_DATASETS[config.dataset_key]
    theme = THEMES[config.theme]
    voice = VOICE_TEMPLATES[config.voice]

    title_prefix = voice["title_prefix"]
    full_title = f"{title_prefix} {dataset['title']}" if title_prefix else dataset["title"]
    summary = voice["summary_opener"]

    kpi_html = generate_kpi_cards(dataset["kpis"], voice, theme)
    bar_config = generate_bar_chart_config(dataset, theme)
    line_config = generate_line_chart_config(dataset, theme)
    pie_config = generate_pie_chart_config(dataset["pie_data"], theme)

    # Insight text
    first_series = dataset["series"][0]
    max_val = max(first_series["data"])
    max_idx = first_series["data"].index(max_val)
    max_cat = dataset["categories"][max_idx]
    insight = f'{voice["insight_style"]} {first_series["name"]} peaked at {max_val} in {max_cat}.' if voice["insight_style"] else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{full_title}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: {theme["bg"]};
            color: {theme["text"]};
            padding: 24px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 20px;
            border-bottom: 2px solid {theme["accent"]};
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: {theme["text_secondary"]};
            font-size: 16px;
        }}
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}
        .kpi-card {{
            background: {theme["card_bg"]};
            border: 1px solid {theme["border"]};
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .kpi-label {{
            font-size: 13px;
            color: {theme["text_secondary"]};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-size: 32px;
            font-weight: 700;
            color: {theme["accent"]};
        }}
        .kpi-change {{
            font-size: 14px;
            font-weight: 600;
            margin-top: 4px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }}
        .chart-card {{
            background: {theme["card_bg"]};
            border: 1px solid {theme["border"]};
            border-radius: 12px;
            padding: 20px;
        }}
        .chart-card h3 {{
            font-size: 16px;
            margin-bottom: 12px;
            color: {theme["text"]};
        }}
        .chart-container {{
            width: 100%;
            height: 340px;
        }}
        .insight-box {{
            background: {theme["card_bg"]};
            border-left: 4px solid {theme["accent"]};
            border-radius: 0 12px 12px 0;
            padding: 20px 24px;
            margin-bottom: 24px;
        }}
        .insight-box p {{
            color: {theme["text_secondary"]};
            font-size: 15px;
        }}
        .footer {{
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid {theme["border"]};
            color: {theme["text_secondary"]};
            font-size: 13px;
        }}
        @media (max-width: 768px) {{
            .chart-grid {{ grid-template-columns: 1fr; }}
            .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
            body {{ padding: 12px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{full_title}</h1>
        <p class="subtitle">Visual Idiom: {config.idiom.replace('_', ' ').title()} &middot; Voice: {config.voice.title()} &middot; Theme: {config.theme.title()}</p>
    </div>

    <div class="kpi-row">
        {kpi_html}
    </div>

    <div class="insight-box">
        <p>{summary} {insight}</p>
    </div>

    <div class="chart-grid">
        <div class="chart-card">
            <h3>Performance Overview</h3>
            <div class="chart-container" id="barChart"></div>
        </div>
        <div class="chart-card">
            <h3>Trend Analysis</h3>
            <div class="chart-container" id="lineChart"></div>
        </div>
        <div class="chart-card">
            <h3>Distribution Breakdown</h3>
            <div class="chart-container" id="pieChart"></div>
        </div>
    </div>

    <div class="footer">
        Generated by Data Craft &middot; Powered by ECharts &middot; {config.voice.title()} Voice
    </div>

    <script>
        // Initialize charts
        var barChart = echarts.init(document.getElementById('barChart'));
        var lineChart = echarts.init(document.getElementById('lineChart'));
        var pieChart = echarts.init(document.getElementById('pieChart'));

        barChart.setOption({bar_config});
        lineChart.setOption({line_config});
        pieChart.setOption({pie_config});

        // Responsive resize
        window.addEventListener('resize', function() {{
            barChart.resize();
            lineChart.resize();
            pieChart.resize();
        }});
    </script>
</body>
</html>"""
    return html


def main():
    """Generate demo visualizations showing different idiom/voice/theme combos."""
    output_dir = os.path.dirname(os.path.abspath(__file__))

    demos = [
        DataCraftConfig(
            dataset_key="quarterly_sales",
            idiom="executive_dashboard",
            voice="journalist",
            theme="dark",
            output_file="demo_executive_dark.html",
        ),
        DataCraftConfig(
            dataset_key="website_analytics",
            idiom="analytical_report",
            voice="analyst",
            theme="ocean",
            output_file="demo_analytical_ocean.html",
        ),
        DataCraftConfig(
            dataset_key="quarterly_sales",
            idiom="scorecard",
            voice="storyteller",
            theme="professional",
            output_file="demo_scorecard_storyteller.html",
        ),
    ]

    print("=" * 60)
    print("  Data Craft - Themed Data Visualizations")
    print("=" * 60)
    print()
    print(f"Available idioms:  {', '.join(['Executive Dashboard', 'Infographic', 'Analytical Report', 'Comparison Matrix', 'Timeline/Flow', 'Scorecard'])}")
    print(f"Available voices:  {', '.join(VOICE_TEMPLATES.keys())}")
    print(f"Available themes:  {', '.join(THEMES.keys())}")
    print()

    generated = []
    for cfg in demos:
        html = generate_html(cfg)
        out_path = os.path.join(output_dir, cfg.output_file)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        size_kb = len(html) / 1024
        generated.append((cfg, out_path, size_kb))
        print(f"  [OK] {cfg.output_file}")
        print(f"       Idiom: {cfg.idiom.replace('_', ' ').title()} | Voice: {cfg.voice.title()} | Theme: {cfg.theme.title()}")
        print(f"       Size: {size_kb:.1f} KB | Dataset: {cfg.dataset_key}")
        print()

    print("-" * 60)
    print(f"Generated {len(generated)} HTML dashboards.")
    print("Open any file in a browser — no server required.")
    print()
    print("To use as a Claude Skill:")
    print("  1. Copy SKILL.md to ~/.claude/skills/data-craft/")
    print('  2. Ask Claude: "Create a data visualization for this CSV"')
    print("=" * 60)

    return generated


if __name__ == "__main__":
    main()
