---
name: rugproof_smart_contract_auditor
description: |
  Smart contract security auditor — vulnerability detection, exploit PoC generation, mainnet-fork simulation, audit cards, and on-chain certificate minting for Solidity and Vyper contracts.
  Triggers: smart contract audit, solidity security, vyper vulnerability, rug pull detection, DeFi exploit, EVM security scan, blockchain audit, contract vulnerability scanner
---

# RugProof — Smart Contract Security Auditor

A comprehensive smart contract security auditing skill for Claude Code. Detects vulnerabilities, generates exploit proof-of-concepts, runs mainnet-fork simulations, produces audit report cards, and supports on-chain audit certificates. Works with Solidity and Vyper contracts across EVM-compatible chains.

## When to use

- "Audit this Solidity contract for vulnerabilities"
- "Check this DeFi protocol for rug pull risks"
- "Generate an exploit PoC for this smart contract bug"
- "Run a mainnet-fork simulation to test this contract"
- "Scan this Vyper contract for security issues and produce an audit card"

## How to use

### Prerequisites

- Node.js installed
- Foundry (`forge`, `cast`, `anvil`) or Hardhat for compilation and fork simulation
- An RPC endpoint (e.g., Alchemy, Infura) for mainnet-fork testing
- Clone RugProof: `git clone https://github.com/omermaksutii/RugProof.git && cd RugProof && npm install`

### Step 1 — Identify the target contract

Locate the Solidity (`.sol`) or Vyper (`.vy`) contract file(s) to audit. If auditing a deployed contract, obtain the verified source from a block explorer or provide the contract address and chain.

### Step 2 — Run vulnerability detection

Analyze the contract source for common vulnerability classes:

- **Reentrancy** — external calls before state updates
- **Access control** — missing `onlyOwner`, unprotected `selfdestruct`, privilege escalation
- **Integer overflow/underflow** — unchecked math in pre-0.8.0 contracts
- **Flash loan attack vectors** — price oracle manipulation, single-block exploits
- **Rug pull patterns** — hidden minting, fee manipulation, liquidity removal backdoors, pausable transfers with owner exemptions
- **Logic errors** — incorrect reward calculations, rounding issues, front-running opportunities
- **Storage collisions** — proxy/upgrade patterns with misaligned slots
- **MEV exposure** — sandwich attack and front-running susceptibility

For each finding, classify severity (Critical / High / Medium / Low / Informational) and map to relevant SWC Registry entries.

### Step 3 — Generate exploit proof-of-concept

For Critical and High findings, produce a Foundry test or Hardhat script that demonstrates the exploit:

```solidity
// Example: Reentrancy PoC
function testReentrancyExploit() public {
    AttackerContract attacker = new AttackerContract(address(target));
    vm.deal(address(attacker), 1 ether);
    attacker.attack();
    assertGt(address(attacker).balance, 1 ether);
}
```

### Step 4 — Mainnet-fork simulation

Fork mainnet to validate exploits against live state:

```bash
anvil --fork-url $RPC_URL --fork-block-number <block>
forge test --fork-url http://127.0.0.1:8545 --match-test testExploit -vvvv
```

### Step 5 — Produce audit report card

Generate a structured audit card with contract metadata, finding counts by severity, risk score (A-F), and prioritized recommendations. Output as Markdown or JSON.

### Step 6 — Remediation guidance

For each finding provide root cause, code fix (diff format), reference to OpenZeppelin patterns, and re-test confirmation.

## Key capabilities

- Supports EVM chains: Ethereum, Berachain, Arbitrum, Optimism, Base, Polygon, BSC, Avalanche
- Works with Foundry and Hardhat toolchains
- DeFi protocol awareness: AMMs, lending, staking, vaults, bridges
- Severity classification mapped to SWC Registry

## References

- Source: https://github.com/omermaksutii/RugProof
- SWC Registry: https://swcregistry.io/
- OpenZeppelin: https://docs.openzeppelin.com/contracts
- Foundry Book: https://book.getfoundry.sh/
