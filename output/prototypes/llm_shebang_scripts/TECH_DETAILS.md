# Technical Details

## What It Does

LLM shebang scripts exploit a Unix feature — the shebang line (`#!`) — to make the `llm` CLI the interpreter for plain-text files. When you run `./script.sh`, the kernel reads the first line, sees `#!/usr/bin/env -S llm -f`, and executes `llm -f script.sh`. The `llm` tool strips the shebang, treats the remaining text as a prompt, sends it to the configured LLM, and streams the response to stdout. The `-S` flag (GNU coreutils 8.30+) enables passing multiple arguments through `env`, which normally only accepts one.

There are two modes: **fragment** (`-f`) for raw prompts, and **template** (`-t`) for YAML files that can specify the model, system prompt, and even inline Python functions as tools. Template mode enables tool-use patterns — the LLM can call your Python functions, get results, and incorporate them into its response.

## Architecture

```
User runs ./script.sh
        │
        ▼
    kernel reads shebang: #!/usr/bin/env -S llm -f
        │
        ▼
    env executes: llm [-T tool] -f script.sh [args]
        │
        ▼
    llm CLI parses file, strips shebang
        │
        ├─ fragment mode: file body → prompt
        │
        └─ template mode: YAML → model/system/functions/prompt
                │
                ▼
        LLM API call (Claude, GPT, local models, etc.)
                │
                ▼
        Response streamed to stdout
```

### Key files in this prototype

| File | Role |
|---|---|
| `shebang_builder.py` | Creates and validates shebang scripts. Two subcommands: `create` (generates scripts) and `validate` (parses and checks existing ones). |
| `shebang_simulator.py` | Mock runner that parses scripts identically to the real `llm` CLI but returns canned responses. Used for demos without API keys. |
| `examples/*.sh` | Fragment-mode scripts (plain prompts with optional `-T` tool flags). |
| `examples/calculator.yaml` | Template-mode script with inline Python functions for tool use. |

### Dependencies

- **Python 3.10+** — for `list[str] | None` type syntax
- **PyYAML** — to parse YAML template scripts
- **llm CLI** (for real usage only) — `pip install llm`

No LLM API calls are made by the demo. The simulator uses string-matching against mock responses.

## Limitations

- **GNU coreutils 8.30+ required** for the `env -S` flag. Older Linux, stock macOS, and BSDs lack this. macOS users need `brew install coreutils`.
- **No stdin + file simultaneously**: the shebang mechanism passes the file as an argument, so piping stdin works but interacts differently with some shells.
- **Single shebang line**: all flags must fit on one line. Complex configurations need template mode (`-t`).
- **No argument parsing in fragment mode**: fragment scripts can't define `--help` or custom flags. Template mode supports positional args only.
- **Security**: these scripts send their contents to external LLM APIs. Do not put secrets in the prompt text.
- **Non-deterministic output**: same script, different output each run. Not suitable for scripts that need reproducible results.

## Why This Matters for Claude-Driven Products

**Agent factories / tool builders**: Shebang scripts are the simplest possible "agent" — a single file that takes input and produces output via an LLM. A factory could generate hundreds of specialized prompt scripts and compose them with Unix pipes. `./classify.sh | ./route.sh | ./respond.sh` becomes a three-stage agent pipeline with zero framework code.

**Lead-gen and marketing**: Non-technical marketers can create, modify, and run LLM scripts without touching Python. A `./generate_ad_copy.sh` file is more approachable than a Jupyter notebook. Template mode with tool functions enables scripts that pull live data (CRM lookups, analytics) into prompt context.

**Ad creatives**: Prompt scripts can generate copy, SVGs, and structured JSON for ad variations. Pipe a product feed through a shebang script to produce hundreds of creative variants — each script is version-controlled and auditable.

**Voice AI**: Shebang scripts work well as the "brain" behind voice pipelines. A `./intent_classifier.sh` can be swapped out without redeploying the voice infrastructure. Template mode functions can call TTS/STT APIs as tools.

**Key architectural insight**: these scripts turn LLM calls into Unix-native primitives. Anything that works with files, pipes, and stdout (cron jobs, shell scripts, Makefiles, CI/CD pipelines) can now incorporate LLM reasoning with zero integration overhead.

## References

- [Using LLM in the shebang line of a script](https://simonwillison.net/2026/May/11/llm-shebang/#atom-everything) — Simon Willison
- [LLM CLI documentation](https://llm.datasette.io/en/stable/)
- [LLM fragments](https://llm.datasette.io/en/stable/fragments.html)
- [LLM tools](https://llm.datasette.io/en/stable/tools.html)
