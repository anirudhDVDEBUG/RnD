"""Mock CVE data for offline demonstration. Real usage would query NVD/MITRE APIs."""

MOCK_CVES = {
    "CVE-2024-3094": {
        "id": "CVE-2024-3094",
        "summary": "Malicious code was discovered in the upstream tarballs of xz-utils, starting with version 5.6.0. The backdoor manipulates the liblzma build process to inject code into the resulting library, enabling unauthorized access via sshd.",
        "cvss_score": 10.0,
        "severity": "CRITICAL",
        "attack_vector": "Network",
        "cwe": "CWE-506: Embedded Malicious Code",
        "affected_product": "xz-utils",
        "affected_versions": ">=5.6.0, <=5.6.1",
        "affected_version_ranges": [("5.6.0", "5.6.1")],
        "fixed_version": "5.6.2 or downgrade to 5.4.x",
        "references": [
            "https://nvd.nist.gov/vuln/detail/CVE-2024-3094",
            "https://www.openwall.com/lists/oss-security/2024/03/29/4",
        ],
        "known_exploits": True,
        "dependency_names": ["xz-utils", "liblzma", "xz"],
    },
    "CVE-2024-21626": {
        "id": "CVE-2024-21626",
        "summary": "runc through 1.1.11 has a container breakout vulnerability due to leaked file descriptors. An attacker can use a specially crafted image or Dockerfile to break out of a container and gain host access.",
        "cvss_score": 8.6,
        "severity": "HIGH",
        "attack_vector": "Local",
        "cwe": "CWE-403: Exposure of File Descriptor to Unintended Control Sphere",
        "affected_product": "runc",
        "affected_versions": ">=1.0.0, <=1.1.11",
        "affected_version_ranges": [("1.0.0", "1.1.11")],
        "fixed_version": "1.1.12",
        "references": [
            "https://nvd.nist.gov/vuln/detail/CVE-2024-21626",
            "https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv",
        ],
        "known_exploits": True,
        "dependency_names": ["runc"],
    },
    "CVE-2024-29944": {
        "id": "CVE-2024-29944",
        "summary": "An attacker was able to inject an event handler into a privileged object in Firefox that would allow arbitrary JavaScript execution in the parent process.",
        "cvss_score": 9.8,
        "severity": "CRITICAL",
        "attack_vector": "Network",
        "cwe": "CWE-94: Improper Control of Generation of Code",
        "affected_product": "Firefox",
        "affected_versions": "<124.0.1",
        "affected_version_ranges": [("0.0.0", "124.0.0")],
        "fixed_version": "124.0.1",
        "references": [
            "https://nvd.nist.gov/vuln/detail/CVE-2024-29944",
            "https://www.mozilla.org/en-US/security/advisories/mfsa2024-15/",
        ],
        "known_exploits": False,
        "dependency_names": ["firefox"],
    },
    "CVE-2023-44487": {
        "id": "CVE-2023-44487",
        "summary": "The HTTP/2 protocol allows a denial of service (server resource consumption) via rapid stream resets (Rapid Reset Attack). Multiple implementations are affected.",
        "cvss_score": 7.5,
        "severity": "HIGH",
        "attack_vector": "Network",
        "cwe": "CWE-400: Uncontrolled Resource Consumption",
        "affected_product": "Multiple HTTP/2 implementations",
        "affected_versions": "Various (see vendor advisories)",
        "affected_version_ranges": [],
        "fixed_version": "See vendor advisories",
        "references": [
            "https://nvd.nist.gov/vuln/detail/CVE-2023-44487",
            "https://cloud.google.com/blog/products/identity-security/how-it-happens/",
        ],
        "known_exploits": True,
        "dependency_names": ["nginx", "apache2", "h2", "hyper", "grpc", "nodejs", "node"],
    },
    "CVE-2024-4577": {
        "id": "CVE-2024-4577",
        "summary": "PHP CGI argument injection vulnerability allows remote attackers to execute arbitrary commands on Windows servers running PHP in CGI mode.",
        "cvss_score": 9.8,
        "severity": "CRITICAL",
        "attack_vector": "Network",
        "cwe": "CWE-78: OS Command Injection",
        "affected_product": "PHP (CGI mode on Windows)",
        "affected_versions": "<8.1.29, <8.2.20, <8.3.8",
        "affected_version_ranges": [("8.0.0", "8.1.28"), ("8.2.0", "8.2.19"), ("8.3.0", "8.3.7")],
        "fixed_version": "8.1.29, 8.2.20, or 8.3.8",
        "references": [
            "https://nvd.nist.gov/vuln/detail/CVE-2024-4577",
            "https://www.php.net/ChangeLog-8.php",
        ],
        "known_exploits": True,
        "dependency_names": ["php", "php-cgi"],
    },
}


# Sample project dependency files for demo
SAMPLE_REQUIREMENTS_TXT = """\
flask==3.0.2
requests==2.31.0
pyyaml==6.0.1
cryptography==42.0.5
"""

SAMPLE_PACKAGE_JSON = """\
{
  "name": "demo-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21",
    "axios": "^1.6.7"
  }
}
"""

SAMPLE_GOMOD = """\
module example.com/myapp

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/ulikunitz/xz v5.6.0
    google.golang.org/grpc v1.60.0
)
"""
