#!/usr/bin/env python3
"""
Cloudflare Tunnel Route Manager

CLI tool for managing Cloudflare Tunnel ingress routes.
Add, remove, and list persistent HTTPS subdomains for any local port
without touching the Cloudflare dashboard.
"""

import argparse
import os
import subprocess
import sys
import copy

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


DEFAULT_CONFIG_PATH = os.path.expanduser("~/.cloudflared/config.yml")
CATCH_ALL_RULE = {"service": "http_status:404"}


def load_config(config_path):
    """Load and parse the cloudflared config file."""
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        print("Create a tunnel first: cloudflared tunnel create <name>")
        sys.exit(1)
    with open(config_path, "r") as f:
        return yaml.safe_load(f) or {}


def save_config(config_path, config):
    """Write config back to the YAML file."""
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f"Config saved to {config_path}")


def list_routes(config_path):
    """List all current ingress routes."""
    config = load_config(config_path)
    ingress = config.get("ingress", [])

    if not ingress:
        print("No ingress routes configured.")
        return

    print(f"\n{'#':<4} {'Hostname':<40} {'Service':<30}")
    print("-" * 74)
    for i, rule in enumerate(ingress, 1):
        hostname = rule.get("hostname", "(catch-all)")
        service = rule.get("service", "N/A")
        print(f"{i:<4} {hostname:<40} {service:<30}")
    print()


def add_route(config_path, hostname, service, no_dns=False, tunnel_name=None):
    """Add a new ingress route."""
    config = load_config(config_path)

    if "ingress" not in config:
        config["ingress"] = [CATCH_ALL_RULE]

    # Check for duplicate hostname
    for rule in config["ingress"]:
        if rule.get("hostname") == hostname:
            print(f"Error: Route for '{hostname}' already exists.")
            print("Remove it first with: tunnel_manager remove <hostname>")
            sys.exit(1)

    new_rule = {"hostname": hostname, "service": service}

    # Insert before catch-all (last entry)
    config["ingress"].insert(-1, new_rule)
    save_config(config_path, config)

    print(f"Added route: {hostname} -> {service}")

    # Optionally create DNS route
    if not no_dns and tunnel_name:
        subdomain = hostname.split(".")[0]
        print(f"\nCreating DNS route for '{subdomain}' via tunnel '{tunnel_name}'...")
        try:
            subprocess.run(
                ["cloudflared", "tunnel", "route", "dns", tunnel_name, subdomain],
                check=True,
            )
            print("DNS route created successfully.")
        except FileNotFoundError:
            print("Warning: 'cloudflared' not found. DNS route not created.")
            print(f"Run manually: cloudflared tunnel route dns {tunnel_name} {subdomain}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: DNS route creation failed: {e}")
    elif not no_dns and not tunnel_name:
        print("Tip: Pass --tunnel <name> to auto-create the DNS route.")

    print("\nRestart the tunnel to apply: cloudflared tunnel run <name>")


def remove_route(config_path, hostname):
    """Remove an ingress route by hostname."""
    config = load_config(config_path)
    ingress = config.get("ingress", [])

    original_len = len(ingress)
    config["ingress"] = [
        r for r in ingress if r.get("hostname") != hostname
    ]

    if len(config["ingress"]) == original_len:
        print(f"No route found for hostname '{hostname}'.")
        sys.exit(1)

    # Ensure catch-all still exists
    if not config["ingress"] or config["ingress"][-1] != CATCH_ALL_RULE:
        config["ingress"].append(CATCH_ALL_RULE)

    save_config(config_path, config)
    print(f"Removed route for '{hostname}'.")
    print("Restart the tunnel to apply: cloudflared tunnel run <name>")


def init_config(config_path, tunnel_uuid, credentials_file=None):
    """Initialize a basic tunnel config file."""
    if os.path.exists(config_path):
        print(f"Config already exists at {config_path}")
        print("Use --force to overwrite (not implemented for safety).")
        sys.exit(1)

    config = {
        "tunnel": tunnel_uuid,
        "credentials-file": credentials_file
        or os.path.expanduser(f"~/.cloudflared/{tunnel_uuid}.json"),
        "ingress": [CATCH_ALL_RULE],
    }

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    save_config(config_path, config)
    print(f"Initialized config for tunnel {tunnel_uuid}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage Cloudflare Tunnel ingress routes from the CLI."
    )
    parser.add_argument(
        "-c", "--config",
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to cloudflared config file (default: {DEFAULT_CONFIG_PATH})",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    subparsers.add_parser("list", help="List all ingress routes")

    # add
    add_parser = subparsers.add_parser("add", help="Add an ingress route")
    add_parser.add_argument("hostname", help="Full hostname (e.g., myapp.example.com)")
    add_parser.add_argument("service", help="Local service URL (e.g., http://localhost:8000)")
    add_parser.add_argument("--tunnel", help="Tunnel name (for auto DNS route creation)")
    add_parser.add_argument("--no-dns", action="store_true", help="Skip DNS route creation")

    # remove
    rm_parser = subparsers.add_parser("remove", help="Remove an ingress route")
    rm_parser.add_argument("hostname", help="Hostname to remove")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize a tunnel config")
    init_parser.add_argument("tunnel_uuid", help="Tunnel UUID")
    init_parser.add_argument("--credentials", help="Path to credentials file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list":
        list_routes(args.config)
    elif args.command == "add":
        add_route(args.config, args.hostname, args.service,
                  no_dns=args.no_dns, tunnel_name=args.tunnel)
    elif args.command == "remove":
        remove_route(args.config, args.hostname)
    elif args.command == "init":
        init_config(args.config, args.tunnel_uuid, args.credentials)


if __name__ == "__main__":
    main()
