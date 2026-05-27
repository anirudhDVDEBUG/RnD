# OSS Security Report Triage

**Open-source maintainers are drowning in AI-generated security reports.** This skill + CLI tool triages incoming vulnerability reports, detects likely AI-generated noise, scores severity (CVSS-inspired), and drafts maintainer responses — so you spend time on real bugs, not walls of text.

> **Headline result:** In the demo queue of 5 reports, the engine auto-rejects 2 AI-generated false positives, flags 1 for more info, and surfaces 2 that need human attention — saving an estimated 60+ minutes of manual review.

---

**Context:** Daniel Stenberg (curl maintainer) [wrote on May 26, 2026](https://daniel.haxx.se/blog/2026/05/26/the-pressure/) about receiving 1+ AI-generated vulnerability reports per day, almost all LOW/MEDIUM severity, consuming enormous maintainer time. This tool operationalizes his hard-won triage heuristics.

- **How to install and use** → [HOW_TO_USE.md](HOW_TO_USE.md)
- **Technical details** → [TECH_DETAILS.md](TECH_DETAILS.md)
- **Quick demo** → `bash run.sh`
