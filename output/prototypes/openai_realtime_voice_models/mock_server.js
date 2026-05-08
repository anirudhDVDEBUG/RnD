/**
 * Mock OpenAI Realtime API WebSocket server.
 * Simulates session management, audio streaming, transcription,
 * translation, and function calling — no API key required.
 */
const { WebSocketServer } = require("ws");

const PORT = process.env.PORT || 8765;

const MOCK_TRANSCRIPTS = [
  "Hello, how can I help you today?",
  "The weather in San Francisco is currently 62 degrees and partly cloudy.",
  "Sure, I can translate that for you. Let me process your request.",
  "Hola, el clima en San Francisco es de 62 grados y parcialmente nublado.",
  "Your meeting has been scheduled for 3 PM tomorrow.",
];

const MOCK_TRANSLATIONS = {
  en_to_es: {
    "Hello, how are you?": "Hola, como estas?",
    "What is the weather like?": "Como esta el clima?",
    default: "Traduccion en tiempo real completada.",
  },
  en_to_fr: {
    default: "Traduction en temps reel terminee.",
  },
};

function generateMockAudio(text) {
  // Generate deterministic mock PCM16 audio (base64) proportional to text length
  const samples = text.length * 160; // ~10ms per char at 16kHz
  const buf = Buffer.alloc(samples * 2);
  for (let i = 0; i < samples; i++) {
    const val = Math.floor(Math.sin(i * 0.05) * 3000);
    buf.writeInt16LE(val, i * 2);
  }
  return buf.toString("base64");
}

function startServer() {
  const wss = new WebSocketServer({ port: PORT });

  wss.on("connection", (ws, req) => {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    const model = url.searchParams.get("model") || "gpt-4o-realtime-preview";

    const session = {
      id: `sess_${Date.now()}`,
      model,
      modalities: ["text", "audio"],
      voice: "alloy",
      instructions: "",
      tools: [],
      input_audio_transcription: null,
      turn_detection: { type: "server_vad" },
    };

    // Send session.created
    ws.send(JSON.stringify({
      type: "session.created",
      session: { ...session },
    }));

    let transcriptIndex = 0;

    ws.on("message", (raw) => {
      let event;
      try {
        event = JSON.parse(raw.toString());
      } catch {
        return;
      }

      switch (event.type) {
        case "session.update": {
          Object.assign(session, event.session || {});
          ws.send(JSON.stringify({
            type: "session.updated",
            session: { ...session },
          }));
          break;
        }

        case "input_audio_buffer.append": {
          // Acknowledge audio received (no explicit ack in real API, but useful for demo)
          break;
        }

        case "input_audio_buffer.commit": {
          // Simulate VAD detecting end of speech and generating a response
          const responseId = `resp_${Date.now()}`;
          const itemId = `item_${Date.now()}`;

          // Pick transcript
          let transcript;
          if (session.instructions.toLowerCase().includes("translat")) {
            transcript = MOCK_TRANSLATIONS.en_to_es.default;
          } else {
            transcript = MOCK_TRANSCRIPTS[transcriptIndex % MOCK_TRANSCRIPTS.length];
            transcriptIndex++;
          }

          // If transcription enabled, emit input transcript
          if (session.input_audio_transcription) {
            ws.send(JSON.stringify({
              type: "conversation.item.input_audio_transcription.completed",
              item_id: itemId,
              transcript: "User said something interesting.",
            }));
          }

          // Check for function calls
          if (session.tools.length > 0 && transcript.includes("weather")) {
            const toolCall = session.tools.find((t) => t.name === "get_weather");
            if (toolCall) {
              ws.send(JSON.stringify({
                type: "response.function_call_arguments.start",
                response_id: responseId,
                item_id: itemId,
                name: "get_weather",
              }));
              ws.send(JSON.stringify({
                type: "response.function_call_arguments.delta",
                response_id: responseId,
                delta: '{"location":"San Francisco"}',
              }));
              ws.send(JSON.stringify({
                type: "response.function_call_arguments.done",
                response_id: responseId,
                item_id: itemId,
                name: "get_weather",
                arguments: '{"location":"San Francisco"}',
              }));
            }
          }

          // Stream transcript deltas (word by word)
          const words = transcript.split(" ");
          words.forEach((word, i) => {
            ws.send(JSON.stringify({
              type: "response.audio_transcript.delta",
              response_id: responseId,
              delta: (i > 0 ? " " : "") + word,
            }));
          });

          // Send audio delta
          const audio = generateMockAudio(transcript);
          ws.send(JSON.stringify({
            type: "response.audio.delta",
            response_id: responseId,
            delta: audio,
          }));

          // Response done
          ws.send(JSON.stringify({
            type: "response.audio_transcript.done",
            response_id: responseId,
            transcript,
          }));

          ws.send(JSON.stringify({
            type: "response.done",
            response_id: responseId,
            status: "completed",
            usage: {
              total_tokens: 150 + Math.floor(Math.random() * 100),
              input_tokens: 50 + Math.floor(Math.random() * 50),
              output_tokens: 100 + Math.floor(Math.random() * 50),
            },
          }));
          break;
        }

        case "response.create": {
          // Manual response trigger
          const responseId = `resp_${Date.now()}`;
          const transcript = MOCK_TRANSCRIPTS[transcriptIndex % MOCK_TRANSCRIPTS.length];
          transcriptIndex++;

          ws.send(JSON.stringify({
            type: "response.audio_transcript.delta",
            response_id: responseId,
            delta: transcript,
          }));

          ws.send(JSON.stringify({
            type: "response.audio.delta",
            response_id: responseId,
            delta: generateMockAudio(transcript),
          }));

          ws.send(JSON.stringify({
            type: "response.done",
            response_id: responseId,
            status: "completed",
          }));
          break;
        }

        default:
          // Unknown event type - ignore
          break;
      }
    });

    ws.on("close", () => {});
  });

  console.log(`[Mock Realtime API] Listening on ws://localhost:${PORT}`);
  console.log(`[Mock Realtime API] Simulating model: gpt-4o-realtime-preview`);
  return wss;
}

if (require.main === module) {
  startServer();
}

module.exports = { startServer, PORT };
