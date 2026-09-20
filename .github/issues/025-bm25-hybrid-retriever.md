---
title: "BM25Retriever (lexical) and HybridRetriever — requires passing query text to retrievers"
labels: ["enhancement", "help wanted"]
---

## Description

Dense retrieval alone misses exact matches (error codes, product SKUs, names). Add a lexical `BM25Retriever` and a `HybridRetriever` that fuses dense + lexical results with Reciprocal Rank Fusion.

### The API problem this exposes

`Retriever.retrieve(query_embedding, top_k)` receives only the vector. A lexical retriever needs the **text**. Proposed, backward-compatible change to the ABC:

```python
def retrieve(self, query_embedding: list[float], top_k: int = 5, *, query_text: str | None = None) -> list[Chunk]:
```

`RAGPipeline.query()` always passes `query_text=query`. Existing retrievers ignore it. `BM25Retriever` raises `RetrieverError` if it is `None`.

## Acceptance criteria

- [ ] `Retriever.retrieve` signature extended with keyword-only `query_text`; all built-in retrievers and `RAGPipeline.query()` updated; existing tests pass
- [ ] `BM25Retriever(Retriever)` in `ragframework/retriever/bm25.py` using `rank_bm25` (new `[bm25]` extra, guarded import). Simple whitespace + lowercase tokeniser by default, injectable `tokenizer: Callable[[str], list[str]]`
- [ ] `BM25Retriever.add()` accepts chunks **without** embeddings (document this deviation in the docstring — it is the one retriever where that is legitimate)
- [ ] `HybridRetriever(dense: Retriever, sparse: Retriever, k: int = 60)` in `ragframework/retriever/hybrid.py` implementing RRF; fetches `top_k * 2` from each and returns the fused top_k
- [ ] Tests: BM25 returns an exact-keyword chunk first; hybrid ranks a chunk found by both retrievers above one found by only one
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Added` / `### Changed`

## Files to touch

- `ragframework/base.py`
- `ragframework/pipeline/rag.py`
- `ragframework/retriever/bm25.py`, `ragframework/retriever/hybrid.py` — new
- `ragframework/retriever/__init__.py`, `pyproject.toml`
- `tests/test_retriever/test_bm25.py`, `tests/test_retriever/test_hybrid.py` — new

## Resources

- [rank-bm25](https://pypi.org/project/rank-bm25/)
- [Reciprocal Rank Fusion (Cormack et al., 2009)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)

**Estimated effort:** Large (1-2 days)
