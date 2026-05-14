"""
RugProof Smart Contract Auditor — Demo Implementation

Performs static pattern-based vulnerability detection on Solidity contracts.
Produces structured audit reports with severity classification and remediation guidance.
"""

import re
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFORMATIONAL"


@dataclass
class Finding:
    severity: Severity
    title: str
    description: str
    swc_id: Optional[str] = None
    line_number: Optional[int] = None
    recommendation: str = ""
    exploit_poc: str = ""


@dataclass
class AuditReport:
    contract_name: str
    compiler_version: str
    lines_of_code: int
    findings: list = field(default_factory=list)

    @property
    def risk_score(self) -> str:
        critical = sum(1 for f in self.findings if f.severity == Severity.CRITICAL)
        high = sum(1 for f in self.findings if f.severity == Severity.HIGH)
        if critical >= 2:
            return "F"
        elif critical == 1:
            return "D"
        elif high >= 2:
            return "C"
        elif high == 1:
            return "B"
        else:
            return "A"

    def severity_counts(self) -> dict:
        counts = {s: 0 for s in Severity}
        for f in self.findings:
            counts[f.severity] += 1
        return counts

    def to_json(self) -> str:
        return json.dumps({
            "contract": self.contract_name,
            "compiler": self.compiler_version,
            "loc": self.lines_of_code,
            "risk_score": self.risk_score,
            "findings": [
                {
                    "severity": f.severity.value,
                    "title": f.title,
                    "description": f.description,
                    "swc": f.swc_id,
                    "line": f.line_number,
                    "recommendation": f.recommendation,
                }
                for f in self.findings
            ],
        }, indent=2)


