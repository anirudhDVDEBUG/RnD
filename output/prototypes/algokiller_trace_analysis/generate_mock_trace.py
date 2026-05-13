"""
Generate realistic ARM64 execution traces with embedded cipher algorithm
evidence for testing ak_search.

Produces two trace files:
  - sample_traces/aes_chacha_trace.log   (AES-128 + ChaCha20 mixed)
  - sample_traces/des_sha256_trace.log   (DES + SHA-256 mixed)
"""

import os
import random

random.seed(42)

TRACE_DIR = os.path.join(os.path.dirname(__file__), "sample_traces")


def addr(base: int, offset: int) -> str:
    return f"0x{base + offset * 4:016x}"


def noise_instructions(base: int, start: int, count: int) -> list:
    """Generate plausible ARM64 noise instructions."""
    regs_x = [f"X{i}" for i in range(0, 29)]
    regs_w = [f"W{i}" for i in range(0, 29)]
    templates = [
        "MOV {xr}, {xr2}",
        "LDR {xr}, [SP, #0x{off:02x}]",
        "STR {xr}, [SP, #0x{off:02x}]",
        "ADD {xr}, {xr2}, #0x{small:x}",
        "SUB {wr}, {wr2}, #0x{small:x}",
        "CMP {wr}, #0x{small:x}",
        "B.NE #0x{branch:x}",
        "BL #0x{branch:x}",
        "STP {xr}, {xr2}, [SP, #-0x10]!",
        "LDP {xr}, {xr2}, [SP], #0x10",
        "NOP",
    ]
    lines = []
    for i in range(count):
        t = random.choice(templates)
        line = t.format(
            xr=random.choice(regs_x), xr2=random.choice(regs_x),
            wr=random.choice(regs_w), wr2=random.choice(regs_w),
            off=random.randint(0, 0xFF),
            small=random.randint(1, 0x3F),
            branch=base + random.randint(0, 0x1000),
        )
        lines.append(f"{addr(base, start + i)}  {line}")
    return lines


def generate_aes_chacha_trace() -> list:
    """Generate a trace containing AES-128 and ChaCha20 evidence."""
    base = 0x7f8a000000
    lines = []
    lines.append("# GumTrace ARM64 — captured via Frida 16.5.2")
    lines.append(f"# Target: com.example.secureapp (PID 4821)")
    lines.append(f"# Timestamp: 2026-05-13T02:14:07Z")
    lines.append("")

    # Preamble noise
    lines.extend(noise_instructions(base, 0, 15))

    # ── AES key expansion region ──
    off = 20
    lines.append(f"# --- function: aes_key_expand ---")
    lines.append(f"{addr(base, off)}  MOV W0, #0x63")       # S-box[0]
    lines.append(f"{addr(base, off+1)}  MOV W1, #0x7C")     # S-box[1]
    lines.append(f"{addr(base, off+2)}  MOV W2, #0x77")     # S-box[2]
    lines.append(f"{addr(base, off+3)}  MOV W3, #0x7B")     # S-box[3]
    lines.append(f"{addr(base, off+4)}  MOV W4, #0xF2")     # S-box[4]
    lines.append(f"{addr(base, off+5)}  MOV W5, #0x6B")     # S-box[5]
    lines.append(f"{addr(base, off+6)}  TBL V0.16B, {{V1.16B}}, V2.16B")  # S-box lookup
    lines.append(f"{addr(base, off+7)}  EOR V3.16B, V0.16B, V4.16B")      # AddRoundKey
    lines.append(f"{addr(base, off+8)}  MOV W6, #0x01")     # Rcon[0]
    lines.append(f"{addr(base, off+9)}  MOV W7, #0x02")     # Rcon[1]

    lines.extend(noise_instructions(base, off + 10, 10))

    # ── AES encrypt rounds ──
    off = 45
    lines.append(f"# --- function: aes_encrypt_block ---")
    lines.append(f"{addr(base, off)}  AESE V0.16B, V1.16B")     # AES encrypt
    lines.append(f"{addr(base, off+1)}  AESMC V0.16B, V0.16B")  # AES MixColumns
    lines.append(f"{addr(base, off+2)}  AESE V0.16B, V2.16B")
    lines.append(f"{addr(base, off+3)}  AESMC V0.16B, V0.16B")
    lines.append(f"{addr(base, off+4)}  EOR V0.16B, V0.16B, V5.16B")  # final XOR

    lines.extend(noise_instructions(base, off + 5, 20))

    # ── ChaCha20 quarter-round region ──
    off = 80
    lines.append(f"# --- function: chacha20_block ---")
    lines.append(f"{addr(base, off)}  MOV W10, #0x61707865")   # "expa"
    lines.append(f"{addr(base, off+1)}  MOV W11, #0x3320646E") # "nd 3"
    lines.append(f"{addr(base, off+2)}  MOV W12, #0x79622D32") # "2-by"
    lines.append(f"{addr(base, off+3)}  MOV W13, #0x6B206574") # "te k"
    # Quarter round ops
    lines.append(f"{addr(base, off+4)}  ADD W0, W0, W1")
    lines.append(f"{addr(base, off+5)}  EOR W3, W3, W0")
    lines.append(f"{addr(base, off+6)}  ROR W3, W3, #16")
    lines.append(f"{addr(base, off+7)}  ADD W2, W2, W3")
    lines.append(f"{addr(base, off+8)}  EOR W1, W1, W2")
    lines.append(f"{addr(base, off+9)}  ROR W1, W1, #12")
    lines.append(f"{addr(base, off+10)}  ADD W0, W0, W1")
    lines.append(f"{addr(base, off+11)}  EOR W3, W3, W0")
    lines.append(f"{addr(base, off+12)}  ROR W3, W3, #8")
    lines.append(f"{addr(base, off+13)}  ADD W2, W2, W3")
    lines.append(f"{addr(base, off+14)}  EOR W1, W1, W2")
    lines.append(f"{addr(base, off+15)}  ROR W1, W1, #7")

    lines.extend(noise_instructions(base, off + 16, 15))

    # Epilogue noise
    lines.extend(noise_instructions(base, 120, 10))
    return lines


