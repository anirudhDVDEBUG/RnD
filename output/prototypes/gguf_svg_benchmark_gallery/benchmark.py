"""Run SVG generation prompt against multiple GGUF model files via the llm CLI."""

import os
import subprocess
import sys
import argparse


def run_benchmark(models_dir: str, prompt: str, output_dir: str) -> list:
    """Run prompt against each .gguf file in models_dir, save SVG outputs."""
    os.makedirs(output_dir, exist_ok=True)

    gguf_files = sorted(
        [f for f in os.listdir(models_dir) if f.endswith(".gguf")],
        key=lambda f: os.path.getsize(os.path.join(models_dir, f))
    )

    if not gguf_files:
        print(f"[!] No .gguf files found in {models_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Found {len(gguf_files)} GGUF files in {models_dir}")
    results = []

    for gguf_file in gguf_files:
        model_path = os.path.join(models_dir, gguf_file)
        name = gguf_file.replace(".gguf", "")
        output_path = os.path.join(output_dir, f"{name}.svg")

        print(f"[*] Running: {name} ({os.path.getsize(model_path) / 1e9:.2f} GB)...")

        try:
            result = subprocess.run(
                ["llm", "-m", f"gguf:{model_path}", prompt],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode != 0:
                print(f"    [WARN] llm returned non-zero for {name}: {result.stderr[:200]}")
                continue

            svg_output = result.stdout.strip()
            # Try to extract SVG if wrapped in markdown code blocks
            if "```" in svg_output:
                lines = svg_output.split("\n")
                in_block = False
                svg_lines = []
                for line in lines:
                    if line.strip().startswith("```") and not in_block:
                        in_block = True
                        continue
                    elif line.strip() == "```" and in_block:
                        break
                    elif in_block:
                        svg_lines.append(line)
                if svg_lines:
                    svg_output = "\n".join(svg_lines)

            with open(output_path, "w") as f:
                f.write(svg_output)

            size = len(svg_output)
            print(f"    [OK] Saved {output_path} ({size} bytes)")
            results.append({"name": name, "path": output_path, "size": size})

        except subprocess.TimeoutExpired:
            print(f"    [TIMEOUT] Skipping {name}")
        except FileNotFoundError:
            print("[!] 'llm' CLI not found. Install with: pip install llm llm-gguf", file=sys.stderr)
            sys.exit(1)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark GGUF models on SVG generation")
    parser.add_argument("--models-dir", required=True, help="Directory containing .gguf files")
    parser.add_argument("--prompt", default="Generate an SVG of a pelican riding a bicycle", help="Prompt to send")
    parser.add_argument("--output-dir", default="output", help="Directory to save SVG outputs")
    args = parser.parse_args()

    results = run_benchmark(args.models_dir, args.prompt, args.output_dir)
    print(f"\n[*] Done. {len(results)} SVGs generated in {args.output_dir}/")
    print("[*] Run: python gallery_builder.py --input-dir", args.output_dir)
