"""Sample AI proposals for demonstration — one hype-heavy, one grounded."""

HYPE_PROPOSAL = """
Subject: AI Transformation Initiative — Q3 Roadmap

Team, I'm thrilled to share our revolutionary AI-first strategy that will be a paradigm
shift for the entire organization. We're going to leverage AI to fully automate all
customer support workflows with zero touch, no human intervention needed.

This game-changing initiative will 10x our productivity and make us best-in-class
in the industry. Our cutting-edge agentic AI system will autonomously handle every
customer interaction end-to-end.

By deploying this next-generation intelligent automation platform, we can achieve
near-100% accuracy on all tasks and replace the entire support team. This is truly
a moonshot that could change literally everything about how we operate.

The AI will also turbocharge our sales pipeline through hyper-automation of lead
scoring and outreach. No need for humans in the loop — the system is self-healing
and will democratize access to insights across the org.

Let's disrupt ourselves before someone else does. This is a no-brainer.

— VP of Innovation
"""

GROUNDED_PROPOSAL = """
Subject: AI-Assisted Ticket Triage — Pilot Proposal

Problem: Our L1 support team spends 40% of time (approx 320 hours/month) routing
tickets to the correct specialist queue. Misrouting rate is currently 23%, causing
avg 4-hour resolution delays.

Proposal: Deploy an LLM-based classifier to auto-suggest queue assignments for
incoming tickets. Human agents review and approve/override suggestions.

Scope: Pilot with 3 product categories (Billing, Technical, Account) for 8 weeks.

Expected outcomes:
- Reduce misrouting from 23% to under 10% (measured by weekly audit of 100 random tickets)
- Reduce avg triage time from 4.2 min to under 1.5 min per ticket
- Human-in-the-loop: agents always have override capability

Costs:
- API cost estimate: $1,200/month (based on ~15k tickets/month at ~800 tokens each)
- Engineering effort: 3 weeks for integration + 1 week testing
- Total pilot cost: ~$8,500 including engineering time

Success criteria: If misrouting drops below 12% and agent satisfaction stays above
7/10 in survey, we expand to remaining 5 categories in Q4.

Risks & limitations:
- Model may struggle with multi-category tickets (estimated 8% of volume)
- Fallback: tickets with <70% confidence route to senior agent for manual triage
- No headcount changes during pilot — this augments the team, doesn't replace it

Transition plan: If expanded, L1 agents upskill to handle escalated edge cases
that the model flags as uncertain.

— Engineering Manager, Support Tools
"""

ALL_SAMPLES = {
    "hype_heavy": HYPE_PROPOSAL,
    "grounded": GROUNDED_PROPOSAL,
}
