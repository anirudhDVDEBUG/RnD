# How to Use: AI Agent Skills

## Installation

```bash
# Clone this mini-repo (or the upstream source)
git clone https://github.com/DevelopersGlobal/ai-agent-skills.git
cd ai-agent-skills

# Install (pure Python, no heavy deps)
pip install -e .
```

For this demo prototype, no install is needed - just run:

```bash
pip install -r requirements.txt  # (empty - stdlib only)
bash run.sh
```

## As a Claude Skill

Drop the skill definition into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/ai_agent_skills_production
cp SKILL.md ~/.claude/skills/ai_agent_skills_production/SKILL.md
```

**Trigger phrases** that activate this skill:
- "Add production-grade agent skills to my project"
- "Scaffold a reusable Claude skill module in Python"
- "Create a new agent skill following the ai-agent-skills pattern"
- "Integrate agent skills for my AI application"

## SDK / Programmatic Usage

```python
from skills.registry import registry
import skills.web_scraper
import skills.text_summarizer
import skills.data_validator

# List available skills
print(registry.list_skills())

# Invoke a skill by name
result = registry.invoke("text_summarizer", {
    "text": "Your long article text here...",
    "max_sentences": 3
})

print(result.success)  # True
print(result.data)     # "Summarized text..."
print(result.metadata) # {"compression_ratio": 0.35, ...}
```

## First 60 Seconds

```bash
$ bash run.sh

AI Agent Skills - Production Demo
============================================================

Registered Skills:
  - web_scraper v1.0.0: Extract structured data from HTML content
  - text_summarizer v1.0.0: Summarize text using extractive sentence scoring
  - data_validator v1.0.0: Validate structured data against a schema definition

============================================================
  SKILL: web_scraper
============================================================

Input: HTML page with title, headings, and links
Action: Extract title...
  Result: AI Agent Skills - Production Grade

Action: Extract all links...
  Result: ['https://github.com/DevelopersGlobal/ai-agent-skills', 'https://docs.example.com/skills']

============================================================
  SKILL: text_summarizer
============================================================

Input: 523 chars of text (8 sentences)
Action: Summarize to 2 sentences...
  Summary: Production-grade agent skills require careful error handling...
  Metadata: {"compression_ratio": 0.28, ...}

============================================================
  SKILL: data_validator
============================================================

Test 1: Valid user data
  Valid: True

Test 2: Invalid user data (short name, age>150, short email)
  Valid: False
  Errors:
    - Field 'name': length 1 < min 2
    - Field 'age': value 200 > max 150
    - Field 'email': length 1 < min 5
```

## Creating Your Own Skill

```python
# skills/my_skill/__init__.py
from skills.base import BaseSkill, SkillResult
from skills.registry import registry

@registry.register
class MySkill(BaseSkill):
    name = "my_skill"
    description = "What it does"
    version = "1.0.0"

    def validate_input(self, input_data: dict) -> bool:
        return "required_field" in input_data

    def execute(self, input_data: dict) -> SkillResult:
        # Your logic here
        return SkillResult(success=True, data={"output": "value"})
```
