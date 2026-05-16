# How to Use — Polis Protocol

## Install

No external packages required. Python 3.8+ only (stdlib).

```bash
git clone https://github.com/yehudalevy-collab/polis-protocol.git
cd polis-protocol
bash run.sh
```

Or use this prototype directly:

```bash
cd polis_protocol_multi_agent_routing
bash run.sh
```

## As a Claude Code Skill

This is a **Claude Code skill**. To install:

1. Copy the skill folder:
   ```bash
   mkdir -p ~/.claude/skills/polis-protocol
   cp SKILL.md ~/.claude/skills/polis-protocol/SKILL.md
   ```

2. **Trigger phrases** that activate it:
   - "Set up multi-agent routing across Claude, GPT, and Gemini"
   - "Create capability cards for my AI agent team"
   - "Add bandit routing to pick the best agent for each task"
   - "Build an AGENTS.md protocol for cross-vendor agent coordination"
   - "Track lessons learned across agent runs"

3. Once installed, Claude Code will use the skill to scaffold `.polis/` directories, write capability cards, configure bandit routing, and maintain a lessons ledger in your project.

## First 60 Seconds

```bash
$ bash run.sh

Polis Protocol — Multi-Agent Routing Demo

=================================================================
  POLIS PROTOCOL — Multi-Agent Routing Demo
=================================================================

Loaded 4 agent capability cards:
  claude     | vendor=anthropic   | ctx=  200,000 | cost=medium
  codex      | vendor=openai      | ctx=  200,000 | cost=high
  gemini     | vendor=google      | ctx=1,000,000 | cost=low
  gpt        | vendor=openai      | ctx=  128,000 | cost=medium

-----------------------------------------------------------------
Round  Task Type            Selected       Best   Reward  Match
-----------------------------------------------------------------
    5  code_generation         claude     claude    0.925    YES
   10  creative_writing           gpt        gpt    0.871    YES
   ...
   60  code_review             claude     claude    0.963    YES
-----------------------------------------------------------------

Results over 60 rounds:
  Optimal agent selected: 45/60 (75.0%)
  Average reward:         0.812
  Lessons recorded:       60

Learned routing table (bandit arm stats):
  Task: code_generation
    claude        pulls= 12  mean_reward=0.908  alpha=12.5 beta=2.1
    codex         pulls=  3  mean_reward=0.830  alpha=3.5  beta=1.5
    ...
```

**What happened:**
1. Loaded 4 agent capability cards from `.polis/agents/`
2. Ran 60 simulated tasks across 6 task types
3. Thompson Sampling learned which agent is best for each task type
4. All outcomes saved to `.polis/lessons/ledger.json` (and `.md`)
5. Next run can warm-start from the saved ledger

## Directory Layout

After running:

```
.polis/
├── AGENTS.md              # Protocol index
├── agents/
│   ├── claude.md          # Capability card
│   ├── codex.md
│   ├── gemini.md
│   └── gpt.md
├── routing/
│   └── bandit.md          # Routing config
└── lessons/
    ├── ledger.json        # Machine-readable log
    └── ledger.md          # Human-readable log
```

## Integrating Into Your Own Project

```python
from polis.cards import load_cards
from polis.bandit import BanditRouter
from polis.ledger import Ledger

cards = load_cards(".polis/agents")
router = BanditRouter(list(cards.keys()), strategy="thompson_sampling")
ledger = Ledger(".polis/lessons/ledger.json")
ledger.replay_into(router)  # warm-start

agent, scores = router.select("code_generation")
# ... call the selected agent's API ...
router.update("code_generation", agent, reward=0.9)
```
