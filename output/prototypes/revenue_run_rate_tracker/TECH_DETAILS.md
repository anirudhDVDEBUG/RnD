# Technical Details

## What it does

The revenue run-rate tracker takes a list of (date, revenue) pairs — typically extracted from funding announcements, press releases, or earnings reports — and produces a clean, annotated matplotlib line chart. "Run-rate revenue" means current monthly revenue multiplied by 12; it's the standard metric high-growth startups use to signal trajectory between formal earnings.

The script handles date parsing, axis formatting, data-point annotation, and chart styling in ~60 lines of Python. No API calls, no external data fetches — just structured input to visual output.

## Architecture

```
revenue_tracker.py    # Single-file implementation
  +-- DATA dict       # Company name, dates[], revenues_bn[]
  +-- generate_chart()  # matplotlib figure creation + annotation
  +-- main()          # Entry point, saves PNG

SKILL.md              # Claude Code skill definition
```

### Data flow

1. User provides date + revenue pairs (hardcoded or via Claude skill invocation)
2. `generate_chart()` converts ISO date strings to `datetime` objects
3. matplotlib plots the line with markers, annotates each point with value + date
4. Chart saved as PNG at 150 DPI

### Dependencies

- **matplotlib** — chart rendering (the only external dependency)
- Python 3.8+ standard library (`datetime`)

### No model calls

This skill does not call any LLM API. Claude Code uses the SKILL.md instructions to generate/adapt the Python code, then runs it locally. The skill is a template, not a service.

## Limitations

- **Manual data entry**: You must supply the date/revenue pairs yourself. There is no scraping or API integration to pull figures automatically.
- **Run-rate != actual revenue**: Run-rate extrapolates the latest month across a full year. It overstates if growth is front-loaded or seasonal.
- **Linear interpolation**: The chart connects points with straight lines. It doesn't model growth curves, confidence intervals, or projections.
- **Single company**: Each invocation charts one company. Comparison charts require manual modification.
- **No interactive output**: Produces a static PNG, not an interactive dashboard.

## Why this matters for Claude-driven products

- **Lead-gen / sales decks**: Instantly generate revenue trajectory visuals for prospect research or investor materials. Feed announcement URLs to Claude, have it extract figures and invoke this skill.
- **Marketing**: Turn funding-round press releases into shareable social graphics. "Anthropic just hit $47B run-rate" becomes a chart in seconds.
- **Agent factories**: This is a lightweight pattern for "data in, chart out" skills. The same structure works for tracking user growth, API call volumes, or ad spend — swap the DATA dict and title.
- **Financial analysis agents**: Combine with web-search or RSS-reading MCP servers to build an agent that monitors company announcements and auto-generates updated revenue charts.
