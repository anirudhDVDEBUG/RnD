---
name: datacenter_deal_analyst
description: |
  Analyze data center infrastructure deals for environmental impact, political risk, and business trade-offs.
  TRIGGER: user mentions data center deal, compute infrastructure partnership, colocation agreement, environmental impact of AI infrastructure, or asks to evaluate a cloud/datacenter capacity arrangement.
---

# Data Center Deal Analyst

Analyze data center infrastructure deals and compute capacity agreements, surfacing environmental, regulatory, political, and business risks.

## When to use

- "Evaluate this data center partnership for risks"
- "What are the environmental concerns with this compute facility?"
- "Analyze the trade-offs of this infrastructure deal"
- "Assess political and regulatory risk for a data center arrangement"
- "Compare colocation options considering ESG factors"

## How to use

1. **Gather deal parameters**: Identify the parties, facility location, capacity (MW), power source, duration, and any public reporting on emissions or permits.
2. **Environmental assessment**:
   - Identify power sources (grid mix, on-site generation, renewables).
   - Check for Clean Air Act or equivalent regulatory compliance.
   - Note any history of permit violations, temporary exemptions, or pollution incidents.
   - Assess water usage and cooling infrastructure.
3. **Political and reputational risk**:
   - Research local community sentiment and any opposition (public hearings, protests, news coverage).
   - Identify whether the facility or its operator is politically controversial.
   - Evaluate how the deal may be perceived by customers, regulators, and the public.
4. **Business trade-off analysis**:
   - Weigh compute-constraint urgency against reputational cost.
   - Consider alternative capacity sources and their availability timelines.
   - Assess lock-in risk, pricing, and whether capacity is shared or dedicated.
5. **Output a structured report** with sections: Deal Summary, Environmental Risk, Regulatory/Compliance Status, Political/Reputational Risk, Business Trade-offs, and Recommendation.

### Example analysis framework

```markdown
## Deal Summary
- Parties: [Company A] leasing capacity from [Company B]
- Facility: [Name], [Location]
- Capacity: [X] MW, [Y] GPUs
- Power source: [grid/gas turbines/renewables]

## Environmental Risk
- Power generation method and emissions profile
- Permit status and compliance history
- Documented health or air quality impacts

## Regulatory / Compliance Status
- Relevant regulations (Clean Air Act, local zoning, etc.)
- Any violations, temporary exemptions, or pending enforcement

## Political / Reputational Risk
- Public sentiment and media coverage
- Association with controversial entities
- Impact on brand and stakeholder trust

## Business Trade-offs
- Compute constraint severity vs. alternatives
- Cost and timeline advantages
- Lock-in and dependency risks

## Recommendation
- Proceed / Proceed with mitigations / Seek alternatives
```

## Key considerations

- Facilities classified as "temporary" may bypass pollution controls — flag this as high risk.
- Even data center advocates acknowledge specific facilities can be problematic; general pro-datacenter arguments do not excuse site-specific violations.
- Compute scarcity creates pressure to accept suboptimal deals; quantify the cost of waiting for cleaner alternatives.
- Community health data (e.g., hospital admission trends) near facilities is a leading indicator of regulatory action.

## References

- [Notes on the xAI/Anthropic data center deal — Simon Willison](https://simonwillison.net/2026/May/7/xai-anthropic/#atom-everything)
- Context: Analysis of Anthropic's agreement to use xAI's Colossus data center, highlighting environmental permit violations, air quality concerns, and political optics of AI infrastructure deals.
