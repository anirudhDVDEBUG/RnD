# humanize_chinese

**Rewrites AI-generated Chinese text so it reads naturally and sounds human-written.** Rule-based transformer that swaps formal connectors for colloquial ones, removes hedging, varies sentence rhythm, and adds natural discourse markers — zero API keys, pure Python.

## Headline result

```
INPUT:  综上所述，本产品具有重要意义，在很大程度上满足了用户的需求。
OUTPUT: 说到底，这个产品很重要，基本上满足了用户的需求。
        (5 changes applied)
```

## Quick start

```bash
bash run.sh          # runs 3 sample texts, no setup needed
```

See **[HOW_TO_USE.md](HOW_TO_USE.md)** for installation as a Claude skill and CLI usage.
See **[TECH_DETAILS.md](TECH_DETAILS.md)** for architecture, limitations, and integration ideas.
