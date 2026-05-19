# Technical Details

## What it does

Claude Mythos AI is an open-source frontend client for Anthropic's Claude API, built originally in C# with multi-platform targets (PC, Android APK, iOS). It differentiates itself from generic chat UIs by shipping with opinionated prompt templates for creative writing and roleplay, including SillyTavern-compatible prompt formatting that wraps system prompts and conversation turns in labeled blocks (`[System]`, `[User]`, `[Character]`).

This Python prototype reimplements the core client logic: template management, prompt formatting, config persistence, and API dispatch — so you can evaluate the approach without building the C# solution.

## Architecture

```
main.py              CLI entry point (--interactive, --list, --mock, --template)
mythos_client.py     Core library:
  ├── BUILTIN_TEMPLATES     4 prompt presets (creative_writing, roleplay, worldbuilding, general_assistant)
  ├── format_sillytavern()  Wraps messages in SillyTavern [System]/[User]/[Character] labels
  ├── format_plain()        Standard system-prompt-as-parameter formatting
  ├── MythosConfig          Dataclass for config load/save (~/.mythos/config.json)
  └── MythosClient          API client — wraps anthropic SDK, falls back to mock
demo.py              Non-interactive demo: exercises all templates, shows formatting
```

### Data flow

1. User input enters via CLI or interactive prompt.
2. `MythosConfig` resolves the active template (builtin or custom).
3. Template's `format` field selects the formatter (`plain` or `sillytavern`).
4. Formatter reshapes the system prompt + message history for the API.
5. `MythosClient.chat()` sends the request via `anthropic.Anthropic.messages.create()`.
6. Response text is returned and displayed.

### Dependencies

| Package      | Purpose                        | Required? |
|-------------|--------------------------------|-----------|
| `anthropic` | Anthropic Python SDK (API calls) | Optional (mock mode works without it) |

Python 3.10+ standard library only for mock mode.

## Limitations

- **No UI**: This prototype is CLI-only. The original C# repo provides the GUI.
- **No streaming**: Responses are returned in full, not streamed token-by-token.
- **No image/file support**: Text-only conversations.
- **No auth beyond API key**: No user accounts, no session persistence across restarts.
- **Templates are static**: Custom templates require editing the config JSON directly; no in-app template editor.
- **SillyTavern format is simplified**: The real SillyTavern protocol has more metadata fields; this implements the core label-wrapping pattern.

## Why it matters

For teams building Claude-driven products:

- **Prompt template systems** are table-stakes for any Claude frontend. This shows a clean pattern: dataclass config, named templates with per-template temperature/max_tokens, pluggable formatters.
- **SillyTavern compatibility** demonstrates how to integrate with the large existing ecosystem of roleplay/creative-writing prompt formats — relevant if you're building consumer-facing creative AI tools.
- **Config-as-JSON** pattern is useful for agent factories and white-label deployments where different customers need different system prompts and model settings.
- **Mock mode** pattern (graceful fallback when SDK isn't installed or key isn't set) is a good practice for demo-able prototypes and CI pipelines.
