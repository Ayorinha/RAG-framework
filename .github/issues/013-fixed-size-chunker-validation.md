---
title: "FixedSizeChunker accepts chunk_size <= 0 and negative chunk_overlap"
labels: ["bug", "good first issue"]
---

## Description

`FixedSizeChunker.__init__` only checks `chunk_overlap >= chunk_size`. Invalid values slip through and produce garbage:

```python
FixedSizeChunker(chunk_size=0, chunk_overlap=-1).chunk(Document("d", "hello"))
# -> 5 empty chunks

FixedSizeChunker(chunk_size=10, chunk_overlap=-5).chunk(Document("d", "0123456789ABCDEFGHIJKLMNOPQRS"))
# -> ['0123456789', 'FGHIJKLMNO']   characters A–E and P–S silently dropped
```

`RecursiveChunker` and `RAGConfig` already validate all three conditions; `FixedSizeChunker` and `SentenceChunker` do not.

## Motivation

Negative overlap silently loses text from the index — the worst kind of bug for a retrieval system, because nothing fails and recall just degrades.

## Acceptance criteria

- [ ] `FixedSizeChunker` raises `ValueError` for `chunk_size <= 0` or `chunk_overlap < 0` (same messages as `RecursiveChunker`)
- [ ] `SentenceChunker` raises `ValueError` for `max_sentences <= 0` or `overlap_sentences < 0`
- [ ] `RecursiveChunker.from_config(config)` added, matching the classmethod `FixedSizeChunker` already has
- [ ] Parametrised tests in `tests/test_document/test_chunkers.py` covering each invalid value
- [ ] `CHANGELOG.md` updated under `[Unreleased]` → `### Fixed`

## Files to touch

- `ragframework/document/chunkers.py` — `FixedSizeChunker.__init__` (line 21), `SentenceChunker.__init__` (line 65)
- `tests/test_document/test_chunkers.py`

## Resources

- `RecursiveChunker.__init__` (lines 116–121) for the validation to copy
- `RAGConfig.__post_init__` in `ragframework/config.py`

**Estimated effort:** Small (< 2 hours)
