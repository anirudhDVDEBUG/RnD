# How to Use

## Install

```bash
cd langchain_agent_platform
pip install -r requirements.txt
```

Dependencies: `langchain`, `langchain-core`, `langchain-community`, `faiss-cpu`, `pydantic`.

No API keys needed — the demo uses a mock LLM that simulates responses locally.

## As a Claude Skill

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/langchain_agent_platform
cp SKILL.md ~/.claude/skills/langchain_agent_platform/SKILL.md
```

**Trigger phrases that activate it:**
- "Build a RAG pipeline with LangChain"
- "Create a tool-calling agent using LangChain"
- "Chain multiple LLM calls together with LangChain"
- "Set up document loading and vector search with LangChain"
- "Use LangChain retrievers and embeddings in my app"

## Run the Demo

```bash
bash run.sh
```

No external services, no API keys, no Docker. Pure Python with mock LLM.

## First 60 Seconds

```bash
# 1. Clone and install
git clone <this-repo> && cd langchain_agent_platform
pip install -r requirements.txt

# 2. Run end-to-end demo
bash run.sh

# 3. See output for all four patterns:
#    - LCEL chain (prompt | llm | parser)
#    - Tool-calling agent (calculator)
#    - RAG pipeline (FAISS vector search)
#    - Structured output (Pydantic model)
```

## Switching to a Real LLM

Replace `MockChatModel` in any demo file with a real provider:

```python
# Instead of:
from mock_llm import MockChatModel
llm = MockChatModel()

# Use:
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-20250514")
# Requires: export ANTHROPIC_API_KEY=sk-...
```

All chain/agent/RAG logic stays identical — only the model swap is needed.
