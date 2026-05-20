#!/usr/bin/env python3
"""CLI entry point for Content Provenance Verifier."""

import glob
import json
import os
import sys

from verifier import ProvenanceVerifier
from signer import ProvenanceSigner
from report import format_report, format_summary
from source_types import SOURCE_TYPES


def cmd_verify(path: str):
    v = ProvenanceVerifier()
    result = v.verify(path)
    print(format_report(result))


def cmd_verify_all():
    v = ProvenanceVerifier()
    results = []
    for path in sorted(glob.glob("samples/*.json")):
        result = v.verify(path)
        results.append(result)
        print(format_report(result))
    print(format_summary(results))


def cmd_report(path: str):
    v = ProvenanceVerifier()
    result = v.verify(path)
    print(format_report(result))
    if result.manifest:
        print("\nRaw manifest:")
        print(json.dumps({
            "claim_generator": result.manifest.claim_generator,
            "title": result.manifest.title,
            "source_type": result.source_type,
            "is_ai_generated": result.is_ai_generated,
            "trust_status": result.trust_status,
            "assertions": [{"label": a.label, "data": a.data} for a in result.manifest.assertions],
            "ingredients": result.manifest.ingredients,
        }, indent=2))


def cmd_source_types():
    print("\nIPTC Digital Source Types supported:\n")
    for key, info in SOURCE_TYPES.items():
        ai_tag = " [AI]" if info["is_ai"] else ""
        print(f"  {key}{ai_tag}")
        print(f"    {info['description']}")
        print()


def cmd_sign_demo():
    """Demonstrate signing a file with Content Credentials."""
    signer = ProvenanceSigner(generator="DemoApp/1.0")
    out_path = "samples/newly_signed.json"
    # Create a tiny mock input file
    mock_input = "samples/_mock_input.txt"
    with open(mock_input, "w") as f:
        f.write("This is mock image content for signing demo.")
    result = signer.sign(mock_input, out_path, source_type="trainedAlgorithmicMedia")
    print("\n--- Signing Demo ---")
    print(f"Signed mock file -> {out_path}")
    print(f"Generator: {result['manifest']['claim_generator']}")
    print(f"Source type: trainedAlgorithmicMedia (AI-generated)")
    print(f"Signature hash: {result['manifest']['signature']['hash']}")

    # Now verify what we just signed
    v = ProvenanceVerifier()
    vr = v.verify(out_path)
    print("\nVerification of newly signed file:")
    print(format_report(vr))

    # Clean up mock input
    os.remove(mock_input)


def fix_sample_hashes():
    """Ensure sample manifest hashes are correct for demo verification."""
    import hashlib
    for path in sorted(glob.glob("samples/*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        manifest = data.get("manifest", {})
        if not manifest or "signature" not in manifest:
            continue
        m_copy = dict(manifest)
        m_copy.pop("signature", None)
        h = hashlib.sha256(json.dumps(m_copy, sort_keys=True).encode()).hexdigest()[:16]
        if manifest["signature"].get("hash") != h:
            manifest["signature"]["hash"] = h
            with open(path, "w") as f:
                json.dump(data, f, indent=2)


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [args]")
        print("Commands: verify <file>, verify-all, report <file>, source-types, sign-demo")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "verify" and len(sys.argv) >= 3:
        cmd_verify(sys.argv[2])
    elif cmd == "verify-all":
        cmd_verify_all()
    elif cmd == "report" and len(sys.argv) >= 3:
        cmd_report(sys.argv[2])
    elif cmd == "source-types":
        cmd_source_types()
    elif cmd == "sign-demo":
        cmd_sign_demo()
    elif cmd == "fix-hashes":
        fix_sample_hashes()
        print("Sample hashes fixed.")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
