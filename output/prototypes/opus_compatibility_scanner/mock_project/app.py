"""Example app using Anthropic SDK — intentionally uses deprecated patterns."""

from anthropic import Anthropic, AsyncAnthropic
import anthropic

# Initialize client
client = Anthropic()
async_client = AsyncAnthropic()

# Old completion style (deprecated)
def legacy_complete(prompt: str) -> str:
    response = client.completion(
        model="claude-opus-4-6-20250115",
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
        max_tokens_to_sample=1024,
        stop_sequences=[],
        top_k=-1,
    )
    return response["completion"]

# Messages API (current but with old model)
def chat(user_msg: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": user_msg}],
        metadata={"user_id": "user-123"},
    )
    return response.content[0].text

# Token counting
def check_tokens(text: str):
    count = client.count_tokens(text)
    if count > 200000:
        print("Exceeds token_count limit")
    return count

# Streaming with raw response
def stream_response(msg: str):
    with client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": msg}],
        stream=True,
    ) as response:
        for event in response:
            if event.type == "text_delta":
                print(event.text, end="")

# Beta API usage
def beta_feature():
    result = client.beta.prompt_caching.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": "test"}],
    )
    return result

# Error handling
def safe_call(msg: str):
    try:
        return chat(msg)
    except anthropic.APIError as e:
        print(f"API error: {e}")
        return None

# Raw response
def raw_call(msg: str):
    resp = client.with_raw_response.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": msg}],
    )
    return resp

# Tool choice
def tool_call():
    return client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": "search for X"}],
        tool_choice={"type": "required"},
        tools=[{
            "name": "search",
            "inputSchema": {"type": "object", "properties": {"q": {"type": "string"}}},
        }],
    )
