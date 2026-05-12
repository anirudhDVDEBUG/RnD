#!/usr/bin/env python3
"""
shebang_builder.py — Create executable LLM shebang scripts from the command line.

Generates either fragment-mode (-f) or template-mode (-t) scripts,
sets them executable, and optionally validates the shebang syntax.
"""

import argparse
import os
import stat
import sys
import yaml


def build_fragment_script(prompt: str, tools: list[str] | None = None) -> str:
    """Build a plain-text fragment script with #!/usr/bin/env -S llm -f shebang."""
    tool_flags = ""
    if tools:
        tool_flags = " " + " ".join(f"-T {t}" for t in tools)
    return f"#!/usr/bin/env -S llm{tool_flags} -f\n{prompt}\n"


def build_template_script(
    prompt: str,
    model: str = "claude-sonnet-4-6",
    system: str | None = None,
    functions_code: str | None = None,
) -> str:
    """Build a YAML template script with #!/usr/bin/env -S llm -t shebang."""
    template: dict = {"model": model}
    if system:
        template["system"] = system
    if prompt:
        template["prompt"] = prompt
    if functions_code:
        template["functions"] = functions_code

    yaml_body = yaml.dump(template, default_flow_style=False, sort_keys=False)
    return f"#!/usr/bin/env -S llm -t\n{yaml_body}"


def make_executable(path: str) -> None:
    """Add executable permission to a file."""
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def validate_shebang(path: str) -> dict:
    """Parse and validate a shebang script, returning its metadata."""
    with open(path) as f:
        first_line = f.readline().rstrip("\n")
        body = f.read()

    result = {"path": path, "valid": False, "mode": None, "tools": [], "body": ""}

    if not first_line.startswith("#!"):
        result["error"] = "Missing shebang line"
        return result

    if "llm" not in first_line:
        result["error"] = "Shebang does not invoke llm"
        return result

    parts = first_line.split()
    if "-f" in parts:
        result["mode"] = "fragment"
    elif "-t" in parts:
        result["mode"] = "template"
    else:
        result["error"] = "Missing -f or -t flag"
        return result

    result["tools"] = [parts[i + 1] for i, p in enumerate(parts) if p == "-T" and i + 1 < len(parts)]
    result["body"] = body.strip()
    result["valid"] = True

    if result["mode"] == "template":
        try:
            parsed = yaml.safe_load(body)
            result["template_keys"] = list(parsed.keys()) if isinstance(parsed, dict) else []
        except yaml.YAMLError as e:
            result["error"] = f"Invalid YAML: {e}"
            result["valid"] = False

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Build and validate LLM shebang scripts"
    )
    sub = parser.add_subparsers(dest="command")

    # create subcommand
    create_p = sub.add_parser("create", help="Create a new shebang script")
    create_p.add_argument("output", help="Output file path")
    create_p.add_argument("prompt", help="The prompt text")
    create_p.add_argument(
        "--mode", choices=["fragment", "template"], default="fragment",
        help="Script mode (default: fragment)"
    )
    create_p.add_argument("--model", default="claude-sonnet-4-6", help="Model for template mode")
    create_p.add_argument("--system", help="System prompt for template mode")
    create_p.add_argument("--tools", nargs="*", help="Tool plugins to enable")
    create_p.add_argument("--functions", help="Python functions code for template mode")

    # validate subcommand
    validate_p = sub.add_parser("validate", help="Validate an existing shebang script")
    validate_p.add_argument("files", nargs="+", help="Script files to validate")

    args = parser.parse_args()

    if args.command == "create":
        if args.mode == "fragment":
            content = build_fragment_script(args.prompt, args.tools)
        else:
            content = build_template_script(
                args.prompt, args.model, args.system, args.functions
            )
        with open(args.output, "w") as f:
            f.write(content)
        make_executable(args.output)
        print(f"Created {args.mode} script: {args.output}")
        print(f"Run it with: ./{args.output}")

    elif args.command == "validate":
        for filepath in args.files:
            info = validate_shebang(filepath)
            status = "VALID" if info["valid"] else "INVALID"
            print(f"[{status}] {filepath}")
            if info.get("mode"):
                print(f"  Mode: {info['mode']}")
            if info.get("tools"):
                print(f"  Tools: {', '.join(info['tools'])}")
            if info.get("template_keys"):
                print(f"  Template keys: {', '.join(info['template_keys'])}")
            if info.get("error"):
                print(f"  Error: {info['error']}")
            print()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
