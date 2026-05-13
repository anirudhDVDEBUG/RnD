---
name: tdm_messaging_audit
description: |
  Audit and rewrite product messaging to resonate with Technical Decision Makers (TDMs) who follow analyst trends.
  Triggers: enterprise messaging, TDM positioning, analyst-aligned copy, Gartner-proof messaging, homepage audit
---

# TDM Messaging Audit

Audit product or landing-page copy through the lens of **Technical Decision Makers** — the 90% of buyers who follow analyst trends (Gartner, McKinsey, Forrester) and broad public sentiment rather than deep technical exploration.

## When to use

- "Audit my homepage copy for enterprise buyers"
- "Rewrite this messaging to appeal to technical decision makers"
- "Make our positioning more analyst-friendly"
- "How would a TDM perceive our landing page?"
- "Align our product narrative with Gartner trends"

## How to use

1. **Gather the copy.** Collect the product messaging, landing page text, or positioning document to audit. If a URL is provided, fetch the page content.

2. **Identify the TDM persona.** TDMs are motivated primarily by career safety — not getting fired. They:
   - Work 9-to-5 and do not explore tech communities on weekends
   - Rely on analyst reports (Gartner Magic Quadrants, Forrester Waves, McKinsey briefs) to justify decisions
   - Follow secular trends supported by broad public sentiment
   - Need defensible purchasing decisions they can explain to leadership

3. **Run the audit.** Evaluate the copy against these criteria:
   - **Analyst alignment**: Does the messaging use language and categories that analysts would recognize? (e.g., "Context Engine for AI Apps" vs. a clever but niche tagline)
   - **Career-safety signaling**: Does the copy make the buyer feel safe choosing this product? Look for social proof, enterprise logos, compliance badges, analyst mentions.
   - **Trend anchoring**: Does the product position itself within a recognized secular trend (AI strategy, cloud-native, zero trust, etc.)?
   - **Jargon calibration**: Is the language accessible to someone who doesn't browse Lobsters or push to GitHub on weekends?
   - **Defensibility framing**: Can a TDM point to this page and say "this is the right choice" without deep technical justification?

4. **Score each dimension** on a 1–5 scale and provide an overall TDM Resonance Score.

5. **Rewrite weak sections.** For any dimension scoring below 3, provide concrete rewrites that:
   - Mirror analyst vocabulary and category definitions
   - Lead with outcomes and risk reduction, not technical features
   - Include proof points (customer logos, case studies, analyst quotes)
   - Frame the product as the safe, defensible choice

6. **Output a summary table** with before/after comparisons and the scoring breakdown.

## Key insight

> "The thing about 90% of TDMs is that they're motivated primarily by NOT GETTING FIRED. [...] They follow secular trends supported by analysts and broad public sentiment. Oh, Gartner said that 'AI strategy' is most important? McKinsey said 'context' needs to be managed? Well, 'Context Engine for AI Apps' is going to be defensible. Buy it."
> — Mitchell Hashimoto

## References

- Source: [Quoting Mitchell Hashimoto — Simon Willison's Weblog](https://simonwillison.net/2026/May/12/mitchell-hashimoto/#atom-everything)
- Original comment: [Mitchell Hashimoto on Lobste.rs](https://lobste.rs/s/oznirn/redis_cost_ambition#c_dzrja0)
