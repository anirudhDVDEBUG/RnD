"""Sandbox configuration: file access rules, network policy, and safety guardrails."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json
import xml.etree.ElementTree as ET


@dataclass
class FolderMapping:
    host_path: str
    sandbox_path: str
    read_only: bool = True


@dataclass
class NetworkPolicy:
    enabled: bool = False
    allowed_hosts: list[str] = field(default_factory=list)


@dataclass
class SafetyRules:
    allowed_extensions: list[str] = field(default_factory=lambda: [
        ".py", ".js", ".ts", ".html", ".css", ".json",
        ".md", ".yaml", ".yml", ".toml", ".txt", ".sh",
    ])
    blocked_patterns: list[str] = field(default_factory=lambda: [
        ".env", "secrets.*", "*.pem", "*.key", ".git/*",
        "*.credentials", "id_rsa*",
    ])
    max_file_size_bytes: int = 1_000_000
    timeout_seconds: int = 300
    max_files_changed: int = 20


@dataclass
class SandboxConfig:
    workspace_host: str
    workspace_sandbox: str = "/sandbox/workspace"
    folder_mappings: list[FolderMapping] = field(default_factory=list)
    network: NetworkPolicy = field(default_factory=NetworkPolicy)
    safety: SafetyRules = field(default_factory=SafetyRules)
    logon_command: Optional[str] = None

    def to_wsb_xml(self) -> str:
        """Generate a Windows Sandbox .wsb configuration file."""
        root = ET.Element("Configuration")

        # Mapped folders
        mapped = ET.SubElement(root, "MappedFolders")
        # Always map workspace
        ws = ET.SubElement(mapped, "MappedFolder")
        ET.SubElement(ws, "HostFolder").text = self.workspace_host
        ET.SubElement(ws, "SandboxFolder").text = self.workspace_sandbox
        ET.SubElement(ws, "ReadOnly").text = "false"

        for fm in self.folder_mappings:
            mf = ET.SubElement(mapped, "MappedFolder")
            ET.SubElement(mf, "HostFolder").text = fm.host_path
            ET.SubElement(mf, "SandboxFolder").text = fm.sandbox_path
            ET.SubElement(mf, "ReadOnly").text = str(fm.read_only).lower()

        # Networking
        net = ET.SubElement(root, "Networking")
        net.text = "Default" if self.network.enabled else "Disable"

        # Logon command
        if self.logon_command:
            lc = ET.SubElement(root, "LogonCommand")
            ET.SubElement(lc, "Command").text = self.logon_command

        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="unicode", xml_declaration=True)

    def to_dict(self) -> dict:
        return {
            "workspace_host": self.workspace_host,
            "workspace_sandbox": self.workspace_sandbox,
            "network_enabled": self.network.enabled,
            "allowed_hosts": self.network.allowed_hosts,
            "safety": {
                "allowed_extensions": self.safety.allowed_extensions,
                "blocked_patterns": self.safety.blocked_patterns,
                "max_file_size_bytes": self.safety.max_file_size_bytes,
                "timeout_seconds": self.safety.timeout_seconds,
                "max_files_changed": self.safety.max_files_changed,
            },
            "folder_mappings": [
                {"host": fm.host_path, "sandbox": fm.sandbox_path, "ro": fm.read_only}
                for fm in self.folder_mappings
            ],
        }
