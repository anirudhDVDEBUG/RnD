---
name: ai_hype_audit
description: |
  Audits workplace AI communications, proposals, and strategies for substance vs. hype.
  TRIGGER: user asks to review AI proposals, detect buzzword inflation, audit automation claims, assess AI initiative credibility, or evaluate AI strategy memos.
---

# AI Hype Audit

Analyze AI-related workplace communications, proposals, or strategy documents to distinguish genuine technical substance from empty hype, buzzword inflation, and vaporware claims.

## When to use

- "Review this AI proposal for substance vs. hype"
- "Audit these automation claims — are they realistic?"
- "Check if this AI strategy memo has any technical grounding"
- "Score this AI initiative pitch for buzzword density"
- "Is this automation plan credible or just career theater?"

## How to use

1. **Provide the text** — paste or point to the AI proposal, memo, Slack message, strategy doc, or pitch deck content you want audited.

2. **The audit evaluates across five dimensions:**
   - **Buzzword Density** — ratio of jargon/coined terms to concrete technical details
   - **Specificity Score** — are measurable outcomes defined, or is everything "could change literally everything"?
   - **Feasibility Check** — do the claimed automations match what current AI can actually do?
   - **ROI Grounding** — are costs (API credits, engineering time, integration effort) acknowledged?
   - **Human Impact Honesty** — does it address workforce effects responsibly, or does it "Ralph Loop" people?

3. **Output format:**
   - A 1–10 **Substance Score** (10 = fully grounded, 1 = pure theater)
   - Flagged phrases with explanations of why they are hype vs. substance
   - Suggested rewrites that add specificity and honesty
   - A brief verdict: **Ship It**, **Needs Work**, or **Career Theater**

4. **Guidelines for the audit:**
   - Be direct but constructive — the goal is to improve proposals, not mock them
   - Flag vague automation claims that don't specify *what* is automated, *how*, and *what the fallback is*
   - Flag budget requests without defined success metrics
   - Flag public callouts of team members being "automated" — this is a culture red flag
   - Reward proposals that include limitations, risks, pilot scopes, and measurable KPIs

## References

- Source: [Quoting Mo Bitar — Simon Willison's Weblog](https://simonwillison.net/2026/May/12/mo-bitar/#atom-everything)
- Original: Mo Bitar, "The Unethical Guide to Surviving AI Layoffs" (TikTok) — satirical take on weaponizing AI hype for career advancement
- The satire highlights real patterns: empty buzzwords, theatrical automation claims, and spending API credits with no measurable outcome. This skill exists to catch those patterns before they waste resources or harm team trust.
