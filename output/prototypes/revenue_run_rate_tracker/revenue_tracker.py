#!/usr/bin/env python3
"""Revenue Run-Rate Tracker — plot annualized run-rate revenue milestones."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# ── Data ────────────────────────────────────────────────────────────────
# Edit this dict to track a different company.
DATA = {
    "company": "Anthropic",
    "dates": [
        "2025-12-31",
        "2026-02-12",
        "2026-04-01",
        "2026-05-07",
    ],
    "revenues_bn": [9, 14, 30, 47],
    "sources": [
        "Series E follow-on (Dec 2025)",
        "Series F announcement",
        "Series G announcement",
        "Series H announcement — $47B run-rate",
    ],
}

OUTPUT_FILE = "run_rate_revenue.png"


def generate_chart(data: dict, output_path: str) -> None:
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in data["dates"]]
    revenues = data["revenues_bn"]
    company = data["company"]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Line + markers
    ax.plot(
        dates,
        revenues,
        marker="o",
        linewidth=2.5,
        markersize=9,
        color="#6366f1",
        zorder=3,
    )

    # Fill area under curve
    ax.fill_between(dates, revenues, alpha=0.08, color="#6366f1")

    # Annotate each data point
    for i, (d, r) in enumerate(zip(dates, revenues)):
        # Alternate annotation position to avoid overlap
        offset_y = 16 if i % 2 == 0 else -28
        va = "bottom" if offset_y > 0 else "top"
        ax.annotate(
            f"${r}B\n{d.strftime('%b %d, %Y')}",
            (d, r),
            textcoords="offset points",
            xytext=(0, offset_y),
            ha="center",
            va=va,
            fontsize=9,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#ccc", alpha=0.9),
        )

    # Axes formatting
    ax.set_title(
        f"{company} — Run-Rate Revenue",
        fontsize=16,
        fontweight="bold",
        pad=14,
    )
    ax.set_ylabel("Run-rate revenue ($B)", fontsize=12)
    ax.yaxis.set_major_formatter(lambda x, _: f"${x:.0f}B")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_ylim(bottom=0, top=max(revenues) * 1.25)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Footnote
    ax.text(
        0.5,
        -0.10,
        "Run-rate = most recent month's revenue x 12. Not actual annual revenue.",
        transform=ax.transAxes,
        ha="center",
        fontsize=8,
        color="#888",
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved to {output_path}")


def main():
    print(f"Generating run-rate revenue chart for {DATA['company']}...")
    generate_chart(DATA, OUTPUT_FILE)


if __name__ == "__main__":
    main()
