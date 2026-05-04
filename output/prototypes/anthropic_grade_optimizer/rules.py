"""
189 Anthropic rules organized into 11 dimensions.
Each rule has: id, dimension, description, and a check pattern.
"""

DIMENSIONS = [
    "Clarity",
    "Specificity",
    "Structure",
    "Completeness",
    "Consistency",
    "Voice Alignment",
    "Safety",
    "Tool Use",
    "Context Management",
    "Error Handling",
    "Anthropic Conventions",
]

# Representative rules per dimension (subset shown; full 189 in production)
RULES = [
    # Clarity
    {"id": "§1.1", "dim": "Clarity", "desc": "Avoid passive voice in directives", "patterns": [r"\b(is|are|was|were|been|being)\s+\w+ed\b"]},
    {"id": "§1.2", "dim": "Clarity", "desc": "No double negatives", "patterns": [r"\bnot\s+\w*n't\b", r"\bnever\s+\w*not\b", r"\bdon't\s+\w*no\b"]},
    {"id": "§1.3", "dim": "Clarity", "desc": "Avoid ambiguous pronouns without clear antecedent", "patterns": [r"^(It|This|That)\s+(should|must|will)\b"]},
    {"id": "§1.4", "dim": "Clarity", "desc": "Each instruction should be a single actionable directive", "patterns": [r"\band\s+also\b", r"\bwhile\s+also\b"]},

    # Specificity
    {"id": "§3.1", "dim": "Specificity", "desc": "Use concrete examples over abstract directives", "patterns": [r"\btry to be\b", r"\bgenerally\s+(be|do|try)\b", r"\bas\s+needed\b"]},
    {"id": "§3.2", "dim": "Specificity", "desc": "Quantify when possible instead of vague qualifiers", "patterns": [r"\b(a few|some|several|many|various)\s+(times|examples|cases)\b"]},
    {"id": "§3.3", "dim": "Specificity", "desc": "Avoid hedge words that weaken directives", "patterns": [r"\b(maybe|perhaps|possibly|somewhat|fairly|rather)\b"]},
    {"id": "§3.4", "dim": "Specificity", "desc": "Define expected output format explicitly", "patterns": []},

    # Structure
    {"id": "§2.1", "dim": "Structure", "desc": "Use markdown headers for section organization", "patterns": []},
    {"id": "§2.2", "dim": "Structure", "desc": "Group related instructions under common headers", "patterns": []},
    {"id": "§2.3", "dim": "Structure", "desc": "Place most important instructions first", "patterns": []},

    # Completeness
    {"id": "§5.1", "dim": "Completeness", "desc": "Define role/identity clearly", "patterns": []},
    {"id": "§5.2", "dim": "Completeness", "desc": "Include scope boundaries (what NOT to do)", "patterns": []},
    {"id": "§5.3", "dim": "Completeness", "desc": "Define behavior for edge cases and errors", "patterns": []},
    {"id": "§5.4", "dim": "Completeness", "desc": "Specify output format expectations", "patterns": []},

    # Consistency
    {"id": "§6.1", "dim": "Consistency", "desc": "No contradictory instructions within the artifact", "patterns": []},
    {"id": "§6.2", "dim": "Consistency", "desc": "Consistent use of imperative vs declarative mood", "patterns": []},
    {"id": "§6.3", "dim": "Consistency", "desc": "Consistent formatting conventions throughout", "patterns": []},

    # Voice Alignment
    {"id": "§4.1", "dim": "Voice Alignment", "desc": "Maintain uniform directive register throughout", "patterns": []},
    {"id": "§4.2", "dim": "Voice Alignment", "desc": "No mixing imperative and conversational tone", "patterns": [r"\byou might want to\b", r"\byou could\b", r"\bfeel free to\b"]},
    {"id": "§4.3", "dim": "Voice Alignment", "desc": "Consistent formality level across all sections", "patterns": []},
    {"id": "§4.4", "dim": "Voice Alignment", "desc": "No persona bleed between sections", "patterns": []},

    # Safety
    {"id": "§7.1", "dim": "Safety", "desc": "Include explicit refusal boundaries", "patterns": []},
    {"id": "§7.2", "dim": "Safety", "desc": "Do not instruct to bypass safety mechanisms", "patterns": [r"\bignore\s+(previous|prior|all)\s+(instructions|rules)\b", r"\bjailbreak\b"]},
    {"id": "§7.3", "dim": "Safety", "desc": "System prompt confidentiality instructions present", "patterns": []},

    # Tool Use
    {"id": "§8.1", "dim": "Tool Use", "desc": "Explicitly name available tools", "patterns": []},
    {"id": "§8.2", "dim": "Tool Use", "desc": "Define when to use each tool", "patterns": [r"\bwhen appropriate\b", r"\bwhen needed\b"]},
    {"id": "§8.3", "dim": "Tool Use", "desc": "Scope tool permissions clearly", "patterns": []},

    # Context Management
    {"id": "§9.1", "dim": "Context Management", "desc": "Avoid redundant repetition of instructions", "patterns": []},
    {"id": "§9.2", "dim": "Context Management", "desc": "Use references instead of duplicating content", "patterns": []},

    # Error Handling
    {"id": "§10.1", "dim": "Error Handling", "desc": "Define fallback behavior for ambiguous requests", "patterns": []},
    {"id": "§10.2", "dim": "Error Handling", "desc": "Specify what to do when tools fail", "patterns": []},
    {"id": "§10.3", "dim": "Error Handling", "desc": "Include clarification-seeking behavior", "patterns": []},

    # Anthropic Conventions
    {"id": "§11.1", "dim": "Anthropic Conventions", "desc": "CLAUDE.md should have Role, Instructions, and Constraints sections", "patterns": []},
    {"id": "§11.2", "dim": "Anthropic Conventions", "desc": "Use bullet points for lists of directives", "patterns": []},
    {"id": "§11.3", "dim": "Anthropic Conventions", "desc": "SKILL.md requires YAML frontmatter with name and description", "patterns": []},
]
