---
title: "InMemoryRetriever.add() re-normalises the entire matrix on every call (O(N²))"
labels: ["bug", "good first issue"]
---

## Description

Every call to `InMemoryRetriever.add()` rebuilds `self._matrix` from **all** stored chunks:

```python
self._chunks.extend(chunks)
vectors = np.array([c.embedding for c in self._chunks], dtype=np.float32)  # all N, every time
```

Ingesting N documents one at a time is therefore O(N²). Measured locally: 2 000 single-chunk `add()` calls with 64-dim vectors take ~2 s; 20 000 would take minutes.

## Motivation

`RAGPipeline.ingest()` is called once per source, so per-file ingestion of a folder hits exactly this path. Incremental ingestion should be linear.

## Acceptance criteria

- [ ] `add()` normalises only the **new** vectors and appends them (`np.vstack` onto the existing matrix, or keep a list of row blocks and concatenate lazily on first `retrieve()` after a change)
- [ ] Retrieval results are identical before/after the change (existing tests pass)
- [ ] A test that adds chunks in several batches and asserts `len(r)` and the top result match a single-batch add
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Fixed`

## Files to touch

- `ragframework/retriever/in_memory.py` — `add()` (lines 25–36)
- `tests/test_retriever/test_in_memory.py`

## Resources

- [`numpy.vstack`](https://numpy.org/doc/stable/reference/generated/numpy.vstack.html)

**Estimated effort:** Small (< 2 hours)
