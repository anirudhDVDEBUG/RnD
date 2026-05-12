"""Defensive security utilities (localhost only)."""
import socket
import platform
import os


def scan_localhost_ports(ports=None):
    """Scan common ports on localhost for defensive awareness."""
    if ports is None:
        ports = [22, 80, 443, 3000, 5000, 8000, 8080, 8443, 9090]
    results = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        status = "open" if sock.connect_ex(("127.0.0.1", port)) == 0 else "closed"
        results.append({"port": port, "status": status})
        sock.close()
    return results


def system_info():
    """Gather basic system info for monitoring."""
    return {
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
        "pid": os.getpid(),
    }
