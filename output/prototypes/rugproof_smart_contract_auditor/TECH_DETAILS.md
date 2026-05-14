# Technical Details

## What It Does

RugProof is a Claude Code skill that performs static and dynamic security analysis of EVM smart contracts. It uses Claude's code understanding to identify vulnerability patterns (reentrancy, access control flaws, rug pull backdoors, flash loan vectors), then generates executable exploit proof-of-concepts using Foundry or Hardhat. For deployed contracts, it can fork mainnet state via Anvil to validate whether vulnerabilities are exploitable against live balances and approvals.

The skill encodes domain expertise from the SWC Registry, common DeFi exploit patterns, and OpenZeppelin's security guidelines into structured prompts that guide Claude through a multi-step audit pipeline: detection, classification, PoC generation, and remediation.

## Architecture

```
User prompt ("audit this contract")
    |
    v
SKILL.md (loaded by Claude Code)
    |
    v
Step 1: Parse contract → identify language, version, imports
Step 2: Pattern matching against vulnerability taxonomy
    - Reentrancy (SWC-107)
    - Access control (SWC-105, SWC-106)
    - Integer issues (SWC-101)
    - Rug pull patterns (hidden mint, fee manipulation, LP drain)
    - Flash loan / MEV vectors
Step 3: Severity classification (Critical/High/Medium/Low/Info)
Step 4: Exploit PoC generation (Foundry test format)
Step 5: Audit card output (Markdown/JSON)
```

### Key Files (in full RugProof repo)

- `SKILL.md` — Primary skill definition loaded by Claude Code
- `agents/` — 19 specialized sub-agents for different vulnerability domains
- `skills/` — 33 skills covering audit lifecycle phases
- `commands/` — 38 commands for granular audit control
- `mcp-servers/` — 9 MCP servers for tool integration (block explorer, compiler, fork manager)

### Dependencies

- **Claude Code** — execution environment (required)
- **Foundry** (`forge`, `cast`, `anvil`) — compilation, testing, fork simulation (optional but recommended)
- **Node.js** — for RugProof's MCP servers and tooling
- **RPC endpoint** — Alchemy/Infura for mainnet-fork validation (optional)

## Limitations

- **Static analysis only without Foundry** — the skill alone does pattern matching via Claude's reasoning. It does NOT run Slither, Mythril, or symbolic execution. Foundry is needed for actual PoC execution.
- **No formal verification** — cannot prove absence of bugs, only detect known patterns.
- **Prompt-dependent accuracy** — quality of audit depends on Claude's reasoning; false positives and negatives are possible. Not a replacement for professional audits on high-value contracts.
- **No cross-contract analysis without full source** — if the contract imports unverified dependencies, those are opaque.
- **Fork simulation requires API keys** — mainnet-fork testing needs an RPC endpoint (Alchemy free tier works for basic use).
- **EVM-only** — does not support Solana, NEAR, or non-EVM chains.

## Why This Matters

For teams building Claude-driven products:

- **Agent factories**: Demonstrates a complex multi-step skill with branching logic (detect → classify → generate PoC → remediate). Good template for domain-specific audit agents in other verticals (compliance, code review, infrastructure).
- **Lead-gen / marketing for security firms**: Auto-generating audit previews for DeFi protocols creates inbound — "here's what we found in 60 seconds, hire us for the full audit."
- **Developer tooling integration**: Shows how Claude Code skills can plug into CI/CD pipelines, pre-commit hooks, and PR review workflows for continuous security monitoring.
- **MCP server pattern**: The 9 MCP servers demonstrate how to give Claude real tool access (block explorers, compilers, fork managers) beyond just text reasoning.
