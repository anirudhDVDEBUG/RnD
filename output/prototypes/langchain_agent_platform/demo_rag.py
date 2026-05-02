"""Demo: RAG pipeline — load, split, embed, retrieve, answer."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from mock_llm import MockChatModel, MockEmbeddings

# Try FAISS, fall back to simple in-memory store
try:
    from langchain_community.vectorstores import FAISS
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False


# Sample documents (simulating loaded web pages)
SAMPLE_DOCS = [
    Document(
        page_content=(
            "LangChain is an open-source agent engineering platform that helps developers "
            "build applications powered by large language models. It provides composable "
            "abstractions for chains, agents, retrieval, and tool use."
        ),
        metadata={"source": "langchain_overview"},
    ),
    Document(
        page_content=(
            "LCEL (LangChain Expression Language) allows developers to compose chains "
            "using the pipe operator. Each component implements the Runnable interface "
            "with invoke, stream, and batch methods."
        ),
        metadata={"source": "lcel_docs"},
    ),
    Document(
        page_content=(
            "RAG (Retrieval-Augmented Generation) combines document retrieval with LLM "
            "generation. Documents are split into chunks, embedded into vectors, stored "
            "in a vector database, and retrieved at query time for context."
        ),
        metadata={"source": "rag_guide"},
    ),
    Document(
        page_content=(
            "LangChain supports 700+ integrations including vector stores like FAISS, "
            "Chroma, and Pinecone; document loaders for PDF, web, and databases; and "
            "model providers like Anthropic, OpenAI, and Google."
        ),
        metadata={"source": "integrations"},
    ),
]


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def main():
    print("=== RAG Pipeline Demo ===")

    # Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(SAMPLE_DOCS)

    # Create embeddings and vector store
    embeddings = MockEmbeddings()

    if HAS_FAISS:
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    else:
        # Minimal fallback without FAISS
        print("(FAISS not available, using simple keyword matching)")

        class SimpleRetriever:
            def invoke(self, query):
                # Return docs containing query keywords
                query_lower = query.lower()
                matches = [d for d in chunks if any(
                    w in d.page_content.lower()
                    for w in query_lower.split()
                )]
                return matches[:2] if matches else chunks[:2]

        retriever = SimpleRetriever()

    print(f"Indexed {len(chunks)} documents into vector store")

    # Build RAG chain
    llm = MockChatModel()

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

    # Query
    question = "What is LangChain?"
    result = rag_chain.invoke(question)
    print(f"Q: {question}")
    print(f"A: {result}")
    print()


if __name__ == "__main__":
    main()
