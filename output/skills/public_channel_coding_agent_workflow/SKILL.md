---
name: public_channel_coding_agent_workflow
description: |
  Set up a transparent, public-channel coding agent workflow inspired by Shopify's River pattern.
  TRIGGER when: user wants to design a coding agent that works in public channels, set up a Lehrwerkstatt/teaching-workshop style dev environment, implement osmosis learning for engineering teams, configure a Slack-based coding agent, or make AI-assisted development visible and searchable.
  DO NOT TRIGGER when: user wants private DM-based AI assistance, general Slack bot setup unrelated to coding agents, or standard CI/CD pipelines.
---

# Public-Channel Coding Agent Workflow

Design and implement a coding agent workflow where all AI-assisted development happens in public, searchable channels — enabling osmosis learning across the team.

## When to use

- "Set up a coding agent that works in public Slack channels"
- "I want our team to learn from each other's AI coding sessions like Shopify's River"
- "Make our AI-assisted development visible and searchable for the whole org"
- "Create a Lehrwerkstatt / teaching workshop environment for our engineering team"
- "How do I design a transparent coding agent workflow where everyone can observe and contribute?"

## How to use

### 1. Establish the Public-Channel Pattern

Create dedicated public channels for each developer's agent interactions (e.g., `#alice_agent`, `#bob_agent`). The agent must:

- **Refuse direct messages.** Politely decline DMs and suggest creating or using a public channel.
- **Work only in public channels.** Every prompt, response, code snippet, and iteration is visible.
- **Thread conversations.** Keep related work in threads so channels remain navigable.

### 2. Enable Collaborative Participation

Design the workflow so that any team member can:

- **React to threads** to signal interest, agreement, or flag issues.
- **Add context** by replying in threads with domain knowledge the agent may lack.
- **Pick up the torch** — continue a coding task another person started.
- **Help with reviews** by commenting directly on agent-generated code.

### 3. Make Everything Searchable

Ensure all agent interactions are:

- Stored in a searchable system (Slack search, or mirrored to a knowledge base).
- Tagged with relevant project/topic metadata.
- Indexed so new team members can find past solutions and patterns.

### 4. Implement the Agent Behavior

When building the agent integration:

```python
# Core behavior: reject DMs, require public channels
def handle_message(event):
    if event.channel_type == "im":
        return reply(
            "I only work in public channels! "
            "Create a channel like #yourname_agent and invite me there. "
            "This way everyone can learn from our work together."
        )
    # Proceed with coding task in public channel
    process_coding_request(event)
```

### 5. Foster Osmosis Learning

The key insight from this pattern:

- **No curriculum required.** Learning happens by proximity to visible work.
- **No training plan needed.** Team members self-select what to observe.
- **Senior developers model practices.** Their public agent sessions become live tutorials.
- **Mistakes are visible and instructive.** Failed approaches teach as much as successes.

### Design Principles

| Principle | Implementation |
|-----------|---------------|
| Transparency by default | All agent work in public channels |
| No DMs with the agent | Agent refuses private conversations |
| Searchable history | Every interaction is indexed and findable |
| Open participation | Anyone can join, react, add context |
| Named channels | `#person_agent` pattern for discoverability |

## References

- [Learning on the Shop Floor — Simon Willison](https://simonwillison.net/2026/May/11/learning-on-the-shop-floor/#atom-everything) — Analysis of Shopify's River coding agent and the Lehrwerkstatt pattern
- Tobias Lütke's description of River: a coding agent that works entirely in public Slack, creating osmosis learning at scale
- Parallels to Midjourney's early public Discord channels, where shared prompts accelerated collective learning
