"""Mock content provenance signer — attaches C2PA-style Content Credentials."""

import hashlib
import json
import os
from datetime import datetime, timezone


class ProvenanceSigner:
    """Signs files with C2PA-style Content Credentials (mock implementation)."""

    def __init__(self, generator: str = "ContentProvenanceVerifier/1.0"):
        self.generator = generator

    def sign(self, input_path: str, output_path: str, source_type: str = "trainedAlgorithmicMedia") -> dict:
        """Create a signed manifest for a file.

        In demo mode, produces a JSON manifest fixture.
        With c2pa-python, would sign the actual file.
        """
        manifest = {
            "claim_generator": self.generator,
            "title": os.path.basename(input_path),
            "assertions": [
                {
                    "label": "c2pa.actions",
                    "data": {
                        "actions": [
                            {
                                "action": "c2pa.created",
                                "digitalSourceType": f"http://cv.iptc.org/newscodes/digitalsourcetype/{source_type}",
                                "when": datetime.now(timezone.utc).isoformat(),
                            }
                        ]
                    },
                },
                {
                    "label": "c2pa.hash.data",
                    "data": {
                        "name": "jumbf manifest",
                        "hash": self._file_hash(input_path) if os.path.exists(input_path) else "mock",
                    },
                },
            ],
            "ingredients": [],
        }

        # Compute signature hash
        sig_hash = hashlib.sha256(
            json.dumps(manifest, sort_keys=True).encode()
        ).hexdigest()[:16]
        manifest["signature"] = {
            "alg": "SHA-256",
            "hash": sig_hash,
            "issuer": self.generator,
            "time": datetime.now(timezone.utc).isoformat(),
        }

        output = {"manifest": manifest}
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)

        return output

    def _file_hash(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()[:16]
