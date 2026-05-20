# How to Use — Content Provenance Verifier

## Install

```bash
cd content_provenance_verifier
pip install -r requirements.txt   # pure-Python, no compiled deps
```

The demo runs self-contained with mock C2PA manifests. To use with real
C2PA-signed files, also install the official SDK:

```bash
pip install c2pa-python   # optional — enables real manifest reading
```

## Using as a Claude Code Skill

1. Copy the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/content_provenance_verifier
cp SKILL.md ~/.claude/skills/content_provenance_verifier/SKILL.md
```

2. Trigger phrases that activate the skill:

- "How do I add Content Credentials to images?"
- "Verify if this image has C2PA metadata"
- "Check if media is AI-generated"
- "Integrate SynthID watermarking detection"
- "Implement content provenance tracking"

3. Claude will then use the patterns from the skill to help you write
   C2PA integration code, verification pipelines, or provenance UIs.

## Using as a CLI tool

```bash
# Verify a single file (uses mock data in demo mode)
python verifier.py verify samples/ai_generated.json

# Verify all sample files
python verifier.py verify-all

# Generate a provenance report
python verifier.py report samples/ai_generated.json

# Show supported digital source types
python verifier.py source-types
```

## First 60 seconds

```bash
# 1. Clone and enter
git clone <this-repo> && cd content_provenance_verifier

# 2. Install
pip install -r requirements.txt

# 3. Run the full demo
bash run.sh

# Expected output (< 2 seconds):
# - Verifies 4 sample files (AI-generated, camera photo, edited, unsigned)
# - Prints a provenance report table for each
# - Shows a summary with trust scores
# - Demonstrates signing a new file with Content Credentials
```

## Integrating into your own code

```python
from verifier import ProvenanceVerifier

v = ProvenanceVerifier()

# Check a file
result = v.verify("path/to/image.jpg")
print(result.has_credentials)   # True/False
print(result.source_type)       # e.g. "trainedAlgorithmicMedia"
print(result.is_ai_generated)   # True/False/None
print(result.trust_status)      # "VERIFIED" / "INVALID" / "NONE"

# Sign content with provenance metadata
from signer import ProvenanceSigner
s = ProvenanceSigner(generator="MyApp/1.0")
s.sign("input.jpg", "output.jpg", source_type="trainedAlgorithmicMedia")
```
