"""Vision grounding: screenshot capture and visual embedding for memory anchoring."""

import hashlib
import os
import time
from dataclasses import dataclass


@dataclass
class ScreenCapture:
    path: str
    timestamp: float
    embedding_hash: str  # simulated visual embedding


class VisionGrounding:
    """Captures screenshots and produces visual embeddings to ground agent memory."""

    def __init__(
        self,
        capture_dir: str = "./memory/vision",
        capture_interval: str = "on_action",
        embedding_model: str = "clip",
    ):
        self.capture_dir = capture_dir
        self.capture_interval = capture_interval
        self.embedding_model = embedding_model
        self._captures: list[ScreenCapture] = []
        os.makedirs(capture_dir, exist_ok=True)

    def capture(self, context: str = "") -> ScreenCapture:
        """Simulate a screenshot capture (real impl would use pyautogui/PIL)."""
        ts = time.time()
        # Simulate a visual embedding hash based on context
        embed_hash = hashlib.sha256(f"{context}:{ts}".encode()).hexdigest()[:16]
        filename = f"capture_{len(self._captures):04d}_{embed_hash}.txt"
        path = os.path.join(self.capture_dir, filename)

        # Write a placeholder representing the screenshot metadata
        with open(path, "w") as f:
            f.write(f"[Screenshot Capture]\n")
            f.write(f"Timestamp: {ts}\n")
            f.write(f"Context: {context}\n")
            f.write(f"Embedding ({self.embedding_model}): {embed_hash}\n")

        cap = ScreenCapture(path=path, timestamp=ts, embedding_hash=embed_hash)
        self._captures.append(cap)
        return cap

    def find_similar(self, query_context: str, top_k: int = 3) -> list[ScreenCapture]:
        """Retrieve visually similar past captures (simulated via hash prefix matching)."""
        query_hash = hashlib.sha256(query_context.encode()).hexdigest()[:4]
        scored = []
        for cap in self._captures:
            # Simple similarity: shared prefix length
            shared = sum(1 for a, b in zip(query_hash, cap.embedding_hash) if a == b)
            scored.append((shared, cap))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [cap for _, cap in scored[:top_k]]

    @property
    def capture_count(self) -> int:
        return len(self._captures)
