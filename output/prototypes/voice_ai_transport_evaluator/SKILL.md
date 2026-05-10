---
name: voice_ai_transport_evaluator
description: |
  Evaluate and recommend audio transport protocols for voice AI applications, focusing on the trade-offs between WebRTC and alternatives like MoQ (Media over QUIC). Helps developers choose the right streaming protocol when building LLM-powered voice interfaces.
  Triggers: webrtc voice ai, audio streaming latency, voice ai transport protocol, real-time audio llm, moq vs webrtc
---

# Voice AI Transport Evaluator

Help developers evaluate audio transport protocols for voice AI and LLM-powered audio applications, with awareness of the WebRTC packet-dropping problem for AI prompts.

## When to use

- "Should I use WebRTC for my voice AI app?"
- "What transport protocol should I use for streaming audio to an LLM?"
- "My voice AI audio is getting distorted or dropping words"
- "How do I send reliable audio to a speech-to-text or voice LLM endpoint?"
- "WebRTC vs alternatives for LLM voice interfaces"

## How to use

### 1. Identify the core trade-off

WebRTC is optimized for **real-time human conversation** — it aggressively drops audio packets to keep latency low. This is ideal for video calls but problematic for voice AI because:

- **Dropped packets corrupt LLM prompts**: A garbled prompt produces a garbage response
- **Users would rather wait 200ms** for an accurate prompt than get instant but corrupted input
- **Retransmission is impossible in-browser**: WebRTC's implementation is hard-coded for real-time latency with no option to retransmit lost packets (confirmed by Discord's engineering team)

### 2. Evaluate the application requirements

Ask these questions about the project:

| Question | WebRTC favored | Alternative favored |
|----------|---------------|--------------------|
| Is sub-100ms latency critical? | Yes | No — 200-500ms is acceptable for LLMs |
| Can you tolerate audio packet loss? | Yes (conferencing) | No (LLM prompts need accuracy) |
| Browser-only deployment? | Easier setup | May need custom client |
| Bidirectional real-time audio? | Strong fit | Depends on protocol |

### 3. Recommend a transport approach

**For voice AI / LLM applications, consider alternatives to WebRTC:**

- **MoQ (Media over QUIC)** — see [moq.dev](https://moq.dev): Provides low-latency streaming with reliable delivery. Built on QUIC, supports retransmission without the all-or-nothing latency model of WebRTC.
- **WebSocket + Opus**: Simple, reliable bidirectional audio. Higher latency than WebRTC but guarantees delivery (TCP-based).
- **HTTP/2 or HTTP/3 streaming**: Server-sent events or bidirectional streams over QUIC for chunk-based audio delivery.
- **gRPC streaming**: Bidirectional streaming with protobuf, good for structured audio+metadata payloads.

**When WebRTC is still appropriate:**
- Human-to-human conferencing features alongside AI
- Applications where the WebRTC infrastructure (TURN/STUN) is already deployed
- When using OpenAI's Realtime API (which currently requires WebRTC, with the caveats described above)

### 4. Implementation guidance

When building a voice AI transport layer:

1. **Prefer reliable delivery over minimum latency** — an extra 100-200ms round-trip is negligible compared to LLM inference time
2. **Implement client-side buffering** — collect complete utterances before sending to reduce partial-prompt issues
3. **Add packet-loss monitoring** — if using WebRTC, monitor for dropped frames and alert or retry at the application level
4. **Consider VAD (Voice Activity Detection) on-device** — send complete speech segments rather than continuous streams

## References

- [Luke Curley — OpenAI's WebRTC Problem](https://moq.dev/blog/webrtc-is-the-problem/) — detailed technical analysis of why WebRTC is unsuitable for voice AI
- [Simon Willison's commentary](https://simonwillison.net/2026/May/9/luke-curley/#atom-everything) — context and discussion
- [OpenAI — Delivering low-latency voice AI at scale](https://openai.com/index/delivering-low-latency-voice-ai-at-scale/) — OpenAI's perspective on their WebRTC-based approach
- [MoQ (Media over QUIC)](https://moq.dev) — alternative protocol designed for reliable low-latency media delivery
