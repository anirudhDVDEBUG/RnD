#!/usr/bin/env python3
"""
CVE Triage — Should I Care?

Triages whether a CVE applies to your environment with sourced,
verifiable reasoning. Produces a structured applicability report.

Usage:
    python cve_triage.py CVE-2024-3094 [--project-dir /path/to/project]
    python cve_triage.py CVE-2023-44487 --dep-file requirements.txt
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from mock_cve_data import MOCK_CVES, SAMPLE_REQUIREMENTS_TXT, SAMPLE_PACKAGE_JSON, SAMPLE_GOMOD

# ---------------------------------------------------------------------------
# Version comparison (simplified semver)
# ---------------------------------------------------------------------------

def parse_version(v: str) -> tuple:
    """Parse a version string into a comparable tuple of ints."""
    parts = re.findall(r"\d+", v)
    return tuple(int(p) for p in parts) if parts else (0,)


def version_in_range(version: str, range_low: str, range_high: str) -> bool:
    """Check if version falls within [range_low, range_high] inclusive."""
    v = parse_version(version)
    lo = parse_version(range_low)
    hi = parse_version(range_high)
    return lo <= v <= hi


# ---------------------------------------------------------------------------
# Dependency file parsers
# ---------------------------------------------------------------------------

def parse_requirements_txt(content: str) -> dict:
    """Parse pip requirements.txt into {name: version}."""
    deps = {}
    for line in content.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        match = re.match(r"^([a-zA-Z0-9_.-]+)\s*[=<>!~]+\s*([0-9][^\s,;]*)", line)
        if match:
            deps[match.group(1).lower()] = match.group(2)
        else:
            # Package without version pin
            name = re.match(r"^([a-zA-Z0-9_.-]+)", line)
            if name:
                deps[name.group(1).lower()] = "unknown"
    return deps


def parse_package_json(content: str) -> dict:
    """Parse package.json into {name: version}."""
    deps = {}
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return deps
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        for name, ver in data.get(section, {}).items():
            # Strip semver range operators
            clean = re.sub(r"^[\^~>=<! ]+", "", ver)
            deps[name.lower()] = clean
    return deps


def parse_go_mod(content: str) -> dict:
    """Parse go.mod into {module-name: version}."""
    deps = {}
    in_require = False
    for line in content.strip().splitlines():
        line = line.strip()
        if line.startswith("require ("):
            in_require = True
            continue
        if in_require and line == ")":
            in_require = False
            continue
        if in_require:
            parts = line.split()
            if len(parts) >= 2:
                mod = parts[0].split("/")[-1].lower()
                ver = parts[1].lstrip("v")
                deps[mod] = ver
    return deps


PARSERS = {
    "requirements.txt": parse_requirements_txt,
    "package.json": parse_package_json,
    "go.mod": parse_go_mod,
}


# ---------------------------------------------------------------------------
# Dependency scanner
# ---------------------------------------------------------------------------

def scan_project_deps(project_dir: str | None, dep_file: str | None) -> dict:
    """
    Scan for dependencies. Returns {source_file: {name: version}}.
    Falls back to built-in sample files for demo purposes.
    """
    results = {}

    if dep_file and os.path.isfile(dep_file):
        fname = os.path.basename(dep_file)
        parser = PARSERS.get(fname)
        if parser:
            with open(dep_file) as f:
                results[dep_file] = parser(f.read())
        return results

    if project_dir and os.path.isdir(project_dir):
        for fname, parser in PARSERS.items():
            fpath = os.path.join(project_dir, fname)
            if os.path.isfile(fpath):
                with open(fpath) as f:
                    results[fpath] = parser(f.read())
        return results

    # Demo mode: use sample data
    results["(sample) requirements.txt"] = parse_requirements_txt(SAMPLE_REQUIREMENTS_TXT)
    results["(sample) package.json"] = parse_package_json(SAMPLE_PACKAGE_JSON)
    results["(sample) go.mod"] = parse_go_mod(SAMPLE_GOMOD)
    return results


# ---------------------------------------------------------------------------
# CVE lookup
# ---------------------------------------------------------------------------

def lookup_cve(cve_id: str) -> dict | None:
    """
    Look up CVE details. Uses mock data for demo; in production this
    would call NVD API at:
      https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=<CVE_ID>
    and MITRE API at:
      https://cveawg.mitre.org/api/cve/<CVE_ID>
    """
    return MOCK_CVES.get(cve_id.upper())


# ---------------------------------------------------------------------------
# Triage engine
# ---------------------------------------------------------------------------

def triage_cve(cve_id: str, project_dir: str | None = None,
               dep_file: str | None = None) -> str:
    """Run full triage and return a formatted Markdown report."""

    cve = lookup_cve(cve_id)
    if not cve:
        return (
            f"## CVE Triage: {cve_id}\n\n"
            f"**Verdict**: ? UNKNOWN\n\n"
            f"Could not find CVE data for `{cve_id}`. "
            f"In production, this would query the NVD and MITRE APIs.\n\n"
            f"### Mock CVEs available for demo\n"
            + "\n".join(f"- `{k}`" for k in MOCK_CVES)
        )

    all_deps = scan_project_deps(project_dir, dep_file)

    # Search for the affected dependency across all scanned files
    found_in = {}  # {source_file: (dep_name, installed_version)}
    dep_aliases = [d.lower() for d in cve["dependency_names"]]

    for source, deps in all_deps.items():
        for dep_name, dep_ver in deps.items():
            if dep_name.lower() in dep_aliases:
                found_in[source] = (dep_name, dep_ver)

    # Determine version match
    version_affected = False
    version_details = []
    for source, (dep_name, dep_ver) in found_in.items():
        if dep_ver == "unknown":
            version_details.append(
                f"  - `{dep_name}` in `{source}`: version unknown (cannot determine)"
            )
        else:
            for rng_lo, rng_hi in cve["affected_version_ranges"]:
                if version_in_range(dep_ver, rng_lo, rng_hi):
                    version_affected = True
                    version_details.append(
                        f"  - `{dep_name}` v{dep_ver} in `{source}`: "
                        f"IN affected range [{rng_lo}, {rng_hi}]"
                    )
                    break
            else:
                version_details.append(
                    f"  - `{dep_name}` v{dep_ver} in `{source}`: "
                    f"NOT in affected range"
                )

    # Determine verdict
    if not found_in:
        if not cve["affected_version_ranges"]:
            verdict = "POTENTIALLY AFFECTED"
            verdict_icon = "[!!]"
            verdict_reason = (
                f"This CVE affects multiple implementations of {cve['affected_product']}. "
                f"The affected software was not directly found in scanned dependency files, "
                f"but transitive dependencies or system-level packages may still be affected. "
                f"Manual review is recommended."
            )
        else:
            verdict = "NOT APPLICABLE"
            verdict_icon = "[--]"
            verdict_reason = (
                f"The affected software ({cve['affected_product']}) was not found in any "
                f"scanned dependency files. This CVE does not appear to apply to this project."
            )
    elif version_affected:
        verdict = "AFFECTED"
        verdict_icon = "[!!]"
        verdict_reason = (
            f"The affected software is present and the installed version falls within "
            f"the vulnerable range ({cve['affected_versions']}). "
            f"Immediate action is recommended."
        )
    else:
        verdict = "NOT AFFECTED"
        verdict_icon = "[OK]"
        verdict_reason = (
            f"The software is present but the installed version is outside the "
            f"affected range ({cve['affected_versions']}). No action required at this time, "
            f"but continue monitoring for new advisories."
        )

    # Build report
    sw_present = "Yes" if found_in else "No"
    sw_detail = ""
    if found_in:
        for source, (dep_name, dep_ver) in found_in.items():
            sw_detail += f" (`{dep_name}` v{dep_ver} in `{source}`)"

    version_in_range_str = "Yes" if version_affected else ("N/A" if not found_in else "No")

    exploit_note = "Yes - active exploitation reported" if cve["known_exploits"] else "No known active exploits"

    actions = []
    if verdict == "AFFECTED":
        actions.append(f"Upgrade to {cve['fixed_version']} immediately")
        if cve["known_exploits"]:
            actions.append("Check for indicators of compromise")
        actions.append("Review vendor advisory for additional mitigations")
    elif verdict == "POTENTIALLY AFFECTED":
        actions.append("Audit system-level packages and transitive dependencies")
        actions.append("Check vendor advisories for your specific implementation")
    elif verdict == "NOT AFFECTED":
        actions.append("No immediate action needed")
        actions.append("Monitor for changes to the advisory scope")
    else:
        actions.append("No action needed for this project")

    report = f"""## CVE Triage: {cve['id']}

