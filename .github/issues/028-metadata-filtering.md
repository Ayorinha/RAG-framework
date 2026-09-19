---
title: "Metadata filtering in Retriever.retrieve()"
labels: ["enhancement", "help wanted"]
---

## Description

Allow callers to restrict retrieval to chunks whose metadata matches a filter:

```python
pipeline.query("refund policy", filter={"source": "policies.pdf"})
retriever.retrieve(q, top_k=5, filter={"page_number": 3})
```

## Motivation

Multi-tenant apps, per-document Q&A ("only answer from this file") and date-scoped search all need this. `ChromaRetriever` already stores metadata and Chroma supports `where=`, but the framework API has no way to reach it.

## Proposed design

- `Retriever.retrieve(..., *, filter: Mapping[str, Any] | None = None)` — keyword-only, default `None`
- v1 semantics: exact-match AND across keys. Document that richer operators are out of scope for now
- `InMemoryRetriever` / `FAISSRetriever`: post-filter. Because FAISS returns only `top_k` labels, over-fetch (`top_k * 4`, capped at `len(self)`) and keep the first `top_k` matches; document the limitation
- `ChromaRetriever`: translate to a Chroma `where` clause. **Blocker:** `ChromaRetriever._metadata()` currently serialises all user metadata into a single JSON string under `_ragframework_metadata`, which Chroma cannot filter on. Store scalar keys (`str/int/float/bool`) as top-level Chroma metadata as well, keeping the JSON blob for lossless restore
- `RAGPipeline.query(query, *, filter=None)` passes it through

## Acceptance criteria

- [ ] ABC, all three retrievers, and pipeline updated; `filter=None` behaviour unchanged
- [ ] Chroma metadata storage change is backward compatible with collections written by the current code (`_restore_metadata` still works)
- [ ] Tests per retriever: filter narrows results; filter with no matches returns `[]`; non-scalar filter values raise `RetrieverError`
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Added`

## Files to touch

- `ragframework/base.py`, `ragframework/pipeline/rag.py`
- `ragframework/retriever/in_memory.py`, `faiss.py`, `chroma.py`
- Tests for each

## Resources

- [Chroma `where` filters](https://docs.trychroma.com/docs/querying-collections/metadata-filtering)

**Estimated effort:** Medium (half day)
