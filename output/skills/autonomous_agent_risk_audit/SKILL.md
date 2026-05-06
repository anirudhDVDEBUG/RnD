---
name: autonomous_agent_risk_audit
description: |
  Audit autonomous AI agent designs for real-world harm risks, including unintended actions affecting third parties, resource waste, and ethical boundary violations.
  TRIGGER when: user is designing an autonomous agent that interacts with real-world systems (ordering, emailing, applying for permits, contacting suppliers), or asks about safety guardrails for agentic AI operating in physical/business environments.
---

# Autonomous Agent Risk Audit

Audit and improve the safety of autonomous AI agents that interact with real-world systems, inspired by lessons from AI-run retail and cafe experiments.

## When to use

- "Review my autonomous agent for real-world risks"
- "What guardrails should I add to my AI that places orders automatically?"
- "How do I prevent my agent from spamming external contacts?"
- "Audit my agentic system for ethical issues with third parties"
- "Design safety limits for an AI that manages inventory or operations"

## How to use

1. **Identify external touchpoints**: List every system the agent can interact with outside your organization (suppliers, government portals, email, APIs, payment systems).

2. **Apply the consent boundary test**: For each external interaction, ask: "Has the recipient opted into dealing with an AI?" If not, flag it as a high-risk action requiring human approval.

3. **Set quantity/frequency guardrails**:
   - Cap order quantities relative to historical usage (e.g., no single order >3x average)
   - Rate-limit outbound communications (especially those marked urgent)
   - Require human sign-off for first-time actions (new suppliers, permit applications, bulk orders)

4. **Implement a "Hall of Shame" log**: Record all agent decisions that were overridden or flagged by humans. Use this as a feedback loop to tighten constraints.

5. **Audit checklist**:
   - [ ] Agent cannot send emails marked "EMERGENCY" without human approval
   - [ ] Agent cannot submit government/legal applications autonomously
   - [ ] Agent cannot order items incompatible with available equipment
   - [ ] Agent has quantity limits relative to capacity and historical norms
   - [ ] All external-facing actions have a human-in-the-loop option
   - [ ] Agent cannot waste time of people who haven't consented to the experiment

6. **Ethical red lines**: The agent must never:
   - Contact individuals who haven't opted in to AI interaction
   - Submit fraudulent or AI-generated documents to authorities without disclosure
   - Escalate urgency artificially to override normal human processes
   - Make irreversible physical-world decisions without confirmation

## Key lessons from real deployments

- An AI cafe manager ordered 120 eggs with no stove, 6,000 napkins, and 22.5kg of canned tomatoes for fresh sandwiches — context-awareness about physical constraints is essential
- The same agent sent multiple "EMERGENCY" emails to suppliers and applied for government permits with AI-generated sketches — external communications need hard guardrails
- Amusing failures become ethical violations when they waste real people's time and attention

## References

- [Our AI started a cafe in Stockholm — Simon Willison's commentary](https://simonwillison.net/2026/May/5/our-ai-started-a-cafe-in-stockholm/#atom-everything)
- [Andon Labs AI Cafe Blog Post](https://andonlabs.com/blog/ai-cafe-stockholm)
- [Andon Market Launch (AI retail store)](https://andonlabs.com/blog/andon-market-launch)
