# Technical Details

## What it does

This project scaffolds an autonomous security-testing agent that runs entirely on a local machine. A locally-hosted LLM (Qwen 2.5-7B served via LM Studio) acts as the "brain" — it receives an objective and target, then iteratively decides which Kali Linux tools to run (nmap, nikto, searchsploit), reads the results, and plans the next step. The agent follows a plan-act-observe loop capped at a configurable number of iterations, then produces a summary of findings.

The key value proposition is **zero cloud dependency**: no API keys, no data exfiltration, and full control over the model and tools. This makes it suitable for air-gapped networks, sensitive pentests, and CTF competitions.

## Architecture

```
agent.py  (plan-act-observe loop)
   |
   +-- llm_client.py  (OpenAI-compatible client -> LM Studio)
   |       |
   |       +-- config.py  (endpoint, model, temperature, mock flag)
   |
   +-- tools/
         +-- recon.py     (nmap_scan, whois_lookup)
         +-- web.py       (nikto_scan)
         +-- exploit.py   (searchsploit)
```

### Data flow

1. `agent.py` builds a prompt containing the objective, target, and history of previous actions/results.
2. `llm_client.ask()` sends the prompt to LM Studio's `/v1/chat/completions` endpoint.
3. The LLM returns a JSON action (tool name + args) or `DONE`.
4. `agent.py` dispatches to the matching tool wrapper in `tools/`.
5. The tool wrapper runs a subprocess (nmap, nikto, etc.) and returns stdout.
6. The result is appended to history and the loop repeats.

### Key files

| File | Purpose |
|---|---|
| `agent.py` | Main entry point; CLI parsing, agent loop, prompt building |
| `llm_client.py` | Thin wrapper around the OpenAI client; handles mock mode |
| `config.py` | All tunables via environment variables |
| `tools/recon.py` | nmap and whois subprocess wrappers |
| `tools/web.py` | nikto subprocess wrapper |
| `tools/exploit.py` | searchsploit subprocess wrapper |

### Dependencies

- **Runtime:** `openai` Python SDK (for the OpenAI-compatible API client)
- **External tools (real mode only):** nmap, nikto, searchsploit, whois (standard Kali packages)
- **LM Studio** serving any OpenAI-compatible model (Qwen 2.5-7B recommended)

## Limitations

- **Structured output quality depends on the model.** Qwen 2.5-7B can produce malformed JSON; the agent has basic fallback parsing but may skip steps if the model drifts.
- **No Metasploit RPC integration.** The exploit module only searches for exploits via searchsploit — it does not launch them.
- **No persistent memory.** Each agent run starts fresh; there is no database of previous scans or findings.
- **Sequential execution only.** Tools run one at a time; no parallel scanning.
- **No authentication/credential handling.** The agent cannot perform authenticated scans or brute-force logins.
- **Limited tool set.** Only four tools are wired up. Adding more requires writing a wrapper and registering it in `TOOL_MAP`.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Agent factories** | Demonstrates a clean plan-act-observe pattern with tool dispatch that can be adapted to any domain — replace security tools with marketing APIs, ad platforms, or CRM calls. |
| **Offline / privacy-sensitive workflows** | Shows how to run an agentic loop with a local model, useful for enterprises that cannot send data to cloud APIs (e.g., internal security audits, regulated industries). |
| **Tool-use scaffolding** | The `TOOL_MAP` + JSON-action pattern is a minimal, dependency-free alternative to heavier frameworks like LangChain or CrewAI. Easy to extend or port to Claude tool-use. |
| **Security automation** | For teams building Claude-powered security products, this is a reference for how a small local model can handle tool selection and result synthesis in the security domain. |

## Source

- Repository: https://github.com/XenoCoreGiger31/Local-Model
- LM Studio: https://lmstudio.ai
- Qwen 2.5: https://huggingface.co/Qwen
