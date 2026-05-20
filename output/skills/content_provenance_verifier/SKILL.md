---
name: Content Provenance Verifier
description: |
  Helps implement and integrate content provenance standards (Content Credentials, SynthID, C2PA) into applications to verify AI-generated media authenticity and origin.
  TRIGGER when: user mentions content provenance, Content Credentials, C2PA, SynthID, media verification, AI-generated content detection, image/video authenticity, or digital content origin tracking.
---

# Content Provenance Verifier

A skill for implementing content provenance solutions that help identify, verify, and label AI-generated media using industry standards like Content Credentials (C2PA), SynthID, and verification APIs.

## When to use

- "How do I add Content Credentials to images my app generates?"
- "I need to verify if an image has C2PA metadata attached"
- "Help me integrate SynthID watermarking detection"
- "How can I check if media is AI-generated?"
- "I want to implement content provenance tracking in my pipeline"

## How to use

### 1. Understand the provenance stack

Content provenance relies on three complementary approaches:

- **Content Credentials (C2PA)**: Open standard that attaches cryptographically signed metadata to media files, recording creation and edit history. Uses the Coalition for Content Provenance and Authenticity (C2PA) specification.
- **SynthID**: Imperceptible watermarks embedded directly into AI-generated content (images, audio, video, text) that survive screenshots, crops, and re-encoding.
- **Verification tools**: APIs and services that read Content Credentials or detect watermarks to surface provenance information to end users.

### 2. Implementing Content Credentials (C2PA)

```python
# Install the c2pa-python library
# pip install c2pa-python

from c2pa import Builder, Reader
import json

# Reading Content Credentials from a file
def verify_provenance(file_path: str) -> dict:
    """Read and verify Content Credentials from a media file."""
    reader = Reader.from_file(file_path)
    manifest_store = reader.get_manifest_store()
    return json.loads(manifest_store)

# Adding Content Credentials to generated content
def sign_content(input_path: str, output_path: str, claim_info: dict):
    """Attach Content Credentials to a media file."""
    builder = Builder()
    builder.set_claim_generator("MyApp/1.0")
    builder.add_assertion("c2pa.actions", json.dumps({
        "actions": [{
            "action": "c2pa.created",
            "digitalSourceType": "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
        }]
    }))
    builder.sign_file(input_path, output_path, signer)
```

### 3. Detecting AI-generated content

```python
# Check for SynthID or Content Credentials
def check_ai_generated(file_path: str) -> dict:
    """Check if media has provenance signals indicating AI generation."""
    result = {"has_credentials": False, "is_ai_generated": None, "source": None}

    # Check C2PA Content Credentials
    try:
        reader = Reader.from_file(file_path)
        manifest = json.loads(reader.get_manifest_store())
        result["has_credentials"] = True
        # Look for AI generation assertions
        for assertion in manifest.get("assertions", []):
            if "trainedAlgorithmicMedia" in str(assertion):
                result["is_ai_generated"] = True
                result["source"] = assertion.get("claim_generator", "Unknown")
    except Exception:
        pass

    return result
```

### 4. Best practices

- Always attach Content Credentials at point of creation for AI-generated media
- Use `digitalSourceType` values from the IPTC vocabulary to classify content origin
- Preserve provenance metadata through your pipeline — avoid stripping EXIF/XMP data
- Display provenance information to end users via a standardized UI (cr icon)
- Combine multiple signals (C2PA + watermarks) for robust detection
- Use the official C2PA verification service or libraries for validation

### 5. Key resources

- C2PA specification: https://c2pa.org/specifications/
- c2pa-python SDK: https://github.com/contentauth/c2pa-python
- c2pa-node SDK: https://github.com/contentauth/c2pa-node
- Content Authenticity Initiative tools: https://contentauthenticity.org

## References

- Source: [Advancing content provenance for a safer, more transparent AI ecosystem](https://openai.com/index/advancing-content-provenance) — OpenAI News
- [C2PA Technical Specification](https://c2pa.org/specifications/)
- [Content Authenticity Initiative](https://contentauthenticity.org)
