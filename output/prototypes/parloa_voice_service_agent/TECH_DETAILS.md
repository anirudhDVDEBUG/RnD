# Technical Details

## What it does

This prototype implements the end-to-end pipeline described in Parloa's approach to voice AI customer service: speech-to-text, intent detection, dialogue flow routing, backend tool invocation, response generation, and text-to-speech. All external dependencies (LLM, STT, TTS, CRM) are replaced with deterministic mocks so the full pipeline runs locally without API keys while preserving realistic latency simulation.

A simulation harness replays 5 synthetic customer conversations — billing inquiry, password reset, escalation on unknown issues, account lookup, and an adversarial probe — measuring intent accuracy, tool usage, escalation triggers, and per-turn latency.

## Architecture

```
Customer audio
    |
    v
[MockSTT] ──> transcribed text
    |
    v
[Intent Detection] ──> intent + confidence score
    |                   (keyword-based; swap for LLM classifier)
    v
[Flow Router] ──> selects dialogue flow from flows.yaml
    |              checks escalation threshold
    v
[Backend Tools] ──> lookup_account, get_invoice, search_kb,
    |               create_ticket, check_ticket_status
    v
[Response Generator] ──> template-based reply
    |                     (swap for LLM generation)
    v
[MockTTS] ──> synthesized audio output
```

### Key files

| File | Purpose |
|------|---------|
| `agent.py` | Core agent: STT/TTS mocks, intent detection, flow routing, backend tools, conversation metrics |
| `flows.yaml` | Declarative dialogue flow definitions with tool lists and escalation thresholds |
| `simulator.py` | Test harness: 5 scenarios with pass/fail checks on tool usage, resolution, and escalation |
| `run.sh` | One-command entry point |

### Data flow

1. Customer text enters `VoiceServiceAgent.process_input()`
2. `MockSTT.transcribe()` adds simulated latency (50-150ms)
3. `detect_intent()` scores text against keyword lists, returns intent + confidence
4. `_route_and_act()` selects the dialogue flow, checks escalation threshold, calls backend tools
5. Response text passes through `MockTTS.synthesize()` (80-200ms simulated latency)
6. `ConversationMetrics` records turn count, tool invocations, escalations, avg latency

### Dependencies

- **Python 3.10+**
- **PyYAML** — for loading `flows.yaml`
- No LLM API keys, no network calls

## Limitations

- **No real LLM:** Intent detection uses keyword matching, not a language model. Production systems would use GPT-4o or similar for both classification and response generation.
- **No real STT/TTS:** Audio is simulated as text pass-through with added latency. Real deployments need Whisper, Deepgram, or similar for STT and ElevenLabs/Azure for TTS.
- **No telephony integration:** No SIP/WebRTC layer. This is a conversation-engine prototype, not a phone system.
- **No multi-language support:** English only. Parloa supports 30+ languages.
- **No persistent state:** Conversations exist only in memory during a session.
- **Deterministic responses:** Template-based, not generative. Production agents produce more natural, varied responses via LLM.

## Why it matters for Claude-driven products

- **Voice AI patterns:** Shows the STT -> LLM -> TTS pipeline architecture that any voice agent needs, directly applicable to building Claude-powered voice agents.
- **Tool use / function calling:** Demonstrates the same tool-calling pattern Claude uses (lookup, search, create) — easy to port to Claude's native tool use.
- **Simulation testing:** The harness pattern (replay conversations, assert tool usage, check escalation) is reusable for testing any conversational agent, including Claude-based ones.
- **Agent factories:** The YAML-based flow configuration is a blueprint for building configurable agent templates — useful for platforms that spin up domain-specific agents.
- **Guardrail testing:** The adversarial scenario shows how to verify agents don't execute sensitive operations on malicious input.

## References

- [Parloa builds service agents customers want to talk to — OpenAI](https://openai.com/index/parloa)
