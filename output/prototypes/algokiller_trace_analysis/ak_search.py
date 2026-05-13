"""
ak_search — ARM64 trace evidence analysis & cipher algorithm recovery engine.

Scans ARM64 execution traces (GumTrace / Frida format) for known cryptographic
algorithm signatures: S-box constants, round constants, key-schedule patterns,
and characteristic instruction sequences.
"""

import re
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional

# ── Known cipher signatures ──────────────────────────────────────────────────
# Each signature contains constants or instruction patterns that uniquely
# identify a cipher algorithm when found in an execution trace.

CIPHER_SIGNATURES = {
    "AES-128/256": {
        "description": "AES (Rijndael) block cipher",
        "constants": [
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,  # S-box first row
            0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,  # S-box fragment
        ],
        "round_constants": [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36],
        "instruction_patterns": [
            r"AESE\s+V\d+",       # AES encrypt single round (ARM crypto ext)
            r"AESMC\s+V\d+",      # AES mix columns
            r"AESD\s+V\d+",       # AES decrypt single round
            r"AESIMC\s+V\d+",     # AES inverse mix columns
            r"EOR\s+V\d+.*V\d+",  # XOR (AddRoundKey)
            r"TBL\s+V\d+",       # Table lookup (S-box)
        ],
        "min_constant_hits": 4,
        "min_instruction_hits": 2,
    },
    "DES/3DES": {
        "description": "Data Encryption Standard / Triple DES",
        "constants": [
            0x3F, 0x06, 0x19, 0x20,  # Initial permutation table fragment
            0x07, 0x0D, 0x14, 0x29,  # Expansion permutation fragment
            0x02, 0x0E, 0x06, 0x14,  # S-box 1 fragment
        ],
        "round_constants": [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],  # key schedule shifts
        "instruction_patterns": [
            r"ROR\s+W\d+.*#\d+",    # Rotate right (permutation)
            r"AND\s+W\d+.*#0x3[Ff]", # 6-bit mask (S-box input)
            r"LSR\s+W\d+.*#\d+",    # Logical shift (bit extraction)
            r"EOR\s+W\d+.*W\d+",    # XOR (Feistel)
        ],
        "min_constant_hits": 3,
        "min_instruction_hits": 2,
    },
    "ChaCha20": {
        "description": "ChaCha20 stream cipher (Bernstein)",
        "constants": [
            0x61707865, 0x3320646E, 0x79622D32, 0x6B206574,  # "expand 32-byte k"
        ],
        "round_constants": [],
        "instruction_patterns": [
            r"ADD\s+W\d+.*W\d+",    # 32-bit add
            r"EOR\s+W\d+.*W\d+",    # XOR
            r"ROR\s+W\d+.*#(16|12|8|7)",  # Rotate by 16/12/8/7
        ],
        "min_constant_hits": 2,
        "min_instruction_hits": 3,
    },
    "SHA-256": {
        "description": "SHA-256 cryptographic hash",
        "constants": [
            0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,  # First 4 round constants
            0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,  # Initial hash values
        ],
        "round_constants": [],
        "instruction_patterns": [
            r"SHA256H\s+",          # SHA-256 hash part 1 (ARM crypto ext)
            r"SHA256H2\s+",         # SHA-256 hash part 2
            r"SHA256SU[01]\s+",     # SHA-256 schedule update
            r"ROR\s+W\d+.*#(2|6|7|11|13|17|18|19|22|25)",  # Sigma rotations
        ],
        "min_constant_hits": 2,
        "min_instruction_hits": 2,
    },
    "Blowfish": {
        "description": "Blowfish block cipher (Schneier)",
        "constants": [
            0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344,  # P-array init (digits of pi)
            0xA4093822, 0x299F31D0,
        ],
        "round_constants": [],
        "instruction_patterns": [
            r"LDR\s+W\d+.*\[.*W\d+.*LSL",  # S-box lookup with index
            r"ADD\s+W\d+.*W\d+",
            r"EOR\s+W\d+.*W\d+",
        ],
        "min_constant_hits": 2,
        "min_instruction_hits": 2,
    },
}


@dataclass
class TraceHit:
    """A single matched instruction or constant in the trace."""
    line_number: int
    address: str
    content: str
    match_type: str  # "constant" | "instruction"


@dataclass
class AlgorithmMatch:
    """Result of matching a cipher algorithm in a trace."""
    algorithm: str
    description: str
    confidence: float  # 0.0 - 1.0
    constant_hits: int
    instruction_hits: int
    address_range: tuple
    evidence: List[TraceHit] = field(default_factory=list)


def parse_trace_line(line: str) -> Optional[dict]:
    """
    Parse a single GumTrace-format line.
    Expected formats:
        0x7f8a001234  LDR X0, [X1, #0x40]
        0x7f8a001238  MOV W2, #0x63
        0x7f8a00123c  STR W3, [SP, #0x10]  ; 0x428a2f98
    """
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("//"):
        return None

    m = re.match(r"(0x[0-9a-fA-F]+)\s+(.+)", line)
    if not m:
        return None

    addr = m.group(1)
    instruction = m.group(2).strip()
    return {"address": addr, "instruction": instruction}


