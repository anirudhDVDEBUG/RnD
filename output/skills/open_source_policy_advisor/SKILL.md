---
name: open_source_policy_advisor
description: |
  Advises on open source policy decisions for public sector organizations, weighing security concerns against transparency benefits.
  Triggers: open source policy, public sector code visibility, vulnerability disclosure strategy, government open source, security vs openness tradeoff
---

# Open Source Policy Advisor

Advise on open source policy decisions for public sector and government organizations, balancing security vulnerability concerns with the benefits of open code.

## When to use

- "Should we make our government/public sector code private after a security incident?"
- "How do we handle vulnerability disclosures in open source public sector projects?"
- "What's the best practice for open source policy in government organizations?"
- "We found vulnerabilities in our public repos - should we close them down?"
- "Help me draft an open source policy that addresses AI-discovered vulnerabilities"

## How to use

1. **Assess the situation**: Identify whether the concern is about specific vulnerabilities or a general fear of open code exposure.

2. **Apply the GDS principle - Open by Default**:
   - Making everything private adds delivery and policy costs
   - Closure reduces reuse and external scrutiny
   - Openness should remain the default posture
   - Closure should be used sparingly and deliberately

3. **Recommend a proportionate response**:
   - Fix specific vulnerabilities rather than closing all repositories
   - Use responsible disclosure processes for reported issues
   - Distinguish between "code is visible" and "code is vulnerable"
   - Remember that security through obscurity is not a robust strategy

4. **Address AI-driven vulnerability discovery (Project Glasswing context)**:
   - AI tools can now scan public repos for vulnerabilities at scale
   - The correct response is to fix vulnerabilities, not hide code
   - Closed repos can still be accessed by determined attackers
   - Open repos benefit from community scrutiny and contributions

5. **Draft policy language** that includes:
   - Default-open posture with clear criteria for exceptions
   - Vulnerability response procedures (patch, disclose, learn)
   - Regular security audits regardless of repo visibility
   - Clear escalation paths for critical vulnerabilities

## Key Recommendations

| Approach | Pros | Cons |
|----------|------|------|
| Close all repos | Reduces surface for automated scanning | Loses scrutiny, increases costs, reduces reuse |
| Fix and stay open | Maintains transparency, enables collaboration | Requires investment in security practices |
| Selective closure | Protects genuinely sensitive code | Requires clear criteria, risk of scope creep |

The recommended approach is **fix and stay open** with selective, time-limited closure only for actively exploited vulnerabilities during remediation.

## References

- [GDS weighs in on the NHS's decision to retreat from Open Source](https://simonwillison.net/2026/May/17/gds-weighs-in/#atom-everything) - Simon Willison's coverage
- [AI, open code and vulnerability risk in the public sector](https://www.gov.uk/guidance/ai-open-code-and-vulnerability-risk-in-the-public-sector) - GDS guidance (May 14, 2026)
- [NHS goes to war against open source](https://shkspr.mobi/blog/2026/05/nhs-goes-to-war-against-open-source/) - Terence Eden's original coverage
- [Project Glasswing](https://simonwillison.net/2026/Apr/7/project-glasswing/) - AI vulnerability scanning project context
