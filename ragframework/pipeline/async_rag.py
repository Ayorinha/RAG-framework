"""Async wrapper for the RAG pipeline."""

from __future__ import annotations

import asyncio

from ragframework.base import (
    DocumentLoader,
    Embedder,
    Generator,
    RAGResponse,
    Retriever,
    TextChunker,
)
from ragframework.config import RAGConfig
from ragframework.pipeline.rag import RAGPipeline


class AsyncRAGPipeline:
    """Async interface for RAGPipeline using asyncio.to_thread()."""

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: TextChunker,
        embedder: Embedder,
        retriever: Retriever,
        generator: Generator,
        config: RAGConfig | None = None,
    ) -> None:
        self._pipeline = RAGPipeline(
            loader=loader,
            chunker=chunker,
            embedder=embedder,
            retriever=retriever,
            generator=generator,
            config=config,
        )

    @classmethod
    def from_pipeline(cls, pipeline: RAGPipeline) -> AsyncRAGPipeline:
        """Create an async wrapper from an existing RAGPipeline."""
        instance = cls.__new__(cls)
        instance._pipeline = pipeline
        return instance

    @property
    def config(self) -> RAGConfig:
        """Return the configuration of the wrapped RAG pipeline."""
        return self._pipeline.config

    async def async_ingest(self, source: str) -> int:
        """Asynchronously ingest a document."""
        return await asyncio.to_thread(self._pipeline.ingest, source)

    async def async_query(self, query: str) -> RAGResponse:
        """Asynchronously query the RAG pipeline."""
        return await asyncio.to_thread(self._pipeline.query, query)
