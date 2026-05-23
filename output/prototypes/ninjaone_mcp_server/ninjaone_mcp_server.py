"""
NinjaOne MCP Server — Python mock/demo implementation.

Simulates the Bezalu.NinjaOne.MCP server's capabilities using mock data,
demonstrating the MCP tool surface without requiring live NinjaOne credentials.
"""

import json
import sys
import os
from datetime import datetime, timedelta
import random

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

ORGANIZATIONS = [
    {"id": 1, "name": "Acme Corp", "description": "Technology company", "nodeCount": 47},
    {"id": 2, "name": "Globex Industries", "description": "Manufacturing", "nodeCount": 123},
    {"id": 3, "name": "Initech Solutions", "description": "IT consulting", "nodeCount": 31},
    {"id": 4, "name": "Stark Medical", "description": "Healthcare provider", "nodeCount": 89},
]

DEVICES = [
    {"id": 101, "orgId": 1, "systemName": "ACME-WS-001", "dnsName": "ws001.acme.local", "os": "Windows 11 Pro 23H2", "status": "online", "lastContact": "2026-05-23T08:12:00Z", "role": "WINDOWS_WORKSTATION"},
    {"id": 102, "orgId": 1, "systemName": "ACME-SRV-DC01", "dnsName": "dc01.acme.local", "os": "Windows Server 2022", "status": "online", "lastContact": "2026-05-23T08:15:00Z", "role": "WINDOWS_SERVER"},
    {"id": 103, "orgId": 2, "systemName": "GLX-MAC-042", "dnsName": "mac042.globex.local", "os": "macOS 15.2", "status": "offline", "lastContact": "2026-05-22T17:30:00Z", "role": "MAC"},
    {"id": 104, "orgId": 2, "systemName": "GLX-SRV-APP01", "dnsName": "app01.globex.local", "os": "Ubuntu 24.04 LTS", "status": "online", "lastContact": "2026-05-23T08:14:00Z", "role": "LINUX_SERVER"},
    {"id": 105, "orgId": 3, "systemName": "INIT-WS-007", "dnsName": "ws007.initech.local", "os": "Windows 11 Pro 24H2", "status": "online", "lastContact": "2026-05-23T08:10:00Z", "role": "WINDOWS_WORKSTATION"},
    {"id": 106, "orgId": 4, "systemName": "STARK-SRV-EMR", "dnsName": "emr.stark.local", "os": "Windows Server 2022", "status": "online", "lastContact": "2026-05-23T08:13:00Z", "role": "WINDOWS_SERVER"},
]

ALERTS = [
    {"id": 1001, "deviceId": 103, "severity": "CRITICAL", "message": "Device offline for >12 hours", "created": "2026-05-22T17:30:00Z", "status": "ACTIVE"},
    {"id": 1002, "deviceId": 102, "severity": "WARNING", "message": "Disk usage above 85% on C:", "created": "2026-05-23T06:00:00Z", "status": "ACTIVE"},
    {"id": 1003, "deviceId": 106, "severity": "WARNING", "message": "Windows Update pending reboot", "created": "2026-05-23T03:00:00Z", "status": "ACTIVE"},
    {"id": 1004, "deviceId": 101, "severity": "INFO", "message": "Antivirus definitions updated", "created": "2026-05-23T07:00:00Z", "status": "RESOLVED"},
]

ACTIVITIES = [
    {"id": 5001, "deviceId": 102, "type": "SYSTEM", "message": "Scheduled backup completed", "timestamp": "2026-05-23T04:00:00Z"},
    {"id": 5002, "deviceId": 104, "type": "PATCH", "message": "Security patch applied: CVE-2026-1234", "timestamp": "2026-05-23T05:30:00Z"},
    {"id": 5003, "deviceId": 101, "type": "SOFTWARE", "message": "Chrome updated to 130.0.6723.92", "timestamp": "2026-05-23T07:15:00Z"},
    {"id": 5004, "deviceId": 106, "type": "ALERT", "message": "Alert triggered: pending reboot", "timestamp": "2026-05-23T03:00:00Z"},
    {"id": 5005, "deviceId": 103, "type": "SYSTEM", "message": "Device went offline", "timestamp": "2026-05-22T17:30:00Z"},
]

