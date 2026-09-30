from __future__ import annotations

from typing import Sequence

import numpy as np

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def cosine_similarity(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    """Return the cosine similarity between two embedding vectors."""
    a = np.asarray(vector_a, dtype=np.float64)
    b = np.asarray(vector_b, dtype=np.float64)

    if a.size == 0 or b.size == 0:
        return 0.0

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))


class LocalEmbeddingModel:
    """Wrap a local sentence-transformers model and normalize vectors."""

    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL):
        self.model_name = model_name
        self._model = None

    def _ensure_loaded(self):
        if self._model is not None:
            return

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - dependency error path
            raise RuntimeError(
                "sentence-transformers is not installed. Install project requirements to enable local embeddings."
            ) from exc

        self._model = SentenceTransformer(self.model_name)

    def encode(self, texts: str | list[str]) -> np.ndarray:
        self._ensure_loaded()

        inputs = [texts] if isinstance(texts, str) else list(texts)
        embeddings = self._model.encode(
            inputs,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(embeddings, dtype=np.float64)
