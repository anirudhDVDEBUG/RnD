# Technical Details

## What This Is

A reference implementation of the **public-channel coding agent workflow** described in [Simon Willison's "Learning on the Shop Floor"](https://simonwillison.net/2026/May/11/learning-on-the-shop-floor/#atom-everything). The pattern originates from Shopify's "River" -- a coding agent that works exclusively in public Slack channels. Every prompt, every code suggestion, every iteration is visible to the entire engineering org, creating what Willison calls "osmosis learning" (borrowing from the German *Lehrwerkstatt* tradition of open teaching workshops).

This repo provides a standalone Python simulation of the core pattern: an agent class that enforces public-channel-only operation, refuses DMs, threads conversations, logs everything for search, and supports collaborative participation (reactions, thread replies from other team members).

## Architecture

```
channel_agent.py          Core library
  PublicChannelAgent      Agent that routes messages, refuses DMs
  ChannelWorkspace        Manages channels, threads, reactions, history
  Message / AgentResponse Data classes

demo.py                   End-to-end scenario runner (7 scenarios)
run.sh                    Entry point
SKILL.md                  Claude Code skill definition
```

### Data Flow

```
User message
  --> ChannelWorkspace.send_message()
    --> check channel_type (DM? private? public?)
    --> if DM/private: return refusal with redirect to public channel
    --> if public but wrong name: warn, still process
    --> if public + correct #name_agent: process coding request
    --> log interaction to searchable history
    --> thread the response
  --> teammates can: react, reply in thread, pick up work
  --> all history exportable via get_searchable_history() / search_history()
```

### Key Design Decisions

- **No external dependencies.** The demo runs on Python stdlib so it works anywhere without API keys.
- **Channel type is the first gate.** The agent checks channel type before doing any work -- this is the core enforcement mechanism.
- **Named channel convention.** `#person_agent` pattern makes channels discoverable via search.
- **Thread-first responses.** Every agent response includes a thread_id to keep channels navigable.
- **Searchable history.** Every interaction is logged with user, channel, action type, and text preview.

### Dependencies

- Python 3.10+ (for `list[dict]` type hints)
- No external packages for the demo
- `slack_sdk` only if connecting to real Slack

### Model Calls

None. This is a workflow pattern, not an LLM wrapper. In production, you'd plug your preferred model (Claude, GPT, etc.) into the `_process_request` method. The demo uses pattern-matched mock responses to show the channel routing and collaboration mechanics.

## Limitations

- **No real Slack integration.** This is a simulation -- connecting to Slack requires adding `slack_sdk` and a bot token with appropriate scopes.
- **No actual LLM calls.** Coding responses are mocked. In production, replace `_generate_function` etc. with calls to Claude or another model.
- **No persistence.** History lives in memory. For production, pipe `get_searchable_history()` to a database or search index.
- **No authentication.** The demo trusts user identity. Real Slack handles this via OAuth.
- **Single-agent only.** The demo shows one agent instance. Multi-agent coordination (e.g., specialized agents per domain) would require additional routing.

## Why This Matters

### For agent factories and Claude-driven products

1. **Transparency as a feature.** The biggest barrier to AI coding agent adoption in teams is trust. Public channels make agent behavior auditable by default -- every suggestion is peer-reviewed by proximity.

2. **Built-in training data.** Every public interaction becomes searchable institutional knowledge. New hires can search `#senior_dev_agent` to see how experienced engineers prompt and iterate.

3. **Reduced duplicate work.** When agent sessions are visible, teams naturally avoid re-solving the same problems. Someone searching for "CSV parser" finds the thread where it was already built.

4. **Lead-gen / marketing angle.** Companies selling AI coding tools can point to this pattern as a deployment strategy: "Here's how Shopify scaled AI-assisted development to 3,000 engineers."

5. **Quality signal for agent builders.** If your agent's outputs are good enough to survive in a public channel where senior engineers can see them, that's a strong quality signal. DM-only agents hide their mistakes.

6. **Osmosis over curriculum.** No training budget needed. The learning happens naturally when work is visible. This is the *Lehrwerkstatt* insight: apprentices learn by watching masters work, not by reading manuals.
