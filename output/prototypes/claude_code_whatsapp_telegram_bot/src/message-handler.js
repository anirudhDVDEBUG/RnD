/**
 * Core message handler for WhatsApp/Telegram Claude bot.
 * Routes incoming messages by type (text, voice, image, file)
 * and orchestrates Claude API calls with tool use.
 */

class MessageHandler {
  constructor(anthropicClient, options = {}) {
    this.client = anthropicClient;
    this.model = options.model || "claude-sonnet-4-6-20250514";
    this.maxTokens = options.maxTokens || 4096;
    this.ragStore = options.ragStore || null;
    this.tools = this._defaultTools();
    this.conversations = new Map(); // userId -> message history
  }

  _defaultTools() {
    return [
      {
        name: "web_search",
        description: "Search the web for current information",
        input_schema: {
          type: "object",
          properties: { query: { type: "string" } },
          required: ["query"],
        },
      },
      {
        name: "calculate",
        description: "Evaluate a mathematical expression",
        input_schema: {
          type: "object",
          properties: { expression: { type: "string" } },
          required: ["expression"],
        },
      },
      {
        name: "rag_lookup",
        description:
          "Search uploaded documents for relevant context",
        input_schema: {
          type: "object",
          properties: { query: { type: "string" } },
          required: ["query"],
        },
      },
    ];
  }

  async handleMessage(userId, message) {
    const { type, content, mimeType, fileName } = message;
    let userContent;

    switch (type) {
      case "text":
        userContent = [{ type: "text", text: content }];
        break;

      case "voice":
        const transcript = await this._transcribeAudio(content);
        userContent = [
          {
            type: "text",
            text: `[Voice message transcribed]: ${transcript}`,
          },
        ];
        break;

      case "image":
        userContent = [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: mimeType || "image/jpeg",
              data: content,
            },
          },
          {
            type: "text",
            text: "Describe and analyze this image.",
          },
        ];
        break;

      case "file":
        const fileText = await this._extractFileText(content, mimeType);
        if (this.ragStore) {
          await this.ragStore.ingest(userId, fileName, fileText);
          userContent = [
            {
              type: "text",
              text: `File "${fileName}" has been ingested into your knowledge base. You can now ask questions about it.`,
            },
          ];
        } else {
          userContent = [
            {
              type: "text",
              text: `[File: ${fileName}]\n\n${fileText}\n\nAnalyze this file.`,
            },
          ];
        }
        break;

      default:
        return { text: "Unsupported message type." };
    }

    // Maintain per-user conversation history
    if (!this.conversations.has(userId)) {
      this.conversations.set(userId, []);
    }
    const history = this.conversations.get(userId);
    history.push({ role: "user", content: userContent });

    // Trim history to last 20 messages to stay within context
    if (history.length > 20) {
      history.splice(0, history.length - 20);
    }

    // Call Claude with tool use loop
    const response = await this._callWithToolLoop(history);

    history.push({ role: "assistant", content: response.content });

    // Extract text response
    const textBlocks = response.content.filter((b) => b.type === "text");
    return {
      text: textBlocks.map((b) => b.text).join("\n") || "Done.",
      toolsUsed: response.content
        .filter((b) => b.type === "tool_use")
        .map((b) => b.name),
    };
  }

  async _callWithToolLoop(history, maxIterations = 5) {
    let response = await this.client.messages.create({
      model: this.model,
      max_tokens: this.maxTokens,
      system:
        "You are a helpful AI assistant on a messaging platform. Be concise and direct. You can use tools when needed.",
      tools: this.tools,
      messages: history,
    });

    let iterations = 0;
    while (response.stop_reason === "tool_use" && iterations < maxIterations) {
      const toolBlocks = response.content.filter((b) => b.type === "tool_use");
      const toolResults = [];

      for (const tool of toolBlocks) {
        const result = await this._executeTool(tool.name, tool.input);
        toolResults.push({
          type: "tool_result",
          tool_use_id: tool.id,
          content: result,
        });
      }

      history.push({ role: "assistant", content: response.content });
      history.push({ role: "user", content: toolResults });

      response = await this.client.messages.create({
        model: this.model,
        max_tokens: this.maxTokens,
        system:
          "You are a helpful AI assistant on a messaging platform. Be concise and direct.",
        tools: this.tools,
        messages: history,
      });
      iterations++;
    }

    return response;
  }

  async _executeTool(name, input) {
    switch (name) {
      case "web_search":
        return `[Search results for "${input.query}"]: Results would appear here from a web search integration.`;
      case "calculate":
        try {
          // Safe math evaluation (no eval)
          const result = Function(
            `"use strict"; return (${input.expression.replace(/[^0-9+\-*/().%\s]/g, "")})`
          )();
          return `Result: ${result}`;
        } catch {
          return "Error: Could not evaluate expression.";
        }
      case "rag_lookup":
        if (this.ragStore) {
          const docs = await this.ragStore.search(input.query);
          return docs.map((d) => d.text).join("\n---\n");
        }
        return "No documents in knowledge base yet.";
      default:
        return `Unknown tool: ${name}`;
    }
  }

  async _transcribeAudio(audioBuffer) {
    // In production, this would use Whisper or another STT service
    // For now, returns a placeholder
    return "[Audio transcription would appear here]";
  }

  async _extractFileText(fileBuffer, mimeType) {
    if (mimeType === "application/pdf") {
      // In production: const pdf = require('pdf-parse'); return (await pdf(fileBuffer)).text;
      return "[Extracted PDF text would appear here]";
    }
    if (typeof fileBuffer === "string") return fileBuffer;
    return fileBuffer.toString("utf-8");
  }
}

module.exports = { MessageHandler };
