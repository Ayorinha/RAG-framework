---
title: "InMemoryRetriever returns every chunk when top_k <= 0"
labels: ["bug", "good first issue"]
---

## Description

`InMemoryRetriever.retrieve()` mishandles non-positive `top_k`. With 5 indexed chunks:

```python
r.retrieve(q, top_k=0)   # returns 5 chunks
r.retrieve(q, top_k=-1)  # returns 4 chunks
```

Cause: `k = min(top_k, len(self._chunks))` gives `k = 0`, and `np.argpartition(scores, -0)[-0:]` is `[0:]` — the whole array. `FAISSRetriever` and `ChromaRetriever` both return `[]` for `top_k <= 0`, so the three built-in retrievers disagree.

## Motivation

Retrievers must behave identically for the same inputs so users can swap them freely. Returning the entire corpus for `top_k=0` can also silently blow up a prompt sent to an LLM generator.

## Acceptance criteria

- [ ] `InMemoryRetriever.retrieve()` returns `[]` when `top_k <= 0`
- [ ] Non-integer / bool `top_k` raises `RetrieverError` (mirror `FAISSRetriever.retrieve`)
- [ ] Regression tests in `tests/test_retriever/test_in_memory.py` for `top_k` in `(0, -1, True)`
- [ ] `Retriever.retrieve` docstring in `ragframework/base.py` states the contract: non-positive `top_k` → empty list
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Fixed`

## Files to touch

- `ragframework/retriever/in_memory.py` — `retrieve()` (lines 38–48)
- `ragframework/base.py` — `Retriever.retrieve` docstring
- `tests/test_retriever/test_in_memory.py`

## Resources

- `FAISSRetriever.retrieve` in `ragframework/retriever/faiss.py` for the reference behaviour
- `test_non_positive_top_k_returns_empty` in `tests/test_retriever/test_chroma.py`

**Estimated effort:** Small (< 2 hours)