class VulnerabilityDetector:
    """Pattern-based vulnerability detector for Solidity contracts."""

    def __init__(self, source: str):
        self.source = source
        self.lines = source.split("\n")
        self.findings: list[Finding] = []

    def detect_all(self) -> list[Finding]:
        self._detect_reentrancy()
        self._detect_access_control()
        self._detect_unchecked_return()
        self._detect_rug_pull_patterns()
        self._detect_tx_origin()
        self._detect_selfdestruct()
        self._detect_unbounded_loop()
        self._detect_floating_pragma()
        return self.findings

    def _detect_reentrancy(self):
        """Detect state updates after external calls (SWC-107)."""
        # Find external calls followed by state updates
        call_pattern = re.compile(r'\.call\{.*?value.*?\}\(')
        state_update = re.compile(r'\b(balances|balance|amounts?)\[.*\]\s*=')

        in_function = False
        call_line = None

        for i, line in enumerate(self.lines, 1):
            if "function" in line:
                in_function = True
                call_line = None
            if in_function and call_pattern.search(line):
                call_line = i
            if call_line and state_update.search(line) and i > call_line:
                self.findings.append(Finding(
                    severity=Severity.CRITICAL,
                    title="Reentrancy vulnerability",
                    description=(
                        f"State update on line {i} occurs AFTER external call on line {call_line}. "
                        "An attacker can re-enter the function via a fallback/receive and "
                        "drain funds before the balance is zeroed."
                    ),
                    swc_id="SWC-107",
                    line_number=call_line,
                    recommendation=(
                        "Move state updates before external calls (checks-effects-interactions pattern), "
                        "or use OpenZeppelin ReentrancyGuard."
                    ),
                    exploit_poc=self._generate_reentrancy_poc(),
                ))
                call_line = None

    def _detect_access_control(self):
        """Detect missing access control on sensitive functions (SWC-105)."""
        sensitive_keywords = ["withdraw", "mint", "burn", "pause", "setFee", "setOwner",
                             "transferOwnership", "selfdestruct", "destroy", "setRecipient"]
        modifier_pattern = re.compile(r'\b(onlyOwner|onlyAdmin|onlyRole|require\(msg\.sender)')

        for i, line in enumerate(self.lines, 1):
            if "function" in line and "external" in line or "public" in line:
                func_name = re.search(r'function\s+(\w+)', line)
                if func_name and any(kw in func_name.group(1).lower() for kw in
                                     [k.lower() for k in sensitive_keywords]):
                    # Check next few lines for access control
                    block = "\n".join(self.lines[i-1:min(i+5, len(self.lines))])
                    if not modifier_pattern.search(block):
                        self.findings.append(Finding(
                            severity=Severity.HIGH,
                            title=f"Missing access control on {func_name.group(1)}()",
                            description=(
                                f"Function {func_name.group(1)}() on line {i} is externally callable "
                                "without access control. Any address can invoke this sensitive operation."
                            ),
                            swc_id="SWC-105",
                            line_number=i,
                            recommendation=(
                                "Add `onlyOwner` modifier or OpenZeppelin AccessControl role check."
                            ),
                        ))

    def _detect_unchecked_return(self):
        """Detect unchecked return values from low-level calls (SWC-104)."""
        for i, line in enumerate(self.lines, 1):
            if ".call" in line and "(" in line:
                if "require" not in line and "(bool" not in line and "success" not in line:
                    self.findings.append(Finding(
                        severity=Severity.MEDIUM,
                        title="Unchecked return value on external call",
                        description=f"Low-level call on line {i} does not check the return value.",
                        swc_id="SWC-104",
                        line_number=i,
                        recommendation="Check the boolean return value: `(bool success, ) = addr.call(...); require(success);`",
                    ))

    def _detect_rug_pull_patterns(self):
        """Detect common rug pull patterns."""
        source_lower = self.source.lower()

        # Hidden mint capability
        if re.search(r'function\s+\w*mint\w*.*(?:external|public)', self.source) and \
           "totalsupply" in source_lower and "onlyowner" not in source_lower:
            self.findings.append(Finding(
                severity=Severity.HIGH,
                title="Unrestricted minting capability (rug pull risk)",
                description="Contract has a public/external mint function without clear supply cap. Owner could inflate supply.",
                recommendation="Add a hard cap on total supply or remove public minting.",
            ))

        # Fee manipulation
        if re.search(r'function\s+set(Fee|Tax|Rate)', self.source):
            if not re.search(r'require\(.*<.*100|<=.*10', self.source):
                self.findings.append(Finding(
                    severity=Severity.HIGH,
                    title="Unbounded fee manipulation (rug pull risk)",
                    description="Fee/tax can be set to arbitrary values without an upper bound. Owner could set 100% fee.",
                    recommendation="Add `require(newFee <= MAX_FEE)` with a reasonable maximum (e.g., 10%).",
                ))

        # Pausable with owner exemption
        if "whennotpaused" in source_lower and "paused" in source_lower:
            if re.search(r'if\s*\(\s*msg\.sender\s*==\s*owner', self.source):
                self.findings.append(Finding(
                    severity=Severity.MEDIUM,
                    title="Pausable with owner exemption (soft rug risk)",
                    description="Contract can be paused for all users except the owner, allowing owner-only withdrawals.",
                    recommendation="Ensure pause affects all participants equally, or add a timelock.",
                ))

    def _detect_tx_origin(self):
        """Detect tx.origin usage for authentication (SWC-115)."""
        for i, line in enumerate(self.lines, 1):
            if "tx.origin" in line and ("require" in line or "==" in line):
                self.findings.append(Finding(
                    severity=Severity.MEDIUM,
                    title="tx.origin used for authentication",
                    description=f"Line {i} uses tx.origin for authorization. Vulnerable to phishing attacks via intermediary contracts.",
                    swc_id="SWC-115",
                    line_number=i,
                    recommendation="Use msg.sender instead of tx.origin for authentication.",
                ))

    def _detect_selfdestruct(self):
        """Detect unprotected selfdestruct (SWC-106)."""
        for i, line in enumerate(self.lines, 1):
            if "selfdestruct" in line or "suicide" in line:
                block = "\n".join(self.lines[max(0, i-5):i])
                if "onlyOwner" not in block and "require(msg.sender" not in block:
                    self.findings.append(Finding(
                        severity=Severity.CRITICAL,
                        title="Unprotected selfdestruct",
                        description=f"selfdestruct on line {i} can be called without access control. Anyone can destroy the contract.",
                        swc_id="SWC-106",
                        line_number=i,
                        recommendation="Add strict access control or remove selfdestruct entirely.",
                    ))

    def _detect_unbounded_loop(self):
        """Detect unbounded loops that could cause DoS (SWC-128)."""
        for i, line in enumerate(self.lines, 1):
            if re.search(r'for\s*\(.*\.length', line):
                self.findings.append(Finding(
                    severity=Severity.MEDIUM,
                    title="Unbounded loop over dynamic array",
                    description=f"Loop on line {i} iterates over a dynamic array. If the array grows large, the function may exceed the block gas limit.",
                    swc_id="SWC-128",
                    line_number=i,
                    recommendation="Implement pagination or set an upper bound on array length.",
                ))

    def _detect_floating_pragma(self):
        """Detect floating pragma (SWC-103)."""
        for i, line in enumerate(self.lines, 1):
            if re.match(r'\s*pragma\s+solidity\s*\^', line):
                self.findings.append(Finding(
                    severity=Severity.LOW,
                    title="Floating pragma version",
                    description=f"Line {i} uses a floating pragma (^). Contract may compile with different compiler versions, potentially introducing bugs.",
                    swc_id="SWC-103",
                    line_number=i,
                    recommendation="Lock pragma to a specific version: `pragma solidity 0.8.20;`",
                ))
                break  # Only report once

    def _generate_reentrancy_poc(self) -> str:
        return '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";

