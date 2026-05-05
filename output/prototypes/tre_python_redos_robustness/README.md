# TRE Python Binding — ReDoS Robustness Demo

**TL;DR:** A Python `ctypes` wrapper for the TRE regex engine that completes ReDoS-evil patterns in microseconds, while Python's built-in `re` takes 10-100+ seconds on the same input.

## Headline Result

```
Pattern: (a+)+$  |  Input: "aaa...aaa!" (25 a's)
  Python re:  ~30 seconds (catastrophic backtracking)
  TRE:        ~0.0002 seconds (linear time)
```

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, configure, run in 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — How it works, architecture, limitations
