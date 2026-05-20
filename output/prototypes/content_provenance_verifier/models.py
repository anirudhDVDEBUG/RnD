"""Data models for content provenance verification."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Assertion:
    label: str
    data: dict

    def __str__(self):
        return f"{self.label}: {self.data}"


@dataclass
class Manifest:
    claim_generator: str
    title: str
    assertions: List[Assertion] = field(default_factory=list)
    signature_info: Optional[dict] = None
    ingredients: List[dict] = field(default_factory=list)

    @property
    def digital_source_type(self) -> Optional[str]:
        for a in self.assertions:
            if a.label == "c2pa.actions":
                for action in a.data.get("actions", []):
                    dst = action.get("digitalSourceType", "")
                    if dst:
                        return dst.split("/")[-1]
        return None


@dataclass
class VerificationResult:
    file_path: str
    has_credentials: bool = False
    source_type: Optional[str] = None
    is_ai_generated: Optional[bool] = None
    generator: Optional[str] = None
    trust_status: str = "NONE"  # VERIFIED, INVALID, NONE
    manifest: Optional[Manifest] = None
    error: Optional[str] = None
