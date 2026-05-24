# Technical Details

## What it does

Data Craft is a Claude Code skill that generates self-contained HTML data visualizations. Given structured data (CSV, JSON, or tabular), it produces a single `.html` file with inlined CSS, ECharts v5 loaded via CDN, and responsive layouts. The skill combines a visual idiom (layout pattern), a narrative voice (text tone), and a color theme to create polished dashboards without any build tooling or server.

The core value is templated composition: each of the 6 idioms defines a layout structure (KPI cards, chart grids, flow sections), each of the 6 voices provides text templates for annotations/labels/summaries, and themes supply color palettes. These dimensions are independent, giving 6 x 6 x N possible outputs from the same data.

## Architecture

```
data_craft.py          # Main generator — all logic in one file
├── THEMES             # Color palette dicts (bg, accent, chart colors)
├── VOICE_TEMPLATES    # Text templates per voice (title prefix, insight style, etc.)
├── SAMPLE_DATASETS    # Built-in demo data (quarterly sales, web analytics)
├── generate_*_config  # ECharts option builders (bar, line, pie)
├── generate_kpi_cards # HTML builder for metric cards
└── generate_html()    # Assembles full HTML document from config
```

**Data flow:**
1. User provides data + optional idiom/voice/theme selection
2. `DataCraftConfig` captures the parameters
3. `generate_html()` selects theme colors, voice templates, and builds ECharts configs
4. Chart configs are serialized as inline JavaScript objects
5. Output is a single HTML string written to a file

**Dependencies:** Python stdlib only (`json`, `os`, `sys`, `dataclasses`). ECharts v5 loaded via CDN at runtime in the browser.

**Key files:**
- `data_craft.py` — Complete generator (single file, ~300 lines)
- `run.sh` — Demo runner, generates 3 example dashboards
- `SKILL.md` — Claude Code skill definition with trigger phrases

## Limitations

- **CDN dependency:** Generated HTML requires internet access to load ECharts from `cdn.jsdelivr.net`. Offline use requires bundling the ECharts library.
- **Idiom differentiation is partial:** The current prototype applies the same layout structure across all idioms. A production version would need distinct HTML templates per idiom (e.g., timeline layout vs. comparison matrix).
- **No CSV/JSON parsing:** The demo uses hardcoded sample data. When used as a Claude Skill, Claude itself handles parsing user-provided data — the skill just defines the output format.
- **No data transformation:** Aggregation, filtering, and statistical analysis must be done by Claude before generating the visualization.
- **Single-page only:** Cannot generate multi-page reports or linked dashboards.

## Why it matters

For teams building Claude-driven products:

- **Lead-gen / marketing:** Generate branded data reports from CRM exports. Combine with a voice (Executive for C-suite, Journalist for press kits) to match the audience.
- **Ad creatives:** Produce data-backed infographics as standalone HTML — embed in emails or landing pages without infrastructure.
- **Agent factories:** Drop the skill into any Claude Code agent that handles data. The agent can autonomously select the right idiom/voice for the context.
- **Voice AI integration:** Pair with a voice agent that describes data — the visualization becomes the visual counterpart to spoken insights.
