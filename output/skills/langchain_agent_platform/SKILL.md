---
name: langchain_agent_platform
description: |
  Build LLM-powered agents, RAG pipelines, and chain-based workflows using LangChain.
  TRIGGER when: user asks to build with LangChain, create a RAG pipeline, chain LLM calls,
  use LangChain tools/retrievers/embeddings, or orchestrate LLM workflows with langchain.
  DO NOT TRIGGER when: user is building pure LangGraph agent graphs (use langgraph_agent_graphs),
  using a different framework (LlamaIndex, Haystack), or calling LLM APIs directly without LangChain.
---

# LangChain Agent Platform

Build context-aware, reasoning LLM applications with [LangChain](https://github.com/langchain-ai/langchain) — the agent engineering platform for composing models, tools, and retrieval.

## When to use

- "Build a RAG pipeline with LangChain"
- "Create a tool-calling agent using LangChain"
- "Chain multiple LLM calls together with LangChain"
- "Set up document loading and vector search with LangChain"
- "Use LangChain retrievers and embeddings in my app"

## How to use

### 1. Install

```bash
# Core + model provider
pip install langchain langchain-anthropic
# Or with OpenAI:
pip install langchain langchain-openai
# Community integrations:
pip install langchain-community
```

LangChain is modular — install only the provider packages you need.

### 2. Chat Models

All LLM interactions go through chat model classes with a unified interface.

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-20250514")
response = llm.invoke("Explain retrieval-augmented generation.")
print(response.content)
```

### 3. Prompt Templates and Chains (LCEL)

Use LangChain Expression Language (LCEL) to compose chains with the `|` pipe operator.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in {topic}."),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic": "Python", "question": "What are decorators?"})
```

### 4. Tool-Calling Agents

Bind tools to models and let the LLM decide when to call them.

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))  # Use a safe evaluator in production

llm_with_tools = llm.bind_tools([calculator])
result = llm_with_tools.invoke("What is 42 * 17?")
```

For a full agent loop, use the prebuilt react agent:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools=[calculator])
result = agent.invoke({"messages": [{"role": "user", "content": "What is 42 * 17?"}]})
```

### 5. RAG (Retrieval-Augmented Generation)

Load documents, split them, embed into a vector store, and retrieve for context.

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load and split
loader = WebBaseLoader("https://example.com/docs")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# Embed and store
embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on context:\n{context}"),
    ("human", "{question}"),
])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
result = rag_chain.invoke("What does this document say?")
```

### 6. Structured Output

Parse LLM responses into Pydantic models.

```python
from pydantic import BaseModel, Field

class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    rating: int = Field(description="Rating out of 10")
    summary: str = Field(description="Brief summary")

structured_llm = llm.with_structured_output(MovieReview)
review = structured_llm.invoke("Review the movie Inception")
print(review.title, review.rating)
```

### 7. Streaming

```python
for chunk in chain.stream({"topic": "AI", "question": "What is an LLM?"}):
    print(chunk, end="", flush=True)
```

## Key Concepts

| Concept | Description |
|---|---|
| **LCEL** | LangChain Expression Language — compose chains with `\|` pipe |
| **Chat Models** | Unified interface for Anthropic, OpenAI, Google, etc. |
| **Tools** | Functions the LLM can call; use `@tool` decorator |
| **Retrievers** | Fetch relevant documents from vector stores or other sources |
| **Document Loaders** | Ingest from PDF, web, CSV, databases, and 100+ sources |
| **Text Splitters** | Chunk documents for embedding |
| **Output Parsers** | Parse LLM output into structured formats |
| **Callbacks** | Hooks for logging, tracing, and monitoring |

## Project Structure (Monorepo)

- `libs/core/` — `langchain-core`: base abstractions and LCEL
- `libs/langchain/` — `langchain`: chains, agents, retrieval strategies
- `libs/community/` — `langchain-community`: 700+ third-party integrations
- `libs/partners/` — First-party provider packages (anthropic, openai, etc.)

## References

- **Repository**: https://github.com/langchain-ai/langchain
- **Documentation**: https://python.langchain.com/docs/
- **API Reference**: https://python.langchain.com/api_reference/
- **LangSmith (tracing)**: https://docs.smith.langchain.com/
- **LangGraph (agent graphs)**: https://langchain-ai.github.io/langgraph/
