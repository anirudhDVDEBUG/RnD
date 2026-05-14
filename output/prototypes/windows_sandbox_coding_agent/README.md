# Windows Sandbox Coding Agent

A secure, sandboxed execution environment for AI coding agents on Windows. Enforces file-access allowlists, blocks secret/key files, prevents path traversal, restricts network access, and generates ready-to-use `.wsb` config files for Windows Sandbox — so AI-generated code never touches what it shouldn't.

**Headline result:** The agent writes code, runs tests, and produces output — while automatically rejecting writes to `.env`, `.pem`, paths outside the workspace, and dangerous shell commands like `curl` exfiltration attempts.

---

- **How to set up and run** -> [HOW_TO_USE.md](HOW_TO_USE.md)
- **Architecture and technical details** -> [TECH_DETAILS.md](TECH_DETAILS.md)
- **Quick demo**: `bash run.sh` (no API keys needed, pure Python stdlib)

Source: [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox)
