---
title: "InMemoryRetriever raises raw numpy ValueError on embedding dimension mismatch"
labels: ["bug", "good first issue"]
---

## Description

`InMemoryRetriever` performs no validation of vector shape or content:

```python
r.add([Chunk(id="a", content="a", embedding=[1.0, 0.0, 0.0])])
r.add([Chunk(id="b", content="b", embedding=[1.0, 0.0])])   # ValueError from np.array (ragged)
r.retrieve([1.0, 0.0])                                        # ValueError from matrix @ q
```

`FAISSRetriever` already has `_validated_vector()` that checks 1-D, non-empty, finite, non-zero, and enforces a consistent dimension across `add()` and `retrieve()`, raising `RetrieverError` with a clear message. `InMemoryRetriever` should behave the same way.

## Motivation

Dimension mismatches are the most common mistake when swapping embedders (e.g. 384-dim MiniLM vs 1536-dim OpenAI). Users deserve `RetrieverError: Query embedding has dimension 384; expected 1536.` rather than a numpy shape error.

## Acceptance criteria

- [ ] Move `FAISSRetriever._validated_vector` into a shared helper, e.g. `ragframework/utils/vectors.py::validate_vector(values, label) -> np.ndarray`
- [ ] `InMemoryRetriever.add()` validates every chunk vector before mutating state and tracks `self._dimension`
- [ ] `InMemoryRetriever.retrieve()` validates the query vector and its dimension, raising `RetrieverError`
- [ ] `FAISSRetriever` uses the shared helper (behaviour unchanged, its tests still pass)
- [ ] Tests in `tests/test_retriever/test_in_memory.py` for: wrong dimension on add, wrong dimension on query, NaN, zero vector, empty vector
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Fixed`

## Files to touch

- `ragframework/utils/vectors.py` — new
- `ragframework/utils/__init__.py` — export
- `ragframework/retriever/in_memory.py`
- `ragframework/retriever/faiss.py` — replace private static method with the helper
- `tests/test_retriever/test_in_memory.py`

## Resources

- `FAISSRetriever._validated_vector` (`ragframework/retriever/faiss.py` lines 131–144)

**Estimated effort:** Small (< 2 hours)
