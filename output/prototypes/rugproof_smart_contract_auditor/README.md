# RugProof Smart Contract Auditor

**TL;DR:** A Claude Code skill that audits Solidity/Vyper smart contracts for vulnerabilities (reentrancy, rug pulls, flash loan vectors), generates exploit PoCs, and produces severity-graded audit report cards — all triggered by natural language in your Claude Code session.

## Headline Result

```
Audit Complete: VulnerableVault.sol
  CRITICAL: Reentrancy in withdraw() — funds drainable via callback
  HIGH: Missing access control on setFeeRecipient()
  MEDIUM: Unchecked return value on token transfer
  Risk Score: D (3 Critical, 1 High, 2 Medium findings)
  Exploit PoC generated: test/ReentrancyExploit.t.sol
```

## Quick Links

- [HOW_TO_USE.md](./HOW_TO_USE.md) — Install, configure, and run your first audit in 60 seconds
- [TECH_DETAILS.md](./TECH_DETAILS.md) — Architecture, limitations, and why this matters
- [run.sh](./run.sh) — Self-contained demo (no API keys needed)
