# Open Source Policy Advisor

**A Claude Code skill that advises public-sector organisations on open source policy decisions, weighing security concerns against transparency benefits — grounded in the UK GDS "open by default" framework.**

After the NHS moved to close all public repositories in response to AI-driven vulnerability scanning (Project Glasswing), GDS published guidance reaffirming that the correct response is to fix vulnerabilities, not hide code. This skill encodes that reasoning into actionable policy recommendations.

**Headline result:** Given 3 mock public-sector scenarios (NHS Digital, HMRC, a local council), the advisor correctly recommends "stay open" for 2 and "temporary closure of affected repos only" for the 1 with an actively exploited zero-day — producing draft policy clauses for each.

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install the skill or run the CLI demo
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, logic, and limitations
