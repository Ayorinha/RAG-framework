---
title: "Re-ingesting the same source duplicates chunks in InMemoryRetriever and FAISSRetriever"
labels: ["bug", "help wanted"]
---

## Description

`RAGPipeline.ingest(path)` called twice on the same file doubles the index:

```python
pipe.ingest("doc.txt")   # 12 chunks
pipe.ingest("doc.txt")   # 12 chunks
len(pipe.retriever)      # 24  — same 12 chunk ids stored twice
```

`ChromaRetriever.add()` uses `upsert`, so it is idempotent on chunk id. `InMemoryRetriever` and `FAISSRetriever` blindly append. The `Retriever.add` docstring in `base.py` does not say which behaviour is correct.

## Motivation

Re-running an ingestion script (the normal workflow while iterating) silently pollutes results: the same chunk appears multiple times in `top_k`, crowding out genuinely different context. Chunk ids are already deterministic (`<doc_id>:<index>`, where `doc_id` is a hash of the source path), so idempotency is achievable.

## Acceptance criteria

- [ ] `Retriever.add` docstring in `ragframework/base.py` defines the contract: adding a chunk whose `id` already exists **replaces** it (upsert semantics)
- [ ] `InMemoryRetriever.add()` replaces existing rows by id (maintain an `id -> row index` dict)
- [ ] `FAISSRetriever.add()` handles duplicates. `IndexHNSWFlat` does not support removal, so pick and document one approach: (a) keep an `id -> label` map and tombstone superseded labels (filtered out in `retrieve`, over-fetching to compensate), or (b) wrap the index in `faiss.IndexIDMap2` if it supports the chosen index type. Explain the trade-off in the docstring.
- [ ] Tests for all three retrievers: add the same chunk twice → `len()` unchanged, retrieval returns it once, and the **new** content/embedding wins
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Fixed`

## Files to touch

- `ragframework/base.py` — `Retriever.add` docstring
- `ragframework/retriever/in_memory.py`
- `ragframework/retriever/faiss.py`
- `tests/test_retriever/test_in_memory.py`, `tests/test_retriever/test_faiss.py`, `tests/test_retriever/test_chroma.py`

## Resources

- [FAISS: removing vectors](https://github.com/facebookresearch/faiss/wiki/Special-operations-on-indexes#removing-elements-from-an-index)
- `ChromaRetriever.add` for the upsert reference behaviour

**Estimated effort:** Medium (half day)
