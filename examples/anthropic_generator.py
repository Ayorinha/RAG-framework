"""Anthropic-backed RAG pipeline example.

Demonstrates a full ingest -> query cycle using AnthropicGenerator for
answer synthesis. Requires the optional Anthropic dependency and an API key.

Run:
    pip install "ragframework[anthropic]"
    set ANTHROPIC_API_KEY=your-key-here   # Windows
    export ANTHROPIC_API_KEY=your-key-here  # macOS/Linux
    python examples/anthropic_generator.py
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ragframework.config import RAGConfig
from ragframework.document.chunkers import FixedSizeChunker
from ragframework.document.loaders import TextFileLoader
from ragframework.embeddings.random_embedder import RandomEmbedder
from ragframework.generator.anthropic import AnthropicGenerator
from ragframework.pipeline.rag import RAGPipeline
from ragframework.retriever.in_memory import InMemoryRetriever

SAMPLE_TEXT = """\
Retrieval-Augmented Generation (RAG) combines document retrieval with language
model generation. A typical pipeline loads documents, splits them into chunks,
embeds those chunks, retrieves the most relevant pieces for a query, and then
asks a generator to produce a grounded answer from the retrieved context.
"""


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        print("ANTHROPIC_API_KEY is not set.")
        print("Install the optional dependency with:")
        print('    pip install "ragframework[anthropic]"')
        print("Then set your API key, for example:")
        print("    export ANTHROPIC_API_KEY=your-key-here")
        raise SystemExit(0)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as handle:
        handle.write(SAMPLE_TEXT)
        tmp_path = handle.name

    print(f"Sample document written to: {tmp_path}\n")

    pipeline = RAGPipeline(
        loader=TextFileLoader(),
        chunker=FixedSizeChunker(chunk_size=200, chunk_overlap=40),
        embedder=RandomEmbedder(dim=64, seed=42),
        retriever=InMemoryRetriever(),
        generator=AnthropicGenerator(model="claude-sonnet-5"),
        config=RAGConfig(top_k=3),
    )

    n_chunks = pipeline.ingest(tmp_path)
    print(f"Ingested {n_chunks} chunks.\n")

    query = "What does a RAG pipeline do?"
    print(f"Query: {query!r}\n")

    response = pipeline.query(query)

    print("Answer:")
    print("-" * 60)
    print(response.answer)
    print("-" * 60)
    print(f"\nSource chunks used: {len(response.source_chunks)}")

    Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
