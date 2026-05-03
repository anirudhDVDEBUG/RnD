// TypeScript SDK example — intentionally uses deprecated patterns

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function chat(msg: string) {
  const response = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 4096,
    messages: [{ role: "user", content: msg }],
  });
  return response.content[0];
}

async function streamChat(msg: string) {
  const stream = client.messages.create({
    model: "claude-opus-4-6-20250115",
    max_tokens: 1024,
    stream: true,
    messages: [{ role: "user", content: msg }],
  });
}

// MCP tool with old schema
const toolDef = {
  name: "lookup",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string" },
    },
  },
};
