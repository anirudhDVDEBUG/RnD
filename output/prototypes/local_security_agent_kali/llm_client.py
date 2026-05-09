"""OpenAI-compatible client pointed at a local LM Studio instance."""

import config

SYSTEM_PROMPT = (
    "You are an autonomous cybersecurity assistant. "
    "Respond ONLY with a JSON object: {\"action\": \"<tool_name>\", \"args\": {<args>}} "
    "or {\"action\": \"DONE\", \"summary\": \"<findings>\"}. "
    "Available tools: nmap_scan, nikto_scan, whois_lookup, searchsploit."
)

# ---------------------------------------------------------------------------
# Mock responses used when MOCK_MODE=1 (no LM Studio required)
# ---------------------------------------------------------------------------
_MOCK_RESPONSES = [
    '{"action": "nmap_scan", "args": {"target": "192.168.1.100", "flags": "-sV -sC -T4"}}',
    '{"action": "nikto_scan", "args": {"target": "192.168.1.100", "port": "80"}}',
    '{"action": "searchsploit", "args": {"query": "Apache 2.4.49"}}',
    '{"action": "DONE", "summary": "Target 192.168.1.100 has 3 open ports (22/ssh, 80/http, 3306/mysql). '
    'Web server Apache 2.4.49 is vulnerable to CVE-2021-41773 path traversal. '
    'MySQL allows remote connections. Recommend patching Apache immediately and restricting MySQL bind address."}',
]
_mock_index = 0


def ask(prompt: str, system: str = SYSTEM_PROMPT) -> str:
    """Send a prompt to the local LLM and return the response text."""
    if config.MOCK_MODE:
        return _mock_response()

    import openai

    client = openai.OpenAI(
        base_url=config.LLM_BASE_URL,
        api_key=config.LLM_API_KEY,
    )
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=config.LLM_TEMPERATURE,
    )
    return response.choices[0].message.content


def _mock_response() -> str:
    global _mock_index
    resp = _MOCK_RESPONSES[min(_mock_index, len(_MOCK_RESPONSES) - 1)]
    _mock_index += 1
    return resp
