#!/usr/bin/env python3
"""
Cybrix Deploy Simulator
Demonstrates the deployment workflow that the Cybrix Claude Code skill performs.
Uses mock data — no API keys or Cybrix account needed.
"""

import os
import sys
import time
import json
import yaml

# --- Framework Detection ---

FRAMEWORK_SIGNATURES = {
    "next.config.js": ("nextjs", "Node.js (Next.js)", "npm run build", "npm start", 3000),
    "next.config.ts": ("nextjs", "Node.js (Next.js)", "npm run build", "npm start", 3000),
    "package.json": ("node", "Node.js", "npm run build", "npm start", 3000),
    "requirements.txt": ("python", "Python", "pip install -r requirements.txt", "python app.py", 8000),
    "Dockerfile": ("docker", "Docker", "docker build .", "docker run", 8080),
    "go.mod": ("go", "Go", "go build", "./app", 8080),
    "Cargo.toml": ("rust", "Rust", "cargo build --release", "./target/release/app", 8080),
    "index.html": ("static", "Static Site", "cp -r . /srv", "serve .", 80),
}


def detect_framework(project_dir):
    """Scan project directory for framework indicators."""
    for filename, info in FRAMEWORK_SIGNATURES.items():
        if os.path.exists(os.path.join(project_dir, filename)):
            return {
                "framework": info[0],
                "display_name": info[1],
                "build_command": info[2],
                "start_command": info[3],
                "port": info[4],
            }
    return None


# --- Config Generation ---

def generate_config(project_name, detection):
    """Generate a cybrix.yaml deployment config."""
    config = {
        "name": project_name,
        "framework": detection["framework"],
        "build_command": detection["build_command"],
        "start_command": detection["start_command"],
        "port": detection["port"],
        "auto_deploy": {
            "branch": "main",
            "enabled": True,
        },
        "env": {
            "NODE_ENV": "production" if detection["framework"] in ("nextjs", "node") else None,
        },
    }
    # Remove None env vars
    config["env"] = {k: v for k, v in config["env"].items() if v is not None}
    if not config["env"]:
        del config["env"]
    return config


# --- Simulated Deployment ---

def simulate_deploy(project_name, detection):
    """Simulate the Cybrix deployment process."""
    print(f"\n{'='*60}")
    print(f"  CYBRIX DEPLOY - Simulation")
    print(f"{'='*60}\n")

    # Detection phase
    print(f"[1/5] Scanning project...")
    time.sleep(0.3)
    print(f"      Detected: {detection['display_name']}")
    print(f"      Build:    {detection['build_command']}")
    print(f"      Start:    {detection['start_command']}")
    print(f"      Port:     {detection['port']}")

    # Config phase
    print(f"\n[2/5] Generating deployment config...")
    time.sleep(0.2)
    config = generate_config(project_name, detection)
    config_path = os.path.join(os.path.dirname(__file__), "cybrix.yaml")
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f"      Written: cybrix.yaml")

    # Build phase
    print(f"\n[3/5] Building image...")
    for i in range(5):
        time.sleep(0.2)
        sys.stdout.write(f"\r      Progress: [{'#' * (i+1)}{'.' * (4-i)}] {(i+1)*20}%")
        sys.stdout.flush()
    print(" done")

    # Provision phase
    print(f"\n[4/5] Provisioning resources...")
    time.sleep(0.3)
    print(f"      Region:   us-east-1")
    print(f"      Memory:   512MB")
    print(f"      CPU:      0.5 vCPU")

    # Health check
    print(f"\n[5/5] Health check...")
    time.sleep(0.2)
    print(f"      GET /health -> 200 OK")

    # Result
    app_url = f"https://{project_name}.cybrix.app"
    dashboard_url = f"https://dashboard.cybrix.app/projects/{project_name}"

    print(f"\n{'='*60}")
    print(f"  DEPLOYMENT SUCCESSFUL")
    print(f"{'='*60}")
    print(f"\n  Live URL:     {app_url}")
    print(f"  Dashboard:    {dashboard_url}")
    print(f"  Auto-deploy:  enabled (branch: main)")
    print(f"  Status:       running")
    print()

    # Return deployment info
    return {
        "status": "running",
        "url": app_url,
        "dashboard": dashboard_url,
        "deploy_id": "dpl_sim_abc123",
        "created_at": "2026-05-07T08:00:00Z",
    }


# --- Status Check ---

def simulate_status(project_name):
    """Simulate checking deployment status."""
    print(f"\n{'='*60}")
    print(f"  CYBRIX STATUS - {project_name}")
    print(f"{'='*60}\n")
    print(f"  Status:       running")
    print(f"  URL:          https://{project_name}.cybrix.app")
    print(f"  Uptime:       2h 34m")
    print(f"  Last deploy:  2026-05-07T08:00:00Z")
    print(f"  Requests/min: 142")
    print(f"  Memory:       128MB / 512MB")
    print(f"  CPU:          12% / 0.5 vCPU")
    print()


# --- Main ---

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_name = "demo-app"

    # Create a mock project file for detection
    mock_pkg = os.path.join(project_dir, "mock_project", "package.json")
    os.makedirs(os.path.dirname(mock_pkg), exist_ok=True)
    with open(mock_pkg, "w") as f:
        json.dump({
            "name": "demo-app",
            "version": "1.0.0",
            "scripts": {"build": "next build", "start": "next start"},
            "dependencies": {"next": "^14.0.0", "react": "^18.0.0"}
        }, f, indent=2)

    # Also create next.config.js for framework detection
    with open(os.path.join(project_dir, "mock_project", "next.config.js"), "w") as f:
        f.write("module.exports = { reactStrictMode: true };\n")

    # Detect
    mock_dir = os.path.join(project_dir, "mock_project")
    detection = detect_framework(mock_dir)

    if not detection:
        print("ERROR: Could not detect framework in project directory.")
        sys.exit(1)

    # Deploy
    result = simulate_deploy(project_name, detection)

    # Status
    simulate_status(project_name)

    # Summary
    print("--- Simulation complete. In production, this would hit the Cybrix API. ---")
    print(f"--- Generated cybrix.yaml shows the config that would be deployed.    ---\n")

    # Print the generated config
    print("Generated cybrix.yaml:")
    print("-" * 40)
    with open(os.path.join(project_dir, "cybrix.yaml")) as f:
        print(f.read())


if __name__ == "__main__":
    main()
