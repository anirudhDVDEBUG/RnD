# RAG in Zephyr

Retrieval-Augmented Generation (RAG) indexes local documents and augments
LLM context with retrieved chunks. This grounds the model's responses in
real data rather than relying solely on parametric knowledge.

The pipeline: ingest files -> tokenize -> build inverted index -> retrieve top-k -> inject into prompt.
