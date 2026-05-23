# Technical Details

## What It Does

Awesome Amazon EC Skills is a modular toolkit for Amazon cross-border e-commerce sellers. It packages the most common seller workflows -- listing optimization, keyword research, PPC analysis, and 1688 sourcing evaluation -- as structured Python modules that can run standalone, integrate as Claude Code skills, or serve as an MCP server for live SP-API data. The design is Chinese-first (跨境电商 community), targeting sellers who source from 1688/Alibaba and sell on Amazon US/EU/JP.

Each module takes seller inputs (ASINs, keywords, campaign data, product specs) and produces structured analysis reports with actionable recommendations. In demo mode, all modules run against realistic mock data. In production, the MCP server layer connects to Amazon's SP-API for real-time order, inventory, advertising, and search term data.

## Architecture

```
amazon_ec/
  __init__.py
  listing_optimizer.py   # Title/bullet/keyword scoring & rewriting
  keyword_researcher.py  # Seed → expanded keyword list with metrics
  ppc_analyzer.py        # Campaign ACoS analysis & optimization
  sourcing_evaluator.py  # 1688 supplier comparison & landed cost calc
  mock_data.py           # Realistic mock datasets for all modules
  utils.py               # Shared scoring functions, formatters

run.sh                   # Runs all four modules end-to-end
SKILL.md                 # Claude Code skill definition
```

### Data Flow

1. **Input**: ASIN, seed keywords, campaign ID, or product description
2. **Processing**: Rule-based scoring (title length, keyword density, bullet structure) + heuristic analysis (ACoS thresholds, margin calculations, supplier scoring)
3. **Output**: Structured text report with scores, recommendations, and comparison tables

### Dependencies

- Python 3.9+ (standard library only for core modules)
- `tabulate` for formatted table output
- No ML models or LLM API calls in the analysis modules themselves -- they produce data that Claude interprets and acts on

### MCP Server (production path)

The MCP server (not included in this demo) wraps SP-API endpoints:
- `getListingItem` for catalog data
- `getSearchTermsReport` for keyword/PPC data
- `getOrders` / `getInventory` for operational data

## Limitations

- **Mock data only in demo**: No live Amazon or 1688 API calls without credentials
- **Scoring is heuristic**: Listing scores use rule-based heuristics (title length, keyword count, bullet structure), not trained models
- **No real search volume**: Keyword search volumes are simulated; real data requires SP-API or third-party tools (Helium 10, Jungle Scout)
- **1688 sourcing is template-based**: Supplier data is mocked; actual 1688 integration would need their open platform API
- **English/Chinese only**: Optimizations target US and CN marketplaces

## Why This Matters

For teams building Claude-driven products:

- **Lead-gen / marketing**: The listing optimizer pattern (score → rewrite → re-score) is directly reusable for ad copy, landing pages, and SEO content optimization
- **Agent factories**: Each module is a self-contained "skill" that Claude can invoke by name -- a clean pattern for building skill registries and agent orchestration
- **Ad creatives**: PPC analysis logic (ACoS optimization, negative keyword pruning, bid adjustment) maps to any paid media platform, not just Amazon
- **E-commerce automation**: The sourcing evaluator demonstrates a supplier-scoring pipeline that generalizes to any procurement workflow
