"""
Token Cost Lint Taxonomy
10 categories x 31 sub-patterns for classifying token waste
in multi-agent Claude Code harnesses.
"""

TAXONOMY = {
    "redundant_context": {
        "id": 1,
        "name": "Redundant Context",
        "description": "Same file/content passed to multiple agents",
        "sub_patterns": [
            {
                "id": "1a",
                "name": "duplicate_file_reads",
                "description": "Same file read by multiple agents or multiple times",
                "pattern": r"Read\s*\(.*?['\"](.+?)['\"]\)",
                "detect": "file_read_frequency",
            },
            {
                "id": "1b",
                "name": "shared_context_not_cached",
                "description": "Common context passed inline instead of cached",
                "pattern": r"(system_prompt|context)\s*[:=].*\b(same|shared|common)\b",
                "detect": "inline_context_duplication",
            },
            {
                "id": "1c",
                "name": "full_file_when_snippet_suffices",
                "description": "Entire file included when only a function/section needed",
                "pattern": r"read_file\s*\(.+?\)\s*$",
                "detect": "full_file_reads",
            },
        ],
    },
    "oversized_prompts": {
        "id": 2,
        "name": "Oversized Prompts",
        "description": "System prompts with unnecessary instructions",
        "sub_patterns": [
            {
                "id": "2a",
                "name": "boilerplate_instructions",
                "description": "Generic instructions that don't affect behavior",
                "pattern": r"(You are a helpful|Please be concise|Think step by step)",
                "detect": "boilerplate_phrases",
            },
            {
                "id": "2b",
                "name": "redundant_role_definitions",
                "description": "Role described multiple times across prompt sections",
                "pattern": r"(You are|Your role is|Act as)",
                "detect": "role_definition_count",
            },
            {
                "id": "2c",
                "name": "excessive_examples_in_system",
                "description": "Too many few-shot examples in system prompt",
                "pattern": r"(Example \d|e\.g\.|for example)",
                "detect": "example_count_in_system",
            },
            {
                "id": "2d",
                "name": "long_system_prompt",
                "description": "System prompt exceeding 2000 tokens",
                "detect": "system_prompt_length",
            },
        ],
    },
    "unbounded_history": {
        "id": 3,
        "name": "Unbounded History",
        "description": "Conversation history without truncation/summarization",
        "sub_patterns": [
            {
                "id": "3a",
                "name": "no_history_limit",
                "description": "Messages array grows without bounds",
                "pattern": r"messages\s*\.append\(|messages\s*\+\=",
                "detect": "unbounded_append",
            },
            {
                "id": "3b",
                "name": "full_history_forwarded",
                "description": "Complete conversation passed to sub-agents",
                "pattern": r"messages\s*[:=]\s*conversation|history\s*[:=]\s*messages",
                "detect": "history_forwarding",
            },
            {
                "id": "3c",
                "name": "no_summarization",
                "description": "No summarization step before context grows large",
                "pattern": r"summar",
                "detect": "missing_summarization",
            },
        ],
    },
    "duplicate_tool_results": {
        "id": 4,
        "name": "Duplicate Tool Results",
        "description": "Same tool called repeatedly with identical params",
        "sub_patterns": [
            {
                "id": "4a",
                "name": "repeated_identical_calls",
                "description": "Same tool+args combination called multiple times",
                "pattern": r"(tool_call|function_call)\s*\(",
                "detect": "tool_call_dedup",
            },
            {
                "id": "4b",
                "name": "no_result_caching",
                "description": "Tool results not cached between agent invocations",
                "pattern": r"cache|memoize|lru_cache",
                "detect": "missing_cache",
            },
            {
                "id": "4c",
                "name": "redundant_search_queries",
                "description": "Same search/grep run multiple times",
                "pattern": r"(grep|search|find)\s*\(",
                "detect": "search_dedup",
            },
        ],
    },
    "verbose_output": {
        "id": 5,
        "name": "Verbose Output Formatting",
        "description": "Agents generating markdown/explanation nobody reads",
        "sub_patterns": [
            {
                "id": "5a",
                "name": "machine_consumed_prose",
                "description": "Verbose text output consumed only by another agent",
                "pattern": r"(explain|description|summary)\s*[:=]",
                "detect": "prose_for_machines",
            },
            {
                "id": "5b",
                "name": "unnecessary_markdown",
                "description": "Markdown formatting in agent-to-agent communication",
                "pattern": r"(```|#{1,3}\s|\*\*)",
                "detect": "markdown_in_pipes",
            },
            {
                "id": "5c",
                "name": "echo_back_input",
                "description": "Agent echoes back the input before responding",
                "pattern": r"(You asked|Your question|Let me repeat)",
                "detect": "input_echo",
            },
        ],
    },
    "unnecessary_rereads": {
        "id": 6,
        "name": "Unnecessary Re-reads",
        "description": "Files read multiple times within one task",
        "sub_patterns": [
            {
                "id": "6a",
                "name": "same_file_multiple_reads",
                "description": "File content fetched more than once in a session",
                "pattern": r"(read_file|open\(|Read\()",
                "detect": "file_read_tracking",
            },
            {
                "id": "6b",
                "name": "no_file_content_cache",
                "description": "No in-memory cache of previously read files",
                "pattern": r"file_cache|content_cache",
                "detect": "missing_file_cache",
            },
            {
                "id": "6c",
                "name": "reread_after_write",
                "description": "File read again immediately after writing (content already known)",
                "pattern": r"write.*read|save.*load",
                "detect": "write_then_read",
            },
        ],
    },
    "broad_file_inclusion": {
        "id": 7,
        "name": "Broad File Inclusion",
        "description": "Glob patterns pulling in irrelevant files",
        "sub_patterns": [
            {
                "id": "7a",
                "name": "star_star_glob",
                "description": "**/* patterns without filtering",
                "pattern": r"\*\*/\*|\*\.\*",
                "detect": "broad_glob",
            },
            {
                "id": "7b",
                "name": "no_gitignore_respect",
                "description": "Including files that should be gitignored",
                "pattern": r"node_modules|__pycache__|\.git/",
                "detect": "ignored_file_inclusion",
            },
            {
                "id": "7c",
                "name": "entire_directory_reads",
                "description": "Reading all files in a directory without filtering",
                "pattern": r"(os\.listdir|glob\.glob|readdir)\s*\(",
                "detect": "directory_reads",
            },
        ],
    },
    "uncompressed_examples": {
        "id": 8,
        "name": "Uncompressed Examples",
        "description": "Few-shot examples that could be shorter",
        "sub_patterns": [
            {
                "id": "8a",
                "name": "verbose_few_shot",
                "description": "Few-shot examples with unnecessary detail",
                "detect": "example_verbosity",
            },
            {
                "id": "8b",
                "name": "duplicate_example_patterns",
                "description": "Multiple examples showing the same pattern",
                "detect": "example_dedup",
            },
            {
                "id": "8c",
                "name": "examples_in_every_call",
                "description": "Few-shot examples included in every API call",
                "detect": "example_frequency",
            },
        ],
    },
    "idle_agent_overhead": {
        "id": 9,
        "name": "Idle Agent Overhead",
        "description": "Agents spawned but doing trivial/no work",
        "sub_patterns": [
            {
                "id": "9a",
                "name": "trivial_delegation",
                "description": "Sub-agent spawned for a task completable inline",
                "pattern": r"(Agent|spawn|delegate)\s*\(",
                "detect": "delegation_analysis",
            },
            {
                "id": "9b",
                "name": "parallel_agents_serial_work",
                "description": "Multiple agents spawned for sequential tasks",
                "pattern": r"(parallel|concurrent|async).*agent",
                "detect": "parallel_serial_mismatch",
            },
            {
                "id": "9c",
                "name": "agent_with_large_context_small_task",
                "description": "Agent given large context for minimal output",
                "detect": "context_output_ratio",
            },
        ],
    },
    "retry_amplification": {
        "id": 10,
        "name": "Retry Amplification",
        "description": "Failed calls retried without reducing context",
        "sub_patterns": [
            {
                "id": "10a",
                "name": "full_context_retry",
                "description": "Retrying with identical (full) context on failure",
                "pattern": r"(retry|retries|attempt)\s*[=<>]",
                "detect": "retry_context_check",
            },
            {
                "id": "10b",
                "name": "no_error_context_reduction",
                "description": "No strategy to reduce context on rate limit / context overflow",
                "pattern": r"(rate_limit|context_length|too_long)",
                "detect": "error_handling_check",
            },
            {
                "id": "10c",
                "name": "exponential_token_growth",
                "description": "Each retry adds error info without trimming history",
                "pattern": r"(error_message|traceback|exception).*append",
                "detect": "retry_growth",
            },
        ],
    },
}

# Severity levels
SEVERITY = {
    "critical": {"min_waste_pct": 20, "label": "CRITICAL", "color": "\033[91m"},
    "high": {"min_waste_pct": 10, "label": "HIGH", "color": "\033[93m"},
    "medium": {"min_waste_pct": 5, "label": "MEDIUM", "color": "\033[33m"},
    "low": {"min_waste_pct": 0, "label": "LOW", "color": "\033[36m"},
}

RESET_COLOR = "\033[0m"


def get_all_sub_patterns():
    """Return a flat list of all 31 sub-patterns with their category info."""
    result = []
    for cat_key, cat in TAXONOMY.items():
        for sp in cat["sub_patterns"]:
            result.append({
                "category_id": cat["id"],
                "category_key": cat_key,
                "category_name": cat["name"],
                **sp,
            })
    return result


def get_category_count():
    return len(TAXONOMY)


def get_sub_pattern_count():
    return sum(len(c["sub_patterns"]) for c in TAXONOMY.values())
