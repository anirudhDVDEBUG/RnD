"""
mem0 Memory Layer Demo
======================
Demonstrates mem0's universal memory layer for AI agents.
Uses mem0 with a mock LLM to run fully offline without API keys.
"""

import json
import os
import sys
from unittest.mock import patch, MagicMock

# ---------------------------------------------------------------------------
# Mock LLM responses so the demo runs without any API key
# ---------------------------------------------------------------------------

MOCK_EXTRACTIONS = {
    0: {
        "facts": ["Prefers dark mode", "Likes Python over JavaScript"],
    },
    1: {
        "facts": ["Is working on a Claude-based chatbot project"],
    },
    2: {
        "facts": ["Favorite framework is FastAPI", "Deploys on AWS Lambda"],
    },
    3: {
        "facts": ["Prefers concise documentation", "Uses pytest for testing"],
    },
}

_call_count = 0


def mock_openai_chat_create(*args, **kwargs):
    """Return a mock ChatCompletion that mem0's LLM wrapper accepts."""
    global _call_count
    messages = kwargs.get("messages", [])
    content_text = " ".join(m.get("content", "") for m in messages if isinstance(m, dict))

    # Determine which mock extraction to return based on call count
    idx = _call_count % len(MOCK_EXTRACTIONS)
    _call_count += 1

    # mem0 expects the LLM to return JSON with extracted facts
    facts = MOCK_EXTRACTIONS[idx]["facts"]
    response_json = {"facts": [{"fact": f, "category": "preference"} for f in facts]}

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = json.dumps(response_json)
    mock_message.tool_calls = None
    mock_choice.message = mock_message
    mock_choice.finish_reason = "stop"
    mock_response.choices = [mock_choice]
    mock_response.model = "mock-model"
    mock_response.usage = MagicMock(prompt_tokens=10, completion_tokens=10, total_tokens=20)
    return mock_response


def mock_embedding_create(*args, **kwargs):
    """Return a mock embedding vector."""
    import random
    random.seed(42)
    texts = kwargs.get("input", [""])
    if isinstance(texts, str):
        texts = [texts]

    mock_response = MagicMock()
    data_items = []
    for i, text in enumerate(texts):
        item = MagicMock()
        # Deterministic pseudo-embedding based on text hash
        seed = hash(text) % 10000
        random.seed(seed)
        item.embedding = [random.uniform(-1, 1) for _ in range(1536)]
        item.index = i
        data_items.append(item)
    mock_response.data = data_items
    mock_response.model = "mock-embedding"
    mock_response.usage = MagicMock(prompt_tokens=5, total_tokens=5)
    return mock_response


def run_demo():
    """Run the full mem0 demo with mocked LLM/embeddings."""
    print("=" * 60)
    print("  mem0 Memory Layer Demo (offline / no API keys needed)")
    print("=" * 60)

    # Patch OpenAI calls before importing mem0
    os.environ.setdefault("OPENAI_API_KEY", "mock-key-for-demo")

    try:
        from mem0 import Memory
    except ImportError:
        print("\nERROR: mem0ai not installed. Run: pip install mem0ai")
        sys.exit(1)

    # Apply mocks to OpenAI client
    with patch("openai.resources.chat.completions.Completions.create", side_effect=mock_openai_chat_create), \
         patch("openai.resources.embeddings.Embeddings.create", side_effect=mock_embedding_create):

        print("\n[1] Initializing mem0 Memory (in-memory vector store)...")
        m = Memory()
        print("    OK - Memory instance created")

        # --- Add memories ---
        print("\n[2] Adding memories for user 'alice'...")
        messages_alice = [
            "I prefer dark mode and Python over JavaScript.",
            "I'm working on a Claude-based chatbot project.",
        ]
        for msg in messages_alice:
            result = m.add(msg, user_id="alice", metadata={"source": "demo"})
            print(f"    Added: {msg!r}")
            if isinstance(result, dict) and "results" in result:
                for r in result["results"]:
                    print(f"      -> extracted: {r.get('memory', r)}")

        print("\n[3] Adding memories for user 'bob'...")
        messages_bob = [
            "My favorite framework is FastAPI and I deploy on AWS Lambda.",
            "I prefer concise documentation and use pytest for testing.",
        ]
        for msg in messages_bob:
            result = m.add(msg, user_id="bob", metadata={"source": "demo"})
            print(f"    Added: {msg!r}")
            if isinstance(result, dict) and "results" in result:
                for r in result["results"]:
                    print(f"      -> extracted: {r.get('memory', r)}")

        # --- Retrieve all memories ---
        print("\n[4] Retrieving all memories for 'alice'...")
        alice_memories = m.get_all(user_id="alice")
        if isinstance(alice_memories, dict) and "results" in alice_memories:
            memories_list = alice_memories["results"]
        elif isinstance(alice_memories, list):
            memories_list = alice_memories
        else:
            memories_list = []
        for mem in memories_list:
            mem_text = mem.get("memory", mem) if isinstance(mem, dict) else mem
            print(f"    - {mem_text}")
        print(f"    Total: {len(memories_list)} memories")

        # --- Search memories ---
        print("\n[5] Searching bob's memories for 'testing'...")
        try:
            search_results = m.search("testing frameworks", user_id="bob")
            if isinstance(search_results, dict) and "results" in search_results:
                results_list = search_results["results"]
            elif isinstance(search_results, list):
                results_list = search_results
            else:
                results_list = []
            for r in results_list[:3]:
                if isinstance(r, dict):
                    print(f"    - {r.get('memory', r)} (score: {r.get('score', 'N/A')})")
                else:
                    print(f"    - {r}")
        except Exception as e:
            print(f"    Search returned: {e}")

        # --- Memory history ---
        print("\n[6] Checking memory history...")
        if memories_list and isinstance(memories_list[0], dict) and "id" in memories_list[0]:
            mem_id = memories_list[0]["id"]
            try:
                history = m.history(memory_id=mem_id)
                print(f"    History for {mem_id}: {len(history) if isinstance(history, list) else 'N/A'} entries")
            except Exception as e:
                print(f"    History lookup: {e}")
        else:
            print("    (no memory IDs available for history lookup)")

        # --- Delete a memory ---
        print("\n[7] Deleting all memories for 'alice'...")
        try:
            m.delete_all(user_id="alice")
            remaining = m.get_all(user_id="alice")
            if isinstance(remaining, dict) and "results" in remaining:
                count = len(remaining["results"])
            elif isinstance(remaining, list):
                count = len(remaining)
            else:
                count = 0
            print(f"    Alice's memories after delete: {count}")
        except Exception as e:
            print(f"    Delete result: {e}")

        # --- Multi-level memory ---
        print("\n[8] Multi-level memory organization...")
        try:
            m.add("This agent specializes in billing", agent_id="billing-bot")
            print("    Added agent-level memory for 'billing-bot'")
            m.add("Discussing order #99", user_id="bob", run_id="session-xyz")
            print("    Added session-level memory for bob/session-xyz")
        except Exception as e:
            print(f"    Multi-level: {e}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("  Demo complete!")
    print("=" * 60)
    print("""
Key takeaways:
  - mem0 auto-extracts structured facts from raw text
  - Memories are scoped per user, agent, or session
  - Vector search enables semantic retrieval
  - Pluggable backends: Qdrant, Chroma, PGVector, Pinecone...
  - Works with OpenAI, Anthropic, Ollama, Groq LLMs

Next steps: set OPENAI_API_KEY and remove the mocks to use real
extraction. See HOW_TO_USE.md for full setup instructions.
""")


if __name__ == "__main__":
    run_demo()
