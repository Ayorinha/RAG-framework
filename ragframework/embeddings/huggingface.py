"""Local embeddings powered by Sentence Transformers."""

from __future__ import annotations

from typing import Any, cast

from ragframework.base import Embedder
from ragframework.exceptions import EmbedderError


class HuggingFaceEmbedder(Embedder):
    """Create embeddings with a local Sentence Transformers model.

    Args:
        model_name: Name or path of the Sentence Transformers model.
        device: Optional inference device, such as ``"cpu"`` or ``"cuda"``.

    Raises:
        ImportError: If the ``huggingface`` optional dependency is not installed.
        EmbedderError: If the model cannot be loaded.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str | None = None,
    ) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "HuggingFace support requires 'ragframework[huggingface]'. "
                "Install it with: pip install ragframework[huggingface]"
            ) from exc

        self.model_name = model_name
        self.device = device
        try:
            self._model: Any = SentenceTransformer(model_name, device=device)
        except Exception as exc:
            raise EmbedderError(f"Could not load embedding model {model_name!r}: {exc}") from exc

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector for each input text, in input order."""
        if not texts:
            return []

        try:
            embeddings = self._model.encode(texts, convert_to_numpy=True)
            return cast(list[list[float]], embeddings.tolist())
        except Exception as exc:
            raise EmbedderError(f"Could not create embeddings: {exc}") from exc
