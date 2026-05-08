# Technical Details

## What It Does

OpenAI's **Trusted Access for Cyber** is a gated program that provides verified cybersecurity defenders with access to **GPT-5.5-Cyber** — a variant of the GPT-5.5 frontier model with safety guardrails relaxed specifically for defensive security research. Where the standard GPT-5.5 model would refuse to explain exploit mechanisms, generate proof-of-concept code, or detail attack chains, the Cyber variant provides these capabilities to verified users operating within authorized scope.

This demo repo simulates three workflows the program enables: (1) source-code vulnerability scanning with exploitability ratings and patch suggestions, (2) CVE exploit analysis with detection signatures and remediation steps, and (3) infrastructure configuration auditing with severity-scored findings. The mock data mirrors the depth and structure of actual GPT-5.5-Cyber responses.

## Architecture

```
cyber_analyzer.py          Main demo — runs all three analysis workflows
  |
  +-- Mock data (inline)   Realistic vulnerability/CVE/hardening responses
  |
  +-- OpenAI API path      When OPENAI_API_KEY is set, calls gpt-5.5-cyber
       |
       +-- openai SDK      Standard chat.completions.create() with model="gpt-5.5-cyber"
```

### Key Files

| File | Purpose |
|------|---------|
| `cyber_analyzer.py` | Single-file implementation — mock data + live API integration |
| `run.sh` | Entry point — installs deps, runs demo |
| `requirements.txt` | Only dependency: `openai>=1.0.0` |
| `SKILL.md` | Claude Code skill definition with trigger phrases |

### Data Flow

1. Script checks for `OPENAI_API_KEY` environment variable
2. If set: sends structured prompts to `gpt-5.5-cyber` via `chat.completions.create()`
3. If not set: renders pre-built mock responses that mirror real API output
4. Output is printed to stdout in a structured, scannable format

### Dependencies

- Python 3.8+
- `openai` SDK (optional — mock mode works without it)

## Limitations

- **Access is gated.** You cannot call `gpt-5.5-cyber` without being approved through the Trusted Access program. The standard API key will return a model-not-found error.
- **No fine-tuning or customization.** You use the model as-is; you can't further fine-tune it for your specific codebase or threat model.
- **Not a replacement for manual review.** The model produces leads, not conclusions. False positives and missed vulnerabilities are expected — especially in complex codebases with custom memory allocators or non-standard patterns.
- **Scope restrictions apply.** Trusted Access does not authorize testing systems you don't own. Misuse leads to program revocation.
- **No binary analysis.** GPT-5.5-Cyber works on source code and text-based configurations. It cannot directly analyze compiled binaries, though it can reason about disassembly you paste in.
- **Rate limits.** Cyber model access has stricter rate limits than standard GPT-5.5, especially for long-context vulnerability analysis queries.

## Why This Matters for Claude-Driven Products

**Competitive intelligence.** OpenAI is building a moat around security-specific AI — a vertical where trust and compliance matter as much as model quality. If you're building Claude-driven security tools, this signals:

1. **Specialized models beat general models for security.** OpenAI's approach of fine-tuning + gating validates the strategy of building dedicated security agents rather than prompting a general model. Claude-based security tools should consider similar specialization paths.

2. **Trust programs as distribution.** The Trusted Access program creates a sales channel — verified orgs get exclusive access, creating lock-in. Claude-driven products targeting enterprise security teams need an equivalent trust/verification story.

3. **Reduced refusals are a feature.** For defensive security, the biggest blocker with frontier models is safety refusals. OpenAI is solving this with a verified-user program. Anthropic's usage policies and system prompts could enable similar workflows for Claude users with appropriate authorization context.

4. **Agent factories for security.** The three demos here (vuln scan, CVE analysis, hardening audit) are natural agent workflows. An agent factory could spin up specialized security agents using the patterns shown — code auditor, threat intel analyst, compliance checker — each with tailored system prompts and output schemas.

5. **Lead-gen signal.** Organizations applying for Trusted Access are self-identifying as having security budgets and AI appetite. This is valuable targeting data for anyone selling security-adjacent AI tooling.
