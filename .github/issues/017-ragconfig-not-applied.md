---
title: "RAGConfig.chunk_size / chunk_overlap / embedding_dim are silently ignored by RAGPipeline"
labels: ["bug", "help wanted"]
---

## Description

`RAGPipeline` reads exactly one field from its config — `top_k`. The other three are dead:

```python
pipe = RAGPipeline(
    chunker=FixedSizeChunker(),            # chunk_size=512
    embedder=RandomEmbedder(dim=16),
    config=RAGConfig(chunk_size=20, chunk_overlap=5, embedding_dim=8),
    ...
)
pipe.chunker.chunk_size   # 512 — config ignored, no warning
pipe.embedder.dim         # 16  — embedding_dim=8 never checked
```

The `RAGConfig` docstring says `embedding_dim` "must match the Embedder in use", but nothing verifies it. Only `FixedSizeChunker.from_config()` consumes the chunk fields, and it must be called by hand.

## Motivation

Users reading the README's `config=RAGConfig(top_k=5)` example reasonably assume the other fields work the same way. A config object that looks authoritative but isn't is a trap.

## Proposed resolution

1. **Enforce `embedding_dim`.** In `ingest()` and `query()`, after the first `embed()` call, compare `len(vector)` to `config.embedding_dim` and raise `PipelineError("Embedder produced 16-dim vectors but RAGConfig.embedding_dim is 8")`. Change the default to `embedding_dim: int | None = None` so the check is opt-in and existing users are not broken.
2. **Make the chunk fields usable.** Add `RAGPipeline.from_config(config, *, loader, embedder, retriever, generator, chunker_cls=FixedSizeChunker)` classmethod that builds the chunker via `chunker_cls.from_config(config)` (depends on `RecursiveChunker.from_config` from #25).
3. **Document** in the `RAGConfig` docstring which fields the pipeline enforces vs. which are consumed only by `from_config` helpers.

## Acceptance criteria

- [ ] `embedding_dim` mismatch raises `PipelineError` with both numbers in the message; `None` disables the check
- [ ] `RAGPipeline.from_config(...)` exists and is covered by a test
- [ ] `RAGConfig` docstring updated; README Quick Start mentions `from_config`
- [ ] Existing tests pass unchanged (default `RAGConfig()` must still work with `RandomEmbedder(dim=16)` in `tests/`) — hence the `None` default
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Fixed` / `### Changed`

## Files to touch

- `ragframework/config.py`
- `ragframework/pipeline/rag.py`
- `tests/test_pipeline/test_rag.py`, `tests/test_config.py`
- `README.md`

**Estimated effort:** Medium (half day)
