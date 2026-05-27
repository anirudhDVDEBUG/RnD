# Tech Details — Pi Plugin for Claude Code

## What It Does

The Pi Plugin is a Claude Code plugin that intercepts `/pi:*` slash commands and routes them to the Pi coding agent, which by default uses DeepSeek V4 as its backing model. It acts as a thin routing layer: Claude Code handles primary coding tasks while Pi/DeepSeek provides supplementary code reviews, rescue diagnoses, explanations, and refactoring suggestions. The plugin is a 1:1 fork of [codex-plugin-cc](https://github.com/Agents365-ai/pi-plugin-cc) adapted to target the Pi agent instead of Codex.

This demo reproduces the plugin's architecture locally with mock responses so you can evaluate the routing pattern without needing a DeepSeek API key.

## Architecture

```
User types /pi:review in Claude Code
        |
        v
  PiPluginRouter.parse()     — regex extracts command + payload
        |
        v
  PiPluginRouter.route()     — validates command, emits "routing" event
        |
        v
  callPiAgent(cmd, payload)  — POST to DeepSeek V4 endpoint (mocked here)
        |
        v
  Result returned to Claude Code session with structured findings
```

### Key Files

| File | Purpose |
|---|---|
| `pi_plugin.js` | Core router: config, command parsing, agent call, response generation |
| `demo.js` | End-to-end demo exercising all 4 commands with formatted output |
| `test.js` | Unit tests for parsing, routing, error handling |
| `run.sh` | One-command entry point: runs tests then demo |

### Data Flow

1. **Input**: Raw slash command string (e.g., `/pi:review function foo() { ... }`)
2. **Parse**: Regex `/^\/pi:(\w+)\s*([\s\S]*)$/` splits command name from payload
3. **Validate**: Command checked against registered command map
4. **Route**: Payload sent to Pi agent backend (DeepSeek V4 API in production)
5. **Response**: Structured JSON with findings/diagnosis/suggestions + token usage
6. **Display**: Results rendered back in the Claude Code session

### Dependencies

- **Runtime**: Node.js >= 16 (uses only built-in `events` module)
- **Production**: Would require `node-fetch` or similar HTTP client for live API calls
- **No npm dependencies** in this demo

### Model Calls

In production, the plugin POSTs to DeepSeek's chat completions endpoint:
```
POST https://api.deepseek.com/v1/chat/completions
Authorization: Bearer $DEEPSEEK_API_KEY
Body: { model: "deepseek-v4", messages: [...] }
```

The demo replaces this with deterministic mock responses that mirror the expected response structure.

## Limitations

- **No live API calls**: This demo uses mocked responses. Production use requires a DeepSeek API key and network access.
- **Plugin registration**: The demo shows the routing logic but doesn't actually register with Claude Code's plugin system — that requires the full `pi-plugin-cc` repo.
- **Command set is fixed**: Only 4 commands (`review`, `rescue`, `explain`, `refactor`) are implemented. The upstream repo may add more.
- **No streaming**: Responses are returned as a single JSON blob, not streamed token-by-token.
- **No context passing**: The mock doesn't receive actual file contents from your editor — in production the plugin would pass the active file/selection.

## Why It Matters

For teams building Claude-driven products (lead-gen pipelines, marketing automation, agent factories):

- **Multi-agent code quality**: Get a second opinion from a different model family (DeepSeek) without leaving your Claude Code workflow. Useful for catching model-specific blind spots.
- **Agent routing pattern**: The plugin demonstrates a clean slash-command → external-agent routing pattern that's reusable for any backend (not just DeepSeek). You could fork this to route to your own fine-tuned models.
- **Cost arbitrage**: DeepSeek V4 is significantly cheaper per token than Claude Opus. Routing bulk code reviews through Pi while keeping complex reasoning on Claude is a practical cost optimization.
- **Plugin extensibility**: Shows how Claude Code's plugin system can be extended, which matters if you're building agent factories or custom developer tools on top of Claude Code.
