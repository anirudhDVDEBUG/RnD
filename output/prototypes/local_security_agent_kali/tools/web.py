"""Web scanning tool wrappers: Nikto, directory brute-force."""

import shlex
import subprocess

import config

_MOCK_NIKTO = """- Nikto v2.5.0
+ Target IP:       192.168.1.100
+ Target Hostname:  192.168.1.100
+ Target Port:      80
+ Server: Apache/2.4.49 (Ubuntu)
+ /: The anti-clickjacking X-Frame-Options header is not present.
+ /icons/README: Apache default file found.
+ /server-status: Apache server-status enabled.
+ OSVDB-3233: /icons/README: Apache default file found.
+ 7 items checked: 3 findings"""


def nikto_scan(target: str, port: str = "80") -> str:
    """Run Nikto against a web target."""
    if config.MOCK_MODE:
        return _MOCK_NIKTO

    cmd = f"nikto -h {shlex.quote(target)} -p {shlex.quote(str(port))}"
    result = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        text=True,
        timeout=config.TOOL_TIMEOUT,
    )
    return result.stdout or result.stderr
