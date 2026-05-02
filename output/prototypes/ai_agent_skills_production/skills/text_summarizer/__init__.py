"""Text summarizer skill - produces concise summaries using extractive methods."""

from skills.base import BaseSkill, SkillResult
from skills.registry import registry


@registry.register
class TextSummarizerSkill(BaseSkill):
    name = "text_summarizer"
    description = "Summarize text using extractive sentence scoring"
    version = "1.0.0"

    def validate_input(self, input_data: dict) -> bool:
        return "text" in input_data and len(input_data["text"]) > 0

    def execute(self, input_data: dict) -> SkillResult:
        text = input_data["text"]
        max_sentences = input_data.get("max_sentences", 3)

        # Simple extractive summarization (no ML deps needed)
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

        if not sentences:
            return SkillResult(success=True, data="", metadata={"sentence_count": 0})

        # Score sentences by word frequency
        words = text.lower().split()
        freq = {}
        for w in words:
            w = w.strip(".,!?;:'\"")
            if len(w) > 3:
                freq[w] = freq.get(w, 0) + 1

        scored = []
        for sent in sentences:
            score = sum(freq.get(w.lower().strip(".,!?;:'\""), 0) for w in sent.split())
            scored.append((score, sent))

        scored.sort(reverse=True)
        top = scored[:max_sentences]
        # Preserve original order
        top_sentences = [s for _, s in sorted(top, key=lambda x: sentences.index(x[1]))]
        summary = ". ".join(top_sentences) + "."

        return SkillResult(
            success=True,
            data=summary,
            metadata={
                "original_sentences": len(sentences),
                "summary_sentences": len(top_sentences),
                "compression_ratio": round(len(summary) / len(text), 2),
            },
        )
