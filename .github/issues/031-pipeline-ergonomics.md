---
title: "RAGPipeline ergonomics: ingest_many(), query(top_k=...) override, and RAGResponse.query"
labels: ["enhancement", "good first issue"]
---

## Description

Three small quality-of-life gaps in the public pipeline API:

1. **`ingest_many(sources: Iterable[str]) -> int`** — loop over `ingest()`, return the total chunk count. Saves every user from writing the same loop (and pairs with the `DirectoryLoader` issue).
2. **`query(query, *, top_k: int | None = None)`** — per-call override of `config.top_k` without constructing a new pipeline.
3. **`RAGResponse.query: str`** — the response should carry the question it answers, so callers logging or caching responses don't have to thread it through separately.

## Acceptance criteria

- [ ] `ingest_many()` implemented; on failure, the raised `PipelineError` message includes which source failed and how many succeeded before it
- [ ] `query(top_k=)` implemented; `top_k <= 0` raises `PipelineError` (consistent with `RAGConfig` validation)
- [ ] `RAGResponse` gains `query: str` (add it as the **last** field with a default of `""` so positional construction in existing code does not break)
- [ ] Tests for all three in `tests/test_pipeline/test_rag.py`
- [ ] README Quick Start updated to show `ingest_many`; `CHANGELOG.md` updated

## Files to touch

- `ragframework/pipeline/rag.py`
- `ragframework/base.py` — `RAGResponse`
- `tests/test_pipeline/test_rag.py`
- `README.md`

**Estimated effort:** Small (< 2 hours)
