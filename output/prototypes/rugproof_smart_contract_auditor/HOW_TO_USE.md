# How to Use RugProof Smart Contract Auditor

## Installation

### Option A: As a Claude Code Skill (recommended)

```bash
# Clone the skill into your Claude skills directory
mkdir -p ~/.claude/skills/rugproof_smart_contract_auditor
cp SKILL.md ~/.claude/skills/rugproof_smart_contract_auditor/SKILL.md
```

### Option B: Full toolchain (for exploit PoCs and fork simulation)

```bash
# Clone the full RugProof repo
git clone https://github.com/omermaksutii/RugProof.git
cd RugProof
npm install

# Install Foundry (for PoC generation and mainnet-fork testing)
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

### Option C: Run the demo (this repo)

```bash
pip install -r requirements.txt
bash run.sh
```

## Trigger Phrases

Once the skill is installed, these phrases activate it in Claude Code:

- "Audit this Solidity contract for vulnerabilities"
- "Check this DeFi protocol for rug pull risks"
- "Generate an exploit PoC for this smart contract bug"
- "Run a mainnet-fork simulation to test this contract"
- "Scan this Vyper contract for security issues"
- "Smart contract audit" / "EVM security scan" / "rug pull detection"

## Configuration

For mainnet-fork simulation, set an RPC endpoint:

```bash
export RPC_URL="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
```

Without an RPC key, the skill still performs static analysis and PoC generation — it just skips live fork testing.

## First 60 Seconds

**Input:** Paste or point Claude Code at a Solidity file:

```
Audit this contract for vulnerabilities:

pragma solidity ^0.8.0;
contract VulnerableVault {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] = 0;
    }
}
```

**Output:** Claude produces a structured audit card:

```
=== RUGPROOF AUDIT REPORT ===

Contract: VulnerableVault.sol
Compiler: Solidity ^0.8.0
Lines of Code: 14

FINDINGS:
  [CRITICAL] Reentrancy in withdraw() — SWC-107
    State update (balances[msg.sender] = 0) occurs AFTER external call.
    Attacker can re-enter withdraw() via receive() fallback and drain all ETH.

    Fix: Move `balances[msg.sender] = 0` before the external call,
    or use OpenZeppelin ReentrancyGuard.

  [LOW] No event emissions for deposit/withdraw — poor observability

Risk Score: D
Recommendation: Do NOT deploy without fixing the reentrancy vulnerability.

Exploit PoC: (Foundry test generated)
```

## Workflow Integration

### CI/CD Pipeline

Add to your GitHub Actions:

```yaml
- name: Smart Contract Audit
  run: |
    claude --skill rugproof_smart_contract_auditor \
      --input "Audit contracts/ directory" \
      --output audit-report.md
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
claude --skill rugproof_smart_contract_auditor --input "Quick scan: $(git diff --cached --name-only '*.sol')"
```