SOFTWARE_INVENTORY = {
    101: [
        {"name": "Google Chrome", "version": "130.0.6723.92", "publisher": "Google LLC"},
        {"name": "Microsoft 365 Apps", "version": "16.0.18324", "publisher": "Microsoft"},
        {"name": "Zoom", "version": "6.3.1", "publisher": "Zoom Video Communications"},
        {"name": "Visual Studio Code", "version": "1.98.2", "publisher": "Microsoft"},
    ],
    102: [
        {"name": "SQL Server 2022", "version": "16.0.4155", "publisher": "Microsoft"},
        {"name": "Windows Admin Center", "version": "2.3.0", "publisher": "Microsoft"},
    ],
    104: [
        {"name": "nginx", "version": "1.27.3", "publisher": "Nginx Inc"},
        {"name": "PostgreSQL", "version": "17.2", "publisher": "PostgreSQL Global Dev Group"},
        {"name": "Docker Engine", "version": "27.5.1", "publisher": "Docker Inc"},
    ],
}

OS_PATCHES = {
    101: [
        {"kb": "KB5044384", "title": "2026-05 Cumulative Update for Windows 11", "status": "INSTALLED", "installedOn": "2026-05-14"},
        {"kb": "KB5044901", "title": "2026-05 .NET 8.0.12 Update", "status": "INSTALLED", "installedOn": "2026-05-15"},
    ],
    102: [
        {"kb": "KB5044380", "title": "2026-05 Security Update for Windows Server 2022", "status": "PENDING_REBOOT", "installedOn": None},
        {"kb": "KB5044910", "title": "2026-05 Servicing Stack Update", "status": "INSTALLED", "installedOn": "2026-05-13"},
    ],
    106: [
        {"kb": "KB5044380", "title": "2026-05 Security Update for Windows Server 2022", "status": "PENDING_REBOOT", "installedOn": None},
    ],
}

# ---------------------------------------------------------------------------
# MCP tool handlers
# ---------------------------------------------------------------------------

def list_organizations(**kwargs):
    """List all organizations managed in NinjaOne."""
    return {"organizations": ORGANIZATIONS, "totalCount": len(ORGANIZATIONS)}


def get_devices(org_id=None, status=None, **kwargs):
    """Get devices/endpoints, optionally filtered by org or status."""
    results = DEVICES
    if org_id is not None:
        results = [d for d in results if d["orgId"] == int(org_id)]
    if status is not None:
        results = [d for d in results if d["status"] == status.lower()]
    return {"devices": results, "totalCount": len(results)}


def get_alerts(severity=None, status=None, **kwargs):
    """Get alerts, optionally filtered by severity or status."""
    results = ALERTS
    if severity:
        results = [a for a in results if a["severity"] == severity.upper()]
    if status:
        results = [a for a in results if a["status"] == status.upper()]
    return {"alerts": results, "totalCount": len(results)}


def get_activities(device_id=None, limit=10, **kwargs):
    """Get recent activity log entries."""
    results = ACTIVITIES
    if device_id is not None:
        results = [a for a in results if a["deviceId"] == int(device_id)]
    return {"activities": results[:int(limit)], "totalCount": len(results)}


def get_software_inventory(device_id, **kwargs):
    """List installed software on a specific device."""
    device_id = int(device_id)
    sw = SOFTWARE_INVENTORY.get(device_id, [])
    device = next((d for d in DEVICES if d["id"] == device_id), None)
    return {
        "deviceId": device_id,
        "deviceName": device["systemName"] if device else "Unknown",
        "software": sw,
        "totalCount": len(sw),
    }


def get_os_patches(device_id, **kwargs):
    """Check OS patch status for a device."""
    device_id = int(device_id)
    patches = OS_PATCHES.get(device_id, [])
    device = next((d for d in DEVICES if d["id"] == device_id), None)
    return {
        "deviceId": device_id,
        "deviceName": device["systemName"] if device else "Unknown",
        "patches": patches,
        "totalCount": len(patches),
    }