**Verdict**: {verdict_icon} {verdict}

**CVE Summary**: {cve['summary']}

**CVSS Score**: {cve['cvss_score']} ({cve['severity']})
**Attack Vector**: {cve['attack_vector']}
**CWE**: {cve['cwe']}
**Affected Product**: {cve['affected_product']} ({cve['affected_versions']})
**Known Exploits**: {exploit_note}

### Applicability to This Environment
- **Software present?**: {sw_present}{sw_detail}
- **Version in affected range?**: {version_in_range_str}
"""
    if version_details:
        report += "\n".join(version_details) + "\n"

    report += f"""- **Vulnerable code path reachable?**: Unknown (requires manual review)
- **Mitigations in place?**: Unknown (check network/WAF configuration)

### Reasoning
{verdict_reason}

### Recommended Actions
"""
    for action in actions:
        report += f"- {action}\n"

    report += "\n### Sources\n"
    for ref in cve["references"]:
        report += f"- {ref}\n"

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="CVE Triage - Should I Care?",
        epilog="Example: python cve_triage.py CVE-2024-3094",
    )
    parser.add_argument("cve_id", help="CVE identifier (e.g. CVE-2024-3094)")
    parser.add_argument("--project-dir", help="Path to project directory to scan")
    parser.add_argument("--dep-file", help="Path to a specific dependency file")
    parser.add_argument("--all-demo", action="store_true",
                        help="Run triage on all mock CVEs for demonstration")
    args = parser.parse_args()

    if args.all_demo:
        for cve_id in MOCK_CVES:
            print(triage_cve(cve_id, args.project_dir, args.dep_file))
            print("\n" + "=" * 70 + "\n")
    else:
        print(triage_cve(args.cve_id, args.project_dir, args.dep_file))


if __name__ == "__main__":
    main()
