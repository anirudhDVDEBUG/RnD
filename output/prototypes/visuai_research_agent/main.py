#!/usr/bin/env python3
"""
VisuAI Research Agent — transforms raw research datasets into
publication-ready interactive visualizations.

Autonomous pipeline:
  1. Ingest & Profile    — load data, detect types, distributions, missing values
  2. Domain Detection    — classify research domain for visual conventions
  3. Viz Recommendation  — pick chart types from data structure
  4. Rendering           — generate interactive + static figures
  5. Export              — save PNG / HTML with proper labels & legends
"""

import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Step 1 — Ingest & Profile
# ---------------------------------------------------------------------------

def ingest(path: str) -> pd.DataFrame:
    """Load CSV, Excel, or JSON into a DataFrame."""
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(p)
    elif ext in (".xls", ".xlsx"):
        df = pd.read_excel(p)
    elif ext == ".json":
        df = pd.read_json(p)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return df


def profile(df: pd.DataFrame) -> dict:
    """Generate a data profile: types, missing, distributions."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include="datetime").columns.tolist()

    stats = {}
    for col in numeric_cols:
        stats[col] = {
            "type": "numeric",
            "mean": float(df[col].mean()),
            "std": float(df[col].std()) if len(df[col]) > 1 else 0.0,
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "missing": int(df[col].isna().sum()),
        }
    for col in categorical_cols:
        stats[col] = {
            "type": "categorical",
            "unique": int(df[col].nunique()),
            "top": str(df[col].mode().iloc[0]) if len(df[col].mode()) > 0 else None,
            "missing": int(df[col].isna().sum()),
        }
    for col in datetime_cols:
        stats[col] = {
            "type": "datetime",
            "min": str(df[col].min()),
            "max": str(df[col].max()),
            "missing": int(df[col].isna().sum()),
        }

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "datetime": datetime_cols,
        "column_stats": stats,
    }


# ---------------------------------------------------------------------------
# Step 2 — Domain Detection
# ---------------------------------------------------------------------------

DOMAIN_KEYWORDS = {
    "biomedical": ["gene", "protein", "patient", "dose", "survival", "clinical",
                   "treatment", "placebo", "biomarker", "cell", "tumor"],
    "social_science": ["survey", "respondent", "age", "gender", "income",
                       "education", "population", "region", "country"],
    "engineering": ["voltage", "current", "temperature", "pressure", "force",
                    "stress", "strain", "frequency", "signal"],
    "environmental": ["co2", "temperature", "precipitation", "species",
                      "habitat", "emission", "climate", "pollution"],
    "economics": ["gdp", "inflation", "unemployment", "price", "revenue",
                  "cost", "profit", "market", "stock"],
}

DOMAIN_PALETTES = {
    "biomedical": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    "social_science": ["#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#aec7e8"],
    "engineering": ["#393b79", "#5254a3", "#6b6ecf", "#9c9ede", "#637939"],
    "environmental": ["#2d6a4f", "#40916c", "#52b788", "#74c69d", "#95d5b2"],
    "economics": ["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"],
    "general": ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"],
}


def detect_domain(df: pd.DataFrame) -> str:
    """Score columns against keyword lists to classify domain."""
    cols_lower = [c.lower() for c in df.columns]
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords for c in cols_lower if kw in c)
        scores[domain] = score
    best = max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
    return best


# ---------------------------------------------------------------------------
# Step 3 — Visualization Recommendation
# ---------------------------------------------------------------------------

def recommend_visualizations(profile_info: dict, domain: str) -> list[dict]:
    """Return ordered list of recommended chart specs."""
    recs = []
    num = profile_info["numeric"]
    cat = profile_info["categorical"]
    n_rows = profile_info["rows"]

    # Distribution of each numeric column
    for col in num[:4]:  # cap at 4
        recs.append({
            "type": "histogram",
            "title": f"Distribution of {col}",
            "x": col,
            "reason": "Show spread and skewness of a numeric variable",
        })

    # Scatter for first two numeric pairs
    if len(num) >= 2:
        for i in range(min(len(num) - 1, 2)):
            recs.append({
                "type": "scatter",
                "title": f"{num[i]} vs {num[i+1]}",
                "x": num[i],
                "y": num[i + 1],
                "color": cat[0] if cat else None,
                "reason": "Reveal correlation between numeric variables",
            })

    # Box plots — numeric grouped by categorical
    if num and cat:
        recs.append({
            "type": "box",
            "title": f"{num[0]} by {cat[0]}",
            "x": cat[0],
            "y": num[0],
            "reason": "Compare distributions across categories",
        })

    # Correlation heatmap when >=3 numeric columns
    if len(num) >= 3:
        recs.append({
            "type": "heatmap",
            "title": "Correlation Matrix",
            "columns": num,
            "reason": "Identify multivariate relationships at a glance",
        })

    # Bar chart for categorical counts
    if cat:
        recs.append({
            "type": "bar",
            "title": f"Counts by {cat[0]}",
            "x": cat[0],
            "reason": "Summarise categorical distribution",
        })

    return recs


# ---------------------------------------------------------------------------
# Step 4 — Rendering
# ---------------------------------------------------------------------------

def render_all(df: pd.DataFrame, recs: list[dict], domain: str,
               out_dir: Path) -> list[str]:
    """Render each recommendation to PNG + HTML. Returns list of file paths."""
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio

    palette = DOMAIN_PALETTES.get(domain, DOMAIN_PALETTES["general"])
    outputs = []

    for i, spec in enumerate(recs):
        fig = None
        fname = f"fig_{i+1:02d}_{spec['type']}"

        if spec["type"] == "histogram":
            fig = px.histogram(
                df, x=spec["x"],
                title=spec["title"],
                color_discrete_sequence=palette,
                template="plotly_white",
            )

        elif spec["type"] == "scatter":
            kw = dict(x=spec["x"], y=spec["y"], title=spec["title"],
                      color_discrete_sequence=palette, template="plotly_white")
            if spec.get("color"):
                kw["color"] = spec["color"]
            fig = px.scatter(df, **kw)

        elif spec["type"] == "box":
            fig = px.box(
                df, x=spec["x"], y=spec["y"],
                title=spec["title"],
                color_discrete_sequence=palette,
                template="plotly_white",
            )

        elif spec["type"] == "heatmap":
            corr = df[spec["columns"]].corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns.tolist(),
                y=corr.columns.tolist(),
                colorscale="RdBu_r",
                zmin=-1, zmax=1,
            ))
            fig.update_layout(title=spec["title"], template="plotly_white")

        elif spec["type"] == "bar":
            counts = df[spec["x"]].value_counts().reset_index()
            counts.columns = [spec["x"], "count"]
            fig = px.bar(
                counts, x=spec["x"], y="count",
                title=spec["title"],
                color_discrete_sequence=palette,
                template="plotly_white",
            )

        if fig is None:
            continue

        # Style tweaks for publication readiness
        fig.update_layout(
            font=dict(family="Arial, sans-serif", size=13),
            margin=dict(l=60, r=30, t=50, b=50),
        )

        png_path = out_dir / f"{fname}.png"
        html_path = out_dir / f"{fname}.html"
        fig.write_image(str(png_path), width=900, height=550, scale=2)
        fig.write_html(str(html_path), include_plotlyjs="cdn")
        outputs.extend([str(png_path), str(html_path)])
        print(f"  [OK] {fname}  ->  PNG + HTML")

    return outputs


# ---------------------------------------------------------------------------
# Step 5 — Export & Report
# ---------------------------------------------------------------------------

def write_report(profile_info: dict, domain: str, recs: list[dict],
                 outputs: list[str], out_dir: Path):
    """Write a JSON summary report."""
    report = {
        "dataset_profile": {
            "rows": profile_info["rows"],
            "columns": profile_info["columns"],
            "numeric_vars": profile_info["numeric"],
            "categorical_vars": profile_info["categorical"],
        },
        "detected_domain": domain,
        "visualizations": [
            {"type": r["type"], "title": r["title"], "reason": r["reason"]}
            for r in recs
        ],
        "output_files": outputs,
    }
    report_path = out_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"  [OK] report.json")
    return report


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(dataset_path: str, out_dir: str = "output"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  VisuAI Research Agent")
    print("=" * 60)

    # 1. Ingest
    print("\n[1/5] Ingesting dataset ...")
    df = ingest(dataset_path)
    print(f"  Loaded {len(df)} rows x {len(df.columns)} columns from {dataset_path}")

    # 2. Profile
    print("\n[2/5] Profiling data ...")
    prof = profile(df)
    print(f"  Numeric columns  : {prof['numeric']}")
    print(f"  Categorical cols : {prof['categorical']}")
    missing_total = sum(s["missing"] for s in prof["column_stats"].values())
    print(f"  Total missing    : {missing_total}")

    # 3. Domain detection
    print("\n[3/5] Detecting research domain ...")
    domain = detect_domain(df)
    print(f"  Domain: {domain}")
    print(f"  Palette: {DOMAIN_PALETTES.get(domain, DOMAIN_PALETTES['general'])}")

    # 4. Recommend
    print("\n[4/5] Recommending visualizations ...")
    recs = recommend_visualizations(prof, domain)
    for r in recs:
        print(f"  - {r['type']:12s} | {r['title']}")

    # 5. Render
    print(f"\n[5/5] Rendering {len(recs)} visualizations to {out_dir}/ ...")
    outputs = render_all(df, recs, domain, out)

    # Report
    print("\n--- Summary Report ---")
    report = write_report(prof, domain, recs, outputs, out)
    print(f"\n  Total files generated: {len(outputs) + 1}")
    print(f"  Output directory: {out.resolve()}")
    print("=" * 60)
    print("  Done. Open any .html file in a browser for interactive charts.")
    print("=" * 60)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VisuAI Research Agent")
    parser.add_argument("dataset", help="Path to CSV/Excel/JSON dataset")
    parser.add_argument("-o", "--output", default="output",
                        help="Output directory (default: output)")
    args = parser.parse_args()
    run(args.dataset, args.output)
