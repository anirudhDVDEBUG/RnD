# Quarterly Product Report

**Acme Corp** | Q1 2026

---

## Executive Summary

Revenue grew **23%** year-over-year, driven by strong adoption of our
AI-powered analytics platform. Customer retention remained above 94%.

---

## Key Metrics

| Metric              | Q4 2025   | Q1 2026   | Change  |
|----------------------|-----------|-----------|---------|
| Monthly Active Users | 12,400    | 15,200    | +22.6%  |
| Revenue (USD)        | $2.1M     | $2.6M     | +23.8%  |
| Churn Rate           | 5.8%      | 5.2%      | -0.6pp  |
| NPS Score            | 62        | 68        | +6      |

## Product Highlights

### New Features Shipped

1. **Smart Dashboards** - Auto-generated insights from raw data
2. **Voice Query** - Ask questions in natural language
3. **Export API** - Programmatic access to all report types

### Architecture Overview

```python
class ReportPipeline:
    def __init__(self, data_source):
        self.source = data_source
        self.transforms = []

    def add_transform(self, fn):
        self.transforms.append(fn)
        return self

    def execute(self):
        data = self.source.fetch()
        for t in self.transforms:
            data = t(data)
        return data
```

## Roadmap

- [x] Multi-tenant support
- [x] SSO integration
- [ ] Real-time collaboration
- [ ] Mobile app (beta in Q2)

---

## Next Steps

> Focus on reducing onboarding friction and expanding into the
> European market. Target: 20k MAU by end of Q2 2026.

*Report generated automatically from internal analytics.*
