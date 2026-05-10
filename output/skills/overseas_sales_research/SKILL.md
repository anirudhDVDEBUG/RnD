---
name: overseas_sales_research
description: |
  Conduct structured overseas sales company research producing a standardized "Five Perspectives, Six Decisions" (五看六定) report. Covers company overview, market landscape, competitive analysis, channel evaluation, and strategic recommendations for B2B cross-border sales scenarios.
  Triggers: overseas sales research, company due diligence for international sales, export market research, 海外销售调研, B2B prospect research report
---

# Overseas Sales Research Skill

Generate a comprehensive overseas sales research report in ~30 minutes using the "Five Perspectives, Six Decisions" (五看六定) framework — suitable for client visits, distributor due diligence, competitive analysis, new market entry, and job interview preparation.

## When to use

- "Research this overseas company before our sales visit"
- "Do due diligence on a potential international distributor"
- "Generate a competitor analysis report for this foreign market"
- "Help me prepare a 五看六定 report for market entry"
- "Analyze this company as a B2B sales prospect"

## How to use

### Step 1 — Gather inputs

Ask the user for:
- **Target company name** and website URL
- **Industry / product category**
- **Research purpose**: client visit prep, distributor evaluation, competitive analysis, new market entry, or interview prep
- **Target market / region** (e.g., Southeast Asia, Europe, Latin America)
- **Language preference** for the report (Chinese 中文 or English, default: Chinese)

### Step 2 — Five Perspectives (五看) research

Use web search to investigate and compile findings on each perspective:

1. **看行业 (Industry View)** — Market size, growth rate, key trends, regulatory environment, and industry lifecycle stage in the target region.
2. **看市场 (Market View)** — Target market segmentation, customer profiles, demand drivers, purchasing behavior, and seasonal patterns.
3. **看竞争 (Competition View)** — Top 3-5 competitors, their market share, pricing strategies, channel structures, strengths and weaknesses.
4. **看客户 (Customer View)** — Target company profile: founding year, revenue scale, product lines, organizational structure, key decision-makers, recent news.
5. **看自身 (Self View)** — SWOT positioning: how the user's offering compares, potential value propositions, differentiation angles.

### Step 3 — Six Decisions (六定) strategic recommendations

Based on the research, provide actionable recommendations:

1. **定目标 (Set Objectives)** — Recommended sales targets and KPIs for this market/account.
2. **定策略 (Set Strategy)** — Go-to-market approach: direct sales, distributor model, or hybrid.
3. **定市场 (Set Market)** — Priority sub-segments or regions to focus on first.
4. **定打法 (Set Tactics)** — Concrete sales plays: pricing approach, demo strategy, POC plan.
5. **定资源 (Set Resources)** — Required team, budget, and timeline estimates.
6. **定节奏 (Set Cadence)** — Phased execution plan with milestones (30/60/90 day).

### Step 4 — Compile the report

Write the final report as a Markdown file with:
- Executive summary (1 paragraph)
- Five Perspectives sections with data tables where appropriate
- Six Decisions section with clear, actionable bullet points
- Risk factors and mitigation strategies
- Appendix: source links and data references

Save the report as `overseas_sales_research_<company>_<date>.md` in the current working directory.

### Step 5 — Review and refine

Present the report summary to the user and ask:
- Are there specific sections to expand?
- Any internal data or context to incorporate?
- Preferred format adjustments (slides outline, executive brief, etc.)?

## Output format

The report follows this structure:

```
# 海外销售调研报告 / Overseas Sales Research Report
## Target: [Company Name]
## Date: [YYYY-MM-DD]
## Purpose: [Research Purpose]

### Executive Summary
### 一、看行业 — Industry View
### 二、看市场 — Market View  
### 三、看竞争 — Competition View
### 四、看客户 — Customer View
### 五、看自身 — Self View
### 六、战略建议 — Six Decisions
#### 1. 定目标 — Objectives
#### 2. 定策略 — Strategy
#### 3. 定市场 — Market Focus
#### 4. 定打法 — Tactics
#### 5. 定资源 — Resources
#### 6. 定节奏 — Cadence
### Risk Assessment
### Appendix & Sources
```

## References

- Source repository: https://github.com/xxyshawn-creator/claude-skill-overseas-sales-research
- Framework: 五看六定 (Five Perspectives, Six Decisions) — a structured B2B sales research methodology for cross-border commerce
