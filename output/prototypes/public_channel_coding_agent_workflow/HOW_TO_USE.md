# How to Use

## Installation

### Run the demo (zero dependencies)

```bash
git clone <this-repo>
cd public_channel_coding_agent_workflow
bash run.sh
```

Python 3.10+ required. No external packages needed -- the demo uses only the Python standard library.

### For real Slack integration

```bash
pip install slack_sdk>=3.27.0
```

You'll also need a Slack Bot Token with `chat:write`, `channels:read`, `im:read`, and `reactions:read` scopes.

---

## Claude Code Skill Installation

This repo includes a `SKILL.md` that turns the pattern into a Claude Code skill.

### 1. Drop the skill file

```bash
mkdir -p ~/.claude/skills/public_channel_coding_agent_workflow
cp SKILL.md ~/.claude/skills/public_channel_coding_agent_workflow/SKILL.md
```

### 2. Trigger phrases

Claude Code will activate this skill when you say things like:

- "Set up a coding agent that works in public Slack channels"
- "I want our team to learn from each other's AI coding sessions like Shopify's River"
- "Make our AI-assisted development visible and searchable"
- "Create a Lehrwerkstatt environment for our engineering team"
- "Design a transparent coding agent workflow"

### 3. What it does NOT trigger on

- Private DM-based AI assistance requests
- General Slack bot setup unrelated to coding agents
- Standard CI/CD pipeline configuration

---

## First 60 Seconds

**Input:**

```bash
bash run.sh
```

**Output (abbreviated):**

```
=== Public-Channel Coding Agent Workflow ===

Scenario 1: Developer tries to DM the agent
  alice (DM): Hey, can you help me write a sorting function?
  REFUSED: Hey alice! I only work in public channels so everyone can
  learn from our conversation. Create a channel like #alice_agent...

Scenario 4: Correct usage -- #alice_agent public channel
  alice (#alice_agent): Write a function to aggregate sales data
  AGENT: Here's a function based on your request, alice...
  ```python
  def process_data(items: list[dict]) -> dict:
      ...
  ```

Scenario 5: Team collaboration -- others jump in
  dave reacted with :eyes:
  dave (thread): Nice! Consider using defaultdict.
  eve (thread): We have a similar utility in utils/aggregators.py

Searchable Interaction History
  1. [REFUSED] REFUSED_DM           user=alice    channel=@alice
  2. [REFUSED] REFUSED_PRIVATE      user=bob      channel=#secret-project
  3. [OK]      SUGGEST_RENAME       user=carol    channel=#general
  4. [OK]      PROCESSED            user=alice    channel=#alice_agent
  ...
```

The demo walks through 7 scenarios: DM refusal, private-channel refusal, non-standard channel warning, proper public-channel coding, team collaboration in threads, public code review, and refactoring.

---

## Using the Library in Your Own Code

```python
from channel_agent import PublicChannelAgent, ChannelWorkspace, ChannelType

ws = ChannelWorkspace()
ws.create_channel("#myname_agent")

# This works -- public channel
resp = ws.send_message(
    user="myname",
    text="Write a function to parse CSV files",
    channel="#myname_agent",
    channel_type=ChannelType.PUBLIC,
)
print(resp.text)
print(resp.code)

# This is refused -- DM
resp = ws.send_message(
    user="myname",
    text="Help me secretly",
    channel="@myname",
    channel_type=ChannelType.DM,
)
print(resp.refused)  # True
```

## Connecting to Real Slack

Replace the `ChannelType` detection with Slack's event API:

```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# In your Slack event handler:
def handle_slack_event(event):
    channel_type = event.get("channel_type")  # "im", "channel", "group"
    if channel_type == "im":
        # Agent refuses
        client.chat_postMessage(
            channel=event["channel"],
            text="I only work in public channels! Create #yourname_agent."
        )
        return
    # Process in public channel...
```
