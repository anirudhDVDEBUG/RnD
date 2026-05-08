# LLM Vulnerability Research Harness

Mozilla used Claude to go from ~25 Firefox security fixes/month to **423 in a single month** by systematically scanning legacy C/C++ code for memory safety bugs. This repo packages that "Steer, Scale, Stack" methodology as a Claude Code skill you can point at any codebase.

**Headline result:** The demo scans 2 sample C files and surfaces 8 validated findings across 7 vulnerability classes (heap overflow, UAF, double-free, integer overflow, format string, OOB read, TOCTOU) — with root cause, trigger scenario, and suggested fix for each.

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install the skill and run your first scan in 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, and limitations
