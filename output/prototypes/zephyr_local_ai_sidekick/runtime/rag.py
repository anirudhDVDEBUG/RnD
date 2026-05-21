"""Minimal RAG pipeline — index local text, retrieve relevant chunks."""

import os
import re
from collections import defaultdict


class RAGPipeline:
    """Keyword-based retrieval over local documents (no vector DB needed)."""

    def __init__(self):
        self.documents: list[dict] = []  # {"id", "source", "text"}
        self.index: dict[str, list[int]] = defaultdict(list)  # token -> doc ids

    # ------------------------------------------------------------------
    def ingest_directory(self, path: str) -> int:
        """Recursively ingest .txt and .md files from *path*."""
        count = 0
        for root, _dirs, files in os.walk(path):
            for fname in files:
                if fname.endswith((".txt", ".md")):
                    fpath = os.path.join(root, fname)
                    with open(fpath, "r", errors="replace") as f:
                        text = f.read()
                    self._add_document(fpath, text)
                    count += 1
        return count

    def ingest_text(self, source: str, text: str) -> None:
        self._add_document(source, text)

    # ------------------------------------------------------------------
    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        tokens = self._tokenize(query)
        scores: dict[int, float] = defaultdict(float)
        for tok in tokens:
            for doc_id in self.index.get(tok, []):
                scores[doc_id] += 1.0
        ranked = sorted(scores, key=scores.get, reverse=True)[:top_k]
        return [self.documents[i] for i in ranked]

    # ------------------------------------------------------------------
    def _add_document(self, source: str, text: str) -> None:
        doc_id = len(self.documents)
        self.documents.append({"id": doc_id, "source": source, "text": text[:500]})
        for tok in set(self._tokenize(text)):
            self.index[tok].append(doc_id)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [w.lower() for w in re.findall(r"\w+", text) if len(w) > 2]