def extract_immediates(instruction: str) -> List[int]:
    """Extract immediate values (hex and decimal) from an instruction."""
    values = []
    # Hex immediates: #0xFF or 0xFF in comments
    for m in re.finditer(r"#?0x([0-9a-fA-F]+)", instruction):
        values.append(int(m.group(1), 16))
    # Decimal immediates
    for m in re.finditer(r"#(\d+)(?!\s*x)", instruction):
        val = int(m.group(1))
        if val > 0:
            values.append(val)
    return values


def scan_trace(trace_lines: List[str], verbose: bool = False) -> List[AlgorithmMatch]:
    """
    Scan trace lines for cipher algorithm evidence.
    Returns a list of AlgorithmMatch objects sorted by confidence.
    """
    results = []

    for algo_name, sig in CIPHER_SIGNATURES.items():
        constant_hits = []
        instruction_hits = []
        all_addresses = []

        for line_num, line in enumerate(trace_lines, 1):
            parsed = parse_trace_line(line)
            if parsed is None:
                continue

            addr = parsed["address"]
            instr = parsed["instruction"]

            # Check for constant matches
            immediates = extract_immediates(instr)
            for imm in immediates:
                if imm in sig["constants"] or imm in sig.get("round_constants", []):
                    hit = TraceHit(
                        line_number=line_num,
                        address=addr,
                        content=instr,
                        match_type="constant",
                    )
                    constant_hits.append(hit)
                    all_addresses.append(int(addr, 16))

            # Check for instruction pattern matches
            for pattern in sig["instruction_patterns"]:
                if re.search(pattern, instr, re.IGNORECASE):
                    hit = TraceHit(
                        line_number=line_num,
                        address=addr,
                        content=instr,
                        match_type="instruction",
                    )
                    instruction_hits.append(hit)
                    all_addresses.append(int(addr, 16))
                    break  # one pattern match per line is enough

        # Calculate confidence
        c_score = min(len(constant_hits) / max(sig["min_constant_hits"], 1), 1.0)
        i_score = min(len(instruction_hits) / max(sig["min_instruction_hits"], 1), 1.0)

        if len(constant_hits) >= sig["min_constant_hits"] or len(instruction_hits) >= sig["min_instruction_hits"]:
            confidence = round(0.5 * c_score + 0.5 * i_score, 3)
            if confidence >= 0.25:
                addr_range = (hex(min(all_addresses)), hex(max(all_addresses))) if all_addresses else ("0x0", "0x0")
                evidence = (constant_hits + instruction_hits)[:10]  # cap evidence list
                results.append(AlgorithmMatch(
                    algorithm=algo_name,
                    description=sig["description"],
                    confidence=confidence,
                    constant_hits=len(constant_hits),
                    instruction_hits=len(instruction_hits),
                    address_range=addr_range,
                    evidence=evidence,
                ))

    results.sort(key=lambda r: r.confidence, reverse=True)
    return results


def format_results(matches: List[AlgorithmMatch], output_format: str = "text") -> str:
    """Format analysis results for display."""
    if output_format == "json":
        out = []
        for m in matches:
            d = {
                "algorithm": m.algorithm,
                "description": m.description,
                "confidence": m.confidence,
                "confidence_pct": f"{m.confidence * 100:.1f}%",
                "constant_hits": m.constant_hits,
                "instruction_hits": m.instruction_hits,
                "address_range": {"start": m.address_range[0], "end": m.address_range[1]},
                "evidence_count": len(m.evidence),
                "evidence_sample": [
                    {"line": e.line_number, "addr": e.address, "instr": e.content, "type": e.match_type}
                    for e in m.evidence[:5]
                ],
            }
            out.append(d)
        return json.dumps({"matches": out, "total": len(out)}, indent=2)

    # Text format
    lines = []
    lines.append("=" * 72)
    lines.append("  ak_search — ARM64 Cipher Algorithm Recovery Results")
    lines.append("=" * 72)
    lines.append("")

    if not matches:
        lines.append("  No cipher algorithms detected in trace.")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"  Detected {len(matches)} algorithm(s):\n")

    for i, m in enumerate(matches, 1):
        conf_bar = "#" * int(m.confidence * 20) + "." * (20 - int(m.confidence * 20))
        lines.append(f"  [{i}] {m.algorithm}")
        lines.append(f"      {m.description}")
        lines.append(f"      Confidence: [{conf_bar}] {m.confidence * 100:.1f}%")
        lines.append(f"      Constants matched: {m.constant_hits}  |  Instructions matched: {m.instruction_hits}")
        lines.append(f"      Address range: {m.address_range[0]} — {m.address_range[1]}")
        lines.append("")
        lines.append("      Evidence (top hits):")
        for e in m.evidence[:5]:
            tag = "CONST" if e.match_type == "constant" else "INSTR"
            lines.append(f"        L{e.line_number:>5}  {e.address}  [{tag}]  {e.content}")
        lines.append("")
        lines.append("  " + "-" * 68)
        lines.append("")

    return "\n".join(lines)


def analyze_file(filepath: str, output_format: str = "text") -> str:
    """Read a trace file and return analysis results."""
    with open(filepath, "r") as f:
        trace_lines = f.readlines()

    matches = scan_trace(trace_lines)
    return format_results(matches, output_format)


# ── CLI entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ak_search — scan ARM64 traces for cipher algorithm evidence"
    )
    parser.add_argument("trace_file", help="Path to GumTrace / Frida trace file")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    args = parser.parse_args()

    result = analyze_file(args.trace_file, args.format)
    print(result)
