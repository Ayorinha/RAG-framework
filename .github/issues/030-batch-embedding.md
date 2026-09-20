---
title: "Batch embedding calls in RAGPipeline.ingest()"
labels: ["enhancement", "good first issue"]
---

## Description

`RAGPipeline.ingest()` sends **all** chunk texts to `embedder.embed()` in a single call:

```python
texts = [c.content for c in all_chunks]
embeddings = self.embedder.embed(texts)
```

A 300-page PDF split into 512-char chunks is ~3 000 texts in one request. Hosted embedding APIs reject batches this large (OpenAI caps at 2 048 inputs per request), and local models can run out of memory.

## Acceptance criteria

- [ ] `RAGConfig.embed_batch_size: int = 64` (validated `> 0`)
- [ ] `ingest()` iterates `all_chunks` in batches of that size and concatenates the results; order preserved; `zip(..., strict=True)` check kept
- [ ] A test with a fake embedder that records call sizes, asserting no call exceeds the batch size and the total count is right
- [ ] `RAGConfig` docstring updated; `CHANGELOG.md` updated under `[Unreleased]` → `### Added`

## Files to touch

- `ragframework/config.py`
- `ragframework/pipeline/rag.py` — `ingest()` (lines 96–103)
- `tests/test_pipeline/test_rag.py`, `tests/test_config.py`

## Resources

- [OpenAI embeddings limits](https://platform.openai.com/docs/guides/embeddings) — relevant once #6 lands

**Estimated effort:** Small (< 2 hours)