contract AttackerContract {
    address target;
    constructor(address _target) { target = _target; }

    function attack() external payable {
        // Deposit then immediately withdraw to trigger reentrancy
        (bool s1,) = target.call{value: msg.value}(abi.encodeWithSignature("deposit()"));
        require(s1);
        (bool s2,) = target.call(abi.encodeWithSignature("withdraw()"));
        require(s2);
    }

    receive() external payable {
        if (target.balance > 0) {
            (bool s,) = target.call(abi.encodeWithSignature("withdraw()"));
            require(s);
        }
    }
}

contract ReentrancyExploitTest is Test {
    function testReentrancyExploit() public {
        // Deploy vulnerable contract and fund it
        // AttackerContract attacker = new AttackerContract(address(vault));
        // vm.deal(address(attacker), 1 ether);
        // vm.deal(address(vault), 10 ether);
        // attacker.attack();
        // assertGt(address(attacker).balance, 1 ether);
    }
}'''


def extract_contract_name(source: str) -> str:
    match = re.search(r'contract\s+(\w+)', source)
    return match.group(1) if match else "Unknown"


def extract_compiler_version(source: str) -> str:
    match = re.search(r'pragma\s+solidity\s+([^;]+)', source)
    return f"Solidity {match.group(1).strip()}" if match else "Unknown"


def audit_contract(source: str) -> AuditReport:
    """Run full audit on a Solidity contract source."""
    detector = VulnerabilityDetector(source)
    findings = detector.detect_all()

    report = AuditReport(
        contract_name=extract_contract_name(source),
        compiler_version=extract_compiler_version(source),
        lines_of_code=len([l for l in source.split("\n") if l.strip()]),
        findings=findings,
    )
    return report


def render_report(report: AuditReport, console: Console):
    """Render audit report using rich formatting."""
    console.print()
    console.print(Panel.fit(
        f"[bold white]RUGPROOF AUDIT REPORT[/bold white]",
        border_style="red",
    ))
    console.print()

    # Summary table
    summary = Table(show_header=False, box=None, padding=(0, 2))
    summary.add_column("Field", style="bold cyan")
    summary.add_column("Value")
    summary.add_row("Contract", report.contract_name)
    summary.add_row("Compiler", report.compiler_version)
    summary.add_row("Lines of Code", str(report.lines_of_code))
    summary.add_row("Risk Score", f"[bold red]{report.risk_score}[/bold red]" if report.risk_score in "DEF"
                    else f"[bold yellow]{report.risk_score}[/bold yellow]" if report.risk_score in "BC"
                    else f"[bold green]{report.risk_score}[/bold green]")
    console.print(summary)
    console.print()

    # Severity summary
    counts = report.severity_counts()
    severity_line = " | ".join(
        f"[{'red' if s == Severity.CRITICAL else 'yellow' if s == Severity.HIGH else 'cyan'}]"
        f"{s.value}: {c}[/]"
        for s, c in counts.items() if c > 0
    )
    if severity_line:
        console.print(f"  Findings: {severity_line}")
        console.print()

    # Detailed findings
    for i, finding in enumerate(report.findings, 1):
        color = {
            Severity.CRITICAL: "red",
            Severity.HIGH: "yellow",
            Severity.MEDIUM: "cyan",
            Severity.LOW: "blue",
            Severity.INFO: "dim",
        }[finding.severity]

        console.print(f"  [{color}][{finding.severity.value}][/{color}] {finding.title}")
        console.print(f"    {finding.description}")
        if finding.swc_id:
            console.print(f"    Reference: {finding.swc_id} (https://swcregistry.io/)")
        if finding.recommendation:
            console.print(f"    [green]Fix:[/green] {finding.recommendation}")
        console.print()

    # Exploit PoC notice
    poc_findings = [f for f in report.findings if f.exploit_poc]
    if poc_findings:
        console.print(Panel(
            f"[bold]{len(poc_findings)} exploit PoC(s) generated[/bold] — "
            "run with `forge test --match-test testExploit -vvvv`",
            border_style="yellow",
        ))
        console.print()


# Sample vulnerable contracts for demo
SAMPLE_CONTRACTS = {
    "VulnerableVault": '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableVault {
    mapping(address => uint256) public balances;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        balances[msg.sender] = 0;
    }

    function setFeeRecipient(address _recipient) external {
        // Missing access control!
        owner = _recipient;
    }

    function emergencyWithdraw() external {
        selfdestruct(payable(msg.sender));
    }
}''',

    "RugToken": '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RugToken {
    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;
    address public owner;
    uint256 public transferFee = 5;
    bool public paused;

    constructor() {
        owner = msg.sender;
        totalSupply = 1000000 * 1e18;
        balanceOf[msg.sender] = totalSupply;
    }

    function mint(address to, uint256 amount) external {
        totalSupply += amount;
        balanceOf[to] += amount;
    }

    function setFee(uint256 newFee) external {
        require(msg.sender == owner);
        transferFee = newFee;
    }

    function transfer(address to, uint256 amount) external {
        require(!paused || msg.sender == owner);
        uint256 fee = amount * transferFee / 100;
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += (amount - fee);
        balanceOf[owner] += fee;
    }

    function pause() external {
        require(msg.sender == owner);
        paused = true;
    }

    function distributeDividends(address[] calldata holders) external {
        for (uint i = 0; i < holders.length; i++) {
            balanceOf[holders[i]] += 1e18;
        }
    }
}''',
}


def main():
    console = Console()

    console.print("[bold]RugProof Smart Contract Auditor — Demo[/bold]")
    console.print("=" * 50)

    for name, source in SAMPLE_CONTRACTS.items():
        console.print(f"\n[bold cyan]Auditing: {name}.sol[/bold cyan]")
        console.print("-" * 40)
        report = audit_contract(source)
        render_report(report, console)

        # Save JSON report
        with open(f"audit_{name}.json", "w") as f:
            f.write(report.to_json())
        console.print(f"  [dim]JSON report saved: audit_{name}.json[/dim]")
        console.print()

    console.print("[bold green]Audit complete.[/bold green] See JSON reports for machine-readable output.")


if __name__ == "__main__":
    main()
