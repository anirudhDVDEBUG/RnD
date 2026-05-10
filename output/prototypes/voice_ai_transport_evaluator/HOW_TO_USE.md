# How to Use

## Option A: As a Claude Code Skill (recommended)

### Install

Copy the skill folder into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/voice_ai_transport_evaluator
cp SKILL.md ~/.claude/skills/voice_ai_transport_evaluator/SKILL.md
```

### Trigger phrases

Once installed, Claude Code will activate this skill when you ask questions like:

- "Should I use WebRTC for my voice AI app?"
- "What transport protocol should I use for streaming audio to an LLM?"
- "My voice AI audio is getting distorted or dropping words"
- "How do I send reliable audio to a speech-to-text or voice LLM endpoint?"
- "WebRTC vs alternatives for LLM voice interfaces"
- "moq vs webrtc"
- "audio streaming latency"
- "real-time audio llm"

Claude will walk you through the evaluation framework: identify trade-offs, assess your requirements against a decision matrix, and recommend a protocol with implementation guidance.

## Option B: As a standalone CLI tool

### Install

```bash
git clone <this-repo>
cd voice_ai_transport_evaluator
# No pip install needed -- stdlib only, Python 3.7+
```

### CLI usage

```bash
# Default evaluation (Voice AI / LLM Prompt Streaming)
python3 evaluator.py

# Choose a scenario
python3 evaluator.py --scenario browser_first
python3 evaluator.py --scenario server_to_server

# JSON output (for piping into other tools)
python3 evaluator.py --json

# Run all scenarios
python3 evaluator.py --all-scenarios

# All scenarios as JSON
python3 evaluator.py --all-scenarios --json
```

### Available scenarios

| Scenario key        | Description                              |
|---------------------|------------------------------------------|
| `voice_ai_default`  | LLM prompt streaming -- reliability is king |
| `browser_first`     | Browser-only deployment -- browser support weighted 3x |
| `server_to_server`  | Backend audio pipeline -- browser support irrelevant |

## First 60 Seconds

```bash
$ bash run.sh

=== Voice AI Transport Evaluator ===

Running default scenario (Voice AI / LLM Prompt Streaming)...

====================================================================
  VOICE AI TRANSPORT PROTOCOL EVALUATION
  Scenario: Voice AI / LLM Prompt Streaming (default)
====================================================================

  Protocol               Score  Bar                   Verdict
  ────────────────────── ────── ████████████████████  ──────────────
  WebSocket + Opus         8.25  ████████████████░░░░  ★ RECOMMENDED
  gRPC Streaming           7.68  ███████████████░░░░░
  MoQ (Media over QUIC)    7.54  ███████████████░░░░░
  WebRTC                   7.13  ██████████████░░░░░░
  HTTP/3 Streaming         6.98  █████████████░░░░░░░

  ┌─ #1 WebSocket + Opus ─────────────────────────────────────┐
  │ Weighted Score: 8.25 / 10.00
  │ TCP-based reliable delivery with Opus codec. Simple and predictable.
  │
  │ Pros:
  │   + Guaranteed delivery (TCP)
  │   + Easy to implement in any language
  │   + Works in all browsers
  │   + Simple debugging -- standard HTTP upgrade
  │
  │ Cons:
  │   - Head-of-line blocking under packet loss
  │   - Higher latency than UDP-based protocols (~150-300ms)
  │   - No built-in echo cancellation
  └──────────────────────────────────────────────────────────────┘

  KEY INSIGHT (from Luke Curley / moq.dev):

  WebRTC drops audio packets to keep latency low -- great for video
  calls, but disastrous for voice AI. A garbled prompt produces a
  garbage LLM response. Users would rather wait 200ms for accurate
  input than get instant but corrupted audio.
```

The JSON output (`--json`) can be piped into `jq` or consumed by other tools:

```bash
python3 evaluator.py --json | jq '.results[0]'
```
