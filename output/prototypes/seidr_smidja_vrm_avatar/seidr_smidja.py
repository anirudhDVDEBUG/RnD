#!/usr/bin/env python3
"""
Seidr-Smidja: AI-Agent-Driven VRM Avatar Generator

Generates VRM-format 3D avatars via CLI, API, or MCP interfaces.
This demo uses procedural mesh generation (no external AI models required).
"""

import argparse
import json
import os
import sys

from mesh_generator import generate_humanoid_mesh
from vrm_packager import package_vrm
from style_presets import resolve_style


def create_avatar(name="demo_avatar", style="anime", hair=None, eyes=None,
                  outfit=None, accessories=None, output_dir="output"):
    """Generate a VRM avatar with the given parameters."""
    print(f"[INIT] Seidr-Smidja VRM Generator v0.3.0")

    # Resolve style preset
    config = resolve_style(style, hair=hair, eyes=eyes,
                           outfit=outfit, accessories=accessories)
    print(f"[STYLE] Applying style preset: {style}")

    # Generate base mesh
    mesh_data = generate_humanoid_mesh(config)
    print(f"[MESH] Generating base mesh... {mesh_data['vertex_count']:,} vertices")

    # Create blendshapes
    blendshapes = [
        "neutral", "joy", "angry", "sorrow",
        "fun", "surprised", "blink_l", "blink_r"
    ]
    print(f"[BLEND] Creating blendshapes: {', '.join(blendshapes)}")

    # Configure spring bones
    spring_bone_count = config.get("spring_bones", 24)
    print(f"[BONE] Configuring spring bones: {spring_bone_count} chains (hair, clothing, accessories)")

    # Write VRM metadata
    print(f"[META] Writing VRM metadata (title, author, permissions)")

    # Package and export
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}.vrm")

    vrm_size = package_vrm(
        output_path=output_path,
        mesh_data=mesh_data,
        blendshapes=blendshapes,
        spring_bones=spring_bone_count,
        config=config,
        name=name
    )

    size_mb = vrm_size / (1024 * 1024)
    print(f"[EXPORT] Avatar saved: {output_path} ({size_mb:.1f} MB)")
    print(f"[DONE] VRM avatar ready for VRChat / VTube Studio / 3tene")

    return {
        "status": "success",
        "file": output_path,
        "stats": {
            "vertices": mesh_data["vertex_count"],
            "blendshapes": len(blendshapes),
            "spring_bones": spring_bone_count
        }
    }


def inspect_avatar(path):
    """Inspect a generated VRM file."""
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        return

    size = os.path.getsize(path)
    print(f"[INSPECT] {path}")
    print(f"  Size: {size / (1024*1024):.1f} MB")

    # Read the embedded metadata
    with open(path, "rb") as f:
        # Skip binary glTF header, read JSON chunk
        magic = f.read(4)
        if magic == b'glTF':
            f.read(8)  # version + length
            chunk_len = int.from_bytes(f.read(4), 'little')
            f.read(4)  # chunk type
            json_data = json.loads(f.read(chunk_len))
            meta = json_data.get("extensions", {}).get("VRM", {}).get("meta", {})
            print(f"  Title: {meta.get('title', 'Unknown')}")
            print(f"  Author: {meta.get('author', 'Unknown')}")
            print(f"  Meshes: {len(json_data.get('meshes', []))}")
            print(f"  Materials: {len(json_data.get('materials', []))}")
        else:
            print("  [Not a valid glTF/VRM file]")


def main():
    parser = argparse.ArgumentParser(description="Seidr-Smidja VRM Avatar Generator")
    parser.add_argument("--create", action="store_true", help="Create a new avatar")
    parser.add_argument("--inspect", type=str, help="Inspect an existing VRM file")
    parser.add_argument("--serve", action="store_true", help="Start API server")
    parser.add_argument("--mcp", action="store_true", help="Run as MCP server")
    parser.add_argument("--name", type=str, default="demo_avatar", help="Avatar name")
    parser.add_argument("--style", type=str, default="anime", help="Style preset")
    parser.add_argument("--hair", type=str, help="Hair style")
    parser.add_argument("--eyes", type=str, help="Eye style")
    parser.add_argument("--outfit", type=str, help="Outfit type")
    parser.add_argument("--accessories", type=str, help="Comma-separated accessories")
    parser.add_argument("--output", type=str, default="output", help="Output directory")
    parser.add_argument("--port", type=int, default=8080, help="API server port")

    args = parser.parse_args()

    if args.create:
        accessories = args.accessories.split(",") if args.accessories else None
        result = create_avatar(
            name=args.name,
            style=args.style,
            hair=args.hair,
            eyes=args.eyes,
            outfit=args.outfit,
            accessories=accessories,
            output_dir=args.output
        )
        print(json.dumps(result, indent=2))

    elif args.inspect:
        inspect_avatar(args.inspect)

    elif args.serve:
        print(f"[API] Starting server on port {args.port}...")
        from api_server import start_server
        start_server(port=args.port)

    elif args.mcp:
        print("[MCP] Starting MCP server on stdio...", file=sys.stderr)
        from mcp_handler import run_mcp
        run_mcp()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
