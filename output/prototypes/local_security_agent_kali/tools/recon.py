"""Reconnaissance tool wrappers: nmap, whois, DNS enumeration."""

import shlex
import subprocess

import config

# ---------------------------------------------------------------------------
# Mock outputs for demo mode
# ---------------------------------------------------------------------------
_MOCK_NMAP = """Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.100
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.9p1 Ubuntu
80/tcp   open  http     Apache httpd 2.4.49
3306/tcp open  mysql    MySQL 8.0.28
Service detection performed. 3 services recognized.
Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds"""

_MOCK_WHOIS = """Domain Name: EXAMPLE.COM
Registrar: Example Registrar, Inc.
Creation Date: 1995-08-14T04:00:00Z
Name Server: NS1.EXAMPLE.COM"""


def nmap_scan(target: str, flags: str = "-sV -sC") -> str:
    """Run an nmap scan and return stdout."""
    if config.MOCK_MODE:
        return _MOCK_NMAP

    cmd = f"nmap {flags} {shlex.quote(target)}"
    result = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        text=True,
        timeout=config.TOOL_TIMEOUT,
    )
    return result.stdout or result.stderr


def whois_lookup(target: str) -> str:
    """Run a whois lookup."""
    if config.MOCK_MODE:
        return _MOCK_WHOIS

    result = subprocess.run(
        ["whois", target],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.stdout or result.stderr
