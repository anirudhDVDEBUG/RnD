"""Core content provenance verification engine."""

import hashlib
import json
import os
from typing import Optional

from models import Assertion, Manifest, VerificationResult
from source_types import classify_source_type


class ProvenanceVerifier:
    """Verifies C2PA Content Credentials in media files."""

    def verify(self, file_path: str) -> VerificationResult:
        """Verify content provenance for a file.

        In demo mode, reads .json manifest fixtures.
        With c2pa-python installed, can read real image files.
        """
        result = VerificationResult(file_path=file_path)

        if not os.path.exists(file_path):
            result.error = f"File not found: {file_path}"
            return result

        # Try JSON manifest fixture (demo mode)
        if file_path.endswith(".json"):
            return self._verify_json_manifest(file_path, result)

        # Try real C2PA reading via c2pa-python
        try:
            return self._verify_real_file(file_path, result)
        except ImportError:
            result.error = "Install c2pa-python to verify real image files"
            return result

    def _verify_json_manifest(self, path: str, result: VerificationResult) -> VerificationResult:
        """Parse a JSON manifest fixture and produce a verification result."""
        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            result.error = f"Cannot read manifest: {e}"
            return result

        manifest_data = data.get("manifest", {})
        if not manifest_data:
            # No manifest = unsigned file
            result.has_credentials = False
            result.trust_status = "NONE"
            return result

        # Parse manifest
        assertions = [
            Assertion(label=a["label"], data=a.get("data", {}))
            for a in manifest_data.get("assertions", [])
        ]
        manifest = Manifest(
            claim_generator=manifest_data.get("claim_generator", "Unknown"),
            title=manifest_data.get("title", os.path.basename(path)),
            assertions=assertions,
            signature_info=manifest_data.get("signature", {}),
            ingredients=manifest_data.get("ingredients", []),
        )

        result.has_credentials = True
        result.manifest = manifest
        result.generator = manifest.claim_generator

        # Extract source type
        source_type = manifest.digital_source_type
        if source_type:
            result.source_type = source_type
            info = classify_source_type(source_type)
            result.is_ai_generated = info["is_ai"]

        # Verify signature (mock: check hash matches)
        result.trust_status = self._verify_signature(data)

        return result

    def _verify_signature(self, data: dict) -> str:
        """Mock signature verification using hash comparison."""
        sig = data.get("manifest", {}).get("signature", {})
        if not sig:
            return "NONE"
        expected_hash = sig.get("hash")
        if not expected_hash:
            return "NONE"
        # Recompute hash from manifest content (excluding signature block)
        manifest_copy = dict(data.get("manifest", {}))
        manifest_copy.pop("signature", None)
        computed = hashlib.sha256(
            json.dumps(manifest_copy, sort_keys=True).encode()
        ).hexdigest()[:16]
        if computed == expected_hash:
            return "VERIFIED"
        return "INVALID"

    def _verify_real_file(self, path: str, result: VerificationResult) -> VerificationResult:
        """Verify a real image file using c2pa-python."""
        from c2pa import Reader  # type: ignore

        reader = Reader.from_file(path)
        store = json.loads(reader.get_manifest_store())
        # Extract the active manifest
        active_id = store.get("active_manifest")
        if not active_id or active_id not in store.get("manifests", {}):
            result.has_credentials = False
            return result

        m = store["manifests"][active_id]
        result.has_credentials = True
        result.generator = m.get("claim_generator", "Unknown")
        result.trust_status = "VERIFIED"

        for a in m.get("assertions", []):
            if "trainedAlgorithmicMedia" in json.dumps(a):
                result.is_ai_generated = True
                result.source_type = "trainedAlgorithmicMedia"
                break

        return result


def verify_file(path: str) -> VerificationResult:
    """Convenience function."""
    return ProvenanceVerifier().verify(path)
