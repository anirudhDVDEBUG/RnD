"""Stage 6: Mode B research — on-demand dossier + slides + Q&A."""
from .corpus_builder import build_corpus
from .deck_builder import build_slides_and_notes
from .qa_predictor import predict as predict_qa
from .synthesizer import synthesize
from .topic_expander import expand

__all__ = [
    "build_corpus",
    "build_slides_and_notes",
    "predict_qa",
    "synthesize",
    "expand",
]
