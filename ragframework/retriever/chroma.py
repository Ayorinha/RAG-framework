"""ChromaDB-backed retriever."""

from __future__ import annotations

from typing import Any

from ragframework.base import Chunk, Retriever
from ragframework.exceptions import RetrieverError


class ChromaRetriever(Retriever):
    """Retriever backed by ChromaDB.

    Supports both ephemeral in-memory storage and persistent on-disk storage.

    Args:
        collection_name: Name of the ChromaDB collection.
        persist_directory: Directory for persistent storage. If ``None``,
            ChromaDB uses an ephemeral in-memory client.
    """

    _EMPTY_METADATA_KEY = "_ragframework_empty_metadata"

    def __init__(
        self,
        collection_name: str = "ragframework",
        persist_directory: str | None = None,
    ) -> None:
        try:
            import chromadb
        except ImportError as exc:
            raise ImportError(
                "ChromaDB support requires 'ragframework[chromadb]'. "
                "Install it with: pip install ragframework[chromadb]"
            ) from exc

        try:
            if persist_directory is None:
                self._client = chromadb.Client()
            else:
                self._client = chromadb.PersistentClient(
                    path=persist_directory,
                )

            self._collection = self._client.get_or_create_collection(
                name=collection_name,
            )
        except Exception as exc:
            raise RetrieverError(f"Could not initialize ChromaDB: {exc}") from exc

    def add(self, chunks: list[Chunk]) -> None:
        """Add embedded chunks to the ChromaDB collection."""
        if not chunks:
            return

        for chunk in chunks:
            if chunk.embedding is None:
                raise RetrieverError(
                    f"Chunk '{chunk.id}' has no embedding. "
                    "Embed chunks before adding them to the retriever."
                )

        try:
            self._collection.upsert(
                ids=[chunk.id for chunk in chunks],
                embeddings=[chunk.embedding for chunk in chunks],
                documents=[chunk.content for chunk in chunks],
                metadatas=[self._metadata(chunk) for chunk in chunks],
            )
        except Exception as exc:
            raise RetrieverError(f"Failed to add chunks to ChromaDB: {exc}") from exc

    def retrieve(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[Chunk]:
        """Return the most similar chunks for a query embedding."""
        if top_k <= 0:
            return []

        try:
            result = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas"],
            )
        except Exception as exc:
            raise RetrieverError(f"Failed to query ChromaDB: {exc}") from exc

        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        chunks: list[Chunk] = []

        for chunk_id, document, metadata in zip(
            ids,
            documents,
            metadatas,
            strict=True,
        ):
            metadata = metadata or {}

            if metadata.get(self._EMPTY_METADATA_KEY):
                metadata = {}

            chunks.append(
                Chunk(
                    id=chunk_id,
                    content=document or "",
                    metadata=metadata,
                )
            )

        return chunks

    @classmethod
    def _metadata(cls, chunk: Chunk) -> dict[str, Any]:
        """Return Chroma-compatible metadata for a chunk."""
        metadata: dict[str, Any] = {}

        for key, value in chunk.metadata.items():
            if isinstance(value, (str, int, float, bool)):
                metadata[key] = value
            else:
                metadata[key] = str(value)

        # ChromaDB requires metadata to be a non-empty dictionary.
        if not metadata:
            metadata[cls._EMPTY_METADATA_KEY] = True

        return metadata

    def __len__(self) -> int:
        """Return the number of chunks stored in the collection."""
        return self._collection.count()
