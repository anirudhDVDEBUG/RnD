---
name: llm_shebang_scripts
description: |
  Create executable script files that use Simon Willison's LLM CLI tool in the shebang line, turning plain text prompts and YAML templates into runnable programs.
  TRIGGER when: user wants to make an executable LLM prompt, use LLM in a shebang, create a self-running prompt file, build a CLI tool from a prompt, or use LLM fragments/templates as scripts.
  DO NOT TRIGGER when: user is building a full application, using the Anthropic SDK directly, or working with non-CLI LLM integrations.
---

# LLM Shebang Scripts

Create executable script files that use the `llm` CLI tool in the shebang line, turning plain-text prompts and YAML templates into runnable programs.

## When to use

- "Make this prompt into an executable script"
- "Create a shebang script that calls an LLM"
- "I want to run a text file as an LLM prompt"
- "Build a CLI tool from a prompt using llm"
- "Create an LLM template script with tool use"

## How to use

### 1. Simple prompt script (fragment mode)

Create a file with `#!/usr/bin/env -S llm -f` as the shebang. The rest of the file is the prompt.

```bash
#!/usr/bin/env -S llm -f
Generate an SVG of a pelican riding a bicycle
```

Make it executable with `chmod +x script.sh` and run it directly: `./script.sh`

### 2. Prompt script with tool calls

Add `-T tool_name` to the shebang to enable LLM tool plugins:

```bash
#!/usr/bin/env -S llm -T llm_time -f
Write a haiku that mentions the exact current time
```

### 3. YAML template script with inline Python functions

Use `#!/usr/bin/env -S llm -t` to run a YAML template that can define custom tools as Python functions:

```yaml
#!/usr/bin/env -S llm -t
model: claude-sonnet-4-6
system: |
  Use tools to run calculations
functions: |
  def add(a: int, b: int) -> int:
      return a + b
  def multiply(a: int, b: int) -> int:
      return a * b
```

Run with arguments and optional `--td` for tool-call debug output:

```bash
./calc.sh 'what is 2344 * 5252 + 134' --td
```

### Key flags

| Flag | Purpose |
|---|---|
| `-f` | Treat the file as a fragment (plain-text prompt) |
| `-t` | Treat the file as a YAML template |
| `-T plugin_name` | Enable a tool plugin for the prompt |
| `--td` | Show tool-call debug output |

### Steps to create a new script

1. Decide the mode: simple prompt (`-f`) or YAML template (`-t`).
2. Write the file with the appropriate shebang line.
3. Add the prompt text or YAML template content.
4. Run `chmod +x <filename>` to make it executable.
5. Test by running `./<filename>` directly.

### Prerequisites

- The `llm` CLI must be installed: `pip install llm` or `pipx install llm`
- For tool-use scripts, install the relevant LLM plugin (e.g., `llm install llm-time`)
- The `-S` flag in `env` (for multi-arg shebang) requires GNU coreutils 8.30+

## References

- Source: [Using LLM in the shebang line of a script](https://simonwillison.net/2026/May/11/llm-shebang/#atom-everything) — Simon Willison's Weblog
- [LLM CLI documentation](https://llm.datasette.io/en/stable/)
- [LLM fragments](https://llm.datasette.io/en/stable/fragments.html)
- [LLM tools](https://llm.datasette.io/en/stable/tools.html)