# ---------------------------------------------------------------------------
# Tool registry (mirrors what the real MCP server exposes)
# ---------------------------------------------------------------------------

TOOLS = {
    "list_organizations": {
        "handler": list_organizations,
        "description": "List all NinjaOne organizations",
        "parameters": {},
    },
    "get_devices": {
        "handler": get_devices,
        "description": "Get devices/endpoints from NinjaOne",
        "parameters": {"org_id": "Filter by organization ID", "status": "Filter by status (online/offline)"},
    },
    "get_alerts": {
        "handler": get_alerts,
        "description": "Get alerts from monitored endpoints",
        "parameters": {"severity": "Filter by severity (CRITICAL/WARNING/INFO)", "status": "Filter by status (ACTIVE/RESOLVED)"},
    },
    "get_activities": {
        "handler": get_activities,
        "description": "Query activity logs and events",
        "parameters": {"device_id": "Filter by device ID", "limit": "Max results (default 10)"},
    },
    "get_software_inventory": {
        "handler": get_software_inventory,
        "description": "List installed software on a device",
        "parameters": {"device_id": "(required) Device ID"},
    },
    "get_os_patches": {
        "handler": get_os_patches,
        "description": "Check OS patch status for a device",
        "parameters": {"device_id": "(required) Device ID"},
    },
}

# ---------------------------------------------------------------------------
# Demo runner
# ---------------------------------------------------------------------------

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_json(data):
    print(json.dumps(data, indent=2))


def run_demo():
    """Run an interactive demo of all MCP tools with mock data."""

    print("=" * 60)
    print("  NinjaOne MCP Server — Mock Demo")
    print("  Simulating Bezalu.NinjaOne.MCP tool surface")
    print("=" * 60)

    # 1. Organizations
    print_section("Tool: list_organizations")
    print("Query: 'List all organizations in NinjaOne'")
    result = list_organizations()
    print_json(result)

    # 2. Devices for a specific org
    print_section("Tool: get_devices (org_id=2)")
    print("Query: 'Show me all Globex Industries devices'")
    result = get_devices(org_id=2)
    print_json(result)

    # 3. Offline devices
    print_section("Tool: get_devices (status=offline)")
    print("Query: 'Which devices are currently offline?'")
    result = get_devices(status="offline")
    print_json(result)

    # 4. Active alerts
    print_section("Tool: get_alerts (status=ACTIVE)")
    print("Query: 'Show me devices with active alerts'")
    result = get_alerts(status="ACTIVE")
    print_json(result)

    # 5. Critical alerts
    print_section("Tool: get_alerts (severity=CRITICAL)")
    print("Query: 'Are there any critical alerts?'")
    result = get_alerts(severity="CRITICAL")
    print_json(result)

    # 6. Activities
    print_section("Tool: get_activities")
    print("Query: 'Show recent activity across all devices'")
    result = get_activities()
    print_json(result)

    # 7. Software inventory
    print_section("Tool: get_software_inventory (device_id=101)")
    print("Query: 'What software is installed on ACME-WS-001?'")
    result = get_software_inventory(device_id=101)
    print_json(result)

    # 8. OS patches
    print_section("Tool: get_os_patches (device_id=102)")
    print("Query: 'Show patch status for ACME-SRV-DC01'")
    result = get_os_patches(device_id=102)
    print_json(result)

    # Summary
    print_section("Summary")
    total_devices = len(DEVICES)
    online = sum(1 for d in DEVICES if d["status"] == "online")
    active_alerts = sum(1 for a in ALERTS if a["status"] == "ACTIVE")
    critical = sum(1 for a in ALERTS if a["severity"] == "CRITICAL" and a["status"] == "ACTIVE")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Devices:        {total_devices} ({online} online, {total_devices - online} offline)")
    print(f"  Active alerts:  {active_alerts} ({critical} critical)")
    print(f"  Tools exposed:  {len(TOOLS)}")
    print()
    print("  This demo uses mock data. The real Bezalu.NinjaOne.MCP server")
    print("  connects to NinjaOne's REST API with OAuth2 client credentials")
    print("  and exposes these same tools over the MCP stdio protocol.")
    print()


if __name__ == "__main__":
    run_demo()
