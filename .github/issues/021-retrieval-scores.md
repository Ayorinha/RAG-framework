---
title: "Expose similarity scores from retrievers and in RAGResponse"
labels: ["enhancement", "help wanted"]
---

## Description

All three retrievers compute a similarity score and throw it away:

- `InMemoryRetriever.retrieve` — `scores = self._matrix @ q`, only used for ordering
- `FAISSRetriever.retrieve` — `_scores, labels = self._index.search(...)`
- `ChromaRetriever.retrieve` — `include=["documents", "metadatas"]` (omits `"distances"`)

Users cannot filter by a relevance threshold, log retrieval quality, or show confidence in a UI.

## Proposed design

- Add `score: float | None = None` to the `Chunk` dataclass (last field, default `None`, so existing code is unaffected)
- Each retriever sets `score` on the **returned** chunks. Returned chunks should be shallow copies (`dataclasses.replace(chunk, score=s)`) so the stored chunk is not mutated
- Document the scale: cosine similarity in `[-1, 1]`, higher is better. `ChromaRetriever` must convert Chroma's distance — create collections with `metadata={"hnsw:space": "cosine"}` explicitly (Chroma defaults to L2) and return `1 - distance`
- Add `RAGConfig.score_threshold: float | None = None`; `RAGPipeline.query()` drops chunks below it before generation

## Acceptance criteria

- [ ] `Chunk.score` field added and documented
- [ ] All three retrievers populate it; tests assert the top result's score ≈ 1.0 for an identical vector and that the stored chunk's `score` stays `None`
- [ ] `ChromaRetriever` creates collections with an explicit cosine space
- [ ] `score_threshold` implemented in the pipeline with a test
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Added`

## Files to touch

- `ragframework/base.py` — `Chunk`
- `ragframework/retriever/in_memory.py`, `faiss.py`, `chroma.py`
- `ragframework/config.py`, `ragframework/pipeline/rag.py`
- Tests for each

## Resources

- [Chroma distance functions](https://docs.trychroma.com/docs/collections/configure)
- [`dataclasses.replace`](https://docs.python.org/3/library/dataclasses.html#dataclasses.replace)

**Estimated effort:** Medium (half day)