def generate_des_sha256_trace() -> list:
    """Generate a trace containing DES and SHA-256 evidence."""
    base = 0x55aa000000
    lines = []
    lines.append("# GumTrace ARM64 — captured via Frida 16.5.2")
    lines.append(f"# Target: com.legacy.bankapp (PID 9103)")
    lines.append(f"# Timestamp: 2026-05-13T02:14:22Z")
    lines.append("")

    lines.extend(noise_instructions(base, 0, 10))

    # ── DES key schedule ──
    off = 15
    lines.append(f"# --- function: des_key_schedule ---")
    lines.append(f"{addr(base, off)}  MOV W0, #0x3F")       # IP table
    lines.append(f"{addr(base, off+1)}  MOV W1, #0x06")
    lines.append(f"{addr(base, off+2)}  MOV W2, #0x19")
    lines.append(f"{addr(base, off+3)}  MOV W3, #0x20")
    lines.append(f"{addr(base, off+4)}  AND W4, W5, #0x3F")  # 6-bit S-box mask
    lines.append(f"{addr(base, off+5)}  ROR W6, W7, #3")     # permutation rotate
    lines.append(f"{addr(base, off+6)}  LSR W8, W9, #4")     # bit extraction
    lines.append(f"{addr(base, off+7)}  EOR W10, W11, W12")  # Feistel XOR
    lines.append(f"{addr(base, off+8)}  MOV W13, #0x01")     # key shift = 1
    lines.append(f"{addr(base, off+9)}  ROR W14, W15, #1")

    lines.extend(noise_instructions(base, off + 10, 15))

    # ── SHA-256 region ──
    off = 45
    lines.append(f"# --- function: sha256_compress ---")
    lines.append(f"{addr(base, off)}  MOV W0, #0x428A2F98")    # K[0]
    lines.append(f"{addr(base, off+1)}  MOV W1, #0x71374491")  # K[1]
    lines.append(f"{addr(base, off+2)}  MOV W2, #0xB5C0FBCF")  # K[2]
    lines.append(f"{addr(base, off+3)}  MOV W3, #0x6A09E667")  # H0
    lines.append(f"{addr(base, off+4)}  SHA256H Q0, Q1, V2.4S")
    lines.append(f"{addr(base, off+5)}  SHA256H2 Q1, Q0, V3.4S")
    lines.append(f"{addr(base, off+6)}  SHA256SU0 V4.4S, V5.4S")
    lines.append(f"{addr(base, off+7)}  SHA256SU1 V4.4S, V6.4S, V7.4S")
    lines.append(f"{addr(base, off+8)}  ROR W4, W5, #2")       # Sigma0
    lines.append(f"{addr(base, off+9)}  ROR W6, W7, #13")      # Sigma1
    lines.append(f"{addr(base, off+10)}  ROR W8, W9, #22")

    lines.extend(noise_instructions(base, off + 11, 20))

    return lines


def main():
    os.makedirs(TRACE_DIR, exist_ok=True)

    trace1 = generate_aes_chacha_trace()
    path1 = os.path.join(TRACE_DIR, "aes_chacha_trace.log")
    with open(path1, "w") as f:
        f.write("\n".join(trace1) + "\n")
    print(f"[+] Generated {path1} ({len(trace1)} lines)")

    trace2 = generate_des_sha256_trace()
    path2 = os.path.join(TRACE_DIR, "des_sha256_trace.log")
    with open(path2, "w") as f:
        f.write("\n".join(trace2) + "\n")
    print(f"[+] Generated {path2} ({len(trace2)} lines)")


if __name__ == "__main__":
    main()
