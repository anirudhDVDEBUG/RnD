---
name: revenue_run_rate_tracker
description: |
  Track and visualize company run-rate revenue milestones over time using matplotlib.
  Triggers: "plot run-rate revenue", "chart revenue growth", "visualize financial milestones", "track revenue announcements"
---

# Revenue Run-Rate Tracker

Create clean line charts showing run-rate revenue growth from announcement data points.

## When to use

- "Plot run-rate revenue over time"
- "Chart this company's revenue growth from their announcements"
- "Visualize financial milestone data points"
- "Make a revenue trajectory chart from press releases"
- "Track annualized revenue run-rate"

## How to use

1. **Collect data points**: Gather date + run-rate revenue pairs from funding announcements, press releases, or earnings reports. Run-rate revenue is typically the most recent month's revenue multiplied by 12.

2. **Prepare the data**: Structure as two parallel lists — dates and revenue values in billions.

3. **Generate the chart** using this pattern:

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Example: Anthropic run-rate revenue milestones (2025-2026)
dates = [
    datetime(2025, 12, 31),
    datetime(2026, 2, 12),
    datetime(2026, 4, 1),
    datetime(2026, 5, 7),
]
revenues = [9, 14, 30, 47]  # in $bn

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(dates, revenues, marker='o', linewidth=2, markersize=8, color='#6366f1')

# Annotate each data point
for d, r in zip(dates, revenues):
    ax.annotate(
        f'${r}bn\n{d.strftime("%b %d, %Y")}',
        (d, r),
        textcoords='offset points',
        xytext=(0, 14),
        ha='center',
        fontsize=9,
    )

ax.set_title('Run-Rate Revenue', fontsize=16, fontweight='bold')
ax.set_ylabel('Run-rate revenue ($bn)', fontsize=12)
ax.yaxis.set_major_formatter(lambda x, _: f'${x:.0f}bn')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_ylim(bottom=0)
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('run_rate_revenue.png', dpi=150)
print('Chart saved to run_rate_revenue.png')
```

4. **Customize**: Replace the `dates` and `revenues` lists with the target company's data. Adjust colors, title, and annotations as needed.

5. **Interpret**: Run-rate revenue is an annualized projection, not actual annual revenue. It reflects current momentum but can be misleading if growth is uneven. Note this caveat when presenting the chart.

## Key concepts

- **Run-rate revenue**: Current monthly revenue × 12. Common in high-growth startups to signal trajectory between formal earnings reports.
- **Data sources**: Funding announcements (Series rounds), partnership press releases, and investor letters often disclose run-rate figures.

## References

- [Anthropic's run-rate revenue hits $47 billion — Simon Willison](https://simonwillison.net/2026/May/29/anthropic/#atom-everything)
- [Anthropic Series H announcement](https://www.anthropic.com/news/series-h)
- [Matplotlib documentation](https://matplotlib.org/)
