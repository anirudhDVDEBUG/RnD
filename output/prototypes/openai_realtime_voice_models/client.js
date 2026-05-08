/**
 * OpenAI Realtime API client demo.
 * Connects to a Realtime API WebSocket endpoint (real or mock),
 * demonstrates: session config, audio streaming, transcription,
 * translation, and function calling.
 */
const WebSocket = require("ws");

const API_URL = process.env.REALTIME_API_URL || "ws://localhost:8765";
const MODEL = process.env.REALTIME_MODEL || "gpt-4o-realtime-preview";

const DIVIDER = "─".repeat(60);

function log(label, msg) {
  const ts = new Date().toISOString().slice(11, 23);
  console.log(`  [${ts}] ${label}: ${msg}`);
}

function createMockAudioChunk(text) {
  // Simulate a short PCM16 audio buffer as base64
  const buf = Buffer.alloc(3200); // 100ms at 16kHz mono
  for (let i = 0; i < 1600; i++) {
    buf.writeInt16LE(Math.floor(Math.sin(i * 0.1) * 2000), i * 2);
  }
  return buf.toString("base64");
}

async function runDemo() {
  console.log("\n" + DIVIDER);
  console.log("  OpenAI Realtime Voice API — Interactive Demo");
  console.log(DIVIDER);
  console.log(`  Endpoint : ${API_URL}`);
  console.log(`  Model    : ${MODEL}`);
  console.log(DIVIDER + "\n");

  const url = `${API_URL}?model=${MODEL}`;
  const ws = new WebSocket(url);

  const events = [];
  let resolveNext;
  const waitForEvent = (targetType, timeoutMs = 5000) =>
    new Promise((resolve, reject) => {
      const existing = events.find((e) => e.type === targetType);
      if (existing) {
        events.splice(events.indexOf(existing), 1);
        return resolve(existing);
      }
      const timer = setTimeout(() => {
        resolveNext = null;
        reject(new Error(`Timeout waiting for ${targetType}`));
      }, timeoutMs);
      resolveNext = (ev) => {
        if (ev.type === targetType) {
          clearTimeout(timer);
          resolveNext = null;
          resolve(ev);
          return true;
        }
        return false;
      };
    });

  ws.on("message", (raw) => {
    const event = JSON.parse(raw.toString());
    if (resolveNext && resolveNext(event)) return;
    events.push(event);
  });

  await new Promise((resolve, reject) => {
    ws.on("open", resolve);
    ws.on("error", reject);
  });

  // ── Step 1: Session Created ──
  const created = await waitForEvent("session.created");
  console.log("STEP 1: Session Created");
  log("Session ID", created.session.id);
  log("Model", created.session.model);
  console.log();

  // ── Step 2: Configure session with voice + transcription ──
  console.log("STEP 2: Configure Session (voice + transcription)");
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      modalities: ["text", "audio"],
      voice: "alloy",
      input_audio_format: "pcm16",
      output_audio_format: "pcm16",
      input_audio_transcription: { model: "whisper-1" },
      turn_detection: { type: "server_vad" },
    },
  }));
  const updated = await waitForEvent("session.updated");
  log("Voice", updated.session.voice || "alloy");
  log("Transcription", updated.session.input_audio_transcription ? "enabled (whisper-1)" : "disabled");
  log("Turn detection", updated.session.turn_detection?.type || "server_vad");
  console.log();

  // ── Step 3: Send audio and get response ──
  console.log("STEP 3: Stream Audio & Get Response");
  log("Sending", "3 audio chunks (simulated speech)");
  for (let i = 0; i < 3; i++) {
    ws.send(JSON.stringify({
      type: "input_audio_buffer.append",
      audio: createMockAudioChunk(`chunk_${i}`),
    }));
  }
  ws.send(JSON.stringify({ type: "input_audio_buffer.commit" }));

  // Collect streamed transcript
  let fullTranscript = "";
  let audioBytes = 0;
  let done = false;
  let inputTranscript = null;

  await new Promise((resolve) => {
    const handler = (raw) => {
      const ev = JSON.parse(raw.toString());
      switch (ev.type) {
        case "conversation.item.input_audio_transcription.completed":
          inputTranscript = ev.transcript;
          break;
        case "response.audio_transcript.delta":
          fullTranscript += ev.delta;
          break;
        case "response.audio.delta":
          audioBytes += Buffer.from(ev.delta, "base64").length;
          break;
        case "response.done":
          done = true;
          ws.removeListener("message", handler);
          resolve();
          break;
      }
    };
    ws.on("message", handler);
  });

  if (inputTranscript) {
    log("Input transcription", `"${inputTranscript}"`);
  }
  log("Response transcript", `"${fullTranscript}"`);
  log("Audio received", `${audioBytes} bytes PCM16`);
  console.log();

  // ── Step 4: Enable translation mode ──
  console.log("STEP 4: Translation Mode (English → Spanish)");
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      instructions: "You are a real-time translator. Translate all speech to Spanish.",
      modalities: ["text", "audio"],
    },
  }));
  await waitForEvent("session.updated");
  log("Mode", "Translation (EN → ES)");

  // Send audio for translation
  ws.send(JSON.stringify({
    type: "input_audio_buffer.append",
    audio: createMockAudioChunk("translate this"),
  }));
  ws.send(JSON.stringify({ type: "input_audio_buffer.commit" }));

  let translatedText = "";
  await new Promise((resolve) => {
    const handler = (raw) => {
      const ev = JSON.parse(raw.toString());
      if (ev.type === "response.audio_transcript.delta") translatedText += ev.delta;
      if (ev.type === "response.done") { ws.removeListener("message", handler); resolve(); }
    };
    ws.on("message", handler);
  });
  log("Translated output", `"${translatedText}"`);
  console.log();

  // ── Step 5: Function calling ──
  console.log("STEP 5: Function Calling (Voice Agent)");
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      instructions: "You are a helpful voice assistant.",
      tools: [
        {
          type: "function",
          name: "get_weather",
          description: "Get current weather for a location",
          parameters: {
            type: "object",
            properties: { location: { type: "string" } },
            required: ["location"],
          },
        },
      ],
    },
  }));
  await waitForEvent("session.updated");
  log("Tools registered", "get_weather");

  ws.send(JSON.stringify({
    type: "input_audio_buffer.append",
    audio: createMockAudioChunk("what's the weather"),
  }));
  ws.send(JSON.stringify({ type: "input_audio_buffer.commit" }));

  let functionName = "";
  let functionArgs = "";
  let agentTranscript = "";
  await new Promise((resolve) => {
    const handler = (raw) => {
      const ev = JSON.parse(raw.toString());
      if (ev.type === "response.function_call_arguments.start") functionName = ev.name;
      if (ev.type === "response.function_call_arguments.delta") functionArgs += ev.delta;
      if (ev.type === "response.audio_transcript.delta") agentTranscript += ev.delta;
      if (ev.type === "response.done") { ws.removeListener("message", handler); resolve(); }
    };
    ws.on("message", handler);
  });

  if (functionName) {
    log("Function called", `${functionName}(${functionArgs})`);
  }
  if (agentTranscript) {
    log("Agent response", `"${agentTranscript}"`);
  }
  console.log();

  // ── Summary ──
  console.log(DIVIDER);
  console.log("  SUMMARY");
  console.log(DIVIDER);
  console.log("  Features demonstrated:");
  console.log("    1. WebSocket session lifecycle (create → configure → use)");
  console.log("    2. Streaming audio input with server-side VAD");
  console.log("    3. Real-time speech transcription (Whisper)");
  console.log("    4. Speech-to-speech translation (EN → ES)");
  console.log("    5. Voice-triggered function calling (tool use)");
  console.log();
  console.log("  To use with real OpenAI API:");
  console.log("    export OPENAI_API_KEY=sk-...");
  console.log("    export REALTIME_API_URL=wss://api.openai.com/v1/realtime");
  console.log(DIVIDER + "\n");

  ws.close();
}

if (require.main === module) {
  runDemo().catch((err) => {
    console.error("Demo error:", err.message);
    process.exit(1);
  });
}

module.exports = { runDemo };
