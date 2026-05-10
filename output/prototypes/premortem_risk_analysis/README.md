# Premortem Risk Analysis

**Find the concrete ways a plan could fail before you commit.** A Claude Code skill that runs Gary Klein's premortem technique (2007) combined with Kahneman's outside view — multi-agent silent scan across 5 dimensions, ranked mitigation triplets, and reverse-premortem insights.

### Headline result

> 8 risks surfaced, ranked by likelihood x impact, with specific mitigations — in a single prompt, before writing a line of code.

---

**Quick start:** `bash run.sh` — runs a full premortem on a sample billing migration plan, outputs a ranked risk report to console + markdown + JSON.

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install the skill, trigger phrases, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations, relevance

Source: [AndyShaman/premortem](https://github.com/AndyShaman/premortem)
