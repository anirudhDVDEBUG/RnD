# How to Use

## Install

```bash
git clone <this-repo>
cd parloa_voice_service_agent
pip install -r requirements.txt   # just pyyaml
```

## Run the demo

```bash
bash run.sh
```

No API keys needed — all LLM calls, STT, and TTS are mocked with realistic latency simulation.

## First 60 seconds

**Input:** `bash run.sh`

**Output:** The simulator replays 5 customer conversations against the agent and prints each turn with intent, confidence, tool used, and latency. At the end you get an aggregate report:

```
  Scenarios run:    5
  Checks passed:    7
  Checks failed:    0
  Total turns:      18
  Avg latency:      ~250ms
  Tools invoked:    6
  Escalations:      1

  [PASS] Happy path — billing inquiry
  [PASS] Tech support — password reset
  [PASS] Tech support — unknown issue escalation
  [PASS] Account inquiry — suspended account
  [PASS] Adversarial — out-of-scope request
```

## Use as a Claude Skill

1. Copy the skill file:
   ```bash
   mkdir -p ~/.claude/skills/parloa_voice_service_agent
   cp SKILL.md ~/.claude/skills/parloa_voice_service_agent/SKILL.md
   ```

2. Trigger phrases that activate it:
   - "Build a voice AI customer service agent"
   - "Design a conversational agent for enterprise support"
   - "Create a real-time voice-driven support bot"
   - "Set up dialogue simulation and testing for a service agent"
   - "Parloa-style service bot"

3. Claude will use the skill to guide you through designing dialogue flows, wiring STT/TTS, connecting backend tools, and setting up simulation testing.

## Customization

- **Edit `flows.yaml`** to add new intents, tools, or escalation thresholds.
- **Add mock data** in `agent.py` (`MOCK_ACCOUNTS`, `MOCK_KB`) to simulate your own domain.
- **Add scenarios** in `simulator.py` `SCENARIOS` list to test new conversation paths.
- **Swap mocks for real services:** Replace `MockSTT`/`MockTTS` with your STT/TTS provider SDK, and replace `BackendTools` methods with real API calls.
